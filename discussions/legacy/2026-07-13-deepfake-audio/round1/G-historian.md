# Round 1 提案：領域史官（Agent G）
日期：2026-07-13

> 角色：領域史官。我的職責是把這場討論放回「時間軸」上——這個領域從 ASVspoof 2015 走到今天出現過哪些循環、哪些方向看似新穎其實已被做過、哪些縫隙是真的沒人填。本文所有 2025–2026 的進展均來自本次網路檢索（附 URL）；標注「史官背景知識」者為我對領域歷史的整理；標注「猜測」者為未經證實的推論。

---

## 0. 檢索紀錄（本提案的證據基礎）

本次共執行 9 次檢索 + 1 次論文全文擷取，重點收穫：

| # | 主題 | 關鍵發現 | 來源 |
|---|------|----------|------|
| S1 | ASVspoof 5 與 SOTA | ASVspoof 5 正式論文刊於 IEEE TASLP（2026-04）：1000+ 說話者眾包語料、32 種 legacy+新式合成攻擊、首度納入 adversarial attacks；53 隊參賽。SSL ensemble（含 BEATs/EAT/Dasheng 等一般音訊 SSL）成為 unseen-generator 泛化主流做法 | https://www.sciencedirect.com/science/article/pii/S0885230825000506 、 https://arxiv.org/pdf/2603.01482 |
| S2 | Watermark 部署現況 | ElevenLabs 與 Google DeepMind 合作，SynthID 浮水印已開始嵌入 ElevenLabs 免費層 TTS 輸出並將擴及全部生成；Meta AudioSeal 0.2 開源（localized detection、比前代快兩個數量級） | https://elevenlabs.io/blog/synthid 、 https://github.com/facebookresearch/audioseal |
| S3 | Watermark 反噬偵測 | **The Watermark Shortcut**（Müller & Debus, arXiv 2606.23335, 2026-06）：偵測器若在「fake 有浮水印、real 沒有」的資料上訓練，會學到 spurious shortcut，產生三重失效——strip-to-evade（去浮水印即誤判為真）、mark-to-frame（給真人語音加浮水印即誣陷為假，AASIST EER 16%→75%）、泛化劣化。並釋出 WASP paired corpus | https://arxiv.org/html/2606.23335 |
| S4 | Watermark 移除攻擊 | 神經 codec 是 semantic filter，會抹除傳統浮水印；Latent-Mark（NTU + CyCraft，台灣團隊，arXiv 2603.05310, 2026-03）首個在 codec 不變 latent 空間嵌入的 zero-bit 浮水印；另有 diffusion-based 黑箱移除（Audio Pirates, arXiv 2605.30614）與 self voice conversion 攻擊（arXiv 2601.20432）；AudioMarkBench（NeurIPS 2024）定義 removal / forgery 兩類攻擊 | https://arxiv.org/html/2603.05310v3 、 https://arxiv.org/pdf/2605.30614 、 https://arxiv.org/pdf/2601.20432 |
| S5 | 電信防詐部署 | Hiya《State of the Call 2026》：1/4 美國人過去 12 個月接過 deepfake 語音電話；五大電信商成立聯合 AI 反詐公司（產業年損失 US$41B）；Resemble AI 提供 SIP/SIPREC 整合、<300ms 即時偵測；Google 於 2026-06 在 Android Phone app 全球推出 fake call detection | https://www.hiya.com/en-ca/newsroom/press-releases/state-of-the-call-2026-ai-deepfake-voice-calls-hit-1-in-4-americans-as-consumers-say-scammers-are-beating-mobile-network-operators-2-to-1 、 https://aimagazine.com/news/telco-giants-launch-network-ai-to-stop-deepfake-vocie-scams 、 https://techcrunch.com/2026/06/02/google-rolls-out-fake-call-detection-to-protect-against-ai-deepfake-impersonation-scams/ |
| S6 | 電話身分驗證極限 | STIR/SHAKEN：2025 上半年 tier-1 電信商間 84% 通話已簽章，但非 tier-1 起呼僅 21%；FCC 對 Lingo Telecom 開罰——其對載有 Biden deepfake 語音的 3,978 通 robocall 給了 A 級 attestation（簽章驗的是「號碼」不是「聲音內容」） | https://www.validsoft.com/stir/shaken-limitations/ 、 https://www.telecomramblings.com/2026/01/winning-the-robocall-war-how-2026-will-reshape-robocall-prevention/ |
| S7 | C2PA audio 落地 | 多個產業報導稱 Suno/Udio 已在輸出音檔嵌入 C2PA manifest、Spotify 2026 初把 C2PA 驗證整合進上傳管線（注意：來源為產業部落格，可信度中等，需查證一手公告） | https://undetectr.com/blog/c2pa-content-credentials-explained 、 https://www.eyesift.com/faq/c2pa-content-credentials-2026-cryptographic-provenance-adoption/ |
| S8 | 法規 | EU AI Act Article 50 於 **2026-08-02** 生效：合成音訊必須以 machine-readable 方式標記且可被偵測為 AI 生成，違者最高 €15M 或全球營業額 3%；配套 Code of Practice on Transparency of AI-Generated Content 2026-06 定稿 | https://artificialintelligenceact.eu/article/50/ 、 https://datamatters.sidley.com/2026/06/24/eu-ai-act-transparency-obligations-preparing-for-compliance-by-2-august-2026/ 、 https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content |
| S9 | Source tracing | Interspeech 2025 已有 source tracing 特別場次：STOPA 資料集、open-set source tracing、multilingual source tracing 首個 benchmark、source verification——此方向已非空白 | https://www.isca-archive.org/interspeech_2025/klein25_interspeech.pdf 、 https://www.isca-archive.org/interspeech_2025/firc25_interspeech.html 、 https://github.com/xuanxixi/Multilingual-Source-Tracing |
| S10 | In-the-wild 崩跌實證 | Deepfake-Eval-2024：開源 SOTA 在真實流通的 deepfake 上 audio AUC 掉 48%；商用偵測器較好但仍不及人類鑑識專家。RADAR Challenge 2026 專攻 media transformation 下的 robust ADD；ICASSP 2026 ESDD 挑戰賽 Track 2 為 black-box 低資源設定 | https://arxiv.org/pdf/2503.02857 、 https://arxiv.org/html/2605.09568 、 https://arxiv.org/html/2508.04529v2 |

