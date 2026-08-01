# 五個論文方向的宣稱查證（A–E）

- 日期：2026-07-15
- 研究模式：Validate + Compare
- 查證對象：`discussions/legacy/CLAIMS-TO-VERIFY.md` 的 A1–A8、B1–B8、C1–C4、D1–D4，以及後續新增的 E1–E8
- 增量查證：A–D 先完成；E1–E8 於同日第二輪補查。本檔名保留 `a-d`，避免破壞既有交接連結，內容以本頁標題與此欄為準
- 證據基礎：原始論文、正式會議／出版社頁面、官方資料集頁面、官方法規或規格；本地 discussion 僅作為待驗證線索

## 1. 問題與結論

本文件回答兩個問題：

1. Claude 工作流產生的 novelty、前作、數字與資料可得性宣稱是否成立？
2. 查證結果如何改變五個候選方向，尤其是「未知生成器下語音深偽偵測的可信棄權」？

### 1.1 結論先行

- **A1 被否證。** 語音深偽偵測已有直接的 reliability／rejection 前作。Salvi et al.（ICASSP 2023）估計 detector prediction reliability；Pascu et al.（Interspeech 2024）跨八個 deepfake datasets 評估 calibration，並用 reliability threshold 畫出「保留樣本比例—正確率」曲線。因此不能宣稱 shift-aware selective ADD benchmark 沒有前作。
- **主題一仍可保留，但貢獻必須變窄。** 目前檢索到的直接前作沒有清楚回答：「只在 development distribution 選定的固定閾值，轉移到時間較新、generator-disjoint 的 holdout 時，是否仍滿足預先聲明的 accepted-risk 上限？」這是可研究的 residual gap，但只是 **promising gap**，尚不是 verified novelty。
- **A8 被否證。** Delgado et al. 已把裝置、播放／注入方式與 staged call-center calls 納入；RTCFake 更提供約 600 小時、跨多個 RTC 平台的 offline/online 配對資料。因此「真實電信通道審計仍無前作」不成立。
- **A5 的廣義說法被否證。** AudioMarkBench、RAW-Bench／Özer et al. 與 codec-aware watermarking 已直接碰到 neural codec robustness；只剩「特定真實平台 × 特定 neural codec × payload/capacity frontier」可能尚有較窄空間。
- **RTCFake 的技術內容存在，但授權是單點故障。** 論文與 Hugging Face repository 存在，資料卡顯示自訂 `rtcfake-license`；本輪無法從可索引的官方內容確認允許學術重散布。因此 D2 的「授權允許學術重散布」不得使用。
- **被 agent 擊沉的提案有些確實碰撞、有些是過度推論。** D-CAPTCHA、StreamVC、AuthentiCall 均存在；但 AuthentiCall 並非明顯的 OTT 單邊部署。Codecfake 的場次與任務被說錯；B7 的三篇方法論案例也不能合理推出「可以用文獻校準的合成人類模型取代真人量測」。
- **E 節會實質改變資料規劃。** DFADD 的 2025-04 修正版與 CodecFake+ 可作較新生成器測試資產，但必須固定版本並區分資料語意；MLAAD 官方目前仍是 **v9** 且 Hugging Face 存取需登入同意條款，不是宣稱中的 v10 公開下載；SpeechFake 的 Apache-2.0 只適用於 Hugging Face 上的 metadata／protocol repository，實際釋出的 fake audio 以 CC BY-NC 4.0 為主，部分 partition 另有 GPL 條款。
- **「台灣國語＋哭腔／急迫」仍是待驗證能力，不是模型規格。** 四個候選 TTS 都有可取得的 code 或 checkpoints，但官方資料不足以支持這個組合能力；必須先做小型、人工確認的生成 pilot，不能直接把它寫成資料已可建立。
- **RAW-Bench 是直接前作，但不是唯一前作。** neural codec／neural resynthesis 對 audio watermark 的破壞與防禦在 2025–2026 已有多篇直接工作，方向五不能再以「唯一直接前作」或近乎空白作 novelty 主張。

### 1.2 狀態用語

- **Verified**：原始或官方來源直接支持。
- **Refuted**：原始或官方來源直接衝突，或宣稱把兩個不同工作混成一個。
- **Partially verified**：核心存在，但範圍、數字、場次或推論需修正。
- **Unknown**：本次檢索不足以支持或否證；不得改寫成「沒有前作」。
- **Inference / Hypothesis**：分析性判斷或待實驗命題，不是已證事實。

## 2. 搜尋範圍與限制

### 2.1 搜尋範圍

- 搜尋日期：2026-07-15。
- 文獻來源：ISCA Archive、IEEE/ICASSP 官方資源頁、ACM／USENIX、PMLR、ACL Anthology、CVF Open Access、arXiv、IACR ePrint、Springer、Nature、IMF。
- 資料來源：ASVspoof 官方頁與 Edinburgh DataShare、Fraunhofer AISEC、Zenodo、Hugging Face 官方 dataset／model repositories、作者官方 GitHub／project pages。
- 政策來源：EU AI Act 官方 Article 50 頁面、European Commission／Publications Office。
- 關鍵查詢概念：`audio deepfake reliability estimation`、`selective prediction/rejection/abstention`、`risk coverage audio deepfake`、`unseen generator uncertainty/OOD`、`density vs discriminative uncertainty`、`adversarial reject option`、`audio laundering reversibility`、`watermark neural codec capacity telecom`、`Article 50 audio watermark audit`、`Traditional Chinese short emotion telecom fraud audio deepfake`、各篇題名／arXiv ID／資料集名稱。

### 2.2 限制

