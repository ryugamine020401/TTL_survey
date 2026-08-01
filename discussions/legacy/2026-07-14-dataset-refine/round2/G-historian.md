# Round 2 質詢：領域史官（Agent G）
日期：2026-07-14

> 我這關只認兩件事的證據：**這個新集今天匿名下得到嗎（授權/gate/重散布）**、以及**這次「換」有沒有偷偷變成「加」**。本輪我重新考證了 RTCFake 與 CodecFake+ 的 HuggingFace 頁面（見文末考證紀錄），一個關鍵事實先講：**RTCFake 的 HF 頁面對匿名抓取仍回 HTTP 401（gated），CodecFake+ 同時回 200（MIT、101 GB、非 gate）**。這直接推翻 landscape、B、C、D、F、H 五方一致採納的「RTCFake 已確認公開可下載、D2 單點故障解除」樂觀敘述。

---

## 1. 抓出站不住的換資料集提議（5 個，理由逐一引原文）

### ①【最硬】「RTCFake 已確認公開可下載、D2 風險解除」——事實錯誤，gated
- **對方原文**：landscape §四「已確認**在 HuggingFace 公開可下載**（`JunXueTech/RTCFake`）……D2 的最大風險因此下降」；B「已確認 HuggingFace `JunXueTech/RTCFake` **公開可下載**……D2 最大風險下降」；C「landscape 已證實可下載」；D「**事實上它可直接下載**，D2 最大風險就此下降」；F「已確認 HuggingFace 公開可下載」；H「由『單點故障』**降級為『已確認可下載』**」。
- **反駁（理由 a：申請制/gated，拿不到「直接下載」）**：我 Round 1 已測出 HF 匿名抓取回 **401**，Round 2 再測**仍是 401**（CodecFake+ 對照回 200）。arXiv 頁只說「dataset is provided at HF」，不等於匿名可下載——401 是「需登入 + 同意 gate 條款」的強訊號。**六份提議把我 Round 1 已標的 caveat 直接無視，集體上修為「公開可下載」，這是站不住的。** 定稿把 RTCFake 當「月 0 才知能否取得的單點故障」是**對的**，不該被解除。維持 RTCFake 為錨、但**月 0 go/no-go 必須確認 (a) 能過 gate、(b) 授權允許學術重散布（repo 未明標）**，風險敘述不得下修。

### ②「CodecFake+ 塞進 D1 的 unseen-generator 源軸」——軸糾纏、放錯方向
- **對方原文**：B「CodecFake+（2025）……補上『codec 既是攻擊也是通道』的 shift 格」；C「**CodecFake+ 與 D1 的 `C_neural` 通道軸同構**——channel-shift 與 generator-shift 兩軸在此交會」；D、F 亦把 CodecFake+ 列入 D1 unseen 三格。
- **反駁（理由 c/d：污染軸分離，需要多解釋一層 = 動方法語意）**：C 把「兩軸交會」當賣點，恰恰是問題所在。D1 的 `C_neural` 副本**本身就是把樣本過一次 EnCodec/neural codec**；若 source 格裝的 fake **本來就是 neural-codec 生成物**（CodecFake+），那 `generator-shift`（源軸）與 `channel-shift`（通道副本）在這一格**物理糾纏**——量到的 R–C 退化到底來自「沒見過的生成器」還是「codec 通道」無法乾淨歸因，D1 的整個網格價值就在於這兩軸可分。**CodecFake+ 是 D3（laundering / neural codec 同構）的核心資產，不是 D1 的**。D1 unseen 兩格用 **DFADD（diffusion/FM）+ MLAAD v10 或 SpeechFake 開源部** 即可（此即 A 與我 Round 1 的選法）。

