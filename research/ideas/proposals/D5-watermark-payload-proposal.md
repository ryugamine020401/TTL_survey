# D5 研究計畫書：通訊通道下音訊浮水印之可用承載量前沿估計

> 日期：2026-07-23　狀態：proposal（計畫書階段）
> novelty 陳述一律為 bounded wording：「在 2026-07-23 所記錄的搜尋範圍內未找到直接同題先作」，不等於證明不存在。8.4 與第 9 節之數值均為預期／推估，非實測。

---

## 1. 題目

- 中文：《通訊通道下音訊浮水印之可用承載量前沿估計》
- English：*Operational Reliable-Payload Frontier Estimation for Audio Watermarks over Communication Channels*

## 2. 研究背景

音訊生成技術已可低成本合成擬真語音，浮水印（audio watermarking）因此成為「內容來源標示」的一條主動防線：在生成端把不可聽的訊號嵌入波形，於下游端解出，用以判定內容是否經 AI 生成／竄改，甚至攜帶來源資訊。此路線與被動偵測（passive detection）互補——被動偵測不需生成端合作，浮水印則以生成端主動嵌入換取更高可判定性。

在監理脈絡上，歐盟《人工智慧法》（Regulation (EU) 2024/1689）第 50 條課予提供者「使合成音訊等輸出可被機器判讀為人工生成或操縱」之透明度義務，相關義務自 2026-08-02 適用。歐盟執委會已於 2026-05-05 發布針對 AI 生成音訊標示與偵測之技術報告，並於 2026-07-20 發布第 50 條最終指引。本計畫僅將 Article 50 作為 **use-case motivation（應用情境動機）**，用以說明「通道存活後浮水印還能承載什麼」這一問題的現實重要性；不作任何法律充分性判定，亦不以實驗結果反證政策。

## 3. 問題與痛點

**痛點一：通道壓縮會磨損浮水印，但「約束下還能可靠承載多少」缺乏受控估計。** 詐騙、通話與社群分發的音訊會經過傳統 codec（AMR-WB/Opus/SILK/MP3/AAC）與神經 codec（EnCodec/DAC/SpeechTokenizer）等有損轉碼；既有基準已顯示神經壓縮對浮水印最具破壞性（見第 5 節 RAW-Bench）。然而多數評估在「配定 payload」下報告存活率，較少在**固定品質、false-accept、block-error 約束**下，系統性掃描 payload×ECC 以求出各方法族「還能可靠承載幾個位元」的作業前沿。

**痛點二：detection／payload-provenance／authentication 三個任務常被混談。** 「能否判定為 AI 生成」（detection，接近 1-bit 存在性決策）、「能否解出訊息或索引」（payload/provenance，多位元）、「能否以信任根與簽章驗證來源」（authentication，含金鑰管理與偽造威脅）三者所需位元、可容許錯誤率與威脅模型都不同。若混為一談，會把「偵測得到」錯讀為「來源可驗證」。

## 4. 研究動機

在 AudioMarkBench 與 RAW-Bench 已建立的評估基礎之上，仍存在一個未被系統回答的估計問題：**在預先固定的 watermark family、品質約束、通道族、false-accept 與 block-error 目標下，掃描 payload 與 ECC 所得到的 operational achievable payload frontier（作業可達承載前沿）與塌陷點各在哪裡，而三個任務的可行性邊界又分別落在何處。** 本計畫的動機即是把「配定 payload 下的存活率」推進到「約束下最多能可靠承載多少」，並把三任務明確拆開分別報告，避免任務混淆造成的過度樂觀解讀。此問題可在一人一年、單張 RTX 4090 的硬約束內以離線通道模擬完成，不需真人實測、不需真實電信 rig。

## 5. 先前研究統整

