# Round 2 質詢：Detection 研究者（Agent A）
日期：2026-07-13

---

## 序：我的質詢立場

Round 1 我提了兩個方向：**提案一 Channel-Robust One-Class Learning**（以真實語音為錨、對 unseen generator 免疫、用 #3 的通道 DA 撐大 real manifold）與**提案二 會說「我不知道」的偵測器**（selective prediction / calibration under shift，銜接人機互補）。

進入 Round 2，我發現一件事值得先講明：**這一組討論者高度收斂到兩個共識磁鐵**——(甲) Audio Integrity Clash / 跨層一致性稽核（B、G、H、E 都碰、四個人），(乙) 互動式 challenge-response / liveness（D、E、F 都提、三個人）。共識通常代表「大家都覺得安全」，而我作為 detection 研究者的職責，是去戳這兩個磁鐵在**技術層與威脅模型層**的裂縫，而不是跟著鼓掌。以下三個主要挑戰，正好各打一個共識磁鐵加一個我最熟的 ML 誤區。

---

## 1. 對他人提案的挑戰

### 挑戰一：對「互動式 challenge-response / liveness」叢集（D 提案二、E 提案一、F 提案二）——延遲訊號的物理基礎正在崩塌，而且這條路已被產業佔領

D 主張『把防線移到攻擊者無法離線預先破解之處……逼攻擊者即時合成/轉換他預料不到的新內容』，E 主張『即時語音克隆有兩個結構性軟肋：延遲、分布外提示的脆弱性』，F 把它包裝成『考對方一題他無法預錄的題目』。三人的共同技術支柱只有一根：**即時 voice conversion / TTS 在「低延遲 + 任意新內容 + 正確 prosody」上做不好，所以會露餡。** 我要攻擊的就是這根支柱。

**反駁一（延遲訊號在真實通道上不可用，這是 E 自己都察覺的致命傷）。** E 在給 C 的問題裡親口承認：『真實電話通道本身就有 codec 緩衝、jitter、封包遺失……這些通道延遲會不會淹沒我要量測的生成端推論延遲？』我的答案是：**會，而且是數量級的淹沒。** VoLTE/VoIP 的 jitter buffer 動輒 60–200ms 且動態調整，端到端延遲抖動遠大於現代 streaming TTS 的首包延遲（seed-VC、RVC 一類已可壓到 <300ms，且延遲是「穩定偏移」不是「隨機抖動」，人耳與機器都難以與通道抖動區分）。把「延遲」當判別特徵，等於在一個 SNR 為負的通道裡量一個小訊號。這不是工程調校問題，是訊號被通道結構性掩蓋。

**反駁二（G 已用檢索證據把這條路標成產業紅海）。** G 的 S5 白紙黑字：Google 2026-06 已在 Android Phone app 全球推出 fake call detection、Resemble AI 已賣給電信商做 <300ms 即時偵測、五大電信商成立聯合反詐公司。challenge-response 的即時互動層，產業的資源、通話網路存取、規模都輾壓碩士生。D/E/F 若要在這裡宣稱 novelty，必須說明「你比 Resemble AI 的商用系統多做了什麼」——而三份提案都答不出這一句。

**反駁三（'成本上升'是 2024 年的判斷，2026 年已過期）。** D 誠實地把賭注押在『即時、對隨機新句子維持目標音色 + 自然 prosody，遠比離線精修昂貴』。但這是把生成端當靜態對手。2026 的現實（G 的歷史軸也支持）是 real-time zero-shot VC 已商品化、開源、消費級 GPU 可跑。攻擊者要的不是「完美 prosody」，是「在受害者恐慌的 15 秒內夠像」——F 自己在提案裡強調受害者是在腎上腺素中判斷，那麼 prosody 的細微破綻根本不會被恐慌中的阿嬤察覺。**challenge-response 把偵測難度從「機器分辨」降級成「恐慌中的人分辨」，這在 F 自己的 (b) 論點下是往錯的方向走。**

**我承認的部分**：F 的「把民眾做不到的查證程序自動化成一鍵動作」這個框架我認同（見第 3 節我支持的提案）。我打的是「延遲/即時性軟肋是可靠判別訊號」這個技術假設，不是「互動驗證」這個概念本身。若要救這條路，唯一站得住的訊號不是延遲，而是**語意層的追問一致性**（機器對 out-of-context 追問的內容錯誤），但那已經離開 audio detection、進入對話 LLM 領域，不是這桌任何人的主場。