### ③「SpeechFake 開源部加進 D3」——為換而換、擴搜尋池廣度
- **對方原文**：A「unseen 軸 → DFADD + SpeechFake 開源部」；B「unseen 軸：MLAAD → 補 DFADD + SpeechFake 開源部」；C、D、F 同。
- **反駁（理由 e：舊任務已被 CodecFake+ + DFADD 覆蓋，再加即擴充）**：D3 的 unseen 需求是「neural-codec + diffusion/FM 兩個 2025 關鍵範式」，**CodecFake+ + DFADD 已各覆蓋一個**。再塞 SpeechFake 進 laundering/確認池，是把「搜尋要打穿的 fake 廣度」擴大——greedy 搜尋的攻擊面隨源集數量膨脹，這是「換資料順便擴充」（本輪明令禁止）。我 Round 1 已寫「不採：SpeechFake……再加屬擴充搜尋池」。**D3 只換 CodecFake+ + DFADD，SpeechFake 不進 D3。**

### ④「Deepfake-Eval-2024 在 D1 新增一格」——加格 = 加實驗
- **對方原文**：B「Deepfake-Eval-2024（2025）→ eval-only 錨」列為 D1 第五件；D「把 In-the-Wild 的角色補上 Deepfake-Eval-2024」；F「加 Deepfake-Eval-2024(2025, eval-only)」。（A 誠實列「可選 stretch，不進主線……當主力會加一格」。）
- **反駁（理由 a + c：scrape 再散布受限、且結構性加格）**：Deepfake-Eval-2024 是 🟡（GitHub scrape 內容、**再散布受限**、52 語無生成器標記、無法當受控 unseen 格），且 D1 的 grid 是 **4 source × 3 channel = 12 格**，硬塞第五個 source 就是 12→15，H 已抓「評估前向、RQ3 對抗搜尋、悲觀重跑全部翻倍」。**我背書 A/H 的處理：不進網格，只在 discussion 以一句『本基準未涵蓋 2024 社群真實流通/閉源商用世代』文字帶過；要用就得替換某一格、不得新增。**

### ⑤「ASVspoof 5 當 D3（或 D1）訓練種子」——換種子 = 重訓 = 動方法
- **對方原文**：D「種子池 ASVspoof 2019/2021 → ASVspoof 5(2024, 抽 20k)」；B、C 列「可選升 ASVspoof 5」。
- **反駁（理由 c：換 in-domain 種子要重訓/重驗 EER，等於動方法論）**：A 自己就寫「換種子＝偵測器要對新分布重驗 EER（吃人週），故列可選，不進主線」；D1 的 checkpoint（AASIST/RawNet2/SSL-AASIST）全是 2019 LA 訓練的 frozen 權重，換種子就得重訓，直接違反「日曆是唯一瓶頸」。**維持 ASVspoof 2019 LA 種子。** ASVspoof 5 若要用，只能當 **unseen eval 對象抽 20k**，且授權須讀 LICENSE.txt（非乾淨 CC tag，我 Round 1 已標「備選」）。

---

## 2. 抓出偷渡的範圍擴充（本輪最需防的——逐一點名）

1. **B 的 D1「五件套」**（DFADD + CodecFake+ + SpeechFake + MLAAD v10 + Deepfake-Eval-2024）塞進 4-source grid。→ H 已當場擋（「4 個 source 格就變 7–8 格」），**我背書**。D1 只換兩格。
2. **A/B/C/D/F 的 D3 加 SpeechFake**（見上 §1③）＝擴搜尋池廣度。點名，剔除。
3. **B/D/F 的 D1 加 Deepfake-Eval-2024 新格**（見上 §1④）＝加 source 格。點名，降為 discussion 文字。
4. **D 的 D3「ASVspoof 5 種子」若挾帶 adversarial 子集**（Malafide/Malacopula）＝**復活定稿已砍的白盒對抗軸**。→ H 已釘死「嚴禁碰其 adversarial 子集」，**我背書**：D3 定稿一刀砍白盒 PGD，ASVspoof 5 首次內建 adversarial，一旦「順便測一下」就是範圍回歸。
5. **C 的 D4「移除 EVS codec」——逆向的範圍變更，本輪不該處理**。C 原文「建議自傳統 codec 集移除 EVS……這是移除一個通道條件（縮範圍）＋省 CPU，不是加東西」。→ **反駁**：本輪任務嚴格鎖定「只換餵進去的**資料**、實驗設計維持定稿不動」。EVS 是 D4 **通道矩陣（實驗設計）**的一個條件，增或減都是動設計，不是換資料。C 的 CPU/在地通道論證或許有理，但**本輪不是處理通道設計的場合**——退回定稿通道矩陣，EVS 去留另議。點名 C，剔除本輪。
6. **D5 的 CodecFake+「參照」**：C/D/F/H 與我一致保持 reference-only、不進 pipeline、不擴通道矩陣。→ **這個守住了**，不點名，僅記錄「D5 全員誠實維持」為正例。

