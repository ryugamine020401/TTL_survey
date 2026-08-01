# TTS 領域統整：`tts-history` 87 篇封閉語料綜述與研究缺口推導

- 日期：2026-07-28
- 研究模式：Synthesize（封閉語料）
- 證據範圍：**只使用** `papers/tts-history/` 內以 `001`–`100` 命名的 87 個 PDF。未使用網路、survey、既有研究筆記或資料夾外文獻。
- 抽取方式：87 篇全部以 `pypdf` 抽出全文，逐篇取「首段（題名＋摘要＋引言）／結論或討論段／作者自陳限制句」三段作為證據；其中 7 篇 ISCA 影像式掃描檔（#005、#006、#008、#009、#011、#012、#013）無可抽取文字，改以逐頁影像閱讀首頁。
- 前置文件：本文延續並擴充 `2026-07-27-tts-history-closed-corpus-synthesis.md`（該文為 35 篇版本）。本文新增的是 **52 篇的新證據** 與 **第 6 節的研究缺口推導**，前者所已充分處理的逐篇紀錄不重複。
- 證據等級標記：**Verified**＝多篇論文原文直接支持；**Inference**＝本文的分析框架或推論，非文獻共識。

---

## 0. 一頁摘要

**Verified.** 這批文獻的領域是 **文字轉語音合成（TTS）中的「文字如何變成波形」這條主線**（back-end / waveform generation）。前端（text normalization、G2P、韻律標註）、評估方法學、資料集、Voice Conversion、deepfake 偵測被此語料**刻意排除**——這一點在第 6 節會成為判斷「什麼是真缺口、什麼只是語料盲點」的關鍵。

**Inference（本文主軸）.** 貫穿 60 年的單一問題是：

> **文字嚴重欠定語音。** 同一句文字對應無限多種合法波形。TTS 的全部歷史，就是「**這些缺失的資訊由誰提供、如何被約束**」的一連串不同答案。

Tacotron（#049）自己就這樣寫："TTS is a large-scale inverse problem: a highly compressed source (text) is 'decompressed' into audio."

七個時代 = 七種「殘餘資訊供應者」：人類專家 → 錄音資料庫 → 統計平均 → 深度回歸 → 端到端學習 → 顯式因子化 → 大規模預訓練＋一段 prompt。

**最重要的三個發現：**

1. **穩健性問題是「被交換掉」而不是「被解決」。** T6（FastSpeech/Glow-TTS/Non-Attentive Tacotron）在 2019–2021 幾乎消滅了漏字重複；T7 為了零樣本與表現力改回自回歸，問題全數復發（VALL-E、BASE TTS、VoiceCraft 皆自陳）。MaskGCT（#100）把這個兩難寫成正式對立：AR「韻律多樣但不穩健」，NAR「穩健但更標準化、較不多樣」。**這 87 篇裡沒有任何一篇同時拿到兩者。**
2. **資料飽和的邏輯在 2004 與 2024 重演，但沒人接上。** XIMERA（#019, 2004）發現語料超過約 30 小時後自然度不再提升，並斷定「瓶頸不在資料量，在成本函數本身」。NaturalSpeech 3（#094, 2024）的表 7 顯示 60K→200K 小時 Sim-O 只從 0.72 升到 0.73（已飽和），而 500M→1B 參數從 0.73 升到 0.78（未飽和）。**同一個「資料飽和時瓶頸在目標函數」的論證，2024 年沒有人重提。**
3. **合成停止當科學。** T1 的合成器是驗證語音產生理論的儀器（Klatt 1980/1987、Stevens 1994、Coleman 1990 都在辯論語言學理論）。2000 年之後這 87 篇裡**沒有任何一篇用合成器回頭推進人類語音的知識**。後果很實際：韻律出錯時，領域已無理論可訴諸，只剩「加更多資料」。

---

## 1. 領域是什麼，主要在幹嘛

### 1.1 任務

輸入文字（或音素序列），輸出可懂、自然、且符合指定條件（說話者／韻律／風格／語言）的語音波形。

### 1.2 這是一個欠定的反問題

文字的資訊率約 10–50 bit/s；24 kHz 16-bit 波形約 384 kbit/s。中間差了四個數量級。這四個數量級的資訊，必須由文字**以外**的來源補上。這就是本文的分析主軸。

Skerry-Ryan（#055）給了領域內最乾淨的定義：

> "Prosody is the variation in speech signals that remains after accounting for variation due to phonetics, speaker identity, and channel effects."

亦即「殘餘」定義。本文把它推廣：**每一代 TTS 都是在回答「殘餘由誰提供」。**

### 1.3 領域同時優化的目標（Verified，跨全語料）

可懂度｜自然度｜說話者相似度｜韻律／風格適切性｜穩健性（不漏字、不重複、不崩潰）｜延遲與吞吐｜模型體積｜可控性｜資料效率｜未見說話者泛化｜（2018 起）防濫用。

這些目標**互相衝突**，而且衝突關係在每個時代換一組。這是第 4 節的主題。

---

## 2. 領域的發展歷史

### 2.1 主線（Verified）

