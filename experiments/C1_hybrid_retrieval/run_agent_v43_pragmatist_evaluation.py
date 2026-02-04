# run_agent_v43_pragmatist_evaluation.py  (OpenAI 版本)
# ------------------------------------------------------------
# V4.3 Pragmatist（OpenAI + Milvus）離線檢索預跑器
# - 讀 ultimate_rag_challenge_questions.json 的 gold evidence
# - 建 Milvus(Lite) 向量庫（text-embedding-3-large, 3072d）
# - 執行：規劃 → 查詢重寫 → 檢索 → 抽取 → 充分性評估 → 摘要
# - 對每題輸出前 TOP_K 的 doc（page_content + {"doc_id": ...}）
#
# 輸出：./agent_v43_retrieval_results.json
# ------------------------------------------------------------

import os
import json
import itertools
from typing import List, Dict, Any, Set, TypedDict

from dotenv import load_dotenv
load_dotenv()

from tqdm import tqdm

# LangChain / LangGraph
from langchain_core.documents import Document
# 若想再切片可開啟
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_milvus import Milvus

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END


# =========================
# 0) 基本設定
# =========================
DATA_FILE = "./data/ultimate_rag_challenge_questions.json"
RESULTS_FILE = "./agent_v43_retrieval_results.json"

# 向量庫（Milvus Lite 本地檔案; 用新名稱避免維度衝突）
COLLECTION_NAME = "agent_v43_collection_openai_te3l"
DB_URI = "./agent_v43_milvus_openai.db"

# 模型（OpenAI）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定環境變數 OPENAI_API_KEY")

LLM_MODEL = os.getenv("OPENAI_LLM", "gpt-4o-mini")             # 統一用 gpt-4o-mini
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING", "text-embedding-3-large")  # large v

# RETRIEVER_K = 6         # 每次檢索 top-k
# AGENT_MAX_TURNS = 8     # 最大循環回合
# TOP_K_RETURN = 5        # 每題輸出前 K 份證據

RETRIEVER_K = 8       # ← 3 -> 8
AGENT_MAX_TURNS = 8
TOP_K_RETURN = 5

MIN_TURNS = 3         # ← 至少跑 3 輪
MIN_UNIQUE_DOCS = 2   # ← 至少命中 2 個不同 doc_id 才能停



print("--- Summary Builder Agent (V4.3 - Pragmatist / OpenAI) : Offline Retrieval Runner ---")
print(f"LLM(JSON/Text): {LLM_MODEL} (OpenAI)")
print(f"Embedding: {EMBED_MODEL}")
print(f"Milvus DB: {DB_URI} / {COLLECTION_NAME}\n")


# =========================
# 1) 載入資料集，收集 gold evidence
# =========================
def load_eval_evidence() -> List[Document]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        eval_data = json.load(f)
    unique: Dict[str, str] = {}
    for item in eval_data:
        for ev in item.get("gold_evidence", []):
            did = ev.get("doc_id")
            txt = ev.get("text_snippet")
            if did and isinstance(txt, str):
                unique[did] = txt
    docs = [Document(page_content=txt, metadata={"doc_id": did}) for did, txt in unique.items()]
    return docs

def load_questions() -> List[Dict[str, Any]]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# 2) 建向量庫（Milvus Lite）
# =========================
def ensure_vectorstore(docs: List[Document]) -> Milvus:
    # 若要切片可開啟
    # splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key=OPENAI_API_KEY)

    # 統一重建，避免舊 collection 維度不符
    print("🔧 準備 Milvus(Lite) collection ...")
    vs = Milvus(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        connection_args={"uri": DB_URI},
        drop_old=True,          # 確保用新 embedding 維度重建
        auto_id=True,
    )
    print("   - 寫入 gold evidence ...")
    vs.add_documents(docs)
    print("   - ✅ 向量庫建立完成")
    return vs


# =========================
# 3) V4.3 Agent（精簡但可檢索）
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

# Pydantic models
class SimplePlan(BaseModel):
    plan: List[str] = Field(description="2-3 concrete sub-steps.")

class SimpleHypotheses(BaseModel):
    hypotheses: List[str] = Field(description="2-3 distinct hypotheses.")

class GradedAnswer(BaseModel):
    is_sufficient: str = Field(description="yes or no")

class ExtractedFacts(BaseModel):
    facts: List[str] = Field(description="key facts")

class RewrittenQueries(BaseModel):
    rewritten_queries: List[str] = Field(description="1-3 search queries")

# LLMs（兩個都用 gpt-4o-mini；一個走 JSON 輸出任務，一個自由生成）
llm_json = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=OPENAI_API_KEY)
llm_text = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=OPENAI_API_KEY)

# 這裡的 retriever 會在 main 中注入
RETRIEVER = None  # type: ignore