---

## 3. 題目正式化複審（指出仍不夠正式/不準確者，給修正）

- **F 的 D4 題目仍留破折號金句格式**：F 中文「……評估效度之審計**——以繁體中文語料為例**」、英文亦同構。**破折號式副標正是本輪要去掉的花俏格式**。→ 改冒號式：《……評估效度審計**：一份繁體中文語料研究**》（即 D 的寫法）。
- **A 的 D1「shift 三重冗餘 + 贅字」**：A 中文「分布偏移下……」＋英文「*Shift-Aware……under Distribution Shift*」，shift 出現三次（A 自己也標了）；中文「選擇性預測可靠性基準**研究**」的「研究」是贅字（「基準/benchmark」本身即 deliverable）。→ 採 H 的最簡版（見 §4）。
- **D3 中文譯名四家分歧，須統一**：A/B 保留英文「adaptive-laundering」、D「適應性洗白」、我 Round 1「適應性洗刷」、H「調適式洗訊」。「洗白」帶金融洗錢口語聯想（雖是刻意隱喻，學位論文宜穩）；「洗訊」較能表「對訊號去識別/漂白」且無歧義。→ **統一採「調適式洗訊」**（H 版）。
- **D3「地圖/Map」vs「評估/Assessment」**：「上界地圖」略帶隱喻但屬已成形的 cost-map 框架，可接受；惟學位論文標題以「上界**評估**/Assessment」更正式（A、我 Round 1 之選）。→ 我背書「評估/Assessment」為主標詞。
- **C 的 D5「歐盟 AI 法」不夠正式**：法規全名為「歐盟人工智慧法（EU AI Act）」，「AI 法」為口語簡稱。→ 採 H 的「歐盟人工智慧法第 50 條」。
- **D2 主標**：C 的「離線模擬與真實通訊通道之落差：」以「落差」當主標稍鬆散、偏敘述。→ H 版《……存活的樂觀偏差及其畸變層歸因》最乾淨（保留「樂觀偏差—畸變層歸因」承重連體、名詞收尾）。

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

> 原則：只換餵進管線的 fake/通道**資料**；grid、動作空間、偵測器數、20k/10k 抽樣、通道矩陣、算力全維持定稿。所有大集用修正後版本、非 gate、可重散布者為主力。

**D1（分布偏移選擇性預測基準）**
- unseen 兩格換：ASVspoof 2021 DF → **DFADD（2024，MIT，用 2025-04 修正版）**；MLAAD v5 → **MLAAD v10（2025，抽 20k，drop-in 同管線）**（若要一站式當代廣度，可改 SpeechFake 開源部抽 20k 二擇一，**不同時上**，守 4 格）。
- **不採**：CodecFake+ 進源軸（軸糾纏，留 D3）、Deepfake-Eval-2024 新增格（僅 discussion 文字）、ASVspoof 5 當種子。
- **維持**：ASVspoof 2019 LA in-domain 種子 + eval 格、In-the-Wild real 格；grid 維持 4×3。