- **AudioMarkBench（NeurIPS 2024 Datasets and Benchmarks）**：以已知 ground-truth 浮水印訊息評估 bitwise accuracy 與 detection，涵蓋多種浮水印方法及 EnCodec 等擾動。因此「嵌入已知訊息以取得位元層 ground truth」是**既有實踐**——本計畫沿用此校準做法，不主張其為方法首創。
- **RAW-Bench / 《Will They Survive Neural Codecs?》（Özer 等，Interspeech 2025；arXiv 2505.19663，為同一篇論文）**：提出 Robust Audio Watermarking Benchmark，把 capacity 定義為每單位時間位元數（將方法配到約 5 bps），並報告 bitwise 與 full-message accuracy；發現神經 codec 即使納入訓練仍可能使多種方法的 bit accuracy 逼近隨機。本計畫直接建於其上：RAW-Bench 報告「配定 payload 下的準確率」，本計畫答「固定約束下最多能可靠承載多少」並加入三任務分離。**這是本計畫最直接的前作，殘餘 novelty 也最薄（見第 10 節停損）。**
- **浮水印方法族（本計畫實測對象，皆開源）**：AudioSeal（San Roman 等，ICML 2024）採 generator/detector 架構、支援樣本級定位偵測；WavMark（Chen 等，2023）於 1 秒音訊可嵌入至多 32 位元；SilentCipher（Singh 等，Interspeech 2024）以心理聲學閾值於 44.1 kHz 嵌入。SynthID 因非全開源，不納入。
- **EU 政策文件（僅作情境動機）**：Regulation (EU) 2024/1689 第 50、113 條；EC 2026-05-05 技術報告；EC 2026-07-20 第 50 條指引；EC 第 50 條 FAQ。Article 50(2) 明確含**技術可行性（technically feasible）、成本（cost）、最新技術水準（state of the art）** 等限定，並要求標示在可行範圍內有效、可互通、穩健、可靠；它並未等同要求浮水印攜帶足以做簽章式身分溯源的位元。

## 6. 研究問題（RQ）

- **RQ1（payload frontier 與塌陷點）**：各 watermark family 在「通道 × 約束」矩陣上的 operational reliable-payload frontier 為何？可逆（傳統 CELP 類）與不可逆（神經 codec）通道之間的**容量塌陷點**落在哪裡？
- **RQ2（ECC 外推）**：在 RQ1 的作業上限內，加入外部 ECC 後，能否在固定 block-error 目標下把可靠索引位元 k 外推、並使塌陷點位移？ECC 在哪個通道無法挽救而 k 歸零？
- **RQ3（三任務可行性邊界）**：detection（可否判定 AI 生成）、payload/provenance（可否解出訊息／索引）、authentication（可否驗證來源）三任務的可行性邊界，在同一通道矩陣上分別落在何處？三者所需位元、錯誤率與威脅模型如何區分？

## 7. 方法論

**核心 pipeline（單一，三 RQ 共用）**：`embed（嵌入已知 k-bit / watermark）→ 通道條件 transcode → recover → 以已知訊息校準後數可靠位元`。以嵌入已知訊息取得位元層 ground truth（沿用 AudioMarkBench 既有做法），避免高維互資訊估計的不可靠。

**payload×ECC 掃描**：固定品質約束（以客觀感知指標為門檻）、false-accept 目標與 block-error 目標，於每一通道格逐步提高 payload 並套用不同碼率 ECC，量測「在約束內仍可靠解出的位元數」，描出各 family 的 operational frontier 與塌陷點。所得量為**作業可達承載前沿，非 Shannon capacity**——它綁定於選定的 family、decoder、通道族與錯誤約束，不作資訊理論容量宣稱。

**三任務分離報告**：
1. detection：以偵測器 ROC 工作點為門檻，報 TPR/FPR，本質接近 1-bit 存在性決策；
2. payload/provenance：報 bitwise error、full-message accuracy、ECC 後 block-error 與可靠索引位元 k；
3. authentication：需信任根、簽章、金鑰管理與撤銷；本計畫僅界定其位元與威脅模型需求，**不宣稱達成跨平台可驗證溯源**。soft-binding 索引構造（碼率 ≤ 實測容量的 ECC 索引 + 本地簽章承諾表）之安全價值標為 **Unknown**，降入第 9 節 discussion 討論，不列為主張。

## 8. 實驗

### 8.1 設計

單一 pipeline、三 RQ 為其三種讀法。全程離線通道模擬，frozen 浮水印權重，不重訓、不需 rig、不需 IRB。三任務指標在同一批 recover 結果上分開計算。

### 8.2 資料與矩陣

