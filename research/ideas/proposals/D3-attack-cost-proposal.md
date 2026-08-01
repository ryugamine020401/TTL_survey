# D3 研究計畫書：被動語音深偽偵測之適應性洗刷攻擊成功成本前沿評估

> 撰寫日期：2026-07-23。本計畫書之 novelty 主張一律為 bounded wording，指「在 2026-07-23 所記錄的搜尋範圍內未找到直接同題先作」，不等於證明不存在。承重主張為「多維成本 Pareto frontier ＋ 偵測器排序穩健性」。凡引用皆經查證；查證依據見 `research/validations/2026-07-23-five-directions-contributions-rq-metrics-audit.md`。硬約束：一位碩士生、一年、單張 RTX 4090（24GB）、全程離線免通訊 rig、免 IRB，GPU-hour 總預算約 610。

---

## 1. 題目

- **中文**：《被動語音深偽偵測之適應性洗刷攻擊成功成本前沿評估》
- **英文**：*An Attack-Success Cost-Frontier Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

## 2. 研究背景

語音深偽偵測（audio deepfake detection, ADD）已成為對抗合成語音濫用的第一道被動防線。過去數年，以 AASIST、RawNet2 與 wav2vec2/XLS-R 前端為代表的偵測器，在 ASVspoof 2019 LA 等實驗室基準上可達到亞百分之一等級的等錯誤率（EER）。然而「實驗室分數」與「部署現場的抵抗力」之間有巨大落差：In-the-Wild 語料已顯示同一批偵測器在真實錄音上會退化數個數量級。

更關鍵的是，攻擊者面對的是一個被動、離線、可反覆試探的目標。合成語音在送達受害者之前，往往會經過一連串「洗刷（laundering）」後處理——重取樣、重壓縮、加噪、殘響、低通濾波、神經編解碼器（neural codec）轉檔——這些操作多半是零金錢、開源、一行指令即可完成的。若偵測器對這些廉價後處理不具抵抗力，機構部署它反而會製造「已受保護」的假象。本計畫在此背景下，把 laundering 從「防守方視角的隨機劣化量測」重構為「攻擊者視角的成本問題」。

## 3. 問題與痛點

1. **偵測器可能被廉價 laundering 擊破**：現行 benchmark 幾乎只回答「加了某種後處理後分數掉多少」，而不回答「攻擊者要付出多少成本，才能可靠地把分數壓到不可用」。前者是平均劣化，後者是攻擊者真正在意的預算。
2. **機構部署製造假安全感**：一個在乾淨 benchmark 上 EER 極低、卻在一次開源 codec 轉檔後崩潰的偵測器，若被電信商或平台當作防線，等於用一個一戳即破的東西替受害者背書。缺乏「攻擊成功成本」這個評估軸，採購方無從分辨哪些偵測器是真的難攻、哪些只是難得剛好沒被測到。
3. **成本語言尚未進入文獻**：既有 robustness 研究量的是劣化幅度，未以「明示的攻擊成本、成功門檻、固定搜尋預算與 recipe-level 可重現性」為軸建立攻擊成功成本前沿。

## 4. 研究動機

本計畫的動機是把採購方與監理方真正需要的問題講清楚：**不是「這個偵測器平均會掉多少分」，而是「讓它失效最便宜要付多少、付哪一種幣別（金錢、計算、掛鐘時間、操作步數），以及這種便宜到什麼程度是防守方用資料增強（data augmentation, DA）追得回、什麼追不回」。** 因變數自始至終是機器事實（對抗 laundering 下、固定操作點的偵測率），不需要真人受測、不需要 IRB、不會隨月份過期到無法複現。定位對受害者誠實且有限——不是宣稱能救誰，而是確保沒有機構拿一個廉價即破的偵測器當她的防線。

## 5. 先前研究統整

本計畫誠實承認 laundering／robustness 方向已有直接先作，殘餘缺口是「成本語言 ＋ 前沿幾何 ＋ 排序穩健性」，而非「首次研究 laundering」。

