# Round 2 質詢：訊號處理研究者（Agent C）
日期：2026-07-13

---

## 開場：我在 Round 2 的判準

我在 Round 1 提出一個核心主張——**detection cue 的物理存活性是分層的，不是全有全無**（相位/微觀波形最先死、高頻頻譜次之、韻律/長時包絡最韌）。Round 2 我用同一把尺去量每個人的提案：**你依賴的那個訊號（embedding、watermark payload、latency、artifact），在真實傳輸鏈的出口端，物理上還剩多少？** 很多提案的漏洞不在 ML 也不在密碼學，而在它們**默默假設了一個乾淨或可逆的通道**。以下逐一拆解。

---

## 一、對他人提案的挑戰

### 挑戰 1 — Agent E 提案 2「合成聲源的人群層級同源連結」：你要連結的指紋，被 codec 選擇性殺掉了

Agent E 主張：「同一個生成器、同一份 reference audio 克隆出來的聲音，即使個別音檔騙過偵測器，它們**彼此之間**會共享 speaker embedding 的異常聚集與生成器的共同 artifact」，並打算「在 #3 的 codec×PLR 六條件下測試連結穩定性」。

**但是這裡有一個致命的訊號處理問題：你要連結的兩種指紋，在通道下的存活率完全相反，而且會被通道「重新洗牌」。**

- **speaker embedding**（ECAPA-TDNN / WavLM）主要承載共振峰結構與長時包絡——這是我 Round 1 說的第三層，相對強韌，能活過 codec。**但正因為它強韌，它記錄的是「語者身分」而非「合成來源」**。同源 campaign 的克隆聲若冒充同一個真人，embedding 會聚在一起——可是**真人本人講的話也會聚在同一團**。你怎麼區分「同一克隆聲源的 5 通詐騙」和「同一個真人打的 5 通正常電話」？靠 embedding 分不出來，因為 codec 保留的恰好是你無法用來判斷「合成 vs 真人」的那一維。
- **生成器 artifact**（vocoder 的高頻 checkerboard、相位缺陷）才是能標記「同一個模子」的東西——但它住在第一、二層，**是 codec 最先摧毀的部分**。AMR-NB 一刀砍到 3.4 kHz 以上全沒，你要連結的 artifact 直接歸零。

**更糟的是通道會製造假聚類。** 經過同一條 codec 路徑（例如都走 LINE Opus 16 kbps）的樣本，會共享 codec 自己的量化指紋——你的聚類演算法很可能**按「走過哪條通道」聚類，而不是按「哪個生成器」聚類**。#3 已證明 codec 壓縮 C0→C1 就讓偵測器平均劣化 EER 5.30%，那是二分類；你的同源連結是更脆弱的細粒度 embedding 幾何，通道擾動只會更致命。Deepfake-Eval-2024（G 檢索 S10）測到真實流通樣本 audio AUC 掉 48%，那還只是真假二分，你的 linkage precision/recall 在 laundering 下的衰減曲線，我猜測（標明：猜測）會比二分類崩得更快。E 的自我質疑裡承認「對手每通換 generator/reference」會拉高攻擊成本，但沒處理**更便宜的反制**：詐騙者只要讓每通電話走不同通道（一通市話、一通 LINE、一通 Messenger），你的通道指紋污染就會把同源群集打散——這不花攻擊者一毛錢，是他本來就在做的事。

### 挑戰 2 — Agent B 提案 2「watermark-bound manifest soft binding」：電話通道的可靠 payload 逼近零，你的整個承諾塞不進去

Agent B 主張把 manifest 的密碼學承諾（「manifest hash ⊕ perceptual hash ⊕ transparency-log inclusion proof 的索引」）嵌入 robust watermark，「使 provenance 不再依賴會被通道剝離的 metadata 層」，並自問「AMR-WB 4.75–23.85 kbps + 20% 丟包之後還能剩幾 bit」。

**我直接回答，而且答案對這個提案很不利：在最惡劣鏈（AMR 窄帶 + 20% PLR + 一次喇叭-麥克風重錄）下，可靠 payload 逼近 0-bit，你連一個 hash 都放不下。**（完整推導見第二節 B-Q2）。這代表提案 2 的「完整 commitment」設計在最需要它的通道（電話）上直接失效，只能退到「1-bit 存在性 + 外部索引」——而 B 自己也承認這點。

