# Round 2 質詢：訊號與通道（Agent C）
日期：2026-07-14

> 角色立場：我只從兩件事質詢每一個換血案——(1) 這個換法有沒有把「真實傳輸／通道條件」帶進來、還是只是換一批乾淨合成 fake；(2) 換上去 CPU 前處理（codec 轉檔、resample、tandem 鏈）、磁碟（>TB 下載、通道副本）會不會爆日曆。凡是「新但拿不到 / 新但需要動通道方法論 / 新但把 CPU 前處理推上懸崖 / 為換而換」的，我一律駁回。範圍只限資料集與題目，不碰 RQ、方法、實驗軸。
>
> 先講一句結論：Round 1 七份裡最危險的不是「換錯資料集」，而是**三件被樂觀敘事蓋過去的事實**——(a) RTCFake 其實是 gated（G 已抓到 401），全場卻五份都寫「風險解除」；(b) CodecFake+ 被同時塞進 D2/D3 當 fake，但它本身是 codec 產物，塞進 D2 會污染我這關最在意的「畸變層歸因」；(c) 把 ASVspoof 5 當訓練種子＝重訓＋預先接種，是偽裝成換資料的方法變更。以下逐項。

---

## 1. 抓出站不住的換資料集提議（≥3）

### 駁回 1：「RTCFake 已確認公開可下載，D2 最大風險解除」——事實層錯誤，屬 gated（分類 a）

B 原文：「RTCFake（2026）已確認 **HuggingFace `JunXueTech/RTCFake` 公開可下載** …定稿把它當『月 0 go/no-go 單點故障』，事實層它可直接下載——D2 最大風險下降。」A、D、F 及我自己 Round 1、以及 landscape 全部同調寫「已確認公開可下載 / 降風險」。

反駁：**這是全場最需要修正的一句。** G 這輪實際去抓 HF 頁面，`JunXueTech/RTCFake` 對匿名抓取回 **HTTP 401**，同一時間 CodecFake+ 回 200——401 是「被 gate（需登入 + 同意條款才下載）」的強訊號，且 repo 未明標學術重散布授權。所以正確敘述不是「公開可直接下載、風險解除」，而是「**gated，需過 gate + 讀重散布條款**」。從我的訊號視角，RTCFake 是 D2 唯一的真實 RTC 通道錨（唯一把 Zoom noise-suppression/echo-cancellation/codec/丟包「烘進波形」的公開大集），它到底能不能拿到直接決定 D2 存不存在——這正是 D2「樂觀偏差」主題的自我諷刺：**我們差點對自己的資料取得性犯了樂觀偏差。** 定案：RTCFake 維持為錨，但**月 0 go/no-go 照走、失敗機率不下修**，須確認 (a) 過 gate、(b) 授權允許學術重散布；拿不到就走定稿退路（純模擬臂 + 誠實標明缺真實通道臂）。

### 駁回 2：「CodecFake+ 當 D2 的主 fake」——codec-on-codec 污染畸變層歸因（分類 d，且逼近 c）

A 原文：「fake 生成器世代升級：3 家 2022–2023 開源 TTS → 改抽 SpeechFake 開源部（2025）現成 fake（可補 **CodecFake+ 的 codec 世代**）」；D、F、B 同樣把 CodecFake+ 列進 D2 fake 池；我自己 Round 1 甚至寫「CodecFake+ 的 fake 本身即 neural-codec 產物——當它再過真實 RTC 通道，是『codec 世代訊號 × 真實通道』，正是我最想量的存活場景」。

反駁（這是我這關最強、也最該收回自己 Round 1 的一筆）：**D2 的承重 RQ3 是「逐因子畸變層歸因」——把樂觀偏差 γ 拆給 codec / PLR / jitter / DSP 各層。** CodecFake+ 的 fake 是 neural codec 的產物，訊號進到審計台時 codec artifact 已經烘在裡面。對已 codec 化的波形再過通道 codec，其邊際畸變是**次可加（sub-additive／近似冪等）**的——codec 對已 codec 化訊號的破壞力天生比對乾淨訊號小。後果：**「codec 層」這一格的歸因會被系統性低估**，畫出來的畸變層地圖把 codec 的真實貢獻壓低。（注意：對「聚合 γ」影響較小，因為源端 codec 在模擬臂與真實臂兩側同時存在、差分時部分抵消；受害的是**逐層歸因**，正是 D2 的賣點。）定案：**D2 的主 fake 應是乾淨生成範式——DFADD（diffusion/FM）+ 現成開源 TTS**；CodecFake+ 在 D2 至多當次要對照，且必須在論文明標「源端 codec 對 codec 層歸因的下偏」caveat。**CodecFake+ 的正確歸宿是 D3**（那裡 codec-on-codec 正是 RQ2 的重點，不是污染）。