- **Laundering／robustness 先作（直接對照）**：IH&MMSec 2024 的 laundering database 研究已在 noise、reverb、recompression、resampling、low-pass filtering 等後處理上，系統性比較七個偵測器的泛化與劣化（Ballesteros 等人，*Can Audio Deepfake Detection Generalize?*，2024）。它量的是「劣化多大」；本計畫量的是「達成劣化最便宜付多少、付哪種幣」。
- **實體重放（相鄰威脅模型）**：ReplayDF 已系統性量測 speaker–microphone 實體重放對偵測器的衝擊，涵蓋多語言、多 TTS 與上百組裝置，顯示 EER 顯著惡化（Müller 等人，Interspeech 2025）。因此「物理重錄」本身也不是新缺口；本計畫聚焦離線、可重現的軟體 laundering 動作空間，而非實體 rig。
- **對抗音訊**：Carlini 與 Wagner 建立針對語音辨識的目標式對抗樣本（IEEE S&P Workshops 2018）；Malafide（Interspeech 2023）與 Malacopula（2024）進一步提出針對 ADD／ASV 反制系統的對抗性卷積雜訊與 Hammerstein 濾波後處理攻擊。本計畫定位不同：對抗音訊多為白盒、逐樣本、可微優化；本計畫刻意採「不需白盒梯度、以公開離線動作組成配方」的黑盒 recipe-level 搜尋，貼近真實攻擊者的低門檻工具箱。
- **Codec robustness**：neural codec 轉檔對訊號存活的衝擊已有專門量測（如 *Will They Survive Neural Codecs?*，Interspeech 2025，量 watermark 於 neural codec 下的存活）。本計畫將 codec 視為動作空間中的一類 laundering 動作，並以「DA 是否實測可恢復」而非任何資訊理論下界來刻畫其效果。
- **偵測器**：AASIST（Jung 等人，ICASSP 2022）、RawNet2（Tak 等人，ICASSP 2021）、wav2vec2/XLS-R 前端加後端（Tak 等人，Odyssey 2022）為本計畫的受測偵測器族。

## 6. 研究問題（RQ）

核心方法是**一套適應性洗刷攻擊成功成本評估協定**：固定一組公開偵測器、一個離線 laundering 動作空間與一個多維成本向量，對每個偵測器跑一次 recipe-level 貪婪（greedy）搜尋，三個 RQ 是同一次計算的三種讀法。

- **RQ1（成本前沿與幾何）**：使某偵測器的 TPR@FPR≤1% 跌破預先指定的可用門檻，最便宜的 laundering 配方，其**多維成本前沿**為何？該成本–TPR 曲線是懸崖（每加一點成本 TPR 陡降，防守方有著力點）還是緩坡（廉價逐步壓垮，等於裸奔）？greedy 搜尋在固定動作空間、成功準則與成本準則下，只提供最優攻擊成本的**實證上界** `c* ≤ c`；搜尋失敗**不得**推論偵測器 robust。
- **RQ2（DA 可恢復性）**：一條成功配方中，哪些 laundering 動作的效果可被 channel-aware DA **實測恢復**（訓練分布補上該類劣化後 TPR 回升），哪些不可？此為對每個動作的**經驗性標註**，不主張任何物理可逆性下界。
- **RQ3（排序穩健性）**：偵測器的相對排序是否隨 threat persona 的成本權重與配方 shortlist 而翻轉？若排序在合理權重範圍內穩定，該排序才可作為採購參考；若不穩，即為停損訊號。

## 7. 方法論

**（1）固定 action space（離線、公開、可重現）**：預先凍結一個 ≤8 個動作的 laundering 動作空間，全部為 ffmpeg-native 或 HuggingFace 開源工具（如重取樣、MP3/AAC/Opus/AMR-WB 重壓縮、加性雜訊、殘響、低通、EnCodec/DAC neural codec 轉檔），排除需編譯專利碼或需白盒梯度者。配方為動作序列，搜尋深度 ≤3。動作空間一經凍結即寫入協定，確保 recipe-level 可重現（只發配方與 checksum，不散布合成語音本體）。

**（2）多維成本向量（絕不合成單軸）**：每個動作標註一個成本向量，維度包含**金錢**（API/授權費，開源動作多為 0）、**計算**（GPU/CPU 秒數或 FLOPs）、**掛鐘時間**（wall-clock）、**操作步數**（配方長度／人力介入次數）。這些維度不可通約，因此**分開報告 Pareto frontier**，或在預先宣告交換率的前提下依 threat persona（如「零成本腳本小子」「有預算的專業洗稿者」）加權；**絕不**未定義就壓成單一「攻擊成本」軸。

