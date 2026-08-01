# Round 1 資料集提議：領域史官（Agent G）
日期：2026-07-14

> 角色定位：我不重寫方向，只做兩件事——(1) 用檢索**考證**每個被提議的新資料集「今天下得到嗎？授權允許學術用與重散布嗎？有沒有已知品質問題或撤回？」，避免全場換上一個實際拿不到的資料集；(2) 對我最有把握的方向把花俏題目正式化。所有大集一律沿用定稿的 **20k 分層抽樣**，不放大規模、不加 RQ、不加實驗軸。
>
> 本輪我實際查證了 5 個候選集的 HuggingFace / Zenodo / GitHub 頁面與授權（見文末「考證紀錄」）。**一個關鍵發現先講在前面：RTCFake 的 HF 頁面對匿名抓取回 HTTP 401，而同一時間 CodecFake+ 回 200——這是 RTCFake「被 gate（需登入 + 同意條款才下載）」的強訊號，直接牽動 D2 的月 0 go/no-go，landscape 說它「公開可直接下載」的樂觀需要一個 caveat（見 D2）。**

---

## 考證後的「一句話結論」（授權/取得層級）

| 候選新集 | 授權 | 取得 | 品質/撤回 | 我的判定 |
|---|---|---|---|---|
| **CodecFake+**（2025） | **MIT**（HF 頁面明載） | 🟢 非 gate，101 GB，多 .part 合併 | 2025-10 已補齊 CoRS/CoSG 標籤，無撤回 | **主力可用** |
| **DFADD**（2024） | **MIT**（repo）＋載體 VCTK CC-BY-4.0 / LJSpeech Public Domain | 🟢 HF `isjwdu/DFADD`，非 gate | **2025-04 errata**：修正 Matcha-TTS 音檔/標籤錯配並統一格式——**必須抓修正後版本** | **主力可用（用修正後版）** |
| **SpeechFake 開源部**（2025） | 開源部 Apache 2.0 | 🟢 HF `DeepFense/SpeechFake` | 10 家商用 API 子集**明確不釋出**（拿不到） | **開源部可用，別依賴其閉源覆蓋** |
| **ASVspoof 5**（2024） | LICENSE.txt（**非乾淨 CC tag，需讀條款**）；info@asvspoof.org 之申請是「用其 protocol 生成新 spoof」用，非下載本體 | 🟢 Zenodo 直接下載本體 | 無撤回 | **可用但列「備選（散布條款須讀 LICENSE.txt）」** |
| **RTCFake**（2026） | repo 未明標 | 🟡 **匿名抓取回 401 → 疑似 gated**，非「直接下載」 | 無撤回 | **維持為 D2 錨，但月 0 需先過 gate + 讀重散布條款** |

---

## D1｜分布偏移下語音深偽偵測的選擇性預測基準

**現用舊資料集**（§5.1）：ASVspoof 2019 LA（train + in-domain eval 格）、ASVspoof 2021 DF eval（unseen 格）、In-the-Wild（全集）、MLAAD v5（unseen-generator 廣度）。四個 source 軸 × 三個 channel 副本 = 12 格。

**建議替換**（維持「4 source × 3 channel = 12 格」結構不變，只換兩個 source 格的內容）：
- ASVspoof 2021 DF eval → **CodecFake+（2025, MIT）**：把「unseen 世代」從 2021 生成器升到 2025 neural-codec 世代 fake。
- MLAAD v5 → **DFADD（2024, MIT，用 2025-04 修正版）**：把「unseen-generator 廣度」升到 diffusion / flow-matching 範式——這是 2019/2021 資料完全沒有、SOTA 偵測器已知失效的一格新負領土。
- **維持**：ASVspoof 2019 LA（train + in-domain 對照格，frozen-only 設計，in-domain 種子語意不動）、In-the-Wild（真實流通 real/known 格）。
- **不採**（守紀律）：Deepfake-Eval-2024 雖是唯一「含閉源商用世代」的 eval 錨，但它會**多加一個 source 格 = 12 格→15 格**，屬擴充；只在 discussion 以文字提「未涵蓋閉源商用世代」，不進網格。ASVspoof 5 當訓練種子亦不採——2019 LA train 是 frozen-only 設計的既定 in-domain 語意，換掉屬「可選次要」且 ASVspoof 5 授權須讀 LICENSE.txt，邊際效益不值得動。

