# Round 2 質詢：Detection 研究者（Agent A）
日期：2026-07-14

> 質詢範圍自綁：只質詢「資料集替換」與「題目正式化」兩件事。方法論、RQ、算力我只在「某個換資料集提議會逼著改它們」時才引用，作為反駁武器，不另開戰場。
> 我的角色底線：unseen 要真的 unseen（生成範式錯位，不是版本號錯位），而且不能為了讓 unseen 更漂亮就把 grid 撐大或把種子接種——那兩件事一個違規、一個自欺。

---

## 1. 抓出站不住的換資料集提議（至少 3 個）

### 1.1 「RTCFake 已確認公開可下載、D2 風險解除」——授權/取得層面站不住（B、C、D、F、landscape 全體）

**引用對方原文：**
- B（round1，D2-A）：「RTCFake（2026，ACL 2026）已確認 **HuggingFace `JunXueTech/RTCFake` 公開可下載** …… D2 最大風險下降。」
- C（D2 表）：「RTCFake（2026, ~600h, HuggingFace `JunXueTech/RTCFake` **已確認公開可下載**）：解除風險，非換新」
- D（D2-B）：「**事實上它可直接下載，D2 最大風險就此下降**。」
- F（D2）：「RTCFake：維持，但從『單點故障』改標為『**已確認 HuggingFace 公開可下載**』。」

**反駁（理由 a：其實下不到/申請制）：**
G（史官）本輪唯一一個真的去打了 HTTP 的人，考證紀錄寫得很清楚：**RTCFake 的 HF 頁面對匿名抓取回 HTTP 401，而同一時間 CodecFake+ 回 200**——這是「被 gate（需登入＋同意條款才下載）」的強訊號，不是「公開直接下載」。B/C/D/F 四個人（連同 landscape §四）異口同聲說「已確認公開可下載」，但沒有一個人給出「匿名／未登入狀態實際抓到檔案」的證據，全是把「HF 上有這個 repo 頁面」誤讀成「可直接下載」。這兩件事在 HF 上差很多：gated dataset 的頁面照樣公開可見，檔案卻要登入＋按同意才給。

**判定：** 這不是換資料集提議，是「解除風險」的敘事，而且**解除得太早**。RTCFake 仍是 D2 的錨（無替代品，這點我同意），但定稿把它當「月 0 go/no-go 單點故障」是**對的**，Round 1 集體想把它降級為「已解除」是**錯的**。恢復月 0 硬閘，且閘的內容要擴成兩問：(a) 能不能過 gate、(b) 過了 gate 後授權允不允許學術重散布（repo 未明標）。在這兩問答覆為 yes 之前，D2 的最大風險沒有下降。

---

### 1.2 「D1 unseen 軸換上 DFADD + CodecFake+ + SpeechFake（＋Deepfake-Eval-2024）四件套」——超算力/超結構，是偽裝成替換的擴充（B、C、F、D）

**引用對方原文：**
- B（D1-A）：「ASVspoof 2021 DF + MLAAD v5 → 換上 2024–2025 世代**四件套**」（DFADD＋CodecFake+＋SpeechFake＋MLAAD v10，另加 Deepfake-Eval-2024 eval 錨）。
- C（D1 表）：unseen 軸「→ **DFADD＋CodecFake+＋SpeechFake 開源部**」。
- F（D1）：「三者合成一個『2024–2025 生成範式』的抽樣池」＋加 Deepfake-Eval-2024。
- D（D1-A）：「DFADD＋CodecFake+＋SpeechFake 開源部＋…Deepfake-Eval-2024」。

