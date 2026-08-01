# Round 2 質詢：一般民眾代表（Agent F）
日期：2026-07-14

> 我的判準只有一條：**新資料集是否更接近「真實詐騙現場到達受害者耳朵的那段音訊」**——最新（含閉源）TTS 世代、繁體中文、走過真實通道。這一輪我不看誰的數字漂亮，只看兩件事：(1) 你提議換上的新集，阿嬤那位碩士生「今天真的下得到、授權真的允許」嗎？(2) 你是不是打著「換資料集」的名義，偷偷把砍掉的實驗、砍掉的軸、多開的格子塞回來？兩者都不行。

---

## 1. 抓出站不住的換資料集提議（至少 3 個）

### 駁回①：「RTCFake 已確認公開可下載、D2 單點故障解除」— 全場過度樂觀，事實不成立
**對方原文**：
- A：「RTCFake 已確認 HuggingFace `JunXueTech/RTCFake` 公開可下載…D2 的最大風險就此下降」
- B：「事實層它可直接下載——D2 最大風險下降」
- C：「landscape 已證實可下載，D2 最大單點故障事實層下降」
- D：「事實上它可直接下載，D2 最大風險就此下降」
- 我自己 Round 1 也寫了「已確認公開可下載」——**我第一個認錯。**

**反駁（category a：其實下不到/gated）**：G 這一輪實際去抓了頁面——**RTCFake 的 HF 頁面對匿名抓取回 HTTP 401，同時間 CodecFake+ 回 200**。401 是「被 gate（需登入＋同意條款才下載）」的強訊號，不是「公開直接下載」。也就是說 landscape 那句「公開可下載」是**未經抓取驗證的樂觀**，而五個角色（含我）全部照抄。從民眾視角這很危險：D2 是唯一錨真實通道的方向，如果它的真實通道錨其實是 gated + 重散布條款未明標，那「風險解除」就是自我安慰。**定案：RTCFake 維持定稿的「月 0 go/no-go 單點故障」定位不准降級**，且月 0 要同時確認兩件事——(a) 能否通過 gate 拿到本體、(b) 授權是否允許學術重散布。這不是換資料問題，是「別把沒查證的樂觀寫進論文」。

### 駁回②：「ASVspoof 5 當 D1/D3 的訓練種子（升 in-domain）」— 換了離詐騙沒更近，還讓攻擊面過度樂觀
**對方原文**：
- C（D1）：「訓練種子（可選）2019 LA → **ASVspoof 5 train 抽 20k**…訓練種子的通道多樣性升級」
- C（D3）：「種子 2019/2021 → ASVspoof 5（內建 codec + adversarial）」，B、G 亦列為「可選升級」。

**反駁（category c＋d）**：D（紅隊）已經把話講死——ASVspoof 5 內建 adversarial 攻擊與 neural codec 條件，**拿它當訓練種子＝偵測器被預先接種免疫力**，RQ1 量到的 unseen gap 會人為縮小、RQ3 的攻擊成本會人為升高，攻擊面評估變得過度樂觀。這正是紅隊說的「換資料換到自己騙自己」。加上換種子＝要重訓（D1 定稿明言「日曆是唯一瓶頸、frozen-only 才做得完」），這已經是**改方法論、動算力**，不是換餵進去的資料。從民眾視角更關鍵：把種子從 2019 錄音棚換成 2024 crowdsourced 英文多裝置，**對「台灣阿嬤接到的詐騙電話」一點都沒更近**——它換的是英文 in-domain 的定義，不是詐騙現場。**定案：ASVspoof 5 訓練種子一律不採，連「可選」都不必留**（留著就是給人偷渡 adversarial 的門，見駁回⑥）。

### 駁回③：「Deepfake-Eval-2024 當 D1 的一個 source 格 / eval 錨」— 加格＝擴 grid，且離詐騙現場遠
**對方原文**：
- A：列為「可選 eval 錨」但承認「當主力會加一格、動 12 格結構」；B：「整段當一個 eval 格」；我 Round 1 也提「加 Deepfake-Eval-2024 當真實流通錨」。

**反駁（category a＋b）**：H 抓得對——D1 的 grid 是 4 source × 3 channel = 12 格，Deepfake-Eval-2024 進來就是**第 5 個 source 格 → 15 格**，評估前向、RQ3 對抗搜尋、悲觀重跑全部跟著漲，這是「換資料集偽裝的範圍膨脹」。而且它 🟡 scrape 內容再散布受限、52 語非繁中。民眾視角誠實話：它是唯一「隱含含閉源商用世代」的公開集沒錯，但**它離台灣詐騙現場很遠（52 語、社群 scrape、非電話通道）**，用它換掉某個乾淨可控的 unseen 格，付出的代價（散布風險＋加格）大於它帶來的時效性。**定案：Deepfake-Eval-2024 只在 discussion 以一句話提「本 benchmark 未涵蓋閉源商用世代」，不進網格、不加格、也不替換乾淨格。**

