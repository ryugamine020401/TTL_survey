# Round 2 質詢：紅隊（Agent D）
日期：2026-07-14

> 紅隊立場不變：舊生成器攻擊者早淘汰了，fake/eval 側該積極換新、讓敵情真實。但本輪最大的敵人不是「資料太舊」，而是**兩種自我欺騙**：(1) 把「新資料集」當免費午餐、每格都塞、把 4×3 grid 偷脹成 7×3；(2) 把「我方希望它可得」誤當成「它已可得」，讓某個方向的取得性風險在紙上被消掉。這兩者都會讓攻擊面評估**過度樂觀**。本輪我也毫不留情地駁回我自己 Round 1 的三個提議——紅隊對自己一樣開槍。

---

## 1. 抓出站不住的換資料集提議（駁回 6 項，遠超 3 項下限）

### 駁回 1｜「RTCFake 已確認公開可下載、D2 單點故障解除」——過度樂觀，事實上是 gated

**對方原文**：
- B round1：「RTCFake 已確認 HuggingFace `JunXueTech/RTCFake` **公開可下載**……D2 最大風險下降」（B D2-A）
- C round1：「landscape 已證實可下載，D2 最大單點故障事實層下降」（C D2）
- F round1：「事實層已解除風險」（F D2）
- A round1：「**事實上它可直接下載**，D2 最大風險就此下降」（A D2-B）
- **我自己 Round 1**：「事實上它可直接下載，D2 最大風險就此下降」——我一樣說錯了。

**反駁（理由 a：其實下不到/申請制）**：G 本輪**實際查證**了 HF 頁面，關鍵發現是——「RTCFake 的 HF 頁面對匿名抓取回 **HTTP 401**，而同一時間 CodecFake+ 回 200」（G 開場 + 考證紀錄）。401 是 **gated（需登入＋同意條款才下載）的強訊號**，repo 也未明標學術重散布授權。也就是說：**五個角色（含我）異口同聲的「已解除風險」，是建立在一個沒有人真的去點下載鍵的假設上。** 這正是紅隊最怕的「把希望當事實」。**判定**：撤回「風險解除」敘述，D2 的月 0 go/no-go **維持為真實閘門**，且內容從「能否取得」擴為「(a) 能否過 gate、(b) 授權是否允許學術重散布」兩問。這一條不改任何 RQ，只是把被抹掉的風險放回去——不放回去，D2 的可行性評估就是過度樂觀。

### 駁回 2｜「ASVspoof 5 取代 D1/D3 訓練種子（或種子池）」——需重訓＝改方法論＋接種污染

**對方原文**：
- B round1：「ASVspoof 5 train（抽 20k）列為可選對照」（B D1-B）；D3「in-domain 種子……可選升 ASVspoof 5」（B D3-C）
- C round1：「訓練種子（可選）2019 LA → ASVspoof 5 train 抽 20k」（C D1 表）
- **我自己 Round 1（D3）**：「種子池 `ASVspoof 2019/2021 → ASVspoof 5(2024, 抽 20k)`」——這是我 R1 最該被駁的一句。

**反駁（理由 c：需要改方法論＝換題目）**：A 講得最清楚——D1/D3 用的是 **frozen backbone + 現成 AASIST/RawNet2/SSL-AASIST checkpoint，這些權重全是 ASVspoof19 LA 訓練的；換訓練種子＝要重訓**（A D1）。重訓直接吃掉「日曆是唯一瓶頸」的定稿判定，這不是換資料、是換實驗設計。**疊加兩個紅隊專屬理由**：(1) ASVspoof 5 內建 adversarial（Malafide/Malacopula）與 neural codec 條件，拿它當種子＝**偵測器被預先接種**，RQ1 的 unseen gap 會人為縮小、RQ3 的 confident-real 攻擊成本人為升高——**攻擊面看起來被守住了，其實是敵人被提前餵過**（我 R1 通則第 3 點，這裡回頭打自己 D3 的種子池提議）；(2) G 查證 ASVspoof 5「**授權非乾淨 CC tag，須讀 LICENSE.txt**」，重散布條款不明。**判定**：ASVspoof 5 **不進 D1/D3 種子線**，連「可選對照臂」都不做（那是加實驗）；種子維持 ASVspoof 2019 LA。

### 駁回 3｜「D1 unseen 軸四件套全上」——4×3 grid 偷脹成 7–8 格

