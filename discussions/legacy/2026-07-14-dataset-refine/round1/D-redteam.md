# Round 1 資料集提議：紅隊（Agent D）
日期：2026-07-14

> 紅隊視角的一句話立場：**舊資料集的生成器，攻擊者 2023 年就淘汰了。用 ASVspoof 2019/2021、MLAAD v5、XTTS/VITS/YourTTS 去量「攻擊面」，等於拿考古題估 2026 的敵情。** 但換新不是無腦換——換錯地方會讓某個方向的攻擊面「看起來被守住了，其實是因為敵人拿的還是舊槍」。本文對每個方向不只提「換什麼」，更誠實標出「換了會不會讓攻擊面評估過度樂觀」這一紅隊專屬欄位。
>
> 紀律自檢：本文**只換餵進管線的 fake/通道世代，不動任何 RQ、方法、實驗軸、算力設計**。所有大型新集一律沿用定稿既有的 20k 分層抽樣。凡我想到「順便多比一個生成器」的地方，一律壓回 future work。

---

## 通則：紅隊為什麼在意生成器世代

攻擊面評估有一個不對稱陷阱：**偵測器對舊生成器的失效，攻擊者早就不 care 了；偵測器對新生成器的失效，才是 2026 真實的攻擊入口。** 三個具體後果貫穿五個方向：

1. **「confident-real 攻擊面」在舊 fake 上被低估**：2025 世代 diffusion/FM 與 neural-codec TTS 天生就更接近 human-parity，不需任何對抗介入就已經落在 confident-real 區。用 2021 fake 量「把 fake 推進 confident-real 要付多少成本」，會把攻擊成本估高——因為新 fake 是**免費**就到那裡了。
2. **「攻擊成本上界」在舊 fake 上被高估**：新 fake 需要更少的 laundering 就能打穿偵測器。用舊 fake 量攻擊成本，會讓防守方誤以為攻擊很貴。
3. **反過來的過度樂觀**：如果把**訓練種子**也升級（例如把 ASVspoof5 的 adversarial + neural codec 條件餵進訓練），偵測器等於被預先接種，量出來的 unseen gap 與攻擊面會人為縮小——這是紅隊最要防的「換資料換到自己騙自己」。

紅隊的總原則：**fake/eval 側盡量換到 2025 世代（讓敵情真實）；訓練種子側保守（保留 shift 的誠實）。**

---

## D1｜分布偏移下語音深偽偵測的選擇性預測基準

### 現用舊資料集
- ASVspoof 2019 LA train+dev（訓練種子，2019）
- ASVspoof 2019 LA eval（in-domain 對照格，抽 20k）
- ASVspoof 2021 DF eval（unseen 對象，抽 20k）
- In-the-Wild（unseen real，全集 31,779）
- **MLAAD v5**（unseen-generator 廣度，抽 20k，2023）
- 通道軸 `C_neural`：EnCodec transcode

### 建議替換

**A. unseen-generator 軸（承重換點）：ASVspoof 2021 DF + MLAAD v5 → DFADD（2024）+ CodecFake+（2025）+ SpeechFake 開源部（2025），並把 In-the-Wild 的角色補上 Deepfake-Eval-2024（2025）當 eval-only 真實流通錨。**

這是 D1 全篇最該換的一格。RQ1 的「負領土地圖」與 RQ3 的「confident-real 攻擊面」都建立在 unseen 格上——這些格必須裝 2025 世代 fake，否則畫出來的是「2021 攻擊者的負領土」，對 2026 部署方無參考價值。

**B. 訓練種子 ASVspoof 2019 LA：維持不換（紅隊主張保守）。**

地景文件把 ASVspoof 5 train 列為「可選升級」。**紅隊在此明確主張維持 2019 LA**，理由是攻擊面誠實性：ASVspoof 5 內建 adversarial 攻擊與 neural codec 條件，若拿它當訓練種子，偵測器等於被預先接種了 neural codec 與對抗樣本的免疫力——RQ1 量到的 unseen gap 會人為縮小、RQ3 的 confident-real 攻擊成本會人為升高，**攻擊面評估變得過度樂觀**。2019 LA 定義的「乾淨、未接種的 in-domain 種子」，正是讓 shift 保持誠實的錨。（若指導教授堅持要當代訓練種子，ASVspoof 5 train 只能當**額外對照臂**，不能取代 2019 LA 主線——但那已是加實驗，本輪不做。）

