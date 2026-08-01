# 碩士論文計畫書（D1-B｜來電串流版）

> 本文為候選方向 D1-B 的完整計畫書。**實驗尚未執行**：第 8.4 與第 9 節以「預期／推估」形式呈現，並以結果表骨架（空欄或以符號標示待填）呈現，嚴禁把假設性推論當成已得數值。novelty 一律採「在已記錄搜尋範圍內（2026-07-23）未找到直接同題先作」的措辭，不宣稱「第一個／首創」。本方向繼承 D1-A（proposal-final）之機器與資產，是其 sequential 推廣；若第一道形式化 kill test 不過，即退回 D1-A（見第 10 節停損）。

---

## 1. 論文題目

**中文**：來電串流下輕量音訊深偽偵測器之凍結序列選擇策略轉移

**英文**：Source-Frozen Sequential Selective-Policy Transfer of Lightweight Audio Deepfake Detectors for On-Device Call Screening under Unseen Generators

---

## 2. 研究背景

音訊深偽（audio deepfake）製造門檻持續下降，語音克隆已被包裝成「Scam-as-a-Service」在詐騙產業流通，侵蝕人們對電話與語音的信任。偵測器的部署形態也正從雲端大模型走向本機／edge 輕量模型（DK-CAST、FTDKD、瀏覽器外掛式截短 SSL 偵測），因為隱私、成本與可用性使雲端方案不適合一般大眾。

在**來電**這個高後果場景中，判斷必須即時、逐秒發生：使用者不能等整通講完才知道對方是不是合成語音。可即時取得雙向來電音訊流的部署點在平台層是受限的——iOS CallKit 與 Android 自 Android 10 起皆封鎖第三方 app 讀取蜂巢通話音訊，唯一乾淨的即時部署位置是 OS 特權／預裝系統 Phone app。Google Pixel 的 Scam Detection 即為此層先例：接到陌生來電時以 on-device AI 即時處理通話音訊、音訊不儲存不上傳、never leaves the phone's RAM。**須誠實劃界**：Pixel Scam Detection 偵測的是詐騙話術（內容語意），不是深偽語音，因此它只背書「部署位置」，不背書本論文的偵測任務。本論文全程只做離線模擬，不部署、不攔聽、不建電信 rig、不做真人實測。

在此背景下，串流偵測的核心科學問題不是「短音訊能不能分辨真假」，而是**「聽到第幾秒才有資格開口承諾」以及「這個凍結下來的承諾遇到訓練時沒見過的新生成器還守不守得住」**。

---

## 3. 當前領域遇到的問題與痛點

1. **短前綴下偵測器最弱、承諾最危險**：短 utterance 劣化是已被專門研究的現象（AASIST2 專攻短語音；社群通行數字為 <2 秒段 EER 常 >10%，2–4 秒才降到約 5% 量級）。頭 1–3 秒正是偵測器最不可靠、最需要棄權的區間，卻也是來電最需要及早判定之處。
2. **輕量化評估只看辨識力**：現行輕量化 ADD 研究幾乎只報 EER／AUROC／延遲／模型大小，未回答「壓縮後那條凍結的接受／棄權／判定規則遇到新生成器還守不守得住」。
3. **逐前綴校準會漏承諾**：串流下若對每個前綴各自校準門檻，資料相依停止（optional stopping）會系統性選中「分數路徑早穿越門檻」的通話，使名目承諾與實際風險脫節——這是統計 estimand 的陷阱，不是工程細節。
4. **靜音捷徑會毀掉整個前綴 benchmark**：ASVspoof 2019 LA 的 bona fide／spoof 前導靜音長度分佈不均，僅用前導靜音長度就能達 EER 15.1%。前綴評估把「檔案前幾秒」放大成整個判定依據，若不從語音起點對齊，量到的是靜音長度而非深偽證據。
5. **來電引入質變的攻擊面**：串流 VC 的 SOTA 延遲已低到能在同一通內先用真人開場數秒、再切合成語音，使「前綴→標籤」不再是良定義映射；若「未發現合成證據」被設為吸收停止態，攻擊者撐過乾淨前綴即取得永久綠燈。

---

## 4. 研究動機

