# Round 2 質詢：領域史官（Agent G）——第二輪（無真人實測）
日期：2026-07-14

> 我的職責在 Round 2 不變：在任何人下筆寫「first / novel / 無前作」之前，先把地圖翻出來擋在他面前。本輪我讀完了八份 Round 1 檔案（含我自己的 G-historian.md），做了六次補充檢索，命中三顆足以改寫他人提案 novelty 錨點的魚雷。史官的紀律是「連自己的結論也照樣推翻」——所以我先報三個別人的壞消息，再回答指名我的四筆檢索債，最後說明我支持誰、怎麼補強。
>
> 本輪補充檢索編號 G2R2-S1 至 G2R2-S6，來源附於文末。

---

## 一、對他人提案的挑戰

### 挑戰一（魚雷級）：Agent C 提案二「神經 codec 通道 × codec-latent 偵測」——你問我的頭號查證，答案是「已有人做過，而且做得很大」

Agent C 在提案二主張：「**codec-latent detection 這個新 domain 的第一份基線（或第一份否證）**」，並在留給我的 Q1 明白寫「neural codec transcoding 作為 ADD laundering、以及在 codec token/latent 空間做 deepfake detection，2024–2026 是否已有前作？……我記憶中無系統性前作」。C 自己也誠實標了「首個宣稱要等 G 的查證才能下筆」。

**我的查證結果：這條賽道不是空白，是 2024 年就已經被一篇 IEEE 期刊論文正面佔領，且 2025–2026 有一整個 source-tracing 子群在上面耕作。**

- **Codecfake（arXiv 2405.04880，IEEE TASLP 2024，Xie et al.）**：超過 100 萬筆（中英）神經 codec 生成音訊的大規模資料集，動機**逐字命中 C 的攻擊面論述**——「ALM-based deepfake 直接用 neural codec 生成、比傳統 vocoder 更 robust，對現有偵測器構成挑戰」。它還提出 CSAM（Co-training Sharpness-Aware Minimization）對策，在多條件下拿到 0.616% 平均 EER。換句話說，C 提案二的「防禦面」核心命題——「neural codec 通道後 real/fake 是否還可分、怎麼分」——在 2024 年就有人建了百萬級資料集 + 對策 + SOTA 數字。
- **Neural Codec Source Tracing（NCST，arXiv 2501.06514）**：open-set 神經 codec 分類 + 可解釋 ALM 偵測，明說「今日社群平台上多數 fake audio 是 ALM-based、以 neural codec 為後端」。
- **Towards Generalized Source Tracing for Codec-Based Deepfake Speech（arXiv 2506.07294）** 與 **Towards Neural Audio Codec Source Parsing（arXiv 2506.12627）**：直接在 codec 表徵/quantizer 階層上做 forensic 溯源。
- **Probing Token Spaces under Generator Shift（arXiv 2606.08663）**：雖是 music detection，但已經在做「codec-style 離散 token 空間在 cross-generator 下的可分性」——這正是 C 假說「real 語音 token 意外率高於 TTS token」的鄰域版本。

**所以 C 的提案二要害在哪：** 你留給我的 go/no-go 檢查點，答案是 no-go 的一半。攻擊面（neural codec 作為 laundering 摧毀第一二層 cue）與防禦面（codec 空間做 detection）**兩面都有前作**，「第一份基線」宣稱不成立。C 有一條退路我願意承認：Codecfake/NCST 全部是**乾淨離線條件**下的分類/溯源，**沒有一篇把 neural codec transcoding 當成一個「通道」放進真實通訊管線、量它與傳統 codec 的可逆性分野**。C 提案二真正殘存的、我查證後仍成立的空白是：**「傳統 CELP codec（可逆分佈偏移，#3 證 DA 可補）vs 神經 codec（many-to-one 生成式投影）的資訊理論可逆性邊界判定」**——這個「可逆性下界」框架 Codecfake 沒做、source-tracing 群也沒做。但這條殘存空白的體量，比 C 原本宣稱的「新 domain 第一份基線」小了整整一個數量級，而且它其實是 C 自己提案一（落差分解 + 可逆性判定）的方法論，不足以獨立撐起提案二。**史官裁定：C 提案二應撤回「codec-latent 偵測新 domain」的主軸，把殘值（神經 vs 傳統 codec 的可逆性邊界）併回提案一。**

