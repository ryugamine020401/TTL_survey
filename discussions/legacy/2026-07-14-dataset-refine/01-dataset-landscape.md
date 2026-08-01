# 01｜2024–2026 audio deepfake / anti-spoofing 資料集地景

角色：資料集與 benchmark 策展人（B）
日期：2026-07-15
用途：**這份文件是後續七位角色所有「換資料集」決策的共用事實依據。** 只盤點事實（年份、規模、來源、授權、取得難度），不改任何方向的 RQ、方法、實驗設計、算力預算。
上游依據：`00-constraints.md`（最高指導原則）、`final/D1–D5.md`（定稿）、`01-compute-budget.md`（算力硬預算）、`survey/README.md`。

> **範圍紀律（自我約束）**：本輪只做「舊資料集 → 更新、可取得替代品」。凡是「換上去要改方法論、要加 RQ、要加實驗軸」的資料集，一律不列為主力，只在紅線區誠實標明「看似新但拿不到 / 拉進來就爆範圍」。所有大型資料集都**沿用定稿的分層抽樣 20k 規則**，不因換資料集而放大規模。

---

## 〇、目前五方向在用的「舊」資料集（換前基準）

| 資料集 | 發布年 | 現用於 | 為何算「舊」 |
|---|---|---|---|
| ASVspoof 2019 LA | 2019 | D1（訓練）、D3 | 錄音棚 ~100 語者、生成器停在 2019 世代（HMM/早期 neural TTS/VC） |
| ASVspoof 2021 DF | 2021 | D1、D3（eval） | 2021 生成器；DF 全集 611k 是預算表唯一會炸掉設計的資料集 |
| In-the-Wild | 2022 | D1、D2、D3、D5（real 類） | 名人公開音檔，2022 前生成器；規模小（31,779 筆 / 37.9h） |
| MLAAD | 2023–（現用 v5） | D1、D3 | 現用版本落後，最新已到 v10 |
| 開源 TTS（XTTS-v2/VITS/YourTTS） | 2022–2023 | D2、D4（fake 生成） | 未涵蓋 2024–2025 的 diffusion/flow-matching 與 codec-based 世代 |
| AudioMarkBench | 2024 | D5（baseline） | 尚新，但未含 neural codec 通道專門評估 |
| RTCFake | 2026 | D2（真實通道錨） | 已是最新，保留（見下） |
| AISHELL-3 / LibriSpeech（載體 real） | 2019–2020 | D5 | 作為 watermark 載體語音，年份不影響，保留 |

**結論先講**：真正需要換的是 **unseen-generator 軸**（D1/D3 的 shift/laundering 對象）與 **fake 生成器世代**（D2/D4），因為攻擊者手上的工具 2024–2026 已翻代（diffusion/FM TTS、neural-codec TTS、閉源商用 API）。訓練用的 ASVspoof 2019 LA 是否要換是**次要且可選**（它定義「in-domain 種子分布」，換掉會改變 in-domain 的意義但不改方法）。

---

## 一、ASVspoof 5（2024 發布，anti-spoofing 領域的當代基準）

