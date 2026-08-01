# Round 1 資料集提議：Detection 研究者（Agent A）
日期：2026-07-14

> 角色視角自述：我最在意的一件事是「unseen 到底 unseen 不 unseen」。一個 shift/laundering benchmark 若拿 2021 世代生成器當「沒見過的生成器」，量到的 generalization gap 是對 **2021 攻擊者**的 gap，不是 2026 的。2024 年起真正翻代的是兩個生成範式——**diffusion / flow-matching TTS**（Voicebox / Seed-TTS 世代）與 **neural-codec-based 生成**（EnCodec/DAC/SpeechTokenizer 當骨幹）——這兩者在 ASVspoof 2019/2021 完全不存在，而 SOTA 偵測器對它們明顯失效。所以我的替換全部集中在「把 unseen 軸與 laundering 對象升到 2024–2025 世代」，訓練種子與載體 real 這種「不影響方法、換了只增加日曆負擔」的部分則誠實維持不動。
>
> **紀律自檢**：以下每一條都維持「格數不變、只換餵進格子的內容」，不加 RQ、不加實驗軸、不加 deliverable、不放大抽樣規模（一律沿用 20k 分層抽樣）。凡是換上去要改方法論或要多做一格的，一律降為「可選 stretch」或不採。

---

## D1｜分布偏移下語音深偽偵測的選擇性預測基準

### 現用舊資料集
- **訓練種子**：ASVspoof 2019 LA train + dev（2019 世代生成器）
- **source 軸 4 格**（評估池，各分層抽 20k，In-the-Wild 用全集）：
  1. ASVspoof 2019 LA eval — in-domain 對照格
  2. **ASVspoof 2021 DF eval（2021）— unseen-generator 軸**
  3. In-the-Wild（2022）— in-the-wild real 類
  4. **MLAAD v5（2023）— unseen-generator 廣度**
- 通道軸自建 3 副本：C_clean / C_celp（AMR-WB）/ C_neural（EnCodec）；可選 C_rtc（RTCFake）

### 建議替換
把 source 軸**兩格 unseen-generator 內容換新，格數維持 4 格不變**：

| source 格 | 舊 | 新 | 動作 |
|---|---|---|---|
| 1 in-domain | ASVspoof19 LA eval | ASVspoof19 LA eval | **維持**（見下） |
| 2 unseen-generator | ASVspoof21 DF（2021） | **DFADD（2024，diffusion/FM）** | **換** |
| 3 in-the-wild real | In-the-Wild（2022） | In-the-Wild（2022） | **維持**（見下） |
| 4 unseen 廣度 | MLAAD v5（2023） | **SpeechFake 開源部（2025）** | **換** |

- **維持 in-domain 種子（ASVspoof19 LA train）**：這是刻意的。D1 定稿是 frozen backbone + 現成 AASIST/RawNet2/SSL-AASIST checkpoint，這些權重全是 ASVspoof19 LA 訓練的；換訓練種子＝要重訓，直接違反「日曆是 D1 唯一瓶頸」的定稿判定。且**保留 2019 in-domain 種子反而讓 unseen 軸換上 2024–2025 世代後 shift 更大、negative territory 更 unseen**——這正是我要的。ASVspoof 5 train 作為「可選 in-domain 升級對照」列 future work，不進主線。
- **維持 In-the-Wild**：它不是「舊生成器」問題，它是 detection 領域最經典的 in-the-wild real 類 unseen 測試場，且是 D1 第一週 smoke-test 唯一理想場地（31,779 筆 / 37.9h、跑一次前向 ~10 分鐘）。它承擔的是「真實錄音條件」這一格，不是「最新生成器」那一格——後者由格 2、4 承擔。為換而換會砸掉 D1 定稿的第一週驗證路徑。
- **換掉 ASVspoof21 DF → DFADD**：這是我最有把握的一刀。DF 是 2021 生成器，而 DFADD 專攻 2019/2021 完全沒有的 diffusion + flow-matching 生成範式，SOTA 偵測器對它明顯失效——正是 RQ1「負領土地圖」最精準的一格新負領土。**額外紅利**：DF 全集 611k 是預算表唯一會炸掉設計的資料集，換成小型 DFADD 直接消掉這個風險。
- **換掉 MLAAD v5 → SpeechFake 開源部**：MLAAD v5 是現用版本落後（最新已 v10），且 SpeechFake 開源部（30 開源工具、含 2024–2025 TTS/VC/vocoder 世代 + 完整 metadata）是 unseen 廣度軸最省事的一站式 2025 更新。（若嫌 SpeechFake 下載大，退而用 MLAAD v10 抽 20k 亦可，皆 🟢。）

