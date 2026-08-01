# 算力預算表：單張 RTX 4090（24GB）上的 ADD 實驗成本

日期：2026-07-14
用途：**本文件是五個削減者的硬預算表。** 任何實驗設計都必須用第 5 節的公式當場算出 GPU-hour，總和不得超過 1,200–1,500。
角色：ML 系統工程師（不參與題目選擇，只提供事實基礎）

## 標記約定

- 【查】= 已查證（文獻／官方數據／公開 benchmark，附出處）
- 【推】= 由【查】的數字＋硬體規格推算（附推算過程）
- 【估】= 工程經驗估計，未經實測，**誤差可能 ±50%**

**所有數字都假設「已經 debug 完、程式跑得動」。** 硬約束中的 1,200–1,500 GPU-hour 已經扣掉除錯與重跑，所以本表的數字直接對應**規劃內的實驗**。但我仍建議在規劃內再留 15% 緩衝（見第 8 節）。

---

## 0. TL;DR — 一頁結帳單

| 項目 | 單價 | 說明 |
|---|---|---|
| **1 次標準訓練**（XLS-R 300M + backend，ASVspoof19 LA 規模，full fine-tune） | **6–10 GPU-h** | 本文件的計價基準單位 |
| 1 次輕量訓練（AASIST / RawNet2 從頭，19LA） | 2–4 GPU-h | |
| 1 次 frozen-feature 訓練（特徵已快取） | 0.3–1 GPU-h | 便宜 10–20× |
| **1 格評估**（1 模型 × 1 條件 × 10 萬筆抽樣池，單次前向） | **0.4–0.8 GPU-h** | 7 種 post-hoc 棄權機制**共用同一次前向** |
| 1 格評估（同上，但 ASVspoof21 DF **全集** 611k） | **2.5–5 GPU-h** | ← 全集 vs 抽樣差 **25–30×** |
| Neural codec transcode 10 萬筆 | 4–8 GPU-h | ← 最常被低估 |
| Neural codec transcode ASVspoof21 DF 全集 | **25–40 GPU-h** | 單一 codec、單一 bitrate |

**一年預算 1,200–1,500 GPU-hour 買得到：**
- **約 45–55 次標準訓練**（≈ 350 GPU-h）
- **約 600–800 格評估**（≈ 300 GPU-h）
- **約 200 GPU-h 對抗評估**
- **約 150 GPU-h 資料前處理／codec transcode／特徵抽取**
- **約 200 GPU-h 緩衝（15%）**

**買不起的三件事（會當場燒光預算）：**
1. MC-dropout（T=25）或 deep ensemble × **完整 ASVspoof21 DF（611k）** × 多模型 × 多 shift → 單項 1,000–2,000 GPU-h
2. **通道擴增訓練**（#3 的 5× 資料）× 多模型 × 多 seed → 單項 500–700 GPU-h
3. **逐樣本（per-sample）**的 laundering 搜尋或內嵌白盒最佳化 → 單項 500–700 GPU-h

---

## 1. 硬體基準與換算常數

| 項目 | 數值 | 來源 |
|---|---|---|
| RTX 4090 VRAM | 24 GB GDDR6X（**硬上限，無 NVLink，無法擴充**） | 【查】 |
| BF16/FP16 tensor 峰值（dense） | ~165 TFLOPS | 【查】 |
| 記憶體頻寬 | ~1,008 GB/s | 【查】 |
| **實務有效算力（MFU 25–40%）** | **40–60 TFLOPS** | 【推】語音 SSL 序列短（4s → 200 frames），attention 佔比低、conv 前端與 kernel launch 開銷高，MFU 偏低端 |
| 功耗 | 450 W → 1,300 GPU-h ≈ 585 kWh ≈ NT$2,300 電費 | 【推】可忽略 |
| **牆鐘換算** | 1,300 GPU-h ÷ 24 h/day ≈ **54 天連續滿載**；÷ 12 h/day ≈ **108 天** | 【推】**日曆上做得完，前提是 GPU 夜間無人值守也在跑** |

**參考錨點**（用來校準所有推算）：
> 「training and evaluating the w2v2-AASIST model using a GPU server equipped with two TESLA V100 graphics cards takes approximately 6 hours」——iWAX（Scientific Reports 2025）【查】
> 換算：2×V100 ≈ 250 TFLOPS 峰值、實際 MFU 低且有多卡開銷；單張 4090（165 TFLOPS 峰值、MFU 較好、無多卡通訊）約等於 1.0–1.5× 這台伺服器 → **XLS-R 300M + AASIST 在 19LA 上一次完整 train+eval ≈ 6–10 GPU-h on 4090**【推】。本文件所有 SSL 訓練成本以此為錨。

**資料集規模**（成本計算的分母）：

| 資料集 | 語句數 | 音訊時數（估） | 來源 |
|---|---|---|---|
| ASVspoof2019 LA train | 25,380 | ~27 h | 【查】 |
| ASVspoof2019 LA dev | 24,844 | ~26 h | 【查】 |
| ASVspoof2019 LA eval | 71,237 | ~75 h | 【查】 |
| ASVspoof2021 LA eval | 181,566 | ~190 h | 【查】 |
| **ASVspoof2021 DF eval** | **611,829** | **~650–700 h** | 【查】語句數；【估】時數 |
| In-the-Wild | **31,779** | **37.9 h** | 【查】 |
| MLAAD | 76k（v3）～160k+（v5） | 80–200 h | 【估】依版本，**用前務必自行核對** |