**名稱**：ASVspoof 5
**發布年**：2024（Interspeech ASVspoof Workshop 2024；期刊/完整版 2025-02，arXiv 2502.08857、Computer Speech & Language）
**規模**：建於 **MLS English**（crowdsourced，>4,000 語者，多種錄音裝置）。
- Train：18,797 bona fide + 163,560 spoof（400 語者）
- Dev：31,334 bona fide + 109,616 spoof
- Eval Track 1：138,688 bona fide + 542,086 spoof；Track 2（SASV）另計
- 合計 >150 萬 utterance，數百小時。
**涵蓋的生成器**：共 **32 種攻擊**（A01–A32）——legacy + contemporary TTS/VC，**史上第一次納入 adversarial attacks**（Malafide、Malacopula filter，且對 ASV 與 CM surrogate 雙重最佳化）。eval spoof 由 9 種 TTS/VC + 7 種 adversarial 組成。**不含閉源商用 API 生成器**（全部是研究界可復現的攻擊）。
**真實通道 / codec 條件**：**內建 12 種 codec 條件**，跨寬頻（16 kHz）與窄頻（8 kHz）：Opus、AMR、Speex、**EnCodec（neural codec）**、MP3、M4A 及混合 codec，bitrate 1.5–256 kbps。**這是 ASVspoof 系列第一次把 codec（含 neural codec）寫進官方評估。**
**語言**：英文（MLS English）。
**下載來源**：Zenodo `https://zenodo.org/records/14498691`（挑戰結束後全部免費釋出）。
**授權**：以 Zenodo 上 LICENSE.txt / README.txt 為準（研究用途，非申請制、可直接下載）。
**是否申請制**：否，直接下載。
**磁碟大小**：完整集約數百 GB（>150 萬檔）。→ **必須分層抽樣到 20k**（沿用 D1/D3 既有規則）。
**與 2019/2021 的關鍵差異**：(1) **crowdsourced 非錄音棚**——語者數從 ~100 躍升到數千、含多裝置多聲學條件；(2) **首次含 adversarial 攻擊**；(3) **首次把 codec（含 neural codec）納入官方條件**；(4) 攻擊同時針對偵測器 surrogate 最佳化。→ 對 D1/D3 而言，它同時能當**更新的訓練種子**與**更新的 unseen 對象**。

---

## 二、2024–2026 新的 audio deepfake 偵測資料集

### 2.1 Deepfake-Eval-2024（真正「2024 年在社群流通」的 in-the-wild 攻擊）
**發布年**：2025-03（arXiv 2503.02857；CVPR 2026 Workshop APAI）
**規模**：多模態；**音訊 56.5 小時**（另 44h 影片、1,975 圖）。來自 **88 個網站、52 種語言**。
**涵蓋的生成器**：**2024 年實際在社群媒體與偵測平台使用者間流通的 deepfake**——因此**隱含含最新閉源商用生成器**（未逐一標記生成器，因為是真實蒐集而非受控生成）。含 diffusion-based 合成、非人臉/選擇性操弄、低資源語言音訊。
**真實通道 / codec 條件**：**含真實世界擾動**（壓縮、re-encoding、靜音、環境噪聲）——天然帶通道劣化。
**語言**：52 種（含多語）。
**下載來源**：GitHub `https://github.com/nuriachandra/Deepfake-Eval-2024`（公開釋出）。
**授權**：見 repo；**注意**內容多為社群媒體 scrape，**再散布授權可能受限**（僅供 eval，勿當可自由散布的訓練集）。
**是否申請制**：否（但部分內容可能只給連結/受版權限制）。
**磁碟大小**：音訊部分約數 GB（56.5h）。
**時效性論證**：SOTA 偵測器在其上 **audio AUC 掉 48%**——它是目前唯一「攻擊分布 = 2024 年真實流通」的公開 eval 集，最能證明「舊 benchmark 的結論已過期」。**定位：純 eval-only 的 unseen 錨（不當訓練資料）。**