**反駁（理由 b：超算力預算 / 理由 c：等於動結構）：**
D1 定稿是 **4 source × 3 channel = 12 格**的固定 grid（G 與 H 都明確引了這個結構）。原本 unseen 相關只佔 source 軸的 2 格（2021 DF、MLAAD v5）。把 2 格換成「DFADD＋CodecFake+＋SpeechFake」三個獨立來源，等於 source 軸從 4 格膨脹到 5–6 格，channel 一乘就是 15–18 格——**每一格都是一批前向、一批 risk–coverage 曲線、RQ3 一批 confident-real 攻擊搜尋、悲觀重跑全部翻倍**。H 已經把這件事點名為「換資料集偽裝的範圍膨脹」，我完全同意並補一句 detection 專業判斷：**多塞一個 codec-based 來源到 D1 unseen 軸，邊際資訊近乎零**——DFADD（diffusion/FM）已經補了 2019/2021 沒有的一個生成範式，SpeechFake 開源部（30 工具）已經是廣度一站式，CodecFake+ 的 codec 世代對「generator-shift 廣度地圖」不再多給一個**新範式**，只多給一批要跑的樣本。

**判定：** D1 只換 2 格（見 §4），維持 4×3=12。想上 CodecFake+ 的請去 D3/D5（那裡才與 neural codec 承重論證同構）。Deepfake-Eval-2024 若要用，**必須替換掉某一格、不得新增第 5 格**，且它 🟡（scrape 再散布受限）只能 eval-only、不承重——這點我 Round 1 已自訂，B/F 想把它升成常設錨的，擋下。

---

### 1.3 「ASVspoof 5 當 D1/D3 的 in-domain 訓練種子」——需要重訓＝改設計，且會預先接種＝自欺（C 積極、B/F/D3 列可選）

**引用對方原文：**
- C（D1 表）：訓練種子「2019 LA → **ASVspoof 5 train 抽 20k（2024, crowdsourced 非棚錄、內建 codec 條件）**……訓練種子的通道多樣性升級」——C 是唯一把它寫進正表、給了肯定理由的人。
- B（D1-B）：「可選升 ASVspoof 5 train（2024）」。
- F（D1-3）：「（可選）in-domain 訓練種子：ASVspoof 2019 LA → ASVspoof 5 train」。

**反駁（理由 c：需要改方法論；理由 d：換上去反而不更貼近真實攻擊面）：**
兩重問題，任一個就足以否決當「主線種子」：

1. **改方法論（違規）**：D1/D3 的偵測器是 **frozen backbone + 現成 AASIST/RawNet2/SSL-AASIST checkpoint，這些權重全是 ASVspoof19 LA 訓練的**。換 in-domain 種子＝要重訓 SSL 前端＝動到「日曆是 D1 唯一瓶頸」的定稿判定，也帶進 SSL 復現風險。這不是「換餵進管線的資料」，是換管線本身，屬本輪明令禁止的「改方法＝換題目」。

2. **接種＝攻擊面自欺（我的 detection 專業紅旗）**：ASVspoof 5 首次內建 **adversarial 攻擊（Malafide/Malacopula）＋ neural codec 條件**。拿它當訓練種子，偵測器等於被**預先接種**了對抗樣本與 codec 免疫力——RQ1 量到的 unseen gap 會人為縮小、RQ3 的 confident-real 攻擊成本會人為升高。D（紅隊）把這講得最狠：「把當代 adversarial/neural-codec 條件餵進訓練，讓偵測器被預先接種、攻擊面看起來被守住了」是**全案唯一的過度樂觀陷阱**。C 想升級種子通道多樣性的直覺不壞，但它換來的是「假的、被接種過的 unseen gap」——這恰恰摧毀 D1 存在的理由。

**判定：** in-domain 種子維持 ASVspoof19 LA。ASVspoof 5 train **不進主線**，連「可選對照臂」都要小心（那已是加實驗）。G 另補一刀我採納：ASVspoof 5 授權是 LICENSE.txt 非乾淨 CC tag、且 info@asvspoof.org 那條是「用它 protocol 生成新 spoof」用，不是下載授權——當種子的取得性也不是全綠。

---

### 1.4（追加）「CodecFake+ 放進 D1 generator-shift 格、再過 C_neural 通道」——會把兩條 shift 軸混淆（C、G）

**引用對方原文：**
- C（D1 表）：「**CodecFake+ 與 D1 的 `C_neural` 通道軸同構**——『neural codec 世代的 fake』正好落在『neural codec 通道』上，channel-shift 與 generator-shift 兩軸在此交會，是我最想看的一格」。
- G（D1）：「ASVspoof 2021 DF eval → **CodecFake+（2025, MIT）**」。

