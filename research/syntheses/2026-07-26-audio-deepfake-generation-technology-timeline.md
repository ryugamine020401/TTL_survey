# Audio Deepfake 生成與聲音轉換技術時間軸：第一輪查證

日期：2026-07-26  
研究模式：Synthesize + Validate  
狀態：第一輪查證完成，年代邊界待作者確認

## 研究問題

若以年份作為敘事順序、以技術轉折作為分期依據，`Audio Deepfake` 的生成與聲音轉換技術可以如何分期？哪些論文足以代表當時的主流典範，或代表當時較高能力、較穩健的方法？

## 範圍

本時間軸追蹤兩條平行路線：

1. **Text-to-Speech（TTS）**：改變「說了什麼」，並逐漸能指定「由誰來說」。
2. **Voice Conversion（VC）**：保留原語音內容，改變說話者身分、風格或其他聲學屬性。

早期語音合成與聲音轉換是今日 audio deepfake 的**技術前史**；不能把 1990 年代的研究直接稱為當時的「deepfake」研究。

以下不納入本輪：

- 僅做壓縮、降噪或語音辨識，而不生成或改寫語音的技術；
- 一般音樂、環境聲音生成；
- Detection 方法；
- 商業產品排行與網路聲量。

## 如何判定「代表、主流、穩健」

| 標籤 | 操作性定義 |
|---|---|
| **主流典範** | 有同期或後來的可靠來源明確指出該方法曾占主導、最普遍，或已成為主流技術家族。 |
| **技術轉折代表** | 原始論文引入後續方法反覆沿用的新表示法、訓練方式或任務能力。 |
| **當時高能力代表** | 原論文在明確實驗範圍內，對自然度、相似度、可懂度或速度提供優於當時基線的證據。 |
| **穩健代表** | 原論文明確定義 failure mode 與 robustness 指標，並對該問題提供改善證據。這不等於對所有資料、語言、通道或攻擊都穩健。 |

**重要限制：** 不同論文使用的資料集、聽測者、語言、MOS 設計與比較基線不同，因此不能把跨論文的 MOS 或 WER 排成一張「歷年總冠軍榜」。

## 第一版年代分期

> 年份是閱讀順序；年代邊界是根據「表示法／架構」與「可用能力」至少兩項同時改變而提出。年代邊界屬於 **Inference**，論文年份與下列原論文內部結果則屬於 **Verified**。
>
> 分期表示研究重心與新能力發生轉折，不表示前一代方法在邊界年份後立刻消失。

### 1. 1990–2003：語料拼接與 Unit Selection

**當時主要方法**

- 從大型真人語音庫中搜尋合適片段，再把片段串接成新語句。
- 優點是片段本身是真人錄音，因此在資料庫涵蓋範圍內可有良好自然度。
- 缺點是彈性受語料庫限制；改說話者、語氣或風格通常需要重新收集大量語音。

**代表論文與年份**