### 通過五項驗收（承重換點 A）

| 資料集 | 更新 | 可取得 | 算力相容 | 契合原方法 | 時效性論證（一句話） |
|---|---|---|---|---|---|
| **DFADD** | 2024-09（ICASSP 2025） | HuggingFace（github isjwdu/DFADD），開源，中小型數 GB | 分層抽 20k，遠小於既有池 | 直接當 unseen 格的 fake 來源，`s×g×R–C` 介面一行不改 | diffusion/FM TTS 是 2019/2021 完全沒有的生成範式，SOTA 偵測器對它明顯失效——這才是 2026 攻擊者手上的槍 |
| **CodecFake+** | 2025-01 | HuggingFace CodecFake/CodecFake_Plus_Dataset，開源，大→抽樣 | 分層抽 20k | 當 unseen 格 fake + 同時服務 `C_neural` 通道軸的真實錨 | neural-codec 生成世代讓「neural codec 既是通道也是攻擊」從假想變可測 |
| **SpeechFake 開源部** | 2025-07（ACL 2025） | HuggingFace DeepFense/SpeechFake，**Apache 2.0**（僅開源部；10 家商用 API 子集不釋出），>TB→抽樣 | 分層抽 20k | 一站式 2024–2025 TTS/VC/vocoder unseen 廣度，取代 MLAAD v5 | 30 種 2024–2025 開源工具，是 unseen-generator 廣度最省事的當代更新 |
| **Deepfake-Eval-2024** | 2025-03 | GitHub（eval-only，scrape 內容**再散布受限**），音訊 56.5h | 56.5h 可整段當一個 eval-only 格，零抽樣壓力 | 只讀 R–C 曲線，不進訓練，不改方法 | 唯一「攻擊分布＝2024 真實社群流通」的公開錨；SOTA 在其上 audio AUC 掉 48%，是「舊 benchmark 結論已過期」的鐵證 |

（MLAAD 若要保留一格，升到 **v10（2025，175 TTS/54 語，deepfake-total.com/mlaad，抽 20k）**，但 DFADD+CodecFake++SpeechFake 已覆蓋，MLAAD 可退為廣度補充。）

### 紅隊專屬欄：換新後攻擊面是否更真實 / 是否過度樂觀
- **更真實**：✅ RQ3 的 `max P(confident-real|fake)` 一旦用 2025 diffusion/codec fake 量，會揭露一件舊 benchmark 藏起來的事——**這些 fake 不需要任何 laundering 或 PGD，出廠就落在 confident-real 區**。這正是無綠燈原則要對抗的最危險失效，用舊 fake 根本量不到。
- **過度樂觀風險**：⚠️ 唯一的樂觀陷阱在訓練種子（見上，已用「維持 2019 LA」擋掉）。fake/eval 側全換新只會讓攻擊面更嚴峻、更真實，不會過度樂觀。

---

## D2｜真實通道上音訊深偽反制訊號的樂觀偏差審計

### 現用舊資料集
- bona fide real：ASVspoof 2019 LA real / In-the-Wild real / MLAAD real
- **fake：XTTS-v2 / VITS / YourTTS（3 家開源，2022–2023）**
- 抽 20k
- 真實通道錨：RTCFake（2026，定稿把它當「月 0 才知能否取得」的單點故障）
- watermark：AudioSeal
- 模擬 codec：Opus / AMR-WB

### 建議替換

**A. fake 生成器：XTTS-v2 / VITS / YourTTS → CodecFake+（2025）+ SpeechFake 開源部（2025）世代 fake。**

D2 量的是「反制訊號（偵測器分數、AudioSeal bit）在真實通道 vs 模擬通道的存活落差 γ」。RQ1 的 γ 是「今天這批偵測器在今天的 fake 上」的量測——若 fake 停在 2022–2023，量到的 γ 是對舊 fake 的通道折扣，2026 部署方拿去消費會系統性失準。換成 2025 世代 fake，γ 才是「2026 攻擊者的反制訊號折扣係數」。

**B. RTCFake：維持，且解除單點故障定位（好消息不是換新）。**

地景文件已確認 RTCFake 在 HuggingFace `JunXueTech/RTCFake` 公開可下載、~600h、真實 RTC 傳輸、offline/online 精確配對。定稿把它當「月 0 才知能否取得的單點故障」是過度悲觀——**事實上它可直接下載，D2 最大風險就此下降**。維持月 0 確認學術重散布條款（散布條款未明標），但 go/no-go 的失敗機率大幅降低。

