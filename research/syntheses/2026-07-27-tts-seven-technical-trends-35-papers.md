# TTS 七大技術趨勢與 35 篇核心文獻

日期：2026-07-27  
研究模式：Synthesize + Validate  
研究問題：能否以目前時間軸上的七個節點為基礎，將 TTS 歷史改寫成七個有技術邏輯的趨勢群，並為每群建立足以支持後續討論的文獻集合？

## 結論

可以，但這七群不應被理解成彼此完全排斥的七段年份，而應理解成七種先後成為主流的「生成問題解法」。

劃分依據不是論文用了哪一種神經網路，而是：

1. 系統如何把文字轉成可發聲的表示？
2. 最終波形從規則、資料庫、聲學參數，還是離散 token 產生？
3. 時間對齊、韻律與說話者身分由哪個模組負責？
4. 當時最主要的品質或部署瓶頸是什麼？

因此，同一篇論文可能同時涉及兩個趨勢。本清單依其「主要技術貢獻」只歸入一群，避免重複計數。這是一種分析用的主歸類，不是宣稱文獻天然具有嚴格 MECE 邊界。

## 七群分類邏輯

| 趨勢群 | 約略活躍期 | 波形或聲學資訊從哪裡來 | 主要技術焦點 | 開啟下一群的瓶頸 |
|---|---:|---|---|---|
| T1 規則／共振峰合成 | 1980s–early 1990s | 人工指定的聲學參數與規則 | 可解釋的聲道、聲源及語音規則控制 | 規則工程龐大，自然度有限 |
| T2 單元選擇／串接 | 1990s–2000s | 大型真人語音資料庫中的片段 | 單元表示、target cost、join cost、路徑搜尋 | 資料庫與說話風格綁定，控制與擴展困難 |
| T3 HMM 統計參數式 | 1999–2012 | 機率模型預測的聲學參數，再交給 vocoder | spectrum、F0、duration 的統一建模、參數生成、適應 | 過度平滑與 vocoder 上限 |
| T4 神經統計參數式 | 2013–2016 | DNN／RNN 預測聲學參數，再交給 vocoder | 非線性映射、長期時間依賴、串流與工具化 | pipeline 仍依賴人工 linguistic features、對齊與 vocoder |
| T5 神經端到端／自回歸 | 2016–2019 | seq2seq 預測 spectrogram，神經 vocoder 產生波形 | attention、端到端學習、高品質 waveform、多說話者／零樣本聲音 | 推論慢、attention 可能漏字／重複、部署成本高 |
| T6 平行化／穩健對齊／單階段 | 2019–2022 | 非自回歸聲學模型、flow／GAN／diffusion vocoder，或單一生成模型 | 速度、單調對齊、穩定性、單階段 waveform generation | 大規模零樣本泛化與跨任務能力仍有限 |
| T7 Codec LM／大規模零樣本生成 | 2022– | codec／semantic token 或連續 latent，由 LM、flow、diffusion、masked model 生成 | 大規模預訓練、acoustic prompt、in-context learning、speech editing | 可控性、穩健性、來源追溯、濫用風險與跨分布檢測 |

**Verified：** 表中每個機制都能由下列原始論文的任務定義與方法描述支持。  
**Inference：** 活躍期與「主流趨勢群」是為理解歷史所做的綜合判斷；本次沒有做逐年論文量或引用量統計，不能把它解讀成精確的 popularity ranking。

## 35 篇核心文獻

符號說明：

- ★：目前七節點時間軸的單篇代表作。
- 「已發表」：已能在期刊、正式會議或正式 proceedings 查到出版紀錄。
- 「工作坊論文」：收錄於工作坊 proceedings，不把它誤標成期刊或主會議論文。
- 「預印本」：目前以 arXiv／研究機構技術稿為出版狀態；其影響力不等同於已通過同儕審查。

### T1 規則／共振峰合成：把語音知識寫成可控制參數