**對方原文**：
- B round1：D1 unseen 軸「DFADD＋CodecFake+＋SpeechFake 開源部＋MLAAD v10」四件套，外加 Deepfake-Eval-2024 eval 錨（B D1-A）
- F round1：「DFADD＋CodecFake+＋SpeechFake 開源部……另加 Deepfake-Eval-2024」（F D1）
- **我自己 Round 1（D1）**：「DFADD(2024) + CodecFake+(2025) + SpeechFake 開源部(2025) + Deepfake-Eval-2024」——四加一，我也犯規。

**反駁（理由：本輪明令禁止的範圍膨脹）**：H 已當場擋下——「4 個 source 格就變 7–8 格，**評估前向、RQ3 對抗搜尋、悲觀重跑全部翻倍**」（H D1）。定稿 grid 是 **4 source × 3 channel = 12 格**，替換後**仍須是 4×3**。unseen 軸只有兩格可換（原 2021 DF、原 MLAAD v5），能換上去的新集**最多兩個**，不是四個。**判定**：D1 unseen 兩格＝DFADD（換 2021 DF）＋（MLAAD v10 **或** SpeechFake 開源部，二選一，換 MLAAD v5）。CodecFake+、Deepfake-Eval-2024 一律不進 D1 grid（理由見駁回 4、5）。

### 駁回 4｜「Deepfake-Eval-2024 加成 D1 第 5 個 eval 格」——加格＋散布受限

**對方原文**：F round1「加 Deepfake-Eval-2024（2025, eval-only）當真實流通錨」（F D1-2）；B round1 列為 eval 錨；我 R1 亦列入。

**反駁（理由 a＋範圍膨脹）**：G「Deepfake-Eval-2024……會**多加一個 source 格 = 12 格→15 格**，屬擴充；只在 discussion 以文字提」（G D1）。且它是社群 scrape，**再散布授權受限（🟡）**，連當可散布資料集都勉強。**判定**：Deepfake-Eval-2024 **不進任何 grid**，只在 discussion 以一句話標明「本 benchmark 未涵蓋 2024 真實流通與閉源商用世代」。要它進 grid 就得**替換**掉某一格、絕不新增——而四格沒有一格值得被它換掉（它無生成器標記，破壞分層抽樣的可控性）。

### 駁回 5｜「CodecFake+ 當 D1 的 unseen-generator 格」——codec×codec 與 C_neural 通道軸共線，讀不出負領土

**對方原文**：
- G round1：D1「ASVspoof 2021 DF eval → **CodecFake+（2025）**」（G D1）
- C round1：「CodecFake+ 與 D1 的 `C_neural` 通道軸同構……channel-shift 與 generator-shift 兩軸在此交會，**是我最想看的一格**」（C D1 表）
- A/B/F/我 R1 亦把 CodecFake+ 放進 D1 unseen 池。

**反駁（理由 d：換上去讓評估變不真實）**：C 把「兩軸交會」當賣點，紅隊看到的是**混淆（confound）**。D1 的科學價值在能把失效**歸因**到「generator-shift」還是「channel-shift」——這是逐格可控的 4×3 grid。**但 CodecFake+ 的 fake 本身就是 neural-codec 產物**；把它放進 generator 軸，再過 `C_neural`（EnCodec transcode）通道副本，那一格就是 **codec-on-codec**，generator 軸與 channel 軸在該格**物理共線**，偵測器在該格失效你**無法判定是「沒見過的生成器」還是「neural codec 通道」造成的**。負領土地圖在該格失去可讀性。DFADD（diffusion/FM，**非** codec-based）才是乾淨的 unseen-generator 格。**判定**：CodecFake+ **不當 D1 generator 格**；它的正確歸宿是 D3（那裡 codec 本來就是主題）。D1 若想要 neural-codec 世代的存在感，讓它待在 channel 軸 `C_neural` 的**通道實作**即可，別汙染 generator 軸。

### 駁回 6｜「D3 unseen 軸在 CodecFake++DFADD 之上再加 SpeechFake 開源部」——為換而換的搜尋池灌水

**對方原文**：A round1「unseen 軸 → DFADD + SpeechFake 開源部」（A D3）；B/C/F round1 D3 均把 SpeechFake 疊進 laundering/unseen 池。

