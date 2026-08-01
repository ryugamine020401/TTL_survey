# TTS 領域發展史：`tts-history` 35 篇論文封閉語料精讀綜述

- 日期：2026-07-27
- 研究模式：Synthesize
- 核心問題：僅根據 `papers/tts-history/` 內 35 篇論文，這個領域是什麼、如何發展、可如何分期，以及各階段有何共同點與差異？
- 證據範圍：只使用該資料夾內 35 篇 PDF 的正文、表格、圖與附錄；未使用網路、專案內既有討論、研究筆記、survey、README 或其他論文。
- 證據限制：這是一個人為選取的 35 篇封閉語料，不是完整系統性文獻回顧。因此下文能說明「這批論文呈現的發展史」，不能據此宣稱完整涵蓋全領域，更不能做「首次」或「無其他先行研究」的結論。

## 核心結論

**Verified（由論文共同支持）**：這批文獻所屬領域是文字轉語音合成（Text-to-Speech, TTS），更廣義地屬於語音合成與條件式語音生成。其任務是把文字或語言單位轉成可懂、自然、符合指定說話者／韻律／風格的語音波形。

**Inference（本綜述分期）**：35 篇文獻最合理的歷史切法不是只按模型名稱，而是按每一代主要在解決的「瓶頸」分成七個重疊階段：

1. 規則與聲學知識：如何從少量可解釋參數產生可懂語音。
2. 串接與單元選擇：如何直接重用真人錄音以提高自然度。
3. HMM 統計參數合成：如何以統一機率模型產生平滑、穩定、可調的語音。
4. 神經統計參數合成：如何以深度網路改善上下文映射與長時序建模。
5. 端到端自回歸與神經聲碼器：如何從字元／音素直接學習對齊並產生高品質波形。
6. 平行生成與單階段整合：如何同時解決速度、對齊錯誤、控制與兩階段落差。
7. 大規模提示式生成：如何利用大資料、codec／latent 表示與 in-context learning，對未見說話者做零樣本、跨語言、多任務語音生成。

這不是七次完全替代。新方法持續重新使用舊概念：單調對齊延續 HMM／動態規劃思想；顯式時長回到早期韻律控制；codec 又建立新的中介表示；提示式模型則把「說話者、韻律、錄音環境」從手工標籤改為由參考音訊提供。

---

## 1. 這是什麼領域

### 1.1 任務定義

TTS 的基本映射是：

> 文字／音素序列 → 語言與時序結構 → 聲學表示 → 語音波形

各代方法對中間兩步採不同實作：

- formant synthesizer 直接控制 F0、共振峰、頻寬、噪音與振幅等聲學參數；
- unit selection 從語音資料庫搜尋最合適的真人錄音片段並串接；
- HMM／DNN SPSS 預測頻譜、F0、時長等聲學軌跡，再由聲碼器重建；
- Tacotron 類模型由文字直接預測 spectrogram，神經聲碼器再產生波形；
- VITS 類模型把聲學模型與波形生成合併訓練；
- VALL-E、MaskGCT 類模型把語音轉成離散 codec／semantic tokens，再將 TTS 視為條件式 token 生成；
- Voicebox、NaturalSpeech 2 則以連續 mel／latent 配合 flow matching 或 diffusion 做非自回歸生成。

### 1.2 這個領域真正同時優化的目標

這 35 篇顯示，TTS 從來不只追求「像真人」。它同時優化：

- 可懂度與文字忠實度；
- 自然度與音質；
- 說話者、口音、情緒、韻律與錄音環境相似度；
- 穩定性，例如不漏字、不重複、不崩潰；
- 延遲、吞吐量、模型大小與裝置部署；
- 可控制性，例如時長、語速、F0、停頓與風格；
- 資料效率、未見說話者泛化與跨領域能力；
- 近年新增的安全問題，例如冒用聲音、詐騙與合成語音偵測。

因此，TTS 應被理解為一個多目標的條件式序列生成問題，而不是單一的音訊重建問題。

---

## 2. 領域的歷史發展

| 階段 | 約略年代（以本語料為準） | 核心表示 | 核心生成／選擇機制 | 主要解決的瓶頸 | 新出現的主要問題 |
|---|---:|---|---|---|---|
| 1. 規則與聲學知識 | 1980–1994 | formant、F0、聲源與發音控制參數 | 手工規則、source-filter、formant synthesizer | 先產生可懂、可分析、可控制的語音 | 規則龐雜、語言／方言依賴、自然度有限 |
| 2. 串接與單元選擇 | 1990–2007 | 真人錄音單元 | 動態規劃、Viterbi、target/join cost、CART clustering | 用真人聲音提高局部自然度 | 資料庫覆蓋、接點破綻、韻律失配、品質忽好忽壞 |
| 3. HMM 統計參數合成 | 1999–2009 | 頻譜、F0、時長機率分布 | HMM／MSD-HMM／HSMM、MLPG、決策樹、GV | 統一建模、穩定產生、適應新說話者 | 過度平滑、vocoder 音色、條件獨立與模型誤差 |
| 4. 神經統計參數合成 | 2013–2016 | 同上，但以神經網路預測 | DNN、MDN、BLSTM、LSTM | 改善上下文映射、長依賴與序列平滑 | 仍受手工特徵與聲碼器上限限制；訓練／串流取捨 |
| 5. 端到端自回歸＋神經聲碼器 | 2016–2018 | raw waveform、mel／linear spectrogram、speaker embedding | WaveNet、attention seq2seq、autoregressive decoder | 大幅提升音質；由資料學文字—聲學對齊 | 推論慢、attention 漏字／重複、訓練暴露偏差、資料覆蓋問題 |
| 6. 平行生成與單階段整合 | 2019–2021 | mel、flow latent、raw waveform latent | FastSpeech、flow、GAN、diffusion、VAE＋GAN | 速度、穩定、顯式控制、去除外部對齊器、端到端整合 | 平行模型的時長／多樣性；GAN 訓練；diffusion 多步延遲 |
| 7. 大規模提示式生成 | 2022–2025 | semantic token、codec token、continuous codec latent、mel | codec LM、masked prediction、flow matching、latent diffusion、in-context learning | 零樣本說話者、多語、多任務、資料規模與開放域泛化 | 長序列與取樣成本、prompt 屬性糾纏、口音／資料覆蓋、安全濫用 |

