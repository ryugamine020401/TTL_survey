# 五個收斂方向（一位碩士生 / 一年 / 一張 RTX 4090）
日期：2026-07-14

> 統整者按：本文閱讀了 `00-constraints.md`（最高指導原則）、`01-compute-budget.md`（硬預算表）、`cuts/` 五份削減紀錄、`final/` 五份定稿，並以第二輪 `2026-07-14-deepfake-audio-v2/03-synthesis.md`（範圍失控版）為對照。五個方向皆已通過「削減 → 雙重審查（算力鷹派 + 收斂性法官）→ 定稿」。全部滿足六條收斂規則：一個問題、三個共用同一方法的 RQ、通過「拿掉它論文還成立嗎」測試、GPU-hour 在預算內、可獨立完成、核心假設破裂仍有成篇退路。

---

## 一、砍了什麼：從第二輪到現在

### 對照表

| 方向 | 第二輪 deliverable 數 | 第二輪 GPU-h（超支倍數） | 定稿 deliverable | 定稿 GPU-h |
|---|---|---|---|---|
| **一、誠實棄權** | **12 項**（shift benchmark、7 棄權機制、density-vs-discriminative、confident-real 對抗、四維人類模型掃描、θ\* 適用域分治、年齡聽力濾波器、失效歸因診斷、硬耦合方向二/四…） | **≈5,200**（**超支 3.5–4.3×**） | 3 偵測器 × 6 棄權機制 × 12 格，收斂成**一個** shift-aware 選擇性預測 benchmark | **430–520** |
| **二、通道審計** | **22 項**（D1–D22：蜂巢電信 rig、LINE 通話/語音/Messenger/社群/混合五種通道、雙素材臂、神經模擬器蒸餾、multi-domain 5× 重訓、SynthID、C2PA 容器、SSL probing 熱圖…） | GPU **≈1,700–1,900（超支 1.3–1.6×）**；**真正死因是「日曆無界」的 rig** | 2 探針（偵測器分數、AudioSeal watermark bit）＋ 1 套差分存活協定，真實通道只錨 RTCFake | **≈510** |
| **三、攻擊成本地圖** | **11 項**（D1–D11：三類防線被動/provenance/liveness、per-sample 白盒 + oracle 搜尋、beam search、5 偵測器、全集評估、真實通道依賴…） | **≈2,200–3,000**（**超支 1.5–2.5×**） | 一套 adaptive-laundering 攻擊成本評估協定的**四個面**（greedy 搜尋一次，三種讀法） | **610** |
| **四、現場考卷** | **9 項**（詐騙語料、四象限主實驗、四因子交互、品質解耦、通道疊加、閉源 TTS 臂、S5 augmentation、守門下載、「全場共用考卷」耦合…） | GPU **≈85（不超支，僅用 6%）**；**超支的是日曆與論文邊界** | 一份語料，一個框架**讀三次**（彙總/分層/配對） | **≈180**（含 2.5× 重跑） |
| **五、Provenance/Article 50** | **13 項**（D1–D13：真實電信 rig、C2PA 容器、傳統/neural watermark、索引構造、transparency-log 分散式服務、端到端 demo、Article 50 審計、覆蓋率天花板 base-rate 建模…） | GPU **≈300–500（不超支）**；**方法論超支 2.5–3 篇、日曆超支 2.5–3×** | 一條「可靠 bit 復原」pipeline，三 RQ 是它的量測/構造/政策三種讀法 | **≈220** |

### 最常被砍掉的是哪一類東西？

**第一名，遠遠第一名：「偽裝成同一篇論文的第二、三篇論文」——任何需要換一套方法論才能回答的 RQ 或 deliverable（違反收斂規則 2）。** 五個方向無一例外都在這裡失血最多：

- **方向一**砍掉「四維人類模型掃描（δ×φ×ρ×γ）＋ 適用域分治 θ\*」——削減者判詞：「它換了方法論：從『訓練模型、跑前向、讀曲線』換成『假設人類模型族、做穩健性偏序』——這是決策理論，不是 ADD 實驗……**那是兩篇論文縫在一起，只是共用作者。**」
- **方向二**砍掉「神經通道模擬器蒸餾」——「訓練一個神經模擬器逼近真通道是**生成建模**，與『審計量測』是兩套方法論」。
- **方向三**砍掉 provenance 與 liveness 兩條防線——削減者判詞最鋒利：「provenance 要換成 C2PA 密碼學稽核、liveness 要換成 streaming VC relay rig……**砍掉它們不是損失亮點，而是本框架能自洽的前提。**」
- **方向五**是這一類的極端：削減者直接用「方法論超支」計量——「不是 GPU 超支 N 倍，而是**方法論超支 2.5–3 篇**……量測地基（訊號工程）、密碼學構造（系統工程）、政策覆蓋率（統計政策）是三套互不相通的方法論，**直接撞死收斂規則第 2 條。**」

收斂性法官對**方向二**下的是最硬的翻轉條件：若把 C2PA 容器 + Article 50 保留為與 recall 落差矩陣**並列的實驗 deliverable**，「全案從『需修正』翻為『不合格』」——這一句話直接把 C2PA/Article 50 從實驗軸降為 discussion 的一段文字解讀。

**第二名：跨方向依賴（違反規則 5）。** 幾乎每個方向都被接了臍帶：方向一硬耦合方向二（γ 通道落差）與方向四（詐騙素材）；方向三依賴方向二的 rig 與方向一的偵測器；方向四被接上方向二 rig 當「全場共用考卷」；方向五的真實 rig 直接是方向二的主軸。方向一削減者的判詞：「**把自己的畢業掛在別人的 rig 上**——收斂規則 5 明文禁止。」全部切斷，各方向改用「今天下午就能下載到」的輸入。

