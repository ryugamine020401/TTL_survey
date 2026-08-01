# 五方向貢獻、RQ 與指標查證

日期：2026-07-23  
查證對象：`research/ideas/2026-07-23-five-directions-contributions-rq-metrics.md`  
研究模式：Validate  
問題：原稿中的先作定位、無先作／第一個主張、方法保證、指標解釋與部署／法規敘述，是否足以作為 proposal 的已查證依據？

## 結論

**總判定：未通過整份查證。** 原稿適合作為五方向的「proposal 設計草案」，但不應保留「所有內容均已查證」的聲明。五方向各有可保留部分，但也有直接遭先作反證、數學定義不一致，或目前只能標為 Unknown 的核心主張。

方向層級判定：

| 方向 | 判定 | 可保留的核心 | 必須撤回或縮限之處 |
|---|---|---|---|
| D1-B sequential | **Promising but not yet validated** | 「source-frozen、lineage-disjoint、整通話 policy risk、資料相依停止」的交集，在本次搜尋未找到直接同題先作 | 「框架貢獻無條件成立」與「第一個」尚不可用；optional-stopping inflation 與主 leakage 指標方向不一致；LTT 保證不能外推為未知生成器保證 |
| D1-A full-utterance | **Partially verified；五者中最穩** | 輕量模型的 source-frozen selective-policy 外部轉移；拆解 discrimination、ranking、operating point、calibration | DK-CAST「只報 EER/latency」不正確；`Δ_light` 目前不是 double difference；Zhou & Wang 已直接碰撞 threshold transfer |
| D3 attacker cost | **Major revision required** | 對固定 threat model 報告「找到成功 laundering recipe 的最低觀察成本」可能有殘餘空間 | laundering 並非無先作；「物理可逆性下界」無理論錨；neural codec 不等於不可逆 killer move；多種成本不能未定義就合成單軸 |
| D4 zh-TW factorial corpus | **Exact gap unknown；causal claim not supported** | zh-TW、詐騙語意、時長、情緒、通道的精確交集，本次未找到直接同題先作 | 「所有先作皆單軸」為假；UTMOS+ECAPA matching 不能識別 causal quality-adjusted gap；無音訊發佈時較像 protocol/manifest 而非可重用 corpus |
| D5 reliable payload / Article 50 | **Core novelty claims refuted** | 可縮成固定 watermark family 下的 payload–reliability–quality frontier | AudioMarkBench 已用已知植入訊息；RAW-Bench 已量 capacity、bit/full-message accuracy；Article 50 audio 已有 EC 技術報告；「零 bits 即政策反證」不成立 |

**建議：** 若現在需要從這份稿件拿一個方向進 proposal，D1-A 仍是證據最穩的基線；D1-B 可以作為需先過 formalization gate 的增量方向，而不能先宣稱是已成立的主貢獻。D3–D5 應先重寫貢獻邊界再比較。

## 查證方法與限制

- 搜尋日期：2026-07-23。
- 優先使用原始論文、正式 proceedings、官方資料集頁、平台文件及 EU 官方文件。
- 搜尋焦點包括：audio deepfake 的 sequential／prefix／anytime selective prediction、source-frozen policy transfer、laundering／replay／codec robustness、中文電詐與情緒語音資料、audio watermark capacity，以及 AI Act Article 50 audio marking。
- 「本次未找到」只表示在記錄之關鍵字、資料庫與相鄰先作中未找到直接命中，**不等於證明不存在**。
- 新符號、新名稱或把既有量相減，不會自行構成方法或量測創新；仍須證明它回答一個前作沒有回答、且可辨識的研究問題。
- 法規部分只是研究定位查證，不是法律意見。

## D1-B：來電場景 sequential selective policy

### 先作與部署查證

