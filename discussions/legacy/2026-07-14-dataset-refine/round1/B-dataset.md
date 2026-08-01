# Round 1 資料集提議：資料集與 benchmark 策展人（Agent B）
日期：2026-07-14

> 立場與紀律：本輪只做兩件事——(1) 把偏舊的資料集換成更新、可取得的替代品；(2) 把花俏題目正式化。三個 RQ 結構、核心方法、實驗設計、算力預算一律不動。所有大型新集**沿用定稿既有的 20k 分層抽樣規則**，不因換資料集放大規模。凡「換上去要改方法論／加 RQ／加實驗軸」者，一律不列為主力（見各方向紅線註）。事實依據：`../01-dataset-landscape.md`。
>
> 誠實原則：能維持就維持——若舊資料集仍是該任務最佳選擇，我直說「維持」，不為換而換。真正需要換的只有兩類軸：**unseen-generator 軸**（D1/D3）與 **fake 生成器世代**（D2/D4）。訓練種子、載體語音、watermark 家族多半維持。

---

## D1｜分布偏移下語音深偽偵測的選擇性預測基準

### 現用舊資料集（定稿 §5.1）
- 訓練種子：**ASVspoof 2019 LA train+dev**（2019，in-domain 種子）
- 評估池（各分層抽 20k）：ASVspoof 2019 LA eval、**ASVspoof 2021 DF eval**（2021）、**MLAAD v5**（unseen-generator 廣度）
- In-the-Wild 全集（2022，unseen 真實流通）
- 通道軸自建 C_clean / C_celp / C_neural；可選 C_rtc = RTCFake

### 建議替換

**(A) unseen-generator 軸（核心，必換）：ASVspoof 2021 DF + MLAAD v5 → 換上 2024–2025 世代四件套**
- **DFADD（2024，HuggingFace）**：diffusion + flow-matching TTS——2019/2021 完全沒有的生成範式，是「generator-shift」最精準的新負領土格。
- **CodecFake+（2025，HuggingFace）**：neural-codec-based 生成世代，補上「codec 既是攻擊也是通道」的 shift 格。
- **SpeechFake 開源部（2025，HuggingFace，Apache 2.0）**：30 開源工具、2024–2025 TTS/VC/vocoder，一站式擴充 unseen 廣度，取代 MLAAD v5。
- **MLAAD v10（2025）**：若要保留 MLAAD 血統，直接升版（v5→v10，175 TTS / 54 語）而非停在 v5。
- **Deepfake-Eval-2024（2025，GitHub）→ eval-only 錨**：唯一「攻擊分布＝2024 真實流通」的公開集，SOTA 音訊 AUC 掉 48%；音訊僅 56.5h，整段當一個 eval 格。**僅作 eval-only，不進訓練、不當可散布訓練集**（scrape 內容散布受限）。

**(B) 訓練種子（可選，非必須）：ASVspoof 2019 LA → 可選升 ASVspoof 5 train（2024）**
- 誠實建議：**訓練種子維持 ASVspoof 2019 LA 為主**。它定義「in-domain 種子分布」，是社群公認的復現基準；換掉會改變 in-domain 的科學意義，且 D1 的貢獻在「shift 下棄權可靠性」，種子新舊不是承重點。**ASVspoof 5 train（抽 20k）列為可選對照**，供想讓 in-domain 種子也升到 crowdsourced 多裝置世代的學生選用——方法一行不改。

### 通過五項驗收（以核心 unseen 四件套為準）
- **更新**：DFADD 2024、CodecFake+ 2025、SpeechFake 2025、MLAAD v10 2025、Deepfake-Eval-2024 2025——全部晚於現用的 2021 DF / MLAAD v5。
- **可取得**：DFADD / CodecFake+ / SpeechFake 開源部 / MLAAD v10 皆 🟢 HuggingFace 直接下載（SpeechFake 開源部 Apache 2.0）；Deepfake-Eval-2024 🟡 GitHub 公開但 eval-only、再散布受限。ASVspoof 5 train 🟢 Zenodo（14498691）直接下載。
- **算力相容**：每個新集一律**分層抽 20k**，總評估池規模與定稿 ≈9.2 萬筆同量級，GPU-hour 430–520 不變；Deepfake-Eval-2024 音訊 56.5h 可整段當一格，不放大。
- **契合原方法**：全部是「把餵進同一條『一次前向→快取 logits+pooled embedding』管線的 fake 換成更新世代」，`s / g / R–C` 三物件、6 機制、3 RQ 一個都不動。generator 軸只是換 cell 內容。
- **時效性論證**：讓「unseen shift」是 2024–2025 的 diffusion/FM 與真實流通世代而非 2021 生成器，負領土地圖才反映 2026 攻擊者手上的工具，而非五年前的。