**第三名：算力紅線與稀釋型亮點。** ASVspoof21 DF 全集（611k）× 任何乘數、MC-dropout×全集、multi-domain 5× 重訓、per-sample 白盒搜尋、frame-level 特徵快取（18 TB）——一律抽樣到 2 萬筆或改 recipe-level。以及「拿掉論文照樣成立」的亮點：失效歸因診斷章、unseen×unseen 交叉切片、SSL probing 熱圖、10s+ 超長句層、閉源 TTS 對照臂。

**貫穿五份審查的元判詞（算力鷹派，在 D1/D2/D4/D5 反覆出現）：「在單張 4090 上，一篇 ADD 碩論的瓶頸不是 GPU-hour，是有沒有人在設計時算過乘法——而算完乘法之後，真正超載的往往不是 GPU，是一個人的日曆。」** 這解釋了為什麼方向四、五在 GPU 上從未超支（85、300–500）卻仍被大砍：它們超支的是方法論篇數與日曆工時。

### 放棄「受騙率當因變數」造成了什麼影響？

`00-constraints.md` 承認一個不相容：「不做真人實測」與「因變數必須是受騙率」無法並存，並裁定**放棄受騙率當因變數，社會價值改在 introduction 與 discussion 用文字論證**。這一刀的影響集中而深遠：

1. **它直接殺死了方向一那「另一篇論文」的半邊。** 方向一削減者點名：「#5（四維人類模型掃描）、#6（θ\* 適用域分治）、#7（年齡聽力濾波器）三項的存在理由**全部來自那個已被裁掉的因變數**。」受騙率一旦不是因變數，人類模型族、dominance 偏序、社工算子 `A_social(c)`、聽力濾波器就全部失去定義域——θ\* 本身是「人類模型參數空間裡的一個邊界」，沒有人類模型連定義域都不存在。**這一裁定正是把方向一從「兩篇論文縫在一起」變回「一個問題」的關鍵。**

2. **它替整個 cohort 卸下了「必須辯護模擬可不可信」的包袱。** 第二輪辯論的核心張力（Agent E 語）是「當使用者被拿走，全場不約而同把『人』拆成可計算的零件重新裝回管線」——素材、判斷、攻擊者、後果、通道。放棄受騙率等於承認這個縫合終究會滑向「純技術指標的自我安慰」，於是索性把因變數統一收回**機器事實**：棄權可靠性（一）、訊號存活率（二）、對抗下 recall（三）、fixed-FPR recall 落差（四）、可靠 bit 數（五）。五個因變數全是可計算、可複現、不需真人、不會過期的量。

3. **方向一因此換掉了一個 RQ（而非砍掉一個問題）。** 原「哪種棄權/警告 policy 對人較優」需要人類模型族——換成 RQ3「對抗介入下排序是否翻轉」。定稿者說得精準：「排序穩健性的問題還在，只是問的對象從**人的變異**換成**攻擊者的介入**——後者可以用同一條管線量，前者不行。」社會價值（無綠燈原則、開 pilot 的門檻證據）全部移進 discussion，用文字承載，一個字都不進實驗設計。

---

## 二、五個方向（依推薦順序）

**排序依據（依 task 指定的五個維度）**：收斂度（是不是真的一個問題）、算力可行性、novelty、真實情境意義、失敗退路的可靠度。綜合結果為 **一 → 三 → 四 → 五 → 二**。三處接近的取捨在下方各方向與比較表註明；特別是**方向二在第二輪是 co-首選，本輪定稿後因「全案繫於 RTCFake 單點故障 + Delgado 團隊已進場的搶先風險」在『失敗退路可靠度』一欄落到最後**，但它在「真實情境意義 / 監理落地」仍強，監理導向的學生應把它往前挪（見比較表註）。

---

### 推薦 #1｜原方向一：分布偏移下語音深偽偵測的選擇性預測基準

**一句話問題**
> 當語音深偽偵測器遇到訓練時沒見過的生成器與通道，它的棄權訊號還能不能可靠地認出「自己這次會答錯」？

**題目**
- 中：《不知道就別答——分布偏移下語音深偽偵測的選擇性預測基準》
- 英：*Abstain When Unsure: A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*

**三個 RQ 與貫穿的同一種方法**
核心方法是**「棄權分數函數 × shift 網格 × risk–coverage 讀數」的單一量測介面**——形式上只有三個物件：`s:x→ℝ`（任何棄權機制＝一個信心分數函數）、`g:(source,channel,adversary)→cell`（任何偏移＝網格上一格）、`R–C(s|cell)`（任何 RQ＝在同一組快取分數上讀不同切片）。工程上只有一條管線：固定 3 個 checkpoint → 每格跑一次前向 → 快取 logits + pooled embedding → 全部 6 種機制、3 個 RQ 都在這份快取上離線計算。
- **RQ1（劣化）**：generator-shift 與 channel-shift 下，各棄權訊號的判別力還剩多少（固定 FPR≤1% 的 selective recall、risk–coverage、ECE）？是否存在「偵測 AUC≈0.5 但棄權仍有效」的格？→ 沿 cell 兩軸讀邊際劣化，輸出**負領土地圖**。
- **RQ2（分岔）**：density-based（只建模 bona fide：Mahalanobis-on-SSL、energy）與 discriminative-derived（依賴 fake 端邊界：MSP、temperature、MC-dropout、deep ensemble）兩族分數，在同格是否分道揚鑣？→ 對同一組曲線做一次**分族切割**。
- **RQ3（對抗）**：攻擊者以 recipe-level laundering 或白盒擾動介入，把各棄權訊號推進 confident-real 區（`max P(confident-real|fake)`）的最低成本是多少？RQ1/RQ2 的排序在對抗欄下是否翻轉？→ 為網格加**第三根軸（adversary）**，用逐 bit 相同的介面重讀一次。
- **為何是一個框架**：三個 RQ 共用同一組物件、同一批 checkpoint、同一份快取、同一種曲線讀數；差別只在「讀哪個切片」，不在「用哪套機器」。原案裡真正換方法論的那一項（人類模型族 + θ\* 適用域分治）已整條移除。