**（3）recipe-level greedy 搜尋**：對每個偵測器，以 greedy（depth≤3、branching≤動作空間大小）搜尋能使 TPR@FPR≤1% 跌破門檻的最低成本配方。greedy 給出的是實證上界 `c* ≤ c`；更強的搜尋可能改變曲線形狀與偵測器排序，故所有結論限定於「此固定搜尋預算下」，並在討論中明列此界線。

**（4）DA 可恢復性實證標註**：對成功配方中的每個動作，訓練一個補上該類劣化的 channel-aware DA 對照偵測器，量 TPR 回升幅度，將動作經驗性地標為「DA 可恢復／部分可恢復／實測未恢復」。這是對「本批偵測器 × 本組 DA」的量測，不是資訊理論定理，也不宣稱任何動作「物理不可逆」。

**（5）可控植入（用於 artifact 存活，而非物理定理）**：以可控植入一個**已知的合成 artifact**到樣本中，追蹤該 artifact 在逐步套用配方動作後的**存活率**，作為「動作對偵測器可用證據的破壞程度」之經驗代理。此設計目的是量 artifact 存活，明確**不**用來論證任何物理可逆性下界或「neural codec 不可逆必殺動作」——這兩項主張已於查證中撤回，本計畫不復活。

**（6）指標**：主指標為 **TPR at fixed FPR≤1%**。因無 reject／coverage 規則，**不**稱為 selective recall。輔以多維成本向量、DA 恢復率、前沿幾何（懸崖／緩坡的曲率）。

## 8. 實驗

### 8.1 設計

單一貪婪搜尋、三種讀法。對 4 個偵測器各跑一次 recipe-level greedy 搜尋，輸出：每個偵測器的多維成本 Pareto frontier（RQ1）、成功配方逐動作的 DA 可恢復性標註（RQ2）、跨 persona 權重的排序穩健性矩陣（RQ3）。全程 frozen checkpoint、零重訓（DA 對照臂除外，且以固定預算計入結帳單）。

### 8.2 資料集、偵測器與動作空間

- **資料集**（全部公開、離線可得、免 rig）：
  - **CodecFake+**（2025，HF `CodecFake/CodecFake_Plus_Dataset`，MIT）——laundering 主對象與確認池，分層抽 20k 確認／10k 搜尋；涵蓋 neural codec 與 codec-based 生成系統，使被打的樣本本身即當代 codec 世代 fake。
  - **DFADD**（2024，HF `isjwdu/DFADD`，MIT，用 2025-04 修正版）——unseen-generator 軸，抽 20k／10k；把偵測器面對的 fake 升到 diffusion／flow-matching 範式。
  - **ASVspoof 2019 LA**——in-domain 種子與 frozen checkpoint 之訓練分布，不換（換即重訓，違反 frozen 約束）。
  - **In-the-Wild**——真實錄音 real 類與第一週 smoke-test（37.9 小時，一次前向約 10 分鐘）。
- **偵測器（4 個）**：AASIST、RawNet2、wav2vec2/XLS-R 前端＋後端、自建 Mahalanobis-on-SSL baseline（支撐 RQ3 的 SSL vs 手工特徵比較）。全部使用 ASVspoof 2019 LA 訓練之公開權重。
- **動作空間（≤8）**：ffmpeg-native／HF 開源動作，配方深度 ≤3。已排除需編譯專利碼之 EVS/AMR-WB 專利路徑與白盒 PGD。

### 8.3 參數、搜尋預算與 GPU-hour