### 紅線註
SpeechFake 商用 API 子集（10 家閉源）**不釋出**，只用開源部；閉源商用世代維持定稿「不自建」，唯一入口是 Deepfake-Eval-2024（eval-only）。

---

## D2｜真實通道上音訊深偽反制訊號的樂觀偏差審計

### 現用舊資料集（定稿 §五）
- bona fide：ASVspoof 2019 LA real / In-the-Wild real / MLAAD real
- fake：**XTTS-v2 / VITS / YourTTS**（2022–2023 開源 TTS）
- 20k 分層抽樣池
- 真實通道錨：**RTCFake（定稿當「月 0 才知能否取得」的單點故障）**
- watermark：AudioSeal 單一；模擬臂 Opus + AMR-WB

### 建議替換

**(A) RTCFake：維持——但「解除風險」而非「換新」**
- RTCFake（2026，ACL 2026）已確認 **HuggingFace `JunXueTech/RTCFake` 公開可下載**，~600h、真實 RTC 傳輸（Zoom 等）、offline/online 精確配對。定稿把它當「月 0 go/no-go 單點故障」，事實層它可直接下載——D2 最大風險下降。**仍保留月 0 確認學術重散布條款**（授權未明標）。這不改任何 RQ，只把「可能拿不到」的假設校正為「可下載、待確認散布條款」。

**(B) fake 生成器：XTTS-v2/VITS/YourTTS → 補 2024–2025 世代開源 fake**
- 反制訊號（偵測器分數、AudioSeal bit）要在 **2024–2025 世代 fake** 上測存活，量出的 γ 才是 2026 的「反制訊號折扣係數」。建議 fake 池補入 **CodecFake+（2025）** 與 **SpeechFake 開源部（2025）** 的分層樣本，取代或補充 2022–2023 三家。

**(C) bona fide real 類：可選補 SpoofCeleb（2024）——備選**
- SpoofCeleb（2024，VoxCeleb1 衍生，in-the-wild 真實錄音 + 23 當代 TTS）是比 ASVspoof19 real 更貼近真實錄音條件的 real/fake 同源配對。**但受 VoxCeleb 非商用研究授權約束、再散布受限，列為備選**，不當主力；主力維持公開 real 類。

### 通過五項驗收
- **更新**：RTCFake 2026、CodecFake+ 2025、SpeechFake 2025、SpoofCeleb 2024——全部晚於現用 2022–2023 fake。
- **可取得**：RTCFake 🟢 HuggingFace（散布條款月 0 確認）；CodecFake+/SpeechFake 開源部 🟢 HuggingFace；SpoofCeleb 🟡 VoxCeleb 衍生授權（備選）。
- **算力相容**：全走既有 20k 抽樣池，~510 GPU-hour、~30 通道條件不變；watermark 仍 AudioSeal 單一。
- **契合原方法**：審計台「灌探針→過通道→量差分存活」完全不動，只換灌進去的 fake 世代與確認 RTCFake 可得性；不新增探針、不新增管線。
- **時效性論證**：γ 是「今天這批模型 + 真實 RTC 通道」的量測，fake 世代升到 2024–2025 才讓「通道折扣係數」對 2026 的反制部署有參考價值。

### 紅線註
RTCFake 散布條款維持月 0 go/no-go；SpoofCeleb 受原授權約束不可自由再散布。

---

## D3｜被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖

### 現用舊資料集（定稿 §五）
- **ASVspoof 2019 LA / 2021 DF**（20k 確認池 / 10k 搜尋池）
- In-the-Wild、**MLAAD**（unseen-generator 軸分層抽樣）
- laundering 動作空間：EnCodec/DAC + Opus/AMR-NB/G.711/MP3/AAC
- 偵測器：AASIST / RawNet2 / XLS-R backend / Mahalanobis-on-SSL baseline