### 駁回 3：「ASVspoof 5 當 D1/D3 訓練種子」——重訓＋預先接種，偽裝成換資料的方法變更（分類 c＋a）

landscape 與我 Round 1 都列「訓練種子（可選）2019 LA → ASVspoof 5 train 抽 20k」；D3 的 A/F/H 也把 ASVspoof 5 列為「可選種子升級」。

反駁：三個理由，全部指向「這不是換資料，是換方法」。(1) **重訓成本**：D1/D3 用的是 frozen backbone + 現成 AASIST/RawNet2/SSL checkpoint，全是 ASVspoof19 LA 訓練的權重；換種子＝全部重訓 + 重驗 EER，A 已指出「日曆是 D1 唯一瓶頸」，這直接加訓練 GPU-h、違反本輪禁止。(2) **預先接種**（D-redteam 的點，我完全背書）：ASVspoof 5 內建 12 codec 條件 + 首含 adversarial，拿它當種子＝偵測器被預先接種 neural codec 與對抗免疫力，unseen gap 人為縮小、攻擊面過度樂觀。(3) **訊號視角**：ASVspoof 5 的 12 codec 是**綁死在資料上、不可逐因子拆解**的既成通道條件；一旦進訓練種子，就把 codec 變異灌進「in-domain 種子分布」，污染我方逐格可控的 `C_clean/C_celp/C_neural` 自變數——選擇性預測 shift 網格需要「乾淨、未接種」的種子當錨。定案：**種子維持 2019 LA**；ASVspoof 5 若真要碰，只能是額外對照臂（＝加實驗，本輪不做），或明確標為 future work。

### 駁回 4（附帶）：「D2 real 類換 SpoofCeleb」——為換而換（分類 e）

B/A/我 Round 1 都把 SpoofCeleb 列為 D2 real 類備選。反駁：D2 量的是「通道存活差分 γ」，real 只是承載反制訊號的載體，**其生成年份/錄音條件不進 γ 的一階項**；換 SpoofCeleb 只帶來 VoxCeleb 非商用衍生授權的再散布風險，科學收益為零。定案：**D2 real 維持公開 real（In-the-Wild 等）**，SpoofCeleb 連備選都不必留。

### 駁回 5（附帶）：「Deepfake-Eval-2024 當 D1 的 eval 錨」若作**新增格**——散布受限 + 偷加格（分類 a＋擴充）

B/D/F 把 Deepfake-Eval-2024 列為 D1「真實流通 eval 錨」。反駁：它是社群 scrape、再散布受限（🟡），且若當獨立 eval 格＝12 格→15 格（見第 2 節）。定案：**只能替換某一格，或留在 discussion 文字**（誠實標「未涵蓋閉源商用世代」），不得新增。G、H 的處理正確，我背書他們。

---

## 2. 抓出偷渡的範圍擴充（本輪最需要防）

1. **D1 的「四件套 / 四個全上」= 偷加格（點名 B、D）。** B 原文把 unseen 軸寫成「DFADD + CodecFake+ + SpeechFake 開源部 + MLAAD v10」四件套，D 更加上 Deepfake-Eval-2024 湊成四~五個。H 已當場抓到：「若四個全上，4 個 source 格就變 7–8 格——評估前向、RQ3 對抗搜尋、悲觀重跑全部翻倍」。**訊號側加碼**：每多一個 neural-codec fake 格，過我方 `C_neural`（EnCodec transcode，GPU）就多一份 codec transcode 成本——偷加的不只是前向，是 GPU transcode。定案：unseen 軸維持既有 2 格可換內容，三種新集**擇二填格**（不是三格），其餘只在 discussion 提。A、G、H 的「replace ≤2 cells、4×3 不動」是紀律正解，我背書。

2. **Deepfake-Eval-2024 從「eval 錨」滑成「第 5 格」（點名 D、F、B）。** 同上，additive 即擴充。守 H/G。

3. **ADD-C 從「模擬對照」升成「模擬側新軸」（G 提、我 Round 1 也碰）。** H 已釘死「至多 discussion 引用，不進實驗」。我背書並補訊號理由：D2-RQ3 的逐因子分解需要模擬臂是**我能逐項加回丟包/jitter/DSP 的受控管線**，ADD-C 的固定條件無法逐因子拆，升為軸就違規。

4. **CodecFake+ 在 D5 從「參照」滑成「新載體/通道軸」（D、F、我 Round 1 皆提參照）。** D、H 已警告「只作參照、不擴通道矩陣」。我背書：D5 通道矩陣（EnCodec/DAC/SpeechTokenizer × bitrate）是我設計的物理界線，CodecFake+ 的 31 codec 清單只能當「覆蓋是否充分」的旁證，一旦進矩陣就是 R9 級 GPU transcode 爆炸。

