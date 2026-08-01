# 給學長的暫定碩論提案 v2

日期：2026-07-17  
狀態：工作提案，尚未選題定案；pilot 暫停  
證據基礎：D1-P/D1-C literature gates、Claude red-team、recalibration-transfer 與 holdout-lineage 小型 gate

## 暫定題目

中文：**未知生成器下輕量音訊深偽偵測器的選擇性可靠性：固定門檻轉移與校準保留**  
英文：**Selective Reliability of Lightweight Audio Deepfake Detectors: Fixed-Threshold Transfer and Calibration Preservation under Unseen Generators**

題目仍刻意不用 `Preserving...` 起頭，因為方法能否保留可靠性尚未被 H1/H2 證明。

## 為什麼做

我的長期目標不是只把 audio deepfake detector 的 benchmark 分數再提高一點，而是讓它更容易部署，也更能在一般人、記者或查核者真的遇到未知生成器時安全使用。

本機、低成本的 detector 必須輕量；但現有 lightweight／edge ADD 工作主要用 EER、F1、速度與記憶體說明模型「仍然能分」。真實使用還多一個問題：模型何時足夠可信可以給判斷，何時應該棄權並交給人工或更強的檢查？若輕量化保留 AUROC，卻讓 source 開發集設定的 confidence／decision thresholds 到新 generator 就失準，使用者會收到看似確定、其實錯誤的「真人」判斷。

因此論文不是要證明偵測器能驗證某人「一定是真人」，而是研究一個較誠實的三態支援：

- 發現合成證據；
- 未發現合成證據；
- 證據不足，棄權並建議升級查核。

主要使用情境暫定為**記者／事實查核者的本機初篩**：棄權後有明確的升級動作，也比直接向大眾承諾真假裁決更符合 detector 的能力邊界。一般語音訊息使用者是後續可用性對象，不是本論文先承諾的部署族群。

## 核心研究問題

> 在偵測能力與資源預算相近時，輕量化是否破壞只由 source-dev 決定的 accept/abstain operating point 在未知 generator 上的轉移？若簡單重新校準不足，能否設計一個超過普通 soft-label KD 的方法保留這種選擇性可靠性？

## 可否證假設

- **H1a — failure existence：** 在 AUROC 與 eAURC 落在預先設定的 matching tolerance 內，ordinary lightweight student 仍比 teacher 有更高的 unseen-generator、generator-macro confident-real leakage／risk violation。
- **H1b — trivial-repair gate：** 只用 source-dev 擬合的 temperature scaling（另以 affine/Platt scaling 作 sensitivity）不能把 ordinary KD 的 external fixed-threshold reliability 修復到 teacher 水準。
- **H2 — method gate：** 一個明確超過 confidence imitation 的 reliability-aware distillation mechanism，在 matched AUROC/eAURC、latency 與參數量下，勝過 ordinary KD、ordinary KD + source-dev TS，以及 Platt sensitivity。

H1a 不成立就停止；H1b 不成立、簡單 recalibration 已足夠，也停止 H2。這兩種結果不會被事後包裝成方法成功。

## 最小方法與公平比較

### Phase 0：資料與 score-only gate（先做，尚不跑 full pilot）

1. Reference：一個 frozen SSL teacher／reference detector。
2. Cheap lightweight probes：截短層 probe，以及至多一個 ordinary-KD student；先不搜尋大量架構。
3. 每個模型各自只用相同 source train/dev 擬合 calibration，並在相同 source operating constraint 下決定自己的 `(q_m,t_m)`；不能把 teacher 的數值門檻硬套到 student。
4. 凍結全部設定後才進入 holdout，不用 holdout label 調 threshold、temperature、preprocessing 或 model choice。
5. 主要 holdout 候選：ASVspoof 5 evaluation 的 C00 非 adversarial、非 legacy 子集；保守約 7 個 architecture families。DFADD corrected release 作 exploratory replication，不作主要方法檢定。
6. 同步完成 lineage、speaker/content/source、checkpoint、license、hash 與 shortcut manifest。未通過就不解鎖 H1。

### Phase 1：只有 H1a/H1b 都成立才做方法

候選機制暫定為 **correctness-aware operating-point／selection-consistency distillation**：除了 ordinary soft-label KD，直接約束 student 對「哪些例子應接受、哪些應棄權」的 correctness ranking／threshold margin，並在 paired clean↔codec views 維持 selection decision。這比單純模仿 teacher confidence 多了一個可測機制，但在開始前仍須做 closest-work collision gate；若 collision 或最小實作過大，應換機制或砍題，而不是只改 loss 名稱。

## 主要量測

- 主要部署風險：對每個 generator family，`P(accepted 且判為 real | 實為 fake, family g)`，再做 family macro average。
- 同時報 coverage、selective risk／risk violation，以及逐 family 結果。
- AUROC、EER、eAURC 是 matching／diagnostic，不代替固定 operating-point 結果。
- 分析單位是 generator family，不把 utterances 當完全獨立樣本；使用 family bootstrap 或 hierarchical interval，並誠實呈現約 7 clusters 的寬不確定性。
- 資源限制：parameter count、latency、memory；H2 必須在相同 student budget 下比較。

## 必要 baselines

1. frozen SSL teacher／reference；
2. truncated lightweight probe；
3. ordinary KD；
4. **ordinary KD + source-dev temperature scaling**；
5. ordinary KD + source-dev affine/Platt scaling（sensitivity）；
6. H1a/H1b 通過後的 proposed reliability-aware KD。

## 預期貢獻與誠實邊界

若全部 gates 通過，貢獻 owner 是一個能打贏簡單重新校準的 reliability-preserving method；matched-discrimination protocol 與 edge ADD 評估修正是 supporting contributions。這避免論文最後只剩「跑很多 uncertainty methods 畫曲線」。

但風險必須先說清楚：若 H2 打不贏 KD+recalibration，論文只剩 measurement／deployment warning，而這低於我目前期待的方法貢獻。屆時應回到其他候選題目，而不是勉強把負結果說成原先目標已完成。

不宣稱：

- 任意未知 generator 的 distribution-free 保證；
- detector 可驗證說話者一定是真人；
- 7 個 holdout families 能代表所有未來模型；
- 目前已是首創或方法已有效。

## 一年內的最小範圍

- 一個 source 訓練設定；
- 一個 primary holdout（ASVspoof 5 selected C00）；
- 一個 teacher、至多兩個 ordinary lightweight transformations；
- 一個 proposed mechanism；
- score-level／family-level 主分析；
- reference deployment artifact 只證明輸入、三態輸出與 latency 可行，不做完整產品或大型 user study。

## 希望學長先裁決的三件事

1. 以「方法必須打贏 ordinary KD + source-dev recalibration」作 thesis-level contribution bar，是否合理？
2. 以記者／fact-checker 的本機初篩為主要 deployment claim，是否比 general-public 真偽裁決更可守？
3. 若 H1a 成立但 H1b 或 H2 失敗，是否同意立即回到候選題比較，而不把純量測結果硬定為碩論主題？

下一個最小步驟是先請學長審這三點；同時只完成 ASVspoof 5 小型 protocol/lineage manifest 與 preregistration-ready H1 規格。pilot、資料集大檔下載與訓練仍暫停。