### 通過五項驗收（換上去的兩格）
**DFADD（格 2）**
- **更新**：2024-09（arXiv 2409.08731，ICASSP 2025）；diffusion/FM 世代，2021 DF 沒有的生成範式。
- **可取得**：HuggingFace（`github.com/isjwdu/DFADD`），開源，中小型（數 GB），非申請制，2025-04 已修正 Matcha-TTS 標籤並統一格式。🟢
- **算力相容**：規模小，可整段納入或分層抽 20k 與其他格對齊；比 DF 全集便宜 20–30×，直接省掉 D1 最大的 budget 風險。
- **契合原方法**：就是一個 source 格的樣本內容，走完全相同的「一次前向 → 快取 logits+pooled embedding → 離線讀 R–C」介面，方法一行不改。
- **時效性論證**：讓「unseen-generator shift」測到的是 2024 human-parity diffusion/FM TTS，D1 的負領土地圖才反映 2026 攻擊者手上的工具而非 2021 的。

**SpeechFake 開源部（格 4）**
- **更新**：2025-07（ACL 2025，arXiv 2507.21463）；30 開源工具涵蓋 2024–2025 TTS/VC/vocoder。
- **可取得**：HuggingFace `DeepFense/SpeechFake`，**開源部 Apache 2.0**，附完整 metadata，下載腳本 `github.com/YMLLG/SpeechFake`。🟢（注意：10 家商用 API 子集因授權不釋出，**只用開源部**，不依賴其閉源覆蓋。）
- **算力相容**：完整 >數 TB，**強制分層抽 20k**（沿用 D1 既有規則），與其他格同規模。
- **契合原方法**：同一 source 格內容替換，metadata 齊全反而讓分層抽樣更乾淨；方法不變。
- **時效性論證**：一站式把 unseen 廣度軸升到 2024–2025 開源世代，涵蓋最廣的當代生成家族，比 MLAAD v5 的 2023 世代更貼近 2026。

### 可選 stretch（不進主線，避免加格）
- **Deepfake-Eval-2024（2025，eval-only）**：唯一「攻擊分布 = 2024 年社群真實流通、隱含含閉源商用世代」的公開 eval 集，SOTA 偵測器在其上 audio AUC 掉 48%。它最能證明「舊 benchmark 結論已過期」，但**再散布授權受限且是第 5 格**——若當主力會加一格、動 12 格結構。故僅列為與 C_rtc 同級的可選 eval 錨（🟡），不承重、砍了不影響任何 RQ。

---

## D3｜被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖

### 現用舊資料集
- **laundering 對象 / 確認池**：ASVspoof 2019 LA / 2021 DF（DF 611k → 抽 20k 確認池、10k 搜尋池）
- **unseen-generator 軸**：In-the-Wild、MLAAD（分層抽樣子集）
- **laundering 動作空間工具鏈**：EnCodec / DAC + Opus/AMR-NB/μ-law/MP3/AAC（不動）
- 偵測器 checkpoint：AASIST / RawNet2 / wav2vec2-XLS-R backend + 自建 Mahalanobis-on-SSL baseline

### 建議替換
把「被 laundering 的 fake 樣本」的生成器世代換新，**動作空間、搜尋協定、確認/搜尋池規模全部不動**：

