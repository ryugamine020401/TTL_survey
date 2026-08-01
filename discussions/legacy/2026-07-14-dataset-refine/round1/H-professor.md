# Round 1 資料集提議：指導教授（Agent H）
日期：2026-07-14

> 我的雙重把關立場：(1) 題目要**正式**（學位論文慣例，中英皆去除破折號金句、問句、口語 hook）；(2) 守住碩士尺度——**換資料集只能「替換」不能「新增」**。凡是把「4 個 source 格擴成 8 格」「2 家開源 fake 擴成 4 家」「多接一個對照集/對照臂」偽裝成資料更新的，一律當場擋下。三個 RQ、核心方法、實驗設計、20k 分層抽樣、算力預算全部不動。
>
> 貫穿五個方向的一條紅線（我作為教授要反覆講的）：**新資料集越多越誘人，越要問「這是替換舊格，還是偷加一格？」** 偷加一格＝偷加一批前向、一批對抗搜尋、一批重跑，那就是本輪明令禁止的範圍膨脹。下面每個方向我都標出它最可能被偷加的地方。

---

## D1：分布偏移下語音深偽偵測的選擇性預測基準

**現用舊資料集**
- ASVspoof 2019 LA train+dev+eval（in-domain 訓練種子 + in-domain 對照格）
- ASVspoof 2021 DF eval（unseen-generator 格，分層抽 20k）
- In-the-Wild（unseen 格，全集 37.9h）
- MLAAD v5（unseen-generator 廣度格，分層抽 20k）
- 通道軸自建 C_clean / C_celp / C_neural（可選 C_rtc）

**建議替換（最小替換，grid 維持 4 source × 3 channel = 12 格不動）**
- **MLAAD v5 → MLAAD v10（2025）**：同一來源、同一下載/前向管線的版本升級，是全案最便宜、零風險的更新。drop-in。
- **ASVspoof 2021 DF 這一格 → DFADD（2024，diffusion / flow-matching TTS）**：2021 DF 是最舊的一格；DFADD 帶進 2019/2021 完全沒有的 diffusion/FM 生成範式，正是 shift 網格最該有的一格新負領土。以 DFADD 抽 20k 填掉原 2021 DF 那一格。
- **In-the-Wild：維持**。它是 Q1 第一週的 smoke-test（全集跑一次前向 ~10 分鐘），也是唯一「真實名人流通」風味的 unseen 格，換掉反而失去便宜的驗證場地。
- **ASVspoof 2019 LA in-domain 訓練種子：維持為主，ASVspoof 5 train 僅列可選備選**。換 in-domain 種子會改變「seen 分布」的定義並帶進 SSL 復現風險；ASVspoof 5 crowdsourced 種子雖更貼近現實，但**屬於「可換可不換」，不是本方向的痛點**，教授建議留在可選欄，不強推。

**我擋下的偷加**：landscape 一次擺出 MLAAD v10 + DFADD + SpeechFake 開源部 + Deepfake-Eval-2024 四個。若四個全上，4 個 source 格就變 7–8 格——**評估前向、RQ3 對抗搜尋、悲觀重跑全部翻倍，這是換資料集偽裝的範圍膨脹**。定稿的 grid 是 4×3，替換後仍須是 4×3。**Deepfake-Eval-2024 只作可選 eval-only 備選**（scrape 散布受限🟡），要用就得**替換**某一格、不得新增。

**通過五項驗收**（以 DFADD 換 2021 DF 格為例）
- 更新：DFADD 2024（ICASSP 2025），vs 2021 DF；MLAAD v10 2025 vs v5。
- 可取得：DFADD HuggingFace 開源直接下載；MLAAD v10 deepfake-total.com 公開。皆🟢非申請制，數 GB。
- 算力相容：沿用分層抽 20k，評估池仍 ≈9.2 萬筆，格數不增，GPU 430–520 不動。
- 契合原方法：只換「某一格裝什麼樣本」，`s / g / R–C` 介面與一次前向快取骨架一行不改。
- 時效性一句話：讓「unseen-generator shift」量到的負領土反映 2024–2025 的 diffusion/FM 世代，而非已被偵測器見慣的 2021 生成器。