**個人動機接到技術貢獻的因果鏈**：

> 手機接到可疑電話時，我希望能**及時**判斷對方是不是合成語音 → 判斷必須逐秒、在本機、低成本發生 → 必須輕量化、必須串流前綴 → 但輕量化＋串流不能只看短音訊準確率，要問「模型什麼時候才有資格承諾，且承諾在新生成器上守不守得住」 → 因此必須把「整通話的風險承諾」形式化，並稽核它在未見生成器上的轉移。

三態輸出對應能力邊界：`發現合成證據`（唯一吸收停止態，觸發即終局並升級人工／帶外查證）／`未發現合成證據`（**非吸收**，持續監聽至掛斷，不等於已驗證真人）／`證據不足，棄權`（綁定升級動作——回撥已知號碼、帶外查證，不靜默放行）。棄權綁升級同時也是隱私最小化論證：OS 級、本機、瞬態、不留存、anytime 早停與隱私 minimization 同構。

**明確不主張**：不驗證說話者身分、不做 adaptive／最佳化攻擊實驗、不做真人實測，故不宣稱降低受騙率。8kHz post-channel、on-device 為本論文的研究範圍與威脅模型，不是已查證的普遍來電部署條件（wideband VoLTE/VoNR 誠實列為 coverage 缺口）。

---

## 5. 先前相關研究的論文與統整

**(a) 最接近的工作（closest work）與誠實對照**
- **"Hi!"（Shi et al., ICASSP 2026, arXiv:2601.19573）**——頭號 closest work。針對 0.5–2.0 秒超短音訊、以「詐騙者開場問候」為場景，主打低 RTF、少參數、edge 部署。**重疊**：來電動機、超短前綴、輕量化三項全撞。**未覆蓋**：它把 0.5/1/2 秒當固定長度**分別評測**，不回答「聽到第幾秒才有資格 commit」，無棄權／selective policy，無凍結門檻下的風險承諾。**本文量的是「第幾秒有資格承諾」與整通話風險轉移，而非短音訊準確率。**
- **RTCFake（Findings of ACL 2026, arXiv:2604.23742）**——約 600 小時、經真實 RTC 平台傳輸的深偽資料集＋phoneme-guided consistency learning，評測含未見平台與噪音。**重疊**：真實通訊通道。**未覆蓋**：仍為 utterance 級離線判定，無早期判定、棄權、輕量化軸。**注意**：其資料集目前需挑戰賽註冊審核（gated），違反本論文免申請 hard gate，故排除於 critical path，僅開放後至多作 exploratory。

**(b) sub-utterance 時間解析度**：PartialSpoof 系（TASLP 2023, arXiv:2204.05177）標注細至 20ms，已發展成 manipulated-region localization 子領域。**關鍵區別**：它們是**事後回看完整音訊做定位**（「哪段是假」），非因果前綴上的早期判定（「何時有資格說」）。

**(c) 通道現實性**：Delgado et al.（arXiv:2509.26471, 2025）論證 raw deepfake 與經呈現通道（電話播放／注入）的深偽分佈差異是泛化失敗主因；但其方法依賴實體 calling pipeline，正是本論文硬約束禁止的路線——這反而支持「用 ASVspoof 5 離線通道條件替代」。

**(d) selective classification 與 shift**：El-Yaniv & Wiener（JMLR 2010）risk-coverage 理論；Selective Classification Under Distribution Shifts（TMLR 2024）為通用方法；Cattelan & Silva（NeurIPS 2023 workshop）顯示 selective 退化可能由 accuracy 及其 shift degradation 解釋——這是本文 H1 可被否證的重要反證（但為 vision workshop 證據，不可當作 audio 已成立的定律）。ADD 內的棄權工作多為非 streaming。

**(e) sequential / anytime 統計**：SAVI（Ramdas, Grünwald, Vovk & Shafer, Statistical Science 2023, arXiv:2210.01948）的 anytime-valid 建立在**跨樣本**的 test martingale 上，**不適用於單通話內高度相依的音框**，只能作跨通話部署監測的加分項。通話內資料相依停止的正確先例是 **Ringel et al., "Early Time Classification with Accumulated Accuracy Gap Control"（ICML 2024, arXiv:2402.00857）**：用 **Learn-then-Test（LTT, arXiv:2110.01052）**校準停止規則，給有限樣本、distribution-free 且條件在累積停止時間上的保證。SPRT-TANDEM（ICLR 2021, arXiv:2006.05587）放寬 SPRT 的 iid 假設，但誤差控制為漸近／啟發式，只能作 policy 基線。