| 用途 | 舊 | 新 | 動作 |
|---|---|---|---|
| laundering 主對象 / 確認池 | ASVspoof21 DF（2021） | **CodecFake+（2025，neural-codec 世代）** | **換** |
| unseen-generator 軸 | MLAAD（2023） | **DFADD（2024）+ SpeechFake 開源部（2025）** | **換** |
| in-domain 種子 | ASVspoof19 LA | ASVspoof19 LA（維持，見下） | **維持** |
| 動作空間工具鏈 | EnCodec/DAC + ffmpeg codec | 同上 | **維持** |

- **換 laundering 對象 → CodecFake+**：這是 D3 換資料最強的一刀，理由是**資料與 RQ2 直接同構**。RQ2 的承重錨是「neural codec transcode 的 many-to-one 投影是物理不可逆必殺動作」。過去這是拿乾淨 fake 去跑 neural codec 通道「模擬」的假想威脅；改用 CodecFake+（31 開源 neural codec + 17 codec-based 生成系統，2025-01 為此領域最大公開集）後，被打的樣本**本身就是 codec 世代的 fake**——「neural codec 既是攻擊生成骨幹、也是不可逆 laundering 動作」這條論證從假想變成可實測。攻擊成本地圖打的是 2025 世代生成器，不是 2021 的。
- **unseen 軸 → DFADD + SpeechFake 開源部**：與 D1 同理由，把 laundering 要打穿的偵測器所面對的 fake 升到 diffusion/FM + 2024–2025 開源世代。
- **維持 ASVspoof19 LA 種子**：同 D1，偵測器 checkpoint 相容性；且換掉會動搜尋/確認池的 in-domain 基準定義。
- **附帶紅利**：換掉 DF 611k 全集，直接遠離預算表紅線 #2；CodecFake+ 抽 20k 確認池 / 10k 搜尋池與定稿完全對齊。

### 通過五項驗收
**CodecFake+（laundering 主對象）**
- **更新**：2025-01（arXiv 2501.08238）；31 neural codec + 17 codec-based 生成系統，截至 2025-02 領域最大公開 neural-codec fake 集。
- **可取得**：HuggingFace `CodecFake/CodecFake_Plus_Dataset`（`github.com/ResponsibleGenAI/CodecFake-Plus-Dataset`，2025-10 已補 CoRS/CoSG 標籤），開源，多 .part 檔合併下載，非申請制。🟢
- **算力相容**：大集，**分層抽 20k 確認池 / 10k 搜尋池**（沿用定稿），不放大規模；neural codec transcode 只在抽樣池上做（S10）。
- **契合原方法**：只是換 greedy 搜尋餵進去的離線音訊，動作空間、prefix-caching 轉檔池、成本代理、懸崖/緩坡讀法全部逐字不變；不換方法論。
- **時效性論證**：讓「不可逆必殺動作」是對 2025 真實 codec 世代 fake 的實測，而非對 2021 樣本模擬的假想，RQ2 的資訊理論下界錨得在當代攻擊面上。

**DFADD + SpeechFake 開源部（unseen 軸）**：驗收同 D1（DFADD 🟢 數 GB / SpeechFake 🟢 Apache 2.0 抽 20k），皆一格內容替換、方法不變、時效性 = laundering 打的是 2024–2025 世代偵測對象。

### 可選 stretch
- **ASVspoof 5（2024，抽 20k）取代 ASVspoof19/21 種子**：crowdsourced 非棚錄 + 首次內建 neural codec 條件 + 首次含 adversarial 攻擊，同時升 in-domain 種子與 unseen 對象。但換種子＝偵測器要對新分布重驗 EER（吃人週），故列可選，不進 D3 主線關鍵路徑。

---

## D2｜真實通道上音訊深偽反制訊號的樂觀偏差審計

### 現用舊資料集
- bona fide real：ASVspoof19 LA real / In-the-Wild real / MLAAD real
- **fake：3 家開源 TTS（XTTS-v2、VITS、YourTTS）— 2022–2023 世代，自建生成**
- 真實通道錨：**RTCFake（定稿把它當「月 0 才知能否取得」的單點故障）**
- watermark：AudioSeal（單一）