def hypothesize_node(state: GraphState):
    parser = JsonOutputParser(pydantic_object=SimpleHypotheses)
    prompt = PromptTemplate.from_template(
        "Analyze the user's question and produce 2-3 distinct hypotheses.\n"
        "Question: {original_question}\n"
        "{format_instructions}"
    )
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm_json
    try:
        raw = chain.invoke({"original_question": state["original_question"]})
        data = raw if isinstance(raw, dict) else json.loads(raw.content)  # ChatOpenAI -> AIMessage
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
        "Create 2-3 concrete sub-steps to answer the question.\n"
        "Hypothesis: {current_hypothesis}\n"
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
        "Rewrite the following into 1-3 diverse retrieval queries.\n"
        "Original: {q}\n"
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

    # 檢索
    batch_lists = RETRIEVER.batch(queries)
    merged = list(itertools.chain.from_iterable(batch_lists))

    # 以 doc_id 去重、記錄新取回的與總累積
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
        "Extract salient facts that help answer the original question.\n"
        "Original Question: {oq}\n"
        "Sub-question: {sq}\n"
        "Documents:\n{docs}\n"
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
            state["cumulative_facts"] = list(dict.fromkeys(state["cumulative_facts"]))  # 去重
    except Exception:
        pass
    return state

# def grade_facts_node(state: GraphState):
#     decision = "yes" if state["cumulative_facts"] else "no"
#     if state["turn_count"] >= AGENT_MAX_TURNS or not state.get("has_new_info", True):
#         decision = "yes"
#     state["assessment"] = decision
#     return state

# def grade_facts_node(state: GraphState):
#     uniq_docs = {
#         d.metadata.get("doc_id")
#         for d in state.get("cumulative_retrieved_docs", [])
#         if d.metadata.get("doc_id")
#     }
#     enough_docs = len(uniq_docs) >= MIN_UNIQUE_DOCS
#     enough_turns = state["turn_count"] >= MIN_TURNS
#     hit_max = state["turn_count"] >= AGENT_MAX_TURNS
#     no_new_info = not state.get("has_new_info", True)

#     state["assessment"] = "yes" if ((enough_docs and enough_turns) or hit_max or no_new_info) else "no"
#     return state

def grade_facts_node(state: GraphState):
    distinct_doc_ids = {d.metadata.get("doc_id") for d in state.get("cumulative_retrieved_docs", []) if d.metadata.get("doc_id")}
    has_two_docs = len(distinct_doc_ids) >= 2
    # 若至少跑了 2 回合再評估停止，避免第一輪就收手
    min_turns_done = state.get("turn_count", 0) >= 2
    stop_now = (has_two_docs and min_turns_done) or (state.get("turn_count", 0) >= AGENT_MAX_TURNS) or (not state.get("has_new_info", True))
    state["assessment"] = "yes" if stop_now else "no"
    return state



def decide_to_continue(state: GraphState):
    return "generate_summary" if state.get("assessment") == "yes" else "continue"

def generate_summary_node(state: GraphState):
    if not state["cumulative_facts"]:
        state["final_summary"] = "No sufficient facts were found."
        return state
    prompt = PromptTemplate.from_template(
        "Write a concise answer using only these facts.\n"
        "Question: {q}\nFacts:\n- {facts}\n\nAnswer:"
    )
    chain = prompt | llm_text | StrOutputParser()
    facts_str = "\n- ".join(state["cumulative_facts"])
    state["final_summary"] = chain.invoke({"q": state["original_question"], "facts": facts_str})
    return state

# 圖
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
# 4) 執行每題，輸出檢索結果 JSON
# =========================
def run_agent_once(question: str) -> Dict[str, Any]:
    """回傳 final_state 與 top-k 檢索文件（doc_id + page_content）"""
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
    # 依「首次被檢索到」的順序取前 K
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
    # 1) 建知識庫 & 檢索器
    gold_docs = load_eval_evidence()
    vectorstore = ensure_vectorstore(gold_docs)
    global RETRIEVER
    RETRIEVER = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
    print("✅ Retriever ready.\n")

    # 2) 逐題執行
    eval_data = load_questions()
    results_map: Dict[str, List[Dict[str, Any]]] = {}

    print("--- 開始離線檢索 (V4.3 Pragmatist / OpenAI) ---")
    for item in tqdm(eval_data, desc="Evaluating"):
        qid = item.get("question_id")
        q = item.get("question")
        if not qid or not q:
            continue
        try:
            r = run_agent_once(q)
            results_map[qid] = r["docs"]
        except Exception as e:
            results_map[qid] = []
            print(f"\n⚠️ 問題 {qid} 發生錯誤：{e}")

    # 3) 輸出
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results_map, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 完成！檢索結果已輸出到 {RESULTS_FILE}")
    print("接著到 rag_systems_to_test.py 用 JsonFileRetriever 載入，於 evaluate.py 並列評測。")


if __name__ == "__main__":
    main()