| 時代 | 年代 | 殘餘資訊由誰提供 | 說話者身份如何進入系統 | 品質上限由什麼決定 | 語料中的代表 |
|---|---|---|---|---|---|
| **T1** 規則／共振峰 | 1964–1994 | 人類專家的聲學語音學知識，寫成規則與參數 | 重寫參數集（Klatt 1980 約 20 個控制參數，每 5 ms 更新） | 「我們對語音產生的理解」有多好 | #002 Klatt 1980、#004 Klatt 1987、#005 Coleman、#008 Stevens |
| **T2** 單元選擇／串接 | 1990–2007 | 單一說話者的大型錄音庫，靠**搜尋**取回 | 重錄一個語料庫（數十至上百小時） | 語料覆蓋率＋拼接處是否可聽 | #011 Takeda、#012 Sagisaka ν-talk、#014 Hunt&Black、#019 XIMERA、#020 Multisyn |
| **T3** HMM 統計參數 | 1996–2016 | 語料的**統計平均**，由模型內插未見脈絡 | 模型自適應（MLLR／CSMAPLR），數分鐘資料即可 | vocoder＋模型精度＋over-smoothing（Zen 2009 的三因子） | #023 Yoshimura、#024 Tokuda、#027 GV、#030 Yamagishi、#031 Zen 綜述 |
| **T4** 神經參數（橋接） | 2013–2016 | 同 T3，只把決策樹回歸器換成 DNN／LSTM | 同 T3 | 同 T3（vocoder 仍在） | #035 Zen DNN、#038 MDN、#039 BLSTM、#043 Watts、#044 Merlin |
| **T5** 端到端自回歸 | 2016–2020 | `<text, audio>` 配對，端到端學習；**波形本身第一次被學會** | speaker embedding；末期 speaker encoder（數秒未轉寫音訊） | attention 對齊穩定性＋vocoder 速度 | #045 WaveNet、#049 Tacotron、#051 Tacotron 2、#056 SV2TTS |
| **T6** 平行化／單階段 | 2019–2024 | 同 T5，但殘餘被**顯式因子化**（duration / pitch / energy） | 同 T5 | 一對多建模能力 vs 輸出多樣性 | #063 FastSpeech、#067 Glow-TTS、#068 HiFi-GAN、#079 VITS、#080 NaturalSpeech |
| **T7** Codec LM／零樣本 | 2022– | 大規模預訓練＋一段 acoustic prompt 的 in-context learning | **3 秒 prompt，零微調** | 資料覆蓋＋AR 穩健性＋token 設計 | #081 SoundStream、#082 AudioLM、#084 VALL-E、#090 Voicebox、#094 NS3、#100 MaskGCT |

### 2.2 一條線就能說完的歷史（Inference）

**取得一個人的聲音，成本從「數十小時錄音＋專家調校」降到「3 秒音訊＋零訓練」。**

- Klatt 1980：手設約 20 個參數，逐時間點指定。
- Hunt & Black 1996：CHATR 用 10 分鐘到 150 分鐘的單一說話者資料庫。
- Yamagishi 2009：說話者自適應，數分鐘、且能用「不完美」的資料（HTS-2007 明確強調 robustness to less-than-ideal data）。
- Jia 2018（SV2TTS）：數秒**未轉寫**音訊，零樣本；同一篇論文首次寫下防濫用段落。
- Wang 2023/2025（VALL-E）：**3 秒 enrolled recording，不更新任何參數**。

這條線同時是本專案（Audio Deepfake 方向）最關鍵的一條線。

### 2.3 歷史裡真正的「斷點」只有四個（Inference）

語料清單給的 T1–T7 是七段，但用「**表示或資訊來源是否改變**」當判準，只有四次真正的典範轉移，其餘三段是鞏固期：

| 類型 | 時點 | 改變了什麼 | 證據 |
|---|---|---|---|
| **斷點 1** | 1990 前後 | 知識 → 資料；生成 → 搜尋 | Takeda 1990 明說「no systematic method has been found to control unit attributes」，改用非均勻單元搜尋 |
| **鞏固** | T2 內部 | 搜尋準則從人工權重 → 可訓練 | Hunt&Black 1996 用回歸訓練權重取代手調；Black&Taylor 1997 用分群預先計算 target cost |
| **斷點 2** | 1999–2000 | 實例 → 分布；取回 → 生成 | Yoshimura 1999 + Tokuda 2000：spectrum/pitch/duration 統一在一個 HMM 內，語音**從模型本身產生** |
| **鞏固（T4）** | 2013–2016 | **只換回歸器** | Watts 2016（#043）是這件事的證明：把 HMM→DNN 拆成三個變因逐一驗證，發現只有「決策樹→DNN」與「state→frame」有效，「分離→合併 stream」無效。這說明 T4 不是新典範 |
| **斷點 3** | 2016 | 特徵 → 波形；pipeline → 端到端 | WaveNet 直接建模 raw audio；Tacotron 從字元直接學對齊 |
| **鞏固（T6）** | 2019–2021 | 把 T5 的殘餘顯式化＋平行化 | FastSpeech 2 直接說明是在解 FastSpeech 的 teacher-student 複雜性與 one-to-many |
| **斷點 4** | 2022 | 訊號 → token；模型即聲音 → prompt 即聲音 | AudioLM／VALL-E：TTS 從「條件式訊號回歸」變成「條件式語言建模」 |

**重要反例（Verified）：** 2016 之後 vocoder、對齊、聲學模型、說話者條件、音訊表示是**平行推進**的，不是接力。HiFi-GAN（T6，2020）服務的是 Tacotron 2（T5，2018）；DiffWave／WaveGrad 與 FastSpeech 2 同期但互不依賴。任何把 T1–T7 讀成「嚴格時間取代」的敘事都是錯的。

---

## 3. 技術演進：五條半獨立的軸

用單一軸描述技術演進會失真。這 87 篇顯示至少五條軸各自演進，且**不同步**。

### 軸 1：輸入表示

手設聲學參數軌跡（Klatt 1980）→ 音素＋人工韻律標註 → 完整語言學特徵向量（Zen 2013 說「典型系統約 50 種 context 類型」）→ 字元／音素（Tacotron 2017）→ 音素＋acoustic prompt（VALL-E 2023）→ 字元＋filler token（E2 TTS 2024，連 G2P 與 duration model 都拿掉）

### 軸 2：中間表示（最能區分時代的一條軸）

