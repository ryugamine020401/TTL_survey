# 五個方向（資料集更新版 + 正式題目）
日期：2026-07-14

> 統整者按：本文閱讀了 `00-constraints.md`（最高指導原則）、`01-dataset-landscape.md`（共用事實依據）、`round1/` 與 `round2/` 全 14 份角色文件、以及 `../2026-07-14-convergence/final/D1–D5.md`（五份定稿）。裁決標準：**只換資料集與題目，其餘一律維持 convergence 定稿。** 凡 Round 2 有兩位以上角色以取得性、方法純度或範圍紀律駁回的提議，一律不採；凡定稿已釘死的結構（grid 格數、fake 家數、動作空間、20k/10k 抽樣、算力上限），一律不動。

---

## 一、本輪改了什麼、沒改什麼

**一句話：** 本輪只做兩件事——把每個方向偏舊（2019–2023）的 fake／unseen／baseline 資料換成 2024–2025 世代的可取得替代品，並把花俏題目正式化為學位論文題目；**三個 RQ 的結構、核心方法、實驗設計、一年時程、失敗退路、社會意義、以及算力硬預算（D1 430–520／D2 510／D3 610／D4 180／D5 220 GPU-h，全部 ≤1,000）全部維持 convergence 定稿不動。** 沒有加任何實驗、RQ、deliverable、對照臂或通道條件；所有大型新集一律沿用定稿既有的 **20k 分層抽樣**（D3 為 20k 確認池／10k 搜尋池；D5 為 ~10k 載體池）。偵測器全部維持**現成 frozen checkpoint**（ASVspoof19 LA 訓練權重），**因此本輪沒有任何一處需要重訓**。

### 五方向資料集新舊對照總表