**關鍵觀察**：ASVspoof21 DF 一個資料集就等於其他所有資料集加起來的 2 倍。**它是整份預算表裡唯一一個會把設計炸掉的資料集。**

---

## 2. Backbone 訓練／微調成本表

全部以 **ASVspoof2019 LA train（25,380 筆）、4 秒 crop、bf16 AMP、含每 epoch dev 評估** 為基準。

| Backbone | 參數量 | 訓練 VRAM（bs） | 每 epoch | epochs | **單次訓練 GPU-h** | 24GB 塞得進？ |
|---|---|---|---|---|---|---|
| **AASIST**（從頭） | 297K【查】 | 4–6 GB（bs=24） | 1–2 min | 100【查】 | **2–4** | ✅ 非常寬鬆 |
| **AASIST-L** | 85K【查】 | 3–4 GB | ~1 min | 100 | **1.5–3** | ✅ |
| **RawNet2**（從頭） | ~17.6M | 5–7 GB（bs=24） | 1–2 min | 100 | **2–4** | ✅ |
| **XLS-R 300M + AASIST（full FT）** | 317M | **18–22 GB（bs=14）**<br>13–16 GB（bs=8） | 8–12 min | 20–30 | **6–10** | ⚠️ **塞得進但吃緊**。bs>16 會 OOM |
| 同上 + gradient checkpointing | 317M | 12–14 GB（bs=32） | +30% 時間 | 20–30 | 8–13 | ✅ 用時間換 VRAM |
| **XLS-R 300M frozen + backend** | 特徵已快取 | **2–4 GB** | 20–40 s | 50–100 | **0.3–1**<br>（＋特徵抽取 0.5–1 h，**一次性**） | ✅ **便宜 10–20×** |
| **WavLM Large + backend（full FT）** | 316M | 18–22 GB | 8–12 min | 20–30 | **6–10** | ⚠️ 同 XLS-R 300M |
| **XLS-R 1B — full FT + AdamW** | 965M【查】 | **≥21–23 GB** 且 bs≤2 | 40–60 min | 20 | 15–25 | ❌ **不建議**（見下） |
| **XLS-R 1B — LoRA + grad-ckpt** | 965M 凍結 + ~5–10M 可訓 | **8–12 GB（bs=8）** | 18–30 min | 20–30 | **8–15** | ✅ **這是 1B 在 4090 上唯一理性的做法** |
| **XLS-R 1B frozen 特徵抽取** | — | 4–6 GB（推論） | — | — | 1–2 h/資料集通過 | ✅ |
| **XLS-R 2B** | ~2.2B | 全 FT 完全不可能；LoRA 需 grad-ckpt + bs≤4 | — | — | 25–40 | ⚠️ 僅 frozen 推論可行 |
| **Whisper large-v3 encoder（frozen）** | 635M enc | 8–10 GB（推論 bs=8） | — | — | 特徵抽取 2–3 h / 10 萬筆 | ✅ 但貴（見下） |
| **Whisper large-v3 encoder（fine-tune）** | 635M | OOM（1,500-frame 序列 + 10 GB optimizer state） | — | — | — | ❌ **不可行** |
| **Whisper small encoder（frozen）** | 88M | 3–4 GB | — | — | 0.3–0.6 h / 10 萬筆 | ✅ 便宜 7× |

以上訓練時間全為【推】（以 iWAX 錨點 + FLOPs 推算 + 工程經驗校正），VRAM 為【估】。

### 2.1 XLS-R 1B 的 24GB 死線（算給你看）

AdamW 全參數微調，965M 參數的**記憶體下限**（尚未計入任何 activation）：

```
fp32 master weights   965M × 4 B = 3.86 GB
bf16 working copy     965M × 2 B = 1.93 GB
gradients (fp32)      965M × 4 B = 3.86 GB
Adam m, v (fp32)      965M × 8 B = 7.72 GB
───────────────────────────────────────────
小計                              17.4 GB   ← 還沒開始跑 forward
```
剩 6.6 GB 給 activation。4 秒音訊 = 200 frames × 1280 dim × 48 層，即使開 gradient checkpointing，bs=2 也只是勉強。**結論：技術上「塞得下」，但 bs=2、速度極慢、任何小改動就 OOM，不是可持續的研究節奏。**

**三條可行路徑**：
1. **LoRA（r=8–16，目標 q/v proj）**：base 凍結（bf16 1.93 GB）+ LoRA optimizer（~0.16 GB）+ activation（grad-ckpt, bs=8 → 4–6 GB）→ **8–12 GB，非常舒服**。【推】
2. **8-bit AdamW（bitsandbytes）**：optimizer state 從 7.72 GB → 1.93 GB，總計降到 ~11.6 GB → bs 4–8 可行。
3. **完全 frozen + 快取 pooled 特徵**：最便宜（1–2 h 抽取 + 0.5 h backend 訓練）。

