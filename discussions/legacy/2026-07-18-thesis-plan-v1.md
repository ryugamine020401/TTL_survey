# 碩士論文計畫書 v1

## 未知生成器下輕量音訊深偽偵測器的選擇性可靠性：固定門檻轉移與校準保留
### Selective Reliability of Lightweight Audio Deepfake Detectors under Unseen Generators: Fixed-Threshold Transfer and Calibration Preservation

日期：2026-07-18　狀態：工作計畫（尚未正式定題；pilot/大檔下載/訓練暫停）
證據基礎：8 篇文獻 survey、多輪多角色思辨、Codex 獨立查證（A–E claims、七角色審查、D1-P/D1-C literature gates、Q1–Q3 前作定位、recalibration/holdout gates）、Claude red-team。
> 本計畫刻意**不**用「Preserving…」起頭——方法能否保留可靠性尚待 H1/H2 驗證，不預設成功。

---

## 0. 摘要（30 秒版）

音訊深偽偵測器越來越準，也開始被縮小、放進瀏覽器/edge 供大眾與記者本機使用。但輕量化論文多用 EER、AUC、速度、記憶體證明模型「仍能分」，**沒有回答一個部署關鍵問題：模型縮小後，遇到訓練沒見過的新生成器時，是否仍知道哪些樣本不該自信判斷？** 若輕量化保住了辨識力（AUROC），卻讓開發集凍結的信心/決策門檻在新生成器上失準，使用者會收到「看似確定、其實錯誤」的『真人』判斷。

本論文先驗證這個退化是否存在（H1a）、簡單重新校準能否修好（H1b）；若退化存在且簡單修法不足，再設計一個超過普通蒸餾的方法保留這種選擇性可靠性（H2）。

---

## 1. 研究背景與動機

1. **deepfake audio 門檻極低、語音詐騙侵蝕信任**（survey 動機鏈）。
2. **兩條現有防線各有硬極限**：被動偵測面對未見/閉源生成器 generalization 大幅下降（VoiceWukong：SOTA EER 從 <1% 升到 13.5%+）；密碼學 provenance（C2PA）只證「未被竄改」不證「非 AI 生成」，且對不附憑證的惡意 deepfake 零覆蓋。
3. **部署面的被忽略缺口**：要讓偵測器真正降低大眾受騙風險，得能被本機、低成本、離線使用 → 必須輕量化。但現行輕量/edge ADD（DK-CAST、FTDKD、2026 瀏覽器外掛）只用 EER/AUC/latency 評估，**沒人驗證輕量化是否破壞了『該棄權時棄權』的能力**。
4. **動機鏈**：讓 ADD 更能被大眾安全使用 → 必須本機低成本 → 必須輕量 → 輕量不能只看 EER → 必須研究拒答可靠性是否被破壞、能否保留。

主要使用情境（暫定）：**記者／事實查核者的本機初篩**——棄權後有明確的升級查核動作，比向大眾承諾真假裁決更符合偵測器能力邊界。一般語音訊息使用者是後續受益者，不是本論文已驗證的部署族群。

---

## 2. 從發想到收斂：決策軌跡（為何是這個題目）

本題經過多輪多角色思辨 + Codex 獨立文獻查證的對抗式收斂，非憑空發想：

- **5 個候選方向**（選擇性預測 / 真實通道審計 / 攻擊成本地圖 / 詐騙現場評估 / provenance）→ 作者裁定「不做真人實測」「一人一年一張 RTX 4090」「純量測不足、要方法貢獻」。
- 方向#1（選擇性預測）勝出，但 Codex 查證推翻其多項「零前作」宣稱（Salvi 2023、Pascu 2024、Zhou 2026 等已做量測），**純量測擁擠**。
- 為滿足「方法貢獻」，升級為四候選（conformal / compression / meta-selective / guardrail）。**D1-P（selective-risk-preserving compression）勝出**：對「可部署」和「科學深度」兩種目標都穩健；conformal 因「arbitrary unseen shift 下 source-only 保證不可識別」降為 baseline。
- 作者確認 intent：**主軸更可部署/實用，但要創新方法、對領域有用**（非工程 demo）。
- Codex Q1–Q3 查證再收窄（見 §3）：廣義「reliability-preserving 壓縮法」已存在 → 方法貢獻只在窄交集可能成立，且**需跑便宜稽核才能 derisk**。作者裁定：**先跑 H1a/H1b derisking 稽核**（本計畫 §8）。