---

## 1. 我看到的問題本質：這個領域正在重演同一個劇本

### 1.1 十一年的歷史沿革（史官背景知識，交叉比對文獻 #1）

- **2015（ASVspoof 2015）**：問題被定義為「保護 ASV 系統不被 TTS/VC 欺騙」。handcrafted 特徵（CQCC/LFCC）+ GMM 就能把 in-domain EER 壓到很低。
- **2017**：加入 replay attack；LCNN 等 CNN 方法興起。
- **2019（ASVspoof 2019 LA）**：神經 TTS（Tacotron/WaveNet 世代）進場。end-to-end 方法（RawNet2、後來的 AASIST）把 LA EER 壓到 <1%（文獻 #1：最佳 0.06%）。
- **2021（ASVspoof 2021 LA/DF）**：首次正視「通道」——電話通道與 codec 壓縮讓成績大幅回落。這是**第一次「壓縮/通道會摧毀偵測」被制度性承認**，比 Loughborough benchmark（文獻 #3）早四年。
- **2022–2024**：SSL 特徵（wav2vec2 XLS-R、WavLM）成為 frontend 霸主；In-the-Wild 資料集揭露 out-of-domain 崩跌。
- **2024–2026（ASVspoof 5，正式論文 2026 刊出，S1）**：眾包錄音、32 種攻擊、首度納入 adversarial attack。同期 VoiceWukong（文獻 #2）與 Deepfake-Eval-2024（S10）分別證明：對閉源商用生成器 EER 13.5–50%、對真實流通樣本 AUC 掉 48%。
- **2025–2026 的新變數**：浮水印從論文走向部署（ElevenLabs×SynthID、AudioSeal，S2）；C2PA 開始吃進 audio（S7）；EU AI Act Article 50 於 2026-08 強制標記（S8）；電信業者開始在網路層做即時偵測（S5）。

