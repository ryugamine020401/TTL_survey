# Survey：Deepfake Audio Detection 文獻收錄清單

最後更新：2026-07-13
收錄文獻：8 篇（4 篇原有 + 4 篇新下載）

## 收錄總覽

| # | 文獻 | 類型 | 出處 | 檔案 |
|---|------|------|------|------|
| 1 | Audio Deepfake Detection: What Has Been Achieved and What Lies Ahead | Survey | Sensors 2025 (Zhang et al.) | `audio-deepfake-detection-achieved-and-ahead.pdf` |
| 2 | VoiceWukong: Benchmarking Deepfake Voice Detection | Benchmark | USENIX Security 2025 (Yan et al.) | `voicewukong-benchmarking-deepfake-voice-detection.pdf` |
| 3 | Benchmarking Audio Deepfake Detection Robustness in Real-world Communication Scenarios | Benchmark | arXiv 2504.12423 (Shi et al., Loughborough) | `benchmarking-robustness-communication-scenarios.pdf` |
| 4 | C2PA Technical Specification v2.4 | 標準規格 | C2PA, 2026-04（最新正式版） | `c2pa-technical-specification-v2.4.pdf` |
| 5 | C2PA and Content Credentials Explainer v2.4 | 標準導讀 | C2PA, 2026 | `c2pa-content-credentials-explainer-v2.4.pdf` |
| 6 | Verifying Provenance of Digital Media: Why the C2PA Specifications Fall Short | 安全分析 | UMBC Cyber Defense Lab (Golaszewski, Krawetz, Sherman et al.) | `c2pa-verifying-provenance-falls-short.pdf` |
| 7 | Authenticated Contradictions from Desynchronized Provenance and Watermarking | 攻擊研究 | CVPR 2026 Workshop APAI (Nemecek et al., CWRU/UCLA), arXiv 2603.02378 | `authenticated-contradictions-desync-provenance-watermark.pdf` |
| 8 | A Review of Tools and Technologies to Combat Deepfakes | Review | Information (MDPI) 17(4):347, 2026 (Erokhin & Komendantova) | `review-tools-technologies-combat-deepfakes.pdf` |

三大主題分佈：
- **被動偵測（passive detection）與其極限**：#1、#2、#3
- **密碼學溯源（provenance）與其極限**：#4、#5、#6、#7
- **全局視野 / 分層防禦**：#8

---

## 各篇摘要

### 1. Audio Deepfake Detection: What Has Been Achieved and What Lies Ahead
**一句話定位**：涵蓋 audio deepfake 生成、資料集、偵測方法與新興議題（隱私、公平性、可解釋性）的綜合性 survey。

系統性回顧 audio deepfake detection（ADD）進展：從生成端（TTS、VC）出發，整理主流資料集（ASVspoof 系列、In-the-Wild 等），再依 frontend feature（handcrafted LFCC/CQCC vs. self-supervised Wav2Vec2/WavLM/XLS-R）、backend classifier（GMM、ResNet、CapsNet、GNN）與 end-to-end 系統（RawNet2、AASIST、RawGAT-ST）分類比較。以 ASVspoof 2019 LA 的 EER 排行（最佳 0.06%）與 In-the-Wild 的表現對照，指出 in-domain 與 out-of-domain 成績落差巨大。亦涵蓋 privacy-preserving detection（SafeEar）、explainability、fairness、主動式 watermarking 與壓縮 robustness 對策（FTDKD、E-Specs）。

**關鍵發現**：
- 現有模型 in-domain EER < 1%，但跨語言、跨 domain、面對 novel attacks 時 generalization 明顯受限；SSL 特徵 + data augmentation 是目前最有效的緩解手段
- 訓練資料多為 lossless（FLAC），真實場景多經 MP3/AAC/Opus lossy compression，顯著降低偵測 robustness
- 人類辨識 deepfake audio 準確率僅約 73%，機器模型也未穩定勝過人類直覺
- 主動式 watermarking 與被動偵測互補，但依賴生成端合作

**對論文的啟示**：「generalization to unseen attacks」與「真實條件下的 robustness」是領域最核心的 open problems，現有資料集缺乏真實傳輸條件的覆蓋。