**(f) ADD reliability / threshold transfer**：Zhou & Wang（arXiv:2606.21584, 2026 preprint）已直接稽核 operating-point / threshold transfer 與無標籤校正，但無棄權維度、無 streaming、無壓縮 delta。

**(g) 攻擊面**：StreamVC（arXiv:2401.03078）在 Pixel 7 上約 10ms 推論延遲、端到端約 70ms，證明真人開場後切 VC 是可執行威脅（非科幻）。

**殘餘 gap（bounded wording）**：在 2026-07-23 所記錄的搜尋範圍內，未找到同時具備 (i) 因果前綴上的 anytime 三態判定（非固定長度截斷評測）、(ii) source-frozen 且帶整通話風險承諾的棄權策略、(iii) 部署級輕量模型、(iv) documented lineage-disjoint 未見生成器評測 的 ADD 直接同題先作。此為待驗證交集，不改寫為「第一個」或「框架貢獻無條件成立」。

---

## 6. 研究問題（RQ）

採用查證修正後的**雙風險**版本（承諾轉移／sequential 附加值與 τ*／條件性修復）：

- **RQ1（承諾轉移）**：source 資料上凍結的 call-level sequential selective policy，其**雙承諾**——fake-call miss `R_fake^call ≤ α` 與 bona-fide ever-false-alarm `R_bona^call ≤ β`——在 documented lineage-disjoint 未見生成器上是否轉移？輕量化相對 teacher 的**額外**序列退化 `Δ_light^seq` 有多大？
- **RQ2（sequential 附加值與 τ*）**：資料相依停止相對「最佳固定截斷 τ」是否在 latency/coverage 上構成 Pareto 改善？最早有資格承諾的秒數 `τ*(α,β)` 落在第幾秒？逐前綴多看造成的 `inflation_bona`（掛在 bona-fide ever-false-alarm，見第 7 節）是否非零、方向是否如預測？
- **RQ3（條件性修復）**：若 RQ1 顯示承諾失效或 `Δ_light^seq` 過大，future-aware prefix 蒸餾（full-context teacher → prefix student）能否在**同部署預算**下把承諾修回？
- **RQ4（預先登記的對抗 stress，secondary）**：在 bona-fide→spoof 離線 splice、刻意短句、壓噪誘發棄權三種**靜態資料工序**（非 adaptive attack）下，切換後偵測延遲與「攻擊強度 vs 棄權率曲線」如何變化？此為 stress 條件與 secondary 指標，不升格為主 endpoint。

---

## 7. 方法論

### 7.1 call-level sequential selective policy 狀態機
- 前綴網格 `τ ∈ T = {τ₁,…,τ_K}`（K≤8），串流分數過程 `s_τ(x)=s(x_{≤τ})`，selector `u_τ(x)`。
- 凍結策略 `π_θ`，`θ = {(t_τ, q_τ)}`：在每個 τ，若 `s_τ≥t_τ 且 u_τ≥q_τ` 且方向為 fake → commit「發現合成證據」（**唯一吸收停止態，終局**）；若方向為 real 但證據充分 → 判「未發現」但**非吸收、繼續聽**；若證據不足 → **棄權綁定升級動作**；到 `τ_K` 或掛斷強制三態收尾。
- 停止時間 `T(x)` = 首次觸發 spoof commit 的 τ，是資料相依隨機變數。clean 永不停止監聽，直接回應「真人開場後中途切 VC」的病態標籤切換與綠燈機漏洞。