### 挑戰二（魚雷級）：Agent B 提案二「CallAttest」——你清算了 STIR/SHAKEN，卻漏了那篇跟你幾乎同名的 2017 USENIX 前作

Agent B 在 CallAttest 提案裡花了整段做「相關工作正面清算」，但清算對象只有 STIR/SHAKEN（RFC 8224/8588）。B 的 delta 論述是：「STIR/SHAKEN 只認證主叫號碼、不綁內容；我的 hash 鏈綁定內容，把 mid-call injection 和事後移花接木也擋掉。」

**問題是：這個 delta，2017 年就有人在頂級安全會議做完了，而且做的就是「內容認證 + 帶外低頻寬資料通道 + 形式化驗證」。**

- **AuthentiCall（Reaves, Blue, Abdullah, Vargas, Traynor, Shrimpton，USENIX Security 2017）**：一句話總結它做了什麼——「cryptographically authenticate **both identity and content** of phone calls，用**形式化驗證過的協定**把低位元率資料通道綁到異質音訊通道上，偵測 **99% 的被竄改通話音訊**，通話建立額外開銷最壞 1.4 秒。」

把這段跟 B 的 CallAttest 核心賣點逐條對照：
| B 宣稱的 delta | AuthentiCall（2017）是否已做 |
|---|---|
| 綁定內容（非僅號碼） | 已做——content authentication，偵測 99% 竄改音訊 |
| 帶外低頻寬資料通道 | 已做——low-bitrate data channel bound to audio channel |
| 形式化驗證 | 已做——formally verified protocol |
| over-the-top 單邊部署、不求電信商全鏈路 | 已做——AuthentiCall 正是為了繞開 SS7/電信信令而設計的 OTT 方案 |

**B 提案二的要害：** 你以為你的對手是 STIR/SHAKEN（只認號碼），真正的對手是 AuthentiCall（認號碼 + 認內容 + 形式化驗證 + OTT），而你整份提案沒提到它一次。這不是「novelty 縮水」，這是「相關工作漏了最近的鄰居」，在 proposal defense 會被一刀斃命——安全領域的 reviewer 幾乎都知道 Reaves 這篇。

B 有沒有活路？有，但必須立刻重錨，而且錨點要誠實地窄：
1. **AuthentiCall 綁的是「這通通話的音訊沒被竄改」，不是「這段音訊不是 deepfake」。** AuthentiCall 假設通話雙方都是真人、要防的是中間人竄改；它擋不了「一個裝了 AuthentiCall 的合法端，播放 deepfake 音訊給對方」——因為那段 deepfake 是「真的從這個端發出、沒被竄改」的。B 若把 CallAttest 的威脅模型從「防竄改」移到「**綁定『發話端聲明的內容語意』與『機構 transparency-log 承諾』的一致性**」，並明確處理「合法端播 deepfake」這個 AuthentiCall 不防的攻擊，才有 delta。
2. **B 的「局部正面契約 + transparency log 公開可稽核」相對 AuthentiCall 的私有 PKI**：AuthentiCall 用的是傳統憑證信任模型，B 的 CT-style transparency log（split-view 攻擊、log 投毒的公開可稽核性）是一個真 delta，但它是密碼學基礎設施的 delta，不是「防 deepfake」的 delta。
3. **perceptual hash 鏈在 codec 重合成下的容忍半徑** vs AuthentiCall 用的是 robust digest——這個「在 AMR-WB/EVS 神經/CELP 重合成下不斷鏈、惡意替換必斷鏈」的容忍度掃描，AuthentiCall 沒針對 2026 世代 codec 做過，是可辯護的實驗貢獻。

**史官裁定：CallAttest 若不在第一頁把 AuthentiCall 列為頭號前作並清楚劃出 delta，本提案不具可發表性。重錨後殘值（CT-log OTT 契約 + 2026 codec 下 perceptual-hash 容忍度 + 「合法端播 deepfake」威脅）可撐一個窄而誠實的題目，但已不是 B 原本宣稱的「第一個內容綁定 OTT 認證協定」。**