- 這不是可證明「不存在前作」的系統性回顧；任何未找到精確碰撞的項目都標成 Unknown 或 promising residual gap。
- 2026 年工作可能尚未被所有索引完整收錄。
- RTCFake 的 Hugging Face repository 可確認存在且掛有自訂 license ID。匿名 API 請求回傳 HTTP 401，只能證明未登入不可取，不能證明是自動 gated、人工審核、私有狀態，或「申請即可解」；本輪亦未取得完整 license text，因此不可推定 access 與 redistribution 權利。
- Hugging Face 的 repository license tag 只證明 repository 的宣告，不會自動覆蓋底層語音來源、商用 API 輸出、模型權重或第三方素材的條款；E1、E2、E5、E6 均依此拆開判讀。
- E 節指定「無需再查」的 ASVspoof 5 seed、SpoofCeleb/VoxCeleb 非商用限制與 Deepfake-Eval-2024 scraped-content redistribution 本輪未重做；沒有以沉默表示額外背書。
- VoiceWukong 公開 repository 看得到 user-study results 的存在，但本輪未確認其每一列是否真是 per-sample、per-participant judgment。
- C2PA 查證使用本地原始 preprint `survey/c2pa-verifying-provenance-falls-short.pdf`；該文件是 arXiv:2604.24890v1／IACR ePrint 對應研究，不應誤寫成已 peer-reviewed 的定論。

## 3. A 節：novelty／零前作宣稱

### A1 — shift-aware selective-prediction ADD benchmark 無前作

**狀態：Refuted（廣義宣稱）；窄化後 residual gap 為 Unknown。**

直接前作：