| 方向 | 舊資料集（換前） | 新資料集（換後） | 年份 | 取得方式 | 時效性理由（一句話） | 抽樣 |
|---|---|---|---|---|---|---|
| **D1** unseen-generator 格 | ASVspoof 2021 DF eval | **DFADD** | 2024 | HuggingFace `isjwdu/DFADD`，MIT，非 gate，**用 2025-04 修正版** | 把「沒見過的生成器」換成 2019/2021 完全沒有的 diffusion／flow-matching 範式，負領土地圖才反映 2026 攻擊者的槍 | 抽 20k |
| **D1** unseen-廣度格 | MLAAD v5 | **MLAAD v10**（主）／SpeechFake 開源部（二選一） | 2025 | MLAAD v10：deepfake-total.com 公開；SpeechFake：HF `DeepFense/SpeechFake`，Apache 2.0 | 把 unseen 廣度從 2023 世代升到 2025，drop-in 同管線、零風險 | 抽 20k |
| **D1** in-domain 種子／In-the-Wild／通道軸 | ASVspoof 2019 LA／In-the-Wild／C_clean·C_celp·C_neural | **維持不換** | — | — | 種子換即重訓（違規）；In-the-Wild 是第一週 smoke-test；通道軸須逐格可控 | — |
| **D2** fake 生成器 | XTTS-v2／VITS／YourTTS（3 家） | **3 家 2025 世代乾淨開源 TTS**（如 F5-TTS／CosyVoice 2／一個 diffusion/FM 生成器；或 SpeechFake 開源部乾淨合成） | 2024–2025 | HuggingFace，開源／Apache 2.0 | 反制訊號折扣係數 γ 要量在 2025 世代 fake 上才是 2026 的折扣 | 抽 20k |
| **D2** 真實通道錨 | RTCFake（定稿：月 0 單點故障） | **RTCFake（維持，風險不解除）** | 2026 | HF `JunXueTech/RTCFake`，**G 實測匿名抓取回 HTTP 401＝gated**，非直接下載 | 非換新而是「維持定稿的悲觀」：仍唯一真實 RTC 錨，但月 0 go/no-go 全額保留 | 抽 20k |
| **D2** real／watermark／模擬臂 | 公開 real／AudioSeal／Opus+AMR-WB | **維持不換** | — | — | real 只是載體不進 γ 一階；AudioSeal 是唯一第三方可用 watermark；模擬臂須逐因子可控 | — |
| **D3** laundering 主對象／確認池 | ASVspoof 2021 DF | **CodecFake+** | 2025 | HF `CodecFake/CodecFake_Plus_Dataset`，**MIT，101 GB，非 gate（G 實測 200）** | 與 RQ2「neural codec 不可逆必殺動作」直接同構——被打的樣本本身即 codec 世代 fake，假想威脅變可實測 | 抽 20k 確認／10k 搜尋 |
| **D3** unseen-generator 軸 | MLAAD | **DFADD** | 2024 | HF `isjwdu/DFADD`，MIT，修正版 | laundering 要打穿的偵測器面對的 fake 升到 diffusion/FM 範式 | 抽 20k／10k |
| **D3** 種子／動作空間 | ASVspoof 2019 LA／ffmpeg+EnCodec/DAC | **維持不換** | — | — | 種子換即重訓；動作空間是工具鏈非資料集，EnCodec/DAC 仍主流 | — |
| **D4** fake 生成器 | 2 家開源情緒 TTS（VITS 系／OpenVoice 類） | **2 家 2025 世代 zh 開源情緒 TTS**（CosyVoice 2／F5-TTS／GPT-SoVITS／OpenVoice v2 選 2） | 2024–2025 | GitHub／HuggingFace 開源 checkpoint，自建生成 | 「到達耳朵的三秒」要用 2025 能產哭腔／急迫的當代 zh TTS 才代表 2026 詐騙工具 | 自建 ~2–3 萬筆 |
| **D4** zh-CN 對照臂（新增備選） | （無） | **SpeechFake ZH／CFAD** | 2024–2025 | HF Apache 2.0（開源部）／CFAD 公開 | 佐證落差非單一 zh-TW 腔調 artifact；**僅對照、標外部效度、不升主軸** | 抽樣佐證 |
| **D4** 自建定位／話術／real／通道（含 EVS）／品質協變量 | 自建 zh-TW／~165 話術／real 類／offline codec／UTMOS+ECAPA | **維持不換** | — | — | 無現成 zh-TW deepfake 集，自建定位正確；EVS 去留＝動實驗設計，本輪不碰 | — |
| **D5** baseline 前作 | AudioMarkBench（2024，只做模擬擾動） | **補《Will They Survive Neural Codecs?》** | 2025（Interspeech） | arXiv 2505.19663／repo（論文級對照，0 GPU） | D5 主題（watermark×neural codec）的最新且唯一直接前作，容量塌陷點論證錨到已發表基準 | — |
| **D5** 載體語音／watermark 家族／通道矩陣 | AISHELL-3+LibriSpeech+real／AudioSeal+WavMark+SilentCipher／傳統+neural codec | **維持不換** | — | — | 載體年份不影響 bit 容量；watermark 已是開源全集；通道矩陣是物理界線 | — |

### Round 2 駁回了哪些站不住的提議（取得性／方法純度）

1. **「RTCFake 已確認公開可下載、D2 風險解除」——全場一致撤回。** Round 1 有六份（含 landscape）跟著 landscape §四寫「公開可下載」；G 兩輪實測 HF 匿名抓取皆回 **HTTP 401（gated）**、CodecFake+ 對照回 200。這是「把希望當事實」，D2 的月 0 單點故障不解除。
2. **ASVspoof 5 當 D1／D3 訓練種子——駁回。** 換 in-domain 種子＝frozen 偵測器要重訓＝改方法論（違規）；且其內建 adversarial（Malafide/Malacopula）＋neural codec 條件會「預先接種」偵測器，使 unseen gap 人為縮小、攻擊面過度樂觀。授權亦非乾淨 CC tag。
3. **CodecFake+ 放進 D1 的 generator-shift 格——駁回。** CodecFake+ 的 fake 本身即 neural-codec 產物，放進 generator 軸再過 `C_neural`（EnCodec）通道副本，兩軸物理共線，那一格的失效無法乾淨歸因，破壞 D1「shift 網格逐格可讀」的核心價值。CodecFake+ 的正確歸宿是 D3／D5。
4. **CodecFake+ 當 D2 的主 fake——駁回。** 已 transcode 的樣本進審計台＝codec-on-codec，會系統性下偏 D2-RQ3 的「畸變層歸因」並污染 C0' 基準。D2 fake 只用乾淨合成世代。
5. **D2 real 換 SpoofCeleb、模擬臂引入 ADD-C——駁回。** real 只是載體不進 γ 一階（SpoofCeleb 且受 VoxCeleb 非商用授權）；ADD-C 固定條件無法逐因子拆，會逼改方法論。皆為換而換，至多 discussion 引用。