- **1990 — Takeda, Abe, Sagisaka, _On the unit search criteria and algorithms for speech synthesis using non-uniform units_**，ICSLP 1990。提出非均勻單元的搜尋與選擇方法；主觀與客觀測試優於固定單元方法。[ISCA 原始會議頁](https://www.isca-archive.org/icslp_1990/takeda90_icslp.html)
- **2009 — Zen, Tokuda, Black, _Statistical Parametric Speech Synthesis_**，Speech Communication 綜述。此文回顧時明確指出 unit-selection synthesis 在先前十年間居主導地位，可作為「1990 年代末至 2000 年代曾是主流」的證據。[學術機構書目與摘要](https://pure.nitech.ac.jp/en/publications/statistical-parametric-speech-synthesis-2/)

**判定**

- Unit selection：**主流典範（Verified）**
- Takeda et al. (1990)：**早期技術轉折代表（Verified）**

**對後續 deepfake 問題的意義**

系統已能重組真人聲音片段來說出新內容，但仿冒特定新說話者的成本高、彈性低，拼接邊界與語料覆蓋也限制了輸出。

---

### 2. 2004–2015：統計參數式 TTS 與 GMM Voice Conversion

**當時主要方法**

- TTS 從挑選真人片段，轉向估計聲學參數，再透過 vocoder 重建語音。
- VC 使用來源／目標說話者資料學習聲學特徵的統計映射。
- 相較 unit selection，系統更容易控制說話者、音高與語速，但容易產生過度平滑與 vocoder 音色。

**代表論文與年份**

- **2004 — Toda, _Overview of Voice Conversion_**，SSW 5 tutorial。文中明確稱 GMM-based conversion 為當時「最普遍的轉換方法」，同時列出頻譜不連續、過度平滑與統計模型不適切等限制。[ISCA 原始頁](https://www.isca-archive.org/ssw_2004/toda04b_ssw.html)
- **2007 — Toda, Black, Tokuda, _Voice Conversion Based on Maximum-Likelihood Estimation of Spectral Parameter Trajectory_**，IEEE/ACM TASLP。以整段頻譜軌跡的最大概似估計改善逐幀 GMM 轉換的品質與說話者個性。[IEEE Xplore](https://ieeexplore.ieee.org/document/4317579/)
- **2009 — Zen, Tokuda, Black, _Statistical Parametric Speech Synthesis_**，Speech Communication。回顧 HMM-based statistical parametric speech synthesis，指出此類方法已能有效合成可接受語音，並系統整理相對 unit selection 的利弊。[學術機構書目與摘要](https://pure.nitech.ac.jp/en/publications/statistical-parametric-speech-synthesis-2/)

**判定**

- GMM-based VC：**主流典範（Verified，範圍限定為 2004 年 VC）**
- HMM-based statistical parametric TTS：**重要且有效的統計典範（Verified）**
- 不能僅依這些來源斷言 HMM-TTS 已在所有系統中全面取代 unit selection。

**對後續 deepfake 問題的意義**

偽造不再完全依賴目標句子的真人片段；內容與說話者特徵開始可由模型分開控制。不過輸出中的過度平滑、vocoder 音色與不連續仍可能成為辨識線索。

---

### 3. 2016–2019：深度神經波形、端到端 TTS 與零樣本聲音模仿

**技術轉折**

- 神經生成模型開始直接建模波形，或從文字端到端預測頻譜。
- 多說話者模型將「說話者表示」與「文字內容」解耦。
- 只提供數秒目標聲音，就能對訓練時未見過的說話者合成新語句。

**代表論文與年份**

- **2016 — van den Oord et al., _WaveNet: A Generative Model for Raw Audio_**。直接逐樣本生成波形；Google 的測試中較當時 concatenative 與 parametric TTS 更自然，但自回歸生成計算昂貴。[Google DeepMind 原始研究頁](https://deepmind.google/blog/wavenet-a-generative-model-for-raw-audio/)
- **2017 — Wang et al., _Tacotron: Towards End-to-End Speech Synthesis_**，Interspeech 2017。把文字到頻譜的多階段工程整合為端到端模型，MOS 3.82，優於其 production parametric baseline。[Google Research](https://research.google/pubs/tacotron-towards-end-to-end-speech-synthesis/)
- **2018 — Shen et al., _Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions_（Tacotron 2）**，ICASSP 2018。以 Tacotron 2 + WaveNet 取得 MOS 4.53，該研究的專業錄音為 4.58。[Google Research](https://research.google/pubs/natural-tts-synthesis-by-conditioning-wavenet-on-mel-spectrogram-predictions/)
- **2018 — Jia et al., _Transfer Learning from Speaker Verification to Multispeaker Text-to-Speech Synthesis_**，NeurIPS 2018。利用數秒參考音訊合成訓練時未見說話者；原論文同時警告濫用風險，並承認當時輸出仍可與真實語音區分。[NeurIPS 原始論文 PDF](https://proceedings.neurips.cc/paper/2018/file/6832a7b24bc06775d02b7406880b93fc-Paper.pdf)
- **2019 — Qian et al., _AutoVC: Zero-Shot Voice Style Transfer with Only Autoencoder Loss_**，ICML 2019。以 autoencoder bottleneck 做 non-parallel many-to-many VC，原論文報告當時的 SOTA 結果與 zero-shot VC 能力。[PMLR](https://proceedings.mlr.press/v97/qian19c.html)

**判定**

- WaveNet、Tacotron 系列：**神經語音合成技術轉折代表（Verified）**
- Jia et al. (2018)、AutoVC (2019)：**零樣本聲音模仿／轉換能力代表（Verified）**
- **Unknown：** 尚未找到足夠同期採用資料，可把其中某一篇單獨稱為 2016–2019 全領域「最流行」的方法。

**對 Detection 的壓力**

真假差異從明顯的拼接或傳統 vocoder 痕跡，轉向神經 vocoder、頻譜預測與說話者嵌入所留下的模型特定痕跡。特定說話者偽造所需的目標資料量顯著下降。

---

### 4. 2020–2021：效率、對齊穩定性與單階段高品質生成

**技術轉折**

- 研究焦點不只追求自然度，也開始明確處理漏字、重複、對齊失敗與推論速度。
- 高品質 vocoder 可達遠快於即時生成。
- 單階段、平行 TTS 縮短傳統「文字→頻譜→vocoder」管線。

**代表論文與年份**

- **2020 — Shen et al., _Non-Attentive Tacotron_**。用 explicit duration predictor 取代 attention，並以 unaligned-duration ratio 與 word-deletion rate 衡量對齊穩健性；MOS 4.41，略高於其 Tacotron 2 對照。[Google Research](https://research.google/pubs/non-attentive-tacotron-robust-and-controllable-neural-tts-synthesis-including-unsupervised-duration-modeling/)
- **2020 — Kong, Kim, Bae, _HiFi-GAN_**，NeurIPS 2020。高傳真 GAN vocoder；原論文報告 V100 上 167.9 倍即時速度、CPU 小模型 13.4 倍即時，並測試未見說話者的 mel inversion。[NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2020/hash/c5d736809766d46260d816d8dbc9eb44-Abstract.html)
- **2021 — Kim, Kong, Son, _Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech_（VITS）**，ICML 2021。結合 VAE、flow、adversarial learning 與 stochastic duration predictor，單階段平行生成；在 LJ Speech 的原論文測試中優於當時公開 two-stage 系統，MOS 接近 ground truth。[PMLR](https://proceedings.mlr.press/v139/kim21f.html)

**判定**

- Non-Attentive Tacotron：**對齊穩健代表（Verified，但僅限其定義的 failure modes）**
- HiFi-GAN：**效率與高傳真 vocoder 代表（Verified）**
- VITS：**單階段平行 TTS 技術轉折與當時高能力代表（Verified）**

**對 Detection 的壓力**

生成速度與品質提升，使大量、即時或近即時偽造更可行；模型也開始主動消除早期 attention 造成的漏字與重複等可見失敗。

---

### 5. 2022–2023：Codec Token、Audio Language Model 與大型零樣本生成

**技術轉折**

- 連續波形被離散成 semantic／acoustic tokens，語音生成被重新表述為 language modeling。
- 大規模訓練讓數秒聲音提示成為 speaker、prosody、emotion 與錄音環境的條件。
- Diffusion 與 flow matching 提供非自回歸替代路線，並把 TTS、編輯、去噪、style conversion 合併進同一模型。

**代表論文與年份**

- **2022 — Borsos et al., _AudioLM: a Language Modeling Approach to Audio Generation_**。以 semantic 與 SoundStream acoustic tokens 建立分層 audio LM；可由數秒提示延續說話者、韻律與錄音條件。Google 的人類真假判斷測試為 51.2%，與隨機猜測 50% 無顯著差異。[Google Research](https://research.google/blog/audiolm-a-language-modeling-approach-to-audio-generation/)
- **2023 — Wang et al., _Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers_（VALL-E）**，arXiv 預印本。以 60K 小時資料訓練 codec LM；只用 3 秒未見說話者錄音做個人化 TTS，並保留情緒與聲學環境。[Microsoft Research](https://www.microsoft.com/en-us/research/publication/neural-codec-language-models-are-zero-shot-text-to-speech-synthesizers/)
- **2023 — Le et al., _Voicebox_**，Meta Research paper。50K 小時、多語、非自回歸 flow-matching speech infilling；支援零樣本 TTS、去噪、內容編輯與 style conversion。原文報告相對 VALL-E 有更佳可懂度／相似度且最高快 20 倍。[Meta Research](https://ai.meta.com/research/publications/voicebox-text-guided-multilingual-universal-speech-generation-at-scale/)
- **2023 預印本／2024 ICLR — Shen et al., _NaturalSpeech 2_**。以 neural codec latent + diffusion，訓練於 44K 小時語音與歌聲；原文報告在 zero-shot 的韻律／音色相似、robustness 與品質優於其比較系統。[Microsoft Research](https://www.microsoft.com/en-us/research/publication/naturalspeech-2-latent-diffusion-models-are-natural-and-zero-shot-speech-and-singing-synthesizers/)

**判定**

- Codec-token／audio-language-model 路線：**主流典範轉折（Verified）**。2024 CosyVoice 原文也把 LLM-based TTS 描述為已進入主流，但這是研究團隊對領域趨勢的概括，不是市場占有率統計。
- AudioLM：**奠基性 audio-LM 代表（Verified）**
- VALL-E：**大型 codec-LM zero-shot TTS 代表（Verified；出版狀態為 arXiv）**
- NaturalSpeech 2：**zero-shot diffusion 與論文內穩健性代表（Verified；2024 peer-reviewed）**

**對 Detection 的壓力**

「看過這個生成器／這個說話者」的封閉世界假設更脆弱。相同的 token／foundation-style 框架可跨說話者、語言與任務生成，且可保留提示音訊中的環境特徵。

---

### 6. 2024–2025：簡化的 Flow Matching、Masked Generation 與可擴展零樣本系統

**技術轉折**

- 零樣本 TTS 不再一定需要複雜 duration model、G2P 或明示對齊。
- Flow matching 與 masked token generation 提供平行生成路線。
- 研究進一步追求大規模多語、長文本、streaming、內容一致性與 speaker similarity。

**代表論文與年份**

- **2024 — Eskimez et al., _E2 TTS_**，SLT 2024 accepted。以字元、filler tokens、audio infilling 與 flow matching 建立完全 non-autoregressive zero-shot TTS，不需 duration model、G2P 或 monotonic alignment search。[arXiv 書目與接受資訊](https://arxiv.org/abs/2406.18009)
- **2024 — Du et al., _CosyVoice_**，arXiv work in progress。LLM text-to-token + conditional flow matching token-to-speech；以 supervised semantic tokens改善內容一致性與 speaker similarity，並以大型資料展示 scaling 趨勢。[arXiv](https://arxiv.org/abs/2407.05407)
- **2025 — Wang et al., _MaskGCT_**，ICLR 2025。完全 non-autoregressive masked generative codec transformer，不需 text-speech alignment supervision 或 phone-level duration prediction；在 100K 小時 in-the-wild speech 上，原文報告優於當時比較系統的品質、相似度與可懂度。[ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/74a31a3b862eb7f01defbbed8e5f0c69-Abstract-Conference.html)

**判定**

- E2 TTS：**架構簡化與 flow-matching 代表（Verified）**
- MaskGCT：**peer-reviewed 的大規模 masked-generation 高能力代表（Verified）**
- **Unknown：** 2024–2025 技術仍快速變動，目前不能把任何單一模型查證為全領域穩定的「最流行」或「最穩健」方法。

**排除但保留的反證**

- **F5-TTS** 常被後續研究使用，也具開源影響力，但其 OpenReview 紀錄是 **ICLR 2025 withdrawn submission**，所以本輪不把它列為 2025 的 peer-reviewed 代表；可在後續「採用度」專題中另行評估。
- CosyVoice 的 arXiv 頁標示 **work in progress**，並有 substantial text overlap 的管理註記；因此只能用來表示一條技術路線，不能獨自支撐「最佳方法」結論。

**對 Detection 的壓力**

生成架構更簡單、資料規模更大、推論更平行，代表新生成器變體可以更快出現；只對已知合成器痕跡有效的 detector，面臨更頻繁的 unseen-generator shift。

## 壓縮後的時間軸

```text
1990–2003  Unit selection／語料拼接
    1990 Takeda et al. ─ 技術前史代表
    2009 Zen et al.    ─ 回顧證實 unit selection 曾主導前十年

2004–2015  統計參數式 TTS ＋ GMM Voice Conversion
    2004 Toda          ─ GMM-based VC 被明確稱為當時最普遍方法
    2007 Toda et al.   ─ trajectory-based ML VC
    2009 Zen et al.    ─ HMM statistical parametric TTS

2016–2019  神經波形／端到端／零樣本模仿
    2016 WaveNet       ─ raw-waveform neural generation
    2017 Tacotron      ─ end-to-end text→spectrogram
    2018 Tacotron 2    ─ 接近真人錄音的論文內 MOS
    2018 Jia et al.    ─ 數秒參考音訊、未見說話者
    2019 AutoVC        ─ zero-shot voice conversion

2020–2021  高速、穩定對齊、單階段
    2020 Non-Attentive Tacotron ─ 對齊穩健性
    2020 HiFi-GAN              ─ 高傳真高速 vocoder
    2021 VITS                  ─ 單階段平行 TTS

2022–2023  Codec token／Audio LM／大型 zero-shot
    2022 AudioLM       ─ semantic + acoustic token LM
    2023 VALL-E        ─ 3 秒 prompt 的 codec-LM TTS
    2023 Voicebox      ─ flow matching、多任務 speech infilling
    2023/2024 NaturalSpeech 2 ─ large-scale zero-shot diffusion

2024–2025  Flow matching 簡化／masked generation／scaling
    2024 E2 TTS        ─ 簡化、完全 non-autoregressive
    2024 CosyVoice     ─ LLM token + conditional flow matching
    2025 MaskGCT       ─ peer-reviewed masked codec transformer
```

## 目前可以與不可以下的結論

### 可以

- **Verified：** Unit selection 在 2009 年回顧所指的前十年曾主導 speech synthesis。
- **Verified：** GMM-based VC 在 2004 年的領域 tutorial 中被稱為當時最普遍的 conversion method。
- **Verified：** 2016 後的關鍵轉折包括 raw-waveform neural generation、end-to-end TTS，以及數秒參考音訊的 unseen-speaker synthesis。
- **Verified：** 2020 後有論文明確把對齊失敗、速度與單階段生成列為問題並提出可量測改善。
- **Verified：** 2022 後 codec tokens、audio LM、diffusion／flow matching 與大規模 zero-shot generation 成為主要研究路線。
- **Inference：** 上述共同形成六個適合初學者閱讀的歷史階段。

### 不可以

- 不能說每個年代只有一種方法。
- 不能把原論文自己的 SOTA 宣稱外推成跨資料集、跨語言、跨任務的絕對最佳。
- 不能把「生成穩健」等同於「能避開 detector」。
- 不能在沒有採用度資料時，把 2024–2025 任一模型稱為全領域最流行。

## 未解問題

1. 這六段分期是否要把 TTS 與 VC 畫成兩條泳道，而不是在同一條線上交錯？
2. 是否需要以 citation、正式 benchmark 採用、開源實作或實際資料集生成器清單，另外驗證 2016 後的「流行度」？
3. 2024–2025 應以 E2 TTS／MaskGCT 表示 peer-reviewed 技術轉折，還是另開一層列出影響力大但非 peer-reviewed 的 F5-TTS、CosyVoice 等系統？
4. 這些生成轉折分別使 Detection 的哪些假設失效，尚待 B 與 C 分支查證。

## 建議

將六個年代作為第一版閱讀骨架，但視覺上把 **TTS** 與 **VC** 畫成平行泳道；同一年代可以有多個代表論文。標籤只使用「主流典範」「技術轉折」「當時高能力」「特定穩健性」，不使用沒有範圍的「最佳」。

## 下一個最小查證步驟與停止條件

**下一步：** 請作者先確認六段年代邊界與雙泳道呈現方式；確認後再加入 `problem-map.mm.md`，接著用相同標準建立 Detection 時間軸。

**停止／修正條件：** 若某年代找不到至少一篇原始論文，以及一項可說明「表示法、能力或 failure mode 發生改變」的證據，便不把該年代獨立成段，而與相鄰年代合併。
