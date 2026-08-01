# Round 1 資料集提議：訊號與通道（Agent C）
日期：2026-07-14

> 角色視角：我只從兩個問題看每一次換血——(1)**這批新資料有沒有把「真實傳輸／通道條件」帶進來**（這正是 2019–2021 舊集最缺的一塊）；(2)**換上去之後 CPU 前處理（codec 轉檔、resample、tandem 鏈）會不會爆日曆／磁碟**。凡是「新但需要我改通道方法論」或「新但把 CPU 前處理推上懸崖」的，我一律不當主力。
>
> 紀律聲明：本輪只換餵進管線的 fake／通道資料、只正式化題目。三個 RQ、核心方法、通道軸的建法與量測介面全部維持定稿不動。所有大型新集沿用既有 20k 分層抽樣。

---

## 通則（先講一次，避免每個方向重覆）

**訊號視角的兩條鐵律，決定我對每個換血案的態度：**

1. **「自建、受控的通道軸」不能被「資料集內建的通道條件」取代。** D1 的 `C_celp`/`C_neural`、D2 的模擬 codec 階梯、D5 的通道矩陣、D3 的 laundering 動作空間，都是**我方逐因子可控的自變數**。ASVspoof 5 內建 12 種 codec、Deepfake-Eval-2024 內建真實壓縮劣化——這些是**綁在 fake 上、無法逐因子拆解**的既成條件。所以新資料集只換「餵進通道的 fake 內容」，**通道軸本身仍由我方自建**。這不是保守，是方法要求：D2-RQ3 的逐因子落差分解、D5-RQ1 的可逆/不可逆塌陷點，都需要通道是我能一格一格開關的東西。

2. **CPU 前處理成本不在 GPU 預算表裡，卻是真正的日曆殺手（budget 4.1）。** 換 fake 資料集幾乎不動 CPU 成本（都是 20k 抽樣池、同一套 codec 過一次）；真正會爆 CPU 的是**通道條件數 × 全集**與**EVS 3GPP 參考碼（5–20× realtime，比 ffmpeg 慢 10 倍）**。我在下面每個方向都會標一句「這次換血的 CPU 帳」。

**一句總結：換 fake 資料集我幾乎全部支持（讓 laundering／存活量測的對象升到 2025 世代）；換通道我極度保守（自建受控軸不動，真實通道只認一個已下載的錨 RTCFake）。**

---

## D1｜分布偏移下的選擇性預測基準

### 現用舊資料集
- 訓練種子：ASVspoof 2019 LA train+dev（2019，錄音棚 ~100 語者）
- in-domain 對照格：2019 LA eval 抽 20k
- unseen-generator 軸：**ASVspoof 2021 DF 抽 20k**、**MLAAD v5 抽 20k**
- In-the-Wild 全集（real 類 / 名人音檔）
- 通道軸（自建）：`C_clean` / `C_celp`（AMR-WB+PLR，CPU，0 GPU-h）/ `C_neural`（EnCodec，只在抽樣池）
- 可選 stretch：`C_rtc`（RTCFake）

### 建議替換
| 對象 | 舊 → 新 | 我的角色理由 |
|---|---|---|
| unseen-generator 軸 | 2021 DF + MLAAD v5 → **DFADD（2024, diffusion/FM）+ CodecFake+（2025, neural codec）+ SpeechFake 開源部（2025）** | 三格新負領土各補一種**舊集沒有的生成範式**；其中 **CodecFake+ 與 D1 的 `C_neural` 通道軸同構**——「neural codec 世代的 fake」正好落在「neural codec 通道」上，channel-shift 與 generator-shift 兩軸在此交會，是我最想看的一格 |
| 訓練種子（可選） | 2019 LA → **ASVspoof 5 train 抽 20k（2024, crowdsourced 非棚錄、內建 codec 條件）** | in-domain「seen」分布本身就帶多裝置／多聲學／codec 變異，**訓練種子的通道多樣性升級** = 偵測器的「已見通道」更貼近現實 |
| 通道軸 | **維持自建 `C_clean`/`C_celp`/`C_neural`**（不動） | 見通則鐵律 1：選擇性預測的 shift 網格需要通道是逐格可控的自變數，不能改用資料集內建 codec |
| 真實通道 stretch | `C_rtc`（RTCFake）**維持為可選 stretch，不升為必做** | 訊號上它是唯一真實 RTC 格，但升為必做會擴充網格＝違反本輪禁止；保留 optional 即可 |