**C. watermark AudioSeal：維持。** 它是開源可自由嵌入/偵測的 SOTA localized watermark，沒有更新的可替代品（SynthID 非第三方可用，已砍）。

### 通過五項驗收

| 資料集 | 更新 | 可取得 | 算力相容 | 契合原方法 | 時效性論證 |
|---|---|---|---|---|---|
| **CodecFake+** | 2025-01 | HF，開源，大→抽樣 | 併入既有 20k 抽樣池 | 當 fake 探針源，灌進同一台審計台，管線不變 | 反制訊號要在 2025 neural-codec 世代 fake 上測存活，γ 才是 2026 的折扣係數 |
| **SpeechFake 開源部** | 2025-07 | HF，Apache 2.0（開源部），→抽樣 | 併入 20k 抽樣池 | 同上，換 fake 不換探針 | 30 種 2024–2025 開源 TTS/VC，取代 3 家 2022–2023 老生成器 |
| **RTCFake（維持）** | 2026（ACL 2026） | HF JunXueTech/RTCFake，**公開可下載**，~600h | 抽樣池 20k | 已是核心錨，無需換 | 唯一「真實黑箱 RTC 通道＋offline/online 配對」公開大集，D2 存在的理由 |

### 紅隊專屬欄：換新後攻擊面是否更真實 / 是否過度樂觀
- **更真實**：✅ 舊 fake 的生成 artifact 較粗，偵測器在乾淨條件本來就抓得動，通道劣化後的 recall 落差 γ 反而好看。2025 fake 出廠就更難抓，通道再一劣化，**γ 會更嚴峻也更誠實**。
- **過度樂觀風險**：⚠️ 一個需要監控的點——RQ2 的 AudioSeal watermark bit 存活是量「載體語音上的浮水印過通道」，**與 fake 生成器世代無關**（浮水印嵌在載體上，不在 fake 上）。所以換 fake 世代**不影響 RQ2**，只影響 RQ1/RQ3 的偵測器探針。這不是問題，是要在寫作時講清楚：換 fake 世代只更新被動探針軸，主動探針軸（watermark）的時效性由 AudioSeal 本身承載。

---

## D3｜被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖（紅隊本命方向）

### 現用舊資料集
- ASVspoof 2019 LA / 2021 DF（抽 20k 確認池 / 10k 搜尋池）
- In-the-Wild、MLAAD（unseen-generator 軸）
- laundering 工具鏈：EnCodec / DAC + Opus / AMR-NB / G.711 / MP3 / AAC
- 偵測器：AASIST / RawNet2 / XLS-R backend / Mahalanobis-on-SSL baseline

### 建議替換

**A. laundering 的攻擊對象（被打穿的 fake）：ASVspoof 2019/2021 → CodecFake+（2025）+ DFADD（2024）+ SpeechFake 開源部（2025）；ASVspoof 5（2024）取代 2019/2021 種子池。**

這是紅隊最在意的一格。攻擊成本地圖問的是「攻擊者讓偵測器失效最便宜付多少」——若被 laundering 的 fake 是 2021 世代，量出來的攻擊成本是**對舊 fake** 的成本。2026 攻擊者拿的是 CodecFake+/DFADD 世代的 fake，它們**更接近 bona fide、需要更少 laundering 就能打穿**，真實攻擊成本更低。用舊 fake 量會系統性高估攻擊成本，讓防守方誤判「攻擊很貴、還有戲」。

**B. RQ2 的核心資產（neural codec 不可逆必殺動作）：CodecFake+ 直接強化。**

RQ2 認證「neural codec transcode 是零金錢、物理不可逆的必殺動作」。CodecFake+ 是 31 開源 neural codec + 17 codec-based 生成系統的最大公開集——**它把「neural codec 世代」從 D3 的假想威脅變成可實測的 fake 來源與 laundering 目標**，讓「neural codec 既是攻擊也是不可逆通道」的資訊理論論證有真實 2025 世代 fake 撐腰。

**C. laundering 工具鏈本身：維持。** ffmpeg-native codec + EnCodec/DAC 已覆蓋「常見有損通道 codec」，這是 laundering **動作空間**，不是 fake 資料集，年份不影響（EnCodec/DAC 仍是當前主流 neural codec）。

### 通過五項驗收

