# Round 2 質詢：資料集與 benchmark 策展人（Agent B）
日期：2026-07-14

> 立場：我是決定「每個換資料集提議可不可行」的人。本輪我用同事 G（史官）實際查證的取得性事實，去覆蓋**我自己 R1 與 landscape 裡過度樂觀的敘述**——策展人的誠實優先於維護自己的文件。質詢只鎖定資料集與題目，不碰 RQ／方法。

---

## 1. 抓出站不住的換資料集提議（4 個）

### 駁回 1（類型 a：其實下不到／gated）——「RTCFake 已確認公開可下載，D2 風險解除」

**原文**：A「RTCFake 已確認 HuggingFace `JunXueTech/RTCFake` 公開可下載…D2 最大單點故障事實層下降」；C「landscape 已證實可下載」；D「事實上它可直接下載，D2 最大風險就此下降」；F「已確認公開可下載…降風險」；H「由『單點故障』降級為『已確認可下載』」。**連我自己 R1 都寫了「校正為 HuggingFace 公開可下載」。**

**反駁**：這是**全場一起站在我 landscape 的樂觀敘述上，而那個敘述被 G 的實測推翻了**。G 這輪實際抓 HF 頁面：**RTCFake 匿名抓取回 HTTP 401（gated 強訊號），同一時間 CodecFake+ 回 200。** 401 代表它需要**登入 + 同意 gate 條款**才下得到，不是「直接下載」；且 repo 未明標學術重散布授權。所以「風險解除」是錯的——**RTCFake 仍是月 0 的真單點故障**（gate 能否通過 + 重散布條款兩關未過）。我作為策展人正式撤回 landscape §四「已確認公開可下載」這句，改判為「🟡 疑似 gated、月 0 必須先過 gate 再讀條款」。這不改 D2 方法，但把 D2 的 go/no-go 風險等級**調回定稿的悲觀值**，不准任何人拿「反正下得到」去鬆綁退路。

### 駁回 2（類型 c：需改方法論＝換題目）——ASVspoof 5 當 D1／D3 的「訓練種子」替換

**原文**：C「訓練種子（可選）2019 LA → ASVspoof 5 train 抽 20k」；F「（可選）in-domain 訓練種子 ASVspoof 2019 LA → ASVspoof 5 train」；D3 中 D、F、G-以外多人把 ASVspoof 5 列為「種子池升級」；H「ASVspoof 5 train 僅列可選備選」。

**反駁**：A 這一刀說得最準，我完全背書並升級為硬判定——**換訓練種子＝要重訓，直接違反本輪禁止**。D1／D3 用的是 frozen AASIST / RawNet2 / SSL-AASIST / XLS-R backend，**這些 checkpoint 全是 ASVspoof19 LA 訓練出來的**；把種子換成 ASVspoof 5，偵測器要對新分布重訓、重驗 EER，「日曆是唯一瓶頸」的定稿判定當場破產。這不是「換餵進去的資料」，是**換掉權重的來源＝換方法＝換題目**，屬本輪明令禁止。所以 ASVspoof 5 **不得當訓練種子**，頂多當 eval-only 的 unseen 對象（抽 20k、frozen 前向），且要背 D 的接種警告（見下）。凡把它寫進「訓練種子欄」的提議，一律不合格。

### 駁回 3（類型 d：換上去其實不更貼近該任務的真實，反而污染量測）——CodecFake+ 當 D2 的 fake 來源

**原文**：A「D2 fake…改抽 SpeechFake 開源部…可補 CodecFake+ 的 codec 世代」；C「D2 fake…CodecFake+（2025）+ SpeechFake 開源部為主…CodecFake+ 的 fake 本身即 neural-codec 產物——當它再過真實 RTC 通道，正是我最想量的存活場景」；D、F 同列 CodecFake+ 為 D2 fake。

**反駁**：C 自己把問題講出來卻當成優點——**CodecFake+ 的 fake「本身即 neural-codec 產物」，是已經過一次 codec 的樣本**。D2 量的是「反制訊號在**我方受控通道** vs 模擬通道的差分存活 γ」，這需要 fake 進通道前是**乾淨基準（C0'）**，才能把 γ 乾淨歸因給「我加的那一層通道」。餵一個出廠就帶 codec 畸變的 fake，等於 codec-on-codec，**C0' 基準被污染、γ 的畸變層歸因（D2-RQ3）失真**。這跟 D3 不同——D3 的 laundering 動作**本來就是**再過一次 codec，codec-on-codec 是它要研究的東西；D2 不是。所以 D2 的 fake 世代升級**只用 SpeechFake 開源部的乾淨合成**（landscape §2.2 已註明其「乾淨合成為主、無專門通道條件」），**CodecFake+ 不進 D2 fake 池**；真要有 codec-based 世代，明確標一個乾淨生成的 codec-TTS，不要拿 CodecFake+ 這種已 transcode 的成品。