### 通過五項驗收
- **更新**：DFADD 2024、CodecFake+ 2025-01、SpeechFake 2025-07、ASVspoof 5 2024——全數 ≥2024，取代 2021/2023 世代。
- **可取得**：DFADD（HuggingFace，開源，數 GB）／CodecFake+（HuggingFace `CodecFake/CodecFake_Plus_Dataset`，開源，大→抽樣）／SpeechFake 開源部（HuggingFace `DeepFense/SpeechFake`，Apache 2.0，>TB→抽樣）／ASVspoof 5（Zenodo 14498691，研究用途非申請制，數百 GB→抽樣）。全部 🟢 直接下載。
- **算力相容**：全部沿用**分層抽 20k**；unseen 三格各 20k、in-domain 種子 20k，評估池規模與定稿的 ~9.2 萬持平。**CPU 帳**：新 fake 都是乾淨合成，過 `C_celp`（CPU、20k、數分鐘）與 `C_neural`（EnCodec、僅抽樣池、GPU 10–16h）成本與原設計相同，**不爆 CPU、不爆磁碟**（<100 GB 不變）。
- **契合原方法**：換的是「餵進 shift 網格的 fake 池內容」，棄權分數 × 網格 × risk–coverage 三物件、frozen 前向、pooled 快取一律不動。零方法改動。
- **時效性論證**：讓「unseen shift」是 2024–2025 的 diffusion/FM 與 neural-codec 世代，負領土地圖才反映 2026 攻擊者手上的工具，而非 2021 的 HMM/早期 neural。

---

## D2｜真實通道上反制訊號存活的樂觀偏差審計（**我的核心方向**）

### 現用舊資料集
- bona fide real：ASVspoof 2019 LA real / In-the-Wild real / MLAAD real
- **fake：3 家開源 TTS/VC —— XTTS-v2、VITS、YourTTS（2022–2023 世代）**
- 真實通道錨：**RTCFake**（定稿當「月 0 才知能否取得的單點故障」）
- watermark：AudioSeal（單一）
- 模擬臂：Opus + AMR-WB（現成 library，CPU 為主）

### 建議替換
| 對象 | 舊 → 新 | 我的角色理由 |
|---|---|---|
| fake 生成器 | XTTS-v2/VITS/YourTTS → **CodecFake+（2025）+ SpeechFake 開源部（2025）為主，DFADD（2024）補 diffusion/FM 格** | 這是本方向的靈魂：**「反制訊號折扣係數 γ」必須量在 2025 世代 fake 上才是 2026 的折扣**。尤其 CodecFake+ 的 fake 本身即 neural-codec 產物——當它再過真實 RTC 通道，是「codec 世代訊號 × 真實通道」，正是我最想量的存活場景 |
| 真實通道錨 | RTCFake「單點故障」→ **RTCFake（2026, ~600h, HuggingFace `JunXueTech/RTCFake` 已確認公開可下載）：解除風險，非換新** | 訊號上這是全景唯一「真實黑箱 RTC 通道 + offline/online 精確配對」的公開大集；landscape 已證實可下載，D2 最大單點故障事實層下降（仍保留月 0 確認學術重散布條款） |
| real 類（可選） | ASVspoof19 real → **SpoofCeleb（2024, in-the-wild real）為備選** | in-the-wild 錄音條件的 bona fide 更貼近真實；但受 VoxCeleb 非商用衍生授權約束，**標 🟡 備選**，不當主力 |
| 模擬臂 | **維持 Opus + AMR-WB 自建受控階梯**；ADD-C（2025）僅列 🟡 備選外部對照 | 見通則鐵律 1：RQ3 逐因子落差分解需要模擬側是我能逐項加回丟包/jitter/DSP 的受控管線；ADD-C 的固定條件無法逐因子拆，**只能當外部 sanity 對照，不可升為實驗軸**（升了就違反本輪禁止） |
| watermark | **維持 AudioSeal 單一**（唯一第三方可用 learned watermark） | 不動 |