- **載體語音**：AISHELL-3 + LibriSpeech + ASVspoof19／In-the-Wild real，**分層抽 ~10k 池**（載體年份不影響位元容量量測）。
- **watermark 家族**：AudioSeal、WavMark、SilentCipher（SynthID 非全開源不納入）。
- **通道矩陣**：
  - 傳統 codec（AMR-WB/Opus/SILK/MP3/AAC，CPU）× Gilbert-Elliott 封包遺失率（PLR）；
  - 神經 codec（EnCodec/DAC/SpeechTokenizer）× bitrate（**神經通道只掃 bitrate 不掃 PLR**——反映物理界線）。
- **CodecFake+**：僅作 2025 codec 世代參照，確認塌陷點對新世代仍成立，**不進 pipeline、不擴矩陣**。

### 8.3 參數、約束與算力

- 約束：品質門檻（客觀感知指標）、false-accept 目標（如 ≤10⁻³ 級距，最終依 detection ROC 校準）、block-error 目標（ECC 解碼失敗率上限）。
- GPU-h 結帳單（≈220）：neural transcode 32 + embed/recover 15 + 已知訊息多 seed 校準 90 + 索引構造驗證 10 + 1.5× 緩衝 73 = **~220 GPU-h**（用不到單卡年度上限）。算力非瓶頸，工具鏈成熟度才是。

### 8.4 預期結果（表骨架＋假設推論，數值為預期／推估，非實測）

**表 A（RQ1）operational reliable-payload frontier（單位：可靠 bits；儲存格待實測填入）**

| family × 通道 | 傳統 codec 高 bitrate | 傳統 codec 低 bitrate + 高 PLR | 神經 codec 高 bitrate | 神經 codec 低 bitrate |
|---|---|---|---|---|
| AudioSeal | 預期：較高 | 預期：中度下降 | 預期：明顯下降 | 預期：趨近塌陷 |
| WavMark | 預期：較高 | 預期：中度下降 | 預期：明顯下降 | 預期：趨近塌陷 |
| SilentCipher | 預期：較高 | 預期：中度下降 | 預期：明顯下降 | 預期：趨近塌陷 |

- **假設推論（標「推估」）**：依 RAW-Bench 觀察「神經壓縮使多種方法 bit accuracy 逼近隨機」，推估各 family 的塌陷點主要出現在神經 codec 低 bitrate 欄；傳統 codec 側的前沿較高且隨 PLR 緩降。此為待驗證假設，非結論。

**表 B（RQ2）ECC 後可靠索引位元 k（待實測；「—」表推估歸零）**

| ECC 碼率 \ 通道 | 傳統 codec | 神經 codec 中 bitrate | 神經 codec 低 bitrate |
|---|---|---|---|
| 高碼率（低冗餘） | 預期：k 較大 | 預期：k 下降 | 推估：— |
| 低碼率（高冗餘） | 預期：k 略降但穩 | 預期：k 部分挽回 | 推估：可能仍 — |

- **推估**：ECC 可在「已接近但未跌破」的通道格外推 k；一旦通道使原始 bit 逼近隨機，ECC 無資訊可救，k 推估歸零。塌陷是否可被 ECC 位移即 RQ2 的實測問題。

**表 C（RQ3）三任務可行性邊界（同一通道矩陣，分開報告）**

| 任務 | 主指標 | 所需位元 | 威脅模型 | 預期最先失效的通道 |
|---|---|---|---|---|
| detection | TPR@FPR | ~1-bit 存在性 | 無主動偽造 | 推估：神經 codec 低 bitrate |
| payload/provenance | bitwise / full-msg / block-error | 多位元 | 通道劣化 | 推估：早於 detection 失效 |
| authentication | 可否驗簽（需信任根） | 簽章級位元 | 主動偽造/金鑰 | 推估：最先且最脆弱；價值 Unknown |

## 9. 結果分析與討論（預期措辭）