### Round 2 擋下了哪些偷渡的範圍擴充

1. **D1 unseen 軸「四／五件套全上」（DFADD+CodecFake++SpeechFake+MLAAD v10+Deepfake-Eval-2024）——擋下。** 4×3=12 格會偷脹成 7–8×3，前向／對抗搜尋／重跑全部翻倍。只准換 **2 個 source 格**。
2. **Deepfake-Eval-2024 當 D1 第 5 個 source 格——擋下。** 加格＝加實驗，且 scrape 內容再散布受限、無生成器標記破壞分層抽樣。僅在 discussion 一句話標明「未涵蓋閉源商用世代」。
3. **D3 unseen 軸再疊 SpeechFake（CodecFake++DFADD 之外）——擋下。** 兩範式（neural-codec＋diffusion/FM）已覆蓋，再加＝灌水固定搜尋池、降低攻擊成本上界的解析度。
4. **fake 家數膨脹（D2 擴 5 家、D4 擴 4 家）——擋下。** 等量替換原則：D2 維持 3 家、D4 維持 2 家。
5. **ASVspoof 5 的 adversarial 子集「順便測」——釘死。** 一旦拉進 laundering 評估即復活 D3 定稿已一刀砍掉的白盒 PGD 軸。若不得已用 ASVspoof 5，只取乾淨 TTS/VC＋codec 條件。
6. **D4 移除 EVS 通道條件——擋下（本輪不處理）。** EVS 是通道矩陣（實驗設計），增或減都超出「只換餵進去的資料」的授權；訊號論證縱使有理，留待日後方法複審輪。
7. **D4 的 zh-CN 對照臂升為第二實驗、D5 的 CodecFake+ 拉成新載體／watermark 軸——擋下。** 前者偷換方向主體語言與尺度；後者會讓 D5-RQ1 從「容量塌陷點」滑回被砍的「watermark 分類學」。

---

## 二、五個方向（依原推薦順序，逐一更新）

> 推薦順序沿用 convergence 定稿：**#1 D1 → #2 D3 → #3 D4 → #4 D5 → #5 D2**。

---

### 推薦 #1｜D1：分布偏移下語音深偽偵測的選擇性預測基準

**1. 正式題目**
- 中：《分布偏移下語音深偽偵測的選擇性預測基準》
- 英：*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection under Generator and Channel Shift*
- （去「不知道就別答」口語金句；英文以 "under Generator and Channel Shift" 點明雙 shift 來源且不與 "Shift-Aware" 重複。）

**2. 一句話問題（沿用定稿，不改）**
> 當語音深偽偵測器遇到訓練時沒見過的生成器與通道，它的棄權訊號還能不能可靠地認出「自己這次會答錯」？

**3. 三個 RQ（沿用定稿，僅資料集名稱處更新）**
- RQ1（劣化）：generator-shift 與 channel-shift 下各棄權訊號的判別力還剩多少（fixed-FPR≤1% selective recall／risk–coverage／ECE）？→ 負領土地圖。
- RQ2（分岔）：density-based 與 discriminative-derived 兩族分數在同格是否分道揚鑣？
- RQ3（對抗）：把棄權訊號推進 confident-real 區的最低成本？RQ1/RQ2 排序在對抗欄下是否翻轉？
- 資料集更新只影響 RQ1/RQ3 所讀的 unseen 格內容（DFADD/MLAAD v10 取代 2021 DF/MLAAD v5），量測介面 `s×g×R–C` 一行不改。

**4. 資料集：新舊對照**