### 通過五項驗收
- **更新**：fake 從 2022–2023 → CodecFake+/SpeechFake 2025、DFADD 2024；真實通道錨 RTCFake 2026。
- **可取得**：CodecFake+/SpeechFake 開源部/DFADD 皆 🟢 HuggingFace 直接下載；RTCFake 🟢 可下載、🟡 散布條款月 0 確認；SpoofCeleb 🟡 備選（VoxCeleb 授權）。
- **算力相容**：fake 沿用**抽樣 20k real/fake 池**；RTCFake ~600h → 抽樣 20k。**CPU 帳（我最在意的一筆，結論是好消息）**：
  - 換用 CodecFake+/SpeechFake 這類**預先生成**的 fake，可**免掉原設計 35 GPU-h 的 TTS 生成**（改為下載＋抽樣），對日曆是淨賺（此為前處理型態改變，不改 RQ、不改預算上限）。
  - **RTCFake 的真實通道劣化是「已烘進音檔」的**——我拿到的就是過完 Zoom noise-suppression/echo-cancellation/codec/丟包的波形，**不需要我自己建 rig、也不需要 CPU 重跑 codec 轉檔**。相對「自己模擬真實通道」，RTCFake 反而是 CPU 前處理的減法。模擬臂仍是 Opus+AMR-WB（CPU、20k、~10 GPU-h 等值、budget 已列），**不碰 EVS**（避開 5–20× realtime 的 CPU 懸崖）。
  - 結論：**這次換血讓 D2 的 CPU 前處理不升反降**，總帳仍 ≈510 GPU-h。
- **契合原方法**：審計台三 RQ（被動探針／AudioSeal bit／逐因子歸因）的通道管線、差分存活協定、fixed-FPR 記帳一律不動。只換探針灌進去的 fake 內容 + 確認真實通道錨可下載。零方法改動。
- **時效性論證**：γ 折扣係數若量在 2022 世代 fake × 模擬通道，只是歷史數字；量在 2025 世代 fake × 真實 RTC 通道，才是別的 ADD 研究能直接消費的「2026 通道折扣」。

### 正式題目提議（我最有把握——這是我的核心通道方向）
- **中**：《離線模擬與真實通訊通道之落差：音訊深偽反制訊號存活的樂觀偏差量測與畸變層歸因》
- **英**：*The Gap Between Offline Simulation and Real Communication Channels: Measuring the Optimism Bias in Audio Deepfake Countermeasure-Signal Survival and Attributing Its Distortion Layers*

（去除「模擬騙了我們多少」的問句金句；保留「樂觀偏差 / 畸變層歸因」兩個承重術語。）

---

## D3｜adaptive-laundering 攻擊成本上界地圖

### 現用舊資料集
- ASVspoof 2019 LA / 2021 DF（抽 20k 確認池、10k 搜尋池）
- In-the-Wild、MLAAD（unseen-generator 軸抽樣）
- laundering 動作空間（工具鏈，非資料集）：EnCodec/DAC + Opus/AMR-NB/μ-law/MP3/AAC + resample/time-stretch

### 建議替換
| 對象 | 舊 → 新 | 我的角色理由 |
|---|---|---|
| laundering 對象 / unseen 軸 | 2021 DF + MLAAD → **CodecFake+（2025, neural-codec 世代）為首選 + DFADD（2024）補格；種子 2019/2021 → ASVspoof 5（2024, 內建 codec + adversarial）** | 這是我認為換血收益最大的一格：**D3-RQ2 的整條承重論證是「neural codec transcode 是零金錢、一行指令、物理不可逆的必殺動作」**。用 CodecFake+（31 開源 neural codec + 17 codec-based 生成系統）當 laundering 對象，等於讓「必殺動作」打在「本身就是 codec 產物的 2025 fake」上——**codec-on-codec 的 many-to-one 疊加，把不可逆性論證從假想威脅升成可實測** |
| laundering 動作空間 | **維持 EnCodec/DAC + ffmpeg 原生 codec**（不動；這是動作空間不是資料集） | 見通則鐵律 1 |