### 歷史轉折的因果鏈

1. **規則合成能控制但不自然**，於是轉向直接使用真人錄音。
2. **真人錄音局部自然但串接與覆蓋不穩**，於是轉向統計生成，換取一致性、可調性與小模型。
3. **HMM 生成穩定但過度平滑**，於是以 DNN／RNN 提高非線性與長時序建模能力。
4. **神經 SPSS 仍受手工聲學特徵與傳統聲碼器限制**，WaveNet 與 Tacotron 分別重做波形生成與文字到聲學表示。
5. **自回歸端到端模型音質高但慢且有 attention 錯誤**，FastSpeech／Glow-TTS 導入顯式或內生單調時長，HiFi-GAN／DiffWave 平行化聲碼器，VITS 合併兩階段。
6. **小型、封閉說話者 TTS 已接近真人後，問題轉為多樣性、零樣本與通用性**，AudioLM、VALL-E、Voicebox、NaturalSpeech 2、MaskGCT 將大規模資料、參考音訊提示與生成式表示帶入 TTS。

---

## 3. 從過往到現在的趨勢

### 3.1 從人工指定表示，到學習表示，再到混合表示

- 早期直接由人定義聲學與發音參數。
- unit selection 把表示改成真人片段及其標籤。
- HMM／DNN 時代以 mel-cepstrum、F0、duration 等手工聲學特徵作為中介。
- Tacotron 以 mel spectrogram 作為較低階、較少工程化的介面。
- AudioLM／VALL-E 導入離散 semantic／codec tokens。
- NaturalSpeech 2 反過來批評長離散序列，改用連續 codec latent。
- MaskGCT 再證明離散表示仍可行，但 tokenizer 與非自回歸生成方式是成敗關鍵。

**Inference**：表示方法不是線性地從「落後」走向「先進」，而是在資訊量、序列長度、可生成性、可重建性、可解釋性之間反覆取捨。

### 3.2 從局部音質，轉向長期結構與條件一致性

- formant 與 unit selection 主要處理音素、音節、接點與局部共調。
- HMM／RNN 將問題擴展到狀態序列、全句參數軌跡。
- Tacotron 以 attention 學文字—聲學長序列對齊。
- AudioLM 顯式區分長期語意結構與局部聲學細節。
- VALL-E、Voicebox、NaturalSpeech 2、MaskGCT 進一步要求生成內容、說話者、韻律、情緒與環境都和 prompt 一致。

### 3.3 從固定聲音，到零樣本未見說話者

- 早期多是單語言／單說話者或固定資料庫。
- HMM speaker adaptation 顯示少量資料即可調適平均聲音。
- 2018 speaker verification transfer 將說話者表徵與 TTS 解耦，以數秒無轉錄語音做 zero-shot。
- 2022 後，大規模模型直接以參考音訊作 in-context prompt，不再只把說話者壓縮成單一低維 embedding。

### 3.4 從決定式映射，到明確建模一對多

同一句文字可以有不同語速、停頓、F0、情緒與聲音。早期系統通常輸出單一結果；後來：

- MDN 建模多模態條件分布；
- Glow-TTS 由 flow latent 控制變異；
- VITS 使用 stochastic duration predictor；
- codec LM 以 sampling 產生多種結果；
- flow matching、diffusion、masked generation 以隨機初始狀態或遮罩解碼提供多樣性。

### 3.5 從自回歸到平行，但不是簡單「去序列化」

- WaveNet、Tacotron、VALL-E 第一階段均依賴自回歸，因此品質高但推論逐步進行。
- FastSpeech 使用顯式 phoneme duration 平行生成。
- Glow-TTS 用 MAS 自行找單調對齊。
- diffusion／flow matching／masked prediction 雖能跨時間平行，仍需多個去噪、ODE 或 mask-and-predict 迭代。

**Verified**：平行模型解決了輸出長度線性依賴與 attention 錯誤，但會把難題移到時長、對齊、迭代步數或表示設計。

### 3.6 從乾淨小資料，到大規模 in-the-wild 資料