**貢獻（3 點）**
1. 第一個 shift-aware 的 ADD 選擇性預測基準（6 機制 × 12 格，附負領土地圖）。
2. density-vs-discriminative failure-mode 的實證判決——本論文唯一的科學假說與唯一正面科學宣稱。
3. confident-real 攻擊面的形式化與量測（`max P(confident-real|fake)` + 無綠燈原則）。

**實驗規劃（GPU-hour 總計 ≈ 430–520）**
- 資料集全部公開直接下載、零申請、零 IRB：ASVspoof2019 LA（訓練）、In-the-Wild 全集、ASVspoof2021 DF / MLAAD / 19LA eval 各**分層抽 2 萬筆**（評估池 ≈ 9.2 萬筆）。
- 3 偵測器（AASIST / RawNet2 / **XLS-R 300M frozen + AASIST backend**，涵蓋 spectral-graph / raw-waveform / SSL 三族；**已砍 XLS-R full fine-tune 對照臂**）。
- 通道軸自建 3 副本：`C_clean` / `C_celp`（AMR-WB+PLR，CPU，0 GPU-h）/ `C_neural`（EnCodec，只在抽樣池）。
- 6 棄權機制：MSP、temperature、energy、Mahalanobis-on-SSL（4 種 post-hoc **共用一次前向、邊際成本 0**）＋ MC-dropout(T=10)、deep ensemble(E=3)。**已砍 FADEL evidential。**
- 對抗：recipe-level laundering beam + 白盒 PGD-50（僅可微路徑）。**已砍黑盒 sanity 臂。**
- 結帳單（含差異化重跑係數）：訓練 68 + 前處理 42 + 評估 100 + 對抗 165 + 消融 20 ≈ **430–520 GPU-h**。全套悲觀重跑仍剩約 50% 空間。**日曆是唯一瓶頸**（27–38 人週 vs 24–30 供給，貼合低端）。

**一年時程**
- Q1（1–3，修課重）：復現 3 偵測器 + 建評估池 + 3 通道副本 + **「一次前向→快取 logits+pooled embedding」評估骨架**（全篇基礎設施）。
- Q2（4–6）：**RQ1**，6 機制 × 12 格 risk–coverage/ECE/負領土地圖 → **★保底半篇 benchmark，可投 INTERSPEECH**。
- Q3（7–9）：RQ2（density-vs-discriminative 判決）+ RQ3 上半（laundering beam）。
- Q4（10–12）：RQ3 下半（白盒 PGD + 無綠燈 invariant）+ 消融 + 寫作。

**失敗退路**：三個 RQ 的 null 各自可發表。主假設全滅（所有棄權訊號在 AUC≈0.5 格退化成隨機）→ 轉「選擇性預測在 ADD 上的嚴謹否證 + confident-real 攻擊面 taxonomy」（先例：VoiceWukong 高品質負面結果進 USENIX Security 2025），且 Q2 benchmark 已獨立成篇。RQ3 兩邊都能寫（打得動＝對部署方警告、打不動＝正面部署證據），**無失敗模式**。無任何退路需要新方法論、新資料或新的一年。

**社會意義（文字論證）**：偵測器最危險的失效不是漏抓，是自信地說「這是真人」——替攻擊者背書。本論文把它變成可量測的 `max P(confident-real|fake)` 與可檢查的**無綠燈原則**（系統只有「警示」與「沉默」兩態，沉默不是背書）。它不宣稱救得了任何人並明說這件事；量的是**機器的自知之明**。社會用途是「開 pilot 的門檻證據」——比一個 EER 0.06% 卻在一次 neural codec transcode 後崩到 40% 的排行榜數字有用得多。

**明確不做什麼**：XLS-R full fine-tune、FADEL evidential、黑盒 sanity 攻擊、四維人類模型掃描、θ\* 適用域分治、年齡聽力濾波器、失效歸因診斷章、閉源 TTS 自建、硬耦合方向二/四、VoiceWukong per-sample Zenodo 申請（全部 → future work）。

---

### 推薦 #2｜原方向三：被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖

**一句話問題**
> 對一個被動語音深偽偵測器，攻擊者讓它失效最便宜要付多少，其中多少是防守方永遠追不回的？

**題目**
- 中：《攻擊者付的絕不超過多少——被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖》
- 英：*What Does the Attacker Pay at Most? An Attacker-Cost Upper-Bound Map of Adaptive Laundering against Passive Audio Deepfake Detection*

**三個 RQ 與貫穿的同一種方法**
核心方法是**一套 adaptive-laundering 攻擊成本評估協定**：固定一組公開偵測器與一個離線 laundering 動作空間，對每個偵測器跑一次 **recipe-level 貪婪（greedy）搜尋**（depth≤3、動作空間≤8），三個 RQ 是**同一次計算的三種讀法**。
- **RQ1（成本上界）**：讓固定 FPR≤1% 的 recall 跌破可用門檻的最便宜配方是什麼？→ greedy 搜尋的**終點**。
- **RQ2（可逆性下界）**：這條配方裡哪些是可逆分佈偏移（channel-aware DA 追得回，如傳統 CELP），哪些踩到不可逆資訊摧毀下界（neural codec transcode 的 many-to-one 投影）？→ 對同一條配方逐步套用**資訊理論可控植入標註**。
- **RQ3（懸崖/緩坡）**：攻擊成本-recall 曲線是懸崖（防守方有戲）還是緩坡（在裸奔）？哪些設計讓曲線變陡？→ 同一次搜尋的**軌跡形狀**。
- **為何是一個框架**：終點=上界、對軌跡每步標可逆性=下界分解、整條軌跡形狀=曲線幾何，讀的是同一次計算的三種面。被砍的 provenance（換 C2PA 密碼學）與 liveness（換 streaming VC rig）正是會讓 RQ 之間換方法論的東西——砍掉是本框架能自洽的**前提**。

