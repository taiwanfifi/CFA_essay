# FinEval-CRA-Bigdata

**Repository**: `Salesforce/FinEval`

**Config**: `CRA-Bigdata`

## Dataset信息

- **Splits**: test

### test

- **样本数量**: 1472
- **特征字段**: id, query, answer, text, choices, gold

**示例数据**:

```json
{
  "id": "bigdatasm5695",
  "query": "Examine the data and tweets to deduce if the closing price of $ba will boost or lower at 2020-11-02. Kindly confirm either Rise or Fall.\nContext: date,open,high,low,close,adj-close,inc-5,inc-10,inc-15",
  "answer": "Rise",
  "text": "date,open,high,low,close,adj-close,inc-5,inc-10,inc-15,inc-20,inc-25,inc-30\n2020-10-19,1.2,2.2,-0.6,-0.1,-0.1,-1.4,-1.2,-0.8,-2.4,-2.4,-2.6\n2020-10-20,0.6,1.2,-0.6,0.1,0.1,-0.8,-0.8,-0.7,-2.1,-2.3,-2.",
  "choices": [
    "Rise",
    "Fall"
  ],
  "gold": 0
}
```