文獻中的規模從單說話者約 24 小時、百位說話者數十小時，擴大到 AudioLM／VALL-E 的 60K 小時、Voicebox 的 50K–60K 小時、NaturalSpeech 2 的 44K 小時、MaskGCT 的英中共 100K 小時。

規模帶來未見說話者、錄音條件、韻律與語言泛化，但論文也共同指出：

- audiobook 仍偏朗讀風格；
- 口音、對話、隨意說話與低資源族群覆蓋不足；
- 大資料不等於無偏差或無安全風險；
- 不同論文的訓練資料、評估集和評分流程不同，不能只用單一數字排名。

### 3.7 從 TTS 專用系統，到通用語音生成模型

晚期模型開始把 TTS 與 speech continuation、editing、denoising、voice conversion、cross-lingual dubbing、emotion control、singing、ASR synthetic data generation 放在同一架構內。領域邊界由「讀出文字」擴張為「受文字與音訊條件控制的通用語音生成」。

---

## 4. 領域共同點

跨越七個階段，仍有九個穩定共同點。

1. **內容條件**：所有方法都必須把離散語言內容映射成連續時間信號。
2. **時長／對齊**：文字與語音長度不同，必須透過規則、HMM 狀態、attention、duration predictor、MAS、forced alignment、LM 隱式時長或總長度預測解決。
3. **聲學表示**：每代都選擇某種介面來承載內容、音色與韻律，只是從 formant、片段、參數、spectrogram 變成 latent／token。
4. **波形產生**：即使號稱 end-to-end，多數系統仍存在某種最終渲染機制，例如 formant synthesizer、vocoder、WaveNet、HiFi-GAN、codec decoder。
5. **一對多性**：文字不能唯一決定聲音；說話者、語速、韻律、情緒與環境是額外自由度。
6. **歸納偏置**：手工規則、單調對齊、source-filter、Viterbi、RVQ 層級、period discriminator 都是針對語音結構加入的偏置。
7. **資料覆蓋決定失敗邊界**：每個階段都受資料庫、speaker、語言、錄音風格與 out-of-domain 條件影響。
8. **品質與一致性的拉鋸**：越貼近真人片段或高容量生成，越可能有接點、對齊、抽樣或 hallucination 問題；越強調平滑、平均與穩定，越可能變得沉悶或缺少多樣性。
9. **需要人類聽覺評估**：客觀距離、WER、speaker similarity、FSD 可拆解問題，但自然度仍長期依賴 MOS／CMOS 等主觀測試。

---

## 5. 怎麼區分領域的階段

只按年份或模型骨幹會混淆，因為多個範式長期重疊。較穩健的分期方式是同時看六個判準：

1. **產生單位是什麼**：聲學參數、真人單元、連續特徵、波形樣本、離散 token、連續 latent。
2. **文字—語音對齊如何取得**：手工規則、標註、Viterbi／HMM、soft attention、顯式 duration、MAS、forced alignment、無對齊的 masked generation。
3. **不確定性如何表示**：固定規則、最佳路徑、Gaussian／mixture、autoregressive sampling、flow／VAE／diffusion。
4. **生成是逐步還是平行**：片段搜尋、frame/sample autoregression、feed-forward、iterative parallel generation。
5. **說話者／風格如何條件化**：固定聲音、speaker-dependent model、adaptation、embedding、參考音訊 prompt。
6. **研究主要瓶頸是什麼**：可懂度、自然度、接點、過度平滑、波形品質、速度／穩定、零樣本／通用性。

當上述多數判準一起改變，才應視為新階段。這也解釋為何 WaveNet 雖只重做聲碼器，仍是第五階段的轉折：它改變了波形表示、損失與可達音質，並直接使 Tacotron 2 類兩階段神經 TTS 成立。

---

## 6. 各階段的共同點與相異點

### 階段 1：規則與聲學知識

**共同點**

- 以可解釋聲學／發音參數控制聲音。
- 依賴語音學、音系學與語言特定規則。
- 可精確操控 F0、formant、時長、摩擦與聲源。

**相異點**

- Klatt 是低階 acoustic synthesizer；
- YorkTalk 主張以音系圖與連續控制取代 segment rewrite；
- Korean TTS 加入語言特定規則與 demisyllable database；
- Stevens 將高階 articulatory parameters 映射到 Klatt 控制；
- Pearson 以真人取樣聲源／無聲子音補強純 formant 合成。

### 階段 2：串接與單元選擇

**共同點**

- 從錄音資料庫選單元，追求保留真人微細節。
- 以 target cost 與 join／continuity cost 平衡「像目標」與「接得順」。
- 使用動態規劃、Viterbi 或剪枝搜尋。

**相異點**

- Takeda 搜尋可變長 nonuniform units；
- Black/Campbell 建立特徵成本與自動調權；
- Hunt/Black 將資料庫形式化為狀態轉移網路；
- Black/Taylor 以 CART cluster 緩解稀疏性並減少顯式 target weights；
- Multisyn 建成開放語料、可重現的完整 unit-selection 系統，但再次凸顯 corpus design 與 bad joins。

### 階段 3：HMM 統計參數合成

**共同點**

- 將頻譜、F0、時長轉為機率模型。
- 以 context clustering、parameter generation、vocoder 產生整句。
- 追求一致性、可調適、可插值與小模型。

**相異點**