| 資料集 | 更新 | 可取得 | 算力相容 | 契合原方法 | 時效性論證 |
|---|---|---|---|---|---|
| **CodecFake+** | 2025-01 | HF CodecFake/CodecFake_Plus_Dataset，開源，大→抽樣 | 抽 20k 確認 / 10k 搜尋（沿用） | 當被 laundering 的 fake + neural codec 世代錨，greedy 搜尋協定不變 | RQ2「neural codec 必殺」對上真實 codec 世代 fake，不再是假想威脅 |
| **DFADD** | 2024-09 | HF（github isjwdu/DFADD），開源，數 GB | 抽 20k / 10k | 當 laundering 對象，動作空間與成本代理不變 | diffusion/FM fake 是 2019/2021 沒有的範式，攻擊成本要對它重量 |
| **SpeechFake 開源部** | 2025-07 | HF，Apache 2.0（開源部），→抽樣 | 抽 20k / 10k | 同上 | 2024–2025 unseen-generator 廣度，攻擊成本地圖才覆蓋當代 |
| **ASVspoof 5** | 2024 | Zenodo 14498691，研究用途非申請制，數百 GB→抽樣 | **強制抽 20k**（全集會燒光預算） | 取代 2019/2021 種子池，離線量測不變 | crowdsourced 非棚錄＋內建 neural codec＋首含 adversarial，種子與 unseen 對象同升 2024 世代 |

### 正式題目提議（紅隊本命，最有把握）

- **中**：《被動語音深偽偵測之適應性洗白攻擊成本上界地圖》
- **英**：*An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*

（正式化處理：刪去花俏問句「攻擊者付的絕不超過多少」，保留「攻擊成本上界地圖」這個精確的技術核心；英文沿用定稿副標，刪去 *What Does the Attacker Pay at Most?* 引句。原三 RQ、greedy 搜尋協定、可逆性下界標註全部不動。）

### 紅隊專屬欄：換新後攻擊面是否更真實 / 是否過度樂觀
- **更真實**：✅✅ 這是全五方向換新後**攻擊面最誠實化**的一個。換上 2025 fake，greedy 搜尋會找到「更短、更便宜」的打穿配方——正是紅隊要揭露的：**攻擊比舊 benchmark 說的更便宜**。攻擊成本上界會下降，這不是壞消息，是真相。
- **過度樂觀風險**：⚠️ 一個要防的技術細節——CodecFake+ 的 fake **本身已是 codec-based 生成**，對它再套 neural codec transcode 是「double-codec」情境，可逆性標註要確認不被生成端的 codec 污染（可控植入實驗要以「植入已知 artifact → 過 laundering 動作」為準，不受 fake 生成端 codec 影響，方法上本來就成立）。此外 ASVspoof 5 若當種子池，其內建 adversarial 條件不可外洩進 laundering 動作空間的評估（否則攻擊面被接種而樂觀）——維持「種子只用其乾淨 spoof 子集，adversarial 條件不進 laundering 評估」即可。

---

## D4｜詐騙現場條件下語音深偽偵測的評估效度審計（繁中）

### 現用舊資料集
- 話術腳本 ~165 條（公開反詐/刑事局）
- bona fide：Common Voice zh-TW / AISHELL / 公開廣播 / ASVspoof / In-the-Wild real
- **fake：純 2 家開源情緒可控 TTS/VC（情緒可控 VITS 系 / OpenVoice 類 + VC，2022–2023）**
- 通道：AMR-WB / EVS / Opus + EnCodec / DAC
- 自建 ~2–3 萬筆

### 建議替換

**A. fake 生成器（承重換點）：情緒可控 VITS / OpenVoice → 2025 世代 zh 開源可控情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）。**

這是紅隊對 D4 最強的主張。D4 的整篇論文賭在「詐騙現場那三秒（哭腔、急迫命令）」——**而 2022–2023 的 VITS/YourTTS/OpenVoice 根本產不出可信的台灣國語哭腔與急迫**。用它們當 fake，等於用 2023 的爛哭腔去代表 2026 詐騙集團手上的工具。2025 世代的 CosyVoice 2 / F5-TTS / GPT-SoVITS 才是當代詐騙工具的真實能力上界。**這個換點直接決定 D4 的外部效度是否成立。**

**B. 對照臂：補 SpeechFake ZH 子集（2025）/ CFAD（2024）作 zh-CN 對照，佐證落差非單一腔調 artifact。**