**反駁（理由 e：為換而換）**：G 已明確不採——「SpeechFake 開源部雖可補廣度，但 **CodecFake+ + DFADD 已足以覆蓋 neural-codec + diffusion/FM 兩個 2025 關鍵範式；再加屬擴充搜尋池，違反『不因換資料順便擴充』**」（G D3）。D3 的承重是 greedy 搜尋的攻擊成本上界，laundering 對象每多一個生成器家族，就是多一輪 greedy 搜尋×確認前向。CodecFake+（同構 RQ2）＋DFADD（補 diffusion/FM）已把 2025 兩大範式蓋住，SpeechFake 的邊際只是廣度虛胖。**判定**：D3 laundering 對象＝CodecFake+＋DFADD 兩件，SpeechFake 不進 D3。

---

## 2. 抓出偷渡的範圍擴充（本輪最需防的）

逐一點名，全部壓回「替換不新增」：

| # | 偷渡點 | 誰提的 | 性質 | 處置 |
|---|---|---|---|---|
| ① | D1 unseen 軸四件套全上（→7–8 格） | B、F、**我自己 R1** | 加 3–4 批評估前向＋RQ3 對抗搜尋翻倍 | 只換 2 格（DFADD＋MLAADv10/SpeechFake 二選一） |
| ② | Deepfake-Eval-2024 當 D1 第 5 eval 格 | B、F、**我自己 R1** | 加一格＋scrape 散布受限 | 逐出 grid，僅 discussion 一句話 |
| ③ | D3 疊加 SpeechFake（CodecFake++DFADD 之外） | A、B、C、F | 搜尋池灌水 | 不進 D3 |
| ④ | **ASVspoof 5 的 adversarial 子集**被「順便測一下」 | 風險源（無人明推，H 釘死） | **會復活定稿已一刀砍掉的白盒 PGD 軸** | 沿用 H 釘死：採 ASVspoof5 也只准乾淨 TTS/VC＋codec 條件，adversarial 子集一格不碰。**我 R1 已自守此界，這裡與 H 合力焊死** |
| ⑤ | ADD-C（2025）升為 D2「模擬側對照基準」新軸 | C 列 🟡 備選、H 擋下 | 新增一條資料處理線＋一組評估格 | 至多 discussion 引用，不進實驗 |
| ⑥ | SpoofCeleb 升為 D2 real 主臂 | 眾人列備選 | 新增 real 臂＋VoxCeleb 非商用授權再散布受限 | 維持公開 real，SpoofCeleb 不採 |
| ⑦ | SpeechFake ZH / CFAD 由 D4 對照臂升格為 zh-CN 主軸 | 眾人列對照、H 釘死 | 偷換方向主體語言與尺度 | 維持對照臂，外部效度限制明標 |

**紅隊補一句對 C 的 D4-EVS 提議的裁定**：C 主張「D4 傳統 codec 移除 EVS」（C D4）。這**動的是通道設計、不只是 fake**，嚴格說已越過「只換餵進去的資料」的界線。但——它是**移除一個條件（縮範圍）＋ CPU 減法**，且與 D2/D3/D5 既有的 EVS 排除**一致化**，方向是收斂不是膨脹。**紅隊裁定：可接受，但必須在論文裡框成「與其他方向的通道集一致化」，不得包裝成「新增台灣通道真實性論證」的方法貢獻**——否則就是藉縮範圍偷加賣點。

---

## 3. 題目正式化複審（指出仍不夠正式/不準確者，給修正）

### D1
- **不夠正式處**：A 的英文 *…Selective-Prediction Reliability… under Distribution Shift* 與 B 的 *Shift-Aware… under… Distribution Shift* 都**「shift」出現兩次**（Shift-Aware ＋ under…Shift），A 自己也承認重複。H 的中英最乾淨但**丟失了「shift 來自哪裡」的資訊**。
- **紅隊修正（採 H 中文骨架＋G 英文精確度）**：
  - 中：《分布偏移下語音深偽偵測的選擇性預測基準》（H 版，乾淨、名詞收尾）
  - 英：*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Unseen Generators and Channels*（取 G 的「under Unseen Generators and Channels」replace 掉重複的「Distribution Shift」，一次講清 shift 的兩個來源且無冗字）