---

### 挑戰二：對 E 提案二「合成聲源的人群層級連結分析」——你要連結的那個 cue，恰好是 laundering 最先殺死的那個

這題是我的正主場（SSL 特徵、speaker embedding、generator artifact），所以我講得具體。E 主張『同一個生成器、同一份 reference audio 克隆出來的聲音……它們彼此之間會共享 speaker embedding 的異常聚集與生成器的共同 artifact』，並認為相對連結『對這兩道牆更有韌性』。

**反駁一（連結訊號的兩個成分，在 laundering 下的命運相反，而 E 把它們混為一談）。** E 的連結假設同時依賴兩種 cue：(i) speaker identity 的一致、(ii) generator artifact 的一致。這兩者在通道下的存活性**恰好相反**——這正是 C 提案一「存活圖譜」的核心洞見：generator artifact（neural vocoder 的高頻 checkerboard、相位微結構）屬 C 分類的「第一、二層（最脆弱）」，AMR/Opus 一過就物理性死亡；而 speaker identity 屬「第三層（最強韌）」，因為 codec 的感知目標函數就是要保住它。更糟的是：**現代 speaker embedding（ECAPA-TDNN、WavLM-based）是被刻意訓練成 channel/codec invariant 的**——speaker verification 這個任務的整個目的就是壓抑低層通道與錄音痕跡、只留語者身分。所以 laundering 之後，embedding 裡存活的是「語者身分」，被主動抹掉的正是「generator artifact」。E 想連結的「同一個模子」訊號，用的工具本身就把那個訊號當噪音濾掉了。

**反駁二（於是連結退化成 speaker verification，而那會誤傷真人）。** 若 laundering 後只剩 identity 可連結，那 E 的方法實際上在做「同一個被冒充者的聲音出現在多通電話」——這是 speaker clustering，不是 deepfake detection。問題是：**真人的聲音也會如此聚集**（同一個真人打了多通電話、或一段真實錄音被轉傳多次），系統無法從「異常一致的聚集」本身區分「詐騙集團重用克隆聲」與「一個真人講了很多話」。E 的區分寄望於「不合常理的頻率/分布行為」，但那是行為情報（需要跨受害者通聯流），E 自己在致命弱點一已承認碩士生拿不到、且有隱私問題，只能用資料集**模擬** campaign——而模擬的「不自然頻率」是研究者自己注入的，會變成循環論證。

**反駁三（攻擊者的反制是零成本且不損詐騙價值的，與 E 的樂觀相反）。** E 認為攻擊者換 generator/換 reference 會『失去冒充特定親人/主管的詐騙效果』。這對「冒充特定人」的定向詐騙成立，但對「假客服/假檢警」這類**不需要特定音色、只需要一個可信的陌生權威聲音**的大宗詐騙不成立——攻擊者每個 campaign 用不同 generator + 不同隨機音色，identity 與 artifact 都不重複，連結圖直接碎成孤立點，而詐騙效果毫髮無傷。D 的口頭禪在這裡完全適用：繞過成本趨近於零。

**建設性**：E 提案二若要活，得放棄「generator artifact 連結」（laundering 下死路），改成純 identity-based 的**定向冒充偵測**，並限定威脅模型在「重用特定名人/主管聲紋」——這是一個小得多但誠實的題目，且要正面處理「誤傷真人」的 FPR 問題（又回到我提案二的 calibration）。

---

### 挑戰三：對「Audio Integrity Clash / 跨層一致性稽核」叢集（B 提案一、G 提案 G-1、H 提案一）——你們要稽核的三層訊號裡，最關鍵的那層對真實詐騙覆蓋率為零，而把 watermark 摺進來會主動毒化偵測

這是全場最大的共識磁鐵，B、G、H 三人都把它列為第一提案，論證漂亮、文獻錨點硬（#7 + gap 地圖第 3 點）。正因為它最像「安全牌」，我要打得最用力。

