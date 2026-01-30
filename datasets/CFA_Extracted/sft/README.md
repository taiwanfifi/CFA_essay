# cfa_extracted_qa_sft

**Repository**: `ZixuanKe/cfa_extracted_qa_gpt4_verify_sft_without_material_gpt4_answer`

## Dataset信息

- **Splits**: train

### train

- **样本数量**: 2946
- **特征字段**: topic, title, justification, questions, scenario, exhibit, answer_choices, answer, material, gpt4_answerable_with_material, gpt4_answerable_without_material, gpt4_answer, gpt4_answer_justification, messages

**示例数据**:

```json
{
  "topic": "cfa",
  "title": "CFA 2020 Level II - SchweserNotes Book 4.txt",
  "justification": "The material provides a set of multiple-choice questions from a module quiz pertaining to financial concepts such as yield curves, forward curves, and bond pricing models. I extracted the exact questi",
  "questions": "When the yield curve is downward sloping, the forward curves are most likely to lie:",
  "scenario": "N/A",
  "exhibit": "N/A",
  "answer_choices": "A. above the spot curve.\nB. below the spot curve.\nC. either above or below the spot curve.",
  "answer": "N/A",
  "material": "MODULE QUIZ 32.1To best evaluate your performance, enter your quiz answers online.1. When the yield curve is downward sloping, the forward curves are most likely to lie:A. above the spot curve.B. belo",
  "gpt4_answerable_with_material": "cheat",
  "gpt4_answerable_without_material": "non-contextual",
  "gpt4_answer": "Explanation: According to the reference, specifically in the section discussing relationships between spot and forward rates, it is explicitly stated that for a downward-sloping spot curve, the forwar",
  "gpt4_answer_justification": "Without needing to refer to the provided scenario and exhibit, the question about where the forward curve lies in relation to the spot curve when the yield curve is downward sloping can be answered ba",
  "messages": [
    {
      "content": "Given the answer choices, please answer the question bellow.\n\nQuestion: When the yield curve is downward sloping, the forward curves are most likely to lie:\n\nAnswer Choices: A. above the spot curve.\nB. below the spot curve.\nC. either above or below the spot curve..\n\nAnswer:",
      "role": "user"
    },
    {
      "content": "Explanation: According to the reference, specifically in the section discussing relationships between spot and forward rates, it is explicitly stated that for a downward-sloping spot curve, the forward curve will be positioned below the spot curve. Therefore, the answer is directly drawn from the reference material.\nAnswer: B. below the spot curve.",
      "role": "assistant"
    }
  ]
}
```