### 7.2 主 estimand 與雙風險（掛對方向）
分開定義、分開承諾：
- `R_fake^call = P_fake(整通從未觸發 spoof commit 且未升級)`——fake-call miss。
- `R_bona^call = P_bona(任一前綴誤觸 spoof commit)`——bona-fide ever-false-alarm。
- **雙承諾**：`UCB_{1-δ}[R_fake^call] ≤ α` 且 `R_bona^call ≤ β`。
- **inflation 指標掛在 bona-fide ever-false-alarm，而非 fake leakage**（查證已指出：在同一 threshold rule 下，多看幾個前綴只會增加 fake 至少一次被觸發的機會，故「從未觸發」的 fake leakage 不會發生典型 multiplicity inflation；真正被 repeated looks 放大的是 bona-fide 的整通誤觸）：
  `inflation_bona = R_bona^call − max_t P_bona(alarm at t)`（或用預先指定的 pointwise comparator）。
- `τ*(α,β) = min{τ : dev 上存在可行 (t_τ,q_τ) 使該桶條件承諾守住}`——研究輸出量，不是輸入假設。
- coverage 明確區分「最後自動給出 clean/spoof 的比例」與「未升級的比例」，並以下限＋UCB 聯合約束防「全棄權」與「全拖到 τ_K」兩種作弊。

### 7.3 輕量化額外退化（source/target × student/teacher 雙重差分）
```
Δ_light^seq = (R_fake^call,student,target − R_fake^call,student,source)
            − (R_fake^call,teacher,target − R_fake^call,teacher,source)
```
隔離「學生相對教師的**額外**序列 transfer 退化」，per-family 計算後再 family-macro；並列報 per-family 分量以求透明。

### 7.4 source-frozen policy fitting 與 LTT 校準的界線
同一約束最佳化 `argmax Coverage s.t. UCB[R_fake^call]≤α, R_bona^call≤β`，決策變數從 2 個變 2K 個 → 以單調／低維參數化（如 `t_τ` 單調遞減的兩參數族）抑制 dev 過擬合，family bootstrap 每次重擬整條曲線。**統計保證分層（必須誠實標注）**：
1. source／exchangeable population 內：LTT 式有限樣本、distribution-free 保證成立，δ 沿 τ 網格以 union bound 分配。
2. lineage-disjoint target family 上：LTT **不能**外推為未知生成器保證；shift 下的失效**正是被量測的 outcome**，不是 LTT 已提供的 theorem。
3. 若要對 family shift 有保證，需另加明確 shift assumptions 或 distributionally robust theorem（本論文不承諾）。
SAVI/e-process 不得宣稱於單通話內成立；僅限跨通話部署監測作 optional extension。

### 7.5 離線前綴重評分與 VAD 對齊
wav2vec2 為非因果架構，強制因果化會嚴重劣化。正確做法為**離線前綴重評分**：每個前綴獨立跑一次完整 forward，統計上等價於「非因果模型每秒對到目前為止的音訊重新推論」，RTF 成本誠實報告為部署可行性證據，不做 chunk-based 因果重訓。**前綴時間零點必須錨在能量式 VAD 偵測的語音起點**（不用 target labels，合規），並報告 trim／不 trim 雙版本，否則靜音捷徑會毀掉 benchmark；19LA 只能當 secondary。

### 7.6 encode-once 通道協定
**每 utterance 過一次完整通道（encode-once／decode-once，固定丟包軌跡 seed），前綴在解碼後波形上沿 20ms 幀界截取**。理由：(i) 語音編碼器僅有毫秒級 lookahead，per-prefix 重編碼會在截點產生真實通話中不存在的 flush/padding 偽影；(ii) 同一通話各前綴須共享同一 sample path（filtration 一致性），這是 §7.4 anytime 保證的前提；通道隨機性跨通話進入、非通話內。

---

## 8. 實驗

### 8.1 設計（五分資料切分＋前綴格點）
沿用 D1-A 五分切分防洩漏：A model-train｜B selector-train（out-of-fold correctness/cluster）｜C policy-dev（LTT 校準＋擬合 `(t_τ,q_τ)`＋驗 source 承諾）｜D exploratory target（僅 smoke test，不選方法/不調參/不改 endpoint）｜E confirmatory holdout（只做一次 final eval）。前綴格點 `τ ∈ {0.5,1,2,3,4,6,8}s`，自 VAD 語音起點起算（7 點，K=7≤8）。

