# D1+D4 論文進度追蹤

## 論文資訊
- **標題**: When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making
- **目標期刊**: Finance Research Letters (FRL), SSCI Q1
- **狀態**: 🔴 撰寫中

## 時程
| 日期 | 里程碑 | 狀態 |
|------|--------|------|
| 2/5 | 生成圖表 | 🔴 |
| 2/6-8 | 撰寫初稿 | 🔴 |
| 2/9 | 投稿 | 🔴 |

## 待辦事項

### 數據 & 圖表
- [ ] 跑完整 D1 實驗（CFA-Easy 1,032 題 + CFA-Challenge 90 題）
- [ ] 生成 Reliability Diagram
- [ ] 生成 ECE Bar Chart（跨模型比較）
- [ ] 生成 Heatmap（High-confidence error by CFA topic）
- [ ] 分類 D4 的 74 筆高信心錯誤

### 論文撰寫
- [ ] Introduction（2/6）
- [ ] Methodology（2/6）
- [ ] Results（2/7）
- [ ] Discussion - Economic Significance（2/7）
- [ ] Discussion - CFA Ethics（2/8）
- [ ] Conclusion（2/8）
- [ ] Abstract（最後寫）

### 投稿準備
- [ ] 下載 FRL 官方模板（確認格式）
- [ ] 準備 Cover Letter
- [ ] 確認共同作者資訊
- [ ] 準備 Data Availability Statement

## 核心數據（來自 POC）

| 指標 | 數值 | 來源 |
|------|------|------|
| D1 總樣本 | 250 筆 | experiments/D1/.../results.json |
| 高信心錯誤 (≥80%) | 74 筆 (29.6%) | D4 篩選 |
| 平均錯誤信心 | 89.0% | D4 分析 |
| ECE (gpt-4o-mini) | 0.18 | D1 計算 |

## 關鍵論點

1. **不是考幾分的問題，是知不知道自己考錯的問題**
2. **29.6% 高信心錯誤 = 金融決策的系統性風險**
3. **對接 CFA Ethics：過度自信 AI 是否違反受託責任？**
4. **監管建議：金融 AI 需要最低 calibration 標準**

## 命令備忘

```bash
# 跑 D1 實驗
python -m experiments.D1_confidence_calibration.run_calibration \
  --dataset easy --model gpt-4o-mini

# 生成圖表
python -m experiments.D1_confidence_calibration.visualize \
  --input experiments/D1_confidence_calibration/results/run_*/results.json \
  --output drafts/selected/D1_calibration/figures/

# D4 風險分類
python -m experiments.D4_overconfident_risk.run_experiment \
  --input "experiments/D1_confidence_calibration/results/run_*/results.json" \
  --confidence-threshold 0.8
```