| source 格（維持 4×3=12） | 現用舊集 | 換成新集 | 五驗收簡述 | 抽樣 | 下載來源 |
|---|---|---|---|---|---|
| in-domain 訓練種子 | ASVspoof 2019 LA train+dev | **維持** | 換即重訓（違規）；定義「seen 分布」的社群基準 | 全集 | Edinburgh DataShare |
| in-domain 對照格 | ASVspoof 2019 LA eval | **維持** | 同上 | 抽 20k | Edinburgh DataShare |
| unseen-generator 格 | ASVspoof 2021 DF eval（2021） | **DFADD（2024）** | 更新：diffusion/FM 新範式；可取得：HF MIT 非 gate（用 2025-04 修正版）；算力：抽 20k（附帶消掉 DF 611k 全集紅線）；契合：一格內容替換、介面不改；時效：unseen=2024 human-parity 生成範式 | 抽 20k | HF `isjwdu/DFADD` |
| unseen-廣度格 | MLAAD v5（2023） | **MLAAD v10（2025）**（主）／SpeechFake 開源部（二選一） | 更新：v5→v10 或 2025 開源 30 工具；可取得：deepfake-total.com 公開／HF Apache 2.0；算力：抽 20k；契合：drop-in 同管線；時效：廣度升 2025 世代 | 抽 20k | deepfake-total.com/mlaad ／ HF `DeepFense/SpeechFake` |
| in-the-wild real 格 | In-the-Wild（全集） | **維持** | 第一週 smoke-test（37.9h／~10 分鐘一次前向）＋真實錄音 real 類 | 全集 | Fraunhofer AISEC（request form） |
| 通道軸 | C_clean／C_celp／C_neural（自建） | **維持** | shift 網格需逐格可控自變數，不可改用資料集內建 codec | — | 自建 |

- **不進 grid**：CodecFake+（軸糾纏）、Deepfake-Eval-2024（加格＋scrape 受限，僅 discussion 一句話「未涵蓋閉源商用世代」）、ASVspoof 5 種子（重訓＋接種）。

**5. 因資料集更新而需微調之處**
- baseline checkpoint **不需在新集上重跑訓練**（frozen，種子未動）；DFADD／MLAAD v10 僅走既有「一次前向→快取 logits+pooled embedding」離線介面。
- GPU-hour **維持 430–520**（換掉 DF 611k 全集反而遠離預算紅線 #2；DFADD 數 GB 更便宜）。
- 唯一實務注意：DFADD 務必抓 **2025-04 修正版**（Matcha-TTS 標籤錯配已修）。

**6. 其餘（方法／時程／退路／社會意義）**：維持 convergence 定稿。

---

### 推薦 #2｜D3：被動語音深偽偵測的 adaptive-laundering 攻擊成本上界評估

**1. 正式題目**
- 中：《被動語音深偽偵測之適應性洗刷（adaptive laundering）攻擊成本上界評估》
- 英：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
- （去「攻擊者付的絕不超過多少」問句金句；「adaptive laundering」首次出現以「適應性洗刷」譯並括註英文；「地圖/Map」改「評估/Assessment」以符學位論文正式度。）

**2. 一句話問題（沿用定稿，不改）**
> 對一個被動語音深偽偵測器，攻擊者讓它失效最便宜要付多少，其中多少是防守方永遠追不回的？

**3. 三個 RQ（沿用定稿，僅資料集名稱處更新）**
- RQ1（成本上界）：讓 fixed-FPR≤1% recall 跌破門檻的最便宜 laundering 配方？→ greedy 搜尋終點。
- RQ2（可逆性下界）：配方中哪些可逆（channel-aware DA 追得回）、哪些踩到不可逆資訊摧毀下界（neural codec transcode 的 many-to-one 投影）？
- RQ3（懸崖/緩坡）：攻擊成本-recall 曲線幾何？
- 資料集更新只把「被 laundering 的 fake」升到 2025 世代，greedy 協定／動作空間／可控植入標註一行不改。

**4. 資料集：新舊對照**

| 用途 | 現用舊集 | 換成新集 | 五驗收簡述 | 抽樣 | 下載來源 |
|---|---|---|---|---|---|
| laundering 主對象／確認池 | ASVspoof 2021 DF（2021） | **CodecFake+（2025）** | 更新：31 neural codec + 17 codec-based 生成系統，領域最大公開集；可取得：HF **MIT 101 GB 非 gate**；算力：抽 20k 確認/10k 搜尋，neural transcode 只在抽樣池；契合：換 greedy 餵進的離線音訊，協定不改；時效：**與 RQ2 neural codec 不可逆論證直接同構**，假想威脅變可實測 2025 fake | 抽 20k/10k | HF `CodecFake/CodecFake_Plus_Dataset` |
| unseen-generator 軸 | MLAAD（2023） | **DFADD（2024）** | 同 D1：diffusion/FM 新範式，HF MIT 修正版 | 抽 20k/10k | HF `isjwdu/DFADD` |
| in-domain 種子 | ASVspoof 2019 LA | **維持** | 換即重訓；承重錨是物理可逆性下界（不過期），種子非承重 | — | ASVspoof 官網 |
| laundering 動作空間 | EnCodec/DAC + ffmpeg codec | **維持** | 是工具鏈非資料集；EnCodec/DAC 仍主流 | — | HF / ffmpeg |