---

## 3. 誠實的 novelty 定位（Codex Q1–Q3 查證結果）

把主張拆四層，各層前作狀態不同：

| 層 | 我們的主張 | 前作狀態 | 最接近前作 | 誠實定位 |
|---|---|---|---|---|
| **現象**：壓縮在辨識力不變下傷可靠性 | 在 ADD 觀察 | **Partially（非定律）** | 支持：Zhong ACL 2025（量化 LLM calibration gap）、DistilDoc ICDAR 2024；反證：Mitra CVPRW 2024（pruning 無傷）、量化 BNN | **不主張通用新現象**；主張 ADD unseen-generator external transfer 的預註冊量測 |
| **設定**：輕量/edge ADD | 壓縮 ADD | **已知** | DK-CAST、FTDKD、DOC-KD、2026 edge/browser（2606.30780） | 不在此層 |
| **可靠性**：ADD 拒答可靠性 | 量可靠性 | **已知（full model）** | Pascu、FADEL | 不在泛稱層 |
| **交集+方法**：輕量 ADD × 未見生成器 external selective-policy transfer × 保留方法 | H2 核心 | **Partially（窄交集 open）** | KD(C) ACCV 2024、BN3 CVPR 2021、EnD² NeurIPS 2021、Kim Interspeech 2021（語音 uncertainty-matching KD） | **只在窄交集可能成立**；若只是既有方法套 ADD，降為 application novelty |

**可守的一句 positioning（送審用）**：
> Prior work has shown compression can alter calibration in some settings, has developed calibration- and uncertainty-aware distillation methods, and has evaluated distilled models with AURC. Within our documented search scope, we found no work that tests whether a **source-frozen abstention/classification policy** survives lightweight audio-deepfake transformation on **lineage-disjoint unseen generators**, or develops an **ADD-specific method** for that external selective-risk transfer.

**誠實結論**：這**不是「完全創新」**。是「一個已知現象（可能）+ 已知設定 + 已知關注，三者以前沒接在一起 + 一個尚待驗證是否真有增量的 ADD-specific 方法」。這種「新組合 + 條件性新方法」在碩論是站得住的貢獻型態，但**方法貢獻能否成立，是本計畫要 derisk 的核心賭注**。

---

## 4. 研究問題與假設（kill sequence）

**核心 RQ**：在偵測能力與資源預算相近時，輕量化是否破壞只由 source-dev 決定的 accept/abstain operating point 在未知 generator 上的轉移？若簡單重新校準不足，能否設計一個超過普通 soft-label KD 的方法保留這種選擇性可靠性？

- **H1a（現象存在）**：AUROC/EER 落在預設 matching tolerance 內時，ordinary lightweight student 各自用 source-dev 凍結的 `(q_m,t_m)`，在未見 generator 上的 **generator-macro confident-real leakage / risk violation 顯著高於 teacher**。
- **H1b（trivial-repair gate）**：只用 source-dev 擬合的 temperature scaling（+ affine/Platt sensitivity）**修不好** ordinary KD/truncation 的 external fixed-threshold reliability 到 teacher 水準。
- **H2（方法 gate）**：一個明確超過 confidence imitation 的 reliability-aware distillation 機制，在 matched AUROC/eAURC、latency、參數量下，**同時勝過** ordinary KD、KD + source-dev TS、KD + Platt。

**定序**：H1a 不成立 → 停。H1b 不成立（簡單校準已足夠）→ kill H2。兩種結果都不得事後包裝成方法成功。

---

## 5. 方法與公平比較

- **單位**：一則完整語音訊息（切窗須以預註冊 aggregation 回到 message level）。分析與泛化單位是 **generator family**，不把 utterance 當獨立樣本。
- **teacher/reference**：一個 frozen SSL ADD detector（XLS-R + AASIST 或 + linear head，訓於 source）。
- **lightweight students**：截短層 probe（最便宜、不需訓練）+ 至多一個 ordinary-KD student。
- **公平 estimand（關鍵修正）**：**每個模型各自**用相同 source train/dev 擬合 calibration，並在相同 source operating constraint 下決定自己的 `(q_m,t_m)`；**不得把 teacher 的數值門檻硬套 student**（不同 score scale 會製造近乎必然的假失敗）。凍結後才碰 holdout。
- **matched discrimination**：配平只用 **deployment budget + AUROC/EER equivalence tolerance（預先定）**；**不用 eAURC 當配平變數**（會與主結果 circular）。
- **H2 候選機制（暫定）**：correctness-aware operating-point / selection-consistency distillation——除 soft-label KD 外，直接約束 student 對「哪些該接受、哪些該棄權」的 correctness ranking / threshold margin，並在 paired clean↔codec views 維持 selection decision。**開始前須先過 method closest-work gate**；若撞題或實作過大，換機制或砍題，不只改 loss 名。