**貢獻（3 點）**
1. 把 audio ADD 的 laundering 從「防禦者視角的隨機後處理」形式化為「攻擊者視角的 recipe-level greedy 搜尋」，輸出攻擊成本**上界**（真實成本 ≤ 此值）——「攻擊成本」這個評估軸在 audio ADD 文獻中此前不存在。
2. 用可控植入實驗給每個動作標物理可逆性下界，把 neural codec transcode 認證為「零金錢、一行指令、物理不可逆」的必殺動作——**不隨生成器版本過期的資訊理論錨**。
3. 懸崖 vs 緩坡的偵測器幾何地圖，作為部署方的「照妖鏡」與後續防禦研究的標準壓力測試。

**實驗規劃（GPU-hour 總計 610）**
- 資料集全部公開、全程離線免 rig 免 IRB：ASVspoof2019 LA / 2021 DF（**抽 20k 確認池、10k 搜尋池**）、In-the-Wild、MLAAD。
- 偵測器：AASIST + RawNet2 + wav2vec2-XLS-R backend + **自建 Mahalanobis-on-SSL baseline**（4 個，支撐 RQ3 的 SSL vs 手工特徵比較；**已從 5 砍到 4**）。
- 動作空間 ≤8 個 ffmpeg-native / HF 開源動作（**已砍需編譯專利碼的 EVS/AMR-WB**）。
- 結帳單：偵測器復現 40 + baseline 對照 40 + laundering 前處理 60 + 可控植入 45 + greedy 搜尋前向 130 + tandem 轉檔 90 + 消融 65 + 30% 緩衝 140 = **610 GPU-h**，真餘裕 ~40%。三刀削減：**砍白盒 PGD 驗證整段、beam→greedy、5→4 偵測器**（另據實補回 tandem 轉檔、緩衝 15%→30%）。

**一年時程**
- Q1（1–3）：復現 4 偵測器 + 建抽樣池 + 定義動作空間與成本代理 + baseline 平均劣化對照 → **保底 1：攻擊面地基 +「最壞情況嚴格重於平均」**。
- Q2（4–6）：物理可逆性可控植入 + neural codec 資訊摧毀圖譜 → **保底 2：可逆性圖譜可獨立成篇**。
- Q3（7–9）：recipe-level greedy 攻擊成本上界搜尋（RQ1）+ 攻擊成本-recall 曲線與懸崖/緩坡（RQ3）。
- Q4（10–12）：三項消融 + 跨偵測器地圖整合 + 負責任發布（只發配方與 checksum）+ 寫作。

**失敗退路**：成本代理不可辯護 → 主承載退到物理可逆性下界（資訊理論事實，不需人、不過期），骨幹改「可逆 vs 不可逆動作地圖」，更硬。全是緩坡 → 對部署方的直接警告（現行被動偵測全在裸奔），可發表負面結論。neural codec 竟可逆 → 對「不可逆必殺動作」的否證，同樣可發表。Q1、Q2 各為可獨立發表單元。

**社會意義（文字論證）**：防止機構部署製造虛假安全感的偵測器。因變數自始至終是機器事實（對抗 laundering 下的 recall）。定位對受害者誠實且有限——**不是「救她」，是「少害她」**，確保沒有機構拿一個一戳就破的東西當她的防線。

**明確不做什麼**：白盒 PGD 驗證、per-sample 白盒 + oracle 搜尋、beam search(width>1)、第 5 個偵測器、provenance/liveness 維度、接方向二真實通道、EVS/AMR-WB（全部 → future work）。

---

### 推薦 #3｜原方向四：詐騙現場條件下語音深偽偵測的評估效度審計（繁中）

**一句話問題**
> 現行語音深偽偵測 benchmark 用朗讀長句量出的偵測率，對「詐騙現場實際到達受害者耳朵的三秒音訊」系統性高估了多少、高估來自哪個條件軸？

**題目**
- 中：《到達耳朵的那三秒：詐騙現場條件下語音深偽偵測的評估效度審計》
- 英：*The Three Seconds That Reach the Ear: An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scene Conditions*

**三個 RQ 與貫穿的同一種方法**
核心方法是**受控析因的評估落差量測**：在一份「多軸分層 × 品質協變量標註」的自建詐騙現場語料上，量現成 **frozen** 偵測器的 fixed-FPR(≤1%) recall，用同一批前向做因子分解與品質配對（全程零訓練、零人工聽測）。
- **RQ1（總量）**：標準素材→詐騙現場素材，recall 落差多大？→ 兩 cell 相減（**邊際彙總**）。
- **RQ2（分解）**：話術語意、短句長、情緒韻律、通道各軸主效應與**交互效應**多大（前作全單軸，交互無人量）？→ 對同一批 recall 做**析因切片**。
- **RQ3（效度）**：這落差多少是「偵測器對現場失效」而非「情緒/短句 TTS 品質差被抓」？品質配對後淨落差剩多少？→ UTMOS + speaker similarity **協變量配對**。
- **為何是一個框架**：三個 RQ 共用同一份語料、同一批 frozen 前向、同一個 fixed-FPR recall——差別只在「彙總/分層/配對」三種讀法，沒有任何 RQ 變成訓練新模型或建人類模型。

**貢獻（3 點）**
1. 第一份詐騙現場條件的**繁中** ADD 測試語料（可重現配方，非直接散布合成詐騙語音）——填素材生態效度的正交空白。
2. 量化「素材真實性樂觀偏差」及其多因子（含交互）分解，其中「話術語意/語用是否讓 TTS 露餡」是單軸前作全未觸及的自變數（與「多軸交互項」構成雙錨）。
3. 一個可審計的品質配對協定，把「偵測器對現場失效」與「現場 TTS 品質較差」解耦。