**反駁（理由 c 的軟性版：不改方法論，但會污染該格的科學解讀）：**
C 把「codec 世代 fake × codec 通道交會」當成賣點，但從選擇性預測基準的角度這是**bug 不是 feature**：D1 的整個貢獻是把 shift **分解**成可讀的 source 軸與 channel 軸。把「本身就是 neural codec 產物的 fake」放進 generator 軸、再過 `C_neural`（EnCodec transcode），這一格量到的棄權失效**分不清是 generator-shift 還是 channel-shift 造成的**——兩個自變數在同一格疊在一起。這不需要改方法論，但會讓那一格的 risk–coverage 讀數在論文裡無法乾淨歸因，違背 D1「shift 網格逐格可讀」的初衷。

**判定：** D1 的 generator-shift 格用 **DFADD / SpeechFake 開源部**（非 codec 骨幹的生成範式）較乾淨；CodecFake+ 留給 D3（laundering×codec 同構）與 D5（通道世代參照）。C 想看的「codec×codec 交會」不是不能看，但那是另一篇的 RQ，本輪不開。

---

### 1.5（追加）「D2 補 ADD-C 模擬臂 / SpoofCeleb real 臂」與「D4 移除 EVS 通道」——為換而換 & 動到實驗設計（C、B、G）

**引用對方原文：**
- C（D2 表）：「模擬臂……ADD-C（2025）僅列 🟡 備選外部對照」；C（D4 表）：「**建議自傳統 codec 集移除 EVS**」。
- B（D2-C）／G（D2）：SpoofCeleb（2024）作 real 臂備選。

**反駁：**
- **ADD-C / SpoofCeleb（理由 e：舊的/自建才是正解）**：D2 的模擬臂是 Opus/AMR-WB **自建受控階梯**，real 類是公開 real——這兩者是 D2 能逐因子拆解 γ 的前提。ADD-C 的固定 6 codec×5 PLR 條件**無法逐因子拆**，SpoofCeleb 受 VoxCeleb 非商用衍生授權（🟡 再散布受限）。它們都不比自建的更貼近「可控量測」需求，屬「為換而換」。C 自己也把 ADD-C 標成不可升軸、H 也擋了，但既然它出現在正文表格裡，我就把它明確判為**連備選都不必列**——列了就是給後人一個偷加軸的把手。
- **D4 移除 EVS（理由：這根本不是換資料集，是改實驗設計，越界）**：C 主張把 EVS 從 D4 傳統 codec 集移除，理由是台灣通道以 AMR/Opus 為主＋EVS CPU 慢。**理由本身在訊號上可能對，但這超出本輪範圍**——EVS 是**通道條件（實驗設計的一格）不是資料集**，`00-constraints.md` 白紙黑字「實驗設計全部維持定稿不動」。移除一個通道條件（即使是縮範圍）也是動實驗設計，該進另一場「實驗設計精修」會議，不該搭「換資料集」的便車偷渡。**判定：本輪不採 C 的 EVS 移除**；要不要拿掉 EVS 留給定稿實驗設計的主人決定。

---

## 2. 抓出偷渡的範圍擴充（本輪最需要防的）

逐一點名（只列「藉換資料集偷加東西」的，不重複 §1 已判的取得性問題）：

