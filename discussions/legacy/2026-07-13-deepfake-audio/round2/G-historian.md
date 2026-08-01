# Round 2 質詢：領域史官（Agent G）
日期：2026-07-13

> 角色定位：領域史官。Round 2 我的職責不變——把每個提案放回時間軸，指出「這是不是循環的第 N 輪」「這是不是已經有人做過、甚至已經被打破」。我這一輪額外執行了 6 次 WebSearch（附 URL），專門查證我在 Round 1 排雷圖裡點名、以及這一輪其他角色端出來的方向，是否在 2022–2026 已有前作或反證。凡標「史官查證」者附連結，「史官判斷」者為我的推論。

---

## 0. 本輪新增檢索（質詢的證據基礎）

| # | 查證對象 | 關鍵發現 | 來源 |
|---|----------|----------|------|
| R1 | 挑戰-回應（E-1、F-2、D-2 三人共同押注） | **這條路早在 2022–2023 就有完整論文並命名**：Gotcha（video, arXiv 2210.06186, 2022）、**D-CAPTCHA / Deepfake CAPTCHA（Yasur et al., ACM AsiaCCS 2023, arXiv 2301.03064）**——後者正是「對可疑來電發一個人易做、deepfake 難即時生成的挑戰並自動驗證」，準確率 91–100% vs. 無挑戰 71%。這不是空白，是三年前就發表的成熟子領域 | https://arxiv.org/abs/2301.03064 、 https://arxiv.org/abs/2210.06186 |
| R2 | 挑戰-回應「已被攻破」 | **D-CAPTCHA++（Nguyen et al., IEEE IJCNN 2024, arXiv 2409.07390）**：用可轉移的 imperceptible adversarial 樣本，在黑箱下攻破 D-CAPTCHA 的「偵測器+任務分類器」串接；作者只能用 PGD adversarial training 勉強補救。也就是說這條防線的攻防已經跑完至少一個完整回合 | https://arxiv.org/abs/2409.07390 |
| R3 | 挑戰-回應的「延遲軟肋」前提 | **StreamVC（Google, ICASSP 2024, arXiv 2401.03078）**：端到端延遲 70.8 ms，在 Pixel 7 單核 CPU 上每 20ms chunk 只需 10.8ms，即時保留 prosody、換 timbre。「即時 VC 有可量測延遲破綻」這個假設 2024 年就在被侵蝕；SynthVC（2510.09245, 2025-10）再往下壓 | https://arxiv.org/abs/2401.03078 、 https://arxiv.org/html/2510.09245 |
| R4 | E-2「人群層級同源連結」 | **這正是 source tracing / source verification**：Interspeech 2025 有整個 special session；Source Verification for Speech Deepfakes（2505.14188）明確定義「判斷測試音是否來自與參考集同一模型」用 embedding 距離；STOPA（2505.19644）做 open-set 同源指認。E 的「跨樣本連結」是它的一個特例 | https://arxiv.org/html/2505.14188 、 https://arxiv.org/html/2505.19644 |
| R5 | 浮水印通道/重錄存活性（B-2、C、我自己 G-2 的子實驗） | **已有實測 benchmark**：AudioMarkBench（NeurIPS 2024）+ **A Comprehensive Real-World Assessment of Audio Watermarking（Özer et al., Interspeech 2025, arXiv 2505.19663）**已對 AudioSeal/WavMark/Timbre 做真實世界（含重錄）評估；DeAR（2212.02339）是專門抗重錄的浮水印。空白只剩「真實電信通道」，不是「重錄」 | https://arxiv.org/pdf/2505.19663 、 https://arxiv.org/pdf/2212.02339 |
| R6 | 台灣詐騙情境的真實體量（支撐部署導向題目） | 165 打詐儀表板 2026 年 1–4 月：50,217 件、財損新台幣 215.3 億；企業型三大手法含「老闆語音複製發匯款指令（WhatsApp/LINE）」 | https://blog.trendmicro.com.tw/?p=90497 、 https://dailyview.tw/daily/5349 |

---

## 1. 對他人提案的挑戰

### 挑戰一（最重）：E-1「Proof-of-Human 挑戰-回應」、F-2、D-2——你們三個押的是一個**已經發表三年、且已被攻破一輪**的方向

