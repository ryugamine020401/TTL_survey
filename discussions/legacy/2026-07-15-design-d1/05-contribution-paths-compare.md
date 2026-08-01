# 三條「有方法貢獻」路徑對照

日期：2026-07-15
背景：作者裁定純 measurement thesis 不足、要有方法/建構層級的貢獻。就 1/4/5 各掛一個方法貢獻，對照風險。
紀律前提：**方法只能一個、由量測動機出來、development-only、不碰 holdout 調參**（不是 method zoo）。凡 novelty 宣稱標「待 Codex 查證」。

---

## 對照總表

| 維度 | A：#1 + conformal 選擇性風險方法 | B：#5 + soft-binding 建構 | C：#4 + 通道穩健方法 |
|---|---|---|---|
| **貢獻物** | 一個 development-only 的方法/保證 | 一個你手建的系統/密碼學 artifact | 一個 channel-robust 方法 |
| **量測的角色** | 動機（證明方法被需要） | 容量前緣（證明 payload 不行） | optimism gap γ（證明模擬騙人） |
| **novelty 風險** | **低**（方法在 conformal 文獻，避開擁擠的 ADD-threshold 量測紅海） | **高**（soft-binding 有鄰近前作，C2PA/Authenticated Contradictions） | **高**（量測與 DA 方法都擁擠：Delgado/RTCFake + Shi et al. DA） |
| **算力（4090）** | **最低** ~55–85h（post-hoc on cached scores + 基礎偵測器） | 低 ~220h 但工程重 | 最高 ~510h（通道×偵測器×條件） |
| **資料風險** | **最低**（無 RTCFake 依賴） | 中（watermark 開源；真實通道可選） | **最高**（RTCFake 單點故障 HTTP 401） |
| **一年可行性** | **高**（重用#1 全部設計+pilot） | 中（build 專案，看建多大） | 中（受 RTCFake 取得閘制約） |
| **失敗退路** | **強**：方法失敗＝產出「不可轉移性證書」，仍是方法 | 中：索引也死＝政策級負結果（反脆弱） | 弱：γ≈1 直接抽掉前提 |
| **紀律風險** | 中（忍住別堆多方法） | 中（忍住別過度建 transparency-log） | 中（方法必須非 DA，否則撞 Shi） |

---

## A：方向#1 + conformal 選擇性風險方法（推薦）

**論文形狀**：診斷 → 修復。量測（fixed (q+t) 在未見生成器上系統性違約）是**動機**；貢獻是**方法**。

**方法選項**（選一個）：
1. **generator-shift-aware conformal risk control**（首選）：用 conformal / risk control 給棄權閾值一個 distribution-free 的 selective-risk 保證。核心 twist：標準 conformal 假設 exchangeability，generator shift 打破它 → 提一個 group/worst-case-over-generator-family 的 conformal 程序，**或在做不到時開出「保證不可轉移」的證書**。這是「方法 + 形式性質」。
2. shift-robust score normalization（development-only）：較弱、較經驗。
3. shift-robust rejection objective 訓練（如 group-DRO SelectiveNet）：訓練成本較高。

**為什麼避開紅海**：Zhou/Schäfer 他們做的是「量測失效」，沒人提**修復 + 保證**。方法的 novelty 落在 conformal 文獻，與擁擠的 ADD-threshold-transfer 量測是不同賽道。
**待 Codex 查證**：conformal prediction / risk control 用於 audio anti-spoofing 或 deepfake abstention 是否已有前作；group/shift-robust conformal for selective ADD 是否開放。
**失敗退路（強）**：若任何 development-only 方法都救不了這種 shift，產出「此類 generator shift 下 development-only 保證證明不可轉移 + 何時失敗的證書」——仍是方法貢獻（un-transferability detector），不是純負結果。
**算力**：post-hoc 在快取分數上做，conformal 校準幾乎零 GPU；只有基礎偵測器成本。~55–85h。

## B：方向#5 + 「索引不 payload」soft-binding 建構

**論文形狀**：審計 watermark 在通道的可靠 bit 容量 → 建一個構造繞開容量死結。

**貢獻物**：不把完整 provenance payload 嵌波形（低容量通道會死），只嵌一個短**索引**指向 transparency-log，測「索引能否活在 payload 活不了的通道」。
**novelty 風險（高）**：審計面 A5 已被否證（AudioMarkBench、RAW-Bench、WMCodec 已碰 neural codec）；novelty 必須全落在**構造**。但 soft-binding / 間接綁定在 C2PA 與 Authenticated Contradictions(CVPR 2026 W) 已是鄰近概念——**待 Codex 查證**：「短索引 watermark + 外部 log」是否已被提出。
**算力**：低 ~220h，但工程重（建構造、log、通道管線）。
**資料**：AudioSeal/WavMark/SilentCipher 開源；真實通道可用模擬 codec 階梯替代（去 RTCFake 依賴）。
**失敗退路（中）**：索引也死 → 「provenance 在詐騙通道不可達」政策級負結果，反脆弱。
**適合**：想要「手建系統/密碼學 artifact」的學位，且能承受構造 novelty 風險。

## C：方向#4 + 通道穩健方法

**論文形狀**：量真實 vs 模擬 optimism gap γ → 提方法關上落差。

**方法選項**：channel-distortion-invariant calibration（development-only）/ test-time adaptation；**不能只是 channel-conditioned DA**（Shi et al. 已做，會撞題）。
**novelty 風險（高）**：量測（A8 已否證：Delgado 2025、RTCFake ACL 2026）與最顯然的方法（DA）**都擁擠**；方法必須是非 DA 的東西，空間被挑過。
**算力**：最高 ~510h（通道×偵測器×條件矩陣）。
**資料風險（最高）**：整個「真實 vs 模擬」前提繫於 **RTCFake（HTTP 401、redistribution 未知）**；退到純模擬就抽掉「真實」賣點。
**失敗退路（弱）**：若 γ≈1（模擬其實夠好），前提與方法一起垮。

---

## 建議

**風險調整後排序：A > B > C。**

- **A（#1 + conformal）** 最佳：重用我們已做的全部#1 設計與 pilot、算力最低、資料風險最低、方法落在未擁擠的 conformal 賽道、連失敗都產出方法（不可轉移性證書）。它把「更有貢獻」與「更好守」同時達成。
- **B（#5 建構）** 是好的替代——若你要的「貢獻」specifically 是**手建一個系統/密碼學 artifact**，這條最像那個味道，但構造 novelty 要先過 Codex。
- **C（#4）** 風險最高：方法空間擁擠 + RTCFake 單點故障，除非你能自己取得真實通道資料，否則不建議當主線。

**下一步（選 A 的話）**：pilot 規格幾乎不變（我們已備），只在其上加「conformal 校準 + 一個 baseline 閾值法」的對照；並把「conformal for selective ADD 是否有前作」加進給 Codex 的待查。選 B/C 則需要各自重寫一次設計會。