### 8.2 資料集
| 角色 | 資料集 | 關鍵事實 |
|---|---|---|
| source anchor | ASVspoof 2019 LA（arXiv:1911.01601） | attack 偏舊；平均 2–4 秒＋靜音捷徑，僅作 source 與煙霧測試 |
| **primary confirmatory** | **ASVspoof 5（arXiv:2502.08857）C08–C11 電話通道條件** | C08 Opus-8k／C09 AMR-8k／C10 Speex-8k 窄帶＋C11 八組端到端 PSTN 撥打管線響應卷積；訓練集平均 11.92s、dev 平均 7.08s，支撐至 ~8s 前綴；未見生成器 lineage 已 audit；免申請、免 rig |
| γ 校準／robustness | ASVspoof 2021 LA（arXiv:2109.00535, Zenodo 4837263） | C1/C2/C5/C3 為同源 utterance 配對條件，量「模擬 codec→真實 PSTN」效能差作 γ 經驗上界；攻擊為舊生成器，不入主 confirmatory |
| backbone | wav2vec2-base（Baevski et al., NeurIPS 2020, LibriSpeech-960-only） | lineage-clean，ASVspoof 5 合規；禁用 XLS-R/-ll60k（與 eval 上游重疊） |
| 排除 | RTCFake（gated）、EVS（無開源編碼器） | 前者違免申請 hard gate；後者以 AMR-WB 近似 VoLTE，VoNR/EVS 列 limitation |
通道套件預先登記：{8kHz 重採樣, G.711, GSM-FR, AMR-NB, AMR-WB, Opus-NB, ASVspoof5 C11 IR, Gilbert-Elliott 丟包＋PLC}，皆 CPU 可做（ffmpeg）。

### 8.3 參數設定與算力
- 模型 3 個：teacher（wav2vec2-base＋輕 head）、student ×2（截層 KD 4–6 層版、更小版），維持 teacher/student 對照。
- 格點：`α`（fake-call miss 承諾）、`β`（bona-fide ever-false-alarm 上限）、`δ`（UCB 信心水準）、`τ` 網格 7 點；selector 參數/latency/RAM 計入部署預算。
- baselines（預先登記，調參只用 source）：frozen teacher｜最佳固定 τ 策略｜ordinary KD｜persistence rule｜（gate 過後）future-aware prefix 蒸餾（H2）。
- **GPU-h 粗估 ≤750**：訓練/蒸餾 3 模型 50–70＋主前綴評分 <250＋γ 校準 30–50＋splice 20–30＋SNR 20–30＋RQ3 條件性 200–300，單張 RTX 4090 可行；GPU 非瓶頸，形式化與日曆才是。

### 8.4 預期結果（預期／推估，結果表骨架，尚未執行）
> 下列所有數值欄位均為**待填（以 — 標示）**，文字為**預期／推估**，非既得結果。

**表 A：RQ1 承諾轉移（family-macro，E 集 final eval）**

| 模型 | R_fake^call (src) | R_fake^call (tgt) | R_bona^call (tgt) | 守住 α? | 守住 β? |
|---|---|---|---|---|---|
| teacher | — | — | — | —（預期 borderline） | — |
| student (4–6L) | — | — | — | —（**預期較易破 α**） | — |
| student (smaller) | — | — | — | —（預期最易破） | — |

`Δ_light^seq`（family-macro）＝ —（**預期 > 0**，即輕量化在承諾轉移上有額外退化）。

**表 B：RQ2 sequential 附加值與 τ***

| 策略 | E[T]（承諾秒數） | coverage | R_bona^call | inflation_bona |
|---|---|---|---|---|
| 最佳固定 τ | — | — | — | n/a |
| 資料相依停止 | —（**預期 ≤ 固定 τ**） | —（預期 ≥） | — | —（**預期 > 0**） |

`τ*(α,β)` ＝ — 秒（**預期落在 2–4s 區間**，因 <2s 前綴分數過不穩、無可行承諾點）。

**表 C：RQ4 對抗 stress（secondary）**