### 2.2 SpeechFake（2025，最大規模多語 + 含商用 API 世代）
**發布年**：2025-07（ACL 2025，arXiv 2507.21463）
**規模**：**>300 萬 fake 樣本、>3,000 小時**，由 **40 種生成工具**（30 開源 + **10 商用 API**）產生。分 Bilingual（EN+ZH）與 Multilingual（46 語）兩部。HuggingFace 版標 4.52M rows（train 2.34M / val 384k / test 1.8M）。
**涵蓋的生成器**：TTS + VC + neural vocoder，**含 10 家閉源商用 API 世代**（cutting-edge）。附豐富 metadata（生成法、voice id、語言、逐字稿）。
**真實通道 / codec 條件**：無專門通道條件（乾淨合成為主）。
**語言**：英文 + 中文（zh，偏 zh-CN）+ 46 語多語部。
**下載來源**：HuggingFace `DeepFense/SpeechFake`；下載腳本見 `github.com/YMLLG/SpeechFake`。
**授權**：開源部 **Apache 2.0**。**⚠️ 10 家商用 API 生成的子集因授權問題「不釋出」**——即最有價值的閉源商用世代**拿不到**（見紅線）。
**是否申請制**：開源部否。
**磁碟大小**：完整 >數 TB。→ **必須分層抽樣 20k**。
**時效性論證**：開源部就已涵蓋 2024–2025 世代 TTS/VC/vocoder，是 D1/D3 unseen-generator 軸最省事的「一站式」更新來源（zh 子集也順帶服務 D4 的對照）。

### 2.3 DFADD（2024，diffusion / flow-matching 世代——舊偵測器的盲區）
**發布年**：2024-09（arXiv 2409.08731，ICASSP 2025）
**規模**：5 種主流開源 Diffusion / Flow-matching TTS 生成的 spoof（對照 VCTK real）。
**涵蓋的生成器**：**專攻 diffusion + flow-matching TTS**（對標 Voicebox / Seed-TTS 這類 human-parity 系統）——這是 2019/2021 資料集完全沒有的生成範式。**開源生成器，非閉源商用。**
**真實通道 / codec 條件**：無（乾淨）。
**語言**：英文。
**下載來源**：HuggingFace（見 `github.com/isjwdu/DFADD`）；2025-04 已修正 Matcha-TTS 標籤並統一格式。
**授權**：開源（見 repo）。
**是否申請制**：否。
**磁碟大小**：中小型（數 GB）。
**時效性論證**：SOTA anti-spoofing 對 diffusion/FM 生成「明顯不夠 robust」——是 D1「unseen-generator shift」與 D3「laundering 對象」最精準的一格新負領土。

### 2.4 SpoofCeleb（2024，in-the-wild real + 23 TTS）
**發布年**：2024（arXiv 2409.xxxx）
**規模**：**>250 萬 utterance、1,251 語者**，source data 來自 **VoxCeleb1**（真實、in-the-wild 錄音條件），由在同一真實資料上訓練的 **23 種當代 TTS** 生成 spoof。
**涵蓋的生成器**：23 種當代 TTS（開源）。
**真實通道 / codec 條件**：source 本身即 in-the-wild（含真實錄音噪聲/通道），非受控棚錄。
**語言**：英文為主（VoxCeleb1 名人訪談）。
**下載來源**：專案頁 / HuggingFace（公開）。
**授權**：**衍生自 VoxCeleb1（Oxford VGG 研究授權，非商用）**——再散布受原授權約束，標為**備選**。
**是否申請制**：否，但受 VoxCeleb 條款約束。
**磁碟大小**：大（>250 萬檔）→ 抽樣。
**時效性論證**：對 D2「真實錄音條件的 bona fide + 同源 fake」是比 ASVspoof19 更貼近真實的 real/fake 配對來源。

### 2.5 CodecFake+（2025，neural-codec-based deepfake——D3/D5 的核心新資料）
**發布年**：2025-01（arXiv 2501.08238）
**規模**：截至 2025-02 為此領域**最大公開集**；涵蓋 **31 種開源 neural audio codec + 17 種 codec-based 語音生成系統**。
**涵蓋的生成器**：codec-based TTS/語音生成（EnCodec/DAC/SpeechTokenizer 這類 codec 當生成骨幹的世代）——**與 D3 RQ2「neural codec transcode 是不可逆必殺動作」、D5「neural codec 通道容量塌陷」直接同構**。
**真實通道 / codec 條件**：本質即 neural codec 條件。
**語言**：英文為主。
**下載來源**：HuggingFace `CodecFake/CodecFake_Plus_Dataset`；`github.com/ResponsibleGenAI/CodecFake-Plus-Dataset`（2025-10 已補 CoRS/CoSG 標籤）。
**授權**：見 repo（開源）。
**是否申請制**：否（多 .part 檔合併下載）。
**磁碟大小**：大 → 抽樣。
**時效性論證**：把「codec 世代生成器」從 D3/D5 的假想威脅變成可實測的 fake 來源——強化「neural codec 既是攻擊也是通道」的論證。