### 駁回 4（類型 e：為換而換／舊配置才是正解）——SpeechFake 當 D3 unseen 軸的「核心」新資料

**原文**：B（我 R1）、A、C、D、F 都把 D3 unseen 軸寫成「CodecFake+ + DFADD + **SpeechFake 開源部**」三件套。

**反駁**：G 的紀律我背書——**D3 加 SpeechFake 是多餘的第三源**。D3 的 20k 確認池／10k 搜尋池是**固定容量**；「neural-codec + diffusion/FM」兩個 2025 關鍵範式已由 **CodecFake+（codec 世代，且與 RQ2 同構）+ DFADD（diffusion/FM）** 完整覆蓋。再塞 SpeechFake 進同一個固定池，只會**稀釋前兩者的樣本密度**，對「攻擊成本上界」的解析度是負貢獻；若不進固定池而另開，就是偷加搜尋規模＝違反「不因換資料順便擴充」。所以 D3 的 unseen 軸**核心只保 CodecFake+ + DFADD**，SpeechFake 降為「可選廣度、不進承重搜尋池」。這條同樣適用於 D1：不要四件套（DFADD+CodecFake++SpeechFake+MLAAD v10）全上，見第 2 節。

---

## 2. 抓出偷渡的範圍擴充（逐一點名）

本輪最該防的就是「用換資料集偷加格子／家數／軸」。點名如下：

**（1）D — D1 把 Deepfake-Eval-2024 寫進驗收表當第 5 個承重 eval 格。** D 的 R1 D1 驗收表把 Deepfake-Eval-2024 與 DFADD／CodecFake+／SpeechFake 並列成一格。**這是把 4 source 格擴成 5 格＝偷加一批前向 + RQ3 對抗搜尋 + 悲觀重跑。** H、G 都已釘死：Deepfake-Eval-2024 若要用，只能**替換**某一格、不得**新增**；且它 scrape 內容再散布受限（🟡），最穩的處理是**只在 discussion 以文字提「未涵蓋閉源商用世代」，完全不進網格**。我採 G/H 的判定：D1 grid 維持 4×3，Deepfake-Eval-2024 不進格。（我 R1 與 A、F 也都提了它，一併收斂為「不進格、討論區文字帶過」。）

**（2）C — D4 移除 EVS。** C 主張「自傳統 codec 集移除 EVS」，包裝成「縮範圍 + CPU 減法」。**但這不是換資料集，是動實驗設計（codec 矩陣）。** 本輪憲章白紙黑字：「核心方法、實驗設計全部維持定稿不動——只換餵進去的資料」。EVS 是 D4 的**通道條件**，不是「餵進去的 fake 資料」；增或減都不在本輪授權內。CPU 論證再有理，也該進另一場「實驗設計精修」會，不是這場。**駁回 EVS 移除，D4 codec 矩陣維持定稿。**（同理否決 C 在 D2 想引入 ADD-C 當「模擬側基準」——H 已釘死，那是新增一條資料處理線。）

**（3）C／F — D1／D3 fake 生成器候選列 4 家（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2），D4 若照抄＝家數膨脹。** H 已釘：D4 fake **維持 2 家**、D2 fake **維持 3 家**、等量替換不得擴充。我強化：4 個候選是「選 2／選 3 的池」，**不是全上**。凡把「2025 世代選擇多」當理由擴家數者，偷渡。

**（4）任何人動 ASVspoof 5 的 adversarial 子集。** H 的釘死我原文照收：ASVspoof 5 首次內建 Malafide/Malacopula adversarial 攻擊，D3 定稿已一刀砍白盒 PGD 軸——**若以「新資料剛好有 adversarial，順便測」把它拉回，就是偷偷復活被砍的白盒對抗軸**。即便 ASVspoof 5 只當 eval 對象，也**只准用其 TTS/VC spoof + codec 條件，adversarial 子集嚴禁進評估**。這是本輪第二危險的偷渡，與 RTCFake 樂觀敘述並列我最盯的兩點。