### 建議替換（本方向是最該換的，且換得最契合）

**(A) laundering 對象 + neural-codec 世代：CodecFake+（2025）為核心新資料**
- **CodecFake+（2025，HuggingFace）** 與 D3 的 **RQ2「neural codec transcode 是不可逆必殺動作」直接同構**——它是 31 開源 neural codec + 17 codec-based 生成系統的最大公開集。把「codec 世代生成器」從假想威脅變成**可實測的 2025 世代 fake**，讓 laundering 的攻擊對象、以及「neural codec 既是攻擊也是通道」的論證從紙上落到資料上。

**(B) unseen-generator 軸：MLAAD → 補 DFADD（2024）+ SpeechFake 開源部（2025）**
- **DFADD（2024）**：diffusion/FM 世代，是 laundering 搜尋要打穿的新一格。
- **SpeechFake 開源部（2025）**：一站式擴充 2024–2025 生成廣度。

**(C) in-domain 種子：ASVspoof 2019/2021 → 可選升 ASVspoof 5（2024）**
- ASVspoof 5（2024，Zenodo）crowdsourced + 首次內建 neural codec 條件 + 首次含 adversarial 攻擊，可同時當更新的種子與 unseen 對象。**列為可選**：D3 承重錨是「物理可逆性下界」（資訊理論事實，不過期），種子新舊非承重；想升就抽 20k 換入，方法不改。

### 通過五項驗收
- **更新**：CodecFake+ 2025、DFADD 2024、SpeechFake 2025、ASVspoof 5 2024——全部晚於 2019/2021 + MLAAD。
- **可取得**：CodecFake+ / DFADD / SpeechFake 開源部 🟢 HuggingFace；ASVspoof 5 🟢 Zenodo。全部非申請制。
- **算力相容**：維持 **20k 確認池 / 10k 搜尋池**，greedy depth≤3、動作空間≤8、610 GPU-hour 不變；新集分層抽樣後不放大搜尋規模。
- **契合原方法**：laundering 動作空間、可控植入可逆性標註、greedy 搜尋協定完全不動——只是搜尋要打穿的「偵測器 + 樣本」換成 2025 世代 fake。CodecFake+ 尤其讓 RQ2 的 neural codec 論證有原生資料支撐，不需改一行方法。
- **時效性論證**：laundering 對象是 2025 codec 世代 fake、neural codec 不可逆論證錨在 CodecFake+ 的真實 codec-based 生成，攻擊成本上界地圖才反映 2026 攻擊者一行指令就能做的洗白。

### 紅線註
維持 ffmpeg-native + HF 開源動作空間，不編 EVS/AMR-WB 專利碼（定稿已砍）；neural codec 動作只在抽樣池上。

---

## D4｜詐騙現場條件下語音深偽偵測的評估效度審計（繁中）

### 現用舊資料集（定稿 §五）
- 話術腳本：~165 條反詐公開話術（自建，維持）
- bona fide：Common Voice zh-TW / AISHELL / 公開廣播 + ASVspoof/In-the-Wild real（維持）
- fake：**純 2 家開源情緒可控 TTS/VC（情緒可控 VITS 系 / OpenVoice 類）**（2022–2023 世代）
- 通道：offline codec（AMR-WB/EVS/Opus + EnCodec/DAC）
- 品質協變量：UTMOS + ECAPA speaker similarity

### 建議替換

**(A) 自建定位：維持——這是唯一正確做法**
- **誠實核心事實：目前沒有公開的繁體中文 / 台灣國語（zh-TW）deepfake 語音資料集。** 中文可得的只有 zh-CN（大陸普通話）。因此 **D4 自建語料的定位完全正確、不變**。本輪能更新的只有「fake 生成器世代」，不是「找到現成 zh-TW 集」。

**(B) fake 生成器：VITS/OpenVoice 類 → 2025 世代 zh 開源可控情緒 TTS**
- 換上 **CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2**（2024–2025 開源、zh-capable、情緒/韻律可控）。「到達耳朵的三秒」要用 2025 能產生哭腔/急迫的當代 zh TTS，才代表 2026 詐騙工具手上的生成能力。**仍維持「純 2 家開源」的定稿約束**——只升世代，不加家數、不加閉源臂。