**實驗規劃（GPU-hour 總計 ≈ 180，含 2.5× 重跑）**
- 話術腳本：~165 條刑事局/反詐公開話術 → 去識別化改寫成受控刺激 + 配對中性文本對照臂。
- fake：**純 2 家開源情緒可控 TTS/VC**（情緒 3 層 × 句長 2 層 + 標準長句對照；**已砍閉源臂**，品質天花板改用 UTMOS 連續協變量）。
- 偵測器：AASIST + wav2vec2-XLS-R backend（SSL-AASIST 公開權重），**退路降 2 套（AASIST+RawNet2）不自己重訓**。
- 通道：offline codec 自足，不接任何 rig。品質協變量：UTMOS + ECAPA speaker similarity（機器計算）。
- 結帳單：S0 feasibility 8 + 生成 75 + 通道 25 + 品質標註 18 + 主實驗析因 22 + 緩衝 25 ≈ **180**（悲觀含條件重訓 ~190–315），用不到上限 19%。**算力是全場最寬鬆的；瓶頸是日曆（砍後 21–33 人週）與情緒 zh-TW TTS 取得性。**

**一年時程**
- 月 0–1：feasibility spike + **情緒 zh-TW TTS 硬 go/no-go 關卡**（不可用即切 crash-path B 三軸析因，不拖到月 8）+ 確認 XLS-R backend checkpoint 可得性。
- 月 2–4：語料建構（生成 + 通道 + 品質標註）→ **保底：一份可重現的詐騙現場 ADD 語料**。
- 月 5–7：主實驗（RQ1 落差矩陣）→ **半篇 audit**。
- 月 8–10：多因子析因 + 品質解耦（RQ2、RQ3）。
- 月 10–12：輕量發布（配方 + checksum，**不散布合成詐騙語音本體**）+ 寫作。

**失敗退路**：落差很小（H0）→「現行 benchmark 對詐騙場景的代表性驗證」，可發表否證。話術語意軸無效或情緒 TTS 月 1 不可用 → crash-path B 三軸析因（樣本層檢定力足，主效應由單軸前作幾乎保證存在）。XLS-R 取不到 → 降 2 套偵測器。**核心假設（現場素材≠標準素材）幾乎不可能全滅**——in-domain vs out-of-domain、壓縮通道劣化已有文獻。月 4 有自足語料、月 7 有半篇 audit。

**社會意義（文字論證）**：評估誠實性。今天廠商宣稱「能防詐」的成績單幾乎都來自十秒朗讀句、中性韻律、錄音棚素材；真正到達受害者耳朵的是三秒哭腔、一句急迫命令、走過電話通道的話術。「以後宣稱能防詐的偵測器，得先過『到達耳朵的那三秒』這關。」

**明確不做什麼**：S5 scam-scene augmentation 微調（一拉回即違反規則 2）、閉源 TTS 品質天花板臂、散布合成詐騙語音本體 + 守門下載後端、接方向二 rig / 「全場共用考卷」耦合、10s+ 超長句層、第三偵測器自行重訓（全部 → future work）。

---

### 推薦 #4｜原方向五：詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

**一句話問題**
> 在詐騙實際發生的音訊通道上，watermark provenance 標記還剩幾個可靠 bit，這個數字夠不夠讓 EU AI Act Article 50 要求的「機器可讀標記」真的被讀出來？

**題目**
- 中：《還剩幾個 bit——詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計：一份 EU AI Act Article 50 可讀性判決》
- 英：*How Many Bits Are Left? A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels — an EU AI Act Article 50 Readability Verdict*

**三個 RQ 與貫穿的同一種方法**
核心方法是**唯一一條「可靠 bit 復原」pipeline**：`embed(已知 k-bit / watermark) → 通道條件 transcode → recover → 用可控植入校準後數可靠 bit`（可靠 bit 用可控植入取 ground truth，避開高維互資訊估計的不可靠）。
- **RQ1（容量地圖）**：各 watermark 家族在 codec / neural-codec 通道矩陣上的可靠 bit 容量各多少？可逆（傳統 CELP）與不可逆（neural codec）之間的**容量塌陷點**在哪？→ 逐格跑 pipeline，bit 存活率**就是**容量地圖。
- **RQ2（構造生死）**：在 RQ1 容量上限內，「索引不 payload」的 soft-binding 構造（碼率 ≤ 實測容量的 ECC 索引 + 本地簽章承諾表）能否**單機**端到端存活？k 在哪個通道歸零？→ 用同一條 pipeline 驗證，k 的生死直接讀 RQ1 曲線。
- **RQ3（Article 50 判定）**：把 bit 數字對照兩階操作型門檻（detection-readable / provenance-readable，門檻錨在偵測器 ROC 工作點與登錄簿規模），逐通道判可讀/不可讀。→ 拿前兩 RQ 的**同一組 bit 數字**對法律宣判，零新 pipeline。
- **為何是一個框架**：曾經需要換方法的三塊——真實電信 rig（訊號工程）、分散式 transparency-log（系統工程）、覆蓋率 base-rate 建模（統計政策）——已全部砍出實驗，留下唯一一條 pipeline 的三種讀法。

**貢獻（3 點）**
1. 第一張 watermark provenance 可靠 bit 容量地圖（橫跨傳統與 neural codec 通道，附可控植入 ground-truth 錨，指認可逆/不可逆塌陷點）。
2. 「索引不 payload」soft-binding 構造的容量生死判定——正面工程貢獻，不是純批評。
3. 第一份 EU AI Act Article 50 音訊可讀性審計（2026-08-02 生效，零前作）。

**實驗規劃（GPU-hour 總計 ≈ 220）**
- 載體語音**分層抽 ~10k 池**（AISHELL-3 + LibriSpeech + ASVspoof19/In-the-Wild real）。
- watermark：AudioSeal + WavMark + SilentCipher（皆開源 learned watermark；**已誠實收窄，不硬撐「傳統 vs neural 分類學」、不自刻 echo-hiding**；SynthID 非全開源不納入）。
- 通道：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC，CPU）× Gilbert-Elliott PLR；neural codec（EnCodec/DAC/SpeechTokenizer）× bitrate（**neural 通道只掃 bitrate 不掃 PLR**——物理界線）。**已砍 C2PA 容器層、EVS 3GPP 編譯。**
- 結帳單：neural transcode 32 + embed/recover 15 + 可控植入多 seed 90 + 索引構造驗證 10 + 1.5× 緩衝 73 = **~220 GPU-h**（用不到上限 18%）。**算力從來不是瓶頸，工具鏈成熟度才是。**