| stress 條件 | 切換後偵測延遲 | 棄權率 | R_fake^call 變化 |
|---|---|---|---|
| bona→spoof splice | —（預期非零延遲） | — | —（預期上升） |
| 刻意短句 | n/a | —（預期 coverage 崩） | — |
| 壓噪 | n/a | —（預期單調上升曲線） | — |

---

## 9. 結果分析與討論（預期走向／null 情境，尚未執行）

**RQ1（承諾轉移）——預期走向**：推估 `Δ_light^seq > 0` 且輕量 student 較 teacher 更易在未見生成器上破 α。*推測理由*：壓縮後 accuracy 與排序/校準脫鉤（跨領域證據如 Zhong ACL 2025、DistilDoc ICDAR 2024），`s_τ` 的絕對尺度平移使凍結門檻在新分佈失準，而短前綴的邊界幾何最脆弱。**null 情境**：若 matched AUROC/EER 後 `Δ_light^seq` 消失，或退化可由辨識力下降完整解釋（Cattelan & Silva NeurIPS 2023 W 的反證方向），則撤回「輕量化特有序列 policy fragility」機制主張，保留為有用負結果並觸發停損。

**RQ2（sequential 附加值）——預期走向**：推估資料相依停止在 (coverage, E[T]) 上 Pareto 改善最佳固定 τ，且 `inflation_bona > 0`（掛在 bona-fide ever-false-alarm 方向，符合查證修正）。`τ*(α,β)` 預估落在 2–4s。**null 情境**：若 `inflation_bona ≈ 0` 且自適應停止不支配最佳固定 τ，則 sequential 框架空心，退化為 "Hi!" 式短音訊評測——**這正是 kill 判準**，應停止把 D1-B 當主題。

**與 closest work 的比較解讀**：無論結果如何，本文與 "Hi!" 的差異是**問的問題不同**——"Hi!" 報固定長度上的短音訊 EER，本文報「第幾秒有資格承諾」與整通話雙風險轉移。因此即使 student 短前綴 EER 不勝 "Hi!"，只要 `τ*`、`inflation_bona`、`Δ_light^seq` 三量能被穩定量測且承諾行為可稽核，貢獻仍成立於 commit-time 統計判定層，而非短音訊準確率層。

**威脅有效性**：RQ4 的 splice/短句/壓噪為靜態資料工序，不進最佳化迴圈、不需真人，故不違反硬約束；但它們只能壓測 anytime estimand 對 mid-stream 切換的行為，無法涵蓋 adaptive perturbation 與棄權疲勞人因（後者只進 threat model 文字）。γ 校準（2021 LA C3）給出「模擬通道對真實 PSTN 系統性樂觀」的經驗上界；若 C3 退化巨大且與所有模擬條件無序關，則離線通道模擬支撐來電場景的敘事崩潰，退回 D1-A。

---

## 10. 總結

本計畫把「手機接到可疑電話能否及時判斷」的個人動機，形式化為一個可稽核的技術問題：建立 call-level sequential selective policy——spoof 為唯一吸收停止態、clean 非吸收監聽至掛斷、棄權綁定升級——分開控制並量測 fake-call miss（`R_fake^call`）與 bona-fide ever-false-alarm（`R_bona^call`）兩類整通風險，並稽核凍結 policy 在 lineage-disjoint 未見生成器上的轉移。部署想定錨於 OS 特權 on-device 篩選（8kHz post-channel）。方法論繼承 D1-A 的 lineage-clean backbone、KD 管線、UCB policy fitting 與 TS no-op 控制，是其嚴格 sequential 推廣，改錨損失趨近零。

**誠實停損**：本方向須先過**形式化 kill test（門一）**——在「spoof 吸收、clean 非吸收、splice 標籤切換」約束下寫出 state machine、四個互斥終端 outcome、synthetic 分數上驗證 `inflation_bona` 的方向與單調性、並明列 LTT 的 exchangeability 假設與 target-shift 界線。門一不過（做不出非平凡有限樣本保證），或 Phase-0 前綴 probe 顯示 1 秒前綴效能已≈全長（無「多聽有益」張力），即**退回 D1-A**，來電寫進 motivation／future work，回退損失 ≤3 週。

---

## 11. 未來展望