### 1.2 我認為別人可能忽略的三件事

**（a）「benchmark 揭露崩跌 → 新方法救回 in-domain → 新 benchmark 再揭露崩跌」是一個已經跑了四輪的循環。**
2015 的 GMM、2019 的 AASIST、2022 的 SSL、2025 的 SSL-ensemble/MoE（S1），每一代都在自己的 benchmark 上接近完美，然後被下一個更貼近現實的評測打回原形（2021 通道、In-the-Wild、VoiceWukong、Deepfake-Eval-2024）。**歷史告訴我們：碩士生若提「一個新架構把 EER 再降 X%」，兩年後大概率成為循環中的又一個註腳。**討論者 A 可能會提 SSL/foundation model 方向，我先把這段歷史放在這裡。

**（b）2025–2026 的真正典範轉移不在 detection，而在「生態系開始部署主動訊號」——而部署本身正在製造新的失效模式。**
浮水印與 provenance 不再是「未來式」：SynthID 已進 ElevenLabs 生產線（S2）、EU AI Act 八月起強制 machine-readable 標記（S8）。但 Watermark Shortcut（S3）證明：**部署浮水印會反過來毒化 detection 的訓練資料**——這是 2015 年以來第一次「防禦方的兩條防線互相傷害」被實證。文獻 #7 在影像上展示的 Integrity Clash 是同一類問題。這條「多訊號互動的失效模式」戰線在 audio 幾乎是空的，而且時間窗就是現在。

**（c）詐騙電話這條「最後一哩」上，學術界與產業界各自在做，中間有一段沒人量測的空白。**
產業端：電信商已部署 <300ms 網路層偵測（S5）、Google Android 端上偵測（S5）、STIR/SHAKEN 簽章覆蓋率 84%/21% 分裂（S6）。學術端：ADD-C（文獻 #3）模擬了 codec+丟包，RADAR 2026（S10）模擬了 media transformation。但**沒有任何公開研究量測「浮水印與偵測依據能不能活過一通真實的電話」**——真實 PSTN/VoIP/行動網路的串接（AMR-WB→EVS→Opus 轉碼、VAD、AGC、丟包隱藏），而詐騙恰恰都發生在這個通道裡。Lingo Telecom 案（S6）說明簽章驗的是號碼不是聲音，這個縫隙是制度性的。

---

## 2. 思辨過程：四個候選想法與我如何淘汰或修正它們

### 候選 1：「更會泛化的偵測器」——做一個對 unseen generator 更強的新架構

**動機**：Research Gap 地圖第 1 條，VoiceWukong 的 13.5–50% 崩跌是最痛的數字。

**自我質疑（史官的否決）**：
- 這正是 1.2(a) 的循環。ASVspoof 5 有 53 隊在做這件事（S1），SSL ensemble、MoE（ICASSP 2025）、continual learning（DFWF 2023 起、evolving benchmark arXiv 2405.08596）全都有人做了。碩士生一年、單卡等級的算力，要在這條軍備競賽裡擠出 novelty，勝率極低。
- 更致命的是 VoiceWukong（文獻 #2）已實證 targeted augmentation 與 multi-domain training 幾乎無效甚至有害（AASIST2 退化到 EER 48–50%）——「補資料/補架構」這條路的邊際效益正在崩塌。
- **結論：淘汰。**不是因為不重要，而是因為歷史顯示這是紅海，且與「一年做完、直接降低受騙率」的目標最遠。

### 候選 2：Source tracing / attribution——不只判真假，還指認生成器