- **不加 SpeechFake**（兩範式已覆蓋，屬灌水）。**ASVspoof 5 不換種子**；若不得已用，只取乾淨 TTS/VC＋codec 條件，**adversarial 子集嚴禁進評估**。

**5. 因資料集更新而需微調之處**
- 偵測器 checkpoint **不需重跑訓練**（種子未動）；只換 greedy 搜尋所打的 fake 池。
- **一個必寫的 caveat（紅隊/訊號一致）**：CodecFake+ 的 fake 本身即 codec 產物，RQ2 可控植入的可逆性 ground-truth 必須定義在「植入的已知 artifact → 過動作」上，**不受源端 codec 污染**（方法上本來就成立）。
- GPU-hour **維持 610**；CodecFake+ 101 GB **只下載一次**（與 D5 參照共用），抽 20k。

**6. 其餘（方法／時程／退路／社會意義）**：維持 convergence 定稿。

---

### 推薦 #3｜D4：詐騙情境條件下語音深偽偵測的評估效度審計（繁中）

**1. 正式題目**
- 中：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》
- 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*
- （去「到達耳朵的那三秒」抒情金句與破折號，改冒號從屬；保留「繁體中文語料」地域貢獻；英文用 Scam-Scenario 較 Scam-Scene 標準。）

**2. 一句話問題（沿用定稿，不改）**
> 現行語音深偽偵測 benchmark 用朗讀長句量出的偵測率，對「詐騙現場實際到達受害者耳朵的三秒音訊」系統性高估了多少、高估來自哪個條件軸？

**3. 三個 RQ（沿用定稿，僅資料集名稱處更新）**
- RQ1（總量）：標準素材→詐騙現場素材，fixed-FPR≤1% recall 落差多大？
- RQ2（分解）：話術語意／短句長／情緒韻律／通道各軸主效應與交互效應？
- RQ3（效度）：品質配對後淨落差還剩多少（偵測器失效 vs 生成品質差解耦）？
- 資料集更新只把 fake 生成器升到 2025 世代 zh TTS，析因/配對三讀法不改。

**4. 資料集：新舊對照**

| 用途 | 現用舊集 | 換成新集 | 五驗收簡述 | 抽樣 | 下載來源 |
|---|---|---|---|---|---|
| fake 生成器（維持 2 家） | 情緒可控 VITS 系／OpenVoice 類（2022–23） | **2 家 2025 世代 zh 開源情緒 TTS**（CosyVoice 2／F5-TTS／GPT-SoVITS／OpenVoice v2 選 2） | 更新：2024–2025 世代；可取得：GitHub/HF 開源 checkpoint 自建生成；算力：GPU≈180 不變；契合：純換 fake 生成器世代，析因框架不改；時效：2025 能產可信台灣國語哭腔/急迫，代表 2026 詐騙工具 | 自建 ~2–3 萬筆 | GitHub/HF |
| zh-CN 對照臂（新增備選） | （無） | **SpeechFake ZH／CFAD** | 更新：2025/2024；可取得：HF Apache 2.0（開源部）／CFAD 公開；算力：抽樣佐證不放大；契合：只作對照切片；時效：佐證落差非單一腔調 artifact——**須明標腔調為 zh-CN、屬外部效度限制，不升主軸** | 抽樣佐證 | HF `DeepFense/SpeechFake` ／ CFAD 公開 |
| 自建 zh-TW 定位／~165 話術／real 類／通道矩陣（含 EVS）／UTMOS+ECAPA | （同定稿） | **全維持** | 無現成 zh-TW deepfake 集，自建定位正確；EVS 去留＝動實驗設計，本輪不碰 | — | 自建／公開 |

**5. 因資料集更新而需微調之處**
- 偵測器 frozen、不重訓；只換 fake 由哪個 TTS 生成。
- **月 0–1 情緒 zh-TW TTS 硬 go/no-go 關卡維持不變**——但換上 2025 世代（CosyVoice 2／GPT-SoVITS 情緒與語者控制強於 2022 世代）**反而提高過關機率**。
- GPU-hour **維持 ≈180**（全場最寬鬆）。