**通過五項驗收**
- 更新：CodecFake+ 2025、DFADD 2024，均比 2021 DF / MLAAD v5（2023）新且涵蓋原資料沒有的生成範式。
- 可取得：兩者皆 HuggingFace **非 gate、MIT 授權**（含重散布自由）；DFADD 載體 VCTK CC-BY-4.0 / LJSpeech Public Domain，重散布無虞；CodecFake+ 101 GB。
- 算力相容：兩者皆**分層抽 20k**，替換進原本的 source 格，前向次數與 12 格結構完全不變，GPU 帳（430–520h）一格不動。
- 契合原方法：只是把某一 source 格「裝進不同的 fake」，`s / g / R–C` 量測介面逐 bit 不變，零方法論改動。
- 時效性論證（一句話）：讓「unseen shift」對上的是 2024–2025 的 diffusion/FM 與 neural-codec 世代，負領土地圖才反映 2026 攻擊者真正手上的工具，而非 2021 生成器。

---

## D2｜真實通道上音訊深偽反制訊號的樂觀偏差審計

**現用舊資料集**（§實驗規劃）：bona fide 用公開 real 類、fake 用 3 家開源 TTS（XTTS-v2 / VITS / YourTTS，2022–2023 世代）；真實通道錨 **RTCFake**（定稿當「月 0 才知能否取得」的單點故障）；watermark 用 AudioSeal 單一。

**建議替換**
- fake 生成器：XTTS/VITS/YourTTS → **CodecFake+（2025, MIT）＋ SpeechFake 開源部（2025, Apache 2.0）** 的 2024–2025 世代 fake。反制訊號要在當代 fake 上測存活，才是 2026 的「反制訊號折扣係數」。
- 真實通道錨 RTCFake：**維持（無替代品——它是唯一「真實 RTC 傳輸 + offline/online 精確配對」的公開大集）**，但**下修 landscape 的樂觀**：我的考證顯示其 HF 頁面對匿名抓取回 **401（gated 強訊號）**，故它不是「直接下載」而是「需登入 + 同意 gate 條款」；**月 0 go/no-go 必須確認 (a) 能通過 gate、(b) 授權允許學術重散布（repo 未明標）**——定稿把它當單點故障是對的，landscape 的「已確認公開可下載」需要這個 caveat。
- real 類：**維持公開 real（In-the-Wild 等）**；SpoofCeleb（2024, in-the-wild）雖更貼近真實錄音，但**衍生自 VoxCeleb1（Oxford VGG 非商用研究授權），再散布受限 → 列 🟡 備選**，不當主力（守「可散布」紅線）。
- 模擬側對照：可（選擇性）以 **ADD-C（2025, 模擬 6 codec × 5 PLR）** 當模擬臂的公開基準，但這是既有 Opus/AMR-WB 模擬管線的替代，**不新增實驗軸**。

**通過五項驗收**
- 更新：fake 從 2022–2023 → 2024–2025 世代；通道錨保持 2026。
- 可取得：CodecFake+/SpeechFake 開源部 🟢 可散布；RTCFake 🟡（gated，須月 0 過關）；watermark 仍 AudioSeal 單一開源。
- 算力相容：fake 與通道皆**分層抽 20k**（不碰全集），~510 GPU-h 不變。
- 契合原方法：只換「灌進審計台的 fake / 通道樣本」，fixed-FPR 差分存活協定與探針（偵測器分數 / AudioSeal bit）不變。
- 時效性論證（一句話）：反制訊號的「模擬 vs 真實」樂觀偏差 γ，要在 2025 世代 fake 上量才代表 2026 的真實折扣，而 RTCFake 是唯一能提供 2026 真實 RTC 通道的錨。

---

## D3｜被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖

**現用舊資料集**（§五）：ASVspoof 2019 LA / 2021 DF（抽 20k 確認池 / 10k 搜尋池）、In-the-Wild、MLAAD（unseen-generator 軸）。laundering 工具鏈為 ffmpeg-native + HF neural codec（EnCodec/DAC）。