這一群不是單純代表「很早期」，而是代表生成的核心知識由人明確指定。五篇依序涵蓋合成器本體、規則架構、特定語言的規則、高階構音控制，以及與真人片段混合以突破自然度上限。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T1-01 ★ | 1980，期刊 | Dennis H. Klatt, *Software for a Cascade/Parallel Formant Synthesizer*。建立可程式化的 cascade/parallel formant synthesizer，是此群的技術基準。 | [DOI](https://doi.org/10.1121/1.383940) | `T1-01_Klatt_1980_Cascade_Parallel_Formant_Synthesizer.pdf` |
| T1-02 | 1990，工作坊論文 | John Coleman, *Yorktalk: “Synthesis-by-Rule” Without Segments or Rules*。顯示規則式 TTS 不只處理聲學參數，也牽涉語言表示與規則組織。 | [ISCA Archive](https://www.isca-archive.org/ssw_1990/coleman90_ssw.html) | `T1-02_Coleman_1990_YorkTalk.pdf` |
| T1-03 | 1990，會議論文 | Seung-Kwon Ahn & Koeng-Mo Sung, *The Rules in a Korean Text-to-Speech System*。提供跨語言實例，說明規則需同時涵蓋文字到音標與合成控制。 | [ISCA Archive](https://www.isca-archive.org/icslp_1990/ahn90_icslp.html) | `T1-03_Ahn_Sung_1990_Korean_TTS_Rules.pdf` |
| T1-04 | 1994，會議論文 | Kenneth N. Stevens, Corine A. Bickley & David R. Williams, *Control of a Klatt Synthesizer by Articulatory Parameters*。用高階構音參數降低直接控制大量聲學參數的複雜度。 | [ISCA Archive](https://www.isca-archive.org/icslp_1994/stevens94_icslp.html) | `T1-04_Stevens_1994_Articulatory_Control_Klatt.pdf` |
| T1-05 | 1994，工作坊論文 | Steve Pearson et al., *Combining Concatenation and Formant Synthesis for Improved Intelligibility and Naturalness in Text-to-Speech Systems*。混合真人片段與 formant rules，直接反映純規則式方法的自然度瓶頸。 | [ISCA Archive](https://www.isca-archive.org/ssw_1994/pearson94_ssw.html) | `T1-05_Pearson_1994_Concatenation_Formant_Hybrid.pdf` |

### T2 單元選擇／串接：把生成改寫成資料庫搜尋問題

核心轉變是「不再由規則合成每個聲學細節」，而是從真人錄音庫中找出最合適的片段。五篇涵蓋早期非均勻單元搜尋、選擇成本、經典 Viterbi 形式化、候選分群與成熟的開放領域系統。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T2-01 | 1990，會議論文 | Kazuya Takeda, Katsuo Abe & Yoshinori Sagisaka, *On the Unit Search Criteria and Algorithms for Speech Synthesis Using Non-Uniform Units*。代表大型語音庫與非固定單元搜尋的早期形成。 | [ISCA Archive](https://www.isca-archive.org/icslp_1990/takeda90_icslp.html) | `T2-01_Takeda_1990_Nonuniform_Unit_Search.pdf` |
| T2-02 | 1995，會議論文 | Alan W. Black & Nick Campbell, *Optimising Selection of Units from Speech Databases for Concatenative Synthesis*。明確處理大量候選片段的選擇問題。 | [ISCA Archive](https://www.isca-archive.org/eurospeech_1995/black95b_eurospeech.html) | `T2-02_Black_Campbell_1995_Optimising_Unit_Selection.pdf` |
| T2-03 ★ | 1996，會議論文 | Andrew J. Hunt & Alan W. Black, *Unit Selection in a Concatenative Speech Synthesis System Using a Large Speech Database*。以 target／concatenation cost 與 Viterbi search 形式化經典 unit selection。 | [University of Edinburgh](https://era.ed.ac.uk/items/07a1382d-ac96-4894-8532-b6c8eac44aad) | `T2-03_Hunt_Black_1996_Unit_Selection.pdf` |
| T2-04 | 1997，會議論文 | Alan W. Black & Paul Taylor, *Automatically Clustering Similar Units for Unit Selection in Speech Synthesis*。以決策樹分群縮小候選集合並結合 join cost。 | [ISCA Archive](https://www.isca-archive.org/eurospeech_1997/black97_eurospeech.html) | `T2-04_Black_Taylor_1997_Clustering_Units.pdf` |
| T2-05 | 2007，期刊 | Robert A. J. Clark, Korin Richmond & Simon King, *Multisyn: Open-Domain Unit Selection for the Festival Speech Synthesis System*。代表 unit selection 的成熟、可重建系統與其資料需求。 | [University of Edinburgh](https://www.research.ed.ac.uk/en/publications/multisyn-open-domain-unit-selection-for-the-festival-speech-synth) | `T2-05_Clark_2007_Multisyn.pdf` |

### T3 HMM 統計參數式：把語音改成可訓練、可生成、可調適的機率模型

這一群的辨識點不是「有使用 HMM」而已，而是聲譜、基頻與時長可由統計模型統一預測，再經 vocoder 重建。五篇涵蓋完整架構、參數生成、過度平滑修正、說話者適應與當時的領域總結。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T3-01 | 1999，會議論文 | Takayoshi Yoshimura et al., *Simultaneous Modeling of Spectrum, Pitch and Duration in HMM-Based Speech Synthesis*。把 spectrum、pitch、duration 納入同一 HMM-based framework。 | [ISCA Archive](https://www.isca-archive.org/eurospeech_1999/yoshimura99_eurospeech.html) | `T3-01_Yoshimura_1999_HMM_Spectrum_Pitch_Duration.pdf` |
| T3-02 ★ | 2000，會議論文 | Keiichi Tokuda et al., *Speech Parameter Generation Algorithms for HMM-Based Speech Synthesis*。建立由 HMM 與動態特徵產生連續聲學軌跡的核心算法。 | [HTS 官方網站 PDF](https://hts.sp.nitech.ac.jp/?plugin=attach&refer=Publications&openfile=tokuda_icassp2000.pdf) | `T3-02_Tokuda_2000_HMM_Parameter_Generation.pdf` |
| T3-03 | 2005，會議論文 | Tomoki Toda & Keiichi Tokuda, *Speech Parameter Generation Algorithm Considering Global Variance for HMM-Based Speech Synthesis*。針對統計平均造成的過度平滑與悶聲提出 GV 修正。 | [ISCA Archive](https://www.isca-archive.org/interspeech_2005/toda05b_interspeech.html) | `T3-03_Toda_Tokuda_2005_Global_Variance.pdf` |
| T3-04 | 2009，期刊 | Junichi Yamagishi et al., *A Robust Speaker-Adaptive HMM-Based Text-to-Speech Synthesis*。代表 average voice model 與少量目標語音適應能力。 | [University of Edinburgh PDF](https://www.cstr.ed.ac.uk/downloads/publications/2009/yamagishi-taslp09.pdf) | `T3-04_Yamagishi_2009_Speaker_Adaptive_HMM_TTS.pdf` |
| T3-05 | 2009，期刊綜述 | Heiga Zen, Keiichi Tokuda & Alan W. Black, *Statistical Parametric Speech Synthesis*。整理 HMM/SPSS 的優勢、缺點及與 unit selection 的差異，是判定此世代成熟度的重要綜述。 | [Nagoya Institute of Technology repository](https://nitech.repo.nii.ac.jp/records/5432) | `T3-05_Zen_Tokuda_Black_2009_SPSS_Review.pdf` |

### T4 神經統計參數式：替換聲學模型，但尚未拆掉舊 pipeline

這一群是 2000 與 2017 之間不能省略的橋。DNN／RNN 取代 HMM decision tree 來預測聲學參數，但系統仍依賴 linguistic features、時長／對齊處理與 vocoder，因此還不是 Tacotron 式端到端 TTS。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T4-01 ★ | 2013，會議論文 | Heiga Zen, Andrew Senior & Mike Schuster, *Statistical Parametric Speech Synthesis Using Deep Neural Networks*。以 DNN 學習 linguistic-to-acoustic mapping，超越相近參數量的 HMM baseline。 | [Google Research](https://research.google/pubs/statistical-parametric-speech-synthesis-using-deep-neural-networks/) | `T4-01_Zen_2013_DNN_SPSS.pdf` |
| T4-02 | 2014，會議論文 | Heiga Zen & Andrew Senior, *Deep Mixture Density Networks for Acoustic Modeling in Statistical Parametric Speech Synthesis*。從單一條件平均擴展到可表達多模態與變異數的輸出分布。 | [Google Research](https://research.google/pubs/deep-mixture-density-networks-for-acoustic-modeling-in-statistical-parametric-speech-synthesis/) | `T4-02_Zen_Senior_2014_Deep_MDN_SPSS.pdf` |
| T4-03 | 2014，會議論文 | Yuchen Fan et al., *TTS Synthesis with Bidirectional LSTM Based Recurrent Neural Networks*。把長期時間依賴放進 acoustic model，降低對外加動態限制的依賴。 | [ISCA Archive](https://www.isca-archive.org/interspeech_2014/fan14_interspeech.html) | `T4-03_Fan_2014_BLSTM_TTS.pdf` |
| T4-04 | 2015，會議論文 | Heiga Zen & Haşim Sak, *Unidirectional Long Short-Term Memory Recurrent Neural Network with Recurrent Output Layer for Low-Latency Speech Synthesis*。將神經 SPSS 推向低延遲、frame-synchronous streaming。 | [Google Research](https://research.google/pubs/unidirectional-long-short-term-memory-recurrent-neural-network-with-recurrent-output-layer-for-low-latency-speech-synthesis/) | `T4-04_Zen_Sak_2015_Low_Latency_LSTM_TTS.pdf` |
| T4-05 | 2016，工作坊論文 | Zhizheng Wu, Oliver Watts & Simon King, *Merlin: An Open Source Neural Network Speech Synthesis System*。把 DNN／RNN acoustic model、傳統前端與 vocoder 組成可重建工具鏈。 | [ISCA Archive](https://www.isca-archive.org/ssw_2016/wu16_ssw.html) | `T4-05_Wu_2016_Merlin.pdf` |

### T5 神經端到端／自回歸：讓模型直接學文字、聲學表示與聲音之間的映射

這一群包括兩個互相配合的突破：seq2seq attention 簡化 text-to-spectrogram，以及 neural vocoder 大幅提升 waveform 品質。後期再加入多說話者 embedding 與未見說話者的 voice cloning。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T5-01 | 2016，預印本 | Aäron van den Oord et al., *WaveNet: A Generative Model for Raw Audio*。證明自回歸神經模型能直接產生高品質 waveform；它是關鍵 enabling technology，但本身不是完整 text-to-spectrogram 架構。 | [Google Research](https://research.google/pubs/wavenet-a-generative-model-for-raw-audio/) | `T5-01_Oord_2016_WaveNet.pdf` |
| T5-02 ★ | 2017，會議論文 | Yuxuan Wang et al., *Tacotron: Towards End-to-End Speech Synthesis*。以 character-to-spectrogram seq2seq attention 大幅減少手工 pipeline。 | [ISCA Archive](https://www.isca-archive.org/interspeech_2017/wang17n_interspeech.html) | `T5-02_Wang_2017_Tacotron.pdf` |
| T5-03 | 2018，會議論文 | Wei Ping et al., *Deep Voice 3: Scaling Text-to-Speech with Convolutional Sequence Learning*。展示 fully convolutional attention TTS 的訓練速度、多說話者規模化與 attention error 分析。 | [ICLR 2018](https://iclr.cc/virtual/2018/poster/323) | `T5-03_Ping_2018_Deep_Voice_3.pdf` |
| T5-04 | 2018，會議論文 | Jonathan Shen et al., *Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions*。Tacotron 2 將 recurrent text-to-mel 與 WaveNet vocoder 結合，代表兩階段高自然度架構。 | [arXiv](https://arxiv.org/abs/1712.05884) | `T5-04_Shen_2018_Tacotron_2.pdf` |
| T5-05 | 2018，會議論文 | Ye Jia et al., *Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis*。以獨立 speaker encoder 與短參考語音實現未見說話者合成，直接連到後來的 voice cloning 威脅。 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper_files/paper/2018/hash/6832a7b24bc06775d02b7406880b93fc-Abstract.html) | `T5-05_Jia_2018_Speaker_Verification_to_TTS.pdf` |

### T6 平行化／穩健對齊／單階段：解決自回歸 TTS 的速度與穩定性

這一群不是只有 FastSpeech。它包含 text-to-mel 的非自回歸化、無外部 teacher 的單調對齊、GAN／diffusion waveform generation，以及直接由文字生成 waveform latent 的單階段整合。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T6-01 ★ | 2019，會議論文 | Yi Ren et al., *FastSpeech: Fast, Robust and Controllable Text to Speech*。用 duration predictor 與 length regulator 平行產生 mel-spectrogram，降低漏字與重複並提升速度。 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2019/hash/f63f65b503e22cb970527f23c9ad7db1-Abstract.html) | `T6-01_Ren_2019_FastSpeech.pdf` |
| T6-02 | 2020，會議論文 | Jaehyeon Kim et al., *Glow-TTS: A Generative Flow for Text-to-Speech via Monotonic Alignment Search*。以 flow 與 monotonic alignment search 移除自回歸 teacher aligner。 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper_files/paper/2020/hash/5c3b99e8f92532e5ad1556e53ceea00c-Abstract.html) | `T6-02_Kim_2020_Glow_TTS.pdf` |
| T6-03 | 2020，會議論文 | Jungil Kong, Jaehyeon Kim & Jaekyoung Bae, *HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis*。以 multi-period discriminator 提升高品質平行 neural vocoding。 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2020/hash/c5d736809766d46260d816d8dbc9eb44-Abstract.html) | `T6-03_Kong_2020_HiFi_GAN.pdf` |
| T6-04 | 2021，會議論文 | Zhifeng Kong et al., *DiffWave: A Versatile Diffusion Model for Audio Synthesis*。將非自回歸 diffusion 用於 conditional／unconditional waveform generation。 | [ICLR PDF](https://openreview.net/pdf?id=a-xFK8Ymz5J) | `T6-04_Kong_2021_DiffWave.pdf` |
| T6-05 | 2021，會議論文 | Jaehyeon Kim, Jungil Kong & Juhee Son, *Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech*。VITS 結合 VAE、flow、adversarial learning 與 stochastic duration predictor，代表平行單階段 TTS。 | [PMLR／ICML](https://proceedings.mlr.press/v139/kim21f.html) | `T6-05_Kim_2021_VITS.pdf` |

### T7 Codec LM／大規模零樣本生成：把語音變成可提示、可預訓練的生成表示

這一群的共同點不是都使用 Transformer，而是把語音壓縮到 token 或 latent 空間，使用短語音作 acoustic prompt，並藉大規模資料產生未見說話者與多任務能力。五篇刻意保留四條不同分支：codec LM、flow matching、latent diffusion、masked generation。

| ID | 年份／狀態 | 論文與技術角色 | 取得入口 | 建議檔名 |
|---|---|---|---|---|
| T7-01 | 2022，預印本；非文字條件 TTS | Zalán Borsos et al., *AudioLM: A Language Modeling Approach to Audio Generation*。以 semantic token 與 acoustic codec token 將長期結構及高保真音訊納入語言模型，是 VALL-E 類方法的重要前驅，但本身是 audio continuation，不應誤標為完整 TTS。 | [arXiv](https://arxiv.org/abs/2209.03143) | `T7-01_Borsos_2022_AudioLM.pdf` |
| T7-02 ★ | 2023，預印本 | Chengyi Wang et al., *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers*。VALL-E 把 TTS 改寫成 neural codec code 的條件語言建模，使用 3 秒 acoustic prompt 與 60K 小時資料。 | [Microsoft Research](https://www.microsoft.com/en-us/research/publication/neural-codec-language-models-are-zero-shot-text-to-speech-synthesizers/) | `T7-02_Wang_2023_VALL_E.pdf` |
| T7-03 | 2023，會議論文 | Matthew Le et al., *Voicebox: Text-Guided Multilingual Universal Speech Generation at Scale*。以非自回歸 flow matching 與 speech infilling 統一零樣本 TTS、編輯、去噪及 style conversion。 | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/2d8911db9ecedf866015091b28946e15-Abstract-Conference.html) | `T7-03_Le_2023_Voicebox.pdf` |
| T7-04 | 2024，會議論文 | Kai Shen et al., *NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers*。以 neural audio codec latent 與 diffusion 避免逐 token 自回歸生成，展示 speech prompt 與大規模零樣本能力。 | [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/035a73893121b4534bb3314e831050b1-Abstract-Conference.html) | `T7-04_Shen_2024_NaturalSpeech_2.pdf` |
| T7-05 | 2025，會議論文 | Yuancheng Wang et al., *MaskGCT: Zero-Shot Text-to-Speech with Masked Generative Codec Transformer*。以兩階段 semantic／acoustic token 的 mask-and-predict，代表 fully non-autoregressive、無顯式 text-speech alignment supervision 的近期分支。 | [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/74a31a3b862eb7f01defbbed8e5f0c69-Abstract-Conference.html) | `T7-05_Wang_2025_MaskGCT.pdf` |

## 建議閱讀順序

若一次讀 35 篇會失去歷史主線，可分三輪：

### 第一輪：七篇骨架論文

只讀七篇 ★ 論文的摘要、系統圖、方法與限制：

1. T1-01 Klatt
2. T2-03 Hunt & Black
3. T3-02 Tokuda et al.
4. T4-01 Zen et al.
5. T5-02 Tacotron
6. T6-01 FastSpeech
7. T7-02 VALL-E

目的：先回答「每一代到底改了系統中的哪一個核心假設」。

### 第二輪：七篇世代轉折論文

1. T1-05：規則式開始混合真人片段
2. T2-05：unit selection 成熟後暴露資料庫與風格綁定
3. T3-03：HMM 的過度平滑問題
4. T4-05：神經模型仍留在傳統 pipeline 內
5. T5-05：端到端架構轉向零樣本 voice cloning
6. T6-05：兩階段系統轉成平行單階段
7. T7-05：codec generation 從自回歸轉為 masked parallel generation

目的：確認為什麼舊世代不足以解決下一個問題。

### 第三輪：其餘 21 篇

用來驗證每群不是由單篇論文臆造出來，並補齊同一趨勢內的分支、成熟與限制。

## 下載與回存方式

建議把檔案放在同一資料夾，例如：

```text
papers/
└── tts-history/
    ├── T1-01_Klatt_1980_Cascade_Parallel_Formant_Synthesizer.pdf
    ├── ...
    └── T7-05_Wang_2025_MaskGCT.pdf
```

下載原則：

1. 優先使用上表的正式 proceedings、期刊 DOI、作者機構或大學典藏。
2. 若正式頁面只有摘要或付費版本，可先找作者版；不要用內容與版本不明的二次上傳檔。
3. 保留上述 ID 與檔名。之後可把「論文中的主張」逐一連回七個趨勢群，而不只靠標題整理。
4. VALL-E、AudioLM、WaveNet 的核心稿件在本清單中標為預印本；引用時必須保留出版狀態。

## 證據判定與限制

- **Verified：** 35 篇題名、年份、作者／出版入口與上述出版狀態已在 2026-07-27 由原始 proceedings、研究機構頁、作者頁或機構典藏逐項核對。
- **Verified：** 七群各含 5 篇，共 35 篇；七篇 ★ 與目前問題地圖的七個時間軸節點一致。
- **Inference：** 「七大技術趨勢」是依生成機制與瓶頸綜合出的研究框架，不是文獻界已公認且唯一的七段分期。
- **Unknown：** 尚未以逐年論文數、引用數、商用採用率或 benchmark 勝率量化「當年最流行」。因此目前可稱為「有原始文獻支持的代表性技術趨勢」，不可稱為經文獻計量證明的年度人氣排名。
- **重要反例：** 2016 之後的演進不是單一路徑。Waveform vocoder、alignment、acoustic model、speaker conditioning 與 audio representation 會平行進步，不能只用模型名稱排成單線。
- **範圍限制：** 本清單只整理 TTS 生成史，尚未證明任何 audio deepfake detection 研究缺口，也尚未處理 VC 主線。

## 建議與下一個最小驗證步驟

建議保留目前七個主節點，但在後續問題地圖中把它們標成「技術趨勢群」，不要標成互斥年代。

35 篇原文已於 2026-07-27 下載並驗證，紀錄見 `papers/tts-history/README.md`。下一個最小步驟是閱讀七篇 ★ 骨架論文，對每篇只先抽取六個欄位：

1. 它要解決的前代問題。
2. 輸入與輸出表示。
3. 生成或選擇機制。
4. 說話者身分如何進入系統。
5. 作者明示的限制。
6. 相對前一群新增了哪一種可被濫用的能力。

若七篇原文無法支持目前的世代轉折，就停止擴張問題地圖並修正分群；若能支持，再用其餘 28 篇做群內驗證，最後才連到 detection 假設失效與研究缺口。