**一年時程**
- 月 0：watermark 工具鏈 feasibility spike（無需法律送件）。
- 月 1–3：可控植入 bit-survival pipeline + 傳統 codec 通道 → **保底：可獨立發表的量測單元**。
- 月 4–6：擴 neural codec → 完成 RQ1 容量地圖 + 可逆性邊界。**月 6 檢查點**：RQ1 已足以成篇。
- 月 7–9：RQ2 索引構造（ECC + 單機驗證迴路）+ 消融。**月 8 逃生閥**：RQ2 做不出即降 future work，論文以 RQ1+RQ3 成篇。
- 月 10–12：RQ3 Article 50 審計對照表 + 覆蓋率天花板文字論證 + 寫作。

**失敗退路（反脆弱）**：所有 bit 在最溫和 codec 就歸零 → **政策級否證**（Article 50 要求的機器可讀標記在真實通道根本不可讀），**核心假設越不成立，政策發現越硬**。工具鏈崩 → 退單一 AudioSeal × 完整通道矩陣。RQ2 構造崩（月 8 逃生閥）→ 純容量審計 + Article 50 判定。月 1–3 量測單元在任何崩法下保底。

**社會意義（文字論證）**：provenance 服務「真話自證」不是「假話攔截」——誠實邊界寫在第一頁：對即時詐騙電話救不了，定義域是非即時的語音訊息/媒體檔案/權威來源（服務上班族、選民）。覆蓋率天花板（純文字論證）用公開 165 統計算出「provenance 就算完美，可觸及受害者比例的上限」，是給金管會與 165 的政策級洞察。

**明確不做什麼**：真實蜂巢電信 rig、C2PA 容器層 + audio profile 建議、EVS 編譯、自刻 echo-hiding、分散式 transparency-log 服務、跨平台端到端 demo、覆蓋率天花板量化地圖（移文字論證）、SynthID 實測（全部 → future work）。

---

### 推薦 #5｜原方向二：真實通道上音訊深偽反制訊號的樂觀偏差審計

> 註：第二輪 co-首選。本輪定稿後，因**全案繫於 RTCFake 這個現成資料集的月 0 go/no-go 單點故障**，加上 Delgado 團隊（ASVspoof 組織者）與產業已進場的搶先時間窗，在「失敗退路可靠度」與「被搶先風險」兩項落到最後——但它在「真實情境意義 / 監理落地」仍是強項。**能取得真實通道資料、且以監理審計為志向的工程型學生，應把它往前挪到 #2。**

**一句話問題**
> 離線模擬 codec 相對於可得的真實通道，對音訊 deepfake 反制訊號的存活造成多大的樂觀偏差，而這偏差來自通道的哪一層畸變？

**題目**
- 中：《模擬騙了我們多少——真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》
- 英：*How Much Does Simulation Flatter Us? The Optimism Bias in Audio Deepfake Countermeasure-Signal Survival over Real Channels, and Its Distortion-Layer Attribution*

**三個 RQ 與貫穿的同一種方法**
核心方法是**一台「通道存活審計台」**：建一組固定通道管線當受試環境，把不同波形域反制訊號當探針灌進去，用統一 fixed-FPR 差分存活協定量「真實通道存活 − 模擬通道存活」的落差 γ。受試環境三個 RQ 皆同：{Opus/AMR-WB × bitrate × PLR} ∪ {RTCFake}，另設 C0' 重放對照臂讓通道 artifact 成共有常數項。
- **RQ1（被動探針）**：偵測器分數當探針、recall 當存活指標，模擬 vs RTCFake 的 recall 落差 → 樂觀偏差 γ。
- **RQ2（主動探針）**：探針換成 **AudioSeal watermark bit**，同一組通道同一組樣本同一套記帳灌一次。→ 不換管線、不換方法論、不換資料型態。
- **RQ3（歸因）**：同一台上做**逐因子落差分解**（丟包/jitter/DSP 逐項從真實側加回模擬側）+ 單一 channel-conditioned DA 對照判定該層是否救得回。
- **為何是一個框架**：三 RQ 因變數都是「同一台審計台上 fixed-FPR 下的真實−模擬差分存活」，只是換探針或拆因子。被砍的（神經模擬器蒸餾、multi-domain 重訓、C2PA 容器、Article 50 法律解讀）正是會換方法論的東西。

**貢獻（3 點）**
1. 第一份可得真實通道上、跨被動偵測器與主動 watermark 的存活審計，輸出樂觀偏差係數 γ（供其他 ADD 研究當「通道折扣」直接消費）。
2. AudioSeal watermark bit 在真實通道存活多少的實測（零前作：AudioMarkBench 只做模擬擾動，通道前作沒碰 watermark）；若電話級通道 bit 全滅，於 discussion 對 Article 50 提實測否證。
3. 樂觀偏差的畸變層歸因（指認 γ 來自 codec 重合成 / 丟包 / 端點 DSP 哪一層，該層 DA 是否救得回）。