- Yoshimura 統一 spectrum/pitch/duration，MSD-HMM 處理 voiced/unvoiced F0；
- Tokuda 正式化含 static/delta/delta-delta 的 ML parameter generation；
- Toda/Tokuda 以 global variance 對抗過度平滑；
- Yamagishi 把 speaker adaptation 推到少量、跨域、不一致資料；
- Zen 等人的 review 系統比較 SPSS 與 unit selection，確認前者穩定可控、後者最佳樣本較自然但波動大。

### 階段 4：神經統計參數合成

**共同點**

- 保留 SPSS 的輸入特徵、聲學輸出和 vocoder 框架。
- 以 DNN／RNN 取代決策樹與部分 HMM 映射。
- 目標是減少 fragmentation、捕捉非線性與長期依賴。

**相異點與矛盾**

- Zen 2013 顯示 DNN 優於相同模型大小的 HMM；
- DMDN 修正 MSE 只預測條件平均的問題；
- Fan 的 BLSTM 認為 static output 可不依賴動態特徵／MLPG；
- Merlin 的基準卻顯示 BLSTM 缺少 dynamic features／MLPG 可能更差。

這不是誰必然正確，而是顯示效果依架構、訓練 recipe 與資料而變，不能把「RNN 自然會產生平滑軌跡」當成普遍定律。

### 階段 5：端到端自回歸與神經聲碼器

**共同點**

- 以神經網路學習較低工程量的文字到聲學映射。
- mel／spectrogram 成為聲學模型和波形模型的介面。
- 自回歸提供高條件表達力，但引入速度和錯誤累積。

**相異點**

- WaveNet 專注 raw waveform，音質突破但 sample-by-sample 很慢；
- Tacotron 以 attention 直接從字元預測 spectrogram，但 Griffin-Lim 限制音質；
- Deep Voice 3 以卷積提升訓練與大規模多說話者能力；
- Tacotron 2 組合 location-sensitive attention、mel 與 WaveNet，使單說話者品質接近錄音；
- Jia 等人從 speaker verification 轉移 d-vector，將幾秒未轉錄參考音訊轉為 zero-shot speaker conditioning，但口音、細微相似度與 prosody disentanglement 仍有限。

### 階段 6：平行生成與單階段整合

**共同點**

- 直接回應自回歸延遲、漏字／重複與不可控問題。
- 使用單調對齊或顯式時長。
- 將高品質波形生成平行化，或直接合併聲學與聲碼器訓練。

**相異點**

- FastSpeech 依賴自回歸 teacher 的 attention 與知識蒸餾；
- Glow-TTS 用 MAS 內生學對齊，不再需要外部 aligner；
- HiFi-GAN 用多週期／多尺度判別器高效重建波形；
- DiffWave 以 diffusion 兼顧條件與無條件波形生成，但仍需多步反向過程；
- VITS 以 conditional VAE、flow、MAS、GAN 與 stochastic duration 統一端到端 TTS，並明確處理文字到語音的一對多。

### 階段 7：大規模提示式生成

**共同點**

- 資料擴大到數萬至十萬小時。
- 以短音訊 prompt 提供未見說話者、韻律、情緒或環境資訊。
- 零樣本、多語與多任務成為核心，而非附加功能。
- 以 WER、speaker similarity、prosody、FSD、速度及合成偵測等多面向評估。

**相異點**

- AudioLM 無文字監督，以 semantic＋acoustic token 階層建模長期一致性與音質；
- VALL-E 加入 phoneme prompt，把 TTS 變成 conditional codec LM；
- Voicebox 用 text-guided infilling＋flow matching，同時使用前後文並統一 TTS、編輯、去噪與抽樣；
- NaturalSpeech 2 用 continuous codec latent＋diffusion，批評離散長序列與 AR error propagation；
- MaskGCT 回到離散 semantic/acoustic token，但兩階段皆用 masked iterative parallel decoding，取消 phoneme-level alignment 與時長預測，只預測／控制總長度。

因此晚期不是「codec LM 獲勝」，而是三條仍競爭的路線：自回歸離散 token、連續 latent 的 diffusion／flow、以及離散 token 的 masked non-autoregressive generation。

---

## 7. 領域統整說明

### 7.1 一條最精簡的發展主線

TTS 的發展可以概括成：

> 人工控制聲音形成 → 搜尋真人聲音片段 → 統計生成平均聲學軌跡 → 神經網路學習文字到聲學映射 → 神經模型直接生成高品質波形 → 平行、穩定、可控的端到端生成 → 由大規模模型透過音訊提示生成任意未見聲音與多種語音任務。

### 7.2 真正沒有消失的核心問題：對齊、表示、變異

每一代模型都在重新回答三個問題：

1. **對齊**：哪一段文字對應到哪一段時間？
2. **表示**：模型應預測什麼，才能同時容易學又容易還原高品質聲音？
3. **變異**：文字未指定的說話者、韻律、情緒與環境，要平均掉、明確控制，還是隨機抽樣？

規則、Viterbi、HMM、attention、duration、MAS、forced alignment、masked prediction 都是對第一題的不同答案；formant、單元、mel、raw waveform、semantic token、codec token、continuous latent 是對第二題的不同答案；speaker adaptation、embedding、VAE／flow／diffusion、prompt 是對第三題的不同答案。