| # | 誰 | 偷渡了什麼 | 為何算擴充 |
|---|---|---|---|
| 1 | **B、C、F、D** | D1 unseen 軸一次上 3–4 個新集（DFADD＋CodecFake+＋SpeechFake＋MLAAD v10／＋Deepfake-Eval-2024） | 4×3 grid → 5–6 source 格，前向/搜尋/重跑翻倍（§1.2） |
| 2 | **B、C、D、F** | D3 unseen 軸同時上 CodecFake+ **＋** DFADD **＋** SpeechFake 開源部 三個 | G 已指出 CodecFake+＋DFADD 已覆蓋 codec + diffusion/FM 兩範式，再加 SpeechFake＝擴大搜尋池，違反「不因換資料順便擴充」。我採 G：D3 unseen 軸只需 DFADD 一個新範式格，laundering 主對象用 CodecFake+，**不再加 SpeechFake** |
| 3 | **B、C（＋H 亦點名此陷阱）** | D2 fake 從「等量替換 3 家」被寫成「補 CodecFake+ **＋** SpeechFake」＝往池子裡加來源 | H 明令「fake 只能等量替換 3 家，不得因新世代多就擴成 5 家」。CodecFake+ 與 SpeechFake 二選一等量換入，不是兩個都塞 |
| 4 | **C** | D2 的 ADD-C 進正文表、D4 的 EVS 移除 | §1.5：一個是為換而換的外部對照把手，一個是動實驗設計 |
| 5 | **潛在（H 預防、無人實做但要釘死）** | D3 若用 ASVspoof 5，順手測其 adversarial（Malafide/Malacopula）子集 | D3 定稿已一刀砍白盒 PGD；ASVspoof 5 內建 adversarial 是「順便復活被砍軸」的最大誘惑。我背書 H：**若碰 ASVspoof 5 只取乾淨 TTS/VC + codec 條件，adversarial 子集嚴禁進 laundering 評估**——但我更進一步，主張 D3 **連 ASVspoof 5 都不必動**（見 §4），直接消滅這個誘惑 |
| 6 | **F、B** | D1 Deepfake-Eval-2024 從「eval-only 可選錨」被講成常設真實流通錨 | 它是第 5 格＝加格；且 🟡 scrape 再散布受限。維持「要用就替換某格、eval-only、不承重」 |

**一句總評**：本輪偷渡幾乎全部集中在 unseen 軸「新集很多、忍不住全上」。防守法則就一條——**新集是填掉舊格還是多開一格？** 多開就擋。

---

## 3. 題目正式化複審

### D1
- **仍不夠好之處**：A（我自己）英文 *A Shift-Aware … under Distribution Shift* 有 shift 重複（我自訂時已標）；G 中文《面向未見生成器與通道之語音深偽偵測選擇性預測可靠性基準研究》名詞疊床架屋（「面向…之…偵測…選擇性預測可靠性基準研究」一連七個修飾），偏長；H 英文 *…for Audio Deepfake Detection* 乾淨但把 shift 從英文標題整個拿掉，**丟了本方向的核心限定**（沒 shift 就不是這篇）。
- **我的修正（中取 H 的乾淨、英取 B 的 shift 明確化）**：
  - 中：《分布偏移下語音深偽偵測的選擇性預測基準》
  - 英：*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Shift*
  - （B 原英文 "…Distribution Shift" 尾綴可省一個字，用 "Generator and Channel Shift" 既點明兩條 shift 軸又不與 Shift-Aware 打架。）

### D3
- **仍不夠好之處**：三個問題。(1)「adaptive laundering」中譯全場沒共識——D「適應性洗白」、G「適應性洗刷」、H「調適式洗訊」三種譯法並存，**譯名不定本身就是不夠正式的訊號**；(2)「地圖／Map」是隱喻，對學位論文標題偏花俏，A 與 G 已改用「評估／Assessment」是對的方向；(3) B 把 "adaptive-laundering" 用連字號夾在中文標題裡，格式不統一。
- **我的修正**：
  - 中：《被動語音深偽偵測之 adaptive laundering 攻擊成本上界評估》（譯名未定前保留英文，比選錯一個中譯安全；「評估」取代隱喻的「地圖」）
  - 英：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
  - （若指導教授堅持保留「地圖／Map」作為 deliverable 意象，可接受 H 的《…攻擊成本上界地圖》，但我對正式度的首選是「評估」。）

### D2
- **仍不夠好之處**：C 中文《離線模擬與真實通訊通道之落差：**……**》主標「之落差」讀起來仍像描述句、非名詞收尾；F 保留了「存活**率**」與「審計」但整串偏長。
- **我的修正**：直接背書 **H 版**（最乾淨、名詞收尾、承重詞「樂觀偏差—畸變層歸因」都在）：
  - 中：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》
  - 英：*Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*