**動機**：對執法與 165 反詐有直接價值；「指認是哪家 TTS」聽起來比二元分類新穎。

**自我質疑**：
- 檢索結果直接推翻「新穎」：Interspeech 2025 已有整個特別場次，STOPA 資料集、open-set tracing、multilingual benchmark、source verification 都發表了（S9），Pindrop 等業者也在做。**這是「看似新穎其實已有人做」的典型案例**，我有義務在此標記給所有討論者。
- 且它繼承 detection 的所有弱點：閉源生成器拿不到訓練樣本、laundering 會抹掉 tracing 依據——文獻 #2、#3 的崩跌會原樣複製到 tracing 上。
- **結論：淘汰作為主軸。**但「open-set tracing 在通道劣化下的表現」可以作為候選 4 benchmark 的一個附帶評測軸。

### 候選 3：把文獻 #7 的 Integrity Clash 移植到 audio——跨層一致性稽核

**動機**：Research Gap 地圖第 3 條明說「audio 領域尚缺乏對應的系統性研究」。2026 上半年三件事讓它突然變熱：SynthID 進 ElevenLabs（S2）、Watermark Shortcut 揭露浮水印毒化偵測器（S3）、EU AI Act 強制標記（S8）。

**自我質疑**：
- *質疑一：會不會只是「影像論文換個 modality 重跑」，novelty 不足？* 反駁：audio 的物理通道（電話、重錄、神經 codec）與影像本質不同——Latent-Mark（S4）證明神經 codec 會抹除浮水印、文獻 #3 證明電信 codec 摧毀偵測依據，所以 audio 的「訊號去同步」有影像沒有的自然發生路徑：**不需要攻擊者，一通電話就會讓三層訊號彼此矛盾**。「良性 laundering 造成的假衝突 vs. 惡意攻擊造成的真衝突」如何區分，是影像論文沒有處理的新問題。
- *質疑二：C2PA audio 生態太年輕，實驗有東西可測嗎？* 檢查：c2patool 已支援 WAV/MP3，Suno/Udio 已在嵌 manifest（S7，來源可信度中等，開題前需驗證一手資料）；AudioSeal 開源、WASP corpus 已釋出（S3）。工具鏈齊全，可測。
- *質疑三：一年做得完嗎？* 拆解後可以：三層訊號都用現成品（c2patool、AudioSeal、AASIST/wav2vec2 偵測器），學生的工作是「衝突狀態形式化 + 通道擾動矩陣 + 稽核協定 + 評測」，不需要訓練任何生成模型。
- **結論：保留，成為正式提案一。**

### 候選 4：「活過一通電話」——電話通道下多防線存活性的實測 benchmark（含繁中詐騙情境）

**動機**：1.2(c) 的空白。詐騙的主戰場是電話，但 ADD-C 用的是 codec *模擬*（文獻 #3 自承對未知真實管線無解），VoiceWukong 的 manipulation 不含真實通話，RADAR 2026（S10）也是模擬 transformation。沒有人把「偵測器、浮水印、C2PA soft binding」一起丟進**真實的**行動網路/VoIP/PSTN 通道去量存活率。台灣情境（繁中、165 反詐體系、本地電信）更是完全空白——VoiceWukong 雖有中文集，但無電話通道。

