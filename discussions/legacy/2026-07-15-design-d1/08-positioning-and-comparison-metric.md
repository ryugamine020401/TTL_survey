# 定位框架與比較指標：我們的方法 vs 前作

日期：2026-07-17
目的：在把 prior-art 搜尋交給 Codex 前，先定義「我們的方法是完全創新 / 類似想法不同方法」的判準，以及一個能量化「我們比他們好在哪」的比較指標。
對象方法：narrowed D1-P（輕量 ADD 的選擇性可靠性 + reliability-aware distillation），含 red-team 後的 H1′/H2′。

---

## 一、先誠實分層：我們的「創新」不是單一層，而是四層各有不同狀態

把我們的主張拆成四層，每層的前作狀態不同——這比籠統問「完全創新嗎」有用得多：

| 層 | 我們的主張 | 前作狀態（待 Codex 確認） | 所以我們的 novelty **不在**這層 / **在**這層 |
|---|---|---|---|
| **現象層**：壓縮在辨識力不變下仍破壞 uncertainty/calibration | 我們在 ADD 觀察到 | **很可能在 general ML/vision 已知**（pruning/quantization 傷 calibration 與 OOD） | **不在**——若已知，我們是「在 ADD 確認並利用它」 |
| **設定層**：輕量/edge ADD | 我們壓縮 ADD 偵測器 | **已知**（DK-CAST、FTDKD、edge/browser 2606.30780） | **不在** |
| **可靠性層**：ADD 的 selective reliability | 我們量拒答可靠性 | **已知但在 full model 上**（Pascu、FADEL） | **不在**（泛稱） |
| **交集 + 方法層**：輕量 ADD × 未見生成器的 external selective-risk transfer × 一個「保住它」且打贏 recalibration 的 distillation 方法 | 這是我們的主張 | **看似 open**（Codex gate：no inspected hit） | **在這裡** |

**結論（誠實版）**：我們的方法**不是「完全創新」**（憑空全新）。最誠實的定位是——**「一個已知現象（壓縮傷可靠性）+ 一個已知設定（輕量 ADD）+ 一個已知關注（ADD 可靠性），三者以前沒人接在一起；而我們加的是一個 ADD-specific 的方法，並揭露現有輕量 ADD 悄悄流失了 selective reliability」**。這種「新組合 + 新方法」在碩論是**完全站得住的**貢獻型態，比硬撐「完全創新」誠實也安全。

## 二、關鍵：一個能比較「我們 vs 他們」的指標（回答你的核心問題）

**有，而且它就是這篇論文貢獻的量尺本身。** 更妙的是——**即使前作沒有報告這個指標，我們也能把他們的（開源）模型/方法丟進這個指標去比**，因為指標是我們定義的、可以事後施加的。

### 比較軸：在「辨識力 matched + 部署預算 matched」下，被保住的 selective reliability

固定兩件事讓比較公平：
1. **部署預算 matched**：同 model size / 同 CPU latency（他們的賣點）。
2. **辨識力 matched**：同 AUROC / eAURC（排序能力）。

在這兩者都 matched 之下，比**這個指標**：

> **primary 指標 = 未見生成器 holdout 上，source-fixed `(q,t)` 的 generator-macro confident-real leakage**（等價：fixed-`(q,t)` risk violation / calibration-transfer error）。

### 兩個講故事用的子指標

1. **「悄悄流失」指標（打在他們身上）**：
   `ΔEER ≈ 0（或 matched）` **但** `Δ(fixed-(q,t) violation) > 0`。
   → 這一個數字就說完了「他們在 EER 上看起來沒事，但在實際部署的操作點上漏掉 fake」。這是**我們揭露、他們沒量**的東西。

2. **「保住」指標（我們 vs baseline）**：
   在 matched 辨識力+預算下，`我們的 generator-macro confident-real leakage < {ordinary KD, ordinary KD + source-dev recalibration}`。
   → red-team 的致命 baseline 在這裡就位：**我們必須贏的不只是 ordinary KD，是「ordinary KD + 重新校準」**。

### 為什麼這個比較法很有力
- **不依賴他們有沒有報告**：他們的輕量模型是開源或可複現的，我們把它們跑過我們的指標即可——他們「沒量到」正是我們的貢獻點，不是障礙。
- **公平**：matched 辨識力+預算，排除「你只是模型比較大/比較好」的反駁。
- **直接對應部署**：confident-real leakage 就是「大眾把 fake 當 real 放行」的真實危害，不是抽象的 AUC。

## 三、因此，真正決定成敗的一個前作問題（交給 Codex）

上表的**現象層**是關鍵未知：**general ML/vision 是否已經確立「壓縮在辨識力不變下傷 calibration/uncertainty/OOD/selective prediction」？**
- 若**已確立**（很可能）→ 我們**不宣稱這個現象是我們發現的**，而是引用它當動機；我們的貢獻退到「ADD-specific 確認 + 未見生成器 selective 的專屬量測 + 方法 + 那個 ΔEER≈0 但 Δviolation>0 的 ADD 具體證據」。
- 更關鍵的第二問：**general ML 是否已有「calibration/uncertainty-preserving 的壓縮/distillation 方法」？** 若有 → 我們的 H2 方法**必須對它定位**（我們是 ADD-specific 改良，還是其實在重造它的輪子？）。**這條直接決定 H2 的方法 novelty 生死。**

這兩問是 Codex 的活（全文查證），不是我能憑印象斷的。我把它們寫成搜尋 brief。

## 四、給 Codex 的搜尋 brief（摘要，完整見 handoff）
1. **現象**：compression/pruning/quantization/KD 是否已被證明在 matched accuracy 下傷 calibration/uncertainty/OOD/selective prediction（general ML + 任何 audio/speech）。
2. **方法**：是否已有 calibration/uncertainty/selective-reliability-preserving 的壓縮或 distillation 方法（general ML 或 audio）——這是 H2 novelty 生死線。
3. **指標**：是否有人已用「matched-discrimination 下的 selective-risk / fixed-threshold violation」當壓縮的評估軸——若有，我們的比較指標是沿用；若無，指標本身也是小貢獻。
4. 回填第一節四層表的「前作狀態」欄，讓我們能寫出一句誠實的 novelty 定位。