### 駁回④（補充）：「ADD-C 當 D2 模擬側對照基準」— 為換而換＋偷渡新軸
**對方原文**：G「可（選擇性）以 **ADD-C（2025）** 當模擬臂的公開基準」；C 列 🟡 備選。
**反駁（category e：舊的才是正解）**：C 自己的鐵律 1 講得最清楚——D2-RQ3 的逐因子落差分解**需要模擬側是我方能逐項加回丟包/jitter/DSP 的受控管線**，ADD-C 的固定條件無法逐因子拆。用 ADD-C 換掉自建 Opus/AMR-WB＝把可控自變數換成綁死的既成條件，**方法論被迫改**。H 也明令「ADD-C 不得升為模擬側對照基準新軸」。**定案：自建 Opus/AMR-WB 模擬臂維持，ADD-C 至多 discussion 引用。**

### 駁回⑤（補充）：「SpoofCeleb 當 D2 real 主力」— 授權受限＋英文名人非詐騙現場
**對方原文**：多人列 🟡 備選（A/B/C/D/G/H 皆標備選，這點大家其實有共識）。
**反駁（category a＋d）**：它衍生自 VoxCeleb1（Oxford VGG 非商用研究授權），再散布受限；且內容是英文名人訪談，離「詐騙電話裡的真人 bona fide」很遠。大家已正確標備選——**我只是釘死它不准在 Round 3 被人偷偷扶正為主力。**

---

## 2. 抓出偷渡的範圍擴充（本輪最需要防的）

| 偷渡點 | 點名 | 性質 | 我的裁定 |
|---|---|---|---|
| **D1 unseen 軸一次擺 5 件套**（DFADD + CodecFake+ + SpeechFake 開源部 + Deepfake-Eval-2024 + MLAAD v10） | **A、B**（F 我自己 Round 1 也擺了 3–4 件） | 5 個新集塞進 2 個可換格＝ grid 4×3 爆成 7–8 source 格，前向/搜尋/重跑翻倍 | **擋下。** D1 只有 2 個 source 格可換（unseen-gen、unseen-breadth），最多換 2 個新集，其餘進 future work（H 抓得對） |
| **D2 fake 補 CodecFake+ ＋ SpeechFake ＋ DFADD 三家 diffusion/FM/codec** | **C**（「DFADD 補 diffusion/FM 格」） | 定稿 fake 是 3 家，「補一個 diffusion/FM 格」暗示擴充 fake 多樣性到 4+ 家 | **擋下。** 只准等量替換 3 家（H 明訂），不得因「新世代多」擴家數 |
| **D3 順手用 ASVspoof 5 的 adversarial（Malafide/Malacopula）子集** | 尚無人明講要用，但 **B/C/G 把 ASVspoof 5「內建 adversarial」當賣點列可選種子** | 一旦有人「反正資料集剛好有 adversarial，順便測」＝復活 D3 定稿已一刀砍掉的白盒 PGD 對抗軸 | **釘死。**（H 已釘，我加一票）採 ASVspoof 5 只准用 TTS/VC + codec 條件，adversarial 子集**碰都不准碰**——所以我索性主張 D3 連 ASVspoof 5 都不用（見背書） |
| **D2 ADD-C 升模擬基準 / SpoofCeleb 升 real 主力** | **G（ADD-C）、多人（SpoofCeleb 備選）** | 各自多開一條資料線／評估臂 | **擋下**（見駁回④⑤） |
| **D4 zh-CN 對照臂（SpeechFake ZH / CFAD）升為第二實驗** | 尚無人明升，但 **全場都在提** | zh-CN 對照臂若升格＝偷換方向的主體語言與尺度 | **釘死。** 只服務「證明落差非單一 zh-TW 腔調 artifact」這一句話，外部效度須明標，不得升主軸（H 已釘） |
| **D5 拿 CodecFake+ 拉成新載體軸/新 watermark-family 軸** | 尚無人明升，**C/D/G/H 都正確擋住** | 會讓 RQ1 從「容量塌陷點（codec 軸）」滑回被砍的「watermark 分類學」 | **維持擋下。** CodecFake+ 對 D5 至多是文字參照，不進 pipeline |

**民眾一句話**：這一輪最漂亮的話術是「這個新集剛好也含 X，順便…」——凡是「順便」後面接的東西，都是偷渡。全砍。

---

## 3. 題目正式化複審

> 我只用一把尺：學位論文題目要**名詞收尾、單一 deliverable、無金句、無問句、無破折號 hook、無口語**。