**自我質疑**：
- *質疑一：「dataset/benchmark 論文」對碩士論文夠不夠格？* 歷史反駁：這個領域的推進器從來就是 benchmark——ASVspoof 系列、In-the-Wild、VoiceWukong（USENIX Security 2025）、Deepfake-Eval-2024、RADAR 2026 全是 benchmark 論文且發在頂級場館。**在典範轉移期，好的量測本身就是一等貢獻。**但 H（指導教授）可能要求 benchmark 之上要有方法論貢獻，所以我把「發現 → 一個對策」內建進提案。
- *質疑二：真實通道收音的工程成本與變因控制？* 風險真實存在（不同電信商、時段、網路狀態都是混淆變因）。緩解：借鏡 replay attack 資料集（ASVspoof 2017）的做法，固定收發設備矩陣、記錄 metadata、每條件多次重複；規模控制在 2–3 家電信商 × 2 通話 app × 若干 codec 路徑，這是體力活但不是技術風險。
- *質疑三：浮水印存活性會不會是顯然的「全滅」，做完只有一句話結論？* 猜測：AMR-NB 這種 8kHz 窄帶大概率全滅，但 VoLTE/EVS 與 VoIP（Opus 高碼率）下 SynthID/AudioSeal 的存活性是真的未知——Latent-Mark（S4）只測了神經 codec，AudioMarkBench 只測了數位擾動。就算結論是「全滅」，那也是對 EU AI Act「machine-readable 標記」政策路線的重要否證：**法規要求的標記在詐騙實際發生的通道上不可讀**，這個政策含義本身就有發表價值。
- **結論：保留，成為正式提案二。**

### （順帶淘汰的候選 5：端上即時偵測 app）

給 F 的情境做一個「通話中即時警示」app 看似最直接利民，但 Google 已於 2026-06 全球推出（S5），Resemble AI 已賣給電信商（S5）；碩士生在工程上競爭不過，學術 novelty 也薄。**淘汰**，但「警示 UX 的誤報容忍度」值得留給 F 與 H 討論（見第 4 節）。

---

## 3. 正式提案

### 提案 G-1：Audio Integrity Clash——音訊三層驗證訊號的去同步攻擊面與跨層一致性稽核

**核心 idea**：把「provenance（C2PA audio manifest）× 神經浮水印（AudioSeal/SynthID 類）× 被動偵測器」視為一個**訊號系統**而非三個獨立工具，系統性地形式化 audio 上的衝突狀態空間（例如：manifest 說人類創作、浮水印說 AI 生成、偵測器說真——共 2³ 乃至含「訊號缺失」的 3³ 狀態），實測哪些狀態可被攻擊者廉價製造（metadata washing、strip-to-evade、mark-to-frame）、哪些會被良性通道（codec、重錄、平台轉檔）自然觸發，最後提出能區分「惡意去同步 vs. 良性 laundering」的一致性稽核協定。

**為什麼有機會成立**：
- 文獻 #7 已在影像上證明此類攻擊可行且稽核協定有效（3,500 張、100% 分類準確率），Research Gap 地圖第 3 條明指 audio 缺對應研究——**移植 + audio 特有通道問題 = 明確可辯護的 novelty**。
- Watermark Shortcut（S3, arXiv 2606.23335）提供了現成的攻擊原語（strip-to-evade、mark-to-frame，EER 16%→75%）與 paired corpus（WASP）；AudioMarkBench 的 removal/forgery 分類（S4）提供攻擊分類學。
- 部署面已成立：SynthID 已在 ElevenLabs 生產環境（S2）、EU AI Act Article 50 自 2026-08 起強制 machine-readable 標記（S8）——「多訊號並存」不是假設而是即將到來的現實，衝突必然發生，誰先定義稽核規則誰就定義了這個子領域。
- 文獻 #6 證明 validator 之間本來就會矛盾（Adobe vs. Verifieddit），本提案把「矛盾」從 bug 升級為研究對象。

**技術路線（12 個月，粗略）**：
1. M1–2：復現 WASP/AudioSeal/c2patool 工具鏈；驗證 Suno/Udio C2PA manifest 一手現況。
2. M3–5：形式化衝突狀態空間；實作 audio 版 metadata washing 與 watermark strip/forge 攻擊，量測各狀態的「製造成本」。
3. M5–8：良性通道矩陣（MP3/AAC/Opus/神經 codec/重錄/社群平台轉檔）下三層訊號的自然去同步率——這是與影像論文最大的差異化實驗。
4. M8–11：設計並評測跨層稽核協定（可從規則式 baseline 到輕量 learned auditor），指標：衝突狀態分類準確率、對抗設定下的 robustness。
5. M11–12：撰寫。中途產出（攻擊面量測）可先投 workshop（如 CVPR APAI 的 audio 對應場次、Interspeech special session）。