### 通過五項驗收
- **更新**：CodecFake+ 2025-01、DFADD 2024、ASVspoof 5 2024，取代 2019/2021/2023。
- **可取得**：全部 🟢——CodecFake+（HuggingFace，開源）、DFADD（HuggingFace）、ASVspoof 5（Zenodo）。
- **算力相容**：沿用 **20k 確認池 / 10k 搜尋池**不變。**CPU 帳**：換 fake 資料集**不動動作空間、不動搜尋深度**（greedy depth≤3、動作 ≤8），tandem 轉檔仍是「唯一前綴鏈一次、跨 4 偵測器共用」——neural codec 走 GPU（budget 90 GPU-h，prefix cache），傳統 codec 走 CPU（便宜）。**CodecFake+ 的 fake 已是 codec 產物，過我方 laundering 動作是 codec-on-codec，但這只是波形再過一次同樣的動作空間，前處理成本與原設計同級，不爆 CPU。** 總帳 610 GPU-h 不變。
- **契合原方法**：recipe-level greedy 搜尋、成本代理三軸序數、可控植入可逆性標註一律不動。零方法改動。
- **時效性論證**：laundering 的攻擊對象若停在 2021，量到的「最便宜打穿配方」是打舊偵測器；換成 2025 neural-codec 世代 fake，攻擊成本上界與不可逆下界才對得上 2026 攻擊者的真實工具鏈。

---

## D4｜繁中詐騙現場條件的評估效度審計

### 現用舊資料集
- 話術腳本：~165 條反詐公開話術（自建，不動）
- bona fide：Common Voice zh-TW + AISHELL + 公開廣播 + ASVspoof/In-the-Wild real
- **fake：2 家開源情緒可控 TTS/VC（情緒可控 VITS 系 / OpenVoice 類，2022–2023）**
- **通道：offline codec 自建——傳統可逆 AMR-WB/EVS/Opus（CPU）+ 神經不可逆 EnCodec/DAC（GPU）**
- 品質協變量：UTMOS + ECAPA speaker similarity

### 建議替換
| 對象 | 舊 → 新 | 我的角色理由 |
|---|---|---|
| fake 生成器 | 情緒 VITS/OpenVoice → **2025 世代 zh 開源 TTS：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2** | 「到達耳朵的三秒」要用 2025 能穩定產哭腔／急迫韻律的當代 zh TTS，才代表 2026 詐騙工具；**無現成 zh-TW 集，自建定位不變** |
| zh 對照臂 | （新增備選） **SpeechFake ZH 子集 / CFAD（zh-CN）** | 佐證落差非單一腔調 artifact；🟡 zh-CN 腔調，須標外部效度限制，只當對照 |
| **通道：EVS** | **建議自傳統 codec 集移除 EVS，保留 AMR-WB/AMR-NB + Opus** | **這是我這關唯一的訊號主張**：(1)**訊號論證**——台灣詐騙現場的真實電話通道以 **VoLTE/GSM 的 AMR-WB/AMR-NB 與 VoIP/LINE 的 Opus** 為主導，EVS 在台灣市佔與可及性都非主軸；(2)**CPU 論證**——EVS 3GPP 參考 C 實作是 **5–20× realtime，比 ffmpeg 慢 10 倍（budget 4.1 明列的最常被低估項）**，對「詐騙現場 3s/5s 短句 × ~35k 檔 × 多情緒多句長」的分層網格，EVS 會把 CPU 牆鐘吃掉一大塊。D2/D3/D5 都已把 EVS 排除預設，D4 一致化即可。**這是移除一個通道條件（縮範圍）＋省 CPU，不是加東西** |
| 神經通道 | **維持 EnCodec/DAC**（不動） | 不可逆側需要它 |

### 通過五項驗收
- **更新**：fake 從 2022–2023 → 2025 世代 zh TTS；zh 對照臂 SpeechFake 2025 / CFAD 2024。
- **可取得**：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 皆 🟢 開源 checkpoint；SpeechFake ZH（HuggingFace, Apache 2.0）／CFAD（公開）🟡 zh-CN 備選。
- **算力相容**：自建 ~2–3 萬筆不變（GPU ≈180，全場最寬鬆）。**CPU 帳**：移除 EVS 後，傳統 codec 全走 ffmpeg 原生（AMR-WB/AMR-NB/Opus，50–200× realtime），~35k 短檔並行 batch 的 CPU 牆鐘明顯下降；神經 codec 仍走 GPU（3 種，已列）。**這次換血是 CPU 的淨減法。**
- **契合原方法**：一份語料 × frozen 前向 × fixed-FPR recall 讀三次不動；換 fake 生成器世代 + 移一個通道條件，不改析因/配對方法論。
- **時效性論證**：2025 世代 zh TTS 的情緒擬真度遠高於 2022 VITS，量出的「現場素材樂觀偏差」才是 2026 受害者實際會遇到的；台灣主導通道（AMR/Opus）比 EVS 更是「真正到達耳朵」的那條路。