共振峰參數 → **真人波形片段**（T2 沒有中間表示，直接是波形）→ mel-cepstrum＋F0＋duration（＋STRAIGHT/WORLD vocoder）→ mel-spectrogram（T5/T6）→ **離散 codec token**（SoundStream/EnCodec → VALL-E）／**連續 latent**（NaturalSpeech 2）／**semantic + acoustic 雙層 token**（AudioLM、SPEAR-TTS、MaskGCT）／**SSL-based speechcode**（BASE TTS）

AudioLM（#082）是這條軸的關鍵論證：單一 tokenizer 無法同時給「高重建品質」與「長程結構」，所以必須混合語意 token（來自 masked LM）與聲學 token（來自 codec）。**這個 trade-off 至今未被單一表示解決。**

### 軸 3：生成機制

規則展開 → Viterbi 搜尋（Hunt&Black 把單元庫視為 state transition network，明說「has many similarities to HMM-based speech recognition」）→ ML 參數生成（MLPG，Tokuda 2000）→ 前饋回歸（DNN/LSTM）→ AR seq2seq＋attention → NAR（flow / GAN / diffusion）→ codec LM（AR）／masked generative（MaskGCT）／flow matching（Voicebox、E2 TTS）

### 軸 4：對齊機制（領域裡最反覆的一條）

手工時長規則（Klatt 1987 的 incompressibility constraint）→ target/concatenation cost → HMM 狀態時長 → **HSMM 顯式時長**（Zen 2007 修正了「訓練時沒有時長模型、合成時卻用它」的不一致）→ attention（Tacotron）→ 外部 teacher 抽時長（FastSpeech）→ **MAS 自行搜尋單調對齊**（Glow-TTS，不需外部 aligner）→ 可微分時長（Parallel Tacotron 2）→ 隱含（infilling／filler token；E2 TTS 完全不用 duration model）

這條軸很清楚地**繞了一圈回到原點**：從顯式時長出發，經過 attention，再回到顯式時長，最後又取消。

### 軸 5：說話者身份如何進入

參數重寫 → 重錄語料庫 → 模型自適應（MLLR/CSMAPLR，Yamagishi 2009）→ 可訓練 speaker embedding（Deep Voice 2）→ 獨立訓練的 speaker encoder（SV2TTS，零樣本）→ **acoustic prompt 的 in-context learning**（VALL-E、Voicebox、Seed-TTS）

### 半條軸：責任與安全

2018 年 SV2TTS 首次出現（"we verify that voices generated by the proposed model can easily be distinguished from real voices"）→ 之後成為 T7 的標配段落。演進形式：自建偵測分類器（AudioLM 高準確率、SPEAR-TTS **僅 82.5%**、SoundStorm 98.5%）→ 不開源（BASE TTS、UniAudio 不釋出 checkpoint）→ 浮水印（Seed-TTS 多層浮水印）。但這條軸**從未有一篇獨立研究**，見第 6 節。

---

## 4. 領域常遇到的問題

以下七個問題，每一個都跨越三個以上時代，且每個時代換一個名字。

### 4.1 一對多映射與 over-smoothing

**問題：** 同一段文字有無限多種說法。任何以平均為目標的模型都會塌陷到「悶」的平均值。

| 時代 | 症狀名稱 | 修法 |
|---|---|---|
| T3 | over-smoothing、muffled sound | Global Variance（Toda 2005，明說「generated trajectory is often excessively smoothed due to the statistical processing. Using the over-smoothed trajectory causes the muffled sound」） |
| T4 | unimodal objective、no variance | Mixture Density Network（Zen 2014 明列兩個限制：缺變異數、目標函數單峰） |
| T5 | averaged prosodic distribution | GST（#054）、prosody transfer（#055） |
| T6 | one-to-many mapping | FastSpeech 2 的 variance adaptor（pitch/energy/duration 當條件輸入）；VITS 的 stochastic duration predictor；diffusion |
| T7 | 「更標準化、較不多樣」 | MaskGCT 直指 NAR 系統 "producing more standardized but less diverse speech" |

**這 20 年來換了五種數學工具，問題本身沒變。**

### 4.2 對齊與穩健性（漏字、重複、幻覺）

- T2：Zen 2009 綜述說 unit selection 的問題是 "spurious errors... a single bad join in an utterance can ruin the listeners' flow. It is not possible to guarantee that bad joins will not occur."
- T5：attention 失敗。Battenberg 2020（#061）整篇在處理長句對齊崩潰；Deep Voice 3 專節列 error modes。
- T6：**幾乎解決。** FastSpeech「almost eliminate the problem of word skipping and repeating」，在 hard cases 把 Transformer TTS 的 34% 錯誤率降到近乎 0；Non-Attentive Tacotron 引入 unaligned duration ratio / word deletion rate 兩個大規模穩健性指標。
- T7：**全數復發。** VALL-E："some words may be unclear, missed, or duplicated... disordered attention alignments exist and no constraints to solving the issue."；BASE TTS："occasionally produces hallucinations and cutoffs... an inherent problem with the autoregressive LM approach."；VoiceCraft："long silence and scratching sound that occasionally occur during generation."；NaturalSpeech 2 把 AR codec LM 的問題總結為 "error propagation... word skipping, repeating, and collapse."

### 4.3 品質瓶頸每個時代換一個名字

Zen 2009（#031）提出至今仍最好用的三因子框架：**vocoder、聲學模型精度、over-smoothing**。之後每一篇都在挑其中一個打：

- Zen 2013（DNN）：「This paper addresses the accuracy of acoustic models.」（明說只打第二個）
- WaveNet 2016：打掉第一個（vocoder）
- Toda 2005、Zen 2014：打第三個