**實驗規劃（GPU-hour 總計 ≈ 510）**
- 資料集皆可得：bona fide 用公開 real 類 + 3 家開源 TTS fake，**分層抽 2 萬筆**（不碰 611k 全集）；真實通道錨 **RTCFake（單點故障，月 0 第一天驗）**；watermark 用 **AudioSeal 單一**（**已砍 SynthID**——非第三方可用）。
- 偵測器：AASIST + wav2vec2-XLS-R + RawNet2 現成 checkpoint。模擬臂 Opus + AMR-WB 現成 library（**已砍 EVS 3GPP 編譯、砍 LINE 語音訊息 rig**）。
- 結帳單（含鷹派全部修正係數：條件數 ~30、DA 當一次真實 fine-tune、buffer 50%）：TTS 35 + 模擬 codec 10 + 特徵快取 45 + RQ1 評估 45 + RQ2 bit 35 + RQ3 落差分解 70 + DA 對照 100 + 50% 緩衝 170 = **~510 GPU-h**（約半個上限）。**GPU 不是瓶頸，日曆與 RTCFake 是。**（**已砍 C2PA + Article 50 實驗軸、SSL probing 熱圖、unseen×unseen 交叉切片、可控植入、neural codec 可逆性、multi-domain 重訓。**）

**一年時程**
- **月 0（go/no-go 閘）：第一天先驗 RTCFake**（授權可否學術重散布、是否含 real+fake 配對、標記是否足以做 fixed-FPR）——全案單點故障。
- Q1（1–3）：搭審計台 + 三偵測器復現 + TTS fake + C0' 對照臂 → **保底：模擬 codec 階梯偵測器存活 benchmark（零 rig 零真實通道依賴）**。
- Q2（4–6）：RQ1 主體（模擬 vs RTCFake 差分矩陣 → γ）+ RQ2 AudioSeal bit 存活 → **MVP 可發表單元**。
- Q3（7–9）：RQ3 逐因子落差分解 + channel-conditioned DA 對照 + 消融。
- Q4（10–12）：Article 50 討論章（文字）+ 開源審計台 + 寫作。

**失敗退路**：RTCFake 月 0 不過關（最需防的單點故障）→ 退「模擬 codec 階梯上的跨被動偵測器 + AudioSeal 存活 benchmark」，γ 改為模擬階梯內部衰減率，零真實通道依賴仍成篇。γ≈1（模擬其實夠好，H0）→ 可發表否證（替社群省下自建真實通道成本）。AudioSeal bit 真實通道全滅 → RQ2 最強結果（Article 50 政策否證）。Q1 模擬 benchmark 在任何分支保底半篇。

**社會意義（文字論證）**：不直接攔詐騙，是**上游證據基礎**（決定平台/電信端該部署什麼、165 該信什麼）。獨立第三方審計填補「產業系統全閉源、零第三方評測」的消費者知情權空白；Article 50 政策否證（discussion）；告訴防禦方哪層 DA 救得回、哪層別浪費算力。

**明確不做什麼**：自建蜂巢電信 rig、LINE/Messenger/社群/混合通道 rig、SynthID、C2PA 容器 + Article 50 實驗軸、可控植入 + neural codec 可逆性邊界、SSL probing 熱圖、unseen×unseen 完整交叉、神經模擬器蒸餾、multi-domain 5× 重訓、全集 611k 評估、EVS 編譯、閉源 TTS API、方向四詐騙素材依賴（全部 → future work）。

---

## 三、五方向比較表

| 方向（推薦序） | 一句話問題 | 核心方法 | GPU-h | novelty | 收斂度 | 失敗風險 | 適合什麼樣的學生 |
|---|---|---|---|---|---|---|---|
| **#1 誠實棄權（原一）** | 偵測器遇到沒見過的生成器與通道，棄權訊號還能不能可靠認出「自己會答錯」？ | 棄權分數 × shift 網格 × risk–coverage 單一量測介面，3 RQ = 3 種切片 | 430–520 | ★★★★ | ★★★★☆ | 低-中：每個 RQ null 可發表、Q2 保底半篇；唯一軟肋是日曆最緊（27–38 人週） | **建模型 / 方法論型**，紀律好、Q1 就把快取骨架做對的人 |
| **#2 攻擊成本（原三）** | 攻擊者讓被動偵測器失效最便宜付多少、多少是永遠追不回的？ | 一次 recipe-level greedy 搜尋，終點=上界、標可逆性=下界、軌跡=曲線幾何 | 610 | ★★★★ | ★★★★★ | 低：物理可逆性下界是不過期的資訊理論錨；緩坡也是可發表結論 | **紅隊 / 對抗評估型**，喜歡攻防思維、能寫乾淨搜尋碼 |
| **#3 現場考卷（原四）** | 朗讀長句量出的偵測率，對「到達耳朵的三秒」高估多少、來自哪個軸？ | 一份語料 × frozen 前向 × fixed-FPR recall，讀三次（彙總/分層/配對） | ≈180 | ★★★☆ | ★★★★☆ | **最低**：核心假設幾乎不可能全滅、月 4 保底語料；風險在情緒 zh-TW TTS 取得 | **實證 / 資源建構型**，細心做語料標註、耐得住繁瑣的人 |
| **#4 Provenance（原五）** | watermark 過詐騙通道還剩幾個可靠 bit，夠不夠讓 Article 50 標記被讀出？ | 一條 embed→通道→recover→可控植入校準的 bit 復原 pipeline，量測/構造/政策三讀法 | ≈220 | ★★★☆ | ★★★★ | 低-中（反脆弱）：假設越崩政策發現越硬；風險在 watermark 工具鏈成熟度 | **crypto / 政策型**，對 EU AI Act、ECC 編碼、法規審計有興趣的人 |
| **#5 通道審計（原二）** | 模擬 codec 相對真實通道，對反制訊號存活造成多大樂觀偏差、來自哪層畸變？ | 一台通道存活審計台，換探針/拆因子量真實−模擬差分存活 γ | ≈510 | ★★★☆ | ★★★★ | **中-高**：全案繫於 RTCFake 月 0 go/no-go 單點故障 + Delgado 已進場搶先風險 | **工程 / 實測型**，能搞定資料授權與通道 pipeline、以監理審計為志向的人 |

> **比較表註**：novelty/收斂度為統整者依定稿內容評分（非第二輪 H 的原始分）。**#5（原方向二）在「真實情境意義 / 監理落地」高於 #3、#4**（它是唯一能直接放上監理機關桌面的實測審計），因失敗退路可靠度與搶先風險落到推薦末位；志在監理、且能落實 RTCFake 或其他真實通道資料的學生，應把它視為與 #1 並列的 co-首選——這正是第二輪的定位。