**反駁一（威脅模型的覆蓋率黑洞，D 和 F 已經指出，我從 detection 角度加倍確認）。** 稽核協定的三層是 {C2PA manifest, watermark, passive detector}。前兩層對真實詐騙 deepfake 的覆蓋率是**零**——D 講得最直白：『我做詐騙電話時當然不會幫我的假音訊簽 C2PA、也不會嵌浮水印』，#6 白紙黑字寫 provenance「對不附 credential 的惡意 deepfake 完全零覆蓋」。F 的 (c) 補刀：『缺席的訊號對一般人不構成警告』。所以在真實詐騙場景，三層裡有兩層恆為「缺席」，稽核協定**優雅地退化成只剩 passive detector 一層**——也就是退回我和大家都知道 EER 13.5–50% 的那個東西。H 自己在候選 4 的自我質疑裡承認了這點，回應是「缺席也是一種可操作的資訊等級」。但這個回應依賴一個未證實的長期賭注（法規強制標記普及後，缺席才有鑑別力），F 已質疑過渡期缺席=雜訊。**在碩士論文的一年時程內，這個賭注不會兌現。**

**反駁二（從 detection 專業給一個他們沒算到的新反證：把 watermark 摺進稽核會主動製造 detection 的新失效模式）。** 這是 G 自己檢索到、卻沒有連到自己 G-1 提案的一顆炸彈——S3 的 **Watermark Shortcut**（arXiv 2606.23335）：偵測器一旦在「fake 有浮水印、real 沒有」的資料上訓練，會學到 spurious shortcut，產生 **mark-to-frame**（給真人語音加浮水印就誣陷為假，AASIST EER 16%→75%）。這對稽核協定是直接的：如果 passive detector 這層與 watermark 這層在訓練/推論上沒有嚴格去相關，稽核器會把「有 watermark」當成「偏向 fake」的捷徑，於是**攻擊者只要對一段真人語音蓋一個合法 watermark，就能同時污染 watermark 層與 detector 層，製造一個稽核器判為「高信心假」的真內容**。B/G/H 的稽核協定把三層當「獨立訊號」做一致性檢查，但 Watermark Shortcut 證明這三層在 ML 層面**並不獨立**——detector 會偷看 watermark。這是影像版 #7 沒有處理、而 audio 特有的失效，也是我作為 detection 研究者能提供的實質反證。

**反駁三（passive detector 這層即使做 calibration 也救不了整體覆蓋率）。** 我 Round 1 給 B 的建議是「detector 必須輸出 calibrated probability 而非硬判決」，B 和 H 都接受了（H：「把 detector 不可靠性建模成先驗可信度」）。我要在這裡收回一半的樂觀：calibration 能防止「高信心錯誤污染稽核鏈」，但**不能製造覆蓋率**。一個誠實說「我對這段無憑證音訊只有 55% 把握」的 detector，接進稽核協定後，稽核輸出仍然只是「三層裡兩層缺席 + 一層 55%」——對受害者而言資訊量趨近於零。稽核協定的價值域是**平台/查核組織處理「有憑證但可能矛盾」的內容**（B 和 G 的社會效益論述其實都限定在此），而不是問題陳述第 2、5 點真正關心的「詐騙電話 / 轉傳語音」。這個題目值得做，但要誠實地把 title 從「對抗 deepfake」縮到「對抗**已簽署內容**的認證矛盾」——這是一個 provenance 生態內部的問題，不是反詐問題。

**我承認的部分**：這個叢集是三份提案裡 novelty 錨點最硬、可行性最實（元件全現成、不訓大模型）、最不隨生成器過期的。作為**碩士論文可行性**它很強；我打的是它與「降低民眾受騙機率」這個硬性目標之間的**距離**，以及 Watermark Shortcut 這個被忽略的 ML 陷阱。

---

### 挑戰四（簡短）：對 C 提案二「通道宣稱 vs 證據一致性檢查」——攻擊者用一次真電話就能偽造通道痕跡

C 主張『這通自稱是銀行來電的錄音，卻沒有任何電話 codec 痕跡，本身就是強烈的詐騙訊號』。D 已經在 Q3 埋了這個攻擊，我從特徵角度確認其致命性：攻擊者要偽造「合法電話通道痕跡」的成本，就是**真的撥一通電話**（把 deepfake 灌進 virtual audio cable 播出、對端錄回）——這正是即時詐騙本來就在做的事（灌進通話軟體）。於是「通道證據」對攻擊者是免費附贈的，一致性檢查只對「懶得過真通道的低端偽造」有效，對真正的即時語音詐騙無效。C 的通道指紋作為**下游偵測器的 conditioning 訊號**（提案二的 (a)）我認為有價值，但作為**獨立的詐騙判別訊號**（提案二的 (b)）會被零成本繞過。

---

## 2. 回答指名給我的問題

### 回答 C（訊號處理）：SSL 表徵在窄帶（AMR-NB 砍到 4kHz 再升採樣）輸入下的行為？