到了 T7，三因子變成新的三因子：**codec 重建上限、token 設計、prompt 覆蓋**。SoundStream/EnCodec 是第一個；BASE TTS 說「Selecting the right discrete representation for GPT-style TTS is crucial. More research is needed to establish how different properties of speechcodes translate into end-to-end system quality」是第二個；VALL-E 的 data coverage 段落是第三個。

### 4.4 資料的「規模 vs 品質」永遠衝突

- XIMERA 2004：「From the recording and use of large corpora, we have learned that extending the corpus size introduces a **new factor of degradation** in naturalness, i.e., voice quality variation.」——語料變大，同一說話者的音質漂移反而造成可聽的不連續。
- VALL-E 2023：「Large-scale data crawled from the Internet cannot meet the requirement, and always lead to performance degradation.」
- Voicebox 2023：訓練資料 "neither filtered nor enhanced"（把問題丟給模型容量）
- Seed-TTS 2024：對含背景音樂或過多噪音的 prompt 表現不佳

**同一個張力，20 年，三種不同的處理策略（縮小語料 / 過濾 / 硬吃），沒有共識。**

### 4.5 速度與延遲

每個時代都重打一次，且**從未有共同座標**：
Klatt 1980（軟體 vs 硬體）→ Zen&Sak 2015（單向 LSTM 做串流低延遲）→ WaveNet 太慢 → Parallel WaveNet（20×）／WaveRNN（行動 CPU 即時）／MelGAN（100×）／HiFi-GAN（167.9×）→ diffusion 的步數 trade-off（WaveGrad 六步、Diff-TTS 加速取樣、Grad-TTS 顯式控制步數）→ SoundStorm（比 AudioLM 快兩個數量級）

**各篇的 RTF 在不同硬體上量測，語料中沒有任何一篇給出跨典範的「品質 vs 計算」Pareto 前緣。**

### 4.6 端到端從未真正端到端

- Tacotron 2017：宣稱端到端，但「We perform simple text normalization」
- Deep Voice 3 2018：future work 是「improving the implicitly learned grapheme-to-phoneme model」
- FastSpeech 2 2021：「we use an external high-performance alignment tool and pitch extraction tools, which may seem a little complicated」
- VITS 2021：「there remains a problem of text preprocessing.」
- Voicebox 2023：「depends on a phonemizer and a forced aligner... many existing phonemizers are word-based, which does not take neighboring words of the target into account... cannot accurately predict phonetic transcript because pronunciation is context-dependent in many languages (e.g., liaisons in French)」
- E2 TTS 2024：終於拿掉 G2P 與 duration model

**「端到端」被宣稱了 7 年才部分兌現。**

### 4.7 評估

- Blizzard Challenge 2005（#026）是這 87 篇裡**唯一一篇**評估方法學論文，且其動機正是「跨系統無法比較」。
- 到 2022/2024，NaturalSpeech（#080）仍必須**自己定義**什麼叫 human-level quality（用 CMOS 的 Wilcoxon 符號秩檢定 p ≫ 0.05），並用這個定義證明「先前數個系統其實沒達到」。**60 年後才需要定義驗收標準，本身就是證據。**
- T7 的事實標準指標是 WER（借 ASR）＋ SIM-O（借語者驗證）＋ CMOS。前兩者都是**代理指標**，且是向其他任務借的。

---

## 5. 怎麼切分時代（本文的建議切法）

語料清單的 T1–T7 適合當書目分群；但若要在論文裡當**論證骨架**，建議用兩層：

### 第一層：四個典範（依「殘餘資訊的來源」切，MECE）

| 典範 | 殘餘來源 | 對應 T | 該典範的**內在**上限 |
|---|---|---|---|
| **P1 知識驅動** | 人腦 | T1 | 人對語音產生的理解不足；規則寫不完（Klatt 1987 自陳：「we do not yet know the rules to do this in an optimal way」） |
| **P2 實例驅動** | 錄音庫中的具體實例 | T2 | 覆蓋率有限，且無法保證沒有壞接點（Zen 2009） |
| **P3 分布驅動** | 語料的參數化機率分布 | T3＋T4 | 平均化必然 over-smooth；vocoder 是硬上限 |
| **P4 生成模型驅動** | 大規模資料學到的生成分布＋條件（prompt） | T5＋T6＋T7 | 條件不足以決定輸出時，模型會自己編（幻覺）；資料覆蓋決定一切 |

**注意 P3→P4 的界線在 2016（WaveNet／Tacotron），不在 2013。** T4 屬於 P3，因為它只換回歸器——Watts 2016 用受控實驗證明了這件事。

### 第二層：每個典範內部依「當代自認的瓶頸」切

這是原本的 T1–T7，保留即可，但建議在論文中改稱「階段」而非「世代」，並明確標註 T5/T6 是**平行推進**而非接續。

### 為什麼建議這樣切（Inference）

因為它讓「缺口」可被推導。若只按模型名稱切（Tacotron 時代、VALL-E 時代），缺口只能靠列舉；按「殘餘來源」切，就能問一個可證偽的問題：**在目前的典範下，哪些殘餘資訊仍然沒有任何來源？** 第 6 節就是這個問題的展開。

---

## 6. 研究缺口：推導程序與結果

> 這一節是本文的重點。以下先給出可稽核的推導程序，再給結果。任何人可以拿同一批論文重跑這個程序來檢驗結論。

### 6.0 推導程序（三步）

**Step 1 — 建立 MECE 的問題空間。** 用兩個正交座標系張成一張表。

**座標系 A：一段語音波形中，有哪些資訊必須被決定？**（MECE：合起來窮盡波形，彼此不重疊。此切法對應 NaturalSpeech 3 的 content / prosody / timbre / acoustic-detail 因子化，再細分為七項。）