- **D1**：H 版《分布偏移下語音深偽偵測的選擇性預測基準》/ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection* **最乾淨**，採此。
  - A 版英文 *A Shift-Aware Benchmark…under Distribution Shift* **Shift-Aware 與 under Distribution Shift 語意重複**（A 自己也承認），不採。
  - 「基準研究」的「研究」贅字（基準本身即 deliverable），G/A/B 的「…基準研究」建議刪「研究」。

- **D2**：H 版《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》/ *Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution* **採此**。
  - C 版主標「離線模擬與真實通訊通道之落差：…」**仍是金句式 hook（「之落差」當賣點）**，且整句過長，不採。
  - 我 Round 1 自己的版本沒問題但比 H 版累贅，讓位給 H。

- **D3**：全場英文已收斂 *An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*，但有兩處未定：
  - 中文「洗白」（D）vs「洗訊」（H）vs 保留英文「adaptive-laundering」（A/B）——**需拍板統一**。我傾向 H 的「調適式洗訊」（laundering 是音訊去識別的對抗版，「洗訊」比「洗白」精確、比夾英文正式）。
  - 「地圖 / Map」略帶比喻色彩，G/A 的「評估 / Assessment」更中性學術。**兩者皆可過，但若指導教授要最保守，用「評估上界」而非「上界地圖」。** 我不否決「地圖」，只標示這是唯一還帶一點花俏的殘留。

- **D4**：H 版《…評估效度審計》/ *…under Scam-Scene Conditions* 乾淨，但**主標把「繁體中文」丟掉了**。民眾視角：D4 唯一直接服務台灣受害者，「繁體中文語料」必須寫進題目，讓題目本身就宣告它為誰而寫。採 D 版結構《詐騙情境條件下語音深偽偵測的評估效度審計：一份繁體中文語料研究》/ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*。
  - **我自我修正**：我 Round 1 用了破折號「——以繁體中文語料為例」，**違反「去破折號」原則**，改用冒號副標。
  - 英文 *Scam-Scene*（H）vs *Scam-Scenario*（D/F）——**Scenario 較標準**，採 Scenario。

- **D5**：H 版《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》/ *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment* **採此**。
  - C 版「兼論歐盟 AI 法第 50 條…」的「歐盟 AI 法」是簡稱，H 的「歐盟人工智慧法」全稱較正式。C 版可過但 H 版更嚴謹。

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

> 原則：**離詐騙現場越近的方向、換得越積極；離得越遠、越誠實維持。** 全部沿用 20k 分層抽樣、不加格、不加 RQ、不改方法論。

**D1（通用 benchmark，換 unseen 軸即可）**
- unseen-generator 格：ASVspoof 2021 DF → **DFADD（2024，diffusion/FM，用 2025-04 修正版）**
- unseen-breadth 格：MLAAD v5 → **MLAAD v10（2025）**（drop-in 升版，零風險；SpeechFake 開源部與 CodecFake+ 皆佳，但只能二選一填這一格，不得兩個都上）
- **維持**：ASVspoof 2019 LA 訓練種子（不重訓、不接種）、In-the-Wild real 格、C_clean/C_celp/C_neural 通道軸
- Deepfake-Eval-2024、ASVspoof 5：**不進網格**，僅 discussion 一句話
- grid 維持 4×3=12 格

**D2（換 fake 世代，但真實通道錨別吹牛）**
- fake：XTTS-v2/VITS/YourTTS（2022–23）→ **3 家 2025 開源 TTS 等量替換**（如 F5-TTS / CosyVoice 2 / 一個 codec-based 生成器），家數維持 3
- 真實通道錨 RTCFake：**維持定稿「月 0 go/no-go 單點故障」，不准降級**（G 查證疑 gated；月 0 確認能否過 gate＋能否學術重散布）
- **維持**：real 類（ASVspoof19/In-the-Wild real）、AudioSeal 單一、自建 Opus/AMR-WB 模擬臂
- ADD-C、SpoofCeleb：**不採**（至多 discussion）
- **論文須明寫外部效度限制**：RTCFake 是 Zoom/RTC 通道，≠ 阿嬤接到的 +886 假檢警電話的蜂巢/PSTN 通道

**D3（換得最契合，CodecFake+ 直接對上 RQ2）**
- laundering 對象 / 確認池：ASVspoof 2021 DF + MLAAD → **CodecFake+（2025，MIT，31 codec + 17 codec-based 生成）+ DFADD（2024，修正版）**
- **維持**：ASVspoof 2019 LA 訓練種子（**不換 ASVspoof 5**——為的是連 adversarial 子集的門都不留）、laundering 動作空間工具鏈、greedy 搜尋協定、20k/10k 抽樣
- 若指導教授仍要升種子：**只准 ASVspoof 5 的 TTS/VC + codec 條件，adversarial 子集嚴禁進評估**