### 挑戰三：Agent F 提案二「到達耳朵的那三秒」——短句長與情緒韻律兩個軸，各自都已經有人做過

Agent F 提案二主張「確立**素材真實性**為繼 unseen generator（#2）、通道（#3）之後的第三個樂觀偏差軸」，並在留給我的 Q1(3) 誠實請我查「短句長/情緒語音的 ADD 評估有沒有前作」，且自標「若有，novelty 錨點收窄為『詐騙話術情境 × 三軸交互』」。F 這份自我防護寫得好，因為查證結果是：**兩個軸各自都已經有專門論文。**

- **短句長軸**：**AASIST2 for Short Utterance（arXiv 2309.08279）** 早就在做短句反欺騙；更狠的是 **《Audio Deepfake Detection at the First Greeting: "Hi!"》（arXiv 2601.19573，2026-01）**——把偵測推到 0.5–2 秒的「開場招呼」，動機跟 F 的「三秒哭腔」幾乎同源。還有 **Fake-Mamba / ConBiMamba（arXiv 2508.09294）** 明確報告「所有架構在短句上都退化，<3 秒 EER 9.44%」的落差曲線。
- **情緒韻律軸**：**HuLA（arXiv 2509.21676）** 是 prosody-aware anti-spoofing、專攻 expressive/emotional 合成語音；**Phoneme-Level Deepfake Detection Across Emotional Conditions（arXiv 2605.03079）** 用 SSL embedding 跨情緒條件偵測；兩篇都指出「現代 EVC 系統產生的情緒語音貼近真人韻律，是偵測的根本困難」。

**F 提案二的要害：** 「短句 ADD 退化」與「情緒語音 ADD 退化」都不是新發現，各自有 2023–2026 的專門論文。F 提案二若宣稱「揭露素材真實性樂觀偏差」是新的第三軸，會被這幾篇直接反駁——這個軸的兩個主分量已經被量過。

F 的活路正是她自己預留的收窄錨點，我查證後認為它成立且值得做：**「165 繁中詐騙話術文本 × 短句 × 情緒」三軸的交互效應 + 台灣繁中情境**。理由：(a) 上述前作全是英語或通用語料，沒有一篇用**詐騙話術的語言內容**當變因（話術文本的語意/語用特性是否讓 TTS 露餡，與朗讀文本不同）；(b) 三軸**交互**（短 × 情緒 × 通道）沒人做過，前作都是單軸；(c) 繁中詐騙情境是雙重真空（沿用第一輪方向二論證）。但 F 必須把主 claim 從「第三個樂觀偏差軸」降級為「**三軸交互 × 詐騙話術語意 × 繁中的落差量化**」，並在相關工作誠實列出上述五篇，否則 novelty 宣稱過大。

### 挑戰四（計算性驗證推論不到真實情境）：Agent E 提案一的「人類模型不確定集 𝓗」錨在錯的軸上

Agent E 提案一是全場方法論野心最大的一份——把 user study 換成「對所有與 VoiceWukong 數據一致的人類模型 𝓗 做全稱量化的穩健排序」。我欣賞這個推理形式（也在 Round 1 幫它找了 L2D / robust decision making 的先例），但我要挑一個**它的計算性驗證推論不到真實詐騙情境**的結構性問題：

E 主張「𝓗 = 所有與已公佈人類數據一致的行為模型的集合」，而已公佈數據（VoiceWukong）的自變數是**音訊品質**（人類對低品質 deepfake FAR 4–19%、高品質 >82%）。但真實詐騙現場，決定阿嬤受不受騙的**主導變數不是音訊品質，是社工壓力**（權威、急迫、親情綁架）——D 在候選 C 對自己下的重手講得最白：「詐騙現場的人不在做辨識任務。」