### D4
- **仍不夠好之處**：**F 的《…評估效度之審計——以繁體中文語料為例》仍留著破折號「——」**，直接違反本輪「去破折號金句」的正式化原則（破折號 hook 是明令要拿掉的）。
- **我的修正（H 乾淨主標 + D 的繁中副標，破折號改冒號）**：
  - 中：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》
  - 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scene Conditions: A Traditional Chinese Corpus Study*
  - （繁中是 D4 的實質貢獻與地域定位，應留在標題；用冒號從屬，不用破折號。）

### D5
- **仍不夠好之處**：無實質問題。C 與 H 版都正式；H 的「及其……第 50 條……判定」從屬結構最貼定稿收斂的主從關係。
- **我的修正**：背書 **H 版**：
  - 中：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》
  - 英：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

> 原則：只換餵進管線的 fake/laundering 對象世代；grid/動作空間/搜尋協定/20k 抽樣一律不動；種子與載體保守維持；RTCFake 恢復月 0 硬閘。

**D1（4×3=12 grid 不動，只換 2 個 source 格）**
- 格 2 unseen-generator：ASVspoof 2021 DF（2021）→ **DFADD（2024, diffusion/FM；MIT，非 gate，用 2025-04 errata 修正版）**
- 格 4 unseen 廣度：MLAAD v5（2023）→ **SpeechFake 開源部（2025, Apache 2.0，抽 20k）**；零風險退路 = **MLAAD v10（2025, drop-in）**
- in-domain 種子 ASVspoof19 LA、In-the-Wild real 類：**維持**
- **不採**：CodecFake+ 進 D1（generator×channel 混淆）、ASVspoof 5 當種子（重訓＋接種）、Deepfake-Eval-2024 當常設第 5 格（僅 eval-only 可選、替換不新增）

**D2（錨維持、fake 等量換、恢復硬閘）**
- 真實通道錨 **RTCFake：維持為唯一錨，但恢復月 0 go/no-go 硬閘**（G 查得 HF 401 gated；閘要問「能過 gate 嗎＋允許學術重散布嗎」，答 yes 前風險未解除）
- fake：XTTS-v2/VITS/YourTTS（2022–2023）→ **等量替換為 3 家 2025 世代開源系統**（F5-TTS / CosyVoice 2 / 一個 codec-based 生成器；或自 SpeechFake 開源部抽樣），**維持 3 家、不擴成 5 家**
- real 類、AudioSeal、Opus/AMR-WB 模擬臂：**維持**
- **不採**：SpoofCeleb（VoxCeleb 授權🟡）、ADD-C（無法逐因子拆、為換而換）當實驗軸

**D3（最強一刀，但只換 laundering 對象 + 一個 unseen 範式格）**
- laundering 主對象／確認池：ASVspoof 2021 DF（2021）→ **CodecFake+（2025, MIT, 101 GB, 非 gate；抽 20k 確認 / 10k 搜尋）**——與 RQ2「neural codec 不可逆必殺」直接同構
- unseen 軸：MLAAD（2023）→ **DFADD（2024，抽樣）** 一格新範式即可
- in-domain 種子 ASVspoof19 LA、laundering 動作空間、greedy 搜尋協定：**維持**
- **不採**：D3 unseen 軸再加 SpeechFake（G：CodecFake+＋DFADD 已覆蓋兩範式，再加＝擴搜尋池）；ASVspoof 5 當種子（若不得已用，僅乾淨 TTS/VC+codec，**adversarial 子集嚴禁進 laundering 評估**——但我主張根本不必動種子）

**D4（自建定位不變，只升 fake 世代，維持 2 家）**
- fake：2 家開源情緒 TTS/VC（2022–2023）→ **2 家 2025 世代 zh 開源情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 中選 2 家）**，維持 2 家、月 0–1 情緒 zh-TW TTS 硬 go/no-go 照走
- 自建 zh-TW 定位、話術腳本、real 載體、通道、UTMOS+ECAPA：**維持**
- CFAD / SpeechFake ZH：**僅 zh-CN 對照臂、備選、標外部效度限制，嚴禁升為主軸**
- **不採**：C 的移除 EVS（那是改實驗設計、越界，本輪不動通道條件）