**6. 其餘（方法／時程／退路／社會意義）**：維持 convergence 定稿。

---

### 推薦 #4｜D5：通訊通道對 watermark provenance 標記的可靠位元容量審計

**1. 正式題目**
- 中：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》
- 英：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*
- （去「還剩幾個 bit」口語金句與破折號；以「及其……判定」把政策判定從屬於容量審計；「歐盟人工智慧法」用全名。）

**2. 一句話問題（沿用定稿，不改）**
> 在詐騙實際發生的音訊通道上，watermark provenance 標記還剩幾個可靠 bit，這個數字夠不夠讓 EU AI Act Article 50 要求的「機器可讀標記」真的被讀出來？

**3. 三個 RQ（沿用定稿，僅 baseline 前作處更新）**
- RQ1（容量地圖）：各 watermark 家族在 codec/neural-codec 通道矩陣上的可靠 bit 容量與容量塌陷點？
- RQ2（構造生死）：「索引不 payload」soft-binding 構造能否單機端到端存活、k 在哪個通道歸零？
- RQ3（Article 50 判定）：把 bit 數字對照兩階操作型門檻，逐通道判可讀/不可讀。
- 資料集本體零變動，只補一篇 2025 前作 baseline。

**4. 資料集：新舊對照**

| 用途 | 現用舊集 | 換／維持 | 五驗收簡述 | 抽樣 | 下載來源 |
|---|---|---|---|---|---|
| baseline 前作 | AudioMarkBench（2024，只做模擬擾動） | **補《Will They Survive Neural Codecs?》（Interspeech 2025）** | 更新：2025 Interspeech，正中 watermark×neural codec 主題；可取得：arXiv 2505.19663／repo；算力：純文獻劃界 **0 GPU**；契合：作 RQ1 前作 baseline，不引入新 pipeline；時效：容量塌陷點論證錨到 2025 已發表基準 | — | arXiv 2505.19663 |
| 載體語音 | AISHELL-3+LibriSpeech+ASVspoof19/In-the-Wild real | **維持** | 載體年份不影響 bit 容量量測（量的是通道對 watermark 的摧毀，非偵測 fake） | 抽 ~10k | 公開 |
| watermark 家族 | AudioSeal+WavMark+SilentCipher | **維持** | 當前開源可得的全部 learned watermark；SynthID 非全開源不納入 | — | 官方 repo |
| 通道矩陣 | 傳統 codec×PLR + neural codec×bitrate | **維持** | 可逆/不可逆二分＋neural 只掃 bitrate 的物理界線已正確 | — | ffmpeg/HF |
| neural codec 世代參照 | （無） | CodecFake+（**僅參照，不進 pipeline**） | 確認容量塌陷點對 2025 codec 世代仍成立 | — | HF（與 D3 共用同一份下載） |

**5. 因資料集更新而需微調之處**
- **零實驗變動**：補前作是 related-work／baseline 定位工作，不動 pipeline、不擴通道矩陣。
- GPU-hour **維持 ≈220**。

**6. 其餘（方法／時程／退路／社會意義）**：維持 convergence 定稿。

---

### 推薦 #5｜D2：真實通道上音訊深偽反制訊號存活的樂觀偏差審計

**1. 正式題目**
- 中：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》
- 英：*Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*
- （去「模擬騙了我們多少」問句金句；保留「樂觀偏差—畸變層歸因」承重連體、名詞收尾。）

**2. 一句話問題（沿用定稿，不改）**
> 離線模擬 codec 相對於可得的真實通道，對音訊 deepfake 反制訊號的存活造成多大的樂觀偏差，而這偏差來自通道的哪一層畸變？

**3. 三個 RQ（沿用定稿，僅資料集名稱處更新）**
- RQ1（被動探針）：偵測器分數當探針，模擬 vs RTCFake 的 recall 落差 → γ。
- RQ2（主動探針）：探針換 AudioSeal watermark bit，同組通道同組樣本灌一次。
- RQ3（歸因）：逐因子落差分解＋單一 channel-conditioned DA 對照。
- 資料集更新只把 fake 升 2025 世代、確認 RTCFake 取得性，審計台協定不改。

**4. 資料集：新舊對照**