### 2. VoiceWukong: Benchmarking Deepfake Voice Detection
**一句話定位**：用商用（閉源）+ 開源生成工具與後處理 manipulation 變體，實測 SOTA 偵測器在貼近真實條件下表現的大規模 benchmark。

蒐集 19 個商用工具 + 15 個開源模型生成的 deepfake 語音，施加 6 類後處理 manipulation（noise injection、time stretching、resampling、fading、replay 等）產生 38 個變體，共 265,200 筆英文與 148,200 筆中文樣本。評測 12 個 SOTA 偵測器：最佳的 AASIST2 EER 為 13.50%（英）/ 13.54%（中），其餘全部超過 20%，數個接近隨機猜測（AUC≈0.5）。並含 300+ 人 user study 與 MLLM（Qwen2-Audio）比較。

**關鍵發現**：
- 對閉源商用工具生成的樣本，SOTA 偵測器 EER 從原論文的 <1–5% 暴增至 13.5–50%（如 AASIST2 原報告 0.82% → 實測 13.5%；RawBoost 5.31% → 23.48%），直接量化 generalization gap
- 跨語言（英→中）落差可達 23 個百分點
- 常見補救策略（targeted augmentation、multi-domain training）幾乎無效，multi-domain training 甚至讓 AASIST2 退化至接近隨機（EER 48–50%）
- 人機能力互補：人類對低品質 deepfake 優於偵測器（FAR 4–19%），對高品質遠差於偵測器（FAR > 82%）；MLLM 完全不具偵測能力（英文 F1=0）

**對論文的啟示**：以最大規模證明「學術偵測器在閉源生成器 + 後處理下大幅失效，且現有優化策略補救有限」；支持人機協作偵測框架的方向。

### 3. Benchmarking Audio Deepfake Detection Robustness in Real-world Communication Scenarios
**一句話定位**：針對通訊場景（codec 壓縮 + 封包遺失）的 robustness benchmark，並提出對應的 data augmentation 解法。

建立 ADD-C 測試集：以 FoR、Wavefake+LJSpeech、MLAAD+M-AILABS、ASVspoof2021 LA 為基礎（130,041 real / 240,373 fake、36 種生成演算法），用 6 種 codec（AMR-WB、EVS、IVAS、OPUS、Speex、SILK）× 5 種 Packet Loss Rate（0–20%）構成 C0–C5 六個條件。GMM、LCNN、AASIST 三個 baseline 僅從 C0 到 C1（壓縮、0% 丟包）就平均劣化 EER 5.30%。提出通道模擬 DA 策略（訓練集擴增 5 倍至 1,832,070 筆），重訓後全條件 EER 波動 < 0.1%。

**關鍵發現**：
- codec 壓縮本身（未計丟包）就足以顯著劣化 ADD 性能，丟包率越高劣化越深
- 通道模擬 DA 能幾乎完全消除劣化 → 退化主因是 train/test distribution shift，而非資訊被不可逆摧毀
- 但解法假設已知目標通道的 codec 與 PLR 分布，對未知 codec（如社群平台私有轉檔管線）的泛化未驗證

**對論文的啟示**：確立「通訊/壓縮通道」是 ADD 部署的關鍵失效模式；殘留 gap 在於未見過 codec、真實通道、社群平台轉檔的泛化，以及與 unseen-generator generalization 的交互作用。

### 4. C2PA Technical Specification v2.4
**一句話定位**：C2PA 官方核心技術標準，研究 provenance 方案能力與限制的第一手權威文件。

定義 Content Credentials 完整架構：以密碼學簽署的 manifest 與 assertions 記錄資產的產生方式與修改歷程，涵蓋 provenance 資料儲存格式、COSE 數位簽章要求、基於 X.509 憑證的信任模型、多種媒體格式的嵌入方式，以及 validator 應如何評估 manifest 的完整性與可信度。

### 5. C2PA and Content Credentials Explainer v2.4
**一句話定位**：C2PA 官方入門導讀，進入完整技術規格前的高層次說明。

闡述 C2PA 的動機（在生成式媒體普及下重建對數位媒體的信任）、自願採用（opt-in）的溯源方案定位、架構概觀、使用情境、manifest / assertion 等關鍵組件的直觀說明與信任模型基本概念。