### 2.6 其他掃描到、但**不建議**納入的新集（避免範圍膨脹）
- **CtrSVDD**（2024，Zenodo，47.64h bonafide + 260.34h deepfake、14 法、164 歌手）：**歌唱語音**，與五個方向的「說話/詐騙語音」是不同 modality。→ 紅線（勿為了新而拉進來）。
- **P2V / Perturbed Public Voices**（2025，arXiv 2508.10949）、**A Data-Centric Approach**（2025-12，arXiv 2512.18210）：均為 robust ADD 資料/方法，與現有軸重疊，邊際效益低。
- **RADAR Challenge 2026**（arXiv 2605.09568）：挑戰賽資料，**可能時間窗/報名制**，不當主力。

---

## 三、繁中 / 中文 deepfake 語音資料集（2024–2026）

**核心事實（誠實講）：目前沒有公開的「繁體中文 / 台灣國語（zh-TW）」deepfake 語音資料集。** 中文可得的是 **zh-CN（大陸普通話）**。因此 **D4（繁中詐騙現場審計）自建語料的定位不變、依然正確**——本輪能更新的是「用 2025 世代的 zh-capable 開源 TTS 取代 2022–2023 的 VITS/YourTTS」，而非「找到現成 zh-TW 集」。

| 資料集 | 年 | 語言 | 內容 | 取得 | 對 D4 的用途 |
|---|---|---|---|---|---|
| **CFAD** | 2024（Speech Comm.；arXiv 2207.12308） | zh-CN 普通話 | 12 類 fake、含 noisy 條件 | 公開下載 | **對照/補充**（非 zh-TW，不能當主力，可作「中文 real 類 + 跨腔調對照」） |
| **SpeechFake（ZH 子集）** | 2025 | zh（偏 zh-CN） | Bilingual 部含中文 fake | HuggingFace，Apache 2.0（開源部） | D4 的 zh fake 對照臂（腔調非 zh-TW，需標明外部效度限制） |
| **FMFCC-A** | 2021 | zh-CN | Mandarin 合成語音偵測挑戰集 | 公開 | 舊，僅背景參考 |

**D4 建議**：**主力仍為自建**（Common Voice zh-TW + AISHELL real 類載體 + **2025 世代開源可控情緒 zh TTS**：如 CosyVoice 2、F5-TTS、GPT-SoVITS、OpenVoice v2 等）。SpeechFake ZH / CFAD 僅作「非 zh-TW 對照臂」以佐證落差非單一腔調 artifact。**這不改 D4 方法論，只換 fake 生成器世代。**

---

## 四、真實通道 / 電信 / 壓縮條件資料集

| 資料集 | 年 | 通道性質 | 規模 | 取得 | 授權 |
|---|---|---|---|---|---|
| **RTCFake** | 2026（arXiv 2604.23742，ACL 2026） | **真實 RTC 傳輸**（Zoom 等主流社群/會議平台，含 noise suppression、echo cancellation、codec、封包遺失），**offline/online 精確配對** | **~600 小時** | HuggingFace `JunXueTech/RTCFake`，**公開可下載** | 見 repo（未明標，須月 0 確認學術重散布條款） |
| **ADD-C**（survey #3） | 2025（arXiv 2504.12423，Loughborough） | **模擬** 6 codec（AMR-WB/EVS/IVAS/OPUS/Speex/SILK）× 5 PLR | 130,041 real / 240,373 fake，36 生成法 | 見論文/repo | 學術 |
| **AudioPerturber / 2503.17577**（real-world corruption） | 2025 | 18 種擾動工具（噪聲/壓縮/通道） | 工具框架 | 見論文 | 學術 |
| ASVspoof 5 內建 codec 條件 | 2024 | 官方 12 codec（含 neural） | 見第一節 | Zenodo | 見 LICENSE |