### 建議替換
- **RTCFake：不是換新，是解除風險。** 定稿最大單點故障其實已緩解——RTCFake 已確認 HuggingFace `JunXueTech/RTCFake` 公開可下載（2026，~600h，真實 RTC 傳輸、offline/online 精確配對）。**保留為真實通道錨、保留月 0 go/no-go 閘**（仍需確認學術重散布條款），但風險敘述從「可能整個拿不到」下修為「可下載、僅授權條款待確認」。
- **fake 生成器世代升級**：3 家 2022–2023 開源 TTS → 改抽 **SpeechFake 開源部（2025）現成 fake**（可補 CodecFake+ 的 codec 世代）。反制訊號要在 2024–2025 世代 fake 上測通道存活，量到的 γ 才是 2026 的「通道折扣係數」。**附帶紅利**：改用現成 fake 省掉定稿的 TTS 自建生成成本（結帳單 35 GPU-h 那筆可縮）。
- real 類：ASVspoof19 real 維持（作為載體 real，年份不影響存活量測）；SpoofCeleb 是備選（🟡 VoxCeleb 衍生非商用授權，再散布受限，不當主力）。
- watermark：AudioSeal 維持（開源可得的唯一 SOTA localized watermark，無更新替代；SynthID 非第三方可用已被定稿正確砍除）。

### 通過五項驗收（fake 世代升級）
**SpeechFake 開源部（+ 可選 CodecFake+）作為 fake source**
- **更新**：2025（ACL 2025）/ CodecFake+ 2025-01。
- **可取得**：HuggingFace，SpeechFake 開源部 Apache 2.0 / CodecFake+ 開源。🟢
- **算力相容**：**分層抽 20k**（沿用 D2 既有池），現成 fake 反而省生成算力。
- **契合原方法**：只換灌進審計台的 fake 樣本型態（同為波形域音訊），通道管線、fixed-FPR 差分存活協定、C0' 對照臂全不動。
- **時效性論證**：反制訊號的「模擬 vs 真實通道」樂觀偏差 γ，是對 2024–2025 世代 fake 測的，才是 2026 部署方能直接消費的通道折扣係數。

### 誠實提醒
D2 的核心因變數是「通道存活差分 γ」，fake 世代對 γ 的影響是二階的（通道畸變才是一階）；升級 fake 世代主要提升時效性與外部效度，不改變 D2 的科學骨幹。這一刀價值中等但零成本、零風險，值得換。

---

## D4｜詐騙現場條件下語音深偽偵測的評估效度審計（繁中）

### 現用舊資料集
- real 載體：Common Voice zh-TW + AISHELL + 公開廣播 + ASVspoof/In-the-Wild real 類
- **fake：純 2 家開源情緒可控 TTS/VC（定稿寫 VITS 系 / OpenVoice 類，2022–2023 世代）**
- 品質協變量：UTMOS + ECAPA speaker similarity（機器計算）

### 建議替換
- **維持自建定位**（誠實維持）：目前**沒有公開的 zh-TW / 台灣國語 deepfake 語音集**，D4 自建語料的定位完全正確，不因換資料集而動搖。這不是「為換而換」的地方——沒有現成集可換。
- **只換 fake 生成器世代**：2022–2023 的 VITS/YourTTS/OpenVoice → **2025 世代 zh 開源可控情緒 TTS：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2**。這是「換餵進同一條管線的 fake 生成器」，不改方法論。
- **對照臂補 zh-CN**：SpeechFake ZH 子集（2025，Apache 2.0 開源部）/ CFAD（2024，zh-CN）作為「非 zh-TW 對照臂」，佐證落差非單一腔調 artifact（🟡 zh-CN 腔調，須在論文標明外部效度限制）。