**C. 主力仍為自建：維持（無現成 zh-TW deepfake 集，這是事實）。** 繁中無現成 deepfake 集，D4 的自建定位不變、依然正確——本輪只換 fake 生成器世代，不改自建方法論。

### 通過五項驗收

| 資料集 | 更新 | 可取得 | 算力相容 | 契合原方法 | 時效性論證 |
|---|---|---|---|---|---|
| **CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2** | 2024–2025 | 皆開源（HF / GitHub），自建生成 | 自建 ~2–3 萬筆，生成成本 10–40 GPU-h（沿用） | 純換 fake 生成器，「多軸分層 × 品質配對」框架不變 | 2025 能產哭腔/急迫的當代 zh TTS，才代表 2026 詐騙集團的真實工具 |
| **SpeechFake ZH 子集**（對照） | 2025 | HF DeepFense/SpeechFake，Apache 2.0（開源部） | 抽樣對照臂 | 只作 zh-CN 對照臂，不進主析因 | 佐證落差非 zh-TW 單一腔調 artifact（須標明 zh-CN 外部效度限制） |
| **CFAD**（對照） | 2024 | 公開下載，zh-CN | 抽樣對照 | 同上，背景對照 | 中文 real 類 + 跨腔調對照 |

### 正式題目提議（次有把握——因為它決定生成器世代真實性，紅隊在意）

- **中**：《詐騙情境條件下語音深偽偵測的評估效度審計：一份繁體中文語料研究》
- **英**：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*

（正式化處理：刪去花俏引句「到達耳朵的那三秒」，保留「詐騙情境條件」「評估效度審計」技術核心，並在副標明示「繁體中文語料」這個 D4 的實質貢獻與地域定位。原三 RQ、frozen 前向、fixed-FPR recall、品質配對全部不動。）

### 紅隊專屬欄：換新後攻擊面是否更真實 / 是否過度樂觀
- **更真實**：✅✅ 這是**過度樂觀風險最需要被換新解除**的方向。用 2023 爛情緒 TTS 當 fake，RQ1 的 recall 落差會被「TTS 品質差被抓」污染——RQ3 的品質配對雖然想解耦，但如果 fake 品質天花板本來就低，配對後淨落差會被系統性低估，**讓人誤以為「偵測器對現場其實還好」**。換上 2025 高品質情緒 TTS，fake 是真的好，量到的落差才真的來自「現場條件」而非「生成品質」——**RQ3 的解耦論證因此才站得住**。
- **過度樂觀風險**：無新增。反而是不換才會過度樂觀（低估偵測器對現場的失效）。

---

## D5｜詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

### 現用舊資料集
- 載體語音：AISHELL-3 + LibriSpeech + ASVspoof19 / In-the-Wild real（抽 ~10k）
- watermark：AudioSeal / WavMark / SilentCipher
- 通道矩陣：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC-LC × PLR）+ neural codec（EnCodec/DAC/SpeechTokenizer × bitrate）
- baseline：AudioMarkBench（2024）

### 建議替換

**A. baseline 補「Will They Survive Neural Codecs?」（Özer et al., Interspeech 2025）。**

D5 主題正是「watermark × neural codec 通道」，而 Özer et al.（arXiv 2505.19663，Interspeech 2025）是**這個主題的最新且唯一直接前作**。定稿已在 baseline 提到它作為協定參考，本輪確認扶正為 baseline 對照，讓 D5「第一張可靠 bit 容量地圖」的定位更精準（相對前作補上「可控植入 ground-truth 錨 + 索引構造」）。

**B. neural codec 通道條件：可參照 CodecFake+（2025）的 codec 世代擴充錨。**

CodecFake+ 涵蓋 31 種開源 neural codec——D5 的 neural codec 通道（EnCodec/DAC/SpeechTokenizer）可用它作為「當代 codec 世代覆蓋是否充分」的參照，確認容量塌陷點不是只對三個舊 codec 成立。**但紅隊主張這只作參照，不擴充通道矩陣**（擴充即加實驗，違反本輪禁止）——EnCodec/DAC/SpeechTokenizer 仍是當前主流，三個已足以定出可逆/不可逆塌陷邊界。

**C. 載體語音 AISHELL-3 / LibriSpeech / ASVspoof19 real：維持。** 它們是 watermark 的**載體**，浮水印嵌在乾淨語音上，載體年份不影響容量量測——這是誠實的「維持，因為換了沒有意義」。