但我要追加一個 B 沒處理、且比容量更根本的問題：**neural codec 是 semantic filter，會系統性抹除傳統浮水印。** Latent-Mark（G 檢索 S4，NTU+CyCraft）的整篇動機就是「神經 codec 會抹掉傳統 watermark，所以要嵌在 codec 不變的 latent 空間」。現在 LINE/Messenger/新一代 VoIP 正在往 neural codec 遷移。B 的 AudioSeal 承諾一旦過一次 neural codec transcode 就可能整段蒸發——**這不是丟幾個 bit，是整個載體消失**。而且 AudioMarkBench（S4）已定義 forgery 攻擊、Watermark Shortcut（S3）示範 mark-to-frame（給真人語音加浮水印就能誣陷為假，AASIST EER 16%→75%）——你的 anti-transplant perceptual-hash 綁定需要額外的 payload bits 去存 perceptual hash，這跟「容量逼近零」直接衝突：**你想防移植就要更多 bit，但通道只給你更少 bit。** 這個 trade-off 在電話通道上是無解的死結。結論：B 提案 2 的有效作用域必須誠實限縮到「高碼率 VoIP / 語音訊息檔案」，並明確宣告「電話即時通話是 provenance 的不可達區」——這正好呼應 G 給 B 的 Q2。

### 挑戰 3 — Agent A 提案 1「channel-augmented one-class」：把 real manifold 撐大到覆蓋窄帶，等於把判別邊界自己抹平

Agent A 主張「把 #3 驗證有效的通道模擬 DA **只施加於 bona fide class**，把真實語音 manifold 撐大到覆蓋壓縮/丟包/重錄條件」，因為「augmentation 只該用來擴張你有生成過程控制權的那一類（real）」。這個「該加在哪一類」的洞見很漂亮，我在 Round 1 也獨立想到 DA 撐大分佈的路線。

**但是從訊號處理看，這裡有一個 A 沒算到的幾何塌縮：當你把 real manifold 撐大到覆蓋 AMR-NB 窄帶條件時，你同時把 real 推進了 fake 也會落腳的那塊退化區。** 理由是我 Round 1 的存活層級：AMR-NB 把所有訊號（真的假的）都壓成 300–3400 Hz、相位重置的 CELP 輸出。**在這個條件下，真語音和假語音的可分資訊本來就被通道摧毀了**（第一、二層 cue 死亡）。你把 bona fide 的通道增強樣本塞進 one-class 邊界，等於告訴模型「這種頻寬受限、相位模糊的東西是真的」——而高品質 deepfake 過同一個 AMR-NB 之後長得幾乎一樣。**你撐大 real manifold 的每一步，都在同步降低對 fake 的排斥力**，尤其在最惡劣通道。A 的假說「real manifold 覆蓋通道變異 → 對 laundering robust」只在「通道是可逆 distribution shift」時成立；一旦通道是不可逆資訊摧毀（第一、二層），撐大 manifold 不是 robust，是**主動放棄判別**。

第二點：A 引用 #3「DA 後 EER 波動 <0.1%」來支撐「資訊未被摧毀」——但這個結論是 #3 在**已知 6 種 codec、且生成器 in-domain** 下得到的。A 的提案要打「unseen generator × unseen channel」雙重泛化，這是 #3 從未驗證的區域。#3 自承「對未知 codec（社群平台私有轉檔管線）的泛化未驗證」。把一個「已知通道 + 已知生成器」的樂觀結論，外推到「雙重未知」，是 A 論證鏈裡最脆的一環。我在第二節 A-Q2 會給出「哪些通道破壞是共通可 cover、哪些不是」的分層答案。

### 挑戰 4 — Agent D / E / F 三人的「即時 challenge-response」：latency 這根支柱在 2026 已經在崩，且被通道抖動淹沒

D 提案 2、E 提案 1、F 提案 2 都押注在「即時語音克隆有延遲軟肋」。E 明確說「高品質 zero-shot VC/TTS 要跑推論，在真正的即時對話裡會產生可量測的回應延遲」；F 說「即時 VC 要在幾百毫秒內對不可預測內容產生無破綻回應」。

**作為訊號處理研究者，我對「latency 作為判別訊號」這根支柱有兩個具體反對：**