1. **跨通話部署監測**：SAVI/e-process 在跨通話層面可用，未來可把本論文的單通話 policy 外掛一層 per-round e-process 做串流風險監測（Conformal Selective Acting 方向）。
2. **wideband 通道**：VoLTE（AMR-WB 近似）與 VoNR/EVS 因無開源編碼器暫列缺口，未來取得合法編碼路徑後可擴充通道套件。
3. **因果串流架構**：本論文以離線前綴重評分為代理；chunk-based 因果重訓（chunk-mask／lookahead）為獨立的第二篇論文量級工作。
4. **真人與 adaptive 攻擊**：本論文排除真人實測與最佳化攻擊；未來在有 IRB 與電信合作的條件下，可把 splice/壓噪 recipe 升級為線上對抗評估。
5. **繁中詐騙情境**：與 D4 方向的 zh-TW 詐騙情境評測協定結合，檢驗承諾轉移在中文電詐話術下是否另有退化。

---

## 12. 參考文獻

> 僅列前文實際引用且已於來源中查證（2026-07-23）之文獻。Zhou & Wang 為 arXiv preprint，定稿時重查發表狀態。

**closest work / 場景與通道**
- Shi et al. "Audio Deepfake Detection at the First Greeting: 'Hi!'." ICASSP 2026. arXiv:2601.19573.
- RTCFake. Findings of ACL 2026. arXiv:2604.23742.（gated，排除於 critical path）
- Delgado et al. "On Deepfake Voice Detection — It's All in the Presentation." arXiv:2509.26471 (2025).
- PartialSpoof. IEEE/ACM TASLP 2023. arXiv:2204.05177.
- StreamVC. arXiv:2401.03078.

**輕量／壓縮 ADD 與 reliability / threshold transfer**
- DK-CAST. "Dynamic Knowledge Condensation with Audio-Selective Transformer for Audio Deepfake Detection." Discover Computing 2025. DOI:10.1007/s10791-025-09746-4.
- FTDKD. "Frequency-Time Domain Knowledge Distillation for Low-Quality Compressed Audio Deepfake Detection." IEEE/ACM TASLP 2024.
- Zhou & Wang. "When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors." arXiv:2606.21584 v1 (2026, preprint).

**短音訊與靜音捷徑**
- Zhang & Lu. "Improving Short Utterance Anti-Spoofing with AASIST2." arXiv:2309.08279.
- Müller et al. "Speech is Silver, Silence is Golden: …" ASVspoof workshop 2021. arXiv:2106.12914.

**sequential / anytime / selective classification**
- Angelopoulos et al. "Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control." arXiv:2110.01052.
- Ringel, Cohen, Freedman, Elad & Romano. "Early Time Classification with Accumulated Accuracy Gap Control." ICML 2024. arXiv:2402.00857.
- SPRT-TANDEM. ICLR 2021. arXiv:2006.05587.
- Ramdas, Grünwald, Vovk & Shafer. "Game-Theoretic Statistics and Safe Anytime-Valid Inference." Statistical Science 38(4), 2023. arXiv:2210.01948.
- El-Yaniv & Wiener. "On the Foundations of Noise-free Selective Classification." JMLR 2010.
- "Selective Classification Under Distribution Shifts." TMLR 2024.
- Cattelan & Silva. (matched-accuracy selective performance). NeurIPS 2023 workshop.

**壓縮×可靠性（跨領域）**
- Zhong et al. "Quantized Can Still Be Calibrated…" ACL 2025.
- DistilDoc. ICDAR 2024. arXiv:2406.08226.

**部署平台先例**
- Google. "Pixel Scam Detection"（on-device, ephemeral call audio）. Google support / Google Security Blog, 2025.
- Android Developers. "Sharing audio input"（第三方 app 無法讀取通話音訊；需 privileged app）.

**backbone / 資料集**
- Baevski et al. "wav2vec 2.0." NeurIPS 2020（`facebook/wav2vec2-base`, LibriSpeech-960）.
- ASVspoof 2019 LA. arXiv:1911.01601.
- ASVspoof 5. arXiv:2502.08857（含 C08–C11 電話通道條件）.
- ASVspoof 2021 LA. arXiv:2109.00535（Zenodo 4837263, ODC-By）.