**D. watermark 家族 AudioSeal / WavMark / SilentCipher：維持。** 這是當前開源可得的全部 learned watermark，無更新替代品（SynthID 非全開源）。

### 通過五項驗收

| 標的 | 更新 | 可取得 | 算力相容 | 契合原方法 | 時效性論證 |
|---|---|---|---|---|---|
| **Will They Survive Neural Codecs?**（baseline） | 2025（Interspeech 2025） | arXiv 2505.19663 / repo，論文級對照 | 0 GPU（協定/baseline 對照） | 當 baseline 劃界，不改 pipeline | D5 主題的最新且唯一直接前作，把定位錨到已發表基準 |
| **CodecFake+**（通道世代參照） | 2025-01 | HF CodecFake/CodecFake_Plus_Dataset | 僅作參照，不擴通道矩陣 | 不改既有 3 neural codec 設計 | 確認容量塌陷點對 2025 codec 世代仍成立，不只對三個舊 codec |
| 載體/watermark（維持） | — | 皆開源可下載 | ~10k 池不變（GPU≈220） | — | 載體年份不影響容量；watermark 家族已是開源全集 |

### 紅隊專屬欄：換新後攻擊面是否更真實 / 是否過度樂觀
- **更真實**：✅ 補 Özer et al. baseline 讓「neural codec 通道容量塌陷」的論證有 2025 前作背書。
- **過度樂觀風險**：⚠️ 紅隊要標一個攻擊面盲點——D5 量的是「合法者嵌入的 watermark 過通道還剩幾 bit」，這是**防守方視角的 provenance**，不是攻擊面。從紅隊看，真正的攻擊面是「攻擊者主動剝除/覆寫 watermark」，而 D5 定稿明確**不做 watermark removal 攻擊**（那是另一篇）。這不是換資料能解決的，也不該在本輪動——但要在 discussion 誠實標明：**D5 的 bit 容量地圖量的是「被動通道劣化」下限，不是「主動對抗剝除」下限；後者只會更低。** 這一句紅隊註記不改任何實驗，只防止讀者把「被動容量」誤讀成「對抗下的容量」而過度樂觀。

---

## 回傳資料（純文字）

### 五方向「舊→新」一行版（紅隊視角）

- **D1**：unseen 軸 `ASVspoof 2021 DF + MLAAD v5 → DFADD(2024) + CodecFake+(2025) + SpeechFake 開源部(2025) + Deepfake-Eval-2024(2025, eval-only)`；**訓練種子 ASVspoof 2019 LA 維持不換**（換了會預先接種、攻擊面過度樂觀）。
- **D2**：fake `XTTS-v2/VITS/YourTTS(2022–2023) → CodecFake+(2025) + SpeechFake 開源部(2025)`；**RTCFake(2026) 維持並解除單點故障**（已確認公開可下載）。
- **D3**：laundering 對象 `ASVspoof 2019/2021 → CodecFake+(2025) + DFADD(2024) + SpeechFake 開源部(2025)`；種子池 `ASVspoof 2019/2021 → ASVspoof 5(2024, 抽 20k)`；laundering 工具鏈維持。
- **D4**：fake 生成器 `情緒可控 VITS/OpenVoice(2022–2023) → CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2(2024–2025)`；補 `SpeechFake ZH / CFAD` 作 zh-CN 對照；**自建定位維持**（無現成 zh-TW 集）。
- **D5**：baseline 補 `Will They Survive Neural Codecs?(Interspeech 2025)`；neural codec 通道以 `CodecFake+(2025)` 作世代參照（不擴矩陣）；**載體語音與 watermark 家族維持**（換了沒意義／已是開源全集）。

### 我提議的正式題目

- **D3（本命，最有把握）**
  - 中：《被動語音深偽偵測之適應性洗白攻擊成本上界地圖》
  - 英：*An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- **D4（次有把握）**
  - 中：《詐騙情境條件下語音深偽偵測的評估效度審計：一份繁體中文語料研究》
  - 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*

### 紅隊給七位角色的一句提醒
換 fake/eval 世代（讓敵情真實）要積極，換訓練種子（保留 shift 誠實）要保守——**唯一的過度樂觀陷阱不在 fake 太舊，而在把當代 adversarial/neural-codec 條件餵進訓練，讓偵測器被預先接種、攻擊面看起來被守住了。**