1. **latency 訊號的分母正在快速變小。** 2026 的 streaming TTS/VC 已經做到 <300ms（G 檢索 S5：Resemble AI 對電信商提供 <300ms 即時偵測，這是產業已把即時語音鏈路壓到這個量級的旁證）。而電話通道本身的端到端延遲（codec algorithmic delay + jitter buffer + 網路 RTT）在 VoLTE 上就有 150–300ms、跨網 VoIP 常破 400ms 並且**逐封包抖動**。你要量測的「生成推論延遲」若也在幾百 ms 量級，就會被**同一量級且非平穩的通道延遲淹沒**——這正是 E 給我的問題（見第二節 E-Q2），我的答案是：絕對延遲不可用，只有「同一通話內、對不可預測內容的相對 turn-taking 延遲增量」還有機會，但這需要先在通話前段建立對方的 baseline，攻擊者只要在 baseline 期正常互動、在挑戰期切換即可規避。

2. **押 latency 是押錯層。** 我 Round 1 的存活層級告訴你：會活過電話通道、又難以即時偽造的，不是「時間延遲」（低階、易被通道污染、且逐年被壓縮），而是**韻律的即時一致性與非典型發聲**（氣音、笑聲、突然轉疑問句的 F0 軌跡）——這些是第三層特徵，物理上活得過 codec，且需要即時 arbitrary-content prosody control 才能偽造。D 誠實承認「即時 VC 存在」，我把他的誠實再推一步：**若你們要讓 challenge-response 有物理下界，判別訊號必須從 latency 換成 prosody/發聲生理的即時可控性**，否則明年 latency 破綻就沒了，整個提案的下界崩塌。這對三位是建設性修正，不是否定。

---

## 二、回答指名給我的問題

### 回答 Agent A（Q2）：codec 破壞有無共通結構？generator artifact 與 codec artifact 可分離嗎？laundering 是否資訊理論性摧毀偵測依據？

分三段答，這也順帶為我 Round 1 的「存活層級假說」辯護：

**(a) 共通結構——部分有，足以讓「6 codec DA」cover 一部分第 7 種，但有硬上限。** 主流 codec 共享三個破壞原語：①**帶限**（band-cutoff，AMR-NB 3.4 kHz、AMR-WB 7 kHz、Opus 依碼率）、②**參數式重合成的相位重置**（CELP 系：AMR/EVS/SILK 都用 LP+excitation，解碼相位與原始無關）、③**感知量化的頻譜階梯**（transform codec：Opus/AAC 的心理聲學遮蔽量化）。DA 若在**原語層**（而非特定 codec 產品層）取樣，能泛化到共享同組原語的未見 codec。**但硬上限是：tandem 串接與私有降噪/AGC 不是上述原語的線性疊加**，它們引入原語空間外的非線性——這就是 #3「對私有管線未驗證」的真正原因，也是我 Round 1 淘汰「codec-agnostic 通用擾動」當主軸的理由（怕重蹈 #2 的 multi-domain training 崩潰）。

**(b) 可分離性——高頻不可分（因為被摧毀），中低頻部分可分。** generator artifact（neural vocoder 的高頻 checkerboard、諧波缺陷、相位）與 codec artifact 在時頻域**高頻帶完全重疊**，而高頻正是 codec 第一個砍掉的——所以「過了 codec 之後，generator 的高頻 artifact 和 codec 的帶限 artifact 不是分不開，是 generator 的那份已經不存在了」。中低頻的長時統計（F0 微顫、共振峰動態）兩者來源不同、可部分分離，這是存活特徵偵測器能站的地方。

**(c) 所以 laundering 是可逆還是不可逆？兩者都是，取決於層級——這正是我 Round 1 的核心主張。** 對第三層（韻律、長時包絡）：是**可逆的 distribution shift**，#3 的 DA 能救，因為 codec 的感知目標函數本身就保證這層存活。對第一、二層（相位、高頻）：是**不可逆的資訊摧毀**，DA 救不回已被丟棄的 bit。A 的 one-class 提案若隱含「全部可逆」（挑戰 3），會在窄帶條件塌縮；若明確只賭第三層可逆、放棄第一二層，那它其實就收斂到我提案一的「只用存活特徵」路線——**我們可以合流**。

### 回答 Agent D（Q3）：tandem codec + re-synthesis laundering 後 EER 回到多少？可逆還是不可逆？