**必要 baselines**：frozen teacher ｜ truncated probe ｜ ordinary KD ｜ **ordinary KD + source-dev temperature scaling（致命 baseline）** ｜ + Platt sensitivity ｜（gates 過後）proposed reliability-aware KD。

---

## 6. 資料集

| 角色 | 資料集 | 說明 | 狀態 |
|---|---|---|---|
| **source（train/dev）** | ASVspoof 2019 LA | teacher/student 訓練與門檻擬合；ODC-By | 公開可下載 |
| **exploratory holdout（便宜首探）** | In-the-Wild | 小、可下載；generator lineage 不明 → 僅探路 | 公開（Apache 2.0） |
| **exploratory replication** | DFADD（2025-04 corrected） | 5 具名 TTS family；有固定 LJSpeech 文本/VCTK source shortcut → 不作 confirmatory | HF `isjwdu/DFADD`，MIT+upstream |
| **confirmatory holdout（主）** | ASVspoof 5 eval，C00 非 adversarial/非 legacy 子集 | 排除 adversarial + A19 MaryTTS 後 8 IDs（A17/A21/A22/A24/A25/A26/A28/A29），A21/A22 合併 ≈ **7 architecture families**；shortcut 控制較好 | 142GB；**lineage manifest 待 Codex**、下載待授權；ODC-By |

注意：7 families 是小叢集數 → bounded evidence、family bootstrap、寬區間，不宣稱普遍方法優越。

---

## 7. 評估指標

- **Primary（部署風險）**：每 generator family `P(accepted 且判 real | 實為 fake, g)`，再 family-macro average。
- **Secondary**：coverage、selective risk / risk violation、逐 family、eAURC/error-AUROC、AUROC/EER、calibration（Brier/NLL/ECE 僅輔助，不代替 ranking）。
- **不確定性**：family bootstrap / hierarchical interval，誠實呈現 ~7 clusters 的寬區間；不用 utterance-level p-value 宣稱普遍優越。
- **部署**：parameter count、CPU latency、peak RAM、model size。
- **注意**：risk–coverage/AURC 是 target score sweep（ranking quality）；source-fixed `(q,t)` leakage 是 operating-point transfer（主結果）——兩者分開報，不互相替代。

---

## 8. Phase-0 derisking 稽核（當前執行步驟）

越前面越便宜，前兩階不需 142GB 大檔：

- **Stage 0.0**：建環境 + 復現公開 teacher，ASVspoof19 LA eval 對上論文 EER。（推論級，數小時）
- **Stage 0.1（H1a 便宜首探）**：加截短 probe（不訓練）；各模型 source-dev 凍結 `(q_m,t_m)`；在 **In-the-Wild** 看固定操作點有無退化跡象。有 → 值得投 confirmatory；無 → 提早重估，省下大檔。（推論級，數小時）
- **Stage 0.2（H1a confirmatory）**：ASVspoof 5 C00（7 families，generator-macro）。前置：Codex lineage manifest 通過 + 作者授權下載。
- **Stage 0.3（H1b）**：加 source-dev TS + Platt sensitivity；簡單校準能修好 → **kill H2**；修不好 → H2 有空間，才進 Phase 1。

**決策閘**：見各 stage。核心——H1a 無退化→重估；H1b 簡單校準已足→退回量測（低於作者 bar→轉向）；H1a 成立 + H1b 顯示不足→才設計 H2。

---

## 9. 一年範圍

**做**：一個 source 訓練設定、一個 primary holdout（ASVspoof5 C00）、一個 teacher + 至多兩個輕量 transformation、一個 proposed 機制、score/family-level 主分析、一份三態輸出 + latency 可行的 reference deployment artifact。