**建議替換**（這是最契合的一格——D3 的 RQ2 本來就在講 neural codec transcode 的不可逆）：
- unseen-generator 洗刷對象 ASVspoof 2021 DF + MLAAD → **CodecFake+（2025, MIT）＋ DFADD（2024, MIT）**。CodecFake+ 尤其同構：RQ2「neural codec transcode 是不可逆必殺動作」的宣稱，現在直接對上**用 codec 當生成骨幹的 2025 世代 fake**，而非 2021 生成器——把假想威脅變成可實測。
- **維持**：ASVspoof 2019 LA 作偵測器訓練種子（偵測器 checkpoint 語意不動）；In-the-Wild 作真實流通對照。
- **不採**：SpeechFake 開源部雖可補廣度，但 CodecFake+ + DFADD 已足以覆蓋「neural-codec + diffusion/FM」兩個 2025 關鍵範式；再加屬擴充搜尋池，違反「不因換資料順便擴充」。

**通過五項驗收**
- 更新：CodecFake+ 2025 / DFADD 2024，覆蓋 2021 DF / MLAAD 沒有的 codec-based 與 diffusion/FM 世代。
- 可取得：兩者 🟢 HF 非 gate、MIT、可重散布（DFADD 用修正後版）。
- 算力相容：沿用 **20k 確認池 / 10k 搜尋池**，greedy 搜尋前向數不變，610 GPU-h 一格不動。
- 契合原方法：laundering 動作空間、可控植入可逆性標註、greedy 搜尋協定全不變，只換「被洗刷的 fake 來源」。
- 時效性論證（一句話）：把「neural codec 為不可逆必殺」的物理下界，實測在 2025 真正用 codec 生成的 fake 上，攻擊成本地圖才對得上 2026 攻擊者的洗刷工具箱。

---

## D4｜詐騙現場條件下語音深偽偵測的評估效度審計（繁中）

**現用舊資料集**（§實驗規劃）：話術腳本自建（~165 條反詐公開話術改寫）；fake 用 2 家開源情緒可控 TTS/VC（現況偏 VITS/YourTTS/OpenVoice 世代）；載體 Common Voice zh-TW + AISHELL real。

**建議替換**
- **核心事實（考證確認）：目前沒有任何公開的 zh-TW（台灣國語）deepfake 語音集**，中文可得者僅 zh-CN。**D4 的自建定位完全正確、不動。**
- fake 生成器：2022–2023 世代 → **2025 世代 zh 開源可控情緒 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）**。「到達耳朵的三秒」要用能產生哭腔/急迫韻律的當代 zh TTS，才代表 2026 詐騙工具。
- 對照臂（非主力）：**CFAD（2024, zh-CN, 公開）／ SpeechFake ZH 子集（2025, Apache 2.0 開源部）** 作「非 zh-TW 對照臂」，佐證落差非單一腔調 artifact——但**須在文中明標腔調為 zh-CN、屬外部效度限制**。
- **考證誠實話**：上述 2025 世代 zh TTS 是生成工具而非現成資料集，其「情緒可控性 + zh-TW 適用性」我無法只靠 landscape 打包票；這正是 D4 定稿**月 0/月 1 硬 go/no-go 關卡**存在的理由——不可用即切 crash-path B 三軸析因。此關卡維持不動。

**通過五項驗收**
- 更新：fake 生成器 2022–2023 → 2025 世代；對照臂 CFAD/SpeechFake ZH 皆 2024–2025。
- 可取得：自建語料本就自足；CFAD 🟢 公開、SpeechFake ZH 🟢 Apache 2.0 開源部；2025 zh TTS 多為 GitHub/HF 開源（月 0 feasibility 確認可控性）。
- 算力相容：GPU ≈180 不變（全場最寬鬆），對照臂僅 eval 抽樣，不放大。
- 契合原方法：只換 fake 生成器世代與加一個 zh-CN 對照臂，fixed-FPR recall × 析因 × 品質配對三讀法全不變。
- 時效性論證（一句話）：詐騙者 2026 用的是 2025 世代能產生哭腔/急迫命令的 zh TTS，用它生成的現場素材才讓「評估效度落差」對得上真實攻擊。

---

## D5｜詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

**現用舊資料集**（§實驗規劃）：載體語音抽 ~10k 池（AISHELL-3 + LibriSpeech + ASVspoof19/In-the-Wild real）；watermark AudioSeal + WavMark + SilentCipher；通道傳統 codec + neural codec（EnCodec/DAC/SpeechTokenizer）；baseline AudioMarkBench（2024）。