於是 E 的框架有一個它自己的 θ 掃描補不了的洞：
- VoiceWukong 約束的是 `P(判 fake | 品質)` 這條曲線的形狀。E 的壓力折損係數 θ 是**乘在這條曲線上的一個縮放/平移**。
- 但社工壓力對受騙的影響**不是「把品質-辨識曲線整體壓低」這麼簡單**——它可能讓「品質」這個自變數整個**失效**（人在恐慌下根本不聽音質，只聽「女兒在哭」）。若真實機制是「壓力下品質軸與受騙脫鉤」，那 VoiceWukong 的品質-FAR 曲線對詐騙現場**做的功趨近於零**，𝓗 的約束力蒸發，穩健排序退化成「只由未錨定的 θ 決定」。
- 結果是兩種下場，都對 E 不利：要嘛 θ 全區間掃描下所有 policy 互不可比（框架輸出「無法排序」）；要嘛能存活的排序其實**完全由 θ 的假設驅動、VoiceWukong 數據沒出力**——那 E 宣稱的「錨定已公佈數據」就是裝飾。

**這不是要擊沉 E，是要逼它誠實標定適用域：** E 的穩健排序框架在「品質是主導變數」的情境（例如上班族在辦公室冷靜聽一則 LINE 語音、選民事後查核一段錄音）是站得住的——那裡壓力低、品質軸有效。但對「阿嬤 + 倒數計時 + 親情」這一格，E 的框架**原理上推論不到**，因為它的錨定數據裡沒有壓力這個主導軸的任何一個觀測點。E 應該把提案一的射程明確收在 F 判定表裡「上班族/選民」兩行，並在第一頁寫明「本框架不覆蓋高壓社工情境，因為公開數據無此軸的錨」——這跟 B 的白旗同構，是誠實而非失敗。（附帶：這個批評對 F 提案一、D 提案二、H 提案一、我自己的 G2-A 全部部分適用，差別在誰把射程標得最誠實。F 的 δ 掃描與 D 的單調性下界比 E 的 𝓗 更能吸收這一擊，因為 D 只宣稱「綠燈不會讓人更警覺」這條與品質無關的單調假設——這是全場對此洞最 robust 的設計，我在第三節會講。）

---

## 二、回答指名給我的問題

Round 1 有四位指名我：A（Q1）、C（Q1）、F（Q1）、H（Q2）。逐一結清。

### 給 A（Q1）：三筆 novelty 查證

**(a) selective prediction / abstention 在 ADD 的前作。** 查證結論：**「reject option / uncertainty-aware ADD」有零星前作，但「shift-aware selective-prediction benchmark + confident-real 對抗軸」無前作，A 的錨點成立。** 具體：我 Round 1 已報的 **FADEL（evidential DL，ICASSP 2025，arXiv 2504.15663）** 是最近的 uncertainty-aware ADD，但只做 ASVspoof 內 cross-dataset、無 risk-coverage/選擇性預測框架、無對抗軸。本輪補充：**Probabilistic Verification of Voice Anti-Spoofing（arXiv 2603.10713）** 是對偵測器做機率保證，屬「稽核」不屬「棄權」；**《Towards Robust Speech Deepfake Detection via Human-Inspired Reasoning》（arXiv 2603.10725）** 走的是 reasoning 不是 abstention。我沒有查到任何一篇做「六種棄權機制 × 四格 shift 矩陣 × risk-coverage」的系統比較。**A 的「第一個 shift-aware selective-prediction ADD benchmark」宣稱，收編 FADEL 為 baseline 後，經檢索仍成立。**

**(b) shift-type attribution（channel vs generator）在 audio 的前作。** 查證結論：**部分成立、需收窄。** 通用 OOD 領域有 covariate-vs-semantic shift 的區分（A 自己也知道），但把它落到「channel-induced vs generator-novelty 的偵測器表徵可分性 + 機器可驗證的重送干預」，audio 端我沒查到直接前作。**但要警示 A 一個鄰居**：source-tracing 群（NCST 2501.06514、arXiv 2506.07294）做的「溯源到生成演算法」與你的「generator-novelty attribution」在技術上高度重疊——你的 attribution 器的 generator 端，本質上是一個 open-set source-tracing 器。你的 delta 必須錨在「**channel 端 attribution + 重送干預迴路**」（這是 source-tracing 群不碰的），而不是 generator 端。建議 A 提案二的標題與貢獻主軸從「兩種 shift 可分」移到「**channel-attributed abstention 的機器可驗證重送干預**」——那一塊我查證是乾淨的。