### 7.3 品質問題沒有消失，而是改變形態

- 規則合成：機械、語言規則不足。
- unit selection：壞接點、資料庫外文字與韻律失配。
- SPSS：過度平滑、muffled、vocoder artifacts。
- autoregressive seq2seq：漏字、重複、錯誤發音、不自然韻律、慢。
- 大型生成模型：prompt 屬性糾纏、口音覆蓋、隨機失敗、長序列成本、冒用與深偽風險。

因此「接近真人 MOS」不代表 TTS 已被解決；研究焦點只是從平均單句音質轉向可靠性、條件忠實度、分布覆蓋、可控性與安全性。

### 7.4 模組化與端到端呈擺盪，而非單向演進

- 早期 TTS 高度模組化。
- Tacotron 宣稱減少 text analysis 與 feature engineering。
- Tacotron 2 又明確分為 spectrogram predictor 與 WaveNet。
- VITS 再合併成單階段訓練。
- AudioLM／VALL-E 又使用預訓練 codec 與多階段 token models。
- Voicebox 使用 mel＋HiFi-GAN；NaturalSpeech 2 使用 codec encoder／decoder＋diffusion；MaskGCT 使用 semantic codec、T2S、S2A、acoustic codec。

**Inference**：業界所謂 end-to-end 的真正方向，不是完全沒有模組，而是讓中介表示可學、各模組可大規模預訓練，並減少人工標註與任務專用工程。

### 7.5 對晚近「human-level」結果的解讀

多篇晚期論文在特定資料集、特定 prompt 長度與特定評測中報告接近或優於 ground truth 的 MOS／CMOS。這些結果只能作為該實驗內的比較，不能推出：

- 所有語言、口音、說話方式都達到真人；
- 任意長度與任意文字都穩定；
- 模型不會冒用或洩漏訓練聲音；
- 不同論文的 MOS 可直接排序。

相反地，VALL-E、Voicebox、NaturalSpeech 2、MaskGCT 自己都承認資料覆蓋、口音、朗讀偏差、推論效率、屬性解耦或安全風險仍未解決。

---

## 跨文獻的矛盾、張力與負面證據

1. **自然度 vs. 一致性**：unit selection 最好的個別樣本可優於 SPSS，但 out-of-domain 與 bad joins 使品質不穩；SPSS 更一致卻較沉悶。
2. **平滑 vs. 細節**：HMM 的 ML 軌跡與 DNN 的 MSE 都傾向條件平均；GV、MDN、GAN、flow、diffusion 分別以不同方式補回分布變異。
3. **隱式 alignment vs. 顯式 duration**：attention／AR 能給豐富韻律但會漏字重複；顯式 duration 穩定可控但可能較標準化。MaskGCT 以總長度＋masked generation 嘗試繞開兩者。
4. **離散 token vs. 連續 latent**：VALL-E 強調 codec token 使語言模型與大資料擴展成為可能；NaturalSpeech 2 認為多層離散 token 太長且損失細節；MaskGCT 則主張改良 tokenizer 與 masked NAR 可保留離散方法優點。
5. **端到端 vs. 可訓練性**：Tacotron 簡化 pipeline 但仍需外部波形反演；VITS 單階段訓練改善兩階段 mismatch；晚期大模型又採凍結 codec、forced alignment、外部 ASR 或多模組。
6. **大資料 vs. 泛化**：VALL-E、NaturalSpeech 2 都明確指出，數萬小時 audiobook 仍無法涵蓋所有口音、日常對話與風格。
7. **逼真度 vs. 安全**：Jia 2018 的合成聲仍容易與真人區分；AudioLM 的人類辨識接近隨機，但模型分類器可高準確檢出；後續論文普遍承認 impersonation／spoofing 風險，卻沒有在這 35 篇中形成通用的 provenance 或部署規範。

---

## 35 篇逐篇精讀紀錄

### 階段 1：規則、formant 與混合式合成

1. **[Klatt 1980](../../papers/tts-history/T1-01_Klatt_1980_Cascade_Parallel_Formant_Synthesizer.pdf)**  
   提供軟體 cascade/parallel formant synthesizer，以 F0、formant、bandwidth、aspiration、frication、nasalization 等明確控制參數實現 source-filter 合成。核心價值是可解釋、可操控、可作研究工具；限制是控制規則與聲學知識負擔高。

2. **[Coleman 1990, YorkTalk](../../papers/tts-history/T1-02_Coleman_1990_YorkTalk.pdf)**  
   批評以 segment 與 rewrite rules 為核心的線性管線，主張用豐富音系圖與 unification representation 直接產生連續控制函數，表達事件重疊與共調。顯示「語言表示」本身就是 TTS 瓶頸；錯誤音系／方言知識仍會造成錯音。

3. **[Ahn & Sung 1990, Korean TTS](../../papers/tts-history/T1-03_Ahn_Sung_1990_Korean_TTS_Rules.pdf)**  
   將韓語特定的文字處理、stress／pitch／energy／duration rules、demisyllable database 與修改版 Klatt 合成器結合。說明早期 TTS 必須高度語言特定，也已出現規則＋資料庫的混合設計。