**D4（我最有把握、也最救得了人——fake 世代非換不可）**
- fake：情緒可控 VITS/OpenVoice 類（2022–23）→ **2 家 2025 世代 zh 開源可控情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 中選 2 家）**，家數維持 2
- **維持**：自建 zh-TW 定位（無現成 zh-TW 集，這是硬事實）、~165 條話術腳本、real 載體、offline codec 通道、UTMOS+ECAPA 品質協變量、月 0–1 情緒 zh-TW TTS 硬 go/no-go 關卡
- SpeechFake ZH / CFAD：**僅 zh-CN 對照臂**，明標腔調非 zh-TW 的外部效度限制，不得升主軸
- 民眾理由：用 2022 爛哭腔測 2026 詐騙＝發給廠商免死金牌；升 2025 世代這份繁中考卷才擋得住搪塞

**D5（誠實維持，這不是偷懶）**
- **全部維持**：載體語音（AISHELL-3/LibriSpeech/real，年份不影響物理量測）、watermark 家族（AudioSeal/WavMark/SilentCipher，已是開源全集）、通道矩陣（EnCodec/DAC/SpeechTokenizer）
- 唯一更新：baseline 補 **《Will They Survive Neural Codecs?》（Interspeech 2025）** 為直接前作（零 GPU、零新 RQ）
- CodecFake+：至多文字參照，**不進 pipeline、不拉成新軸**
- 民眾理由：D5 服務事後語音訊息/選民自證，本就不對即時詐騙電話；它量的是 watermark 過通道還剩幾 bit，載體是真人聲、不是 fake，硬換載體是搞錯對象

---

## 回傳摘要（純文字資料）

### 我駁回的提議（每項 ≤30 字）
1. RTCFake「已確認公開可下載、風險解除」— G 查證匿名抓取 401 疑 gated，維持月 0 單點故障。
2. ASVspoof 5 當 D1/D3 訓練種子 — 改 in-domain 定義＋重訓，adversarial 預先接種使攻擊面過度樂觀。
3. Deepfake-Eval-2024 當 D1 新 source 格 — 加第 5 格擴 grid，且 scrape 散布受限、非繁中、離詐騙遠。
4. D1 unseen 軸一次上 5 件套 — 2 個可換格塞 5 集，grid 爆 7–8 格，偷加實驗。
5. ADD-C 升 D2 模擬側對照基準 — 綁死條件無法逐因子拆，逼改方法論＋偷渡新軸。
6. D3 用 ASVspoof 5 的 adversarial 子集 — 復活定稿已砍的白盒對抗軸，違規。
7. SpoofCeleb 當 D2 real 主力 — VoxCeleb 非商用衍生授權受限，且英文名人非詐騙現場。
8. D2 fake 補到 4+ 家（DFADD 另補 diffusion 格）— 定稿 3 家，只准等量替換不得擴家數。

### 五方向最終背書換法
- **D1**：ASVspoof 2021 DF →（unseen-gen 格）DFADD(2024, 修正版)；MLAAD v5 →（breadth 格）MLAAD v10(2025)；ASVspoof19 種子＋In-the-Wild＋通道軸維持；Deepfake-Eval-2024/ASVspoof 5 只進 discussion；grid 維持 4×3。
- **D2**：fake XTTS/VITS/YourTTS → 3 家 2025 開源 TTS（家數不變）；RTCFake **維持月 0 單點故障、不降級**（疑 gated）；real 類/AudioSeal/Opus+AMR-WB 模擬臂維持；ADD-C/SpoofCeleb 不採；論文須標「RTC ≠ 詐騙電話蜂巢通道」。
- **D3**：laundering 對象 2021 DF + MLAAD → CodecFake+(2025, MIT) + DFADD(2024, 修正版)；ASVspoof19 種子維持、**不換 ASVspoof 5**（不留 adversarial 的門）；動作空間/搜尋協定/抽樣維持。
- **D4（最有把握）**：fake 2 家 → 2 家 2025 世代 zh 開源情緒 TTS（家數不變）；自建 zh-TW 定位＋月 0–1 go/no-go 維持；SpeechFake ZH/CFAD 僅 zh-CN 對照臂、標外部效度、不得升主軸。
- **D5**：資料集**全維持**（載體/watermark/通道矩陣皆當前最佳、無更新可換）；唯一更新 baseline 補《Will They Survive Neural Codecs?》(Interspeech 2025)；CodecFake+ 不進 pipeline。

### 一句話立場
最該換、最救得了人的是 **D4 的 fake 世代**（升 2025 zh 情緒 TTS）；最該踩煞車的是 **D2 的 RTCFake 樂觀**（G 查出疑 gated，別把沒查證的「可下載」寫進論文）；**D5 誠實維持不換**（載體年份不影響物理量測，硬換是搞錯對象）。
