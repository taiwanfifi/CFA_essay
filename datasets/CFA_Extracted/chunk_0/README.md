# cfa_extracted_qa_chunk_0

**Repository**: `ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0`

## Dataset信息

- **Splits**: train

### train

- **样本数量**: 1124
- **特征字段**: topic, title, justification, questions, scenario, exhibit, answer_choices, answer, material, gpt4_answerable_with_material, gpt4_answerable_without_material, gpt4_answer, gpt4_answer_justification

**示例数据**:

```json
{
  "topic": "cfa",
  "title": "CFA 2020 Level II - SchweserNotes Book 4.txt",
  "justification": "The material provided includes specific examples and their solutions related to the topics of spot and forward rates, yield to maturity, and expected and realized returns on bonds. These examples cont",
  "questions": "Compute the price and yield to maturity of a three-year, 4% annual-pay, $1,000 face value bond given the following spot rate curve: S1 = 5%, S2 = 6%, and S3 = 7%.",
  "scenario": "N/A",
  "exhibit": "N/A",
  "answer_choices": "N/A",
  "answer": "1. Price = \\(\\frac{40}{(1.05)} + \\frac{40}{(1.06)^2} + \\frac{1040}{(1.07)^3} = $922.64\\) 2. y3 = 6.94%",
  "material": "Video coveringthis content isavailable online.\nMODULE 32.1: SPOT AND FORWARD RATES, PART 1LOS 32.a: Describe relationships among spot rates, forward rates, yield to maturity,expected and realized retu",
  "gpt4_answerable_with_material": "cheat",
  "gpt4_answerable_without_material": "no",
  "gpt4_answer": "Explanation: The price is calculated using the provided spot rate curve by discounting each cash flow (coupon payment and the face value at maturity) back to its present value using the respective yea",
  "gpt4_answer_justification": "The reference provides the exact formula and step-by-step calculation to compute both the price and the yield to maturity for a three-year, 4% annual-pay, $1,000 face value bond given specific spot ra"
}
```