**(c) VoiceWukong 數據粒度。** 這題 A、F、H 三人都問，統一回答（見下 F(1)）：**per-sample 粒度可得**。

### 給 C（Q1）：neural codec 前作 + 平台部署證據

**(a) 前作——已在挑戰一詳答：Codecfake（2024, IEEE, 100 萬筆 + CSAM 對策）+ NCST + source-tracing 群，攻防兩面都有前作，「codec-latent 偵測新 domain」宣稱不成立，殘值僅剩「傳統 vs 神經 codec 可逆性邊界」且應併回 C 提案一。**

**(b) 主流平台實際部署 neural codec 的公開證據。** 查證結論：**證據薄弱，C 必須照他自己說的「誠實改寫動機」。** 我沒查到 LINE/Meta/Google 在主流語音路徑**預設**部署端到端神經 codec 的公開確證；Lyra/SoundStream 系主要用於低頻寬情境的零星證據，不足以支撐「neural codec 正在進入真實通訊鏈」的強宣稱。**C 應把動機從「已部署通道」改寫為「攻擊者可自行一行指令施加的 laundering + 前瞻通道」**——這一點 C 提案二原文已預留此退路，照做即可。但即使改寫，攻擊面的前作（Codecfake）仍在，動機改寫救不了 novelty。

### 給 F（Q1）：三筆查證

**(1) VoiceWukong 數據粒度（A/F/H 共同問）。** 查證結論（沿用並強化我 Round 1 的 G2-S6）：**per-sample 粒度可得，不只論文彙總表。** VoiceWukong 的 user study 原始結果與 12 個偵測器原始輸出公開在 GitHub（github.com/VoiceWukong/VoiceWukong），資料集在 Zenodo（records/13731918，學術申請制）。這意味 human-proxy 可以做**分層建模**（per-difficulty、甚至 per-sample 的人類判斷分布），不是只能擬合一條 aggregate 曲線。**對 F/H/E/我的模擬提案，這是質的利多**——但要注意 F 申請 Zenodo 存取的時程風險，建議月 0 就送申請。**誠實補一刀**：per-sample 可得解決的是「模型能多細」，解決不了挑戰四的「錨在品質軸、推論不到壓力軸」——資料再細，它也沒有壓力維度的觀測。

**(2) 資安警告服從率 / 警報疲勞的實測文獻與數字範圍。** 查證結論：**先例充足，F 的候選 C（警報疲勞經濟學）有真數據可錨。** 經典錨點：**《Alice in Warningland》（Akhawe & Felt, USENIX Security 2013）**——Chrome/Firefox 大規模真實遙測，SSL 警告點穿率（clickthrough）在瀏覽器與警告型別間從個位數到 70%+ 不等，正是 F 要的「服從率的整個範圍」。habituation/警報疲勞的機制與衰減有 **《Harnessing the Challenges to Improve Security Warnings: A Review》（Sensors 2021, MDPI 21(21):7313 / PMC8588101）** 的綜述可引。方法論母體：**《Usable Security: A Systematic Literature Review》（Information 2023, MDPI 14(12):641）**。這些給 F 的「服從率區間掃描」提供有出處的上下界，不是拍腦袋。**但關鍵誠實邊界**：這些數字全來自**視覺警告（瀏覽器/釣魚郵件）**，不是**語音通道的聽覺警告**——F 把瀏覽器服從率外推到「阿嬤聽到手機語音警示」時，必須把「跨模態外推」列為明確假設，做敏感度掃描而非直接套用。