> 【查】旁證：Scalable AASIST（arXiv 2507.11777）指出 **在資料受限時凍結 XLS-R 300M backbone 反而更好**（ASVspoof5 上 frozen EER 8.76%，把 AASIST 的 sinc 前端換成可訓 SSL encoder 只從 27.58% 降到 21.67%）。**這代表「frozen + 快取」不只是省錢的妥協，在碩論的資料規模下可能就是正確做法。** 這是本文件最重要的單一情報。

### 2.2 Whisper encoder 的隱藏稅

Whisper **強制把任何長度的音訊 pad 到 30 秒**（1,500 encoder frames）。

- 前向 FLOPs ≈ 2 × 635M × 1,500 ≈ **1.9 TFLOPs/樣本，與音檔長度無關**【推】
- 對照：XLS-R 300M 在 4 秒（200 frames）上 ≈ 0.2 TFLOPs/樣本 → **Whisper large-v3 貴 ~10×**
- **對「詐騙現場 3–5 秒短句」（方向四）特別不划算：算力有 85% 花在 padding 上。**
- 特徵快取更致命：frame-level 1,500 × 1,280 × 2 B = **3.8 MB/樣本** → 10 萬筆 = 380 GB，611k 筆 = 2.3 TB ❌

**對策**：只用 Whisper-small/medium encoder，或截短 positional embedding、或只快取 pooled 向量（2.5 KB/樣本）。

---

## 3. 推論成本

### 3.1 單位成本（GPU-h / 10 萬筆，4 秒平均，bf16，batched，本機 NVMe，**已含 I/O**）

| 模型 | GPU-h / 100k 筆 |
|---|---|
| AASIST / RawNet2 | **0.15–0.3** |
| XLS-R 300M / WavLM Large（含 backend） | **0.4–0.8** |
| XLS-R 1B | **1.2–2.5** |
| Whisper large-v3 encoder | **2.0–3.5** |
| Whisper small encoder | 0.3–0.6 |

全為【推】（FLOPs 推算 + I/O 開銷 2–3× 修正）。**注意：611k 個小 flac 檔的檔案系統開銷在 Windows 上可能比 Linux 差 2–3×；建議把資料集打包成 webdataset / HDF5 shard。**

### 3.2 跑一次完整 evaluation 要多久（**單一模型、單一條件**）

| 資料集 | AASIST | XLS-R 300M | XLS-R 1B |
|---|---|---|---|
| In-the-Wild 全集（31,779） | **5–10 min** | **10–15 min** | 25–50 min |
| ASVspoof19 LA eval（71,237） | 10–20 min | 20–35 min | 50–110 min |
| ASVspoof21 LA eval（181,566） | 30–55 min | 45–90 min | 2.2–4.5 h |
| **ASVspoof21 DF eval 全集（611,829）** | **1.5–3 h** | **2.5–5 h** | **7–15 h** |
| MLAAD（~100k） | 15–30 min | 25–50 min | 1.2–2.5 h |
| **以上全部（~980k 筆）** | **3–5 h** | **4–8 h** | **12–25 h** |

**削減者請記住這一行**：
> **In-the-Wild 全集便宜到可以隨便跑（10 分鐘）。ASVspoof21 DF 全集是一格 2.5–5 GPU-hour，它會被你設計裡的每一個乘數乘一次。**

---

## 4. 常被低估的成本

### 4.1 CPU codec 轉檔（AMR-WB / EVS / Opus / Speex / SILK）

| 項目 | 數值 |
|---|---|
| ffmpeg Opus/AMR-WB 單核吞吐 | **50–200× realtime**【估】 |
| **EVS 3GPP 參考 C 實作** | **5–20× realtime**【估】← **慢 10 倍，最常被低估** |
| Python/librosa 逐檔 decode-encode round-trip | 比 ffmpeg CLI 慢 **3–10×**【估】 |

以 16 核 CPU、平均 60× realtime/核 計：

| 規模 | 單一 codec 條件的 wall-clock（16 核並行） |
|---|---|
| 10 萬筆（~110 h 音訊） | **~7 分鐘** |
| ASVspoof21 DF 全集（~680 h 音訊） | **~43 分鐘** |
| **#3 的完整 C0–C5 網格（6 codec × 5 PLR = 30 條件）× 全集** | **~21 小時 wall**（若含 EVS → **50+ 小時**） |

**CPU 轉檔本身不吃 GPU 預算，但它吃你的日曆與磁碟。** 30 條件 × 全集 = 產出 30 份資料集副本（見 4.3）。

**紀律**：用 `ffmpeg` CLI + GNU parallel / xargs -P，**絕不要用 python 逐檔 librosa**。

### 4.2 Neural codec（EnCodec / DAC / SpeechTokenizer）transcode — **本表最大的隱藏成本**

| 項目 | 數值 |
|---|---|
| EnCodec / DAC 在 A100/V100 上的純 encode+decode RTF | **0.004–0.017**【查】 |
| **實務 pipeline 有效 RTF on 4090**（載入 flac → resample 到 24k/44.1k → encode → decode → resample 回 16k → 寫檔） | **0.03–0.08**【估】<br>resample 與磁碟 I/O 主導，不是模型 |