4. **[Stevens et al. 1994](../../papers/tts-history/T1-04_Stevens_1994_Articulatory_Control_Klatt.pdf)**  
   以約十個高階 articulatory parameters 經聲學與氣動原理映射到大量 Klatt 控制參數，降低直接聲學控制的複雜度。它試圖在可解釋發音控制與 formant 合成之間建立中介層。

5. **[Pearson et al. 1994](../../papers/tts-history/T1-05_Pearson_1994_Concatenation_Formant_Hybrid.pdf)**  
   將取樣的自然 glottal source／無聲子音與 formant 合成結合。真人波形可提升自然度／可懂度，但 context、記憶體、接合與 spectral matching 形成新問題；部分取樣 transition 並未改善子音可懂度，是重要負面結果。

### 階段 2：串接與單元選擇

6. **[Takeda et al. 1990](../../papers/tts-history/T2-01_Takeda_1990_Nonuniform_Unit_Search.pdf)**  
   搜尋可變長 nonuniform units，成本考慮 boundary continuity、context similarity、coarticulation 與 F0；比較全域 SCF 與 top-down/bottom-up TDH。較長、上下文更合適的單元提高可懂度，並確立動態規劃式單元選擇方向。

7. **[Black & Campbell 1995](../../papers/tts-history/T2-02_Black_Campbell_1995_Optimising_Unit_Selection.pdf)**  
   用 feature vectors、target distortion、continuity distortion、Viterbi／beam search 建立 CHATR 選擇框架。自動調權有效但暴露 objective distance 與人類知覺不一致，例如 cepstral distance 可能看不見爆破音錯誤。

8. **[Hunt & Black 1996](../../papers/tts-history/T2-03_Hunt_Black_1996_Unit_Selection.pdf)**  
   將語音資料庫形式化為 state-transition network：state occupancy 是 target cost，transition 是 concatenation cost，以剪枝 Viterbi 求路徑。比較 weight-space search 與 regression 學權重，確認學習成本權重優於純手調。

9. **[Black & Taylor 1997](../../papers/tts-history/T2-04_Black_Taylor_1997_Clustering_Units.pdf)**  
   以 CART 根據語言／韻律問題分群 phone instances，再以 acoustic distance 與 join cost 搜尋。減輕資料稀疏與顯式 target-weight 設定，但最佳／最差 utterance 差距與 perceptual join cost 仍難處理。

10. **[Clark et al. 2007, Multisyn](../../papers/tts-history/T2-05_Clark_2007_Multisyn.pdf)**  
    形成 Festival 中可重現的 open-domain unit-selection 系統：自動 HMM forced alignment、diphone units、linguistic target costs、MFCC/F0/energy join costs。品質高度依賴 corpus coverage、錄音一致性與清理；out-of-domain、pronunciation variation、prosody 與 bad joins 仍是弱點。

### 階段 3：HMM 統計參數語音合成

11. **[Yoshimura et al. 1999](../../papers/tts-history/T3-01_Yoshimura_1999_HMM_Spectrum_Pitch_Duration.pdf)**  
    統一建模 spectrum、pitch、duration；MSD-HMM 同時處理連續 voiced F0 與 unvoiced 離散狀態，並為不同 stream 建 context decision trees。優點是可調適、可插值；正式主觀評估仍不足。

12. **[Tokuda et al. 2000](../../papers/tts-history/T3-02_Tokuda_2000_HMM_Parameter_Generation.pdf)**  
    正式推導含 static、delta、delta-delta constraints 的最大概似 speech parameter generation，涵蓋固定／隱藏 state 與 mixture。多 mixture 形成更清楚 formant，但論文把主觀驗證留給後續。

13. **[Toda & Tokuda 2005](../../papers/tts-history/T3-03_Toda_Tokuda_2005_Global_Variance.pdf)**  
    指出 ML 生成的統計軌跡因 variance 太低而過度平滑，加入 global variance 機率項。主觀測試顯著改善自然度，尤其 spectral GV；但與 analysis-synthesis 的差距仍存在。

14. **[Yamagishi et al. 2009](../../papers/tts-history/T3-04_Yamagishi_2009_Speaker_Adaptive_HMM_TTS.pdf)**  
    建立 speaker-adaptive HMM/HSMM TTS，以 average voice、CSMAPLR/MAP、GV、STRAIGHT 等對少量、跨域、噪音與不一致資料調適。約數分鐘／百句資料即可調適；unit selection 在大量乾淨同域資料較強，但跨域下降更劇烈。

15. **[Zen, Tokuda & Black 2009](../../papers/tts-history/T3-05_Zen_Tokuda_Black_2009_SPSS_Review.pdf)**  
    系統整理 SPSS：優點是可控制、可調適、多風格／多語、小 footprint、穩定；缺點是 vocoder、acoustic modeling errors、oversmoothing。與 unit selection 的比較揭示「最佳樣本自然度」和「整體穩定度」不是同一目標。

### 階段 4：神經統計參數合成

16. **[Zen et al. 2013](../../papers/tts-history/T4-01_Zen_2013_DNN_SPSS.pdf)**  
    以 DNN 取代 decision-tree/HMM context mapping，讓所有資料共享參數並學複雜 feature interactions。相同模型大小下主觀優於 HMM、較不 muffled，但仍接既有 MLPG／vocoder pipeline。