**D5（誠實維持，只補前作錨）**
- 載體語音（AISHELL-3/LibriSpeech/real）、watermark 家族（AudioSeal/WavMark/SilentCipher）、通道矩陣（傳統 codec + EnCodec/DAC/SpeechTokenizer）：**全維持**（載體年份不影響 bit 容量、watermark 已是開源全集）
- baseline：AudioMarkBench（2024）→ **補「Will They Survive Neural Codecs?」（Interspeech 2025）為直接前作**
- CodecFake+：**至多作 neural codec 世代參照，不進 pipeline、不擴通道矩陣**

---

## 回傳（純文字資料）

### 我駁回了哪些提議（每項 ≤30 字）
1. 「RTCFake 已確認公開可下載、風險解除」——G 查得 HF 401 gated，恢復月 0 硬閘。
2. D1 unseen 軸塞 3–4 個新集——grid 4×3 撐爆，只准換 2 格。
3. ASVspoof 5 當 in-domain 種子——要重訓＝改設計，且接種對抗/codec＝攻擊面自欺。
4. CodecFake+ 放 D1 generator 格再過 C_neural——generator/channel 兩軸混淆，留給 D3/D5。
5. D3 unseen 軸 CodecFake+＋DFADD＋SpeechFake 三個全上——兩範式已足，砍 SpeechFake。
6. D2 fake「補 CodecFake+＋SpeechFake」兩個都塞——只准等量換 3 家。
7. D2 的 ADD-C / SpoofCeleb 當實驗軸——無法逐因子拆／授權受限，為換而換。
8. C 移除 D4 的 EVS 通道——那是改實驗設計，越出本輪範圍。
9. Deepfake-Eval-2024 當 D1 常設第 5 格——僅 eval-only、替換不新增、不承重。
10. ASVspoof 5 adversarial 子集偷測——會復活被砍的白盒軸，釘死。
11. F 的 D4 題目仍留破折號「——」——違反去金句原則，改冒號。

### 我對五方向的最終背書換法（一行版）
- **D1**：2021 DF→DFADD(2024)、MLAAD v5→SpeechFake 開源部(2025)（退路 MLAAD v10）；種子 ASVspoof19 LA 與 In-the-Wild 維持；4×3=12 grid 不動；不上 CodecFake+/ASVspoof5 種子；Deepfake-Eval-2024 僅 eval-only 可選。
- **D2**：RTCFake 維持為唯一錨但**恢復月 0 硬閘（HF gated＋散布條款未決）**；fake 3 家 2022–2023→3 家 2025 世代（等量，不擴）；real/AudioSeal/模擬臂維持；SpoofCeleb、ADD-C 不採。
- **D3**：laundering 對象 2021 DF→**CodecFake+(2025，RQ2 同構)**；unseen 軸 MLAAD→DFADD(2024) 一格即可（**不加 SpeechFake**）；種子/動作空間/搜尋協定維持；ASVspoof5 不動、adversarial 子集嚴禁。
- **D4**：fake 2 家→2 家 2025 世代 zh 開源情緒 TTS（維持 2 家）；自建 zh-TW 定位、通道（含 EVS）維持；CFAD/SpeechFake ZH 僅 zh-CN 對照備選。
- **D5**：載體/watermark/通道矩陣全維持；只補 baseline 前作「Will They Survive Neural Codecs?」(Interspeech 2025)；CodecFake+ 僅參照不進 pipeline。

### 我背書的正式題目（複審後定案）
- **D1**：《分布偏移下語音深偽偵測的選擇性預測基準》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Shift*
- **D2**：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》／ *Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*
- **D3**：《被動語音深偽偵測之 adaptive laundering 攻擊成本上界評估》／ *An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
- **D4**：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》／ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scene Conditions: A Traditional Chinese Corpus Study*
- **D5**：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》／ *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*