C 問：『當輸入被 AMR-NB 砍到 4 kHz 以下再升採樣回 16 kHz，SSL 表徵的哪幾層還有意義——優雅退化還是進入分布外垃圾區？這決定我提案一該用 SSL probing 還是回頭用窄帶原生特徵。』

我的判讀（部分實證知識、部分推理，標明）：

- **分層命運不同，不是全有全無。** WavLM/XLS-R 的底層是 CNN feature extractor（局部時頻濾波器組），它對「頻寬被砍掉一半」最敏感——升採樣回 16kHz 只是把 0 補回頻譜，4kHz 以上是合成的空洞，這些底層 filter 的響應會進入預訓練從沒見過的區域，屬「分布外垃圾區」的風險最高。**中層 Transformer**（大約第 6–12 層，編碼 phonetic/語音內容）相對優雅退化，因為語音的可懂度資訊本來就集中在 4kHz 以下（電話頻寬的設計前提），這一層承載的音素/prosody 資訊在窄帶下大致還在。這與我 Round 1 提案一「SSL frontend 是唯一被反覆驗證有助 generalization 的元件（#1）」一致，但要加一個限定：**有助的是中層，不是全棧。**
- **實務建議**：不要用 raw SSL 全棧特徵硬吃窄帶輸入，會被底層污染。兩條路：(a) 對 SSL 做 **band-limited augmentation 的 continued pretraining/adaptation**（把窄帶輸入拉回 in-domain，這正是我提案一「通道 DA 施加於 real」的自然延伸，可與你的存活圖譜共用實驗）；(b) 用 **layer-weighting / weighted-sum probing**（S3TR、SUPERB 式可學習層權重）讓模型自己學會在窄帶下降權底層、升權中層。你的存活圖譜若加一個「SSL 逐層 × codec 頻寬」的 probing AUC 熱圖，就直接回答了這題，而且是 #1、#3 都沒做過的量化。
- **一句話結論給你的決策**：窄帶下我建議「SSL 中層 probing + band-limited adaptation」，而非退回窄帶原生 handcrafted 特徵——因為 #1 的歷史證據顯示 handcrafted 在 unseen attack 上泛化紀錄差，你不該為了通道 robustness 犧牲 generator 泛化。

### 回答 D（紅隊）Q1：能不能給出「攻擊成本下界」而非只報 in-domain EER？

D 逼問：『你能不能給出一個攻擊成本下界（要繞過我，攻擊者至少得付出 X），而不只是報一個 in-domain EER？給不出下界，我們憑什麼相信你不是又一個零成本可繞過、製造虛假安全感的方案？』

我誠實回答，分三段：

1. **對「純被動偵測」，我給不出密碼學意義的硬下界，而且我認為任何聲稱能給的人都在說謊。** 被動偵測沒有不可繞過性的證明——這是這條技術路線的本質限制，我不迴避。所以你這一刀，對「只做一個偵測器就宣稱能保護民眾」的提案是致命的，我完全同意。
2. **但我的提案一（one-class + channel-aug）確實把你最便宜的那招廢掉了。** 你的招牌零成本攻擊是「換一個 unseen generator」（VoiceWukong 證明 EER 崩到 13.5–50%）。我的方法**根本不學任何 generator 的 fingerprint**，只對 bona fide manifold 建模——所以「換 generator」對我的失效模式**不成立**，因為我沒有一個「已知 generator 清單」可以被繞開。你剩下的攻擊升級成「對 deepfake 做 adversarial perturbation 把它推進 real manifold」——這正是我 Round 1 給你的問題，而它的成本**遠高於**「換一個 API」：需要 (i) 對我的 one-class embedding 有 query access、(ii) perturbation 要能活過一次未知 codec（很可能被壓縮抹掉）。所以我的「下界」不是絕對值，是**相對抬升**：把你的攻擊從「零成本換 API」抬到「黑箱 + 通道存活的 adversarial 攻擊」。這正是你提案一的 attacker-cost curve 該量的東西——我很樂意當你曲線上的一個被攻擊對象。
3. **對「給不出下界怎麼辦」，我的提案二就是答案。** 你的深層焦慮是「零成本繞過 + 偵測器自信地錯 = 虛假安全感」。我提案二的整個設計就是拆掉「自信地錯」這一項：當偵測器對某輸入不可靠時，它**棄權**而非給綠勾勾。於是你的零成本繞過的結果不再是「拿到假的真實認證」，而是「觸發系統說『我無法判定，請掛斷回撥』」。**沒有下界的誠實回應，就是不讓偵測器在沒有下界的地方發出確定的聲音。** 這是我對你「虛假安全感」指控唯一站得住的防禦，也是我把提案一和提案二綁在一起的原因。