**(C) 對照臂：補 SpeechFake ZH / CFAD（zh-CN）——備選、僅佐證**
- **SpeechFake ZH 子集（2025，Apache 2.0）** 與 **CFAD（2024，zh-CN）** 作「非 zh-TW 對照臂」，佐證落差非單一腔調 artifact。**須明標外部效度限制**（腔調為 zh-CN，非 zh-TW）；只作對照，不當主力，不改 D4 方法論。

### 通過五項驗收
- **更新**：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 皆 2024–2025，晚於 2022–2023 的 VITS/YourTTS/OpenVoice；SpeechFake 2025、CFAD 2024。
- **可取得**：2025 世代 zh 開源 TTS 🟢 GitHub/HuggingFace 直接下載；SpeechFake ZH 🟡（Apache 2.0 開源部，腔調限制）；CFAD 🟡（zh-CN 公開）。
- **算力相容**：GPU ≈ 180 不變（全場最寬鬆）；對照臂只抽樣佐證，不放大主實驗。
- **契合原方法**：「多軸分層 × 品質協變量標註 × frozen 偵測器 fixed-FPR recall，讀三次（彙總/分層/配對）」完全不動；只換 fake 生成器與 go/no-go 對象。**月 0–1 情緒 zh-TW TTS 硬 go/no-go 關卡照舊**（新世代 TTS 反而更可能通過台灣國語哭腔/急迫測試）。
- **時效性論證**：詐騙現場的 fake 用 2025 世代 zh TTS 生成，量出的評估落差才代表 2026 真實詐騙工具，而非兩三年前的合成品質。

### 紅線註
維持「純 2 家開源、不加閉源臂」；zh-CN 對照臂須標外部效度限制，不得升格為主力；自建定位不因對照臂存在而動搖。

---

## D5｜詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

### 現用舊資料集（定稿 §五）
- 載體語音：AISHELL-3 + LibriSpeech + ASVspoof19 / In-the-Wild real（10k 池）
- watermark：AudioSeal / WavMark / SilentCipher（全開源 learned watermark）
- 通道：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC）× PLR；neural codec（EnCodec/DAC/SpeechTokenizer）× bitrate
- baseline：**AudioMarkBench（2024）**

### 建議替換（本方向多數維持，只補一個前作錨）

**(A) 載體語音：維持**
- 載體 real 語音的年份**不影響 watermark 容量量測**（它只是承載 payload 的宿主）。AISHELL-3 / LibriSpeech 維持，無需更換。

**(B) watermark 家族：維持**
- AudioSeal / WavMark / SilentCipher **是當前開源可得的全部** learned watermark，無更新替代品。SynthID-audio 非全開源，維持定稿「不納入預設、僅文獻代理」。

**(C) baseline：AudioMarkBench（2024）→ 補「Will They Survive Neural Codecs?」（2025, Interspeech）**
- **「Will They Survive Neural Codecs?」（Interspeech 2025，arXiv 2505.19663）正是 D5 主題（watermark × neural codec）的最新前作**。把 D5 的 baseline 從「只有 AudioMarkBench（2024，只做模擬擾動）」升級為「AudioMarkBench + Will They Survive Neural Codecs（2025）」，讓「第一張可靠 bit 容量地圖」的定位更精準——相對前作補上「可控植入 ground-truth 錨 + 索引構造」。

**(D) neural codec 世代：可參 CodecFake+（2025）**
- neural codec 通道的世代參考可對照 **CodecFake+（2025）** 的 codec 清單，讓「容量塌陷點」論證錨到 2025 最大 neural codec 集。**這是參考錨，不是換載體**——通道矩陣（EnCodec/DAC/SpeechTokenizer）維持。

### 通過五項驗收
- **更新**：baseline 補 2025 Interspeech 前作，晚於 2024 的 AudioMarkBench；CodecFake+ 2025 世代參考。
- **可取得**：Will They Survive Neural Codecs 🟢 論文/repo；CodecFake+ 🟢 HuggingFace；watermark checkpoint 🟢 官方 repo。
- **算力相容**：watermark 家族不變、~10k 載體池不變、通道矩陣不變，GPU ≈ 220 不變。補前作是文獻定位工作，零額外 GPU。
- **契合原方法**：唯一一條「embed→通道 transcode→recover→可控植入校準」pipeline 完全不動；只是把 baseline 對照與 neural codec 世代錨到 2025 最新前作。
- **時效性論證**：把 D5 的容量塌陷點論證錨到 2025 最新「watermark × neural codec」前作，讓「neural codec 通道容量逼近 0」的資訊理論邊界對照到當代 codec，Article 50 可讀性判決更貼近 2026 生效時的真實通道。