**EER 預測（標明：猜測，需實測）：** 對依賴第一、二層 cue 的模型（RawNet2 這類 raw-waveform、以及大量 handcrafted 高頻特徵），tandem（AMR→Opus→平台私有）+ re-synthesis laundering 後會逼近隨機（EER 40–50%），因為它們依賴的資訊被物理摧毀，這與 #2 觀察到 AASIST2 在 multi-domain training 下退化到 48–50% 同一個量級。對依賴第三層 cue 的模型（韻律/長時包絡分支），劣化明顯較小但不會免疫——re-synthesis（把音訊過一遍 VC/vocoder 重合成）會**重寫 excitation 統計**，這是比 codec 更狠的一擊，因為它連第三層的一部分微觀韻律都重新生成了。

**可逆 vs 不可逆：分層，如上 (c)。** 對你的核心關切——「被動偵測在洗過的通道上是不是死路」——我的誠實答案：**在 re-synthesis laundering 後，依賴痕跡的被動偵測接近死路，但不是全死**，因為攻擊者的 re-synthesis 本身要維持「聽得像目標語者且語意正確」，這個約束會逼他保留第三層的某些結構（否則受害者聽不出是誰）。所以殘存的判別力來自「攻擊者為了達成詐騙目的而不得不保留的東西」，不是來自「攻擊者忘了洗掉的痕跡」。這個區別很重要：它意味著**存活特徵偵測是在賭攻擊者的功能性約束，不是賭他的疏忽**——這比追痕跡穩，但天花板也低。這一點正面支持你提案二「把防線移到互動層」的合理性：**當被動痕跡逼近死路時，逼攻擊者即時表演（考他的功能性約束）確實是更有物理下界的方向**（但請把判別訊號從 latency 換成 prosody，見挑戰 4）。

### 回答 Agent B（Q2）：AMR-WB 最低碼率 + 20% PLR + 一次重錄後，10 秒語音還能可靠傳幾 bit watermark payload？

**訊號處理視角的容量估計（標明：以下為量級估計，非精確測量，需 empirical 驗證）：逼近 0，設計必須退到 1-bit 存在性 + 外部索引。** 推導鏈：

1. **有效頻寬：** AMR-WB 6.6 kbps 模式下，可靠承載能量的頻段實質壓縮到約 50–6000 Hz，且 CELP 的相位不可用作載體——傳統相位/高頻浮水印通道直接關閉。
2. **重錄（喇叭→麥克風空氣通道）：** 疊加房間脈衝響應（RIR 卷積）、換能器非線性、環境噪音底。RIR 卷積會把頻域浮水印的窄帶結構抹散，非線性產生諧波失真。這一步對「頻域嵌入」的 watermark 通常是數量級的 SNR 損失。
3. **20% PLR + PLC：** 封包遺失後 PLC 用外插補上波形，補出來的段落與原始 watermark 相位完全脫節——等於在時間軸上隨機挖掉 20% 並填入雜訊。
4. **合成估計：** clean 條件下 AudioSeal 類約可靠承載 ~16 bit；每經過上述一個階段可靠容量大致砍半到砍一個數量級。三階段串接後，我的量級估計是**個位數 bit 甚至 0**。一個 SHA-256 hash commitment 需要 ≥128 bit，差了兩個數量級——**塞不進去**。

**方法論建議（給 B 直接可用）：** 用「bit error rate vs. channel condition」掃描量測，把每個通道階段當獨立 degradation，量 mutual information I(embedded; recovered)，這張 I-vs-condition 表就是 B 提案 2 第一階段可發表的貢獻（他自己也這麼規劃）。**但我的判決是：這張表大概率會證明電話通道下 soft binding 只能做 1-bit「這段音訊曾被合法簽署過」的存在性訊號，無法承載可驗證的 manifest 索引。** 這不是失敗，是一個對 EU AI Act Article 50（G 檢索 S8，2026-08 強制 machine-readable 標記）的重要否證：**法規要求的標記，在詐騙實際發生的電話通道上不可讀。** 這個政策含義本身就值得寫。

### 回答 Agent E（Q2）：電話通道的 codec buffer/jitter/PLC 延遲會不會淹沒生成端推論延遲？能否分離？

**會淹沒絕對延遲，但可以用「相對增量」部分分離——代價是給攻擊者留了規避窗口。** 詳見挑戰 4。技術上：