**關鍵更新**：**RTCFake（2026）是目前唯一「真實黑箱 RTC 通道 + offline/online 配對」的公開大集**，已確認**在 HuggingFace 公開可下載**（`JunXueTech/RTCFake`）——這比定稿 D2 把它當「單點故障、月 0 才知道能不能拿」的假設**更樂觀**：它是可下載的，D2 的最大風險因此下降。ADD-C 則是「模擬通道」的最新公開對照集，正好給 D2「模擬 vs 真實落差 γ」提供模擬側基準。

---

## 五、watermark / provenance benchmark 資料集

| 資料集 / 基準 | 年 | 內容 | 取得 | 對 D5/D2 的用途 |
|---|---|---|---|---|
| **AudioMarkBench** | 2024（NeurIPS 2024，arXiv 2406.06979） | 3 watermark（AudioSeal、Timbre/Wavmark、WavMark）× 15 擾動 × Common Voice（no-box/black-box/white-box） | GitHub 公開（載於 Common Voice，CC0） | D5 baseline / D2 watermark 對照（既有，保留） |
| **「Will They Survive Neural Codecs?」** | **2025（Interspeech 2025，arXiv 2505.19663）** | **watermark 演算法在 neural codec 下的真實世界存活評估** | 論文/repo | **D5 直接前作**——把 D5「neural codec 通道容量塌陷」錨到已發表基準，強化定位 |
| **Deep Audio Watermarks are Shallow** | 2025（ICLR 2025 Workshop，arXiv 2504.10782） | post-hoc 語音 watermark 的極限 | 論文 | D5 discussion 的極限論證 |
| **AudioSeal** | 2024（arXiv 2401.17264，官方 repo `facebookresearch/audioseal`） | 開源 localized watermark，SOTA robustness | 直接下載 | D2/D5 主力 watermark（保留） |

**關鍵更新**：D5 的 baseline 從「只有 AudioMarkBench（2024，只做模擬擾動）」升級為「AudioMarkBench + **Will They Survive Neural Codecs（2025，Interspeech）**」——後者**正是 D5 主題（watermark × neural codec）的最新前作**，讓 D5 的「第一張可靠 bit 容量地圖」定位更精準（相對前作補上「可控植入 ground-truth 錨 + 索引構造」）。**watermark 家族本身（AudioSeal/WavMark/SilentCipher）仍是當前開源可得的全部，無需更換。**

---

## 六、最新閉源商用 TTS（ElevenLabs / OpenAI 等）在哪些公開集裡有樣本

| 途徑 | 是否含閉源商用世代 | 可取得性 | 判定 |
|---|---|---|---|
| **Deepfake-Eval-2024** | 隱含含（2024 真實流通，未逐一標生成器） | GitHub 公開（eval-only，scrape 內容散布受限） | **唯一實務可得**的「含閉源商用世代」公開 eval 集 |
| **SpeechFake 商用子集** | 明確含 10 家商用 API | **不釋出（授權問題）** | ❌ 拿不到（紅線） |
| **Podonos / 商用 benchmark**（~25 TTS 含 ElevenLabs、F5-TTS、Chatterbox） | 含 | 商用平台，資料集是否公開釋出不明 | 備選/不明 |
| **ElevenLabs AI Speech Classifier / SynthID 偵測頁** | 是（自家生成 + SynthID 標記） | 僅線上偵測服務，**非資料集** | 不可當資料集 |
| 自建（呼叫 ElevenLabs/OpenAI API 生成） | 是 | **要錢**（US$300–600 / 2 萬筆）+ guardrail 風險，且 `01-compute-budget.md` R11 紅線 | ❌ 超預算，五方向定稿已全砍閉源自建臂 |