**不做**：多 backbone 大矩陣、六種 uncertainty 方法排行榜、手機 App/完整瀏覽器產品、human-subject study、多語全面泛化、partial deepfake、對抗攻擊、新 foundation model 訓練、任何用 holdout label 調參的步驟。

---

## 10. Kill / pivot 條件與有用的負結果

- **Kill**：matched discrimination 後無 H1a 退化；退化由 teacher 在 target 失效或 dataset shortcut 解釋；有效 family 數不足；需看 holdout 才能選 score/threshold。
- **Kill H2**：ordinary KD（或 + recalibration）已保住 selective behavior；proposed loss 無穩定增益。
- **有用的負結果**：EER 保留但 fixed-threshold transfer 系統性失效，且哪種 source-only 修法能/不能跨 generator 轉移 → 對 edge ADD 評估標準的具體修正 + model card。**但作者已表明純量測/負結果低於期待貢獻**——屆時回到候選題比較，不硬把負結果說成目標達成。

---

## 11. 算力預算（單張 RTX 4090，24GB）

- Phase-0 稽核以**推論 + 截短 probe** 為主，幾十 GPU-hour 級。
- 全論文核心（含 H2 一個 student 訓練、baselines）預估遠低於 500 GPU-hour；不 pretrain foundation model、不做組合爆炸矩陣、大資料集一律分層抽樣。
- teacher/student 用現成 checkpoint；frozen backbone + 特徵快取省算力。

---

## 12. 誠實風險聲明（必讀）

1. **貢獻 bar 押在 H2**：這篇能否「超過量測」完全取決於 H2 打贏 `ordinary KD + source-dev recalibration` 等 baseline，而該 baseline 結果**未知、只能實測**（Ovadia 2019 顯示 post-hoc 校準常在 shift 下失效——對我們有利但不保證）。**pilot 前未 derisk。**
2. **方法 novelty 窄**：廣義 reliability-preserving 壓縮法已存在；H2 必須是 ADD-specific、針對 generator-group external transfer 的機制，且過 closest-work gate，否則降為 application。
3. **統計檢定力**：~7 generator families 是小叢集，方法普遍性主張受限。
4. **holdout 乾淨度**：ASVspoof5 lineage/shortcut 待 Codex manifest 核實；未過不解鎖 confirmatory。

---

## 13. 當前狀態與下一步

- **決策**：跑 H1a/H1b derisking 稽核（作者裁定）。
- **Codex 進行中**：ASVspoof 5 C00 lineage/shortcut manifest（handoff `2026-07-18-1030`）。
- **待作者解鎖**（開跑 Stage 0.0 的前置）：(a) 計算環境（是否此 RTX 4090 機器、Python/CUDA 是否可用）；(b) 授權下載 ASVspoof19 LA + In-the-Wild（數 GB）；ASVspoof5（142GB）延到 manifest 過 + 明確授權；(c) 公開 checkpoint 來源。
- **暫停中**：full pilot、142GB 下載、任何訓練。

---

## 14. 關鍵前作（references，Codex 已查證）

- 量測/可靠性：Salvi (ICASSP 2023)；Pascu (Interspeech 2024)；FADEL (ICASSP 2025)；Zhou & Wang (arXiv 2606.21584)；Schäfer & Steinebach (ICWSM 2026)；Kwok (Interspeech 2025)。
- 輕量/壓縮 ADD：DK-CAST (Discover Computing 2025)；FTDKD (TASLP 2024)；Detecting Audio Deepfakes on the Edge (arXiv 2606.30780)。
- 壓縮×可靠性（現象/方法/指標）：Zhong (ACL 2025)；DistilDoc (ICDAR 2024)；Mitra (CVPRW 2024)；KD(C) (ACCV 2024)；BN3 (CVPR 2021)；EnD² (NeurIPS 2021)；Kim (Interspeech 2021)；Niu (NeurIPS 2022)；Xu (ICPR 2020)。
- 校準轉移：Ovadia (NeurIPS 2019)；Multi-domain TS (NeurIPS 2022)；TransCal (NeurIPS 2020)。
- 資料集：ASVspoof 2019 LA；In-the-Wild；DFADD (arXiv 2409.08731)；ASVspoof 5 (arXiv 2502.08857)。

（各連結詳見 `research/validations/` 對應查證檔。）