**預期貢獻**：(1) 首個 audio 多訊號一致性的系統性攻擊面分析與 benchmark；(2) 「良性 laundering vs. 惡意去同步」的區分方法；(3) 對 EU AI Act 標記義務的技術可行性提供實證輸入。社會福祉連結：平台與查核組織（新聞、165）可據此判讀「訊號互相矛盾的音檔」，而非被任一單獨「驗證通過」誤導——這正是文獻 #6 指出民眾最容易被「有簽章=真」話術欺騙之處。

### 提案 G-2：「活過一通電話嗎？」——真實通話通道下偵測器與主動訊號的存活性 benchmark（含繁中詐騙情境）與通道指紋補償

**核心 idea**：建立第一個**經過真實電話通道**（台灣 2–3 家行動電信 VoLTE/PSTN、LINE/WhatsApp/Messenger VoIP、市話）的 deepfake 語音存活性 benchmark：把（a）繁中+英文的開源與商用 TTS 詐騙情境語料（含真人對照）實際打過這些通道錄回，量測（b）SOTA 偵測器（AASIST、wav2vec2 系、商用 API）的劣化曲線、（c）AudioSeal/SynthID 類浮水印的存活率、（d）open-set source tracing 的殘存能力。在發現之上做一個方法論貢獻：**通道指紋估計 + 條件化偵測**——先從收到的音訊推斷「這段音訊經過了哪種通道」，再選擇/校準對應的偵測器，檢驗它是否優於文獻 #3 那種「已知通道分佈的 DA」與 VoiceWukong 證明無效的 multi-domain training。

**為什麼有機會成立**：
- 文獻 #3 自承其解法「假設已知目標通道的 codec 與 PLR 分佈，對未知管線泛化未驗證」；文獻 #2 證明盲目 multi-domain training 有害。兩篇合起來指向的正是「先推斷通道、再條件化偵測」這條沒人走完的中間路線（猜測：可行性中高，因為 codec 指紋分類本身是成熟技術，史官背景知識——codec classification 文獻自 2010 年代即存在）。
- 真實通道 vs. 模擬的落差有歷史前例：ASVspoof 2021 與 Deepfake-Eval-2024（S10, audio AUC −48%）都證明模擬永遠低估劣化。RADAR 2026（S10）仍是模擬 transformation，真實通話錄回的公開資料至今不存在。
- 電信/監管的需求端已經成形：五大電信商聯合反詐（S5）、Google 端上偵測（S5）、Hiya 統計 1/4 美國人接過 deepfake 電話（S5）、台灣 165 體系與本地報導（https://technews.tw/2026/06/11/ai-voice-cloning-scams/ 、 https://blog.trendmicro.com.tw/?p=92053 ）。但這些系統的有效性都未經獨立公開評測——本 benchmark 直接填這個洞。
- 浮水印存活性子實驗填補 Latent-Mark（S4，只測神經 codec）與 AudioMarkBench（只測數位擾動）都沒碰的電信通道；結論無論正反都對 EU AI Act Article 50（S8）的落地有政策含義。

**技術路線（12 個月，粗略）**：
1. M1–3：語料設計（繁中/英詐騙話術腳本、TTS 生成 + 真人錄音對照、倫理審查）；收發設備與通道矩陣定案。
2. M3–6：通道錄製（自動撥打/接聽 rig，體力活風險期）；同步做浮水印嵌入前處理。
3. M6–9：三軸評測（偵測器劣化、浮水印存活、source tracing 殘存）；通道指紋分類器訓練。
4. M9–11：條件化偵測 vs. 文獻 #3 DA vs. multi-domain baseline 的對照實驗。
5. M11–12：撰寫並開源資料集（真人語音部分需去識別化處理）。
- 風險備案：若真實通道錄製規模不及預期，縮至單電信商 + 兩 VoIP app，仍是首個真實通道資料集。