### D3
- **不準確處**：A、B 的**中文標題把「adaptive-laundering」留英文**——中文學位論文標題夾生英文術語不合慣例，須譯。三個譯法各有毛病：我 R1 的「洗**白**」太口語（whitewash 聯想）、H 的「洗**訊**」是生造詞、G 的「適應性洗**刷**」最接近技術義（audio laundering＝洗刷去識別）。另 A 的「**針對**…之」贅字。
- **紅隊修正**：
  - 中：《被動語音深偽偵測之適應性洗刷（adaptive laundering）攻擊成本上界評估》（採 G 的「適應性洗刷」，首次出現括號附英文；去 A 的「針對」）
  - 英：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
  - **「地圖(Map)」vs「評估(Assessment)」裁定**：Map 較生動但略帶隱喻，學位論文正式度上 **Assessment 較穩**；若口委接受「上界地圖」為指名交付物，Map 亦可保留。紅隊本命方向，我傾向 Assessment。

### D2
- **不夠正式處**：C 的《離線模擬與真實通訊通道之落差：…量測與畸變層歸因》**主標仍是敘事式「之落差」框架且過長**（兩子句＋冒號）；C 英文 *The Gap Between…* 偏敘事。F 的「存活**率**」比 H 的「存活」更精確。
- **紅隊修正（採 H 結構＋F 的「存活率」）**：
  - 中：《真實通道上音訊深偽反制訊號存活率的樂觀偏差及其畸變層歸因》
  - 英：*Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*（H 版，最乾淨）

### D4
- **不夠正式處**：F 的《…審計**——**以繁體中文語料為例》**仍用破折號**，直接違反本輪「去破折號」原則。H 的最乾淨但**把 D4 的核心貢獻「繁體中文」從標題拿掉了**——民眾 F 與 B 都主張繁中定位該在標題現身，紅隊同意（那是 D4 的實質地域貢獻）。另「Scam-**Scene**」(H) 不如「Scam-**Scenario**」(B/F) 自然。
- **紅隊修正（H 主標＋冒號接繁中副標，不用破折號）**：
  - 中：《詐騙情境條件下語音深偽偵測的評估效度審計：繁體中文語料研究》
  - 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*

### D5
- **不夠正式處**：C 的「歐盟 **AI 法**」是非正式簡稱。H 的全名「歐盟人工智慧法」正式。兩者結構皆合格。
- **紅隊修正**：直接採 H 版（無需改）：
  - 中：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》
  - 英：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

> 紅隊總則：fake/eval 側換到 2025 世代（敵情真實），訓練種子/載體/watermark 側保守（保留 shift 誠實、避免預先接種）。取得性一律以 **G 的實測授權**為準（CodecFake+ MIT 非 gate、DFADD MIT 用 2025-04 修正版、SpeechFake 開源部 Apache 2.0、RTCFake gated、ASVspoof5 授權須讀 LICENSE.txt）。

- **D1**：unseen 兩格＝**2021 DF → DFADD(2024, diffusion/FM, 用修正版)**；**MLAAD v5 → MLAAD v10(2025)**（drop-in 最省事；若要更廣可改 SpeechFake 開源部，**二選一**）。**grid 維持 4×3**。**CodecFake+ 不當 generator 格**（codec×C_neural 共線）；**Deepfake-Eval-2024 不進 grid**（僅 discussion）。**訓練種子 ASVspoof 2019 LA 維持、In-the-Wild 維持**（frozen checkpoint＋smoke-test，換了要重訓＝違規）。

- **D2**：**fake XTTS/VITS/YourTTS → 2025 世代開源 fake，維持 3 家等量替換**（優先 SpeechFake 開源部＋一個 diffusion/FM；CodecFake+ 可用但須註明 codec×通道對被動探針的共線）。**RTCFake 維持為錨，但撤回「風險解除」——月 0 go/no-go 維持真實閘門（過 gate＋重散布條款雙確認）**。**AudioSeal、real 類、模擬臂 Opus/AMR-WB 維持**；ADD-C/SpoofCeleb 不進實驗。

- **D3（本命）**：**laundering 對象 2021 DF + MLAAD → CodecFake+(2025, MIT, 同構 RQ2) + DFADD(2024, 修正版)**，**不加 SpeechFake**（灌水）。**種子 ASVspoof 2019 LA 維持**（不換 ASVspoof5：重訓＋接種＋授權不明）。**laundering 動作空間維持**。**釘死：不碰 ASVspoof5 adversarial 子集**（會復活被砍的白盒軸）。攻擊面誠實化紅利：換 2025 fake 後 greedy 會找到更短更便宜的打穿配方——攻擊成本上界**該下降**，這是真相不是壞消息。