| | 資訊類別 |
|---|---|
| A1 | 語言內容（音素序列、發音、同形異音） |
| A2 | 時間結構（時長、節奏、停頓） |
| A3 | 韻律（F0、音強、重音、語調、焦點） |
| A4 | 音色／說話者身份 |
| A5 | 風格／情緒／副語言（笑聲、猶豫、back-channel） |
| A6 | 通道／錄音環境（噪音、殘響、頻寬） |
| A7 | 訊號細節（相位、諧波結構、噪音底） |

**座標系 B：一篇論文可以改變什麼？**（MECE：一個研究貢獻必然落在其一。）

| | 貢獻類型 |
|---|---|
| B1 | 表示（representation） |
| B2 | 生成機制（mechanism） |
| B3 | 條件化與控制（conditioning / controllability） |
| B4 | 資料（規模、來源、覆蓋） |
| B5 | 評估（量尺、判準、基準） |
| B6 | 效率與部署（延遲、體積、串流） |
| B7 | 責任與安全（濫用、偵測、浮水印） |

**Step 2 — 把 87 篇投影到 A×B 的 49 格。** 結果（Inference，逐篇歸主要貢獻）：

- **極密集**：A1–A3 × B1–B2（約佔全語料 6 成以上）、A7 × B1–B2（所有 vocoder／codec 論文）、A4 × B3（說話者條件那條線）
- **中等**：A2 × B2（對齊那條軸）、B6（效率，散佈在各代）、A5 × B3（GST、prosody transfer、PromptTTS 1/2、NS3）
- **稀薄**：A6（通道／環境）僅作為 prompt 的副產物被「保留」，從未被當成研究對象
- **接近空白**：B5（僅 #026 Blizzard 一篇）、B7（**0 篇**）、A1 × B1（前端，0 篇，語料刻意排除）

**Step 3 — 只把符合以下三項判準的格子認定為「缺口」，其餘視為待辦事項。**

| 判準 | 說明 |
|---|---|
| **C1 跨代持續** | 該問題被 ≥3 個不同時代的作者自陳為未解 |
| **C2 規模不可解** | 在現有典範下，單純增加資料或參數不會消除它（需有語料內證據支持） |
| **C3 可證偽** | 能被寫成一個有明確反例的研究問題 |

並把缺口分三類：
- **G-I 結構性空白**：該格幾乎沒有論文。
- **G-II 未解的跨代抱怨**：作者反覆自陳、從未關閉。
- **G-III 被替換而非被解決**：因典範更迭而從文獻消失，但問題本身仍在，且會復發。

---

### 6.1 先分離「語料盲點」與「真缺口」

這一步是誠實性要求。語料清單明文排除：前端、評估方法學、多語／低資源工程、資料集論文、Voice Conversion、speech editing、deepfake 偵測。

| 空白格 | 是語料盲點還是真缺口？ | 判斷 |
|---|---|---|
| A1 × B1（前端） | **主要是語料盲點**，但有殘餘真缺口 | 外部文獻補得上大部分。但 Voicebox 自陳的「word-based phonemizer 無法處理上下文相依發音（法語 liaison）」是在 back-end 內部也解不掉的，屬真缺口 |
| B5（評估） | **兩者皆是** | 外部有 Blizzard 系列與 MOS 方法學文獻可補；但「沒有任何指標度量韻律適切性與長篇連貫性」是真缺口——NaturalSpeech 2022 必須自己定義 human-level 就是證據 |
| B7（安全／偵測） | **兩者皆是，且真缺口更嚴重** | 見 6.2 的 GAP-1 |
| 多語／低資源 | **主要是語料盲點** | XTTS、VALL-E X、SPEAR-TTS 已在語料內部分覆蓋 |

**下文只列真缺口。**

---

### 6.2 八個研究缺口（依「對本專案的價值」排序）

---

#### GAP-1 ★ 所有防濫用宣稱都由攻擊方自評，語料中沒有任何獨立或對抗性驗證

- **座標**：B7 × 全部 A（結構性空白 **G-I**）
- **事實（Verified）**：87 篇中，**0 篇**以偵測或浮水印為研究主題。所有緩解措施都是生成模型作者在 broader-impact 段落自行附上的一段話：
  - SV2TTS 2018：「we verify that voices generated by the proposed model can easily be distinguished from real voices」（無數字）
  - AudioLM 2023：自訓分類器「with very high accuracy」
  - **SPEAR-TTS 2023：偵測器在平衡資料集上僅 82.5%**
  - SoundStorm 2023：98.5%（沿用 AudioLM 同一個分類器）
  - Seed-TTS 2024：多層浮水印＋說話者授權驗證
  - BASE TTS 2024 / UniAudio 2024：以「不開源」作為緩解
  - VoiceCraft 2024：反過來呼籲「more advanced models such as VOICECRAFT presents new opportunities and challenges to safety research」
- **為什麼是缺口而非待辦（C1/C2/C3 檢核）**：
  - C1 ✅ 2018–2024 六年、七篇、同一個處理方式，從未被獨立檢驗。
  - C2 ✅ 規模不可解——生成模型越大，攻擊方自評的偵測率反而**沒有隨之報告下降**，這本身可疑：SPEAR-TTS 的 82.5% 與 SoundStorm 的 98.5% 用同一族方法卻差 16 個百分點，且無人解釋。
  - C3 ✅ 可證偽命題：「以模型 M 自訓的偵測器，在 M 的最新版本／跨 codec／經過重壓縮後仍維持宣稱準確率。」預期為偽。
- **可操作的研究問題**：
  1. 把這 7 篇的自評偵測器在**跨模型、跨 codec、經 MP3/電話頻寬重壓縮**條件下重測，量化衰減。
  2. 建立「生成能力 ↔ 偵測難度」的對照表：以 2.2 的說話者身份軸為 x 軸（需要的目標音訊長度：數十小時 → 數分鐘 → 數秒 → 3 秒），量測偵測 EER 的變化。