---

## 3. 題目正式化複審

**D1**——H 的《分布偏移下語音深偽偵測的選擇性預測基準》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection* **最乾淨**（名詞收尾、無冗字）。A／G／我 R1 的尾綴「…基準**研究**」對一個 benchmail deliverable 是冗字，可刪。英文 A 版 *…under Distribution Shift* 與 *Shift-Aware* **shift 重複**（A 自己也承認）；G 版 *under Unseen Generators and Channels* 精準但中文「面向未見生成器與通道之…可靠性基準研究」修飾語堆疊過長。**建議定案**：中文用 H 的乾淨主幹；英文取 H 主幹 + G 的 shift 來源明示但不重複——*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Shift*（我 R1 的英文，去掉 distribution 一詞即不重複）。

**D3**——五人主幹一致（*An Attacker-Cost Upper-Bound Map/Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*），但**「laundering」中譯四人四樣**：我 R1 保留英文 adaptive-laundering、D「適應性洗白」、G「適應性洗刷」、H「調適式洗訊」。**必須統一。** 「洗白」偏口語、「洗訊」是生造詞、「洗刷」語感雜。**建議定案**：中文標題保留英文術語「adaptive laundering」（learned 術語，論文慣例允許），或採 H 的「調適式洗訊」並在摘要首次出現時括註 (adaptive laundering)。另「上界**地圖**／**Map**」略帶比喻色彩，A／G 已改「上界**評估**／Assessment」較正式——但「cost map」是既成視覺化概念，可保留，屬可接受邊界，我不強制改。

**D4**——**F 的版本仍不合格**：《…評估效度之審計**——以繁體中文語料為例**》用了**破折號**，正是本輪明令要去掉的花俏標點。H 的《詐騙情境條件下語音深偽偵測的評估效度審計》乾淨，但**丟了「繁體中文」這個 D4 的實質貢獻與地域定位**（不該丟）。D 的《…評估效度審計：一份繁體中文語料研究》結構最對（冒號副標 + 保留繁中），僅「一份…研究」略口語，收成「：繁體中文語料庫研究」。英文 *Scam-Scenario*（D/F）優於 H 的 *Scam-Scene*（scene 語感偏「場景畫面」）。**建議定案**：《詐騙情境條件下語音深偽偵測的評估效度審計：繁體中文語料庫研究》／ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*。

**D2**——H 的《…存活的樂觀偏差及其畸變層歸因》／ *Optimism Bias…: A Distortion-Layer Attribution* 最精簡準確。C 的主標是完整子句「離線模擬與真實通訊通道之落差：…」偏長；F「存活**率**」用詞可，皆可接受。採 H。

**D5**——H 的《…可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》優於 C 的「歐盟 **AI 法**第 50 條」（「AI 法」是口語簡稱，學位論文用全名「人工智慧法」）。採 H。

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

**D1｜選擇性預測基準**
- unseen 軸（維持 4×3、只換 2 個 source 格內容）：**ASVspoof 2021 DF 格 → DFADD（2024, MIT, 用 2025-04 修正版）**；**MLAAD v5 格 → SpeechFake 開源部（2025, Apache 2.0）抽 20k**（或最省事的 MLAAD v5→**v10** drop-in，二選一，不併上）。
- **不進格**：CodecFake+（留給 D3／D5，避免 D1 變第 3 新源）、Deepfake-Eval-2024（scrape 受限，僅 discussion 文字帶過）。
- **維持**：ASVspoof 2019 LA 訓練種子（換＝重訓，駁回）、In-the-Wild（第一週 smoke-test）。

**D2｜通道存活審計**
- fake：**XTTS/VITS/YourTTS → SpeechFake 開源部乾淨合成，等量替換 3 家**；**CodecFake+ 不進 D2 fake 池**（已 transcode，污染 C0'／γ，駁回）。
- 真實通道錨：**RTCFake 維持為唯一 RTC 錨，但撤回「風險解除」——G 實測 401/gated，月 0 go/no-go 全額保留**（過 gate + 讀重散布條款）。
- **維持**：real 類公開集（SpoofCeleb 僅 🟡 備選）、AudioSeal、模擬臂 Opus/AMR-WB（ADD-C 不進實驗）。