- [Salvi et al., Reliability Estimation for Synthetic Speech Detection, ICASSP 2023](https://resourcecenter.ieee.org/conferences/icassp-2023/spsicassp23vid1808)：訓練 reliability estimator，捨棄不可靠片段，並在 unseen datasets 報告 generalization。
- [Pascu et al., Towards generalisable and calibrated audio deepfake detection with self-supervised representations, Interspeech 2024](https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html)：以 ASVspoof 2019 訓練、跨八個 deepfake datasets；同時報告 discrimination、calibration，並以 threshold 改變保留樣本比例與已保留樣本的正確率。
- [FADEL, ICASSP 2025](https://arxiv.org/abs/2504.15663)：以 evidential deep learning 處理 fake-audio detection 的 uncertainty 與 OOD overconfidence。

**修正後可研究問題：** 在開發集固定一個 risk/coverage operational point，完全不以外部資料調參，轉移到時間較新且 generator-disjoint 的 holdout 時，實際風險上限超標多少？現有前作已做 rejection curve，但本輪未找到完整等同於「固定閾值的跨世代 risk-constraint transfer protocol」的工作。

**對方向一的影響：** 不能以「首次把棄權引入 ADD」為貢獻；可以把核心放在 threshold transfer、constraint violation、failure-boundary diagnosis 與可重現的 temporal holdout protocol。

### A2 — density-based vs discriminative uncertainty 的分家問題沒人問過

**狀態：Unknown；不得宣稱 nobody asked。**

本輪未找到一篇二元 ADD 論文，在相同 unseen-generator protocol 下明確對照 density-based 與 discriminative-derived uncertainty，並以其排序分歧為主要研究問題。但相鄰工作已很接近：

- [TADA, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/stan25_interspeech.html) 使用 SSL embeddings 與 kNN 做 attribution／OOD detection。
- [Open-Set Source Tracing of Audio Deepfake Systems, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/klein25_interspeech.html) 使用 energy score 並報告 FPR95。
- FADEL 使用 evidential uncertainty；Pascu et al. 使用 entropy/reliability；one-class ADD 已有多種 embedding／distance 類方法。

**Inference：** 若保留此 RQ，需先操作化兩類分數、控制共同 backbone 與 representation quality；否則比較結果可能只是模型容量或 embedding 品質差異。

### A3 — confident-real 對抗軸完全缺席

**狀態：Refuted（跨領域概念）；audio-specific protocol 為 Unknown。**

- [Revisiting Adversarial Robustness of Classifiers With a Reject Option](https://openreview.net/forum?id=UiF3RTES7pU) 與 [Stratified Adversarial Robustness with Rejection](https://proceedings.mlr.press/v202/chen23w.html) 已研究攻擊者同時繞過分類與 reject option。
- [Detecting Adversarial Examples Is (Nearly) As Hard As Classifying Them](https://proceedings.mlr.press/v162/tramer22a.html) 明確形式化帶拒絕輸出的 adversarial robust risk。
- ADD 也已有 [CLAD](https://arxiv.org/abs/2404.15854) 與 [Transferable Adversarial Attacks on Audio Deepfake Detection](https://arxiv.org/abs/2501.11902) 等攻擊／防禦工作。

`max P(confident-real|fake)` 本質上接近「targeted high-confidence misclassification while avoiding rejection」，不是全新的安全概念。若要成為貢獻，需給出明確 threat model、quality/query budget 與相對於一般 targeted attack 的增量價值。

### A4 — 用物理可逆性作 laundering 的資訊理論錨

**狀態：Unknown／未獲支持。**

本輪未找到以「不可逆資訊摧毀 vs 可逆分佈偏移」系統分類 ADD laundering、並推導偵測下界的直接前作；但未找到不等於新穎性已確認。現有 audio adversarial／manipulation work 已研究常見處理、可感知品質與攻擊成本，例如 CLAD。

**主要風險：** codec、resampling、filtering、re-recording 與 neural resynthesis 不容易被二分成物理可逆／不可逆；若沒有明確 channel model、充分統計量與可證明 bound，「資訊理論錨」只會是描述性隱喻。

**最小 kill test：** 先選 2–3 個 transformation family，定義資訊損失量與 detector-relevant feature loss；若無法在 toy model 推出可檢驗 prediction，停止使用「information-theoretic lower bound」措辭。

### A5 — 真實電信 × neural codec × reliable bit capacity 無前作

**狀態：Refuted（廣義說法）；精確三者交集為 Unknown。**

- [AudioMarkBench, NeurIPS 2024 Datasets and Benchmarks](https://openreview.net/forum?id=t6LQXcFTEn) 系統評估三個 audio watermark methods 與 15 種 perturbations。
- [Özer et al., A Comprehensive Real-World Assessment of Audio Watermarking Algorithms: Will They Survive Neural Codecs?, Interspeech 2025](https://arxiv.org/abs/2505.19663) 的 RAW-Bench 比較四個方法；Encodec／DAC 下 bitwise accuracy 通常低於 0.5、full-message accuracy 接近 0，直接碰到 neural codec survival。
- [WMCodec](https://arxiv.org/abs/2409.12121) 將 neural speech codec 與 watermarking 聯合設計；ICASSP 2025 亦已有 codec augmentation for robust collaborative watermarking。

因此「neural codec transcode 前作未碰」錯誤。尚可能保留的窄題是：固定真實 RTC platform、端到端 latency 與 payload，在未知 platform processing 下估計可達 BER／payload Pareto frontier；但需再查舊有 telephony watermarking 文獻，不能先稱首次。

### A6 — Article 50 詐騙音訊通道可讀性審計零前作

**狀態：Refuted（Article 50／audio marking 廣義審計）；詐騙通道特定交集為 Unknown。**

- [EU AI Act Article 50 官方條文](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) 要求 synthetic audio 等輸出採 machine-readable、detectable 的標記。
- European Commission 已發布 [Article 50 transparency code of practice 工作頁](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)。
- EU Publications Office 於 2026 發布專門的 [Technical solutions for marking and detecting AI-generated audio content in the context of Article 50(2) AI Act](https://op.europa.eu/en/publication-detail/-/publication/4f7b8585-4829-11f1-8095-01aa75ed71a1/language-en)。

因此「Article 50 標記／audio machine-readability 零前作」不成立。若只研究詐騙電話的端到端存活，可能仍有 deployment-context gap，但法律合規不宜作為 EE 論文唯一技術貢獻。

### A7 — 繁中話術 × 短句 × 情緒 × 通道撞題最少

**狀態：Unknown；精確四軸交集未找到，但鄰近碰撞很多。**

本輪未找到同時完整涵蓋繁中、詐騙話術語意、短句、情緒與通道的控制實驗。最接近工作包括：

- [Audio Deepfake Detection at First Greeting: Hi!](https://arxiv.org/abs/2601.19573)：以 0.5–2 秒詐騙開場與 communication degradation 為核心。
- [Emotion and Acoustics Should Agree](https://arxiv.org/abs/2601.13847) 與 [EmoFake](https://aclanthology.org/2024.ccl-1.99/)：直接研究 emotion／audio deepfake。
- [TeleAntiFraud-28k](https://arxiv.org/abs/2503.24115)：電信詐騙 audio-text、TTS 再生成與 fraud semantics。
- CFSDD dataset card 自稱中文 speech deepfake 與 telecom-fraud scenarios；其資料來源與授權仍需另查。

**Inference：** 四軸一起做會造成嚴重 confounding，且一年碩論難以估 interaction。較合理的 EE 題目只保留兩個可控制因素，例如 duration × emotion，不把繁中或詐騙語意本身當成已驗證 novelty。

### A8 — 真實電信通道存活審計是唯一無前作空白

**狀態：Refuted。**

- [Delgado et al., On Deepfake Voice Detection – It’s All in the Presentation, 2025 preprint](https://arxiv.org/abs/2509.26471) 涵蓋手機、Bluetooth／wired direct injection、loudspeaker presentation，以及呼叫 staged call center 的 real-world setup；其 private dataset 含 80 位參與者、2,263 個 call segments。
- [RTCFake, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.285/) 透過 WeChat、Zoom、QQ、DingTalk、Lark、VooV、Telegram 等真實 black-box RTC platforms 傳輸，約 600 小時，並提供 offline/online paired utterances、unseen-platform 與 unseen-noise evaluation。

**Inference：** 搶先／碰撞風險高。只有「真實 RTC 與特定模擬器的 paired optimism gap」或不同於兩篇前作的 measurement protocol 可能保留；若拿不到 RTCFake 完整資料與條款，應停止把此方向列為主要候選。

## 4. B 節：關鍵前作的存在性與內容

### B1 — D-CAPTCHA / D-CAPTCHA++

**狀態：Verified，惟「使所有互動挑戰題都失去 novelty」是 Inference。**

- [D-CAPTCHA, ACM AsiaCCS 2023](https://arxiv.org/abs/2301.03064)，DOI 10.1145/3579856.3595801；41 位志願者，challenge 條件約 91–100% 對比無 challenge 71% 的宣稱可在原文找到。
- [D-CAPTCHA++, IJCNN 2024](https://arxiv.org/abs/2409.07390)，DOI 10.1109/IJCNN60899.2024.10650401；先展示 transferable imperceptible adversarial attack，再做 adversarial training。

一般性的 audio challenge-response novelty 已被佔據；新提案必須有不同 threat model，例如真正 streaming attacker、不同 challenge entropy 或 deployment constraint。

### B2 — StreamVC 70.8 ms

**狀態：Verified。**

[StreamVC, ICASSP 2024](https://arxiv.org/abs/2401.03078) 報告 Pixel 7 上 60 ms architectural latency + 10.8 ms computation = 70.8 ms end-to-end latency，且定位於 calls/video conferencing。這足以否證「高延遲是現代 streaming VC 的可靠 liveness cue」；但一個單一系統的 latency 不代表所有 attacker capability。

### B3 — AuthentiCall 完整覆蓋 CallAttest delta

**狀態：Partially verified。**

[AuthentiCall, USENIX Security 2017](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/reaves) 確實提供雙方 authentication、conversation integrity、形式化驗證，並把低 bitrate authenticated data 綁到 audio；原文報告偵測 99% tampered audio、worst-case setup 約 1.4 秒。

但「OTT 單邊部署」未獲支持：協定需要雙方 AuthentiCall clients／enrollment／server participation。它大幅侵蝕 CallAttest 的身份與內容完整性 novelty，卻不自動覆蓋單邊、無對方安裝、跨 OTT 平台的 deployment delta。

### B4 — Codecfake 是 IEEE TASLP 2024、100 萬、codec-latent source tracing

**狀態：Refuted／需更正。**

[Codecfake](https://arxiv.org/abs/2406.08112) 的正式場次是 **Interspeech 2024**，不是 IEEE/ACM TASLP 2024。官方資料稱 1,058,216 samples（132,277 real、925,939 fake），涵蓋七種 neural codecs，並評估 unseen codecs。主要任務是 codec-generated／resynthesized speech 的 **binary detection**，不是 source tracing。它確實佔據 neural-codec domain detection 的大量空間，但不能被描述成已完成 codec-latent attribution。

### B5 — FADEL

**狀態：Verified。**

[FADEL](https://arxiv.org/abs/2504.15663) 為 accepted ICASSP 2025 工作，以 evidential learning 處理 audio deepfake detection 的 uncertainty 與 OOD overconfidence。方向一必須列為 primary baseline／closest work，而非只在 related work 一筆帶過。

### B6 — Authenticated Contradictions

**狀態：Verified。**

[arXiv:2603.02378](https://arxiv.org/abs/2603.02378) 與 [CVPR 2026 Workshop APAI 正式 PDF](https://openaccess.thecvf.com/content/CVPR2026W/APAI/papers/Nemecek_Authenticated_Contradictions_from_Desynchronized_Provenance_and_Watermarking_CVPRW_2026_paper.pdf) 對應。應記為 CVPR 2026 workshop paper，不要寫成 CVPR main conference。

### B7 — 三個方法論案例可支持用合成人類模型取代真人

**狀態：存在性 Verified；方法論推論 Refuted／unsupported。**

- [OpenL2D, Scientific Data 2025](https://www.nature.com/articles/s41597-025-04664-y) 使用 synthetic experts，但與真實 fraud analysts 校準／比較。
- [UMUAI 2026 cognitive phishing model](https://link.springer.com/article/10.1007/s11257-026-09441-z) 有 participant-response studies 作 grounding。
- [IMF WP 2025/085](https://www.elibrary.imf.org/view/journals/001/2025/085/article-A001-en.xml) 是金融系統的 cyber stress-testing simulation，不是人類受騙行為量測。

三者不能支持在 voice-scam 新領域直接以「文獻校準的 synthetic human」取代真人 response data。若沒有外部真人資料校準，只能把輸出稱為 simulation sensitivity analysis，不能稱受騙率或 human effectiveness。

### B8 — STOPA = arXiv 2505.14188 source verification、open-set 崩潰

**狀態：Refuted（混合兩篇工作）。**

- [arXiv:2505.14188](https://arxiv.org/abs/2505.14188) 是 Negroni et al. 的 **Source Verification for Speech Deepfakes**，accepted Interspeech 2025；不是 STOPA。它研究 reference/test 是否同源，並分析 speaker diversity、language mismatch、post-processing 與 open-set vulnerability。
- [STOPA, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/firc25_interspeech.html) 是 Firc et al. 的 **Systematic VariaTion Of DeePfake Audio** dataset，服務 open-set source tracing/attribution。

CLAIMS 文件把題名、縮寫與 arXiv ID 混在一起。兩篇都存在且都會侵蝕一般性的 open-set source-linking novelty，但應分開引用，不能說 STOPA 的 arXiv ID 是 2505.14188。

## 5. C 節：具體數字

### C1 — VoiceWukong detector 與人類研究數字

**狀態：數字 Verified；per-sample human-data 可得性 Unknown。**

[VoiceWukong, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/yan-ziwei) 支持：AASIST2 EER 為 English 13.50%、Chinese 13.54%，其他受測方法均高於 20%；若干 detector／language cell 的 AUC 接近 0.5。人類研究共三輪，每輪 38 份中文與 68 份英文 questionnaires，共 318 questionnaire completions；這不必然等於 318 位不重複 participants。

作者 [GitHub repository](https://github.com/VoiceWukong/VoiceWukong) 公開 `Userstudy/result` 與原始輸出，但本輪未確認其粒度是否足以建立每個 audio sample 的 human correctness/uncertainty。不得先寫「Zenodo 申請後可得 per-sample 人類標籤」。

### C2 — 閉源商用生成器使 EER 從 <1–5% 升至 13.5–50%

**狀態：Partially verified；因果歸因過度。**

VoiceWukong 支持 benchmark gap：例如 AASIST2 原始 benchmark 約 0.82% EER、VoiceWukong 最佳約 13.5%；RawBoost 原始約 5.31%、VoiceWukong 約 23.48%；完整測試 cell 可高到約 50%。但 VoiceWukong 混合 19 個 commercial tools、15 個 open-source tools 與多種 manipulations，不能把整個 13.5–50% 區間單獨歸因於「閉源商用生成器」。

**建議寫法：** 「模型從原 benchmark 的低個位數 EER，轉到包含商用／開源新工具與 manipulation 的 VoiceWukong 後，EER 可升至 13.5% 以上，部分 cell 接近隨機。」

### C3 — ASVspoof 2021 DF = 611,829

**狀態：Verified。**

[ASVspoof 2021 官方頁](https://www.asvspoof.org/index2021.html) 提供 DF database 與 protocol；同資料的正式論文 protocol/table 報告 DF evaluation set 共 611,829 utterances。引用時應寫清楚這是 **DF evaluation set**，不是 train+dev+eval 總量。

### C4 — C2PA 五項安全目標全部未達成

**狀態：Verified as authors' finding；證據層級需註明 preprint。**

本地原文 `survey/c2pa-verifying-provenance-falls-short.pdf`（Golaszewski et al., arXiv:2604.24890v1，2026-04-23）列出兩項 C2PA claimed goals：claim integrity、weak file integrity；以及作者主張必要的三項 additional goals：timestamp agreement、validator consistency、strong file integrity。作者明確結論是 versions 2.2–2.4 與 implementations 未達成這五項。

這是該研究團隊的安全分析結論，不應擴寫成所有學界已形成共識；引用時需保留版本範圍與 preprint status。

## 6. D 節：資料集可得性與授權

### D1 — ASVspoof、In-the-Wild、MLAAD 都可自由下載且可學術用

**狀態：Partially verified；「自由」需拆成下載與使用條款。**

- [ASVspoof 2021](https://www.asvspoof.org/index2021.html)：官方 Zenodo download；ODC Attribution license。
- [ASVspoof 2019 LA](https://datashare.ed.ac.uk/handle/10283/3336)：官方 Edinburgh DataShare 可下載；實際使用仍需遵守資料頁條款與來源語音權利。
- [In-the-Wild](https://deepfake-demo.aisec.fraunhofer.de/in_the_wild)：官方下載頁；資料頁標示 Apache 2.0。
- [MLAAD v9](https://deepfake-demo.aisec.fraunhofer.de/mlaad)：官方透過 Hugging Face 提供，CC BY-NC 4.0；目前頁面要求登入、同意分享聯絡資訊後才能存取，不是匿名自由下載。fake audio 與所依賴的 M-AILABS bona-fide audio 需分別遵守條款。

結論是「有官方取得管道且原則上可作非商業研究」大致成立，但 license 與 access friction 並不相同；尤其 MLAAD 的登入同意、NC 限制與 real-audio upstream license 不能省略。

### D2 — RTCFake real/fake 配對、真實 RTC、可學術重散布

**狀態：技術內容 Partially verified；redistribution Unknown。**

[RTCFake paper](https://aclanthology.org/2026.findings-acl.285/) 與 [Hugging Face repository](https://huggingface.co/datasets/JunXueTech/RTCFake) 均存在。論文支持：

- 約 600 小時、307 speakers；
- 經多個真實 black-box RTC platforms 傳輸；
- 對同一 utterance 提供 offline/online pairing；
- 有 bona-fide 與 spoof labels，並設計 seen/unseen platform/noise splits。

需修正「real/fake 配對」措辭：論文清楚的是 **同一來源 utterance 的 offline/online 配對，且兩個 class 都有資料**，不等於每個 real sample 都有同內容、同說話者的 fake twin。

Hugging Face 顯示自訂 `rtcfake-license`，但匿名 API 回傳 HTTP 401，本輪也未取得可確認「允許 academic redistribution」的完整條文。**401 不等於已證實的 gated 申請流程；在 access mechanism 與授權文字被人工保存、審核前，只能視為可見 repository，不能視為可取得或可重散布。** 這仍是方向四／五的 single-point risk。

### D3 — VoiceWukong per-sample human data 在 Zenodo、申請制

**狀態：Partially refuted。**

- [VoiceWukong audio dataset v1](https://zenodo.org/records/13731918) 是 restricted access；條款限 academic evaluation、禁止 redistribution／commercial use，並要求申請與機構承諾。
- [VoiceWukong v3 code/software record](https://zenodo.org/records/14862059) 是公開的 code／leaderboard／weights replica，不等於完整受限 audio dataset。
- user-study result files 看起來存在於公開 GitHub；是否具有可直接做 per-sample selective-analysis 的 row-level labels仍未驗證。
- 核准率與平均核准時間未公開，屬 Unknown。

因此不能把「申請制 per-sample human data」放入關鍵路徑。若需要新版人類判斷資料，可另外評估 Fraunhofer AISEC 的 [Human Perception of Audio Deepfakes (2026)](https://deepfake-demo.aisec.fraunhofer.de/human_perception_2026)：官方頁稱 35,532 judgments、1,768 anonymous participants、138 systems，且 CSV 為 judgment-level；但其 associated preprint 尚待正式發布與方法細查。

### D4 — Delgado 團隊已進場，真實通道搶先風險最高

**狀態：前作存在 Verified；風險排序為 Inference。**

Delgado et al. 的 2025 preprint 已做裝置／presentation／call-center 實驗，RTCFake 2026 又提供更大規模 RTC benchmark。因此「真實通道」若沒有 paired simulation-bias、公開 protocol 或不同 threat model，碰撞風險確實高。這是有強證據支持的風險判斷，但「最高」仍是相對於其他候選的決策性 inference。

## 7. E 節：2024–2026 新資料集與模型資產

### E1 — DFADD：diffusion／flow-matching、MIT、2025-04 修正版

**狀態：Verified；版本與衍生授權需保留。**

- [DFADD 論文](https://arxiv.org/abs/2409.08731)與[官方 repository](https://github.com/isjwdu/DFADD)支持其為 SLT 2024 資料集，包含五種 TTS：Grad-TTS、NaturalSpeech 2、StyleTTS 2、Matcha-TTS、PFlow-TTS；前三者屬 diffusion，後兩者屬 flow matching。
- 論文報告 109 speakers、44,455 bona-fide、163,500 spoof，spoof 約 179.88 小時；英文、16 kHz、speaker-disjoint。當前 [Hugging Face repository](https://huggingface.co/datasets/isjwdu/DFADD) 是公開非 gated，viewer 顯示 207,955 rows；hosting／壓縮後體積與論文時數不是同一種規模指標。
- 官方 changelog 的 2025-04 更新明載：修正 Matcha-TTS audio 與 labels mismatch，並統一 audio formats。因此實驗必須記錄取得日期／commit，不能混用舊版。
- GitHub 與 Hugging Face 均標示 MIT；但官方頁同時指出 VCTK、LJSpeech 等來源，使用者仍須保留 upstream attribution／license audit。MIT tag 不應被解讀為消除所有底層條款。

2019／2021 challenge corpus 按時間不可能包含這些具名的較晚系統，故它可提供較新的 generator family；但「名字較新」不自動等於嚴格 unseen。是否有訓練語料、聲學模型或 vocoder family overlap，仍需在 split manifest 中逐一控制。

### E2 — CodecFake+：101 GB、MIT、與 CodecFake 的關係

**狀態：Partially verified；不是另一個無關的同名資料集。**

- [官方 Hugging Face repository](https://huggingface.co/datasets/CodecFake/CodecFake_Plus_Dataset) 公開、非 gated，metadata 標示 MIT，repository 約 101 GB；檔案樹可見四個約 25.1 GB 的 CoRS archives、CoSG archive 與 label／protocol files。
- [目前 arXiv 版本](https://arxiv.org/abs/2501.08238)已於 2026-06 修訂，publication status 是 IEEE/ACM TASLP 2026。它以 31 個 codec models（21 codec types）產生 codec-resynthesized speech（CoRS），並以 17 個 codec-based speech-generation systems（9 codec types）的 CoSG 作評估。
- CodecFake+ 是 Interspeech 2024 **CodecFake** 的後繼／擴充，不是毫無關係的另一資料集。原 CodecFake 與更新版在規模、codec coverage 與 protocol 上要分開引用，但不能寫成兩個碰巧同名的獨立來源。
- CoRS 是把 bona-fide 經 codec 重建後當作 actual codec-fake 的 proxy training data；CoSG 才是實際 codec-based generation。若拿來研究 laundering，必須明確指定使用哪一部分，否則 threat model 會混淆。

Repository-level MIT 與公開下載可確認；底層 bona-fide sources 的再散布與衍生權利仍需在正式納入前做 partition-level audit。

### E3 — RTCFake：access、配對與重散布

**狀態：技術內容 Partially verified；access、核准條件與 redistribution Unknown。**

[Findings of ACL 2026 論文](https://aclanthology.org/2026.findings-acl.285/)支持約 600 小時、307 speakers、真實 black-box RTC platforms，以及 seen／unseen platform 和 noise evaluation。配對是同一 utterance 的 offline／online 版本，bona-fide 與 spoof 兩類都有；不是逐筆 real/fake content-matched twins。

[Hugging Face repository](https://huggingface.co/datasets/JunXueTech/RTCFake) 顯示自訂 `rtcfake-license`，匿名 API 實測為 HTTP 401。這不足以判定其為何種 gated flow，也不能推導審核時間、核准條件或可重散布。**結論：目前不可把 RTCFake 放在碩論關鍵路徑；只有在本人完成登入後的條款人工審核、取得方式測試與小樣本 schema audit 後，才能升級。** 本輪依規範未替作者登入、申請或下載大型資料。

### E4 — MLAAD v10／v9 與 v5 差異

**狀態：Refuted as written。官方目前是 v9，不是已確認的 v10。**

- [官方 MLAAD 頁](https://deepfake-demo.aisec.fraunhofer.de/mlaad)與 [deepfake-total](https://deepfake-total.com/mlaad)目前均稱 **version 9**：超過 1,000 小時 fake audio、50+ languages、175+ TTS models，CC BY-NC 4.0。
- [Hugging Face tree](https://huggingface.co/datasets/mueller91/MLAAD/tree/main)要求登入並同意分享聯絡資訊才能取得；因此「v10、公開匿名下載」兩部分都不成立。
- [IJCNN 2024 原始論文](https://arxiv.org/abs/2401.09512)描述較早快照：378 小時、38 languages、82 TTS models。可以確認資料集後續大幅擴充，但本輪未找到官方逐版 changelog，不能精確聲稱「v10 相對 v5 的每項差異」。

對主題一的含義：MLAAD 仍可作多語、多模型 development／external corpus 候選，但要寫成 **v9 gated-contact-share、fake-only**，並另配合法取得的 bona-fide data；不能用「v10 最新公開資料」作賣點。

### E5 — SpeechFake 開源部分、中文與授權

**狀態：Partially refuted。中文涵蓋 Verified；Apache-2.0 不能套到整個 audio dataset。**

- [ACL 2025 論文](https://aclanthology.org/2025.acl-long.493/)報告 300 萬以上 fake utterances、3,000+ 小時、40 個 generation tools、46 languages；baseline subset 含英文與中文，multilingual subset 的 train/dev 亦含英文與中文，故中文 coverage 成立。
- [Hugging Face repository](https://huggingface.co/datasets/DeepFense/SpeechFake)標示 Apache-2.0，但目前主要存放 paths、protocol／metadata parquet 與下載指引，不是把全部 audio 直接以 Apache-2.0 包在 56.8 MB repository 中。
- 原始論文的 license section 說明：釋出 fake part，real data 以來源連結處理；主要 actual dataset 採 CC BY-NC 4.0，部分 partition 另有 GPL-3.0 等條款，商用 API 產物則受非商業研究條件影響。

因此它可以是新資料與 zh-CN coverage 的候選，但正式使用前要以實際 partition 建 license matrix，並先確認下載 scripts 目前能取得哪些音訊；不能只看 Hugging Face 的 Apache tag。

### E6 — CosyVoice 2、F5-TTS、GPT-SoVITS、OpenVoice v2

**狀態：checkpoint／code 可得性大致 Verified；「2025 世代、台灣國語＋哭腔／急迫」Partially refuted／Unknown。**

| 候選 | 官方可得性與 license | 已有官方能力證據 | 不可直接宣稱的部分 |
|---|---|---|---|
| [CosyVoice 2](https://github.com/FunAudioLLM/CosyVoice) / [0.5B model](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B) | code、model 均標示 Apache-2.0 | 中文 zero-shot、instruct／方言示例、笑聲等細粒度控制 | 2024-12 已發布，不是純 2025 模型；沒有台灣國語＋哭腔／急迫的正式驗證 |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | code MIT；官方 pretrained weights 因 Emilia 標示 CC BY-NC | 中英語音與 reference-prompt generation | 不可把 code license 當 weights license；指定台灣腔與兩種情緒需 pilot |
| [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | repository MIT，提供官方 releases／weights；底層 components 仍需逐項 audit | 中文、粵語、英日韓；v3 notes 提及更豐富情緒表現 | README 仍把進一步 TTS emotion control 列為未完整實作；台灣國語未驗證 |
| [OpenVoice v2](https://github.com/myshell-ai/OpenVoice) | code 與 V1/V2 weights MIT，官方明載 research／commercial 可用 | native Chinese、style control（emotion、accent、rhythm 等） | v2 是 2024-04；台灣國語、哭腔與急迫的組合品質未有正式 benchmark |

研究上的安全結論不是「四者都能做」，而是先選兩個 license 較清楚且機制不同的模型做 20–50 句 pilot，使用有同意的台灣說話者 reference，人工確認 accent、emotion、可懂度與 identity leakage。若達不到預註冊品質門檻，D4 應縮成現成 zh-CN 資料比較，不能用主觀挑選成功樣本補洞。

### E7 — CFAD 中文資料

**狀態：存在與涵蓋 Verified；精確 license Unknown（官方頁內部矛盾）。**

[官方 Zenodo record](https://zenodo.org/records/8122764)公開約 35.6 GB 的 Mandarin dataset，包含 12 種 fake types（11 種 synthesis 與 1 種 partially fake），另有 clean、noise 與 codec versions、speaker-disjoint train/dev/test，以及 seen／unseen fake tests。它適合做 zh-CN 歷史對照與 codec/noise control。

但同一官方 record 的 description 寫 CC BY-NC-ND 4.0，Rights metadata 卻寫 CC BY 4.0；第三方 Hugging Face repack 的 CC BY tag 不能解決官方矛盾。應採較保守條款，或在納入再散布／衍生流程前請作者澄清。另須註明：資料建立於 2022 左右、期刊版為 Speech Communication 2024；它不是 2025–2026 新生成器 holdout，也不代表台灣國語或情緒語音。

### E8 — RAW-Bench／《Will They Survive Neural Codecs?》

**狀態：論文與內容 Verified；「唯一直接前作」Refuted。**

[Interspeech 2025 正式頁](https://www.isca-archive.org/interspeech_2025/ozer25_interspeech.html)、[arXiv:2505.19663](https://arxiv.org/abs/2505.19663)與[官方 repository](https://github.com/SonyResearch/wm_robustness_eval)均存在。RAW-Bench 評估四種 audio watermarking algorithms 在真實 transformation pipeline 下的穩健性，並發現 neural codecs 是最困難的操作之一；它確實是方向五非常接近的 benchmark baseline。

但截至 2026-07，至少還有下列直接相鄰工作：

- [Deep Audio Watermarks are Shallow](https://arxiv.org/abs/2504.10782)（ICLR 2025 GenAI Watermarking workshop）研究 speech watermark 經 transformations／removal 的脆弱性；
- [Defend for Self-Vocoding](https://www.isca-archive.org/interspeech_2025/lin25d_interspeech.html)（Interspeech 2025）直接研究 neural vocoder reconstruction 對 watermark recovery 的破壞與防禦；
- [Latent-Mark](https://arxiv.org/abs/2603.05310)（2026 preprint）以 neural resynthesis／semantic compression robustness 為核心。

所以可說 RAW-Bench 是「最接近的獨立 benchmark 之一」，不能說是唯一直接前作。方向五若保留，必須提出比既有 robustness benchmark 更窄且可量測的 delta，例如固定通訊平台與 codec 的 BER–payload–quality frontier；否則 novelty 不足。

### 7.1 E 節對資料組合的直接建議

**Inference / recommendation：** 對目前第一候選「未知生成器下的棄權門檻轉移」，較穩健的最小資料設計是：

1. 歷史 train／dev anchor 固定為一個既有 benchmark，不因看到 holdout 結果而換 seed corpus。
2. 先以 **DFADD 2025-04 corrected release** 做 diffusion／flow-matching family holdout；保存 commit、file list 與 label sanity check。
3. 再從 **CodecFake+ 的 CoSG** 或 SpeechFake 可合法取得的明確 partition 選一個不同機制的第二 holdout；不要把 CoRS proxy 與 actual generated fake 混成同一語意。
4. MLAAD v9 僅在登入條款可接受且 fake-only pairing 問題解決後加入；RTCFake 不列關鍵路徑。
5. Deepfake-Eval-2024 若依其條款只能 evaluation，就只作 untouched final external test，不用於 calibration、threshold selection 或方法選擇。

這套組合重視的是 **generator mechanism 與時間的角色分離**，不是單純追求資料集發布年份。資料越新越好只在版本、標記、授權與 threat model 可控時成立。

## 8. 對五個方向的重新排序

| 查證後順位 | 方向 | 查證後可守住的核心 | 關鍵風險／停止條件 |
|---|---|---|---|
| 1 | 未知生成器下的可信棄權 | development-fixed threshold 的跨世代 transfer、risk constraint violation、failure boundary | 不得聲稱首次可靠棄權；若 closest-work 出現相同 fixed-threshold protocol，或 pilot 無可分析的 risk/coverage structure，轉向 |
| 2 | 有界黑箱洗白最低成本 | 有明確 query、quality、transform-depth budget 的 high-confidence escape cost | generic adversarial reject-option 與 ADD attacks 已存在；若「reversibility」無可檢驗 formalization，移除資訊理論主張 |
| 3 | 華語 duration × emotion | 僅兩因素的 controlled interaction 與 generator shift | 不做四軸；若 paired/control data 無法建立，停止 |
| 4 | 真實 vs 模擬 RTC 的 optimism gap | 同 utterance 的 real-platform vs reproducible simulation paired comparison | RTCFake／Delgado 已強碰撞；license 或 paired data 不可得即停止 |
| 5 | 通訊條件下 watermark payload frontier | 極窄、明示 platform/codec/latency 的 BER–payload–quality frontier | neural-codec robustness 已非空白；若只是重做 AudioMarkBench/RAW-Bench，停止 |

## 9. 主題一是否適合作為電子工程碩士論文

**結論：可以，而且技術上屬於電子工程常見的語音訊號處理、機器學習與系統可靠度交界；但要有工程／方法貢獻，不能只做資料集排行榜。**

適合作為 EE 碩論的條件：

1. **明確系統輸入輸出：** waveform → detector score／uncertainty → accept/abstain decision。
2. **數學上可檢驗的 operating criterion：** coverage、selective risk、AURC、risk-constraint violation、calibration error，並區分 ranking quality 與 fixed-threshold transfer。
3. **可重現 signal/ML pipeline：** 至少兩個 detector、預先固定的 train/dev/test roles、generator-family split、dataset version/hash、無 holdout tuning。
4. **統計可信度：** 多 seeds 或 deterministic baseline、bootstrap confidence intervals、按 generator/language/source 分層，並診斷 channel、duration、quality 等 confound。
5. **至少一個技術 artifact：** 建議是 reusable threshold-transfer evaluation protocol；若時間允許，再提出一個小而清楚的 shift-aware score normalization／calibration improvement。後者不必追求新 backbone。

不夠像 EE 碩論的版本：只套六種 uncertainty library、在多個 dataset 畫 risk–coverage 圖，然後宣稱某法最好。這會像 benchmark report，且 A1 已有近前作。

### 9.1 建議題目修訂

比目前題目更精準的版本：

> **未知語音生成器下深偽偵測棄權門檻的可轉移性：跨資料集風險違約與失效邊界**

英文：

> **Transferability of Abstention Thresholds for Audio Deepfake Detection under Unseen Generators: Cross-Dataset Risk Violations and Failure Boundaries**

這個題目把「可信」從結論改成待檢驗命題，也直接避開 A1 的過度 novelty 宣稱。

### 9.2 可辯護的貢獻組合

**C1 — Measurement contribution（核心）**  
建立 development-fixed、generator-disjoint、temporal holdout 的 selective-evaluation protocol，分開量測：

- uncertainty ranking 是否仍有效；
- 固定 threshold 是否仍達成 risk target；
- 失敗是 calibration shift、ranking collapse，還是 detector 本身接近隨機。

**C2 — Empirical contribution（核心）**  
在受控新生成器與真實流通 holdout 上，量化 risk constraint violation、coverage collapse 與 high-confidence error，並以 generator family／語言／來源做 failure map。

**C3 — Method contribution（選配但推薦）**  
提出一個輕量、development-only 的 score normalization／conformal risk control／embedding-aware calibration 方法；成功標準不是整體 EER SOTA，而是在至少兩個 untouched holdout 上降低 risk violation，且不過度犧牲 coverage。

**C4 — Negative-result contribution（成立）**  
若所有 uncertainty score 的 threshold 都無法轉移，則證明「低 confidence 可作部署安全閥」在新生成器下不成立，並指出其失效條件。這是可用的負結果，但要有足夠 base detector performance 與 confound controls。

## 10. 下一個最小驗證與停止條件

### 下一個最小驗證

用一個已可重現 detector、MSP/entropy 與一個 embedding score，在一個 dev dataset 設定兩個 risk targets（例如 5%、10%），完全凍結後跑一個 generator-disjoint、時間較新的 10–20% pilot subset。主要輸出只做：

- dev 選定 threshold；
- external observed risk、coverage 與 risk violation；
- AURC／error-detection AUROC；
- 每 generator family 的 bootstrap interval；
- base AUROC/EER gate。

### 成功條件

- 至少一個 detector 在 external pilot 不接近隨機；
- ranking 與 threshold transfer 呈現可重複、可解釋差異；
- 資料 split 可以在 generator-family 層級證明無洩漏；
- 結果不是完全由語言、取樣率、duration 或來源 pipeline 解釋。

### 停止／轉向條件

- 找到與 fixed development threshold + newer generator-disjoint holdout + risk violation 幾乎相同的前作，且沒有明確 measurement delta；
- 所有外部 detector 接近隨機，使 abstention 分析退化成「全部拒絕」；
- generator metadata 不足，無法支持 unseen-generator claim；
- pilot 的差異只由 dataset/source shortcuts 解釋；
- 需要用 holdout 調 threshold 才能得到正面結果。

## 11. 給 Claude 的交接摘要

Claude 更新五方向時應採用以下修正：

1. D1 保留第一順位，但刪除「selective ADD 無前作」；主張改為 fixed-threshold temporal/generator transfer 的 residual gap。
2. FADEL、Salvi 2023、Pascu 2024 同列 closest work；不能只把 FADEL 當唯一競爭者。
3. D2／真實 RTC 大幅降級；RTCFake 與 Delgado 已直接碰撞，且 RTCFake redistribution 未核實。
4. D5 刪除「neural codec 未碰」；AudioMarkBench、RAW-Bench、WMCodec 必須納入。
5. B4 更正為 Codecfake／Interspeech 2024／binary detection；B8 拆成 Source Verification 與 STOPA 兩篇。
6. VoiceWukong 數值可用，但 per-sample human-data 不能當已驗證資產。
7. E1 的 DFADD 可保留，但鎖定 2025-04 corrected release；E2 的 CodecFake+ 是 CodecFake 後繼，且 CoRS proxy／CoSG actual fake 必須分開。
8. E3 的 RTCFake 401 不足以證明 gated 可解；access、核准條件、完整 license 與 redistribution 都是 Unknown，不得放關鍵路徑。
9. E4 改成 MLAAD **v9**、gated contact-share、CC BY-NC 4.0；刪除 v10 公開下載宣稱。
10. E5 的 SpeechFake 有中文，但 Apache-2.0 只可安全地描述 HF metadata／protocol repository；actual audio 以 CC BY-NC 4.0 為主且有 mixed-license partitions。
11. E6 不得把台灣國語＋哭腔／急迫當已驗證模型能力；先做兩模型小 pilot。E7 的 CFAD 是較舊 zh-CN 對照，官方 license 欄位互相矛盾。
12. E8 將 RAW-Bench 改寫為 closest baseline **之一**，並加入 Deep Audio Watermarks are Shallow、Defend for Self-Vocoding、Latent-Mark 等相鄰工作。

## 12. 目前建議

**Recommendation：** 主題一可繼續作第一候選，也適合電子工程碩論，但應立刻改名與改寫貢獻。先完成 fixed-threshold transfer pilot，再決定是否正式定題；在 pilot 前不更新 `DECISIONS.md` 為已選定方向。

**Promising idea, not yet a verified research gap：** 目前可辯護的是「跨世代固定棄權門檻的風險違約與失效邊界」值得測，不是「語音深偽首次可信棄權」。