- **對本專案的價值**：**最高。** 本專案方向是 Audio Deepfake，而這個語料恰好證明了「生成端的防護宣稱從未被獨立檢驗」——這是一個由封閉語料本身推導出來、有文獻證據支撐的正當研究缺口。

---

#### GAP-2 ★ 穩健性與多樣性的兩難：沒有任何一篇同時拿到兩者

- **座標**：A2＋A3 × B2（**G-III 被替換而非被解決**）
- **事實（Verified）**：MaskGCT 2025 把這個兩難寫成正式對立：

  > "AR-based TTS systems... offer diverse prosody but also suffer from problems such as poor robustness and slow inference speed. NAR-based models... require explicit text and speech alignment information as well as the prediction of phone-level duration, resulting in a complex pipeline and **producing more standardized but less diverse speech**."

  歷史軌跡：T5 有多樣性但不穩健 → T6 用顯式時長換到穩健但變標準化 → T7 為零樣本改回 AR，穩健性全數復發（VALL-E、BASE TTS、VoiceCraft、NS2 皆自陳）。
- **判準檢核**：C1 ✅（T5、T6、T7 三代）；C2 ✅（BASE TTS 在 100K 小時、1B 參數下仍自陳「an **inherent** problem with the autoregressive LM approach」——明確排除規模解）；C3 ✅
- **語料內的最佳候選解與其未驗證處**：MaskGCT（masked generative，非 AR 也不需 phone-level duration）與 E2 TTS（flow matching＋filler token，連 duration model 都不要）是兩條可能出路，但**兩篇都沒有報告 hallucination／cut-off 率**，只報 WER。WER 會低估幻覺（多說的話若通順，ASR 不一定罰）。
- **可操作的研究問題**：用 Non-Attentive Tacotron（#069）提出的 **unaligned duration ratio 與 word deletion rate** 這兩個 2020 年的指標，去測 2023–2025 的 T7 模型。這兩個指標在 T7 文獻中**完全消失**了——這本身是一個乾淨的、立即可做的實驗。

---

#### GAP-3 ★ 資料飽和後，沒有人回頭質疑目標函數

- **座標**：B4 × B5 交界（**G-II**，且是本文認為最被低估的一個）
- **事實（Verified）**：
  - XIMERA 2004（#019）：「Saturation was found at around 30 hours in the relationship between the corpus size and cost. This fact indicates that **further extending the corpus size does not contribute to improving naturalness as far as the present cost function is used, and that its improvement is indispensable.**」
  - NaturalSpeech 3 2024（#094）表 7／表 8：資料 1K→60K→200K 小時，Sim-O 為 0.64→0.72→**0.73**（第二段幾乎持平）；模型 500M→1B，Sim-O 0.73→**0.78**（仍在增長）。
  - VALL-E：「Even if we use 60K hours of data for training, it still cannot cover everyone's voice」——把飽和歸因於**覆蓋不足**，而非目標函數。
  - BASE TTS：「Our approach points towards **potential** Scaling Laws of LTTS models」——承認尚未建立。
- **推論（Inference）**：2004 年 XIMERA 在遇到飽和時做出的推論（瓶頸在成本函數）是正確的方法論；2024 年遇到同一現象時，領域一致地把它歸因於資料覆蓋，並繼續加資料。**沒有任何一篇問：現行的訓練目標（token 的 cross-entropy／flow-matching 的重建損失）是否本身就無法再區分「更好的語音」？**
- **判準檢核**：C1 ✅（2004、2024，且 T3 的 GV、T4 的 MDN 都是「目標函數不對」的間接證據）；C2 ✅（定義上：這正是「規模不可解」的那類問題）；C3 ✅
- **可操作的研究問題**：在固定模型與資料下，換用不同目標（含感知加權、對抗、偏好學習）看 Sim-O／CMOS 是否突破飽和線。Seed-TTS 的 RL 偏好偏置（preference biasing through RL）是語料中**唯一**朝這個方向的嘗試，且它自陳「Careful network tuning is required to achieve the optimal performance that balances these trade-offs afforded by RL」——尚未系統化。

---

#### GAP-4 韻律：40 年、5 個時代、同一句抱怨

- **座標**：A3＋A5 × B2＋B3（**G-II**，領域的永恆缺口）
- **事實（Verified）**，按時間排：
  - Klatt 1987：「a flexible formant synthesizer may permit manipulation of the voicing source characteristics over a sentence, but **we do not yet know the rules to do this in an optimal way**」
  - Clark 2007（Multisyn）：「The system as described here contains **no real control over prosody**... there are occasions where the resulting speech has primary phrasal stress placed inappropriately.」
  - Tokuda 2013（Proc. IEEE）：「In conversational speech, naturalness of prosody is **still insufficient** to properly convey nonverbal information, e.g., emotional expressions and emphasis.」
  - Skerry-Ryan 2018：「A substantial open question is how to disentangle the textual information implicit in the reference signal from the prosodic information... this is a somewhat **ill-defined task, and a more careful formalization of this problem is needed**.」
  - Seed-TTS 2024：「the model sometimes has limitations in scenarios requiring **nuanced emotion and contextual understanding**.」
- **判準檢核**：C1 ✅✅（五個時代）；C2 ✅（BASE TTS 用 100K 小時仍需另建專門測試集來量「emergent」韻律能力，代表規模只是把問題推後）；C3 ⚠️ **這是弱點**——Skerry-Ryan 2018 自己指出這個問題**尚未被良好定義**，因此難以直接證偽。
- **本文判讀（Inference）**：GAP-4 之所以四十年未解，關鍵不在模型，在 **C3 不成立**——領域從未有「韻律是否正確」的可操作定義。這使 GAP-4 實際上是 GAP-5（評估）與 GAP-8（失去科學回路）的下游症狀。**若要做這個題目，正確的切入點是先解 GAP-5，而不是再提一個模型。**