**結論**：**閉源商用 TTS 樣本在公開、可自由取得、可散布的資料集裡幾乎不存在**——唯一實務入口是 Deepfake-Eval-2024（eval-only）。這印證五方向定稿「不自建閉源臂」的決定是對的：真要碰閉源世代，就用 Deepfake-Eval-2024 當 eval 錨，而非自己花錢生成。

---

## 七、新舊對照建議表（五方向；每格附取得難度）

> 取得難度圖例：🟢 可直接下載（HuggingFace/Zenodo/GitHub，非申請制）｜🟡 可取得但有條款/衍生授權/scrape 限制（列備選或 eval-only）｜🔴 拿不到 / 超預算 / 換方法論（紅線，不採）

| 方向 | 現用舊資料集 | 建議新替代（年份） | 取得難度 | 為什麼更新更好（時效性一句話） | 算力相容備註 |
|---|---|---|---|---|---|
| **D1 選擇性預測基準** | ASVspoof 2021 DF + MLAAD v5（unseen-generator 軸） | **① MLAAD v10（2025，175 TTS/54 語）② DFADD（2024，diffusion/FM）③ SpeechFake 開源部（2025）④ Deepfake-Eval-2024（2025，eval-only in-the-wild）** | 🟢①②③ / 🟡④ | 讓「unseen shift」是 2024–2025 的 diffusion/FM 與真實流通世代，而非 2021 生成器；負領土地圖才反映 2026 攻擊者 | 全部分層抽 20k；Deepfake-Eval-2024 音訊僅 56.5h 可整段當 eval 格 |
| **D1（可選）訓練種子** | ASVspoof 2019 LA（in-domain 訓練） | **ASVspoof 5 train（2024，crowdsourced 非棚錄）** | 🟢 | in-domain 種子從 2019 錄音棚升到 2024 crowdsourced 多裝置，"seen" 分布本身更貼近現實 | 抽 20k 訓練子集；frozen XLS-R 方法不變 |
| **D2 通道存活審計** | 真實通道錨「RTCFake（月 0 才知能否取得）」 | **RTCFake（2026）——已確認 HuggingFace 公開可下載** | 🟢 | 不是「換新」而是「降風險」：定稿假設它是單點故障，事實上可直接下載，D2 最大風險解除 | ~600h → 抽樣池 20k |
| **D2 fake 生成器 + real 類** | ASVspoof19 real + XTTS/VITS/YourTTS fake | **real 類改 SpoofCeleb（2024，in-the-wild）備選；fake 補 CodecFake+/SpeechFake 開源世代** | 🟢CodecFake+/SpeechFake｜🟡SpoofCeleb（VoxCeleb 衍生授權） | 反制訊號要在 2024–2025 世代 fake 上測存活，才是 2026 的「反制訊號折扣係數」 | 抽樣；watermark 仍 AudioSeal 單一 |
| **D3 攻擊成本地圖** | ASVspoof 2019/2021 + In-the-Wild + MLAAD | **① CodecFake+（2025，neural-codec 世代）② DFADD（2024）③ SpeechFake 開源部（2025）；ASVspoof 5 取代 2019/2021 種子** | 🟢 | RQ2「neural codec 為不可逆必殺」對上 CodecFake+ 的 codec 世代 fake，laundering 對象是 2025 生成器 | 20k 確認池 / 10k 搜尋池不變 |
| **D4 繁中詐騙審計** | Common Voice zh-TW + AISHELL + VITS/YourTTS/OpenVoice fake | **fake 換 2025 世代 zh 開源 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）；對照臂補 SpeechFake ZH / CFAD** | 🟢自建｜🟡CFAD/SpeechFake（zh-CN 腔調，外部效度須標明） | 「到達耳朵的三秒」要用 2025 能產生哭腔/急迫的當代 zh TTS，才代表 2026 詐騙工具；**無 zh-TW 現成集，自建定位不變** | GPU ≈180 不變（全場最寬鬆） |
| **D5 watermark 位元容量** | AudioMarkBench（2024）baseline；AISHELL-3/LibriSpeech 載體 | **baseline 補「Will They Survive Neural Codecs?」（2025, Interspeech）；neural codec 世代可參 CodecFake+** | 🟢 | 把 D5 錨到 2025 最新的「watermark × neural codec」前作，容量塌陷點論證更硬 | watermark 家族不變；~10k 載體池不變（GPU≈220） |