- **通道延遲的性質：** codec algorithmic delay（AMR-WB ~25ms、Opus 依 frame）+ 自適應 jitter buffer（50–200ms，隨網路狀態緩慢變動）+ 網路 RTT（跨網可破 400ms 且逐封包抖動）。這是一個**非平穩、與生成延遲同量級**的干擾源。你想量的「對不可預測內容的推論延遲」若是幾百 ms，就直接被埋在通道抖動裡。
- **可分離的部分：** 通道延遲在**單通話內短時間尺度上相對穩定**（jitter buffer 秒級才調整一次），而「對突發挑戰的 turn-taking 反應延遲」是**事件觸發的、語意層的**。做法：在通話前段（正常寒暄）建立對方的 baseline turn-taking 延遲分佈，挑戰時偵測**延遲增量**而非絕對值——這樣通道的固定偏移被 baseline 減掉。
- **殘留漏洞（我必須誠實指出）：** ①攻擊者只要在 baseline 期用真人或低延遲常規回應、在挑戰期才切高負載生成，你的 baseline 就被他控制；②baseline 本身要花時間建立，違背「高風險通話要快」的情境；③承挑戰 4，2026 的即時鏈路已壓到 <300ms，這個增量訊號的信噪比逐年惡化。**結論：latency 可作為輔助特徵但不能當主支柱，主支柱應是 prosody 即時可控性與非典型發聲**——這是我對你提案 1 判別訊號選擇的具體修正建議。

### 回答 Agent H（Q3）：AudioSeal 類 watermark 經「喇叭播放→手機翻錄」空氣通道後的存活率，有沒有實測或文獻數據？

**有間接文獻，方向一致地指向「重錄對浮水印非常致命」，但「空氣通道 + 電話 codec 串接」的公開實測目前是空白——這正是可做的貢獻。**

- **文獻現況：** AudioMarkBench（NeurIPS 2024，G 檢索 S4）系統測了**數位擾動**下的 removal/forgery，但**不含空氣重錄**。Latent-Mark（S4）測的是**神經 codec**抹除，也不是空氣通道。Audio Pirates（S4）做 diffusion-based 黑箱移除。**沒有一篇公開量測「喇叭→麥克風重錄」串接電話 codec 後的 AudioSeal 存活率**——G 在 1.2(c) 也點出「沒有任何公開研究量測浮水印能不能活過一通真實電話」。
- **我的物理預判（標明：猜測）：** 空氣重錄對 sample-level 對齊的 watermark（AudioSeal 靠時域 localized 偵測）特別致命，因為 RIR 卷積 + 重採樣時鐘偏移會破壞 sample-level 對齊；SynthID 這類頻域/頻譜浮水印可能稍韌但仍受 RIR 頻率選擇性衰落影響。串接 AMR-NB 之後我預期**接近全滅**。
- **對 H 提案一（AudioClash）的直接影響：** 你問「re-recording 是否讓 watermark 與 manifest **同時**消失，使稽核退化成單靠 passive detector」——我的答案是**大概率同時消失**（manifest 在容器層、重錄直接丟掉；watermark 在訊號層、空氣通道摧毀）。所以在「重錄 + 電話」這條最貼近詐騙的鏈上，AudioClash 的三層會塌成一層（只剩 passive detector），而 passive detector 在此條件下又逼近隨機（見 D-Q3）——**稽核協定在此情境退化為無資訊**。這不代表 AudioClash 沒價值，而是它的有效作用域必須誠實限縮到「語音訊息檔案 / 平台轉檔」這種容器與訊號層尚存的情境，把「即時電話 + 重錄」明確劃為協定的失效區。這個「作用域邊界」本身就是一個誠實且可發表的結論。

---

## 三、我支持的提案

### 支持 1 — Agent G 提案 G-2「活過一通電話嗎？真實電話通道存活性 benchmark（含繁中詐騙情境）」

**為什麼支持：** 這和我 Round 1 提案二（真實 laundering 傳輸鏈資料集）幾乎是同一個題目的兩個版本，而 G 的版本更完整——他加了浮水印存活與 source tracing 兩個評測軸，並用檢索證據（S5 電信部署、S6 STIR/SHAKEN 84%/21% 分裂、S10 Deepfake-Eval-2024 AUC −48%、台灣 165 體系）把「真實 vs 模擬的落差」這個 gap 錨得很硬。G 也正確引用了 #3 自承的「對未知真實管線無解」和 #2 的「multi-domain training 有害」，論證「先推斷通道、再條件化偵測」這條中間路線沒人走完——這正是我提案二的通道指紋模組。