5. **我自己 Round 1 的「D4 移除 EVS」= 出界，主動撤回。** 誠實講：移除 EVS 雖然是縮範圍 + CPU 減法，但它動的是**通道軸（實驗設計）**，不是「換餵進去的資料」。本輪 00-constraints 明令「實驗設計全部維持定稿不動」，即使是減法也不該在「換資料集」這輪做。定案：**D4 的 EVS 去留移出本輪**，留給日後的方法複審輪；本輪 D4 只換 fake 生成器世代。這是我這關唯一的自我糾正。

---

## 3. 題目正式化複審

- **D1**：A 的英文 *A Shift-Aware Benchmark for Selective-Prediction Reliability … under Distribution Shift* **shift 重複兩次**（A 自己也承認），不夠精練。B 的 *…under Generator and Channel Distribution Shift* 與 G 的 *…under Unseen Generators and Channels* 都精確且不重複。H 的《…選擇性預測基準》最乾淨，但**中英都刪掉了 channel shift**——D1 的通道軸（`C_clean/C_celp/C_neural`）是實打實的第二 shift 來源，題目略去等於低報貢獻。修正建議：採 B/G 路線，題目點明 generator 與 channel 兩個 shift 源。

- **D2（我的核心，須最準）**：F 用「存活**率**」不妥——D2 量的是「存活差分 γ」，「率」暗示某個固定比率指標，宜作「存活」。H 的結構最正式（主標＋冒號副標），但英文 *over Communication Channels* 掉了「Real」——而 real vs simulated 正是整篇的軸心，「Real」是承重詞不可省（F 的英文有保留 *Real Communication Channels*）。修正建議：中文取 H《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》；英文取 H 結構 + F 的 Real → *Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over **Real** Communication Channels: A Distortion-Layer Attribution*。

- **D3**：中文的「adaptive laundering」譯法四家分歧——B 直接夾英文「adaptive-laundering」（放進中文標題略不正式）、D「適應性洗白」、G「適應性洗刷」、H「調適式洗訊」。從訊號本義（讓訊號過 codec/變換以抹除可偵測 artifact），**H 的「洗訊」最技術貼切**，「洗白」帶洗錢語感（主題上其實不違和，但易被誤讀）。「地圖 / Map」vs「評估 / Assessment」：A/G 降級為「評估」是怕「地圖」被讀成花俏；但「攻擊成本上界地圖」是對 laundering 動作空間的實體 deliverable（如 attack-surface map），我認為「Map」可保留，惟若口委對「地圖」敏感，「Assessment」是更安全的正式退路。修正建議：中文《被動語音深偽偵測之調適式洗訊攻擊成本上界地圖》，英文維持 *An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*。

- **D4**：F 的破折號「——以繁體中文語料為例」——**破折號正是 00-constraints 要去掉的花俏標記**，宜改冒號「：以繁體中文語料為例」。H 最乾淨但掉了「繁體中文語料」定位（那是本方向的實質貢獻與地域錨，值得留在副標）。「Scam-Scene」(H) 不如「Scam-Scenario」(D/F) 標準。修正建議：採 D《…評估效度審計：一份繁體中文語料研究》/ *…under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*。

- **D5（我的第二核心）**：H 與我 Round 1 皆可用。H「可讀性判定」略泛；Article 50 要求的是 **machine-readable** 標記，宜作「機器可讀性」以精確。修正建議：中文《通訊通道上音訊浮水印溯源標記的可靠位元容量審計：兼論歐盟 AI 法第 50 條之機器可讀性判定》，英文 *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels, with a **Machine-Readability** Determination for EU AI Act Article 50*。

---

## 4. 我背書的最終換法（含維持不換）

**通則（CPU/磁碟裁決，我這關的職責）**：本輪沒有任何換資料集會爆 CPU 或磁碟——**但有兩個工程紅線必須寫進協定**：(i) **CodecFake+（G 查證 101 GB）被 D1/D2/D3/D5 同時引用，只准下載一次、共用一份 20k 分層抽樣**，不得四方向各自 clone；(ii) **SpeechFake 開源部 >TB，只准用 HF 部分下載/streaming 抓 20k 分層樣本**，嚴禁 clone 全庫（否則撞 4.3 的 2TB NVMe 生死線）。另一個好消息成立：以 CodecFake+/SpeechFake/DFADD 這類**預生成 fake** 取代自建 TTS，D2/D4 省掉生成算力，CPU 前處理不升反降。