- **塌陷點與可逆性邊界解讀**：若某 family 在某通道格的可靠 payload 推估歸零，這**只反證該方法族在該 bounded setting（該通道、該 payload、該 decoder、該約束）下的 operational payload**，不可外推為「浮水印政策層級不可行」，更不反證 Article 50——因為法條含 technically feasible／cost／state of the art 等限定，並允許不同標示與偵測技術。此界線在第 2、5 節已明列，於此重申以避免 bit 歸零被誤讀為政策否證。
- **三任務邊界解讀（預期）**：推估三任務失效順序為 authentication 早於 payload/provenance 早於 detection——因所需位元遞減、威脅模型嚴苛度遞增。故「通道後仍能 detection」不蘊含「仍能 provenance」，「仍能 provenance」不蘊含「來源可驗證」。三者須各自對照其門檻宣判，不可互相代替。
- **soft-binding 索引構造（降 discussion，標 Unknown）**：短索引 + 本地簽章承諾表之安全價值需完整威脅模型、信任根、金鑰散布、撤銷、索引碰撞、查詢可用性、隱私與互通性方能評估；若 verifier 承諾僅存在本地，不自動構成跨平台溯源。本計畫僅量其容量生死（k 是否存活），**不宣稱其安全性**。
- **ECC 外推的界線（預期）**：ECC 能在「資訊尚存」的通道外推 k，但無法從逼近隨機的通道創造資訊；因此 ECC 的價值在於位移塌陷點，而非消除塌陷。

## 10. 總結

本計畫在 AudioMarkBench 與 RAW-Bench 之上，於固定品質、false-accept 與 block-error 約束下，掃描 payload×ECC 求出各 watermark family 的 operational payload frontier 與塌陷點，並把 detection／payload-provenance／authentication 三任務的可行性邊界分開報告。貢獻界定為 **「固定約束下的作業承載前沿估計 + 三任務分離」**，非容量地圖首創、非可控植入首創、非 Article 50 首份審計。

**誠實聲明——殘餘 novelty 最薄**：本方向與 RAW-Bench 高度相鄰。**停損條件**：若 payload×ECC 掃描與 false-accept 控制相對 RAW-Bench 僅是「增加更多 codecs」，而未帶來新的估計問題或設計洞見（operational frontier 的塌陷點刻畫、ECC 外推邊界、三任務分離的可行性判定），則本方向不應作為論文主題，**降為 benchmark extension 或作備案**，另擇 D1-A 等證據更穩之方向為主線。

## 11. 未來展望

- 加入真實電信／RTC 通道錨（本計畫以離線模擬為界，未涵蓋真實通道之聯合畸變）。
- authentication 任務的完整密碼學實作（信任根、C2PA 容器、transparency-log）——本計畫僅界定其位元與威脅模型需求。
- 覆蓋率天花板之政策級量化（本計畫僅作情境動機，不量化）。
- 納入更多浮水印方法族（含日後開源之 SynthID 類方法）與非語音載體。

## 12. 參考文獻（僅列查證過之引用）

1. Liu 等（AudioMarkBench: Benchmarking Robustness of Audio Watermarking），NeurIPS 2024 Datasets and Benchmarks。https://openreview.net/pdf/17301d982d1e5ab0f0511e202cae5e1c02701532.pdf
2. Özer, Choi, Serrà, Singh, Liao, Mitsufuji（A Comprehensive Real-World Assessment of Audio Watermarking Algorithms: Will They Survive Neural Codecs?，即 RAW-Bench），Interspeech 2025；arXiv:2505.19663。https://www.isca-archive.org/interspeech_2025/ozer25_interspeech.html ／ https://arxiv.org/abs/2505.19663
3. San Roman 等（Proactive Detection of Voice Cloning with Localized Watermarking，AudioSeal），ICML 2024；arXiv:2401.17264。https://arxiv.org/abs/2401.17264 ／ https://github.com/facebookresearch/audioseal
4. Chen 等（WavMark: Watermarking for Audio Generation），2023；arXiv:2308.12770。https://arxiv.org/abs/2308.12770 ／ https://github.com/wavmark/wavmark
5. Singh, Takahashi, Liao, Mitsufuji（SilentCipher: Deep Audio Watermarking），Interspeech 2024。https://www.isca-archive.org/interspeech_2024/singh24_interspeech.html ／ https://github.com/sony/silentcipher
6. Regulation (EU) 2024/1689（Artificial Intelligence Act），Article 50 與 Article 113。https://eur-lex.europa.eu/eli/reg/2024/1689/oj
7. European Commission（State-of-the-art methods for marking and detecting AI-generated audio content），2026-05-05。https://op.europa.eu/en/publication-detail/-/publication/4f7b8585-4829-11f1-8095-01aa75ed71a1/language-en
8. European Commission（Guidelines on Article 50 transparency obligations for providers and deployers of AI systems），2026-07-20。https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
9. European Commission（FAQ: Transparency obligations under Article 50 AI Act）。https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