**我的角色能如何補強：**
1. **通道矩陣的物理設計。** G 的風險備案擔心「真實通道收音的變因控制」（不同電信商/時段/網路狀態是混淆變因）。我可以貢獻一個受控的收發設備矩陣與 codec 路徑標註方案：固定 UE、記錄每通的協商 codec（AMR-WB/EVS/Opus）與實測 PLR/jitter，讓「真實 vs 模擬落差」的量測有乾淨的 confounder 控制——這是把 G 的「體力活」升級成有統計效力的實驗。
2. **通道指紋分類器。** G 說「codec 指紋分類是成熟技術」但沒展開；我 Round 1 提案二的核心就是這個模組（從 bit allocation、帶寬截止、PLC 波形特徵反推通道路徑），可直接嵌入 G-2 當第四個評測軸，並延伸成「通道宣稱 vs 通道證據」一致性檢查（「自稱銀行來電卻無任何電話 codec 痕跡」）。
3. **存活層級解釋框架。** G 的 benchmark 會產出「哪些偵測器在哪條通道劣化多少」，但和 #3 一樣是黑盒 EER。我的存活圖譜（提案一）能回答「為什麼劣化」——把 G 的黑盒劣化曲線拆解成第一/二/三層 cue 的存活貢獻。**兩者合流即是一篇「量測 + 機制解釋」都齊全的強論文。** 若指導教授只准一組人做，我主張把我提案二併入 G-2，我負責訊號層的物理拆解與通道指紋。

### 支持 2 — Agent D 提案 1「Adaptive-Laundering 攻擊成本曲線」

**為什麼支持：** D 把 laundering 從「防禦者視角的隨機 distribution shift」重新定義成「攻擊者最佳化的武器」，並提出 attacker-cost curve 當新指標。這個「成本軸」在 audio ADD 文獻中確實不存在，而且它直接服務「阻止機構部署形同無效卻讓人鬆懈的偵測器」這個社會目標——戳破虛假安全感。方法上不需訓大模型，碩士一年可行。

**我的角色能如何補強（也是 D 最缺的一塊）：** D 的攻擊成本曲線目前把每個 laundering 動作標一個「主觀成本代理」（工具難度、金錢、時間）。但缺一個**物理下界**：哪些動作是「不可逆資訊摧毀」（一旦做了，任何偵測器都救不回，成本對攻擊者=近零但收益=永久）、哪些只是「可逆 distribution shift」（防禦者補 DA 就能抵消，攻擊者要持續投入）。這個區分決定了曲線的形狀是「懸崖」還是「緩坡」。我的存活層級分析正好提供這個下界：

- 我能告訴 D，他猜測的「re-synthesis laundering + 一次平台真實轉檔是共通殺招」——**這個猜測我從物理上支持**（re-synthesis 重寫 excitation = 摧毀第一二層 + 部分第三層），並能量化它摧毀了哪幾層 cue、對哪類偵測器是懸崖式崩塌。
- 反過來，我能標出「哪些防禦設計選擇能讓曲線變陡」（D 想要的反向產出）：**依賴第三層存活特徵的偵測器，其攻擊成本曲線最陡**，因為攻擊者要洗掉第三層就必須破壞「聽得像目標語者」這個功能性約束——這是他不能付的成本（見 D-Q3）。這把 D 的經驗性成本曲線接上了一個物理原理性的解釋。

**合流形態：** D 提供攻擊者最佳化框架與成本軸，我提供每個動作的資訊理論可逆/不可逆標註與存活層級。產出的 attacker-cost curve 就不只是經驗曲線，而是有「物理硬下界」的曲線——這對部署方（銀行、電信、165）是更可信的「照妖鏡」。

---

## 附：我這份質詢與我 Round 1 立場的一致性

以上所有挑戰與回答都建立在我 Round 1 的單一核心主張——**cue 存活的分層性**——之上，沒有臨時改口。對 E 的同源連結、對 B 的 soft binding、對 A 的 one-class、對 D/E/F 的 latency，用的都是同一把尺：先問「你依賴的訊號在傳輸鏈出口物理上還剩多少」。我 Round 1 押注提案二（真實傳輸鏈資料集），Round 2 我很樂意把它併入 G-2 並貢獻訊號層拆解——因為研究的目的是降低民眾受騙率，不是保住我的提案編號。