| 規模 | GPU-hour（單一 codec、單一 bitrate） |
|---|---|
| 10 萬筆（~110 h 音訊） | **4–8 GPU-h** |
| In-the-Wild 全集（37.9 h 音訊） | 1.5–3 GPU-h |
| **ASVspoof21 DF 全集（~680 h 音訊）** | **25–40 GPU-h** |
| **3 codec × 3 bitrate = 9 條件 × ASVspoof21 DF 全集** | **225–360 GPU-h** ❌ **吃掉 1/4 預算** |
| 同上但只在 5 萬筆抽樣子集上 | **18–36 GPU-h** ✅ |

**這是「一行 ffmpeg、零金錢」的錯覺陷阱。** 傳統 codec 確實幾乎免費；**neural codec transcode 是一個要跑在 GPU 上的 300M–1B 級生成模型**，成本和跑一次推論同級。任何把「neural codec transcode」寫成起點動作的設計（方向一 step iii、方向三 step i、方向五）**都必須在抽樣子集上做**。

### 4.3 磁碟空間

**基準**：16 kHz / 16-bit mono → WAV = 115 MB/小時；FLAC ≈ 60–70 MB/小時。

| 項目 | 空間 |
|---|---|
| 原始資料集（19LA + 21LA + 21DF + ITW + MLAAD） | **120–180 GB**【估】 |
| **每一個通道條件的副本（全集，FLAC）** | **~60 GB/條件** |
| 3 個通道條件（2×3 shift 矩陣） | +180 GB ✅ |
| **#3 的 30 條件網格（6 codec × 5 PLR）** | **+1.8–3.1 TB** ❌ |

**SSL 特徵快取——這裡是磁碟的生死線**：

| 快取粒度 | 每筆大小 | 10 萬筆 | **3 模型 × 6 條件 × 10 萬筆（180 萬筆）** |
|---|---|---|---|
| Frame-level、全 25 層、fp16 | ~10 MB | 1 TB | **18 TB** ❌❌ |
| Frame-level、僅最後一層、fp16（200×1024） | 410 KB | 41 GB | **740 GB** ❌ |
| **Pooled（時間平均）、全 25 層、fp16（25×1024）** | **51 KB** | 5 GB | **92 GB** ✅ |
| **Pooled 最後一層 + logits** | **2 KB** | 0.2 GB | **3.6 GB** ✅✅ |

> **鐵律：快取 pooled 向量，永遠不要快取 frame-level。差 200×。**
> 例外：若真的需要 frame-level（例如時間定位），只能在 ≤2 萬筆的子集上做。
> 副作用：SSL layer × channel 的 probing 熱圖（方向二 step (2)）**必須用 pooled per-layer 特徵**，這在方法上完全合理，且把 18 TB 壓成 92 GB。

**建議硬體**：**2 TB NVMe（工作區，特徵快取 + 當前條件）+ 4–8 TB HDD/外接（原始資料與封存）**。這筆錢（約 NT$8,000–15,000）比任何 GPU 優化都值。

### 4.4 對抗攻擊最佳化——每個樣本要跑幾次前向／反向

| 攻擊型態 | 每樣本 fwd/bwd 次數 | 每樣本耗時（XLS-R 300M，batch 化後） |
|---|---|---|
| PGD-50（白盒、可微） | 50 × (fwd+bwd) | **0.2–0.3 s**【推】 |
| PGD-50 + EOT-10（穿過不可微 codec，需 BPDA/EOT） | 500 × (fwd+bwd) | **2–3 s** ← **×10** |
| 黑盒 query 攻擊（NES / SimBA，2,000 queries） | 2,000 × fwd | **3–5 s** |
| 黑盒 query 攻擊（10,000 queries） | 10,000 × fwd | **15–25 s** ← **×5** |
| Laundering beam search（**recipe-level**，B=5, D=4, A=8 ≈ 160 node） | 160 × (batch transcode + fwd) | ~100 s / **每個 500 筆的 batch** |
| Laundering beam search（**per-sample**） | 160 × (transcode 4s + fwd) | **30–40 s / 樣本** ← **炸彈** |

**具體算例**：

| 設計 | GPU-hour |
|---|---|
| PGD-50，5,000 樣本 × 3 模型 × 5 個可微機制 | **6–13 h** ✅ |
| 同上但要穿過 codec（EOT-10） | **60–130 h** ⚠️ |
| 黑盒 2,000-query，1,000 樣本 × 3 模型 × 5 機制 | **20–40 h** ✅ |
| 黑盒 10,000-query，5,000 樣本 × 3 模型 × 5 機制 | **500–1,000 h** ❌ |
| Laundering beam search，**recipe-level**，5 偵測器 | **20–40 h** ✅ |
| Laundering beam search，**per-sample**，5,000 樣本 × 5 偵測器 | **200–280 h** ⚠️ |
| Laundering beam search，**per-sample + 每 node 內嵌 PGD-50** | **500–700 h** ❌ |

> **鐵律：laundering 搜尋必須在 recipe 層級（一條 pipeline 套用到全部樣本），不是 per-sample。** 這符合威脅模型（攻擊者找的是一個可重複的洗白配方，不是為每通電話客製），也省 100–500×。方向三的「攻擊成本上界」框架本來就是 recipe-level 的，這點運氣不錯——**但實作時要明文寫進協定，否則很容易滑進 per-sample。**