---

## 四、給作者的建議

### 如果只能選一個：選 #1（誠實棄權選擇性預測基準）

**為什麼**：它是這場辯論裡被 A、D、E、F、H 五個角色在最終推薦中列為推薦一或 co-首選的方向，三個把關角色罕見一致——紅隊 D **主動推薦一個防禦方案**（「全場唯一不給攻擊者背書的防禦，它沒有在擋不住的地方發出確定的綠燈」）、民眾 F 判它是阿嬤那行唯一有「可以」、上班族情境直接「可以」的方向、教授 H 列 co-首選。定稿後它同時最硬地滿足全部硬約束：**收斂度高**（θ\* 決策理論瘤已切除，如今是一個真正的單一量測介面）、**算力有 ~50% 餘裕**（430–520）、**novelty 不隨生成器版本過期**（robust decision framing + shift-aware selective prediction 無前作）、**真實情境意義全場最高**（無綠燈原則直接對抗「侵蝕信任」）、**失敗退路最可靠**（三個 RQ 的 null 各自可發表，Q2 保底半篇 benchmark 不依賴任何後續假設）。唯一的軟肋是日曆最緊，但那已靠「砍 full-FT + evidential + 黑盒」三刀壓進可完成區間。

### 第一週先做什麼（具體到可以馬上動手）

定稿的關鍵決策是「**frozen-only + 全年零外部申請**」——所以第一週不送任何 Zenodo 申請（那是已死的人類模型的燃料），而是純下載 + 跑 baseline + 驗一個假設：

1. **下載資料集（今天下午就能做）**：ASVspoof2019 LA（Edinburgh DataShare，直接下載）+ **In-the-Wild 全集**（Fraunhofer AISEC，request form 提早送、留 1 週緩衝）。In-the-Wild 只有 31,779 筆、37.9 h，全集跑一次前向只要 ~10 分鐘——它是第一週最理想的 smoke-test 場地。
2. **跑 baseline（下載完當天）**：抓 **AASIST 官方 repo + ASVspoof2019 LA checkpoint**，在 In-the-Wild 全集上跑一次前向，確認能復現論文附近的 EER（這是「偵測器復現對不對」的第一個檢查點）。
3. **搭最小快取骨架（第一週的真正產出）**：把這次前向改寫成「一次前向 → 快取 logits + pooled embedding（全 25 層 pooled，非 frame-level）」——這是整篇論文的基礎設施，第一週把介面定對，後面全是離線 numpy 計算。
4. **驗核心假設（第一週就能得到 yes/no 訊號）**：在 In-the-Wild（對 ASVspoof 訓練的模型而言就是 unseen-generator shift）上，算 MSP / energy 這兩個 post-hoc 分數，檢查**偵測器答錯的樣本，其信心分數是否系統性低於答對的樣本**。這是 RQ1 核心假設（「至少某些棄權訊號在 shift 下仍保有判別力」）的最小可證偽測試——如果連在 In-the-Wild 上都完全失效，就提早知道要走失敗退路（轉「嚴謹否證 + confident-real 攻擊面 taxonomy」），而不是等到第八個月。

一週結束時，作者手上會有：可復現的 AASIST baseline、一個能吐 pooled 特徵快取的骨架、以及「棄權訊號在真實 unseen 資料上到底有沒有訊號」的第一個實證答案。

### 誠實指出兩件事

**哪一個的 novelty 最禁得起兩年後回頭看：#2（攻擊成本地圖）。** 它的承重錨是**資訊理論可控植入的物理可逆性下界**——「neural codec transcode 的 many-to-one 投影是永久失效」是資訊物理事實，不隨生成器版本、不隨月份過期（削減者、Agent C、Agent D 三方都認證這一點）。兩年後 ASVspoof 出到 2027、生成器換了三代，「攻擊成本上界 + 可逆/不可逆分解」這個評估軸與它的物理下界仍然成立，而且「攻擊成本」這個軸在 audio ADD 文獻裡此前根本不存在。次穩的是 #1 的 robust-decision framing（G 認證「不隨生成器版本過期」）。相對地，最吃「當期 SOTA 偵測器數字」的是 #5 的 γ 係數——它是對「今天這批模型 + 今天的 RTCFake」的量測，兩年後需要重測。

**哪一個最可能被別人搶先：#5（通道審計，原方向二）。** 這不是猜測，是紀錄裡白紙黑字的時間窗警報——史官 G 指出「首個真實通道」的錨已被 arXiv 2509.26471（Presentation，作者 Delgado 正是 ASVspoof 組織者）與 RTCFake 侵蝕，並下結論「**Delgado 團隊與產業已進場，再放一年就沒了**，MVP 必須前置到月 6」。真實通道 × watermark 存活是產業與 ASVspoof 核心圈都看得到的下一步，一個碩士生用一年去賽跑風險最高。次高的是 #3（現場考卷）——短句/情緒 ADD 已有五篇單軸前作（AASIST2、Fake-Mamba、HuLA…），「詐騙話術語意 + 四軸交互」是明顯的下一格，雖然目前無人做，但護城河窄。相對安全的是 #1 與 #2：#1 的無綠燈原則 + shift-aware selective prediction、#2 的攻擊成本軸，都是「換個問法」而非「搶同一個資料集」，被正面撞題的機率較低。

---

*本統整完成於 2026-07-14，以 `00-constraints.md` 六條收斂規則為最高裁決標準。五個方向皆為一位碩士生、一年、一張 RTX 4090（24GB）、不做真人實測、不需 IRB 之下，解決一個問題、有三個共用同一方法的 RQ、附 GPU-hour 粗估（全部在 1,200–1,500 預算內）、可獨立完成、核心假設破裂仍可成篇的碩士論文題目。*