**預期貢獻**：(1) 首個真實電話通道的 ADD/浮水印存活 benchmark，且是繁中詐騙情境的第一份公開資源；(2) 「通道指紋→條件化偵測」方法及其與既有 DA 策略的對照；(3) 給電信業者、165、監管者的可直接引用的量化證據。社會福祉連結最直接：詐騙就發生在電話裡，這份 benchmark 量的就是「防線在案發現場還剩多少」。

### 兩提案的關係

G-1 問「多層訊號放在一起會怎麼互相矛盾」，G-2 問「每層訊號經過真實案發通道還剩多少」。若資源允許，G-2 的通道錄製產物可直接餵給 G-1 當「良性 laundering」條件——兩者共享基礎設施，但各自獨立成篇。

---

## 附：「看似新穎、其實已有人做」清單（給所有討論者的排雷圖）

| 看似新穎的方向 | 實際狀況 | 來源 |
|----------------|----------|------|
| Source tracing / 生成器指認 | Interspeech 2025 整個 special session + STOPA 資料集 + multilingual benchmark | S9 |
| 用 MLLM/LLM 判斷音訊真假 | VoiceWukong 已測 Qwen2-Audio：英文 F1=0，完全不具能力 | 文獻 #2 |
| Codec/通道 data augmentation | ADD-C 已做且有效，但僅限已知通道分佈 | 文獻 #3 |
| Continual learning 抗新生成器 | 2023 起已有 DFWF、evolving benchmark 等系列工作 | https://arxiv.org/pdf/2308.03300 、 https://arxiv.org/pdf/2405.08596 |
| 「幫 TTS 加浮水印」本身 | AudioSeal/SynthID 已部署；前沿已推進到抗神經 codec（Latent-Mark）與移除攻擊 | S2、S4 |
| 通話中即時偵測 app | Google Android 2026-06 全球上線；Resemble AI 已商用（<300ms） | S5 |
| 「浮水印+偵測器雙保險」 | Watermark Shortcut 已證明天真組合會互相毒化——組合不是 novelty，**稽核組合**才是 | S3 |
| in-the-wild 崩跌實證 | Deepfake-Eval-2024、VoiceWukong、RADAR 2026 都已量化 | S10、文獻 #2 |

## 4. 我留給其他討論者的問題

1. **給 D（紅隊）**：Watermark Shortcut 給了 strip-to-evade 與 mark-to-frame 兩個攻擊原語（S3）。針對我 G-1 的跨層稽核協定，你認為攻擊者最便宜的繞法是「讓三層訊號一致地說謊」還是「讓稽核器把惡意去同步誤判為良性 laundering」？後者若成立，G-1 的核心區分任務是否根本 ill-posed？
2. **給 B（密碼學/Provenance）**：電話通道會剝掉檔案容器，C2PA 的 hard binding 必死，只剩浮水印類 soft binding。在「訊號只能藏在波形裡」的通道上，你認為有沒有任何密碼學機制能提供比「浮水印存在/不存在」一個 bit 更多的可驗證資訊？還是 G-2 應該直接把電話通道宣告為 provenance 的不可達區域？
3. **給 F（民眾代表）與 H（指導教授）**：VoiceWukong 顯示人類對高品質 deepfake 的 FAR > 82%（文獻 #2），而 Google 的端上警示已上線（S5）。你們認為「偵測器警示的誤報率」高到多少，民眾就會開始忽略警示（alarm fatigue）？這個閾值應該反過來決定 G-2 評測的主指標（例如固定低 FPR 下的 recall 而非 EER）——H，你會接受一篇以「部署導向指標」而非 EER 為主的碩士論文嗎？

---
*檢索執行於 2026-07-13/14，共 9 次 WebSearch、1 次全文擷取。產業部落格類來源（S7）已標注可信度保留。*