- 搜尋：greedy，depth≤3、branching≤8；每偵測器一次；成功門檻＝TPR@FPR≤1% 跌破預先指定可用線。
- 成本向量：金錢／計算／掛鐘／步數四維，分開報或依 persona 權重（權重於分析前宣告）。
- CodecFake+（101 GB）只下載一次、共用一份 20k 分層抽樣。
- **GPU-hour 結帳單（合計 610）**：偵測器復現 40 ＋ baseline 對照 40 ＋ laundering 前處理 60 ＋ 可控植入 45 ＋ greedy 搜尋前向 130 ＋ tandem 轉檔 90 ＋ 消融 65 ＋ 30% 緩衝 140 ＝ **610 GPU-h**，真餘裕約 40%。日曆而非 GPU 為主要瓶頸。
- **一年時程**：Q1 復現 4 偵測器＋建抽樣池＋凍結動作空間與多維成本向量＋baseline 平均劣化對照（保底：攻擊面地基＋「最壞情況嚴格重於平均」）。Q2 可控植入 artifact 存活圖譜＋DA 可恢復性實證標註（保底：可恢復性圖譜可獨立成篇）。Q3 recipe-level greedy 成本前沿搜尋（RQ1）＋成本–TPR 曲線幾何（RQ1）＋排序穩健性（RQ3）。Q4 消融＋跨偵測器地圖整合＋負責任發布（只發配方與 checksum）＋寫作。

### 8.4 預期結果（表骨架＋假設推論；所有數值待測，標「預期／推估」）

以下為**計畫書階段的表骨架與方向性假設推論**，數值一律以「—／待測」佔位，不捏造。

**表 A（預期）——各偵測器攻擊成功成本上界（RQ1）**

| 偵測器 | 金錢成本 c*₍$₎ | 計算成本 c*₍compute₎ | 掛鐘 c*₍wall₎ | 步數 c*₍steps₎ | 曲線幾何（懸崖/緩坡） |
|---|---|---|---|---|---|
| AASIST | —／待測 | —／待測 | —／待測 | —／待測 | —／待測 |
| RawNet2 | —／待測 | —／待測 | —／待測 | —／待測 | —／待測 |
| XLS-R 後端 | —／待測 | —／待測 | —／待測 | —／待測 | —／待測 |
| Mahalanobis-SSL | —／待測 | —／待測 | —／待測 | —／待測 | —／待測 |

*假設推論（推估）*：由於多數開源 laundering 動作金錢成本趨近 0，前沿**預期**主要在「計算／掛鐘／步數」三軸展開，金錢軸退化；**推估** neural codec 轉檔類動作因步數少、金錢為 0，可能落在多個 persona 的前沿上，但其能否壓垮各偵測器須實測，不預設結論。

**表 B（預期）——成功配方逐動作 DA 可恢復性（RQ2）**

| 配方動作 | 對 TPR 之衝擊（預期方向） | DA 後 TPR 回升（待測） | 經驗標註 |
|---|---|---|---|
| 重取樣 | 下降（推估較小） | —／待測 | 可恢復／部分／未恢復（待測） |
| 傳統 codec 重壓縮 | 下降 | —／待測 | （待測） |
| neural codec 轉檔 | 下降（推估較大） | —／待測 | （待測） |

*假設推論（推估）*：**預期**部分通道型劣化（如傳統 CELP 類重壓縮）在補上對應 DA 後 TPR 明顯回升，標為「可恢復」；neural codec 轉檔是否可由 DA 恢復**須實測**，不預先斷言不可恢復。

**表 C（預期）——排序穩健性矩陣（RQ3）**

| threat persona | 偵測器排序（由難攻到易攻，待測） | 排序是否翻轉 |
|---|---|---|
| 零成本腳本小子（步數/金錢權重高） | —／待測 | —／待測 |
| 有預算專業洗稿者（計算權重高） | —／待測 | —／待測 |

*假設推論（推估）*：若排序在合理權重範圍內穩定，**預期**可提出一份可供採購參考的偵測器難攻度排序；若 RQ3 顯示排序對權重／seed／shortlist 高度敏感，則觸發停損。

## 9. 結果分析與討論