**D2（真實通道存活樂觀偏差審計）**
- fake：XTTS/VITS/YourTTS → **等量替換 3 家 2025 世代開源 TTS（F5-TTS / CosyVoice 2 / 一個 codec-based 生成器），家數不變**（不因「新世代很多」擴家數，也不用 CodecFake+/SpeechFake 打包灌）。
- **RTCFake：維持為真實通道錨，但恢復定稿「月 0 go/no-go 單點故障」定位——駁回「風險已解除」**（HF 401 gated，月 0 須過 gate + 讀重散布條款）。
- **維持**：public real 類、AudioSeal 單一、Opus/AMR-WB 模擬臂；SpoofCeleb 僅備選（VoxCeleb 非商用衍生）、ADD-C 不進實驗。

**D3（adaptive-laundering 攻擊成本上界）**
- laundering 對象 2021 DF + MLAAD → **CodecFake+（2025，MIT，非 gate，與 RQ2 neural codec 同構）+ DFADD（2024，修正版）**。**SpeechFake 不加**（見 §1③）。
- **維持**：ASVspoof 2019 LA 種子（不換 ASVspoof 5；若真要，只當 unseen eval 抽 20k、**嚴禁 adversarial 子集**）、laundering 動作空間 ≤8、4 偵測器、20k 確認/10k 搜尋池。

**D4（繁中詐騙現場評估效度審計）**
- fake：2 家開源（2022–2023）→ **2 家 2025 世代 zh 開源情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 選 2），維持 2 家**。
- CFAD / SpeechFake ZH **僅 zh-CN 對照臂**，明標外部效度限制，不升主軸。
- **維持**：自建 zh-TW 定位（無現成 zh-TW 集，硬事實）、話術腳本、real 類、品質協變量、**通道矩陣（含 EVS，C 的移除案本輪不處理）**、月 0–1 情緒 zh-TW TTS 硬 go/no-go。

**D5（watermark 可靠位元容量審計）——誠實維持**
- **維持**：載體語音（AISHELL-3/LibriSpeech/real，年份中性）、watermark 家族（AudioSeal/WavMark/SilentCipher，已是開源全集）、neural codec 通道矩陣（EnCodec/DAC/SpeechTokenizer）。
- **唯一更新**：baseline 補 **《Will They Survive Neural Codecs?》（Interspeech 2025）**為直接前作（零 GPU、零新 RQ）。CodecFake+ 僅 neural codec 世代**參照**，不進 pipeline、不擴矩陣。

**五方向背書題目（中／英）**
- **D1**：《分布偏移下語音深偽偵測的選擇性預測基準》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*（H 版最乾淨；若需點明雙 shift 來源，英文可作 *…under Generator and Channel Shift*）
- **D2**：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》／ *Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*（H 版）
- **D3**：《被動語音深偽偵測之調適式洗訊攻擊成本上界評估》／ *An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
- **D4**：《詐騙情境條件下語音深偽偵測的評估效度審計：一份繁體中文語料研究》／ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*（去 F 的破折號）
- **D5**：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》／ *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*（H 版）

---

## 考證紀錄（Round 2 新測）
- **RTCFake**（`JunXueTech/RTCFake`）：HF 匿名抓取 Round 1、Round 2 兩次皆回 **HTTP 401 → gated**；arXiv 2604.23742 僅稱「provided at HF」，非匿名可下載。**「公開可下載」不成立。**
- **CodecFake+**（`CodecFake/CodecFake_Plus_Dataset`）：HF 回 200，**license: MIT，101 GB，非 gate**，可匿名下載。主力可用。
- DFADD 用 2025-04 修正版（Matcha-TTS 標籤錯配已修）；SpeechFake 開源部 Apache 2.0（10 家商用 API 子集不釋出）；ASVspoof 5 授權見 Zenodo LICENSE.txt（非乾淨 CC tag，列備選）。

Sources: [RTCFake HF](https://huggingface.co/datasets/JunXueTech/RTCFake)、[RTCFake arXiv](https://arxiv.org/abs/2604.23742)、[CodecFake+ HF](https://huggingface.co/datasets/CodecFake/CodecFake_Plus_Dataset)