---

#### GAP-5 沒有任何指標度量「韻律適切性」與「長篇連貫性」

- **座標**：B5 × A3＋A5（**G-I 結構性空白**，部分為語料盲點）
- **事實（Verified）**：
  - 87 篇中只有 #026（Blizzard 2005）以評估為主題。
  - T7 的事實標準是 WER＋SIM-O＋CMOS。WER 是 ASR 代理，SIM-O 是語者驗證代理，**兩者都與韻律無關**。CMOS 只給整體偏好，不定位。
  - NaturalSpeech 2022 必須自己定義 human-level（Wilcoxon p ≫ 0.05），並據此判定「先前數個系統其實沒有達到」。
  - Non-Attentive Tacotron 2020 引入的兩個穩健性指標，在 T7 文獻中消失（見 GAP-2）。
- **判準檢核**：C1 ✅（2005、2018、2020、2022 各有一次「必須自己造指標」的紀錄）；C2 ✅；C3 ✅
- **可操作的研究問題**：建立以「同一文字的多種合法唸法」為基礎的**分布級**指標——目前所有指標都預設有唯一正解，這與 4.1 的一對多本質直接矛盾。這是一個定義清楚、且有邏輯必然性的缺口。

---

#### GAP-6 輸入介面停在「一個句子」：沒有語境、沒有對話

- **座標**：A3＋A5 × B3（**G-I**）
- **事實（Verified）**：87 篇的輸入一律是「句子（＋可選的 prompt）」。沒有一篇把**篇章語境**（前文說了什麼、對誰說、對話行為）當成條件。
  - NaturalSpeech 2022：future work 才要處理「longform audiobook voices... that have more dynamic, diverse, and **contextual** prosody」
  - Voicebox 2023：「may not transfer well to **conversational speech**... which is more casual and contains more non-verbal sounds such as laughing and back-channeling (e.g., um-hmm)」
  - Battenberg 2020：只解決長句的**對齊**泛化，不涉及語境內容
  - SoundStorm 2023 生成多輪對話，但條件是「標註 speaker turn 的逐字稿」，仍不是語境建模
- **判準檢核**：C1 ✅（T5 Battenberg、T6 NaturalSpeech、T7 Voicebox）；C2 ✅（BASE TTS 的「emergent prosody on textually complex sentences」仍限於**單句內**的文本理解）；C3 ✅
- **注意（Inference）**：GAP-4 的多數失敗例——重音放錯、疑問語調、焦點——在資訊論上**根本無法從單句推得**。這使 GAP-6 成為 GAP-4 的必要（非充分）條件。

---

#### GAP-7 屬性級可組合控制：沒有解耦，也沒有驗證

- **座標**：A4＋A5＋A6 × B3（**G-II**）
- **事實（Verified）**：
  - Voicebox 2023 最直白：「the model **does not allow independent control of each attribute**. In other words, one cannot ask the model to generate speech that resembles voice of one sample while resembling the emotion of another sample. We leave disentangled control of attributes... for future work.」
  - PromptTTS 2 2024：文字 prompt 的 one-to-many 問題——「not all details about voice variability can be described in the text prompt」
  - NaturalSpeech 3 2024 是語料中最完整的嘗試（FVQ 把波形分解成 content／prosody／timbre／acoustic detail 四個子空間），但其消融顯示去掉 factorization 會掉 0.12 Sim-O、0.68 WER，**代表因子化目前是靠架構強制而非驗證得到的**。
  - XTTS 2024 future work：「We also intend to **disentangle speaker and prosody information** to be able to do cross-speaker prosody transfer.」
- **關鍵漏洞（Inference）**：語料中**沒有任何一篇驗證「模型是否真的照著要求的屬性做了」**。所有控制論文都以「輸出品質沒有變差」＋「主觀上像」來論證，沒有一篇做「控制忠實度」的獨立量測。這與 GAP-5 同源。
- **判準檢核**：C1 ✅；C2 ✅（NS3 用 200K 小時仍需靠架構強制解耦）；C3 ✅

---

#### GAP-8 合成不再是科學：知識回流的迴路斷了

- **座標**：跨全表（**G-III**，最深、也最不可直接發表）
- **事實（Verified）**：
  - T1 的論文在辯論**理論**。Klatt 1980 的開場是「A need exists in **psychology and the speech sciences** for a flexible research tool in order to study speech perception through the synthesis of speech」；Klatt 1987 是一篇 57 頁的聲學語音學教程；Stevens 1994 在測試「發音參數 → 聲學參數」的映射關係；Coleman 1990（YorkTalk）在檢驗一個明確的語言學假說（"no-segment, no-rewrites"）。
  - Klatt 1987 甚至有整節談應用場景（失語輔具、盲人閱讀器、醫療），**這 87 篇中 1987 年之後沒有第二篇這樣做**。
  - 2000 年之後，語料中**沒有任何一篇用合成器回頭產生關於人類語音的新知識**。
- **判準檢核**：C1 ✅；C2 ✅（規模在定義上不會恢復解釋性）；C3 ⚠️（作為研究命題偏軟，但作為論文的 discussion 論點很強）
- **為什麼重要（Inference）**：這是 GAP-4 為何四十年未解的**根本原因**。當韻律出錯時，T1 有理論可以檢查哪條規則錯了；T7 只能加資料。GAP-4 → 需要 GAP-5（量尺）→ 量尺需要理論 → 理論來自 GAP-8 的迴路。**GAP-8 是 GAP-4/5/7 的共同上游。**

