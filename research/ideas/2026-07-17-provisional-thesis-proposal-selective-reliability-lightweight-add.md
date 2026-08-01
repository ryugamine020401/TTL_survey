# 給學長的暫定碩士論文提案：未知生成器下輕量 ADD 的選擇性可靠性

日期：2026-07-17  
模式：Synthesize + Decide（暫定推薦，尚待學長／指導教授審閱）  
證據基礎：Claude 四案 red-team、D1-P DK-CAST citation-forward gate、D1-C conformal P1/P2 gate  
狀態：可以拿去討論；pilot 尚未解除暫停

## 暫定題目

中文：

> **未知生成器下輕量音訊深偽偵測器的選擇性可靠性與保留方法**

英文：

> **Selective Reliability of Lightweight Audio Deepfake Detectors under Unseen Generators**

若 H1 證明確有退化、H2 方法也有效，最終可改成更積極的：

> **Preserving Selective Reliability in Lightweight Audio Deepfake Detection under Unseen Generators**

目前不使用後者，因為它預設了方法成功。

## 30 秒版本

現有 audio deepfake detector 越來越準，也開始能被縮小、放進瀏覽器或 edge device；但部署論文多用 EER、AUC、速度與模型大小評估。這些指標無法回答：**模型縮小後，在遇到訓練沒見過的新生成器時，是否仍知道哪些樣本不該自信判斷？**

我的論文想先驗證：一個小模型可能保留相近的辨識能力，卻破壞 confidence ranking、拒答行為及在開發集固定的門檻。若這個現象存在，再設計一個 reliability-aware distillation 方法，在相同模型大小與延遲下，比普通 distillation 更能保留「該拒答時拒答」的能力。

## 為什麼要做：完整故事

### 1. 社會問題不是「沒有 detector」，而是 detector 難以被安全地使用

一般使用者、記者或小型組織若要檢查可疑語音，雲端 detector 會遇到隱私、成本與可用性問題；本機模型則必須更小、更快。2026 年已有研究把 truncated XLS-R 放進 Chrome extension，證明這個需求真實且工程上可行。

### 2. 但是「跑得動」不等於「可以放心採用輸出」

未知生成器與資料分布改變會讓 ADD 失效。更危險的是，公開工具若只回傳 `real/fake`，使用者很容易把 `real` 誤解為「已驗證真人」。一個誠實系統至少應該能輸出：

- 疑似合成；
- 無法判定，交給人工或其他證據；
- 未發現合成證據，但不代表真人身分已驗證。

### 3. 現有輕量化評估漏掉了這個部署問題

EER/AUROC 主要描述 score 的排序／可分性；模型每次部署卻需要固定的 classification threshold 與 abstention threshold。即使 teacher 與 student 的 EER 相近，壓縮、截層或 distillation 仍可能改變 score geometry，使原本凍結的門檻在新 generator 上過度自信地把 fake 判成 real。

### 4. 因此論文的核心不是「再做一個小模型」

核心科學問題是：

> **從大型 detector 到輕量 detector 的轉換，保留了 discrimination，是否也保留了 selective reliability？如果沒有，能否在不增加部署成本的情況下保留它？**

這把個人動機與技術貢獻接在同一條鏈上：希望讓 ADD 更容易被大眾使用 → 必須本機、低成本 → 必須輕量化 → 輕量化不能只看 EER → 必須研究拒答可靠性是否被破壞。

## Problem contract

- **主要 stakeholder（暫定）**：需要在一般筆電上、離線檢查 voice message 的記者／事實查核者；一般大眾是未來受益者，而非本論文已驗證的使用者族群。
- **分析單位**：一則完整語音訊息。
- **決策**：`疑似合成 / 無法判定 / 未發現合成證據`。
- **review action**：`無法判定` 表示保留判斷、尋找來源／上下文／第二種工具，不是自動刪除內容。
- **主要風險**：fake utterance 被 detector 接受並高信心輸出為 real（confident-real leakage）。
- **核心 threat model**：完整合成語音、真正未見 generator family；另加一種常見 codec/channel 作 secondary condition。
- **不宣稱**：不驗證說話者身分、不涵蓋所有語言／partial deepfake／live VC／adaptive adversary；沒有 user study 時，不宣稱已降低受騙率或社會風險。

## Research questions

### RQ1：診斷

在 teacher 與 lightweight detector 的 discrimination 相近時，truncation／ordinary distillation 是否仍會破壞 calibration、error ranking、risk–coverage 與 source-fixed threshold transfer？

### RQ2：方法

若 RQ1 的退化存在，selective-reliability-aware distillation 是否能在相同 student architecture、資料與推論預算下，比 ordinary KD 更能保留 teacher 的拒答行為？

### RQ3：外部效度

上述現象與改善是否能在 generator-family-disjoint holdout 及一種 codec condition 下重現，而不是 dataset shortcut？

## 可否證假設

- **H1**：在 AUROC/EER 差異被控制後，ordinary lightweight transformation 的 eAURC、error ranking 或 generator-macro confident-real leakage仍顯著劣於 teacher。
- **H2**：reliability-aware objective 在相同 student、latency 與 coverage 下，能降低 generator-macro confident-real leakage，且改善不只是來自 discrimination 上升。

H1 必須先於 H2。若 H1 不成立，不訓練為了證明 H2 而設計的新 loss。

## 最小方法與實驗

### Phase 0：兩週內可殺題的 score audit