### 4.5 TTS 生成（方向四 / 商用樣本）

| 項目 | 成本 |
|---|---|
| 開源 TTS（XTTS-v2 / F5-TTS / CosyVoice）RTF on 4090 | 0.05–0.3【估】 |
| 生成 2 萬筆 × 5 秒 | **2–8 GPU-h** ✅ 便宜 |
| 5 家開源生成器 × 2 萬筆 | **10–40 GPU-h** ✅ |
| **閉源 API（ElevenLabs 等）2 萬筆 × ~100 字元 = 2M 字元** | **US$300–600**【估，需查當期價目】← **這是錢不是 GPU** |

---

## 5. 組合爆炸的價目表

### 5.1 總公式

```
GPU-hour_total =
    A. 訓練   = Σ_models  N_seed × N_train_variant × T_train(model, |D_train|)
  + B. 前處理 = Σ_conditions [ |D|·L·RTF_neural            (GPU, neural codec)
                             + |D|·L / (R_cpu · n_core)   (CPU, 傳統 codec，不吃 GPU 預算) ]
  + C. 評估   = N_model × M_condition × T_fwd(|D_eval|) × P_passes
  + D. 對抗   = N_model × K_diffable × N_attack_samples × Q_queries × t_fwd
```

**其中 `P_passes` 是決定生死的那一項：**

```
P_passes = 1                                    ← 全部 post-hoc 機制（MSP / temperature / energy /
                                                   Mahalanobis / softmax entropy）共用這一次前向
         + T_mc      (MC-dropout，T = 10~30)     ← 直接乘 10–30 倍
         + E         (deep ensemble，E = 5)      ← 乘 5 倍，而且還要多訓練 (E-1)×N_model 次
         + 1         (evidential / FADEL，需自己的 checkpoint，但推論是單次前向)
```

### 5.2 削減者的三個判斷法則（背下來）

| 法則 | 內容 |
|---|---|
| **法則 1：K（棄權機制）幾乎不乘訓練成本** | MSP / temperature scaling / energy / Mahalanobis / entropy 全部是 **post-hoc**——它們吃的是同一個 checkpoint 的同一次前向的 logits 與 pooled embedding。**只要你把 logits + pooled embedding 快取下來，第 2 到第 5 個機制的邊際 GPU 成本是零（後續全在 numpy/CPU 上算）。** 只有 MC-dropout（×T）、deep ensemble（×E 訓練 + ×E 推論）、evidential（+1 次訓練）真的要錢。**K=7 看起來嚇人，實際上只有 3 個要錢。** |
| **法則 2：M（shift 條件）只乘評估與前處理，不乘訓練** | ——**除非**你做 channel-augmented training。一旦要做通道擴增訓練（#3 的做法），訓練資料 ×5，單次訓練從 6–10 h 變 **30–50 h**，整個訓練預算 ×5。**通道擴增訓練 與 deep ensemble 不能同時要。** |
| **法則 3：資料集大小是所有乘數的共同底數** | ASVspoof21 DF 全集（611k）比 10 萬筆抽樣池貴 **6×**，比 In-the-Wild 全集貴 **20×**。**分層抽樣到 2 萬筆，成本降 30×，而 EER 標準誤只從 ~±0.1% 升到 ~±0.4%**【推，以 binomial SE 估】——**足以分辨 >1 個百分點的差異，而 ADD 的 shift 效應都是 5–40 個百分點的量級。** 這是整份預算表裡 CP 值最高的一刀。 |

### 5.3 具體算例（削減者可直接套用）

#### 算例 1：方向一「原案全開」（3 模型 × 7 機制 × 6 shift 格 × 全部資料集全集）

| 項目 | 計算 | GPU-h |
|---|---|---|
| 訓練 | 3 base + 3 evidential + 3×4 ensemble seed = **18 run** × 6 h | **108** |
| 前處理 | neural codec transcode 980k 筆 × 2 個 codec 條件 | **80–120** |
| 評估（單次前向，5 個 post-hoc 機制共享） | 3 模型 × 6 格 × 9.8（十萬筆）× 0.6 h | **106** |
| **＋ MC-dropout T=25** | × 25 | **＋2,646** ❌❌ |
| ＋ deep ensemble ×5 | × 5 | ＋530 ❌ |
| 對抗（PGD-50，5,000 樣本 × 3 模型 × 5 機制） | | 13 |
| **總計** | | **≈ 3,500 GPU-hour** |
| **判定** | | ❌ **超出預算 2.5×。單一元凶：MC-dropout × 全集。** |

#### 算例 2：同一個設計，只換兩個決策（分層抽樣 + 快取共用）

決策：(a) ASVspoof21 DF / 19LA eval / MLAAD 各分層抽 2 萬筆，In-the-Wild 用全集（本來就只有 32k）→ **評估池 ≈ 10 萬筆**；(b) 快取 logits + pooled embedding，post-hoc 機制全部離線算；(c) MC-dropout T 降到 10。