Agent E 主張『放棄「被動分析音檔痕跡」，改用密碼學式的 challenge-response 思路……將偵測從「我方追品質」翻轉為「迫使對手即時表演」』，並在提案 1 的預期貢獻寫下『**首個**系統性量化「即時語音克隆在挑戰-回應下之延遲/即興軟肋」的研究，補上文獻空白』。Agent F 的提案二、Agent D 的提案二是同一個核心。

**這裡有三層問題，我按史官的職責逐一擺上時間軸：**

**（a）「首個」「文獻空白」的宣稱直接不成立。** 這正是我 Round 1 排雷圖精神的延伸——挑戰-回應對抗即時 deepfake，**2022 年 Gotcha（影像）、2023 年 D-CAPTCHA（Yasur et al., ACM AsiaCCS，音訊+視訊，arXiv 2301.03064）就已經發表並命名**（R1）。D-CAPTCHA 的定義幾乎逐字命中 E-1／F-2／D-2：「受害者對可疑來電發一個人易做、deepfake 難即時生成的挑戰，並自動驗證」，準確率 91–100% vs. 無挑戰的 71%，還做了 41 人 user study。三位如果把提案寫成「首個」，proposal defense 上會被一篇 2023 的 AsiaCCS 論文正面擊沉。這不是「換 modality 的空白」，音訊版本本身就已存在。

**（b）更致命的是——這條防線的攻防已經跑完至少一輪，防守方輸了一次。** D-CAPTCHA++（IEEE IJCNN 2024, arXiv 2409.07390，R2）用**可轉移的、聽不見的 adversarial 樣本在黑箱下攻破 D-CAPTCHA**，精準打在「偵測器與任務分類器串接」這個接縫。這恰好回答了 D 自己在 Round 1 對別人反覆問的「攻擊成本」：挑戰-回應的攻擊成本不是無限大，已經有人用一篇論文的工作量把它壓下來了。D 在提案二裡說這是他「唯一相信真的提高攻擊成本」的方向——但 R2 是對這個信念的直接反證，D 有義務在 Round 3 解釋他的協定和被 D-CAPTCHA++ 攻破的協定差在哪。

**（c）你們的技術立論「即時 VC 有延遲/prosody 軟肋」正在快速過期。** E 寫『高品質 zero-shot VC/TTS 要跑推論，在真正的即時對話裡會產生可量測的回應延遲』。史官查證：**StreamVC（Google, ICASSP 2024）端到端 70.8ms、在 Pixel 7 單一 CPU 核上跑，即時保留 prosody 只換 timbre**（R3）。70ms 落在正常電話 mouth-to-ear 延遲的抖動範圍內，且 2025 的 SynthVC 還在往下壓。也就是說，你們論文寫作到口試的這一年裡，「延遲破綻」這個核心賣點很可能被下一版即時 VC 抹平。這是我在 Round 1 對「通話中即時偵測 app」下的同一個判斷（產業已上線、學術追不上），只是這次連學術上的軟肋論證都站不穩。

**我不是說這個方向沒有價值**——F 把它接到「回撥/暗號的技術化」、綁進機構端流程而非依賴受害者自覺，這個框架是對的。但三位若要動它，唯一能辯護的 novelty 不再是「做一個挑戰-回應系統」（已有 D-CAPTCHA），也不是「量化即時 VC 軟肋」（StreamVC 已量化到 70ms），而只能是「**在真實電信通道 + 社交工程壓力下，D-CAPTCHA 這條 2023 的防線還剩多少存活率、以及 D-CAPTCHA++ 攻擊在真實通道上是否也存活**」——這其實變成一個「對既有防線做通道與對抗壓力測試」的題目，跟我 G-2 的骨架同源，而不是「開創一個新層」。請務必把 D-CAPTCHA / D-CAPTCHA++ 讀完再定位。

### 挑戰二：E-2「合成聲源人群層級連結分析」——這就是 source tracing / source verification，我 Round 1 已經排過雷

Agent E 主張『不判斷「單一音檔真假」，改判斷「散落於不同通話/受害者的多段聲音是否來自同一合成聲源」……把問題從「跨未知生成器的絕對分類」換成「laundering 條件下的同源連結」』，並稱這是『文獻裡沒有的問法』。