17. **[Zen & Senior 2014](../../papers/tts-history/T4-02_Zen_Senior_2014_Deep_MDN_SPSS.pdf)**  
    指出 DNN MSE 只學條件平均且假設單峰固定變異，改用 mixture density network 輸出 GMM 的 mean／variance／mixture weight。多模態特別改善 F0 與自然度。

18. **[Fan et al. 2014](../../papers/tts-history/T4-03_Fan_2014_BLSTM_TTS.pdf)**  
    BLSTM 直接建模前後長期上下文；hybrid DNN＋BLSTM 在客觀與主觀上優於 HMM／DNN，並主張 static outputs 已足夠平滑。代價是整句非串流、訓練與參數成本較高。

19. **[Zen & Sak 2015](../../papers/tts-history/T4-04_Zen_Sak_2015_Low_Latency_LSTM_TTS.pdf)**  
    以單向 LSTM＋recurrent output layer 做低延遲序列生成，避免 utterance-level MLPG；output recurrence 能平滑，但若再疊加傳統 smoother 會過度平滑。

20. **[Wu et al. 2016, Merlin](../../papers/tts-history/T4-05_Wu_2016_Merlin.pdf)**  
    開源神經 SPSS toolkit，提供 DNN/LSTM/BLSTM/GRU 與 STRAIGHT/WORLD recipes，使可重現性與模組化成為研究基礎。其實驗也提醒 BLSTM 是否可捨棄 dynamic features／MLPG 不是普遍結論。

### 階段 5：神經聲碼器、端到端 attention 與 zero-shot speaker encoding

21. **[van den Oord et al. 2016, WaveNet](../../papers/tts-history/T5-01_Oord_2016_WaveNet.pdf)**  
    自回歸建模 raw waveform，以 dilated causal convolutions、gated units、residual/skip connections 與條件輸入產生高音質。相較傳統系統大幅提高 MOS，但 sample-by-sample 推論慢，有限 receptive field 也不足以自行處理長期韻律。

22. **[Wang et al. 2017, Tacotron](../../papers/tts-history/T5-02_Wang_2017_Tacotron.pdf)**  
    用 attention seq2seq 由字元直接預測 mel／linear spectrogram，CBHG encoder/postnet 與 autoregressive decoder 學 alignment，減少 phoneme aligner 與手工 linguistic features。Griffin-Lim 造成 artifacts，attention 仍可能失敗。

23. **[Ping et al. 2018, Deep Voice 3](../../papers/tts-history/T5-03_Ping_2018_Deep_Voice_3.pdf)**  
    全卷積 attention seq2seq，支援數千說話者與大型資料；position／monotonic constraints 緩解 repeat/skip，phoneme 輸入改善罕見詞與發音控制。展現訓練速度、規模與部署，但 noisy LibriSpeech 的音質明顯下降。

24. **[Shen et al. 2018, Tacotron 2](../../papers/tts-history/T5-04_Shen_2018_Tacotron_2.pdf)**  
    location-sensitive attention 的 recurrent spectrogram predictor 加上 mel-conditioned WaveNet。報告 MOS 4.526、接近 ground truth 4.582；ablation 顯示 mel 是緊湊介面、WaveNet 明顯勝 Griffin-Lim。錯誤仍集中於誤發音、names、異常韻律與 out-of-domain coverage。

25. **[Jia et al. 2018](../../papers/tts-history/T5-05_Jia_2018_Speaker_Verification_to_TTS.pdf)**  
    將獨立 speaker-verification encoder 的 d-vector 餵入 Tacotron 2；以數秒未轉錄語音 zero-shot 合成未見說話者。大量、多樣 speaker encoder 資料對泛化關鍵；自然度可高但未見 speaker 相似度下降，口音與 prosody 無法完全解耦，合成聲仍可被 verifier 區分。

### 階段 6：非自回歸、flow、GAN、diffusion 與單階段 TTS

26. **[Ren et al. 2019, FastSpeech](../../papers/tts-history/T6-01_Ren_2019_FastSpeech.pdf)**  
    以 feed-forward Transformer、length regulator 與 duration predictor 平行產生 mel；duration 來自自回歸 teacher attention 並使用 sequence-level distillation。報告 mel 生成約 270×、端到端約 38× 加速，困難句 0 repeat/skip；但依賴 teacher／外部對齊。

27. **[Kim et al. 2020, Glow-TTS](../../papers/tts-history/T6-02_Kim_2020_Glow_TTS.pdf)**  
    用 flow exact likelihood 與 dynamic programming 的 MAS 自行尋找最可能單調對齊，移除外部 aligner。相較 Tacotron 2 約 15.7× 快，長句更穩，並可控制 pitch、speed 與 speaker；flow invertibility 仍帶架構限制。

28. **[Kong et al. 2020, HiFi-GAN](../../papers/tts-history/T6-03_Kong_2020_HiFi_GAN.pdf)**  
    全卷積 generator 搭配 multi-period／multi-scale discriminators、mel loss 與 feature matching。period modeling 是關鍵，去除 MPD 造成大幅 MOS 下降；模型兼具高音質、GPU／CPU 速度、unseen speaker 泛化與小 footprint。