**正式題目提議（★ 我最有把握的方向之一）**
- 中：《分布偏移下語音深偽偵測的選擇性預測基準》
- 英：*A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*
- 理由：去掉「不知道就別答」這句口語 hook。「選擇性預測基準（selective-prediction benchmark）」本身即為學界成熟的論文類型名，單一 deliverable、名詞收尾，翻譯乾淨，最符合學位論文慣例。

---

## D2：真實通道上音訊深偽反制訊號存活的樂觀偏差審計

**現用舊資料集**
- real 類：ASVspoof 2019 LA real / In-the-Wild real / MLAAD real
- fake：3 家開源 TTS/VC（XTTS-v2、VITS、YourTTS，2022–2023 世代）
- 真實通道錨：RTCFake（定稿當「月 0 才知能否取得的單點故障」）
- watermark：AudioSeal（單一）
- 模擬臂：Opus + AMR-WB

**建議替換**
- **RTCFake：維持，但由「單點故障」降級為「已確認可下載」**。這不是換新，是**解除風險**——landscape 已查證 `JunXueTech/RTCFake` 在 HuggingFace 公開可下載、~600h、offline/online 精確配對。定稿 D2 最大的失敗風險（月 0 拿不到）在事實層已緩解。**保留月 0 go/no-go，但改為只確認「學術重散布條款」而非「能否取得」**。
- **fake 世代 XTTS/VITS/YourTTS（2022–2023）→ 2025 世代開源 TTS（維持 3 家不變）**：反制訊號要在 2024–2025 世代 fake 上測存活，量出來的 γ 才是 2026 的「通道折扣係數」。以 F5-TTS / CosyVoice 2 / 一個 codec-based 生成器等 2025 開源系統**等量替換**原 3 家，管線不變。
- **real 類：維持**（ASVspoof19/In-the-Wild real）。SpoofCeleb（2024 in-the-wild）雖更貼近真實錄音，但受 VoxCeleb 非商用衍生授權約束🟡，且換 real 載體不改變「真實−模擬差分存活」的量測——**僅列備選，不採為主力**。
- **AudioSeal：維持**（唯一第三方可自由嵌入/偵測的開源 watermark，SynthID 定稿已砍）。
- **模擬臂 Opus/AMR-WB：維持**。

**我擋下的偷加（D2 是全案最容易被偷加的方向——它排 #5、退路最脆，任何「順便多測一點」都會壓垮日曆）**：
1. **ADD-C（2025 模擬通道集）不得升為「模擬側對照基準」新軸**。D2 的模擬臂已由 Opus/AMR-WB 自建，再拉 ADD-C 進來對照就是新增一條資料處理線與一組評估格。→ 至多在 discussion 引用，不進實驗。
2. **SpoofCeleb real 臂不得新增**（見上，備選）。
3. **fake 世代只能等量替換 3 家，不得因「新世代很多」擴成 5 家**。

**通過五項驗收**（以 fake 世代替換為例）
- 更新：F5-TTS / CosyVoice 2 等 2025 開源 vs XTTS/VITS/YourTTS 2022–2023。
- 可取得：皆 HuggingFace 開源🟢；RTCFake `JunXueTech/RTCFake`🟢（散布條款月 0 確認）。
- 算力相容：分層抽 20k 不變、~30 通道條件不變、GPU ≈510 不動。
- 契合原方法：fake 只是灌進審計台的探針素材，通道管線與 fixed-FPR 差分協定一行不改。
- 時效性一句話：讓樂觀偏差 γ 是「2025 世代 fake × 可得真實通道」的折扣係數，而非 2022 世代的過期數字。

**正式題目提議**（信心中等，見下方我最有把握的兩個）
- 中：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》
- 英：*Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*
- 理由：去掉「模擬騙了我們多少」問句 hook。保留定稿已收斂的「樂觀偏差—畸變層歸因」連體（一個問題的量測＋歸因兩層），冒號分隔主副標，符合慣例。

---

## D3：被動語音深偽偵測的調適式洗訊攻擊成本上界地圖