---

## D5｜通訊通道對 watermark provenance 標記的可靠位元容量審計（**我的第二核心方向**）

### 現用舊資料集
- 載體語音：AISHELL-3 + LibriSpeech + ASVspoof19/In-the-Wild real（分層抽 ~10k 池）
- watermark：AudioSeal + WavMark + SilentCipher（開源）
- **baseline：AudioMarkBench（2024，只做模擬擾動）+ Özer et al. Interspeech 2025**
- 通道矩陣：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC × PLR）+ neural codec（EnCodec/DAC/SpeechTokenizer × bitrate）

### 建議替換
| 對象 | 舊 → 新 | 我的角色理由 |
|---|---|---|
| baseline / 前作定位 | AudioMarkBench 單錨 → **補「Will They Survive Neural Codecs?」（Interspeech 2025, arXiv 2505.19663）為 watermark×neural-codec 最新直接前作** | 這是我這關最強的一筆：D5 的整個承重貢獻是「watermark × neural codec 的可靠 bit 容量地圖」，而這篇 2025 Interspeech 前作**正是同主題最新前作**；把它明列為 baseline，D5「補上可控植入 ground-truth 錨 + 索引構造」的增量定位才精準、才不會被說重造輪子 |
| 載體語音 | **維持 AISHELL-3 + LibriSpeech + ASVspoof19/In-the-Wild real** | 誠實說維持：載體只是承載 watermark 的乾淨語音，**年份不影響 bit 容量量測**（landscape 同此判斷）。為換而換無意義 |
| watermark 家族 | **維持 AudioSeal + WavMark + SilentCipher** | 這已是當前開源可得的全部 learned watermark；SynthID 非全開源不納入。無可換 |
| 通道矩陣 | **維持**（傳統可逆 × neural 不可逆、neural 只掃 bitrate 不掃 PLR） | 這本來就是我這個角色會設計的矩陣：可逆/不可逆二分 + neural 通道的物理界線（PLR 對 neural codec 無意義）已正確。不動 |

### 通過五項驗收
- **更新**：baseline 從 2024 單錨升為 2024+2025（Interspeech）雙錨；資料集本體無需換（載體與通道矩陣已是當前最佳）。
- **可取得**：「Will They Survive Neural Codecs?」論文/repo 公開（arXiv 2505.19663）；載體語料與 watermark checkpoint 皆 🟢 已下載。
- **算力相容**：~10k 載體池、通道矩陣、~220 GPU-h **完全不變**。**CPU 帳**：傳統 codec 全 ffmpeg CPU（AMR-WB/Opus/SILK/MP3/AAC × 4 PLR）、**已排除 EVS**，neural codec 32 GPU-h 在 10k 池。此換血只增一個文獻對照，**CPU 前處理零變動**。
- **契合原方法**：唯一一條 embed→通道→recover→可控植入校準 pipeline 不動；只是把量出的曲線對齊一篇更新的前作。零方法改動。
- **時效性論證**：把 D5 錨到 2025 最新的「watermark × neural codec 存活」前作，容量塌陷點的論證站在當代基準之上，而非只對 2024 的模擬擾動 baseline 喊話。

### 正式題目提議（我第二有把握——watermark×通道是我的域）
- **中**：《通訊通道上音訊浮水印溯源標記的可靠位元容量審計：兼論歐盟 AI 法第 50 條之機器可讀性判定》
- **英**：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance Marks over Communication Channels, with a Machine-Readability Determination for EU AI Act Article 50*

（去除「還剩幾個 bit」的口語金句與破折號；保留「可靠位元容量 / 通訊通道 / Article 50 可讀性」三個承重詞。）

---

## 附：我這關的自我紅線檢查

- 是否加了實驗／RQ／deliverable？**否。** 換的全是餵進管線的 fake／前作對照；通道軸與量測介面一格未動。
- D4 移除 EVS 是否算「動實驗」？**否——那是移除一個通道條件（縮範圍）＋ CPU 減法，且與 D2/D3/D5 的既有 EVS 排除一致化。**
- D2 的 ADD-C 是否被我升為新軸？**否——明列 🟡 備選外部對照，禁止升為實驗軸。**
- 是否超算力？**否。** 全部沿用 20k / 10k 抽樣；D2、D4 的 CPU 前處理不升反降。
</content>
</invoke>