| 項目 | 計算 | GPU-h |
|---|---|---|
| 訓練 | 18 run × 6 h（不變） | **108** |
| 前處理 | neural codec 10 萬筆 × 2 條件 | **10–16** |
| 評估（單次前向） | 3 × 6 × 1.0 × 0.6 | **11** |
| ＋ MC-dropout T=10 | × 10 | ＋108 |
| ＋ deep ensemble ×5 | × 5 | ＋54 |
| 對抗（PGD-50） | | 13 |
| **總計** | | **≈ 300 GPU-hour** ✅ |
| **判定** | | ✅ **買得起，還剩 4× 餘裕。** |

> **算例 1 → 算例 2：3,500 → 300 GPU-hour（12×），設計的科學內容一格都沒少。**
> **削減者請把這件事讀進去：方向一的問題從來不是算力，是「有沒有人算過」。**

#### 算例 3：加入通道擴增訓練（#3 的做法）

若每個模型都要有「乾淨訓練」與「通道擴增訓練（5× 資料）」兩個 variant：

| 情境 | GPU-h |
|---|---|
| 3 模型 × (6 h 乾淨 + 40 h 擴增) = 3 × 46 | **138** ✅ 可接受 |
| 同上 × 5 個 ensemble seed | **690** ❌ 佔掉半個預算 |
| **判定** | **通道擴增訓練 XOR deep ensemble。二選一，不能都要。** |

#### 算例 4：方向三攻擊成本地圖

| 情境 | GPU-h |
|---|---|
| 5 偵測器 × recipe-level beam search（B=5, D=4, A=8） | **20–40** ✅ |
| ＋ 3 類防線（被動 / provenance / liveness） | **60–120** ✅ |
| 若滑進 per-sample search | **200–280** ⚠️ |
| 若 per-sample + 每 node 內嵌 PGD | **500–700** ❌ |

#### 算例 5：方向四（詐騙現場考卷）

| 項目 | GPU-h |
|---|---|
| 5 家開源 TTS × 2 萬筆生成 | 10–40 |
| ＋ 情緒 3 檔 × 句長 3 檔 = 9 分層（不增加總樣本數，只是分層抽） | +0 |
| 通道疊加（CPU codec 為主 + 1 個 neural codec） | 5–10 |
| 3 偵測器 × 4 象限評估（評估池 ~10 萬筆） | 7–10 |
| 品質協變量標註（UTMOS + speaker similarity，10 萬筆） | 3–6 |
| **總計** | **≈ 30–70 GPU-hour** ✅ **全場最便宜的方向** |

#### 算例 6：一個「看起來合理但買不起」的設計（給削減者當警示）

> 「5 個 backbone（含 XLS-R 1B、WavLM Large）× 7 種棄權機制 × 6 codec × 5 PLR（30 個通道條件）× 3 個資料集全集，每個配置 3 個 seed」

| 項目 | GPU-h |
|---|---|
| 訓練 5 backbone × 30 通道條件（channel-conditioned）× 3 seed × 平均 15 h | **6,750** ❌ |
| 前處理 30 條件 × 980k 筆（含 neural codec） | **300+** ❌ |
| 評估 5 × 30 × 9.8 × 1.0 h × P_passes(16) | **23,500** ❌❌ |
| **總計** | **≈ 30,000 GPU-hour（= 20 年）** |

**這個設計沒有一個字看起來不合理。它會殺死一篇碩論。** 削減者在看到任何「N × M × K」的句子時，請當場套 5.1 的公式。

---

## 6. 紅線清單——這張卡上明確做不到的事

| # | 項目 | 為什麼做不到 |
|---|---|---|
| **R1** | **從頭 pretrain 任何 SSL backbone**（XLS-R / WavLM / wav2vec2） | XLS-R 300M 原始 pretrain ≈ 數千至數萬 GPU-day。**差 3–4 個數量級。連想都不要想。** |
| **R2** | **XLS-R 1B / 2B 的全參數 fine-tune（標準 AdamW）** | 1B 的 optimizer state + master weights = **17.4 GB，還沒開始跑 forward**。2B 直接不可能。**只能 LoRA / 8-bit optimizer / frozen。** |
| **R3** | **Whisper large-v3 encoder 的 fine-tune** | 1,500-frame 序列 + 10 GB optimizer state → OOM。**只能 frozen 特徵。** |
| **R4** | **MC-dropout（T≥20）或 deep ensemble × ASVspoof21 DF 全集（611k）× 多模型 × 多 shift** | 單項 **1,000–2,600 GPU-h**。**必須抽樣。** |
| **R5** | **完整複製 #3 的 6 codec × 5 PLR × 全資料集網格，並在其上重訓** | 訓練集擴增到 180 萬筆（#3 自己就是這麼做的）→ **單次訓練 100–200 GPU-h**，+ 磁碟 **1.8–3.1 TB**。 |
| **R6** | **Frame-level SSL 特徵快取（全 25 層）於大資料集** | **18 TB。磁碟先死，GPU 都還沒動。** |
| **R7** | **Per-sample laundering search 內嵌白盒最佳化** | 500–700 GPU-h。**必須 recipe-level。** |
| **R8** | **黑盒 query 攻擊（≥10,000 queries）× ≥5,000 樣本 × 多模型 × 多機制** | 500–1,000 GPU-h。**N_attack × Q 是乘法，要當場算。** |
| **R9** | **3 個 neural codec × 3 個 bitrate × ASVspoof21 DF 全集 transcode** | 225–360 GPU-h（**光是 transcode，還沒開始評估**）。 |
| **R10** | **真正的超參數 sweep（>20 組配置）× SSL 訓練 × 多模型** | 20 × 5 模型 × 8 h = 800 GPU-h。**碩論只能用文獻的超參數，最多掃 3–5 組 learning rate。** |
| **R11** | **>1 萬筆閉源商用 API 生成** | **不是 GPU 問題，是錢**（US$300–600 / 2 萬筆，且 guardrail 風險）。 |
| **R12** | **同時做兩個方向**（例如方向一 + 方向二） | 不是算力問題（加起來 ~500 GPU-h 也還好），**是一個人的日曆問題**。方向二的 rig 工程工時是 GPU-hour 之外的獨立預算。 |