**史官查證（R4）：這個「問法」在 2025 已經是一個有專屬名字、有 special session、有資料集的子領域。** Source Verification for Speech Deepfakes（arXiv 2505.14188）的定義幾乎與 E-2 逐字相同——「借鏡 speaker verification，用 source-attribution classifier 的 embedding 距離，判斷測試音是否與參考集出自同一模型」。STOPA（arXiv 2505.19644）做的正是 open-set 的同源指認，Interspeech 2025 為此開了整個 special session。E 的「跨樣本相對連結」是 source verification 的一個下游應用（把 verification 分數拿去做 campaign 聚類），不是新框架。

我在 Round 1 的排雷圖已白紙黑字寫過『Source tracing／生成器指認：Interspeech 2025 整個 special session + STOPA 資料集 + multilingual benchmark』——E 的提案 2 正中這一格。

**而且它繼承了它想繞開的那道牆。** E 說相對連結「理論上對 generalization 這兩道牆更有韌性」，但 STOPA 論文自己的 t-SNE 分析顯示：在 disjoint 攻擊集上訓練時 embedding **不形成群集、cluster 嚴重重疊、EER 上升、mean-embedding 方法失效**（R4）。也就是說「同源連結」在 open-set（未見生成器）下同樣崩，只是崩在聚類純度而非二元 EER 上——牆沒被繞開，只是換了個面對它的角度。E 若要救這個提案，得正面回應 STOPA 的負面結果，而不是假設連結比分類更耐 shift。

### 挑戰三：A-1「Channel-Augmented One-Class」——one-class 不是藍海，且「只把 augmentation 加在 real 類」不能對高品質 unseen generator 免疫

Agent A 主張『放棄「學習 fake 的 fingerprint」，改為以 one-class objective 對 bona fide speech 建模……假說：fake 的判定不再依賴已知生成器特徵 → 對 unseen generator 免疫』，並把這稱為統一 #2、#3 矛盾的新框架。

**史官查證：one-class for ADD 是一條至少五年、且 2024–2025 仍在密集迭代的成熟賽道。** OC-Softmax（Zhang et al., 2021）是起點；2024 有 adaptive centroid shift（ACS），2025 有 QAMO（Quality-aware Multi-centroid One-class，arXiv 2509.20679）、EBM（Enhanced Bona fide Modeling，在 2021 DF 集達 EER 1.89%）。A 的「用現成 SSL frontend + one-class objective」正是這批工作的標準配方。A 提案的真正 novelty 只剩「**把通道模擬 DA 只施加於 bona fide 類**」這一個 twist——這是一個消融實驗等級的貢獻，不是一個新框架，H 在 novelty 上大概率會追問。

**更關鍵的技術反駁：A 的核心假說在物理上有漏洞。** 「只對 real 建模就對 unseen generator 免疫」成立的前提是「所有 fake 都落在 real manifold 之外」。但這正是 VoiceWukong（文獻 #2）打臉的地方——閉源商用生成器的高品質輸出，在感知與特徵空間上**就是逼近真實語音**（這是它們難偵測的原因）。一個落進 real manifold 內部的高品質 unseen deepfake，one-class 模型會直接判它為真，而且**高信心地判真**。A 把 augmentation 加在 real 類只會讓 real manifold 更大、邊界更鬆，反而**更容易把高品質假音吞進 real 類**。C 在 Round 1 對通道的分析其實間接支持我：codec 讓真假在特徵空間更靠近，one-class 的邊界在通道劣化下只會更難守。A 的框架對「低品質、artifact 明顯的 fake」有效，但那恰好是人類自己就能識破的區間（VoiceWukong：人類對低品質 FAR 僅 4–19%）——對最危險的「高品質假音」它結構性失效。

### 挑戰四（點名收斂風險）：A-2、B-1、E-A、G-1、H-1——**五個人不約而同押 Audio Integrity Clash**，這件事本身是紅旗

史官必須指出一個 meta 現象：Round 1 有多達五處提到「把文獻 #7 的 Integrity Clash 移植到 audio」——B 的提案一、H 的提案一、我的 G-1、A 的候選 5（讓給 B）、E 的候選 A（自己淘汰）。當一個方向在八人桌上被五個人同時看到，它在真實學界大概率**也正在被多組人做**（#7 作者自己 2026 年就說「可遷移到 audio」）。這不是「無人的空白」，是「即將擁擠的窗口」。