### 6. Verifying Provenance of Digital Media: Why the C2PA Specifications Fall Short
**一句話定位**：對 C2PA（v2.2–2.4）的首個獨立綜合性安全分析（含 formal methods），屬攻擊/安全分析類文獻。

釐清 C2PA 提供的是 provenance（檔案歷史）而非 authenticity（內容真實性），但宣傳材料常誇大。C2PA 規格只宣稱兩項安全目標（claim integrity、weak file integrity），作者補充三項必備目標（timestamp agreement、validator consistency、strong file integrity），並證明現行 C2PA **五項全部未達成**。

**關鍵發現**：
- timestamp 未被簽章綁定、可無痕替換；revocation 檢查為 optional——Nikon Z6 III 憑證被撤銷六個月後，Adobe Inspect 仍判有效而 Verifieddit 判無效（同一張圖矛盾結論）
- exclusion range 內的資料（如 Pixel 10 Pro 的 GPS）可被竄改而不破壞簽章：「簽章有效」≠「檔案未被動過」
- 憑證過期使已簽署媒體數月內失去可驗證性，與法定保存年限不相容（Arizona 選舉試點案例）
- 已示範用 conforming 相機替 AI 生成影像簽出「真實拍攝」憑證；且 provenance 依賴主動簽署，對不附 credential 的惡意 deepfake 完全無覆蓋

**對論文的啟示**：密碼學 provenance 目前無法單獨承擔對抗 deepfake 的任務，為「被動 detection 與密碼學 provenance 如何互補整合」提供明確的 research gap 論證。

### 7. Authenticated Contradictions from Desynchronized Provenance and Watermarking
**一句話定位**：展示 C2PA 溯源與不可見浮水印兩層驗證訊號可被「去同步」而互相矛盾的攻擊研究，並提出跨層稽核協定。

指出 C2PA 與 invisible watermarking 雖被定位為互補防線，但兩個驗證層技術上彼此獨立。作者形式化並實證「Integrity Clash」：一個資產可同時攜帶密碼學上有效、宣稱人類創作的 C2PA manifest，而像素卻帶有標識 AI 生成的浮水印，且兩者驗證皆通過。他們用 metadata washing 工作流程——僅利用標準編輯流程、省略規格允許省略的單一 assertion 欄位——即可產生「經認證的假內容」，完全不需破解密碼學。提出的跨層稽核協定在 3,500 張測試影像（四種衝突狀態 × 三種擾動）上達 100% 分類準確率。

**對論文的啟示**：單一驗證訊號各自「有效」不代表整體可信——多訊號之間的一致性檢查本身就是一個新的研究層次，此思路可遷移到 audio。

### 8. A Review of Tools and Technologies to Combat Deepfakes
**一句話定位**：跨影像/影片/音訊的反制手段全景 review，主張分層防禦。

將反制手段分為三大類：被動偵測（從內容痕跡推斷）、主動溯源（密碼學 manifest 綁定 metadata，含威脅模型分析）、浮水印（含 diffusion 時代浮水印與產業部署）。並分析對抗性強健性、資料集與 benchmark、評估指標、部署限制，以及法律、倫理與政策議題。

**關鍵發現**：
- 在真實對抗環境中**沒有任何單一反制手段是充分的**
- 最實際的做法是結合溯源 + 浮水印 + 內容偵測 + 人工監督的**分層防禦（layered defense）**
- 優先研究方向：泛化能力、互通性、可信的使用者體驗

---

## 文獻整體拼出的 Research Gap 地圖

1. **被動偵測的極限**（#1、#2、#3）：閉源生成器 → EER 崩跌至 13.5–50%；壓縮/通道 → 顯著劣化且對未知 codec 無解；現有補救策略（augmentation、multi-domain training）效果有限甚至有害。
2. **密碼學溯源的極限**（#4–#7）：只證 provenance 不證 authenticity；規格層攻擊可行（timestamp、revocation、exclusion range）；生態系 validator 彼此矛盾；長期可驗證性失效；只覆蓋「願意簽署」的內容。
3. **多訊號整合是未被充分探索的層次**（#7、#8）：provenance、watermark、passive detection 各自獨立運作時可被各個擊破或彼此矛盾；跨層一致性檢查與分層防禦是共同指向的方向，但 **audio 領域尚缺乏對應的系統性研究**。