---

## 7. 省錢技巧與各能省多少

依 **CP 值排序**（省下的倍數 ÷ 實作代價）：

| # | 技巧 | 省多少 | 代價 | 削減者請注意 |
|---|---|---|---|---|
| **S1** | **一次前向、快取 logits + pooled embedding，全部 post-hoc 棄權機制共用** | **省 (K−1)/K ≈ 85%**（K=7 時，只有 3 個機制真的要 GPU） | 零。就是好工程。 | **這是本論文最大的一筆省錢，而且它讓「7 種棄權機制」這個看似奢侈的設計變成幾乎免費。削減者不必為了省錢砍掉棄權機制的數量。** |
| **S2** | **分層抽樣**（ASVspoof21 DF 611k → 2 萬筆） | **省 30×** | EER 標準誤從 ±0.1% → ±0.4%【推】。ADD 的 shift 效應是 5–40 個百分點量級，**完全分得出來**。 | 在論文裡老實寫「evaluation subset (stratified, n=20,000, seed fixed)」並附 bootstrap CI。**這是可以理直氣壯寫進 paper 的做法，不是偷工減料。** |
| **S3** | **快取 pooled 而非 frame-level 特徵** | **磁碟省 200×**（18 TB → 92 GB） | 失去時間定位能力（本論文不需要）。 | 讓 SSL layer-wise probing 從「不可能」變成「92 GB」。 |
| **S4** | **共用 checkpoint**：全部 shift 條件、全部棄權機制、全部對抗攻擊共用同一組 3–6 個 base checkpoint | **省 M×K 倍的訓練成本** | 零——這本來就是正確的實驗設計（要比較機制，就必須固定 backbone）。 | 若看到任何設計「每個 shift 條件重訓一次」，**當場砍掉**，除非它明確要研究 channel-conditioned training。 |
| **S5** | **混合精度（bf16 AMP）** | VRAM **省 30–40%**，速度 **1.5–2×** | 零（4090 原生支援）。 | **強制，非選項。任何沒開 AMP 的估算都是錯的。** |
| **S6** | **Frozen SSL + 快取特徵訓練 backend** | 訓練成本 **6–10 h → 0.3–1 h（省 10–20×）**；VRAM **22 GB → 3 GB** | 【查】在資料受限時**可能沒有代價，甚至更好**（ASVspoof5 上 frozen EER 8.76%）。 | **這是碩論最理性的預設值。full fine-tune 應該是需要辯護的例外，不是預設。** |
| **S7** | **LoRA（用於 XLS-R 1B / WavLM Large）** | VRAM **從不可行 → 8–12 GB**；時間比全 FT **省 30–40%** | 通常 EER 略遜於全 FT（0–2 個百分點）。 | **這是把 1B 級模型放進論文的唯一方式。** 但先問：**論文真的需要 1B 嗎？** |
| **S8** | **Recipe-level（而非 per-sample）laundering 搜尋** | **省 100–500×** | 零——**而且更符合威脅模型**（攻擊者要的是可重複的配方）。 | |
| **S9** | **資料集打包成 webdataset / HDF5 shard** | I/O **省 2–3×**（尤其在 Windows 上讀 611k 個小 flac） | 一天的工程。 | 這一項在 Windows 上比在 Linux 上重要得多。 |
| **S10** | **neural codec 只在抽樣子集上做** | **省 12–30×**（360 h → 25 h） | 零（反正評估也在子集上）。 | |
| **S11** | **短 crop（4s → 2s）訓練** | 訓練成本近似**減半** | 短句 ADD 有已知效能代價（AASIST2 論文的主題）。**若論文主題就是短句（方向四），這反而是必要的。** | |
| **S12** | **torch.compile + SDPA/flash attention** | SSL 前向 **1.2–1.5×** | 半天的工程 + 偶發相容性問題。 | 有餘力再做。 |

**S1 + S2 + S4 + S6 疊加起來，就是算例 1（3,500 h）→ 算例 2（300 h）的那 12 倍。**

---

## 8. 給削減者的一頁結帳單

### 8.1 建議的預算分配（以 1,350 GPU-hour 中位數計）