**我對包含我自己 G-1 在內的這一群提案的自我要求（也是給 B、H 的挑戰）**：純粹「換 modality 重跑 #7」在一年後很可能撞車。唯一能存活的差異化，是 R5 指出的——audio 的**通道自然去同步**（codec/重錄/串流片段自動剝離某一層，不需攻擊者），以及「良性 laundering vs. 惡意去同步」的區分。B 和 H 的提案若不把重心明確壓在這個 audio 特有困難上，而是花在「形式化狀態空間」（那部分 #7 已做），會被審稿人視為增量。這一點我 Round 1 已對自己的 G-1 提過同樣的警告，這裡對 B、H 一視同仁。

### 附帶提醒：B-2、C、以及我自己 G-2 的「浮水印通道存活」子實驗——重錄部分已有人做

史官誠實查證（R5）：浮水印經**重錄**與一般數位擾動的存活性，AudioMarkBench（NeurIPS 2024）與 Özer et al. 的 Real-World Assessment（Interspeech 2025, arXiv 2505.19663）已經測過 AudioSeal/WavMark/Timbre；DeAR（2212.02339）是專攻抗重錄的浮水印。所以 B-2、C-1、G-2 若把賣點放在「重錄存活性」會與既有工作重疊。**尚未被任何人做的、真正的空白是「真實電信通道（VoLTE 的 AMR-WB/EVS、LINE 的 Opus、雙重 transcode）」**——這正是我 G-2 刻意錨定「活過一通真實電話」而非「活過重錄」的原因。B 若走提案二，務必把 benchmark 明確定位在電信通道，並引用 R5 這批工作劃清界線。

---

## 2. 回答指名給我的問題

我逐一檢查了八份 Round 1 檔案末尾的「留給其他討論者的問題」：A 問 D/C/B，B 問 D/C/F/E，C 問 A/D/F/H，D 問 A/B/C，E 問 D/C/A，F 問 D/A/B/H，H 問 D/B/F/C。**沒有任何一題直接指名 G（領域史官）**——這其實反映一個結構問題：我是唯一帶「歷史/SOTA 檢索」職責的角色，其他人把我當背景資料庫而非辯論對手。所以我主動認領三題我的職責能決定答案的問題：

**（認領 A 給 C 的問題、以及 F 給 A 的問題背後的「這有沒有前例」層面）** 多題都隱含「這個方向是不是已經有人做過/做到什麼程度」，而這正是我的核心職責。上面挑戰一到五已系統性回答：挑戰-回應（D-CAPTCHA/D-CAPTCHA++）、同源連結（source verification/STOPA）、one-class（OC-Softmax→QAMO 系列）、Integrity Clash audio（#7 作者已預告 + 五人撞題）、浮水印重錄存活（AudioMarkBench/Özer/DeAR）——這五個方向都**不是空白**，請各位在 Round 3 更新自己的 novelty 定位。

**（回應我 Round 1 留給 F/H 的問題，順帶自答）** 我 Round 1 問 F/H「偵測器警示的誤報率到多少民眾會 alarm fatigue、H 是否接受以部署導向指標而非 EER 為主的碩論」。H 在他的 Round 1 提案一/二裡其實已經正面回答了我——他明確主張『任何提案如果只打算報 EER，我在 proposal defense 就會擋下來，必須報 fixed-operating-point 指標、calibration、多 base rate 下的 expected cost』。這等於官方背書了「部署導向指標」路線。史官補一個數據錨點給這個共識：Hiya《State of the Call 2026》顯示 1/4 美國人一年內接過 deepfake 語音電話（我 Round 1 的 S5），R6 顯示台灣 2026 年 1–4 月光是通報就 5 萬件、財損 215 億——base rate 在詐騙熱線上其實不低，這對 H 的 expected-cost 論證有利（base rate 越高，偵測器的部署價值越容易為正）。

---

## 3. 我支持的提案（含史官能如何補強）

### 支持一：H 提案二 + F 提案一 + A 提案二 這一整叢「不追軍備競賽、改做部署導向的人機協作 triage / 校準棄權」