- frozen XLS-R detector + logistic head 作 teacher／reference；
- truncated layers 作便宜的 lightweight probe，利用已有 browser-edge work 降低重現成本；
- source train/dev 決定 classifier、temperature、classification threshold `t` 與 abstention threshold `q`；
- holdout 只評估，禁止挑 layer、門檻或 preprocessing；
- 先找 discrimination-matched teacher/lightweight pairs，再比較 selective metrics。

### Phase 1：只有 H1 成立才做方法

- 固定一個 student architecture；
- ordinary KD 對比 `KD + correctness/error-ranking distillation + selection consistency`；
- 同資料、同 student、同訓練 budget；
- 一個 primary holdout、一種 codec family。

### Metrics

- **Primary**：generator-macro confident-real leakage at fixed/matched coverage；
- **Selective**：risk–coverage、AURC/eAURC、error-AUROC、source-fixed `(q,t)` violation；
- **Calibration**：Brier、NLL、ECE 僅作輔助，避免把 calibration 與 ranking 混為一談；
- **Discrimination gate**：AUROC、EER；
- **Deployment**：CPU latency、peak RAM、model size。

統計單位不能只把 utterance 當獨立樣本；至少以 generator family／dataset clustered bootstrap 報告不確定性，並列出每個 generator 的結果。

## 預期貢獻

1. **Measurement contribution**：分解 lightweight ADD 的 discrimination、calibration、error ranking 與 fixed-threshold transfer，指出只報 EER 會漏掉什麼。
2. **Method contribution（H1 成立才有）**：在相同資源預算下保留 selective reliability 的 distillation objective。
3. **Deployment contribution**：一份三態輸出、資源成本與 failure conditions 清楚的 reference model card；外掛/UI 只作展示，不宣稱為新穎性。

## Closest work 與 residual gap

- [Pascu et al., Interspeech 2024](https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html)：frozen SSL 的跨資料集 generalization 與 calibration；告訴我們 detector reliability 可被研究。
- [DK-CAST, Discover Computing 2025](https://doi.org/10.1007/s10791-025-09746-4) 與 [FTDKD, TASLP 2024](https://doi.org/10.1109/TASLP.2024.3492796)：codec-aware／compressed-audio KD；告訴我們 lightweight KD 已有人做。
- [Edge browser plugin, 2026 preprint](https://arxiv.org/abs/2606.30780)：truncated SSL、六個 OOD datasets 與 Chrome extension；告訴我們 edge/public deployment 也已有人做。

**Residual gap（目前是 evidence-bounded inference）**：所檢查的 lightweight ADD work 沒有驗證壓縮／截層後的 selective risk、risk–coverage 與 source-fixed abstention-threshold transfer。論文研究的是這個交集，不是重做三條前作中的任一條。

## 為何不選 conformal 當主題

目前沒有查到直接的 ADD conformal paper，但 generic selective conformal risk control 已很新且擁擠。標準保證依賴 exchangeability 或明示的 shift assumptions；只用 source data 無法對任意未知生成器給非平凡保證。因此 conformal 適合作 baseline 或用來展示假設破裂，不應包裝成「unseen generator 下仍 distribution-free 的 certificate」。

## 一年 scope

保留：一個 teacher、一個 student、一種 lightweight mechanism、一個 primary holdout、一種 codec、ordinary vs proposed loss、score audit 與 resource benchmark。

不做：多個 backbone 大矩陣、六種 uncertainty methods、手機 App、完整 browser product、human-subject study、多語全面泛化、partial deepfake、對抗攻擊。

## 失敗條件與仍有價值的負結果

- **Kill**：teacher 在 holdout 接近隨機；holdout 無法證明 generator-family disjoint；差異全由 dataset shortcut 解釋；或 matched discrimination 下 reliability 沒有退化。
- **Kill H2**：ordinary KD 已保留 selective behavior，或 proposed loss 在相同資源下無穩定增益。
- **Possible negative contribution**：H1 明確顯示 EER 保留但 threshold transfer 失效，可形成 lightweight ADD 的評估警告與 protocol；但是否足以作完整 thesis，需先向學長／指導教授確認，不能事後才圓。

## 想請學長先回答的三個問題

1. 這個「輕量化保留 selective reliability」的 contribution owner 是否足以成為碩論，而不是只算 evaluation？
2. 應把 stakeholder 定為記者／查核者，還是更一般的 voice-message 使用者？前者的決策流程較清楚，也較容易避免過度宣稱。
3. 是否同意先做兩週內的 H1 score audit 與 lineage check，通過後才正式 commit 並開始 H2？

## 建議給學長的訊息

> 我目前把方向 #1 收斂成「未知生成器下，音訊 deepfake detector 輕量化後是否仍保有可靠拒答能力」。現有研究已經分別做過 calibrated detector、knowledge distillation，以及瀏覽器端輕量模型，但多半用 EER/AUC 和速度評估；我想研究的是模型看似維持辨識能力時，固定在開發集的信心／拒答門檻是否會在新生成器上失效。如果確有失效，再做一個 reliability-aware distillation 方法；如果沒有，就及早停題。我先整理了一頁 problem contract、closest work、兩階段實驗與 kill conditions，希望請學長判斷這個貢獻是否足以作為碩論主軸，以及 stakeholder 應鎖定記者／查核者還是一般使用者。

## 下一個最小步驟

先請學長用上述三題審閱。獲得「值得做 H1 gate」的回覆後，再完成 dataset/generator lineage manifest 與 score-only audit specification；在這之前不跑 full pilot。