**現用舊資料集**
- ASVspoof 2019 LA / 2021 DF（分層抽 20k 確認池 / 10k 搜尋池）
- In-the-Wild、MLAAD（unseen-generator 軸子集）
- laundering 工具鏈：EnCodec/DAC + Opus/AMR-NB/μ-law/MP3/AAC
- 偵測器：AASIST + RawNet2 + XLS-R backend + 自建 Mahalanobis baseline

**建議替換（這是全案最有說服力的一次替換）**
- **laundering 對象 2021 DF + MLAAD → CodecFake+（2025）+ DFADD（2024）**：RQ2 的承重宣稱是「neural codec transcode 是零金錢、物理不可逆的必殺動作」。CodecFake+ 是 31 開源 neural codec + 17 codec-based 生成系統的最大公開集，**把 neural codec 世代從假想威脅變成可實測的 2025 fake**，與 RQ2 直接同構；DFADD 補上 diffusion/FM 一格。以兩者分層抽樣填掉原 2021 DF + MLAAD 的搜尋/確認池內容。
- **ASVspoof 2019 種子 → ASVspoof 5（2024）：可選升級，僅取其 TTS/VC spoof + codec 條件部分**，抽 20k。crowdsourced 非棚錄 + 內建 neural codec 條件同時服務 in-domain 種子與 unseen 對象。
- **In-the-Wild：維持**（unseen real 風味子集，便宜）。

**我擋下的偷加（D3 最危險的一個陷阱，教授必須明文釘死）**：
> **若採用 ASVspoof 5，只准用它的 TTS/VC spoof 與 codec 條件，嚴禁碰它的 adversarial 子集（Malafide / Malacopula）。** D3 定稿已一刀砍掉白盒 PGD 驗證整段（兩位審查者一致必砍）。ASVspoof 5 首次內建 adversarial 攻擊——一旦有人以「新資料集剛好有 adversarial，順便測一下」把它拉進來，等於偷偷把砍掉的白盒對抗軸復活，這是換資料集偽裝的範圍回歸，我當場擋下。laundering 動作空間維持 ≤8、偵測器維持 4 個、greedy 搜尋維持不變、20k/10k 抽樣維持不變。

**通過五項驗收**（以 CodecFake+ 換 laundering 對象為例）
- 更新：CodecFake+ 2025 / DFADD 2024，vs 2021 DF + 2019 LA。
- 可取得：CodecFake+ `CodecFake/CodecFake_Plus_Dataset`🟢（多 .part 合併）、DFADD HuggingFace🟢；ASVspoof 5 Zenodo🟢。
- 算力相容：維持 20k 確認 / 10k 搜尋池，動作空間與偵測器數不增，GPU 610 不動。
- 契合原方法：CodecFake+ 只是更新「laundering 貪婪搜尋所打的 fake 池」，recipe-level greedy、可控植入可逆性標註、成本代理三軸全部沿用。
- 時效性一句話：讓「攻擊成本上界 + 可逆/不可逆分解」打的是 2025 neural-codec 世代 fake，把「neural codec 必殺」從假想錨實測成 2026 的攻擊事實。

**正式題目提議**（信心高，但把兩個正式化名額留給更乾淨的 D1/D4；此處仍給定案）
- 中：《被動語音深偽偵測之調適式洗訊攻擊成本上界地圖》
- 英：*An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- 理由：去掉「攻擊者付的絕不超過多少」口語 hook。「adaptive laundering」譯為「調適式洗訊」（音訊去識別/洗白之對抗性版本），「攻擊成本上界地圖」為單一 deliverable 名詞收尾。

---

## D4：詐騙情境條件下語音深偽偵測的評估效度審計（繁中）

**現用舊資料集**
- real 類：Common Voice zh-TW + AISHELL + 公開廣播 + ASVspoof/In-the-Wild real
- ~165 條反詐/刑事局公開話術腳本（自建刺激）+ 中性文本對照臂
- fake：2 家開源情緒可控 TTS/VC（VITS 系 / OpenVoice 類，2022–2023）
- 通道：offline codec；品質協變量 UTMOS + ECAPA

