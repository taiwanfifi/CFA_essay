"""
RAG Agent Pragmatist - 基于 LangGraph 的多轮检索 Agent
适配 thelma2 数据格式
"""
import os
import json
import itertools
from typing import List, Dict, Any, Set, TypedDict

from dotenv import load_dotenv
load_dotenv()

from tqdm import tqdm

# LangChain / LangGraph
from langchain_core.documents import Document
from langchain_milvus import Milvus
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

from data_loader import load_thelma2_dataset

print("--- RAG Agent Pragmatist (LangGraph Multi-turn Retrieval) ---")

# =========================
# 配置
# =========================
OUTPUT_FILE = "./rag_agent_pragmatist_results.json"
COLLECTION_NAME = "rag_agent_pragmatist_collection"
DB_URI = "./rag_agent_pragmatist_milvus.db"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定環境變數 OPENAI_API_KEY")

LLM_MODEL = os.getenv("OPENAI_LLM", "gpt-4o-mini")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING", "text-embedding-3-large")

RETRIEVER_K = 8
AGENT_MAX_TURNS = 8
TOP_K_RETURN = 5

print(f"LLM: {LLM_MODEL}")
print(f"Embedding: {EMBED_MODEL}")
print(f"Milvus DB: {DB_URI} / {COLLECTION_NAME}\n")


# =========================
# Agent 状态和节点
# =========================
class GraphState(TypedDict):
    original_question: str
    question: str
    question_history: List[str]
    rewritten_queries: List[str]
    hypotheses: List[str]
    current_hypothesis: str
    assessment: str
    cumulative_facts: List[str]
    final_summary: str
    newly_retrieved_docs: List[Document]
    cumulative_retrieved_docs: List[Document]
    all_retrieved_doc_ids: Set[str]
    has_new_info: bool
    turn_count: int
    plan: List[str]


class SimplePlan(BaseModel):
    plan: List[str] = Field(description="2-3 concrete sub-steps.")


class SimpleHypotheses(BaseModel):
    hypotheses: List[str] = Field(description="2-3 distinct hypotheses.")


class ExtractedFacts(BaseModel):
    facts: List[str] = Field(description="key facts")


class RewrittenQueries(BaseModel):
    rewritten_queries: List[str] = Field(description="1-3 search queries")


# LLMs
llm_json = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=OPENAI_API_KEY)
llm_text = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=OPENAI_API_KEY)

RETRIEVER = None  # type: ignore


def hypothesize_node(state: GraphState):
    parser = JsonOutputParser(pydantic_object=SimpleHypotheses)
    prompt = PromptTemplate.from_template(
        "分析用户问题并生成 2-3 个不同的假设。\n"
        "问题: {original_question}\n"
        "{format_instructions}"
    )
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm_json
    try:
        raw = chain.invoke({"original_question": state["original_question"]})
        data = raw if isinstance(raw, dict) else json.loads(raw.content)
        out = SimpleHypotheses.model_validate(data)
        state["hypotheses"] = out.hypotheses
        state["current_hypothesis"] = out.hypotheses[0]
    except Exception:
        state["hypotheses"] = [state["original_question"]]
        state["current_hypothesis"] = state["original_question"]
    return state


def plan_node(state: GraphState):
    parser = JsonOutputParser(pydantic_object=SimplePlan)
    prompt = PromptTemplate.from_template(
        "创建 2-3 个具体的子步骤来回答问题。\n"
        "假设: {current_hypothesis}\n"
        "{format_instructions}"
    )
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm_json
    try:
        raw = chain.invoke({"current_hypothesis": state["current_hypothesis"]})
        data = raw if isinstance(raw, dict) else json.loads(raw.content)
        out = SimplePlan.model_validate(data)
        state["plan"] = out.plan
    except Exception:
        state["plan"] = [state["current_hypothesis"]]
    return state


def execute_plan_node(state: GraphState):
    if not state["plan"]:
        state["question"] = ""
        return state
    nxt = state["plan"].pop(0)
    state["question"] = nxt
    return state


def rewrite_query_node(state: GraphState):
    if not state["question"]:
        state["rewritten_queries"] = []
        return state
    parser = JsonOutputParser(pydantic_object=RewrittenQueries)
    prompt = PromptTemplate.from_template(
        "将以下内容改写为 1-3 个不同的检索查询。\n"
        "原始: {q}\n"
        "{format_instructions}"
    )
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm_json
    try:
        raw = chain.invoke({"q": state["question"]})
        data = raw if isinstance(raw, dict) else json.loads(raw.content)
        out = RewrittenQueries.model_validate(data)
        qs = [s for s in out.rewritten_queries if isinstance(s, str) and s.strip()]
        state["rewritten_queries"] = qs or [state["question"]]
    except Exception:
        state["rewritten_queries"] = [state["question"]]
    return state


def retrieve_node(state: GraphState):
    state["turn_count"] += 1
    queries = state.get("rewritten_queries", [])
    if not queries:
        state["newly_retrieved_docs"] = []
        state["has_new_info"] = False
        return state

    batch_lists = RETRIEVER.batch(queries)
    merged = list(itertools.chain.from_iterable(batch_lists))

    seen = state["all_retrieved_doc_ids"]
    truly_new = []
    for d in merged:
        did = d.metadata.get("doc_id")
        if did and did not in seen:
            truly_new.append(d)
            seen.add(did)

    state["newly_retrieved_docs"] = truly_new
    state["cumulative_retrieved_docs"].extend(truly_new)
    state["has_new_info"] = len(truly_new) > 0
    return state