| 用途 | 現用舊集 | 換／維持 | 五驗收簡述 | 抽樣 | 下載來源 |
|---|---|---|---|---|---|
| fake 生成器（維持 3 家） | XTTS-v2／VITS／YourTTS（2022–23） | **3 家 2025 世代乾淨開源 TTS**（F5-TTS／CosyVoice 2／一個 diffusion/FM 生成器；或 SpeechFake 開源部乾淨合成） | 更新：2024–2025；可取得：HF 開源/Apache 2.0；算力：抽 20k，現成 fake 反省生成算力；契合：只換探針灌進的 fake，管線不改；時效：γ 量在 2025 fake 上才是 2026 折扣係數 | 抽 20k | HF |
| 真實通道錨 | RTCFake（定稿：月 0 單點故障） | **維持（風險不解除）** | 更新：2026 唯一真實 RTC 錨；可取得：**G 實測 HF 401＝gated**，非直接下載；契合：真實通道劣化已烘進波形，無須自建 rig；**月 0 go/no-go 全額保留**（過 gate＋學術重散布條款雙確認） | 抽 20k | HF `JunXueTech/RTCFake`（gated） |
| real 類／watermark／模擬臂 | 公開 real／AudioSeal／Opus+AMR-WB | **維持** | real 不進 γ 一階；AudioSeal 唯一第三方可用；模擬臂須逐因子可控 | — | 公開／官方 repo |

- **不採**：CodecFake+ 當 fake（codec-on-codec 污染畸變層歸因）、SpoofCeleb（授權受限、為換而換）、ADD-C（無法逐因子拆，至多 discussion 引用）。

**5. 因資料集更新而需微調之處**
- 偵測器 frozen、不重訓。
- 若改用現成預生成 fake（SpeechFake 開源部乾淨部）取代自建 TTS，**可省定稿結帳單中 35 GPU-h 的 TTS 生成**（前處理不升反降）。
- GPU-hour **維持 ≈510**。
- **論文須明寫外部效度限制**：RTCFake 是 Zoom/RTC 通道，≠ 詐騙電話的蜂巢/PSTN 通道。

**6. 其餘（方法／時程／退路/社會意義）**：維持 convergence 定稿（含月 0 RTCFake go/no-go 單點故障退路）。

---

## 三、資料集取得行動清單

> 圖例：🟢 匿名可直接下載（G 實測或 landscape 確認）｜🟡 可取得但有條款/腔調/散布限制（列備選/僅對照）｜🔴 gated/申請制（第一週先送件）

| 資料集 | 用於 | 下載/申請連結 | 授權 | 大小 | 申請制？ |
|---|---|---|---|---|---|
| **DFADD**（2024，用 2025-04 修正版） | D1, D3 | HF `isjwdu/DFADD`（`github.com/isjwdu/DFADD`） | MIT（載體 VCTK CC-BY-4.0／LJSpeech PD） | 數 GB | 🟢 否 |
| **CodecFake+**（2025） | D3（主）, D5（參照） | HF `CodecFake/CodecFake_Plus_Dataset` | MIT | 101 GB（多 .part） | 🟢 否（G 實測 200） |
| **MLAAD v10**（2025） | D1（廣度格主選） | deepfake-total.com/mlaad | 公開研究用途 | 大 → 抽 20k | 🟢 否 |
| **SpeechFake 開源部**（2025） | D1（廣度格替代）, D2（fake 替代）, D4（zh-CN 對照） | HF `DeepFense/SpeechFake`（`github.com/YMLLG/SpeechFake`） | Apache 2.0（開源部；10 家商用 API 子集不釋出） | >TB → **只部分下載抓 20k，勿 clone 全庫** | 🟡 開源部否 |
| **2025 世代 zh 開源情緒 TTS**（CosyVoice 2／F5-TTS／GPT-SoVITS／OpenVoice v2，選 2） | D4（fake 生成） | GitHub/HF 官方 repo | 各開源 | checkpoint | 🟢 否（月 0–1 go/no-go 驗情緒可控性） |
| **2025 世代乾淨開源 TTS**（F5-TTS／CosyVoice 2／一 diffusion 生成器，選 3） | D2（fake 生成） | GitHub/HF 官方 repo | 各開源 | checkpoint | 🟢 否 |
| **《Will They Survive Neural Codecs?》**（Interspeech 2025） | D5（baseline 前作） | arXiv 2505.19663／repo | 論文 | — | 🟢 否（文獻，0 GPU） |
| **CFAD**（2024，zh-CN） | D4（對照，備選） | 公開下載（arXiv 2207.12308） | 學術 | 中 → 抽樣 | 🟡 否（zh-CN 腔調） |
| **RTCFake**（2026） | D2（真實通道錨） | HF `JunXueTech/RTCFake` | repo 未明標重散布 | ~600h → 抽 20k | 🔴 **gated（HF 401）——第一週先送 gate 申請＋讀重散布條款**（D2 月 0 單點故障） |
| ASVspoof 2019 LA／In-the-Wild／AISHELL-3／LibriSpeech／AudioSeal・WavMark・SilentCipher | D1/D2/D3/D5（維持） | Edinburgh DataShare／Fraunhofer AISEC（request form）／官方 repo | 各公開/研究用途 | 既有 | 🟢/🟡（In-the-Wild request form 留 1 週緩衝） |