- **D4**：**fake 2 家 2022–2023 → 2 家 2025 世代 zh 開源情緒 TTS**（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 中選 2，**維持 2 家不加家數**）。**自建 zh-TW 定位維持**（無現成 zh-TW 集）。**SpeechFake ZH / CFAD 僅 zh-CN 對照臂**，外部效度限制明標，不升格。**月 0–1 情緒 zh-TW TTS 硬 go/no-go 維持**。C 的移除 EVS：接受，但須框成通道集一致化、非新方法貢獻。**紅隊強調：D4 是唯一「不換才會過度樂觀」的方向**——用 2023 爛哭腔 TTS 當 fake，RQ3 品質配對後的淨落差會被系統性低估，讓人誤以為偵測器對現場還行；換 2025 高品質情緒 TTS，落差才真的來自現場條件而非生成品質。

- **D5**：**維持載體語音 / watermark 家族(AudioSeal/WavMark/SilentCipher) / 通道矩陣**——這是誠實的「換了沒意義」。**唯一更新：baseline 補「Will They Survive Neural Codecs?」(Interspeech 2025)**。**CodecFake+ 僅作 neural codec 世代參照，不進主 pipeline、不當載體軸/watermark 軸**。紅隊註記維持：D5 量的是「被動通道劣化下的 bit 容量下限」，不是「攻擊者主動剝除/覆寫 watermark 下的容量」，後者只會更低——這句要在 discussion 標明，防止讀者把被動容量誤讀成對抗容量而過度樂觀。

---

## 回傳（純文字資料）

### 我駁回的提議（每項 ≤30 字）
1. RTCFake「已解除風險/可下載」：G 實測 401，實為 gated，維持 go/no-go。
2. ASVspoof 5 換 D1/D3 種子：要重訓＝改方法，且接種污染攻擊面。
3. D1 unseen 四件套全上：4×3 grid 偷脹成 7–8 格，只准換 2 格。
4. Deepfake-Eval-2024 加成 D1 第 5 格：加格＋scrape 散布受限，逐出 grid。
5. CodecFake+ 當 D1 generator 格：codec×C_neural 共線，負領土讀不出。
6. D3 疊加 SpeechFake：CodecFake++DFADD 已覆蓋，屬搜尋池灌水。
（另釘死：ASVspoof5 adversarial 子集不得「順便測」，會復活被砍白盒軸。）
（自我開槍：上述 1、2、3、4 我 Round 1 都犯過，此輪一併撤回。）

### 五方向最終背書換法
- **D1**：2021 DF→DFADD(2024 修正版)；MLAAD v5→MLAAD v10(2025)（或 SpeechFake 二選一）；grid 維持 4×3；CodecFake+/Deepfake-Eval 不進 grid；ASVspoof19 種子＋In-the-Wild 維持。
- **D2**：fake XTTS/VITS/YourTTS→2025 開源 3 家（等量）；RTCFake 維持但 go/no-go 不解除（gated）；AudioSeal/real/模擬臂維持；ADD-C/SpoofCeleb 不進實驗。
- **D3**：laundering 對象 2021 DF+MLAAD→CodecFake+(2025)＋DFADD(2024)；不加 SpeechFake；種子 ASVspoof19 維持（不換 5）；adversarial 子集釘死不碰。
- **D4**：fake 2 家→2025 世代 zh 開源情緒 TTS（維持 2 家）；自建 zh-TW 維持；SpeechFake ZH/CFAD 僅 zh-CN 對照臂；月 0 go/no-go 維持。
- **D5**：載體/watermark 家族/通道矩陣全維持；只補 baseline「Will They Survive Neural Codecs?」(Interspeech 2025)；CodecFake+ 僅參照。

### 紅隊一句總結
本輪真正的攻擊面風險不在「fake 太舊」，而在**兩個過度樂觀陷阱**：把 gated 的 RTCFake 當已解除（D2）、把當代 adversarial/neural-codec 條件餵進訓練或塞滿 grid（D1/D3）——前者讓可行性評估失真，後者讓偵測器被預先接種、攻擊面看起來被守住了。fake/eval 換新要積極，種子/grid 結構要焊死。