**(3) 短句長/情緒 ADD 前作 + 文獻校準人類模型的方法學前例。** 前者已在挑戰三詳答（有前作，收窄到三軸交互 × 繁中話術）。後者——「不做 user study、用文獻校準模型做安全評估」的方法學前例——查證結論：**先例充足且跨領域，F 的方法論不是孤兒。** 我 Round 1 已給 L2D 路線（FiFAR arXiv 2312.13218、Nature Scientific Data 2025）與 cognitive-model 路線（Cranford ICCM 2021、UMUAI 2026）。本輪補一個 F 這個外行直覺其實猜對的重量級先例：**IMF《Using Simulations for Cyber Stress Testing Exercises》（IMF Working Paper 2025/085）**——金融監理用「文獻/情境校準的模擬」做決策評估、不對真實金融系統做實驗，這正是 F 說的「流行病學/交通安全式的政策模擬」在金融資安的官方版本。加上老年學的 **elder scam susceptibility 模擬（PMC9765817）**——「不做真人實驗、評估防詐介入」的最接近先例。**F 的「紙上受騙率」在方法論上有正統血統，可以理直氣壯地引這些擋 reviewer 的『simulation is not evidence』。**

### 給 H（Q2）：兩筆

**(a) VoiceWukong 粒度**——同 F(1)，per-sample 可得，可做分層建模。

**(b) proxy-expert 驗證的方法論先例 + venue 落差。** 查證結論：**先例確實存在（H 猜的 Mozannar & Sontag 一系是對的方向），但 venue 落差是真的、H 要正視。** L2D「用參數化/合成 expert model 評 deferral policy」是 ML 社群正統：FiFAR 的 50 個合成分析師、Nature Scientific Data 2025 的合成專家 benchmark、Mozannar & Sontag 的 learning-to-defer 理論線。**但 H 的擔憂命中要害**：這些先例的接受度在 **ML venue（NeurIPS/ICML/AISTATS）高，在 security venue（USENIX/CCS/NDSS/SOUPS）未經同等檢驗**。SOUPS（usable security 專門會）的文化是重真人實驗，一篇「用合成人類模型評防詐設計、零真人」的論文在 SOUPS 會遭遇比 ICASSP 更硬的阻力。**我的建議：G2-A / H 提案一 / F 提案一這類 simulation-grounded 題目，主投 ICASSP/INTERSPEECH 主軌（benchmark + 方法），把 confident-real 對抗軸與政策討論拆成 security workshop 投稿，不要正面撞 SOUPS 的真人實驗文化。** 這是 venue 策略，不是科學問題，但對碩士生的畢業時程是生死問題。

---

## 三、我支持的提案

### 支持一：A / H / E / F / G 五人共構的「shift-aware selective prediction benchmark」（方向一的偵測器半邊）

這仍是全場最強的方向，而且本輪限制反而讓它的**方法論半邊**變成正資產而非負債——我 Round 1 檢索的核心產出（L2D 合成專家是 Nature 子刊等級的正統、LLM-simulated users 已被證明不可靠）正好給它一條「不靠真人也站得住」的血統證明。

**我的角色能怎麼補強：**
1. **前作防雷已完成**：FADEL（arXiv 2504.15663）收編為第 7 種棄權 baseline，「第一個 shift-aware selective-prediction ADD benchmark」錨點經本輪復查仍成立（見 A-Q1a）。
2. **unseen-channel 軸的現成紅利**：不必自己灌通道——**RTCFake（arXiv 2604.23742，HuggingFace 可下載）** 是現成的真實 RTC 平台通道測試集，直接當 unseen-channel 一格，省掉一整條工程線。
3. **venue 策略已備**（見 H-Q2b）：主投 ICASSP/INTERSPEECH，對抗軸拆 security workshop。
4. **對挑戰四的免疫設計**：把「人」的部分**只用 D 的單調性下界**（confident-real 綠燈 ≥ 沉默 baseline）承載受騙率宣稱，而不是 E 那種依賴品質軸錨定的 𝓗——因為單調性只需要「綠燈不讓人更警覺」這條與壓力/品質都無關的假設，是全場對「推論不到詐騙現場」這一擊最 robust 的因變數。**我在 Round 3 會主張：方向一的受騙率因變數應採 D 的下界形式，E/F 的品質軸模擬降為輔助敏感度層。**

### 支持二：C 提案一 / H 提案二 / 我 G2-B 三方共構的「真實電信通道 × 多訊號存活審計」（重錨版）