- **D1**：unseen 軸兩格 `ASVspoof 2021 DF + MLAAD v5` → **DFADD（2024, diffusion/FM）+ CodecFake+（2025, neural codec）**（擇二填格，維持 4×3）；選 CodecFake+ 是因為它落在我方 `C_neural` 上、generator-shift 與 channel-shift 在此格交會，是我最想看的一格。SpeechFake/MLAAD v10 只作 discussion 廣度註，Deepfake-Eval-2024 不進格。**訓練種子 2019 LA 維持、通道軸自建維持**。

- **D2**：fake **主力 = DFADD（乾淨 diffusion/FM）+ 現成開源 TTS**；**CodecFake+ 只當次要對照，附 codec 層歸因下偏 caveat**（駁回 2）。real **維持公開 real，不採 SpoofCeleb**（駁回 4）。真實通道錨 = RTCFake，**風險不解除、月 0 go/no-go 照走**（駁回 1）。模擬臂 Opus+AMR-WB 自建維持、不碰 EVS、ADD-C 僅 discussion。watermark = AudioSeal 維持。

- **D3**：laundering 對象 **主力 = CodecFake+（2025）**——此處 codec-on-codec 正是 RQ2「neural codec 不可逆必殺」的重點，不是污染；**但採 D-redteam 的 caveat：可控植入的可逆性 ground-truth 必須定義在植入的已知 artifact 上，不受源端 codec 污染**。補 **DFADD** 填 diffusion/FM 格。**種子維持 2019 LA**（駁回 3）；若真碰 ASVspoof 5，H 的釘死照辦——**只取乾淨 TTS/VC spoof，嚴禁其 adversarial 子集**（否則復活被砍的白盒軸）。動作空間、20k/10k 維持。

- **D4**：fake `情緒 VITS/OpenVoice(2022–23)` → **2025 世代 zh 開源可控 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 擇 2 家，維持 2 家）**；SpeechFake ZH / CFAD 僅 zh-CN 對照臂（標外部效度限制，不升主軸）；**自建 zh-TW 定位維持**。**EVS 去留撤出本輪**（我 Round 1 的越界，第 2 節已自糾）。

- **D5**：**全維持**——載體語音（年份不影響 bit 容量）、watermark 家族（AudioSeal/WavMark/SilentCipher 已是開源全集）、通道矩陣（我設計的可逆/不可逆物理界線）皆不換。唯一更新：baseline 補 **《Will They Survive Neural Codecs?》（Interspeech 2025）** 為 watermark×neural-codec 最新前作；CodecFake+ **僅參照、不進矩陣**。零 GPU 變動。

---

## 回傳（純文字資料）

**我駁回的提議（每項 ≤30 字）：**
1. 「RTCFake 已公開可下載、風險解除」——實為 gated（G 抓到 401），風險不解除。
2. 「CodecFake+ 當 D2 主 fake」——codec-on-codec 下偏 RQ3 畸變層歸因，改 DFADD。
3. 「ASVspoof 5 當 D1/D3 訓練種子」——重訓＋預先接種，偽裝成換資料的方法變更。
4. 「D2 real 換 SpoofCeleb」——real 只是載體、不進 γ 一階，且授權受限，為換而換。
5. 「Deepfake-Eval-2024 當新增 eval 格」——散布受限＋12→15 格偷加，只能替換或 discussion。
6. 「D1 四件套全上」——4→7~8 格偷加，含多份 C_neural GPU transcode。
7. 「我 Round 1 的 D4 移除 EVS」——動通道軸＝出界，本輪撤回。

**五方向最終背書換法：**
- D1：unseen 兩格 → DFADD + CodecFake+（擇二、維持 4×3）；種子 2019 LA 維持、通道軸自建維持；SpeechFake/MLAAD v10/Deepfake-Eval-2024 不進格。
- D2：fake 主力 DFADD＋開源 TTS，CodecFake+ 僅次要對照（附 caveat）；real 維持公開 real、不採 SpoofCeleb；RTCFake 維持但風險不解除、月 0 go/no-go 照走；模擬臂 Opus+AMR-WB 維持。
- D3：laundering 對象主力 CodecFake+（codec-on-codec 是 RQ2 重點，附植入 ground-truth caveat）＋DFADD；種子 2019 LA 維持，ASVspoof 5 只取乾淨 spoof、嚴禁 adversarial。
- D4：fake → 2025 世代 zh 開源 TTS（擇 2 家）；zh-CN 對照臂僅佐證；自建定位維持；EVS 去留撤出本輪。
- D5：全維持（載體/watermark/通道矩陣），僅補 baseline 前作《Will They Survive Neural Codecs?》，CodecFake+ 僅參照。

**CPU/磁碟裁決：** 無換法爆 CPU；兩紅線——CodecFake+（101GB）四方向共用一份 20k、SpeechFake（>TB）只部分下載抓 20k，勿 clone 全庫。預生成 fake 取代自建 TTS 使 D2/D4 前處理不升反降。