這三個提案在技術上高度同構（selective prediction、calibration under shift、把不確定樣本 route 給人），我把它們視為同一個最有潛力的方向叢。**為什麼我作為史官支持它**：這是唯一**主動跳出我 Round 1 指出的「benchmark→救回 in-domain→新 benchmark 再打回原形」四輪循環**的方向。它不跟 ElevenLabs 比架構，而是接受「偵測器就是 13.5–50% EER」的歷史事實，把貢獻放在「不隨生成器版本過期」的評估框架與人機分工上——H 自己也點出這種貢獻「五年後還會被引用」。它也最直接回答問題陳述的硬要求「降低民眾受騙機率」。

**史官能補強的三點**：
1. **時間軸正當性**：EU AI Act Article 50 於 2026-08-02 生效、強制合成音訊 machine-readable 標記（我 Round 1 的 S8）。這意味著「訊號本該存在卻缺席」的鑑別力會**逐年上升**——H 提案一的「缺席=可操作的風險等級」論證，有一個正在逼近的政策時鐘撐腰。這個 deadline 讓 triage 系統「對無憑證音訊採取何種先驗」從空想變成 2026 下半年就要面對的現實。
2. **人機互補的產業佐證**：我 Round 1 查到的 Hiya 統計、Google Android 端上 fake-call detection（S5）都在做「給民眾提示」，但**沒有一個公開量測過提示對真實受騙率的因果效果**——F 提案一的 user study 正好填這個產業都沒做的洞，史官可以幫 F 把「產業已部署但未評估」這個 gap 論證寫得無可辯駁。
3. **排雷**：MLLM 判真假這條捷徑已被 VoiceWukong 證偽（Qwen2-Audio 英文 F1=0），所以 triage 的「機器層」只能用專用偵測器 + 校準，不能偷懶塞一個大模型當 judge——這一點史官幫他們先擋掉一個 reviewer 會問的問題。

### 支持二：C 提案二「真實傳輸鏈資料集 + 通道指紋一致性檢查」（與我 G-2 互補，我願意讓路或合流）

C 提案二和我 G-2 錨定同一個真實空白：**沒有人把音訊灌過真實電信/VoIP 通道量測**（#3 用的是離線 codec 模擬，RADAR 2026 也是模擬 transformation）。我支持它，因為 R5 已證明「重錄存活」被做過、但「真實通道存活」沒有；R6 證明台灣詐騙的主戰場（老闆語音、LINE 匯款指令）就在這些通道裡。**史官能補強**：C 的「通道宣稱 vs. 通道證據一致性」（「自稱銀行來電卻無電話 codec 痕跡」）其實是把 #7 的多訊號一致性思路從「密碼學層」下放到「物理通道層」——這是一個影像領域完全沒有的 audio 原生貢獻，史官可以幫他把這個「通道即一種可稽核訊號」的定位講清楚，讓它不只是資料集論文。若 H 只准一題、而 C 和我都想做真實通道，兩人應合流：C 出通道指紋與資料集，我出浮水印/偵測器/tracing 的三軸存活評測，共用一套錄製基礎設施。

---

## 4. 對我自己 Round 1 提案的辯護（史官為前作負責）

有人（尤其 H、E）可能質疑我的 G-1（Audio Integrity Clash）落在挑戰四點名的「五人撞題」裡。我承認並辯護：我 Round 1 已預先寫下這個風險，且我的差異化不在「形式化狀態空間」（#7 已做、五人都會做），而在「**良性通道自然去同步 vs. 惡意去同步的區分**」這個 audio 獨有、且 R5 證明尚無人系統做的問題。若這個窗口在一年內被填滿，我的退路是 G-2——而 G-2 錨定的「真實電信通道存活」經過本輪 R5 查證，確認仍是無人碰的空白，風險下界比 G-1 更穩。這也是我這一輪願意把資源往 C 提案二/G-2 合流傾斜的原因。

---

*本輪執行 6 次 WebSearch，全部附 URL。核心貢獻：把三個「看似新穎」的方向（挑戰-回應、同源連結、one-class）標記為「已有前作、部分已被攻破」，並指出五人撞題的收斂風險，同時確認「真實電信通道存活」仍是可辯護的空白。*