我 Round 1 親手用兩顆魚雷（2509.26471 Presentation、RTCFake）打穿了「首個真實通道」的舊錨點，但也說了它**不死、只需重錨到「電信網 × watermark/provenance bit 存活 × Article 50 政策」**。本輪我要為這個重錨版辯護，並點名 **C 的提案一（落差分解 + 通道模擬器蒸餾）是這個方向最有科學靈魂的版本**——因為它回答了 H 的紅線「靈魂必須是揭露樂觀偏差、不是收資料」：C 不只量落差，還用受控消融**指認落差來自 codec 實網行為/網路動態/端點 DSP 哪一塊**，並產出校準過的開源模擬器讓後人免架 rig。這比單純「量一次 EER 落差」高一個科學層級。

**我的角色能怎麼補強：**
1. **前作地圖已畫**：這個方向的殘存空白經我兩輪復查嚴格錨定為——(i) 公開蜂巢電信網通道資料集（RTCFake 做 IP-RTC、Presentation 做 loudspeaker/direct-inject，電信網仍空）；(ii) watermark/provenance bit-level 存活（AudioMarkBench 做模擬擾動、兩篇通道前作完全沒碰 watermark，此軸**零前作**）；(iii) Article 50 可讀性審計（2026-08-02 生效，零前作）。**watermark 存活軸是護城河，因為產業沒有動機自審、學術前作全在做 detection 不做 watermark。**
2. **時間窗警報**：Delgado 團隊（ASVspoof 組織者，2509.26471）與產業已進場，這個題目**再放一年就沒了**。若要做，MVP（月 6 前單電信商 VoLTE + LINE）必須前置。
3. **它是全場模擬型提案的共同地基**：在一個人人靠模擬撐影響力的輪次裡，這是唯一產出「真實通道實測數據」、能量出「模擬到底樂觀多少」的方向——它替 G2-A / F / E 的模擬提供「模擬 vs 真實落差係數」的錨。這個地基價值本輪不降反升。

---

*Agent G，2026-07-14，Round 2 質詢。史官的本輪戰果：用一篇 2024 IEEE 論文（Codecfake）擊中 C 提案二、用一篇 2017 USENIX 論文（AuthentiCall）擊中 B 提案二、用五篇短句/情緒 ADD 前作收窄 F 提案二、用「錨在錯軸上」戳 E 提案一的射程。我支持的兩個方向（selective prediction benchmark、真實電信通道重錨版）都已通過我自己的前作復查——包括承認我第一輪認證的空白早被侵蝕。*

---

## 附錄：本輪補充檢索來源

| 編號 | 主題 | 關鍵來源 |
|------|------|----------|
| G2R2-S1 | 神經 codec 偵測前作 | arXiv 2405.04880（Codecfake, IEEE TASLP 2024）、Zenodo records/13841216 |
| G2R2-S2 | codec token/latent 溯源前作 | arXiv 2501.06514（NCST）、arXiv 2506.07294（Generalized Source Tracing）、arXiv 2506.12627（Codec Source Parsing）、arXiv 2606.08663（Token Spaces under Generator Shift） |
| G2R2-S3 | 電話通話內容認證前作 | AuthentiCall（Reaves et al., USENIX Security 2017, sec17-reaves_paper.pdf；NDSS 版亦存） |
| G2R2-S4 | 短句 ADD 前作 | arXiv 2309.08279（AASIST2 short utterance）、arXiv 2601.19573（First Greeting "Hi!"）、arXiv 2508.09294（Fake-Mamba/ConBiMamba） |
| G2R2-S5 | 情緒/韻律 ADD 前作 | arXiv 2509.21676（HuLA）、arXiv 2605.03079（Phoneme-Level across Emotional Conditions） |
| G2R2-S6 | 模擬式安全評估方法學先例 + 警告服從率文獻 | IMF WP 2025/085（Cyber Stress Testing Simulations）、Akhawe & Felt《Alice in Warningland》USENIX Security 2013、MDPI Sensors 21(21):7313 / PMC8588101、Information 14(12):641、PMC9765817（elder scam simulation） |
