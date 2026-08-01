# 碩士論文方向辯論：Deepfake Audio Detection

日期：2026-07-13
文獻基礎：`d:\code\Master Thesis\survey\README.md`（8 篇文獻與 Research Gap 地圖）

## 問題陳述

1. 現代社會製造 deepfake audio 變得容易，門檻極低。
2. 語音詐騙氾濫，正在侵蝕人們對各種資訊（電話、語音訊息、新聞）的信任。
3. 已有機構提出用密碼學方式（C2PA 等 content provenance）為聲音或影像內容做保證，但只能保證「內容沒有被竄改」，不能保證「內容不是 AI 生成的」。
4. 現有 deepfake detection 模型遇到閉源生成模型時能力大幅下降（VoiceWukong 實測：EER 從 <1% 暴增至 13.5–50%）。
5. 音訊經社群軟體、重新錄製、壓縮或改動（laundering）後，往往遺失 detection 依據（Loughborough benchmark：僅 codec 壓縮就顯著劣化，對未知轉檔管線無解）。

## 討論目標

在上述限制下提出開創性的解法，統整出 **5 個可以成為碩士論文的方向與實驗規劃**。

硬性要求：
- 要能套用到真實情境，盡量降低人受騙的機率
- 要能為社會福祉做出貢獻
- 一位碩士生在約一年內做得完

## 八位討論者

| 代號 | 角色 | 視角 |
|------|------|------|
| A | Detection 研究者 | ML、generalization、SSL 特徵 |
| B | 密碼學 / Provenance 研究者 | C2PA、watermarking、信任模型 |
| C | 訊號處理研究者 | codec、通道、laundering robustness |
| D | 紅隊 / 攻擊者 | 對每個方案找出繞過方式 |
| E | 開創性思維者 | 跳出框架、重新定義問題 |
| F | 一般民眾代表 | 真實受騙情境、可用性 |
| G | 領域史官 | 歷史沿革、SOTA 進展、未來展望（含網路檢索） |
| H | 指導教授 | novelty、可行性、評估方法、時程 |

## 討論流程與紀錄

- `round1/` — 各角色獨立提案（8 檔）
- `round2/` — 交叉質詢：每人挑戰至少 3 個他人提案（8 檔）
- `round3/` — 答辯與修正：回應針對自己的挑戰（8 檔）
- `03-synthesis.md` — 最終統整：5 個論文方向與實驗規劃