> **工程紅線（訊號角色 C 裁定，寫進協定）**：CodecFake+（101 GB）被 D3/D5 引用，**只下載一次、共用一份 20k 分層抽樣**，勿多方向各自 clone；SpeechFake 開源部（>TB）**只部分下載/streaming 抓 20k**，勿 clone 全庫（撞 2TB NVMe 生死線）。

---

## 四、給作者的建議

**推薦順序有無變化？** 無。維持 **D1 → D3 → D4 → D5 → D2**。資料集更新沒有動搖任一方向的收斂度、算力或退路可靠度；D2 仍因 RTCFake 單點故障排最後——而本輪 G 的實測反而**確認了它是 gated（HTTP 401）**，等於把定稿的悲觀從假設變成事實，D2 排末位更站得住。

**哪個方向因換上最新資料集而 novelty/時效性提升最多？D3（攻擊成本評估）。** 這是全五方向換得最契合的一換：CodecFake+ 與 RQ2「neural codec transcode 是零金錢、一行指令、物理不可逆的必殺動作」**直接同構**——被打的 laundering 對象本身就是 2025 codec 世代 fake，把「neural codec 既是攻擊也是不可逆通道」從假想威脅升成可實測結論。七位角色在兩輪中一致認證這是最強的一刀。其次是 D1（DFADD 帶進 2019/2021 完全沒有的 diffusion/FM 範式，SOTA 偵測器對它已知失效）與 D4（2025 世代 zh 情緒 TTS 直接決定「三秒哭腔」的外部效度是否成立）。相對地，D5 誠實維持（載體年份不影響物理量測）、D2 的 γ 是「當期模型×當期通道」量測本就會過期——這兩個方向的資料更新是「補時效性缺口」而非「提升 novelty」。

**第一週先下載哪個資料集、驗證它可用？**
- **若選 #1 D1（最推薦）**：第一週下載 **DFADD（2025-04 修正版，HF MIT 非 gate，數 GB，~10 分鐘）** ＋ **In-the-Wild 全集**，抓 **AASIST 官方 repo + ASVspoof19 LA checkpoint**，在 In-the-Wild 上跑一次前向復現 EER，並把它改寫成「一次前向→快取 logits+pooled embedding」骨架——這是全篇基礎設施。DFADD 小、非 gate、當天就能驗「新 unseen 格能不能無痛接進管線」。
- **若選 #2 D3**：第一週下載 **CodecFake+（HF MIT，G 已實測回 200 可匿名下載，101 GB）**＋ DFADD，抽 20k 確認池，先驗「codec-on-codec 情境下可控植入的可逆性 ground-truth 能否乾淨定義在植入 artifact 上」——這是 RQ2 承重論證的地基。
- **若選 #5 D2**：第一週**第一天先送 RTCFake 的 HF gate 申請並讀重散布條款**（G 實測 401，這是全案單點故障）——在 gate 通過前不要投入其他工程，若拿不到即啟動定稿退路（純模擬 codec 階梯 benchmark）。

**一句提醒**：本輪真正被糾正的不是「資料太舊」，而是兩個過度樂觀——把 gated 的 RTCFake 當已解除（D2）、把 CodecFake+ 無腦塞進每個方向（D1 軸糾纏、D2 codec-on-codec 污染）。換新要積極，但取得性與量測純度由證據把關，不由熱情把關。