**Verified：** “Hi!” 是 ICASSP 2026 論文，測試 0.5、1、1.5、2 與 4 秒固定截斷，重點是 ultra-short ADD 的 EER、效率與通訊退化；論文未建立棄權或 finite-sample policy risk framework。這支持原稿對它的基本描述，但不能單憑此文推出「本研究為第一個」。  
來源：[“Hi!”: Toward Efficient and Lightweight Deepfake Speech Detection in Real-World Communication Scenarios](https://arxiv.org/abs/2601.19573)。

**Verified：** RTCFake 已研究真實 RTC 平台、offline/online 配對、未見平台與噪音，故「真實通話通道」本身不是新缺口。  
來源：[RTCFake, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.285/)。

**Partially verified：** 本次沒有找到同時滿足「ADD、prefix sequential decision、nonabsorbing clean、abstain/escalation、source-frozen、unseen-generator external transfer」的直接先作。這使精確交集值得繼續驗證，但目前證據只允許：

> 在 2026-07-23 所記錄的搜尋範圍內，未找到直接評估 source-frozen sequential selective policy 在 lineage-disjoint 未見生成器上整通話風險轉移的 ADD 研究。

不能改寫成「第一個」或「框架貢獻無條件成立」。

**Verified, with scope：** Android 官方文件顯示，語音通話 capture 需要預裝且具 `CAPTURE_AUDIO_OUTPUT` 的 privileged app；一般第三方 app 並不能假設可讀取 call audio。Pixel 的 scam detection 則提供 on-device、ephemeral audio、不錄音／不上傳的產品先例。因此「OS 特權、on-device、不留存」是有平台先例的部署位置，但不是一般 app 可行性，也不是 ADD 任務的新穎性證據。  
來源：[Android—Sharing audio input](https://developer.android.com/media/platform/sharing-audio-input)、[Google Security Blog—AI-powered scam detection](https://blog.google/security/new-ai-powered-scam-detection-features/)。

**Unknown：** 「8 kHz post-channel」是實驗 threat model，不是已查證的普遍來電部署條件。它應寫成研究範圍，並說明是否排除 wideband VoLTE/VoNR，而非列為已驗證的唯一部署點。

### 形式化問題

**Refuted as currently defined：** 原稿把 spoof 設為唯一 absorbing stop，clean 則 nonabsorbing；同時將主風險定義為：

`L_CR^seq = P_fake(整通從未觸發 spoof evidence 且未升級)`。

在相同 threshold rule 下，多看幾個 prefix 只會增加 fake call 至少一次被觸發的機會，因此「從未觸發」的 fake leakage 不會因 repeated looks 而發生典型 multiplicity inflation。真正會被 repeated looks 放大的通常是：

`P_bona(任一 prefix 誤觸 spoof)`，

也就是 bona-fide call 的整通話 false-alarm probability；若存在錯誤的 absorbing clean commitment，才會有另一種錯誤停止風險。原稿卻明定 clean 不吸收。因此「optional-stopping inflation＝逐前綴名目承諾與 policy 實際洩漏之差」與主 endpoint 的方向不一致。

應先分開定義：

- `R_fake^call = P_fake(no spoof alarm before hangup and no escalation)`；
- `R_bona^call = P_bona(any spoof alarm before hangup)`；
- 若有 escalation，再另外報 `P(escalate | class)` 與 escalation 的成本／有效性；
- `inflation_bona = R_bona^call - max_t P_bona(alarm at t)`，或用預先指定的 pointwise comparator；
- coverage 到底是「最後自動給出 clean/spoof 的比例」、還是「未升級的比例」，不可混用。

**Partially verified：** Learn-then-Test 可在 i.i.d./exchangeable calibration setting 下提供 finite-sample risk control，但不能保證 source 校準後在未知生成器 distribution shift 下仍守住 α。未知生成器上的失效正是要被量測的 outcome，不是 LTT 已提供的 theorem。  
來源：[Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control](https://arxiv.org/abs/2110.01052)。

因此 proposal 應區分：

1. source/exchangeable population 內的形式保證；
2. lineage-disjoint target family 上的 empirical transfer audit；
3. 若希望對 family shift 有保證，需要另加明確的 shift assumptions 或 distributionally robust theorem。

**Unknown：** `τ*(α)`、`Δ_light^seq` 可作為預先定義的 estimand，但本次沒有證據支持它們本身是「三個新的量測貢獻」。尤其 `Δ_light^seq` 必須先定義差分兩端和反事實比較，不能只靠命名。

### 可用的縮限版本

**Bounded contribution：**

> 建立並外部稽核一個 source-frozen 的 call-level sequential selective policy，分別控制／量測 fake-call miss、bona-fide ever-false-alarm、escalation 與 latency；比較資料相依停止是否在 lineage-disjoint generator families 上優於預先指定的固定截斷策略。

**最小先行測試：**

1. 在玩具分布與 source-dev 上寫出 policy state machine 和四個 mutually exclusive terminal outcomes。
2. 用 simulation 證明或反證 proposed inflation metric 的單調性。
3. 比較 fixed-τ、alpha-spending／confidence-sequence 式 rule、簡單 persistence rule。
4. 若 sequential rule 不能在預先指定的 call-level false-alarm constraint 下 Pareto 改善 latency/coverage，停止把 D1-B 當主題，退回 D1-A。

## D1-A：完整語音 selective-policy transfer

### 先作查證

**Refuted in wording：** DK-CAST 並非「只報 EER/latency」。正式論文報告 accuracy、F1、precision、recall、EER、min t-DCF、score distributions，以及 mobile CPU latency、參數量與 GFLOPs。較精確的差異是：本次未在 DK-CAST 找到 source-frozen selective policy、AURC、coverage-risk curve 或 lineage-disjoint operating-policy transfer。  
來源：[DK-CAST, Information Retrieval Journal, 2025](https://link.springer.com/article/10.1007/s10791-025-09746-4)。

**Verified：** FTDKD 是 2024 年 IEEE/ACM TASLP 論文，主軸是以 feature translation distillation 壓縮 ADD，常用指標為 EER/min t-DCF；這支持把它當 lightweight KD baseline，但不支持把「重現 baseline」單獨視為足夠強的論文貢獻。  
來源：[FTDKD, IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/10747292)。

**Verified and important collision：** Zhou & Wang 2026 已直接以 LA source threshold 轉移到 ITW/DF21，報告 HTER/FRR/FAR，並比較七種無標籤校正。它沒有 lightweight student 或 abstention，但已碰撞「operating-point/threshold transfer」核心。必須標成 **2026 preprint**，並將殘餘缺口縮到 source-frozen selective policy、compression delta、family-macro external audit。  
來源：[Unsupervised Score Correction for OOD Robust Deepfake Speech Detection](https://arxiv.org/abs/2606.21584)。

**Verified as adjacent generic work：** selective classification under distribution shift 已有通用方法；ADD 論文必須說明 domain-specific failure mechanism，而不是把 AURC／abstention 本身當新穎性。  
來源：[Selective Classification Under Distribution Shifts, TMLR 2024](https://openreview.net/forum?id=dmxMGW6J7N)。

**Verified contrary evidence, scoped：** Cattelan & Silva 在 ImageNet classifier 的 NeurIPS 2023 workshop 研究發現，selective performance 很大程度可由 accuracy 及其 shift degradation 解釋。這是保留 H1 可被否證的重要反證，但它是 vision workshop evidence，不可當作 audio 已成立的定律。  
來源：[NeurIPS 2023 workshop poster](https://nips.cc/virtual/2023/80532)。

### 指標與論證問題

**Incorrect label：** 若 `Δ_light = G_student - G_teacher`，它只是 paired teacher-relative difference，不是 double difference；且原稿沒有定義 `G`。若要稱為 double difference，可用例如：

`Δ_light = (L_student,target - L_student,source) - (L_teacher,target - L_teacher,source)`。

這才隔離「學生相對教師的額外 transfer degradation」。若只關心 target，請改稱 teacher-relative gap。

**Requires conditions：** Temperature scaling／Platt scaling 對 rank-based selection 是 no-op，只在轉換嚴格單調、並在轉換後重新選 threshold 的條件下成立。它會改變 calibration，也可能改變固定數值 threshold 的 operating point；原稿不可無條件宣稱 no-op。

**Useful metric, not automatic novelty：**

`P_fake(accept ∧ classify real | fake,g)` 可直接表達 high-consequence leakage，但必須把 accept 定義為「自動決策、未 abstain/escalate」，並同時報：

- overall、fake、bona-fide coverage；
- family-macro leakage 與 family-level interval；
- bona-fide false rejection／false alarm；
- source-locked threshold 的 target drift；
- teacher/student matched discrimination 與部署預算。

### 可用的縮限版本

> 在固定 source-dev policy、lineage-disjoint generator-family 外部測試及 matched deployment budget 下，估計 lightweight student 相對 teacher 的 selective-risk transfer degradation，並判斷其是否超出 discrimination drop 可以解釋的部分。

**Stop/pivot condition：** 若 teacher/student 的 target selective gap 在 matched AUROC/EER 後消失，或由 accuracy/ranking drop 完整解釋，則撤回「lightweight 特有 policy fragility」機制主張；保留為有用負結果或只做 deployment replication。

## D3：attacker-cost laundering frontier

### 先作查證

**Refuted：** laundering robustness 並非只有 generic/random corruption 先作。IH&MMSec 2024 已在 laundering database 上比較七個 detector，涵蓋 noise、reverb、recompression、resampling 與 low-pass filtering。  
來源：[Can Audio Deepfake Detection Generalize?, ACM IH&MMSec 2024](https://arxiv.org/abs/2408.14712)。

**Verified adjacent threat：** ReplayDF 系統性量測 speaker–microphone replay，涵蓋多語言、TTS 與 109 組裝置，且觀察到 detector EER 顯著惡化。因而「物理播放／重錄」本身也不是新 threat model。  
來源：[Replay Attacks Against Audio Deepfake Detection, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/muller25_interspeech.html)。

**Unknown residual gap：** 本次未找到以明示 attack cost、成功門檻、固定 search budget 和 recipe-level reproducibility，建立 ADD laundering cost frontier 的已發表直接同題研究。可研究的是這個精確實驗設計，而非「首次研究 laundering」。

### 核心問題

**Unsupported：** 「physical reversibility lower bound」目前沒有 channel model、資訊量、可逆映射定義或可證下界。重取樣、編碼和播放雖可能丟失 waveform information，但不代表必然丟掉 detector-relevant evidence，更不代表必然提升 attack success。

**Refuted as an implication：** neural codec transcode 不是「不可逆 killer move」。不可逆只描述不能完美還原輸入；是否逃逸取決於 detector、codec artifact、訓練分布和 operating point。某些 detector 反而會利用 codec／vocoder artifact。

**Requires definition：** greedy search 找到一個成本 `c` 的成功 recipe，只能在固定 action space、成功準則和 scalar cost function 下，給出最優攻擊成本 `c* ≤ c` 的實證 upper bound。若搜尋沒找到，不能推論系統 robust；更強搜尋也可能改變曲線形狀和方法排序。

**Invalid aggregation unless specified：** 金錢、compute、wall-clock、instruction steps、查詢次數和所需設備是不同維度。除非預先指定交換率或 threat persona，不能合成一條自然的「attacker cost」軸。較安全的做法是 Pareto frontier 或分 threat persona 報告。

**Incorrect name：** 在 fixed FPR ≤ 1% 下報 recall 就是 TPR/recall at fixed FPR；若沒有 reject/coverage rule，不應稱為 selective recall。

### 可用的縮限版本

> 在預先固定的 laundering action space、攻擊者能力與多維成本向量下，估計可重現的 attack-success Pareto frontier，並比較 detector 排序是否隨 threat persona 與 channel recipe 改變。

**Stop/pivot condition：** 若 cost ranking 對合理的成本權重、search seed 或 action shortlist 高度不穩定，撤回單一 attacker-cost 曲線；改報 recipe-level robustness matrix 與 sensitivity analysis。

## D4：zh-TW scam-condition factorial benchmark

### 先作查證

**Refuted：** 「所有 prior 都是單軸」不成立：

- “Hi!” 同時研究 utterance duration 與 communication degradation。
- EmoFake 已研究英文／中文 emotional voice conversion。來源：[EmoFake, CCL 2024](https://aclanthology.org/2024.ccl-1.99/)。
- TeleAntiFraud-28k 已處理 telecom-fraud 的 audio-text semantics。來源：[TeleAntiFraud-28k](https://arxiv.org/abs/2503.24115)。
- CFSDD 資料卡已明示 Chinese speech deepfake、telecom-fraud、benign real vs fraudulent fake，以及 clean/noise/noise-suppression/codec 測試條件。其同行評審狀態與 exact dialect composition 仍需確認。來源：[CFSDD dataset card](https://huggingface.co/datasets/Izzyzlin/CFSDD)。

**Unknown exact gap：** 本次未找到完全相同的「zh-TW/Taiwan Mandarin × 詐騙語意 × 時長 × 情緒 × 通道」全因子 ADD benchmark。這是可繼續驗證的 dataset-context intersection，不等於四個軸各自沒有先作，也不能稱「scam semantic variable zero prior」。

### 測量與可重用性問題

**Not causally identified：** UTMOS 是 MOS prediction model，ECAPA embedding 是 speaker/identity proxy。用兩者 matching 最多能說「在兩個 proxy 接近後仍有 residual association」，不能識別「控制 TTS 品質後的 detector field failure」。UTMOS 的 OOD generalization 本身有限；近期 preprint 甚至展示可在維持 UTMOS score 時降低人類感知品質。  
來源：[UTMOS, Interspeech 2022](https://www.isca-archive.org/interspeech_2022/saeki22c_interspeech.html)、[Score-Preserving Attacks on UTMOS](https://arxiv.org/abs/2606.31105)。

若不做人類評聽，主張應縮成：

> detector error 與語意／情緒／時長／通道之關聯，在 UTMOS 與 ECAPA proxy adjustment 後是否仍存在。

不能寫成已經「排除低品質 TTS confounding」。

**Design risk：** 四軸、多 level、多 generator、多 speaker 的全因子設計會快速擴張；同一句／同 speaker／同生成器的重複樣本需要 mixed-effects 或 hierarchical analysis。若各 cell 由不同 TTS 或不同語料生成，axis effect 會與 generator、speaker、lexical content 混淆。

**Reusability concern：** 只發 recipes＋checksums、不發音訊，在雲端 TTS、模型版本或 preprocessing 改變後，可能無法重建相同 bytes。除非有可存取的凍結模型、seed、環境、授權和 deterministic pipeline，較準確名稱是「evaluation protocol/manifest」，不是可直接重用 corpus。

### 可用的縮限版本

> 建立一個授權與 lineage 明確的 zh-TW scam-condition evaluation protocol，以 crossed 或部分因子設計估計 semantics、emotion、duration、channel 及預先選定交互作用；所有結論限於已量測 generator/speaker population。

**Stop/pivot condition：** 若合法可發佈／可重建的 zh-TW audio lineage 不成立，或 factorial cells 無法在 speaker、text、generator 上合理 crossed，停止 corpus claim，改做小型 controlled diagnostic study。

## D5：watermark reliable payload 與 Article 50

### 直接反證

**Refuted：** AudioMarkBench 已以已知 ground-truth watermark message 評估 bitwise accuracy 和 detection，涵蓋多種 watermark 方法及 EnCodec 等擾動。因此「controlled implantation ground-truth anchor 是方法上的首次差異」不成立。  
來源：[AudioMarkBench, NeurIPS 2024 Datasets and Benchmarks](https://openreview.net/pdf/17301d982d1e5ab0f0511e202cae5e1c02701532.pdf)。

**Refuted／must narrow：** RAW-Bench 已明確把 capacity 定義為每單位時間的訊息 bits，將方法配到約 5 bps，並報 bitwise 與 full-message accuracy；它也顯示 neural codec 下多種方法可能接近隨機 bit accuracy。原稿不能說先作「只報 survival %」。  
來源：[RAW-Bench, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/ozer25_interspeech.html)。

尚可能存在的殘餘問題是：在固定 watermark family、品質約束、channel family、false-accept 與 block-error target 下，掃描 payload／ECC 得到 **operational achievable payload frontier**。不要未經 theorem 稱為 Shannon capacity。

**Refuted：** Article 50 audio machine-readability 並非「zero prior」。European Commission 於 2026-05-05 已發佈專門針對 AI-generated audio marking/detection 的技術報告；2026-07-20 又發佈 Article 50 最終 guidelines。  
來源：[EC—State-of-the-art methods for marking and detecting AI-generated audio content](https://op.europa.eu/en/publication-detail/-/publication/4f7b8585-4829-11f1-8095-01aa75ed71a1/language-en)、[EC—Guidelines on Article 50 transparency obligations](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems)。

**Verified, but misinterpreted：** Article 50(2) 要求 provider 使 synthetic audio 等 output 可被 machine-readable 標記並可偵測為 artificially generated/manipulated，且要求在技術可行範圍內 effective、interoperable、robust、reliable，同時考慮內容特性、成本與 state of the art；相關義務自 2026-08-02 適用。它並未等同要求 watermark 攜帶足夠 bits 以做 signed identity provenance。  
來源：[Regulation (EU) 2024/1689, Article 50 and Article 113](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)、[EC Article 50 FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)。

因此必須拆開三個任務：

1. detection：能否判定為 AI-generated/manipulated；
2. payload/provenance：能否解出 message 或 index；
3. authentication：能否以信任根、簽章及 key management 驗證來源。

這三者的 bits、錯誤率與威脅模型不同。

### 推論與政策問題

**Refuted：** 某幾種 watermark 在選定 channel、payload 和 decoder 下可可靠解出的 bits 為零，只能反證該方法族在該 bounded setting 的 operational payload；不能推出「政策層級不可行」或反證 Article 50，因為法條有 technically feasible、cost 和 state-of-the-art 等限定，也允許不同 marking/detection 技術。

**Unknown security value：** 「短 index＋本地 signed commitment」需要 threat model、信任根、key distribution、revocation、index collision、lookup availability、privacy 與 interoperability。若 verifier 的 commitment 只存在本地，不能自動構成跨平台 provenance。

### 可用的縮限版本

> 對選定 watermark families，在預先指定的 audio channel、品質、false-accept 和 block-error constraints 下，估計 operational reliable payload frontier，並將「AI-generation detectability」與「provenance/authentication payload」分開報告；Article 50 僅作 use-case motivation，不宣稱法律充分性或政策反證。

**Stop/pivot condition：** 若 payload sweep、ECC 和 false-accept control 相對 RAW-Bench 只增加更多 codecs，而沒有新的估計問題或設計洞見，則不應作為論文主題；可降為 benchmark extension。

## 對原稿的最小修訂清單

1. 把首頁「未新增未經查證的主張」改為「proposal hypotheses；各方向查證狀態見 validation audit」。
2. 刪除所有未附搜尋範圍與日期的「第一個」「零先作」「無條件成立」。
3. D1-B 先完成 state machine、call-level risk 與 optional-stopping 方向的形式化，再談 novelty。
4. D1-A 將 DK-CAST 描述改成「未報 source-frozen selective-policy transfer」，並承認 Zhou & Wang 是 operating-point transfer 的直接相鄰先作。
5. 將 `Δ_light` 改成真正的 source/target × student/teacher double difference，或改名 paired gap。
6. D3 刪除「物理可逆性下界」「neural codec killer move」，以 bounded multi-cost Pareto frontier 取代。
7. D4 刪除「所有 prior 單軸」；把 UTMOS/ECAPA 結論降為 proxy-adjusted association。
8. D5 刪除 ground-truth implantation 與 Article 50 zero-prior 主張；改以 RAW-Bench 之上的 payload–reliability frontier 定位。
9. 每個方向把「新指標」與「新研究問題的 estimand」分開；命名新量不等於方法貢獻。
10. 在任何選題決策前，把 supporting evidence 和 closest contradicting work 同列，不以分數取代證據。

## 建議的下一個最小驗證步驟

優先做 D1-B formalization kill test，因為它能最快決定主線是 B 還是退回 A：

1. 一頁 state machine：每個 prefix 的 action、terminal state、hangup action、escalation outcome。
2. 一頁 probability table：fake/bona 各自的 call-level miss、ever-false-alarm、coverage、escalation。
3. 在 synthetic scores 上比較 repeated looks 對兩類風險的方向，驗證 proposed peeking metric。
4. 明列 LTT 的 exchangeability assumption 與 target-shift audit 的界線。
5. 通過後才做 bounded novelty search；若不通過，就將 D1-A 保留為 proposal-final 形態。

本次查證不改動 `PROJECT.md`、`TASKS.md` 或 `DECISIONS.md`：尚無作者核准的新 scope 或 decision，且查證結果本身只要求修正證據狀態。