- **成本定義敏感度**：多維成本向量的每個維度都有量測不確定性（GPU 秒數受硬體與批次影響、步數的粒度取決於動作切分）。分析將對成本定義做敏感度分析——變動維度量化方式、persona 交換率與門檻位置，檢查前沿形狀與排序結論是否穩定。凡結論隨成本定義改變者，一律標為「定義相依」，不上升為一般性宣稱。
- **greedy 上界的界線**：所有成本數字都是固定搜尋預算下的實證上界 `c* ≤ c`。搜尋未找到便宜配方，只代表「在此動作空間與 depth≤3 下沒找到」，**不**代表偵測器 robust；更強搜尋可能使前沿內移、使排序改變。此界線在討論中反覆聲明。
- **懸崖 vs 緩坡的部署意涵**：若曲線為懸崖，防守方在陡降點附近有著力空間；若為緩坡，代表現行被動偵測在該動作維度上近乎裸奔，對部署方是直接警告。
- **排序不穩的停損情境**：若成本排序對合理成本權重、search seed 或 action shortlist 高度不穩定，即撤回「單一攻擊成本前沿／單一難攻度排序」的承重主張，改報 **recipe-level robustness matrix ＋敏感度分析**——這是預先寫入計畫的成篇退路，仍是有用的負結果（等於證明「攻擊成本排序本身不穩」也是對採購方的重要情報）。
- **與先作的關係**：本計畫不宣稱首次研究 laundering（IH&MMSec 2024 已比較七偵測器）或首次研究重放（ReplayDF 2025 已量測）；貢獻邊界嚴格限定於「以明示成本／成功門檻／固定搜尋預算／recipe-level 可重現性建立攻擊成功成本前沿，並檢驗排序穩健性」。

## 10. 總結

本計畫把 audio ADD 的 laundering robustness 從「防守方視角的平均劣化」推進到「攻擊者視角的多維成本前沿」，以固定動作空間、多維成本向量與 recipe-level greedy 搜尋，對四個公開偵測器輸出攻擊成功成本的實證上界、DA 可恢復性的經驗標註，以及跨 persona 的排序穩健性。全案離線、免 rig、免 IRB，GPU-hour 約 610，一人一年可獨立完成，且在承重主張失效時有預先寫好的成篇退路（robustness matrix ＋敏感度分析）。

## 11. 未來展望

- 將 greedy 上界收緊為更強搜尋（beam／學習式搜尋）下的更緊上界，量化前沿隨搜尋預算的移動。
- 把離線動作空間延伸到實體重放與真實通訊通道（需 rig，超出本計畫離線約束），與 ReplayDF 類實測對接。
- 將白盒對抗後處理（Malafide／Malacopula 類）納入動作空間的成本比較，回答「白盒梯度值多少成本、換多少額外攻擊力」。
- 把成本前沿轉為防禦方的標準壓力測試套件，供後續 DA／偵測器設計研究作為統一評估。

## 12. 參考文獻

> 僅列查證過之引用（查證日 2026-07-23）。

1. Ballesteros, D. M. 等人，*Can Audio Deepfake Detection Generalize?*（ACM IH&MMSec 2024；laundering database 比較七偵測器）。arXiv:2408.14712。
2. Müller, N. 等人，*Replay Attacks Against Audio Deepfake Detection*（ReplayDF，Interspeech 2025）。ISCA Archive: interspeech_2025/muller25_interspeech。
3. Carlini, N. 與 Wagner, D.，*Audio Adversarial Examples: Targeted Attacks on Speech-to-Text*（IEEE Security and Privacy Workshops 2018）。arXiv:1801.01944。
4. Tak, H. 等人，*Malafide: a novel adversarial convolutive noise attack against deepfake and spoofing detection systems*（Interspeech 2023）。arXiv:2306.07655。
5. Todisco, M. 等人，*Malacopula: adversarial automatic speaker verification attacks using a neural-based generalised Hammerstein model*（2024）。arXiv:2408.09300。
6. Jung, J. 等人，*AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*（ICASSP 2022）。
7. Tak, H. 等人，*End-to-End anti-spoofing with RawNet2*（ICASSP 2021）。arXiv:2011.01108。
8. Tak, H. 等人，*Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation*（Odyssey 2022）。
9. Wang, X. 等人，*ASVspoof 2019: A large-scale public database of synthesized, converted and replayed speech*（Computer Speech & Language, 2020）。arXiv:1911.01601。
10. Müller, N. 等人，*Does Audio Deepfake Detection Generalize?*（In-the-Wild 語料，Interspeech 2022）。ISCA Archive: interspeech_2022/muller22_interspeech。
11. *Will They Survive Neural Codecs?*（watermark 於 neural codec 存活量測，Interspeech 2025）。arXiv:2505.19663。
12. CodecFake+ 資料集，HuggingFace `CodecFake/CodecFake_Plus_Dataset`（2025，MIT）。
13. DFADD 資料集，HuggingFace `isjwdu/DFADD`（2024，MIT；2025-04 修正版）。