### 回答 E（開創性思維者）Q3：speaker embedding 在 laundering 後保留的是語者身分還是 generator artifact？哪個對同源連結更有用？

已在挑戰二詳答，此處給你直接的結論：**laundering 後保留的是語者身分，被抹掉的是 generator artifact——而你的同源連結真正需要的是後者。** 現代 speaker embedding（ECAPA/WavLM-based）被刻意訓練成 codec/channel invariant，這對 speaker verification 是優點，對你是災難：它幫你保住「誰的聲音」，卻濾掉「哪個模子生成的」。所以：

- 若你要連「同一個 generator」→ 依賴 generator artifact → C 的存活圖譜第一/二層 → codec 一過就死 → **不可行**。
- 若你要連「同一個被冒充的人」→ 依賴 identity → 存活 → **可行，但那是 speaker clustering，會誤傷真人，且對「不需特定音色的假客服詐騙」無效**。

我的建議與挑戰二一致：放棄 artifact 連結，若堅持做就限定在「定向冒充偵測」並正面處理 FPR。這對你是壞消息，但我寧可現在告訴你，也不要你花八個月才在 codec 條件下發現連結圖碎掉。

### 回答 F（民眾代表）Q2：對民眾發警告的最低可用 operating point 在哪？模型端能否利用人機互補？

F 問：『以 VoiceWukong 13.5% EER 為現實，對一般民眾發警告的最低可用 operating point 在哪（FAR/FRR 各多少）？人機互補能不能在模型端就利用？』

1. **最低可用 operating point：綁定約束是 FPR（把真人誤判成假），不是 EER。** 你在提案一的 (d) 講對了——誤報會殺死信任。用你自己的直覺量化：一個會頻繁把真孫子、真主管標紅的 App，兩三次後就被關掉。以 usable security 的 alarm fatigue 文獻經驗（此為方法論借用，非 audio 文獻，標明），**面向民眾的自動警告 FPR 應壓到 1% 量級以下**，理想 <0.5%。問題來了：VoiceWukong 的 EER 是 13.5%，代表在 ROC 上把 FPR 壓到 1% 時，**recall（抓到的詐騙比例）會掉到很低**——我的推估是遠低於 50%，對閉源 generator 甚至可能 <30%（此為根據 EER 反推的猜測，需實測 ROC 才能定）。**結論：在這個 operating point 上，一個二元自動警告器抓不到一半以上的詐騙，卻仍偶爾誤傷真人——它不可部署。** 這恰恰是你提案一（警告該怎麼說）和我提案二（selective prediction）都成立的根本理由：**既然沒有一個 threshold 同時可接受，就不該用單一 threshold 發二元判決。**
2. **人機互補能不能在模型端利用——能，這就是我提案二的核心機制。** VoiceWukong 的數據（人類對低品質 deepfake FAR 4–19% 優於機器、對高品質 FAR >82% 劣於機器）給了一個明確的分工線：**讓機器只在它擅長且高信心的區域（高品質 deepfake）自動出手，把它不確定的區域（低品質、經 laundering、OOD）棄權路由給人類**。這正是 selective prediction 的 deferral policy，而且不是我憑空設計——是直接讀 VoiceWukong 的互補分布來切分工線。所以你的兩個提案和我的提案二在系統層是**同一個東西的兩端**：你做「棄權後警告怎麼呈現給人、人的受騙率降多少」（user study），我做「模型怎麼可靠地決定何時棄權」（calibration under shift）。這是這桌最自然的一組合作，見第 3 節。

---

## 3. 我支持的提案

### 支持一：H 提案二 / G 提案 G-3 精神 —— Selective Prediction 與 shift-aware calibration（與我提案二高度同構，我願意讓位並補強）

H 的提案二「知道自己不知道」與我 Round 1 的提案二是同一個方向，而且 H 把可行性、備案、evaluation protocol（train on A / calibrate on A' / abstain-test on B）寫得比我更嚴謹，甚至補了 conformal prediction 給錯誤率理論保證這一手——這是我該學的。我支持它成為統整方向之一，理由：