| 科目 | 預算 | 買到什麼 |
|---|---|---|
| **訓練** | **350 GPU-h** | **≈ 45–55 次標準訓練**（6–8 h/次，XLS-R 300M 級 full FT）<br>或 ≈ 100 次輕量訓練（AASIST/RawNet2）<br>或 ≈ 350 次 frozen-feature backend 訓練 |
| **評估** | **300 GPU-h** | **≈ 600–800 格評估**（1 模型 × 1 條件 × 10 萬筆抽樣池，含快取共用的全部 post-hoc 機制）<br>或 ≈ 70 格評估（若堅持 ASVspoof21 DF 全集） |
| **對抗評估** | **200 GPU-h** | recipe-level laundering 搜尋（5 偵測器 × 3 類防線）+ PGD-50 白盒（5,000 樣本 × 15 個 (模型,機制) 組合）+ 中等規模黑盒 query 攻擊 |
| **資料前處理 / codec / 特徵抽取 / TTS 生成** | **150 GPU-h** | neural codec transcode 抽樣子集（多條件）+ SSL 特徵抽取與快取 + 開源 TTS 生成 |
| **緩衝（15%）** | **200 GPU-h** | 你會用到的。 |
| **合計** | **1,200 GPU-h** | （上限 1,500 時，緩衝可放大到 350） |

### 8.2 削減者的檢查清單（每個設計都要跑一遍）

1. **有沒有任何一格用到 ASVspoof21 DF 全集（611k）？** → 若有乘數（MC-dropout / ensemble / 多 codec）在它身上，**立刻抽樣到 2 萬筆**。
2. **P_passes 是多少？** → 若 >5，找出是誰（八成是 MC-dropout 或 ensemble），問「拿掉它論文還成立嗎」。
3. **訓練次數 × 每次時數是多少？** → 若 >400 GPU-h，八成是 (a) ensemble seed，或 (b) channel-augmented training。**這兩個不能同時要。**
4. **有沒有 neural codec transcode？在多大的資料上？** → 每 10 萬筆 4–8 GPU-h，全集 25–40 GPU-h/條件。
5. **對抗評估是 recipe-level 還是 per-sample？** → per-sample 是紅線。
6. **特徵快取是 pooled 還是 frame-level？** → frame-level 是紅線（除非 ≤2 萬筆）。
7. **有沒有 XLS-R 1B / 2B 的全參數 fine-tune？** → 紅線。改 LoRA 或 frozen，**或先問論文真的需要 1B 嗎**。
8. **磁碟夠嗎？** → 通道條件數 × 60 GB + 特徵快取。>2 TB 就要重新設計。

### 8.3 工程師的一句話結論

> **在單張 4090 上，一篇 ADD 碩論的瓶頸不是 GPU-hour，是「有沒有人在設計時算過乘法」。**
> 同一個科學內容，會不會用「共用快取 + 分層抽樣 + 共用 checkpoint + frozen backbone」這四招，決定了它是 300 GPU-hour（買得起，還剩 4× 餘裕）還是 3,500 GPU-hour（買不起，論文死在第 8 個月）。
> 真正的紅線只有三條：**(1) 大模型全參數微調（VRAM 死線，物理事實，無解）；(2) 任何乘數 × ASVspoof21 DF 全集；(3) per-sample 的最佳化搜尋。** 避開這三條，第二輪那個「8 個 deliverable」的方向一，**在算力上其實買得起**——它買不起的是**一個人的日曆**，而那不是這份文件能解決的問題。

---

## 附錄：查證來源

- AASIST 297K / AASIST-L 85K 參數、100 epochs、ASVspoof2019 LA — [AASIST (arXiv 2110.01200)](https://arxiv.org/pdf/2110.01200)
- w2v2-AASIST 訓練+評估 ≈ 6 h on 2× Tesla V100（本文件所有 SSL 訓練估算的錨點） — [iWAX, Scientific Reports 2025](https://www.nature.com/articles/s41598-025-24361-5)
- Frozen XLS-R 300M 在資料受限時優於可訓前端（ASVspoof5 EER 8.76% vs 21.67%） — [Towards Scalable AASIST (arXiv 2507.11777)](https://arxiv.org/pdf/2507.11777)
- XLS-R 1B ≈ 965M 參數 — [XLS-R + SLS Classifier (OpenReview)](https://openreview.net/pdf?id=acJMIXJg2u)
- EnCodec / DAC GPU RTF 0.004–0.017（A100 / V100） — [DualCodec (arXiv 2505.13000)](https://arxiv.org/pdf/2505.13000)、[FlexiCodec (arXiv 2510.00981)](https://arxiv.org/pdf/2510.00981)
- In-the-Wild 31,779 語句 — [多篇引用，見 ASVspoof 2021 (arXiv 2210.02437)](https://arxiv.org/abs/2210.02437)
- ASVspoof 2021 DF / LA 評估集規模 — [ASVspoof 2021 (arXiv 2210.02437)](https://arxiv.org/abs/2210.02437)
- 通道模擬 DA 擴增到 1,832,070 筆訓練樣本（R5 紅線的來源） — survey #3，[arXiv 2504.12423](https://arxiv.org/abs/2504.12423)
- LoRA / adapter 用於 ADD 的 SSL backbone — [Wav2DF-TSL (arXiv 2509.04161)](https://arxiv.org/pdf/2509.04161)