**沒有任何一列需要改方法論、加 RQ 或加實驗軸——全部是「把餵進同一條管線的 fake/通道換成更新世代」，並沿用既有 20k 抽樣。**

---

## 八、紅線：看似新、其實拿不到 / 拉進來就爆範圍

| 標的 | 表面吸引力 | 真相 | 判定 |
|---|---|---|---|
| **SpeechFake 商用 API 子集** | 「含 10 家閉源商用世代」 | **因授權問題明確不釋出**，只給開源部 | 🔴 不可依賴其「閉源商用覆蓋」；只用開源部 |
| **閉源商用 TTS 自建（ElevenLabs/OpenAI）** | 「最貼近 2026 真實攻擊」 | 要錢（US$300–600/2 萬筆）+ guardrail 風險；`01-compute-budget.md` R11 紅線；五方向定稿已全砍 | 🔴 超預算，維持不自建 |
| **Deepfake-Eval-2024 當訓練集** | 「2024 真實流通、含商用」 | 內容多為社群 scrape，**再散布授權受限**；且只有 56.5h | 🟡 僅 eval-only 錨，勿當可散布訓練集 |
| **CtrSVDD** | 「2024 新、規模大」 | **歌唱語音，不同 modality** | 🔴 與五方向無關，勿為新而拉進 |
| **RADAR Challenge 2026 資料** | 「2026 最新挑戰」 | 挑戰賽資料，可能報名/時間窗限制 | 🟡 授權不明，不當主力 |
| **SpoofCeleb / VoxCeleb 衍生集** | 「250 萬筆 in-the-wild」 | 受 **VoxCeleb 非商用研究授權**約束，再散布受限 | 🟡 備選，須守原授權 |
| **ASVspoof 5 全集直接用** | 「當代基準」 | >150 萬檔、數百 GB，任何乘數 × 全集即燒光預算（budget 法則 3） | 🟢 但**強制抽樣 20k**，不可用全集 |
| **MLAAD v10 全集** | 「1002.9h、175 TTS」 | 全集過大 | 🟢 但抽樣 20k |
| **RTCFake 授權** | 「HuggingFace 公開」 | 檔案可下載，但**學術重散布條款未明標** | 🟢 可下載、🟡 散布條款須月 0 確認（D2 已排入 go/no-go） |

---

## 九、給七位角色的一頁結論

1. **最該換的是 unseen-generator 軸**（D1/D3）：把 2021 DF + MLAAD v5 換成 **DFADD（diffusion/FM）+ CodecFake+（neural codec）+ SpeechFake 開源部 + MLAAD v10**，並用 **Deepfake-Eval-2024** 當 eval-only 的真實流通錨。方法一行不改，只換抽樣池內容。
2. **RTCFake 是好消息不是風險**：它 2026、~600h、HuggingFace 公開可下載——D2 的「單點故障」在事實層已緩解，仍保留月 0 確認散布條款。
3. **ASVspoof 5** 是可選但強力的「訓練種子 + unseen 對象」雙用更新（crowdsourced + 內建 neural codec + adversarial），對 D1/D3 尤其契合；務必抽樣 20k。
4. **繁中（D4）沒有現成 zh-TW 集**——自建定位正確，只需把 fake 生成器升到 2025 世代 zh 開源 TTS；CFAD/SpeechFake ZH 僅作 zh-CN 對照臂。
5. **閉源商用世代拿不到可散布資料**——維持定稿「不自建閉源臂」，唯一入口是 Deepfake-Eval-2024（eval-only）。