### 紅線註
watermark 家族已是開源全集，不硬撐「傳統 vs neural 分類學」（定稿已收窄）；SynthID 維持不納入；載體語音維持不換。

---

## 正式題目提議（僅對我最有把握的 2 個方向：D1、D3）

> 選 D1、D3 的理由：這兩個方向的資料集替換最徹底（unseen-generator 軸整軸更新），題目又最需要脫去花俏破折號金句、正式化為學位論文慣例。其餘三個方向的題目正式化，交由 H（指導教授）與其他角色把關更妥。

### D1 正式題目
- **花俏原題**：《不知道就別答——分布偏移下語音深偽偵測的選擇性預測基準》／ *Abstain When Unsure: A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*
- **正式中文**：《分布偏移下語音深偽偵測之選擇性預測基準研究》
- **正式英文**：*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Distribution Shift*
- 正式化說明：去除「不知道就別答」口語金句與破折號；主標即研究對象，符合學位論文慣例；英文保留 selective-prediction / shift-aware 領域術語，補明 shift 的兩個來源（generator / channel）。

### D3 正式題目
- **花俏原題**：《攻擊者付的絕不超過多少——被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖》／ *What Does the Attacker Pay at Most? An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- **正式中文**：《被動語音深偽偵測之 adaptive-laundering 攻擊成本上界地圖》
- **正式英文**：*An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- 正式化說明：去除「攻擊者付的絕不超過多少」問句金句；保留 adaptive-laundering 專有術語與「攻擊成本上界地圖」核心貢獻；英文去問句、直陳研究交付物。

---

## 回傳一行版（舊→新）＋正式題目

**逐方向「舊→新」一行版：**
- **D1**：ASVspoof 2021 DF + MLAAD v5（unseen 軸）→ DFADD(2024) + CodecFake+(2025) + SpeechFake 開源部(2025) + MLAAD v10(2025)，並以 Deepfake-Eval-2024(2025) 當 eval-only 錨；訓練種子 ASVspoof 2019 LA 維持（ASVspoof 5 train 可選）。
- **D2**：RTCFake 從「月 0 才知能否取得的單點故障」→ 校正為「HuggingFace 公開可下載、僅待確認散布條款」（降風險非換新）；fake XTTS/VITS/YourTTS → 補 CodecFake+(2025) + SpeechFake 開源部(2025)；real 類可選補 SpoofCeleb(2024, 備選)。
- **D3**：ASVspoof 2019/2021 + MLAAD（laundering/unseen 對象）→ 核心換 CodecFake+(2025，與 RQ2 neural codec 同構) + DFADD(2024) + SpeechFake 開源部(2025)；in-domain 種子可選升 ASVspoof 5(2024)。
- **D4**：fake VITS/OpenVoice 類(2022–2023) → 2025 世代 zh 開源可控情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）；補 SpeechFake ZH / CFAD 作 zh-CN 對照臂(備選)；**自建 zh-TW 定位維持不變（無現成 zh-TW 集）**。
- **D5**：baseline AudioMarkBench(2024) → 補「Will They Survive Neural Codecs?」(Interspeech 2025) 為直接前作，neural codec 世代可參 CodecFake+(2025)；**載體語音、watermark 家族、通道矩陣全維持**。

**我提議的正式題目（D1、D3）：**
- D1：《分布偏移下語音深偽偵測之選擇性預測基準研究》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Distribution Shift*
- D3：《被動語音深偽偵測之 adaptive-laundering 攻擊成本上界地圖》／ *An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*

**紀律自檢**：無加實驗、無加 RQ、無加 deliverable；所有新集沿用 20k 分層抽樣、GPU-hour 全部維持定稿（D1 430–520 / D2 510 / D3 610 / D4 180 / D5 220）；每個替換皆「換餵進同一條管線的 fake/通道世代」，零方法論變更；閉源商用世代維持不自建。