### 通過五項驗收（fake 世代升級 + zh-CN 對照臂）
- **更新**：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 皆 2024–2025 世代；SpeechFake ZH 2025 / CFAD 2024。
- **可取得**：生成模型皆開源可下載（🟢，自建）；SpeechFake ZH HuggingFace Apache 2.0、CFAD 公開下載（🟡 zh-CN）。
- **算力相容**：D4 是全場算力最寬鬆（≈180 GPU-h，用不到上限 19%），2 家開源 TTS 生成 2 萬筆 ~2–8 GPU-h，換 2025 世代模型不改變量級；對照臂分層抽樣。
- **契合原方法**：D4 核心是「同一組 frozen 偵測器在標準 vs 現場素材的 recall 落差」，換 fake 生成器只影響 fake 樣本世代，受控析因量測、fixed-FPR recall、UTMOS 品質配對協定全不動。
- **時效性論證**：「到達耳朵的那三秒」要用 2025 能穩定產生台灣國語哭腔/急迫的當代 TTS，才代表 2026 詐騙工具；2022 世代 TTS 的露餡點已不是攻擊者現在用的。

### 誠實提醒
D4 的**真正取得性風險不在資料集、在「2025 世代 zh 開源 TTS 能不能穩定產出可信台灣國語哭腔/急迫」**——這正是定稿月 0–1 硬 go/no-go 關卡守的東西。換上更新世代 TTS 反而提高這關過關機率（CosyVoice 2 / GPT-SoVITS 的情緒與語者控制強於 2022 世代），與定稿退路（crash-path B 三軸析因）相容。這方向非我核心專長，我的建議僅限「確認 fake 生成器是 2025 世代」，語料建構與繁中標註交由策展人 B 與相關角色主導。

---

## D5｜詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

### 現用舊資料集
- 載體 real：AISHELL-3 + LibriSpeech + ASVspoof19 / In-the-Wild real 類（分層抽 ~10k 池）
- watermark 家族：AudioSeal / WavMark / SilentCipher（皆開源 learned watermark）
- **baseline：AudioMarkBench（2024，只做模擬擾動，未含 neural codec 通道專門評估）**
- 通道：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC）× PLR ＋ neural codec（EnCodec/DAC/SpeechTokenizer）× bitrate

### 建議替換：大致維持，只補 baseline 前作（誠實維持）
- **載體 real（AISHELL-3/LibriSpeech/ASVspoof19/In-the-Wild）維持**：它們是 watermark 的**載體語音**，watermark 嵌在乾淨 real 語音上再過通道；載體的生成器年份**不影響可靠 bit 容量量測**（D5 量的是通道對 watermark 的摧毀，不是偵測 fake）。換載體對 RQ 零助益，屬「為換而換」，不採。
- **watermark 家族（AudioSeal/WavMark/SilentCipher）維持**：這是當前開源可自由嵌入/偵測的**全部**learned watermark；SynthID 非全開源（定稿已正確排除）。無更新替代品可換。
- **唯一該補的是 baseline 前作**：AudioMarkBench（2024）→ **補上「Will They Survive Neural Codecs?」（Interspeech 2025，arXiv 2505.19663）**。它正是 D5 主題（watermark × neural codec 存活）的最新前作，讓 D5「neural codec 通道容量塌陷 / 第一張可靠 bit 容量地圖」的定位錨在 2025 已發表基準上，相對前作補的是「可控植入 ground-truth 錨 + 索引不 payload 構造」。
- 通道矩陣維持（傳統 codec × PLR + neural codec × bitrate，物理界線已由定稿釘死）。

### 通過五項驗收（baseline 前作）
- **更新**：Will They Survive Neural Codecs? 2025（Interspeech 2025），比 AudioMarkBench（2024）新一年、且**正中 D5 主題**（前者只做模擬擾動，未碰 neural codec 通道）。
- **可取得**：論文 + repo 公開。🟢（僅作對照/劃界，不是新運算資料集，零下載負擔。）
- **算力相容**：純文獻劃界 + 協定對照，0 GPU-h。
- **契合原方法**：作為 RQ1 容量地圖的前作 baseline 劃界，不引入新 pipeline、不改可靠 bit 復原方法。
- **時效性論證**：把 D5 錨到 2025 最新的「watermark × neural codec」前作，容量塌陷點論證從「無直接前作」升級為「相對 2025 前作補足 ground-truth 錨與構造」，定位更硬更貼近 2026。