**D3｜攻擊成本上界地圖**
- laundering 對象／確認池：**ASVspoof 2021 DF → CodecFake+（2025, MIT, 101 GB, 非 gate；與 RQ2 neural-codec 同構）**，抽 20k 確認／10k 搜尋。
- unseen 軸：**MLAAD → DFADD（2024, 修正版）**。**SpeechFake 降為可選廣度、不進承重搜尋池**（駁回三件套）。
- **維持**：ASVspoof 2019 LA 種子（駁回 ASVspoof 5 換種子）；laundering 動作空間。若學生仍要 ASVspoof 5 當 eval 對象，**只取 TTS/VC+codec、adversarial 子集嚴禁進評估**。

**D4｜繁中詐騙審計**
- fake：**2022–2023 世代 → 2025 世代 zh 開源情緒 TTS，自 CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 選 2 家（維持 2 家，不擴 4 家）**。
- **維持**：自建 zh-TW 定位（無現成 zh-TW 集）、real 類、話術腳本、**codec 矩陣含 EVS（駁回 C 的 EVS 移除）**、UTMOS/ECAPA 品質協變量、月 0–1 情緒 zh-TW TTS 硬 go/no-go。
- 對照臂：CFAD / SpeechFake ZH **僅 zh-CN 對照、標外部效度、不升格**。

**D5｜watermark 位元容量**（誠實維持方向）
- **維持**：載體語音（年份不影響量測）、watermark 家族 AudioSeal/WavMark/SilentCipher（已是開源全集）、通道矩陣（EnCodec/DAC/SpeechTokenizer）。
- 唯一更新：**baseline 補「Will They Survive Neural Codecs?」（Interspeech 2025, arXiv 2505.19663）**，0 GPU、0 新 RQ。
- CodecFake+ **僅文獻參照、不進 pipeline**（駁回把它拉成新載體／新軸）。

---

## 回傳（純文字資料）

### 我駁回的提議（每項 ≤30 字）
1. RTCFake「公開可下載、風險解除」——G 實測 401/gated，D2 單點故障不解除。
2. ASVspoof 5 當 D1/D3 訓練種子——換種子＝重訓 frozen 偵測器＝換方法，違規。
3. CodecFake+ 當 D2 fake 來源——已 transcode，污染 C0' 與 γ 歸因。
4. SpeechFake 當 D3 unseen 核心第三源——CodecFake++DFADD 已足，稀釋固定池。
5. Deepfake-Eval-2024 進 D1 網格（D）——4×3 變 5 格，偷加前向與重跑。
6. D4 移除 EVS（C）——動 codec 矩陣＝改實驗設計，非換資料，越權。
7. ASVspoof 5 adversarial 子集進評估——復活被砍的白盒對抗軸。
8. D4 fake 擴為 4 家、D2 擴為 5 家——等量替換原則，家數不得膨脹。

### 我對五方向的最終背書換法
- **D1**：ASVspoof 2021 DF 格→**DFADD(2024 修正版)**；MLAAD v5 格→**SpeechFake 開源部(2025)** 或 **MLAAD v10** 二選一；grid 維持 4×3；ASVspoof 2019 LA 種子與 In-the-Wild **維持**；CodecFake+／Deepfake-Eval-2024 **不進格**。
- **D2**：fake→**SpeechFake 開源部乾淨合成，等量 3 家**（CodecFake+ 不用）；**RTCFake 維持但月 0 go/no-go 全額保留（gated，非風險解除）**；real 類／AudioSeal／模擬臂 **維持**。
- **D3**：laundering 對象→**CodecFake+(2025, MIT)**；unseen→**DFADD(2024)**；SpeechFake 降可選；種子 ASVspoof 2019 LA **維持**（ASVspoof 5 至多 eval-only 且禁 adversarial）。
- **D4**：fake→**2025 世代 zh 開源 TTS 選 2 家**；自建定位、codec 矩陣（含 EVS）、go/no-go **維持**；CFAD/SpeechFake ZH 僅 zh-CN 對照。
- **D5**：載體／watermark 家族／通道矩陣 **全維持**；唯一補 baseline 前作「Will They Survive Neural Codecs?」(2025)；CodecFake+ 僅參照。

### 一句話總結
最該被糾正的不是「舊資料」，而是**兩個過度樂觀**：RTCFake 其實 gated（G 實測），CodecFake+ 不能無腦塞進每個方向（D2 會被 codec-on-codec 污染）——換新要積極，但取得性與量測純度由我把關，不由熱情把關。