def extract_facts_node(state: GraphState):
    if not state["newly_retrieved_docs"]:
        return state
    parser = JsonOutputParser(pydantic_object=ExtractedFacts)
    prompt = PromptTemplate.from_template(
        "从以下文档中提取有助于回答原始问题的关键事实。\n"
        "原始问题: {oq}\n"
        "子问题: {sq}\n"
        "文档:\n{docs}\n"
        "{format_instructions}"
    )
    docs_txt = "\n\n".join(
        f"[doc_id={d.metadata.get('doc_id')}] {d.page_content}" for d in state["newly_retrieved_docs"]
    )
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm_json
    try:
        raw = chain.invoke({"oq": state["original_question"], "sq": state["question"], "docs": docs_txt})
        data = raw if isinstance(raw, dict) else json.loads(raw.content)
        out = ExtractedFacts.model_validate(data)
        if out.facts:
            state["cumulative_facts"].extend(out.facts)
            state["cumulative_facts"] = list(dict.fromkeys(state["cumulative_facts"]))
    except Exception:
        pass
    return state


def grade_facts_node(state: GraphState):
    distinct_doc_ids = {d.metadata.get("doc_id") for d in state.get("cumulative_retrieved_docs", []) if d.metadata.get("doc_id")}
    has_two_docs = len(distinct_doc_ids) >= 2
    min_turns_done = state.get("turn_count", 0) >= 2
    stop_now = (has_two_docs and min_turns_done) or (state.get("turn_count", 0) >= AGENT_MAX_TURNS) or (not state.get("has_new_info", True))
    state["assessment"] = "yes" if stop_now else "no"
    return state


def decide_to_continue(state: GraphState):
    return "generate_summary" if state.get("assessment") == "yes" else "continue"


def generate_summary_node(state: GraphState):
    if not state["cumulative_facts"]:
        state["final_summary"] = "未找到足够的事实。"
        return state
    prompt = PromptTemplate.from_template(
        "使用以下事实撰写简洁的答案。\n"
        "问题: {q}\n事实:\n- {facts}\n\n答案:"
    )
    chain = prompt | llm_text | StrOutputParser()
    facts_str = "\n- ".join(state["cumulative_facts"])
    state["final_summary"] = chain.invoke({"q": state["original_question"], "facts": facts_str})
    return state


# 构建工作流
workflow = StateGraph(GraphState)
workflow.add_node("hypothesize", hypothesize_node)
workflow.add_node("plan", plan_node)
workflow.add_node("execute_plan", execute_plan_node)
workflow.add_node("rewrite_query", rewrite_query_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("extract_facts", extract_facts_node)
workflow.add_node("grade_facts", grade_facts_node)
workflow.add_node("generate_summary", generate_summary_node)

workflow.set_entry_point("hypothesize")
workflow.add_edge("hypothesize", "plan")
workflow.add_edge("plan", "execute_plan")
workflow.add_edge("execute_plan", "rewrite_query")
workflow.add_edge("rewrite_query", "retrieve")
workflow.add_edge("retrieve", "extract_facts")
workflow.add_edge("extract_facts", "grade_facts")
workflow.add_conditional_edges("grade_facts", decide_to_continue, {
    "generate_summary": "generate_summary",
    "continue": "plan"
})
workflow.add_edge("generate_summary", END)
agent = workflow.compile()


# =========================
# 执行函数
# =========================
def run_agent_once(question: str) -> Dict[str, Any]:
    """运行一次 Agent，返回最终状态和 top-k 检索文档"""
    init = {
        "original_question": question,
        "question": "",
        "question_history": [],
        "rewritten_queries": [],
        "hypotheses": [],
        "current_hypothesis": "",
        "assessment": "",
        "cumulative_facts": [],
        "final_summary": "",
        "newly_retrieved_docs": [],
        "cumulative_retrieved_docs": [],
        "all_retrieved_doc_ids": set(),
        "has_new_info": True,
        "turn_count": 0,
        "plan": [],
    }
    final_state = agent.invoke(init, {"recursion_limit": 50})
    
    # 按首次检索顺序取前 K
    uniq: Dict[str, Document] = {}
    for d in final_state.get("cumulative_retrieved_docs", []):
        did = d.metadata.get("doc_id")
        if did and did not in uniq:
            uniq[did] = d
    top_docs = list(uniq.values())[:TOP_K_RETURN]
    
    out_bundle = [
        {"page_content": d.page_content, "metadata": {"doc_id": d.metadata.get("doc_id")}}
        for d in top_docs
    ]
    return {"state": final_state, "docs": out_bundle}


def main():
    # 1) 加载数据
    questions, docs = load_thelma2_dataset()
    
    # 2) 建立向量库
    print("🔧 建立 Milvus 向量库...")
    embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key=OPENAI_API_KEY)
    vectorstore = Milvus(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        connection_args={"uri": DB_URI},
        drop_old=True,
        auto_id=True,
    )
    vectorstore.add_documents(docs)
    print("✅ 向量库建立完成\n")
    
    # 3) 设置检索器
    global RETRIEVER
    RETRIEVER = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
    
    # 4) 执行检索
    print("--- 开始执行 Agent 检索 ---")
    results_map: Dict[str, List[Dict[str, Any]]] = {}
    
    for item in tqdm(questions, desc="处理问题"):
        qid = item.get("question_id")
        q = item.get("question")
        if not qid or not q:
            continue
        try:
            r = run_agent_once(q)
            results_map[qid] = r["docs"]
        except Exception as e:
            results_map[qid] = []
            print(f"\n⚠️ 问题 {qid} 发生错误：{e}")
    
    # 5) 输出结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results_map, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 完成！检索结果已输出到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

