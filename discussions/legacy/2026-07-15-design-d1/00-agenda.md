# 方向#1 精簡設計會：議程與紀律

日期：2026-07-15
對象：方向#1《未知語音生成器下深偽偵測棄權門檻的可轉移性》
基礎：`discussions/2026-07-15-verified/five-directions-verified.md`（查證後定稿）
      `research/validations/2026-07-15-claims-to-verify-a-d.md`（Codex A–E 查證，尤其 A2、A3、E1、第 8 節 EE 碩論形狀、第 9 節 pilot）
      `discussions/2026-07-14-convergence/01-compute-budget.md`（算力硬預算）

## 這場會的目的（範圍嚴格鎖定）

方向#1 已選定。這場會**不重新發想、不比較其他方向**，只做一件事：**把 pilot 前必須先答的設計問題定成單一決策**，讓後續 pilot 與全論文有明確規格。

## 紀律（違反即不合格，這是前幾輪範圍爆炸的教訓）

1. **每個設計問題輸出「單一決策 + 一句理由」**，不是列選項清單。
2. **只准砍與收斂，不准加**：不得新增實驗、RQ、資料集、baseline，超出查證後定稿的範圍。任何「不如順便多做…」一律標為 out-of-scope/future work。
3. **算力對帳**：任何設計選擇若增加訓練/評估次數，必須當場用 `01-compute-budget.md` 估 GPU-hour，總和守在 **430–520 GPU-h**。
4. **前作宣稱不自己下結論**：凡「這是首次/無前作」一律標記「待 Codex 查證」，不寫死。
5. **社會意義只進 intro/discussion**，不長出實驗（已放棄受騙率當因變數）。

## 待定的設計問題（pilot-critical 優先）

### 【pilot 必須先答】
- **Q-SPLIT**：generator-family disjoint 的 split 具體怎麼切？如何控制 DFADD 的訓練語料/vocoder 與 ASVspoof19 LA 種子的重疊（Codex E1：名字新 ≠ 嚴格 unseen）？train/dev/test 各扮什麼角色？如何證明無 leakage？
- **Q-METRIC**：primary metric 定哪一個（fixed-FPR≤1% selective recall / AURC / risk-coverage violation）？risk-constraint violation 怎麼量與報告？
- **Q-PILOT**：把 Codex 第 9 節的最小驗證**具體化**：用哪一個 detector、哪個 dev 集、哪兩個 risk target、哪個 DFADD holdout 子集、success/stop 條件的數值門檻。

### 【全論文需要、pilot 可先用子集】
- **Q-SCORES**：最終要納哪幾種棄權分數？（候選：MSP、temperature scaling、deep ensemble、MC-dropout、energy、Mahalanobis-on-SSL、FADEL evidential）——**deep ensemble = N× 訓練，須算 GPU-hour 決定納不納**；砍到算力守得住的集合。
- **Q-RQ2**：density-based 與 discriminative-derived 兩類分數，如何在**控制共同 backbone 與 representation quality** 下公平比較（Codex A2），否則結論只是模型容量差？
- **Q-RQ3**：confident-real / `max P(confident-real|fake)` 的 threat model、query/quality budget、以及相對一般 targeted attack 的增量價值怎麼定（Codex A3）？
- **Q-CONTRIB**：貢獻結構（protocol / failure map / 選配 method / 負結果）與**可證偽的 primary claim**一句話；負結果長什麼樣、在什麼條件成立。

## 角色（4）

- **M 選擇性預測方法學家**：Q-SCORES、Q-RQ2、Q-METRIC 主責
- **E 評估嚴謹度方法學家**：Q-SPLIT、Q-METRIC、leakage/confound 主責
- **T 威脅模型設計者**：Q-RQ3 主責
- **P 指導教授（範圍/貢獻把關）**：Q-CONTRIB、算力對帳、EE 碩論形狀、pilot 收斂主責

## 輸出

`03-design-decisions.md`：每個 Q 一個單一決策 + 理由 + GPU-hour 影響 + 是否待 Codex 查證；外加一份**可直接執行的 pilot 規格**。