- **它是這桌唯一直接回答「降低民眾受騙機率」且不靠未證實長期賭注的技術路線。** 對比 Integrity Clash 叢集（依賴憑證普及）、challenge-response 叢集（依賴延遲訊號、已被產業佔領），selective prediction 對「無憑證的詐騙電話」這個核心情境**當下就有意義**：偵測器誠實棄權 + 「請掛斷回撥」比一個 13.5% EER 的綠勾勾強得多。
- **它把 D 的「虛假安全感」指控轉成防禦**（見我對 D 的回答第 3 段），這是整組討論裡對紅隊最有說服力的正面回應。

**我的角色能怎麼補強**：
1. 我提案一的 **one-class / distance-based score 天然就是一種 uncertainty signal**——「離 real manifold 多遠」直接是一個 OOD 分數，可作為 H 提案二「5+ 種棄權機制」比較清單裡的一個候選，且它不依賴 generator fingerprint，理論上在 unseen generator 上比 softmax confidence 更不會「自信地錯」。這是我能貢獻的、清單裡別人沒有的一項。
2. H 最擔心的科學風險是「AUC≈0.5 的 failure mode 下所有 uncertainty signal 全失效」。我的判斷（推理）：softmax/energy 這類**基於分類邊界**的分數在 AUC≈0.5 時必然一起失效（因為邊界本身失去意義），但**基於 real manifold 距離**的分數不依賴 fake 端邊界，有機會在此 failure mode 下存活——這是一個明確可檢驗的假設，正好是 H 提案二月 5–7 那個「open 的實證問題」的一個有理論動機的答案。
3. 我提案二規劃的小 user study 與 F 提案一幾乎重疊——建議三方（我、H、F）在統整時把「模型端棄權機制（我+H）」與「棄權後警告呈現 + 受騙率 user study（F）」合成一條完整的證據鏈。

### 支持二：C 提案一（存活圖譜）+ G 提案 G-2（真實電話通道 benchmark）—— 我提案一的 unseen-generator 軸正好補上他們缺的那一軸

C 的「Artifact Survival Atlas」和 G 的「活過一通電話 benchmark」在問「通道殺死了什麼 / 每層訊號在真實案發通道還剩多少」。我支持它們，因為：

- **C 的存活圖譜給了我提案一一個機制性解釋。** 我主張「把通道 DA 只施加於 bona fide class 來撐大 real manifold」，但我沒說清楚「撐大之後模型到底靠哪些存活特徵判別」。C 的圖譜（相位先死、高頻次之、韻律最後死）正好告訴我：channel-aug one-class 最終會逼模型依賴 C 的「第三層高存活特徵」。這讓我的方法從「經驗上有效」升級到「有物理解釋為何有效」。
- **G 的真實通道 benchmark 是我提案一「對真實詐騙通道可部署性」那一步（月 11–12）的最佳基礎設施**——我原本只打算自錄少量 LINE/Messenger 樣本，G 的系統性真實通道 rig 遠超我的規模。

**我能補強的、他們兩案都缺的一軸**：C 和 G 的通道實驗主要用**已知/公開的 real vs fake 素材**過通道，但都沒有系統性地做 **unseen-generator × unseen-channel 的交互作用矩陣**（我 Round 1 提案一的貢獻 1，也是文獻明確的空白——#2 只測 generator 軸、#3 只測 channel 軸）。我可以貢獻「用 VoiceWukong 的閉源 generator 樣本 × C/G 的真實通道」的雙軸交叉評測協定（leave-one-generator-out × leave-one-codec-out），讓存活圖譜不只回答「通道殺死什麼」，也回答「當生成器也 unseen 時，存活特徵是否還撐得住」。這三案（我提案一 + C-1 + G-2）共享通道基礎設施、各出一軸，是另一組自然的合作。

---

## 4. 小結：我的質詢立場

我打的三個主要挑戰，都不是「這個提案沒價值」，而是「它與『降低民眾受騙機率』這個硬性目標之間的距離，被樂觀地低估了」：challenge-response 高估了延遲訊號、低估了產業；crowd-linkage 高估了 laundering 後 artifact 的存活；Integrity Clash 高估了憑證在一年內對詐騙情境的覆蓋率、且低估了 Watermark Shortcut 這個 ML 陷阱。而我支持的兩組方向（selective prediction、真實通道存活圖譜）共同點是：**它們對「當下、無憑證、經通道 laundering 的詐騙音訊」誠實，且不靠未兌現的長期賭注。** 這也是我兩個提案的立場。