### 誠實提醒
D5 是五個方向裡**最不需要換資料集**的一個——它的資料是「載體 real + 開源 watermark + 離線通道」，這三者要嘛年份不影響（載體）、要嘛已是開源全部（watermark）、要嘛物理定義（通道）。唯一有時效性缺口的是 baseline 前作，補一篇 2025 Interspeech 即可。**不為換而換**是這裡最誠實的答案。

---

## 正式題目提議（我最有把握的兩個方向：D1、D3）

> 正式化原則：去金句、去破折號式標語、去問句、去口語；保留專有名詞英文（audio deepfake detection、selective prediction、adaptive laundering）；符合學位論文標題慣例（一個名詞性中心語 + 限定範圍）。

### D1（我最有把握，這是我的核心領域：selective prediction × domain generalization）
- **舊（花俏）**：《不知道就別答——分布偏移下語音深偽偵測的選擇性預測基準》/ *Abstain When Unsure: A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*
- **正式（中）**：《分布偏移下語音深偽偵測之選擇性預測可靠性基準研究》
- **正式（英）**：*A Shift-Aware Benchmark for Selective-Prediction Reliability in Audio Deepfake Detection under Distribution Shift*
  - （若嫌 shift 重複，英文可作：*A Benchmark for Selective-Prediction Reliability in Audio Deepfake Detection under Generator and Channel Shift*）

### D3（我的核心領域：對抗評估 × laundering × neural codec 不可逆性）
- **舊（花俏）**：《攻擊者付的絕不超過多少——被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖》/ *What Does the Attacker Pay at Most? An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- **正式（中）**：《針對被動語音深偽偵測之 adaptive-laundering 攻擊成本上界評估》
- **正式（英）**：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

---

## 回傳摘要（純文字資料）

**五方向「舊 → 新」一行版：**
- **D1**：source 軸 unseen-generator 兩格 ASVspoof 2021 DF（2021）→ DFADD（2024, diffusion/FM）、MLAAD v5（2023）→ SpeechFake 開源部（2025）；in-domain 種子 ASVspoof19 LA、In-the-Wild real 類維持（格數維持 4 格）。
- **D2**：真實通道錨 RTCFake 由「單點故障」解除為「已確認公開可下載」（保留月 0 go/no-go）；fake 生成器 XTTS-v2/VITS/YourTTS（2022–2023）→ SpeechFake 開源部（+ 可選 CodecFake+，2025）；AudioSeal / 載體 real 維持。
- **D3**：laundering 主對象 ASVspoof 2021 DF（2021）→ CodecFake+（2025, neural-codec 世代，直接同構 RQ2）；unseen 軸 MLAAD（2023）→ DFADD（2024）+ SpeechFake 開源部（2025）；動作空間工具鏈、搜尋協定、種子維持。
- **D4**：無現成 zh-TW 集，自建定位維持不變；fake 生成器 VITS/YourTTS/OpenVoice（2022–2023）→ CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2（2025）；對照臂補 SpeechFake ZH / CFAD（zh-CN，標外部效度限制）。
- **D5**：資料集大致維持（載體 real 年份無關、watermark 家族已是開源全部）；只補 baseline 前作 AudioMarkBench（2024）→ 加上「Will They Survive Neural Codecs?」（Interspeech 2025）。

**提議的正式題目：**
- **D1**：《分布偏移下語音深偽偵測之選擇性預測可靠性基準研究》/ *A Shift-Aware Benchmark for Selective-Prediction Reliability in Audio Deepfake Detection under Distribution Shift*
- **D3**：《針對被動語音深偽偵測之 adaptive-laundering 攻擊成本上界評估》/ *An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