**建議替換：大體維持，只補一個 2025 前作錨——這是「誠實說維持」的方向。**
- **維持載體語音（AISHELL-3 / LibriSpeech / real 類）**：它們只是 watermark 的**載體**，其發布年份不影響 watermark×codec 的量測結論；換新載體無科學收益，屬為換而換。
- **維持 watermark 家族（AudioSeal / WavMark / SilentCipher）**：這是當前開源可得的**全部**，無更新替代品。
- **維持 neural codec 通道（EnCodec/DAC/SpeechTokenizer）**：仍是當代主流開源 neural codec。
- **唯一更新（非資料集，是 baseline 前作錨）**：baseline 從「只有 AudioMarkBench（2024, 只做模擬擾動）」補上 **《Will They Survive Neural Codecs?》（Interspeech 2025, arXiv 2505.19663）**——它正是 D5 主題（watermark × neural codec）的最新前作，讓 D5「第一張可靠 bit 容量地圖」的定位相對前作更精準（補上可控植入 ground-truth 錨 + 索引構造）。
- **（可選）**：若要展示 neural-codec 世代 fake 的通道行為，可參照 **CodecFake+（2025, MIT）** 作 neural codec 條件的旁證，但**不進主 pipeline**（避免擴充）。

**通過五項驗收**
- 更新：baseline 前作補到 2025（Interspeech）；資料本體無需更新（載體年份中性）。
- 可取得：watermark 三家皆開源可下載；前作為公開論文/repo；CodecFake+ 🟢 MIT。
- 算力相容：~10k 載體池、~220 GPU-h 完全不變。
- 契合原方法：embed→通道→recover→可控植入校準 pipeline 一行不改，補的是引用與定位。
- 時效性論證（一句話）：把 D5 錨到 2025 最新的 watermark×neural-codec 前作，容量塌陷點的論證從「無前作」升為「相對已發表基準的精進」，定位更貼近 2026。

---

## 正式題目提議（僅對我最有把握、且已完整讀過定稿的 D1、D3）

> 正式化原則（沿指導原則）：去掉破折號金句、去掉問句、去掉口語，保留專有名詞英文，符合學位論文慣例。

**D1**
- 中：《面向未見生成器與通道之語音深偽偵測選擇性預測可靠性基準研究》
- 英：*A Shift-Aware Selective-Prediction Reliability Benchmark for Audio Deepfake Detection under Unseen Generators and Channels*

**D3**
- 中：《被動語音深偽偵測之適應性洗刷攻擊成本上界評估》
- 英：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

---

## 考證紀錄（本輪實際查證的來源）

- **CodecFake+**（2025, MIT, 101 GB, 非 gate, 31 codecs + 17 CoSG）— [HF CodecFake/CodecFake_Plus_Dataset](https://huggingface.co/datasets/CodecFake/CodecFake_Plus_Dataset)（頁面明載 license: mit，匿名抓取回 200）、[arXiv 2501.08238](https://arxiv.org/abs/2501.08238)、[專案頁](https://responsiblegenai.github.io/CodecFake-Plus-Dataset/)
- **DFADD**（2024, MIT, 載體 VCTK CC-BY-4.0 / LJSpeech Public Domain；2025-04 修正 Matcha-TTS 標籤錯配）— [GitHub isjwdu/DFADD](https://github.com/isjwdu/DFADD)、[HF isjwdu/DFADD]、[arXiv 2409.08731](https://arxiv.org/abs/2409.08731)
- **SpeechFake**（ACL 2025；開源部 Apache 2.0；10 家商用 API 子集不釋出）— [HF DeepFense/SpeechFake](https://huggingface.co/datasets/DeepFense/SpeechFake)、[ACL Anthology 2025.acl-long.493](https://aclanthology.org/2025.acl-long.493/)、[arXiv 2507.21463](https://arxiv.org/abs/2507.21463)
- **ASVspoof 5**（2024；Zenodo 直接下載本體，授權見 LICENSE.txt，非乾淨 CC tag；申請信 info@asvspoof.org 是為用其 protocol 生成新 spoof）— [Zenodo 14498691](https://zenodo.org/records/14498691)、[HF jungjee/asvspoof5 README](https://huggingface.co/datasets/jungjee/asvspoof5/blob/main/README.md)、[arXiv 2502.08857](https://arxiv.org/abs/2502.08857)
- **RTCFake**（2026；**匿名抓取回 HTTP 401 → 疑似 gated**，repo 未明標重散布授權）— [HF JunXueTech/RTCFake](https://huggingface.co/datasets/JunXueTech/RTCFake)、[arXiv 2604.23742](https://arxiv.org/html/2604.23742v1)
</content>
</invoke>