**建議替換（唯一該換、也只需換這一處）**
- **fake 生成器 2 家開源（2022–2023）→ 2 家 2025 世代 zh 開源情緒 TTS（維持 2 家不變）**：如 CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 中選 2 家。「到達耳朵的三秒」要用 2025 能穩定產生哭腔/急迫的當代 zh TTS，才代表 2026 詐騙工具。
- **無現成 zh-TW deepfake 集——自建定位完全不變**（landscape 已確認）。
- **real 類、話術腳本、通道、品質協變量：全部維持**（載體 real 年份不影響其作為 bona fide 的效力）。

**我擋下的偷加（D4 有兩個要盯死的地方）**：
1. **fake 只能等量替換為 2 家，不得因「2025 世代選擇多」擴成 4 家**。定稿已一刀砍掉閉源臂、把 fake 收斂為純 2 家開源；趁換世代偷加家數，就是重蹈範圍膨脹。
2. **SpeechFake ZH / CFAD 僅作 zh-CN 對照臂，嚴禁升為 zh-CN 主軸或第二實驗**。它們只服務「證明落差非單一 zh-TW 腔調 artifact」這一句話，且腔調非 zh-TW（外部效度限制須明標）。D4 已有「情緒 zh-TW TTS 月 0–1 硬 go/no-go」，若把 zh-CN 對照升格，等於偷換方向的主體語言與尺度。
3. 月 0–1 情緒 zh-TW TTS 硬關卡維持不變——換上 2025 世代 TTS 不代表取得性風險消失，go/no-go 照走。

**通過五項驗收**
- 更新：CosyVoice 2 / F5-TTS 等 2025 世代 vs VITS/OpenVoice 2022–2023。
- 可取得：皆 HuggingFace/GitHub 開源🟢；CFAD/SpeechFake ZH🟡（zh-CN，僅對照）。
- 算力相容：自建 ~2–3 萬筆規模不變、2 家不變、GPU ≈180 不動。
- 契合原方法：只換「fake 由哪個 TTS 生成」，多軸分層 × frozen 前向 × fixed-FPR recall × 品質配對一行不改。
- 時效性一句話：讓「詐騙現場素材」的合成器是 2025 能產哭腔/急迫的當代 zh TTS，量出的評估落差才對應 2026 詐騙者手上的工具。

**正式題目提議（★ 我最有把握的方向之一）**
- 中：《詐騙情境條件下語音深偽偵測的評估效度審計》
- 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scene Conditions*
- 理由：去掉「到達耳朵的那三秒」抒情 hook。「評估效度審計（evaluation-validity audit）」是明確的方法論類型名，單一 deliverable、名詞收尾、繁中定位清楚，最符合學位論文慣例。

---

## D5：通訊通道對音訊浮水印來源標記之可靠位元容量審計

**現用舊資料集**
- 載體語音：AISHELL-3 + LibriSpeech + ASVspoof19/In-the-Wild real（分層抽 ~10k 池）
- watermark：AudioSeal + WavMark + SilentCipher
- 通道：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC × PLR）+ neural codec（EnCodec/DAC/SpeechTokenizer × bitrate）
- baseline：AudioMarkBench（2024）

**建議：大體維持——這是「誠實說維持、不為換而換」的方向**
- **載體語音：維持**。它只是 watermark 的承載真音，年份不影響其功能，landscape 明確判定保留。
- **watermark 家族：維持**。AudioSeal / WavMark / SilentCipher 已是當前開源可得的**全部** learned watermark，無更新的開源替代品可換。
- **neural codec 通道（EnCodec/DAC/SpeechTokenizer）：維持**。這些本身就是當前世代 neural codec。
- **唯一該更新的是 baseline 前作錨點——補上「Will They Survive Neural Codecs?」（Interspeech 2025）**。這**不是換資料集、也不是加實驗**，而是把 D5「neural codec 通道容量塌陷」的定位對準 2025 最新的「watermark × neural codec」前作，讓時效性論證更硬（相對前作補上「可控植入 ground-truth 錨 + 索引構造」）。零 GPU、零新 pipeline、零新 RQ。
- CodecFake+ 至多作為「選 neural codec 條件時的參考」，**不作資料替換**——D5 的 pipeline 是把 watermark 嵌進真實載體再過通道，fake 語音世代不是它的核心輸入。