---

## 附錄：查證來源（附年份）

- ASVspoof 5（2024/2025）— [arXiv 2408.08739](https://arxiv.org/html/2408.08739v1)、[期刊版 arXiv 2502.08857](https://arxiv.org/abs/2502.08857)、[Zenodo 14498691](https://zenodo.org/records/14498691)、[ISCA Archive](https://www.isca-archive.org/asvspoof_2024/wang24_asvspoof.html)
- SpoofCeleb（2024）— [ResearchGate PDF](https://www.researchgate.net/publication/387992135_SpoofCeleb_Speech_Deepfake_Detection_and_SASV_In_The_Wild)
- Deepfake-Eval-2024（2025）— [arXiv 2503.02857](https://arxiv.org/abs/2503.02857)、[GitHub](https://github.com/nuriachandra/Deepfake-Eval-2024)
- SpeechFake（ACL 2025）— [arXiv 2507.21463](https://arxiv.org/abs/2507.21463)、[HuggingFace DeepFense/SpeechFake](https://huggingface.co/datasets/DeepFense/SpeechFake)、[GitHub](https://github.com/YMLLG/SpeechFake)
- DFADD（2024/ICASSP 2025）— [arXiv 2409.08731](https://arxiv.org/abs/2409.08731)、[GitHub](https://github.com/isjwdu/DFADD)
- CtrSVDD（2024）— [arXiv 2406.02438](https://arxiv.org/abs/2406.02438)、[Zenodo test set 12703261](https://zenodo.org/records/12703261)
- MLAAD v7/v10（2025）— [arXiv 2401.09512](https://arxiv.org/abs/2401.09512)、[deepfake-total.com/mlaad](https://deepfake-total.com/mlaad)
- CFAD（Speech Communication 2024）— [arXiv 2207.12308](https://arxiv.org/abs/2207.12308)、[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0167639324000931)
- RTCFake（ACL 2026）— [arXiv 2604.23742](https://arxiv.org/abs/2604.23742)、[HuggingFace JunXueTech/RTCFake](https://huggingface.co/datasets/JunXueTech/RTCFake)
- CodecFake+（2025）— [arXiv 2501.08238](https://arxiv.org/html/2501.08238v2)、[HuggingFace CodecFake/CodecFake_Plus_Dataset](https://huggingface.co/datasets/CodecFake/CodecFake_Plus_Dataset)
- ADD-C / real-world communication（2025）— [arXiv 2504.12423](https://arxiv.org/abs/2504.12423)
- Real-world corruption / AudioPerturber（2025）— [arXiv 2503.17577](https://arxiv.org/html/2503.17577)
- AudioMarkBench（NeurIPS 2024）— [arXiv 2406.06979](https://arxiv.org/html/2406.06979v2)、[OpenReview](https://openreview.net/forum?id=t6LQXcFTEn)
- Will They Survive Neural Codecs?（Interspeech 2025）— [arXiv 2505.19663](https://arxiv.org/pdf/2505.19663)
- Deep Audio Watermarks are Shallow（ICLR 2025 WS）— [arXiv 2504.10782](https://arxiv.org/pdf/2504.10782)
- AudioSeal（2024）— [arXiv 2401.17264](https://arxiv.org/pdf/2401.17264)、[GitHub facebookresearch/audioseal](https://github.com/facebookresearch/audioseal)
- 閉源商用 benchmark（2025）— [Podonos deepfake audio benchmark](https://www.podonos.com/blog/deepfake-audio-benchmark)、[ElevenLabs SynthID](https://elevenlabs.io/blog/synthid)
- RADAR Challenge 2026 — [arXiv 2605.09568](https://arxiv.org/pdf/2605.09568)
</content>
</invoke>