29. **[Kong et al. 2021, DiffWave](../../papers/tts-history/T6-04_Kong_2021_DiffWave.pdf)**  
    以 diffusion reverse process 從白噪音逐步去噪生成波形，支援 mel-conditioned、class-conditioned 與 unconditional generation。vocoder MOS 可匹配 WaveNet且快許多，無條件生成優於 WaveNet／WaveGAN；但仍慢於最強 flow vocoder，多步推論是明示限制。

30. **[Kim et al. 2021, VITS](../../papers/tts-history/T6-05_Kim_2021_VITS.pdf)**  
    conditional VAE＋normalizing flow＋MAS＋HiFi-GAN decoder／discriminator＋stochastic duration predictor，單階段、平行地由文字生成波形。LJ 與 VCTK MOS 接近 ground truth；ablation 顯示 prior flow 與高解析 posterior 輸入重要，隨機時長能補回平行模型韻律多樣性。

### 階段 7：大規模音訊提示、codec／latent 與通用語音生成

31. **[Borsos et al. 2022, AudioLM](../../papers/tts-history/T7-01_Borsos_2022_AudioLM.pdf)**  
    無文字標註，階層建模 w2v-BERT semantic tokens 與 SoundStream coarse/fine acoustic tokens。實驗證明 semantic token 擅長 phonetic／長期結構、acoustic token 擅長重建／speaker／環境；3 秒 prompt 能延續未見 speaker。人類真偽辨識約隨機，但專用分類器可高準確偵測。

32. **[Wang et al. 2023, VALL-E](../../papers/tts-history/T7-02_Wang_2023_VALL_E.pdf)**  
    將 TTS 定義為 phoneme＋acoustic prompt 條件下的 EnCodec language modeling：第一層 AR、其餘七層 NAR。60K 小時半監督資料帶來 3 秒 zero-shot in-context voice cloning、多樣輸出、環境與情緒保留；仍有 AR 漏字／重複、口音覆蓋與推論問題。

33. **[Le et al. 2023, Voicebox](../../papers/tts-history/T7-03_Le_2023_Voicebox.pdf)**  
    以 text-guided speech infilling 訓練非自回歸 continuous normalizing flow，flow matching 的 optimal-transport path 提高訓練與推論效率。單一模型可做 mono/cross-lingual zero-shot TTS、去噪、編輯、style transfer 與 diverse sampling；相較 VALL-E 報告更低 WER、較高相似度且最快約 20×，但仍限 audiobook/read speech，prompt 屬性不能任意拆分。

34. **[Shen et al. 2024, NaturalSpeech 2](../../papers/tts-history/T7-04_Shen_2024_NaturalSpeech_2.pdf)**  
    用 continuous codec latent＋latent diffusion，顯式 duration／pitch prior 與 speech prompting，反駁長離散 RVQ token＋AR 的穩定性／細節取捨。44K 小時、400M 模型在零樣本 speech／singing 上報告高品質與低 WER；限制是 audiobook coverage、diffusion 多步延遲與僅 30 小時 singing data。

35. **[Wang et al. 2025, MaskGCT](../../papers/tts-history/T7-05_Wang_2025_MaskGCT.pdf)**  
    兩階段皆採 masked generative transformer：text→VQ semantic tokens、semantic→12-layer acoustic tokens；無 text-speech alignment supervision，也不做 phone-level duration，只指定／預測總長度。100K 小時英中資料上報告接近真人的相似度、可懂度與自然度；結果也顯示 VQ semantic codec 明顯優於 k-means，尤其中文，且約 25 個 T2S 迭代已接近飽和。

---

## 證據解讀限制

1. 這 35 篇不是隨機或系統性抽樣，分期可能反映資料夾策展邏輯。
2. 1990 年代部分 PDF 為掃描圖像；已逐頁閱讀，但 OCR／印刷清晰度可能限制對公式與小字的辨識。
3. 各論文的 MOS／CMOS、聽者、語料、聲碼器、sample rate、prompt、資料量與 baseline 不一致，不做跨論文數值排名。
4. 部分論文的比較使用作者 demo 或重實作 baseline；它們的證據強度低於同資料、同流程、同聽測的直接比較。
5. 晚期模型常以論文內「human-level」描述特定 benchmark；本綜述不把它外推為整體領域已解決。
6. 本文的七階段是綜合歸納，不是任何單篇論文已驗證的唯一歷史分法。

## 尚未解決的不確定性

- 若納入此資料夾之外的工作，七階段邊界是否仍最合理？
- codec token、continuous latent 與 masked generation 三路線在相同資料、算力、延遲與安全條件下何者更優？
- 現有零樣本評估能否充分拆分 timbre、accent、prosody、emotion、channel 與語義忠實度？
- 合成偵測器在跨模型、壓縮、重錄、通訊通道與 adversarial laundering 後是否仍有效？

## 下一個最小驗證步驟與停止／轉向條件

**下一步**：若要把這份封閉語料史用於論文背景章，先建立一個只引用這 35 篇的 claim-to-source matrix，逐項對應「分期、表示、對齊、生成方式、資料規模、評估與限制」，再決定哪些歷史敘述需要開放式外部文獻查證。

**停止／轉向條件**：若目的只是理解 `tts-history` 資料夾，本綜述已完成；若要主張完整領域史、技術首次、目前 SOTA 或研究缺口，必須停止使用封閉語料結論並另做有搜尋範圍與日期的系統性驗證。