**我擋下的偷加**：D5 已誠實收窄，不硬撐「傳統 vs neural watermark 分類學」、不自刻 echo-hiding。本輪不得藉「有 CodecFake+ 這種新集」把 neural-codec 世代 fake 拉成新的載體軸或新的 watermark-family 軸——那會讓 RQ1 從「容量塌陷點（codec 軸）」滑回被砍掉的「watermark 分類學」。維持 codec 軸承重。

**通過五項驗收**（此處是「維持」判定，故逐項說明為何維持已達標）
- 更新：載體/watermark/neural codec 皆為當前最佳，無更新可換；時效性由 baseline 補 Interspeech 2025 前作達成。
- 可取得：現用皆🟢公開；新增前作為論文引用，無取得成本。
- 算力相容：完全不動，GPU ≈220。
- 契合原方法：不改任何 pipeline。
- 時效性一句話：把可靠 bit 容量地圖錨到 2025 最新的 watermark×neural-codec 前作之上，讓「塌陷點」論證站在最新基準線後方，而非 2024 只做模擬擾動的 AudioMarkBench。

**正式題目提議**
- 中：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》
- 英：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*
- 理由：去掉「還剩幾個 bit」口語 hook 與破折號金句。以「及其……可讀性判定」把政策判定從屬於容量審計（一個 deliverable 的兩層讀法），符合定稿已收斂的從屬結構與學位論文慣例。

---

## 教授總結：本輪守住的三條尺度線

1. **替換不新增**：D1 grid 維持 4×3、D3 動作空間維持 ≤8/偵測器維持 4、D4 fake 維持 2 家、所有大集維持 20k 分層抽樣。每一個新資料集都是**填掉一個舊格**，不是**多開一格**。
2. **兩個最危險的偷加已釘死**：D3 的 ASVspoof 5 adversarial 子集（會復活被砍的白盒軸）、D4 的 zh-CN 對照臂升格（會偷換方向尺度）。
3. **誠實維持**：D5 沒有真該換的資料集，就說維持，只更新 baseline 前作錨點——不為換而換。

---

## 回傳（純文字資料）

### 五個方向「舊 → 新」一行版
- **D1**：MLAAD v5 → MLAAD v10（2025）；ASVspoof 2021 DF 這一格 → DFADD（2024，diffusion/FM）；In-the-Wild 與 ASVspoof2019 in-domain 維持；grid 維持 4×3 不新增格（Deepfake-Eval-2024 僅可選 eval-only 備選，要用須替換不得新增）。
- **D2**：fake XTTS/VITS/YourTTS（2022–2023）→ 3 家 2025 世代開源 TTS（家數不變）；RTCFake 由「月 0 單點故障」降為「已確認 HuggingFace 可下載」（維持，風險解除，僅月 0 確認散布條款）；real 類與 AudioSeal 維持（SpoofCeleb 僅備選、ADD-C 不進實驗）。
- **D3**：laundering 對象 2021 DF + MLAAD → CodecFake+（2025）+ DFADD（2024）；ASVspoof 2019 種子 → ASVspoof 5（可選，僅取 TTS/VC + codec 條件，**嚴禁碰其 adversarial 子集**）；動作空間/偵測器/RQ/抽樣全不變。
- **D4**：fake 2 家開源（2022–2023）→ 2 家 2025 世代 zh 開源情緒 TTS（CosyVoice 2 / F5-TTS 等，**維持 2 家**）；CFAD / SpeechFake ZH 僅作 zh-CN 對照臂（外部效度須標明）；自建定位不變。
- **D5**：**維持**（載體/watermark/neural codec 皆當前最佳，無更新可換）；唯一更新為 baseline 前作補「Will They Survive Neural Codecs?」（Interspeech 2025），零 GPU、零新 RQ。

### 我提議的正式題目（中／英）
- **D1（★最有把握）**：《分布偏移下語音深偽偵測的選擇性預測基準》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*
- **D4（★最有把握）**：《詐騙情境條件下語音深偽偵測的評估效度審計》／ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scene Conditions*
- **D2**：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》／ *Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*
- **D3**：《被動語音深偽偵測之調適式洗訊攻擊成本上界地圖》／ *An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*
- **D5**：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》／ *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*