---

### 6.3 缺口之間的依賴關係（Inference）

不要把八個缺口當成八個平行選項，它們有明確的上下游：

```
GAP-8 (失去科學回路)
   └─> GAP-5 (沒有韻律/長篇的量尺)
          ├─> GAP-4 (韻律四十年未解)
          └─> GAP-7 (控制無法驗證)
GAP-6 (輸入停在單句) ──> GAP-4  [資訊論上的必要條件]
GAP-3 (資料飽和後不質疑目標函數) ──> GAP-4, GAP-2
GAP-2 (穩健 vs 多樣兩難) ── 獨立，且是目前最可立即實驗的
GAP-1 (安全宣稱無獨立驗證) ── 獨立，且與本專案方向最相關
```

**可立即動手、且不依賴其他缺口的只有兩個：GAP-1 與 GAP-2。**

### 6.4 給本專案的建議（Inference）

- **主線建議 GAP-1。** 它是結構性空白（B7 一篇都沒有）、與本專案 Audio Deepfake 方向直接對齊、且推導完全來自這個封閉語料本身，不需要外部文獻就能論證正當性。
- **GAP-2 適合當第二條線或方法章的實驗**：把 #069 的 unaligned duration ratio／word deletion rate 套用到 T7 模型，是一個成本低、結論明確、且在文獻中確有空白的實驗。
- **GAP-3 適合當 discussion 的思想貢獻**（XIMERA 2004 ↔ NS3 2024 的跨 20 年對照是一個很有辨識度的論點），但不建議當主線，工程量大。
- **GAP-4 不建議直接做**：它的 C3 不成立，做下去會變成「又一個韻律模型」。

---

## 7. 需要回報的三項語料層級更正

**更正 1（重要，需修改既有文件）：#012 是 ν-talk（nu-talk），不是 μ-talk。**

`2026-07-27-tts-100-paper-collection-list.md` 的「本次查證推翻的四項」第 2 點宣稱正確題名是 μ-talk，並說 ν-TALK 是錯的。**這個更正本身是錯的。** 證據：

- 掃描原件首頁標題逐字為 **「ATR ν-TALK SPEECH SYNTHESIS SYSTEM」**，內文寫「Non-Uniform Unit ( ν ) selection scheme」——ν 就是 **N**on-uniform 的字首代號。
- Hunt & Black 1996（#014）參考文獻第 2 項寫「ATR v-talk speech synthesis system」（v 為 ν 的抽取退化）。
- Black & Campbell 1995（#013）引言：「The ATR ν-talk system for Japanese」。
- Kawai 2004（#019）：「two TTS systems, namely ν-talk and CHATR」。

建議把清單改回 **ν-talk**，並記錄此次反轉。

**更正 2：#012 的 DOI 與清單不符。** 清單只寫「ISCA Archive」；PDF 內嵌 DOI 為 `10.21437/ICSLP.1992-125`（清單的頁碼 483–486 與 PDF 頁眉一致，可保留）。

**更正 3：7 篇為影像式掃描，無可抽取文字。** #005、#006、#008、#009、#011、#012、#013。任何以文字比對為基礎的自動化流程都會在這 7 篇上靜默失敗。建議在 README 標註，並保留本次產生的頁面影像流程（`pypdf` + `pillow` 抽取內嵌 XObject 影像）作為讀取方式。

---

## 證據限制

1. 本文的證據是每篇的「首段／結論段／限制句」，**不是全文精讀**。因此對「某篇論文有沒有做某件事」的否定陳述（尤其是 6.2 中「沒有任何一篇……」）的信心等級是**高但非確定**；若要寫進論文，建議對關鍵的 3–5 篇做全文複核，優先順序：#100 MaskGCT、#097 E2 TTS、#094 NaturalSpeech 3、#090 Voicebox、#085 SPEAR-TTS（附錄 E 的偵測實驗）。
2. 本語料**刻意排除**前端、評估方法學、多語／低資源、資料集、VC、speech editing、deepfake 偵測。6.1 已據此區分語料盲點與真缺口，但 GAP-1 與 GAP-5 的「零篇／一篇」是**相對於此語料**而言；宣稱它們是全領域缺口之前，必須另做一次針對這兩個主題的開放檢索。這是本文最重要的一項待驗證前提。
3. A×B 的 49 格投影是本文的分析框架（Inference），未經文獻計量驗證；每篇的主歸類是單一歸類，實際上多篇跨格。
4. 87 篇中缺 13 篇（付費牆與專書，見清單）。缺的多為 T1/T3 的期刊經典（Holmes 1964、MITalk 專書、Klatt&Klatt 1990、PSOLA、STRAIGHT）。這使 T1 與 T3 早期的敘事**偏向本語料實際持有的那幾篇**，特別是 PSOLA 與 STRAIGHT 缺席會低估「訊號處理」這條線在 T2/T3 的份量。

## 下一個最小驗證步驟

1. 對 #085 SPEAR-TTS 附錄 E、#082 AudioLM 第 IV-H 節做全文精讀，確認 GAP-1 的「自評偵測器」描述無誤（半天）。
2. 開放檢索一次「synthetic speech detection / audio watermarking 2018–2026」，確認 GAP-1 是全領域缺口還是僅是本語料盲點（一天）。**這是 GAP-1 能否成為主線的決定性檢查。**
3. 若 GAP-1 成立，即以 2.2 的「取得聲音所需音訊長度」時間軸作為論文第一張圖，把生成能力與偵測難度並置。

**停止／轉向條件**：若步驟 2 發現偵測與浮水印已有成熟且經獨立驗證的文獻體系，則 GAP-1 降級為背景章，主線轉向 GAP-2（穩健性指標在 T7 的消失），該缺口不依賴外部檢索即成立。
