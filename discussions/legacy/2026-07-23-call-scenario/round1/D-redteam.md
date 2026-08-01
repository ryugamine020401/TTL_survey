# D-redteam 紅隊席 — 來電場景版研究問題攻擊面掃描

日期：2026-07-23
席位：D-redteam（Formalize 波，收 Gate 三判後發言）
判準：沿用「不給攻擊者背書」——任何在攻擊者手上會退化成綠燈機的 policy 一律否決。

---

## 立場摘要（≤5 行）

1. 場景不 kill，但「來電」相對 proposal-final 引入一個**質變的攻擊面**：攻擊者是活人在線、可即時適應，且 streaming VC 的 SOTA 延遲已低到能真人接手後無縫切換。
2. 候選 RQ 最致命的漏洞是「commit 後不再監聽」——若「未發現合成證據」是**吸收態（停止聽）**，攻擊者只要撐過前綴就取得**永久綠燈**，這是直接的背書失敗。
3. 三種來電特有攻擊（真人開場後切 VC、刻意短句讓前綴永遠不夠、壓噪誘發棄權疲勞）中，**前兩者可用 recipe-level 離線拼接模擬納入實驗且不爆範圍**；棄權疲勞是人因，只能進 threat model 文字。
4. Gate 改錨選項裡，「語音訊息事後分析」法律最乾淨但**抽掉了 anytime 早停的對抗動機**，等於自廢 RQ 核心；視訊會議保留活人攻擊面。
5. anytime 保證必須是「整通全程連續」，不是「首次 commit」，否則統計 estimand 對 mid-stream 切換無效。

---

## 主體分析

### A. streaming VC 現況：真人接手後切換是可執行威脅，不是科幻

**Verified**：Google StreamVC 一次推論處理 20ms、3-frame/60ms lookahead、Pixel 7 上約 10ms 推論延遲、端到端約 70ms（google-research.github.io/seanet/stream_vc poster；arXiv:2401.03078，查證 2026-07-23）。ITU 類建議互動語音單向延遲 < 150ms（fish.audio 2026 綜述，查證 2026-07-23）。**Verified**：零 lookahead 串流 VC（Zero-VC，arXiv:2606.20218）與 CPU 上即時 VC（arXiv:2311.00873）已出現，門檻持續下降。

**Inference**：端到端 < 150ms 且可跑在手機/CPU，意味攻擊者能在**同一通電話內**先用真人聲音應答數秒（讓偵測器在乾淨前綴上 commit 成「未發現」），再切到即時 VC 或預錄深偽。這使「聽到第幾秒才判定」的前綴假設出現一個**真實標籤會在串流中途改變**的病態：前綴是真人、後綴是合成，`prefix → label` 不再是良定義的映射。

**Verified**：詐騙產業已把即時語音克隆包裝成「Scam-as-a-Service」套件，非技術犯罪者也能大規模執行（group-ib.com/blog/voice-deepfake-scams；cnbc.com 2026-05-09，查證 2026-07-23）。攻擊者具動機與工具去適應任何公開的偵測 policy。

### B. 候選 policy 何時退化成綠燈機（背書判準核心）

**Hypothesis → 設計級否決**：anytime 三態在以下設計下必然退化：

1. **「未發現/clean」被設為吸收停止態**：一旦 commit 就停止監聽。攻擊者用乾淨前綴騙過即停，之後隨意切 VC → **永久綠燈**。這是最嚴重的背書。**修正要求**：唯一允許吸收停止的是「發現合成證據」；「未發現」必須是**非吸收態——持續聽到掛斷**。proposal-final 已寫「未發現 ≠ 已驗證真人」，但在串流下必須把它強化為「未發現亦不停止監聽」，否則語意警告救不了行為漏洞。

2. **棄權零成本且無承接動作**：持續棄權 = 靜默放行。攻擊者壓低音量/加背景噪音把 SNR 拉到偵測器持續棄權 → 使用者疲勞後自行接受（棄權疲勞＝實質綠燈）。**修正要求**：沿用 proposal-final 的 coverage 下限 + UCB 聯合約束，且棄權必須綁定升級動作（回撥已知號碼、帶外查證）。

3. **commit 為每通一次性而非連續重評**：單次早判被 mid-stream 切換直接擊穿。**修正要求**：估計對象改為「整通全程的 any-time 偵測」——只要任一時窗出現合成證據即判 spoof，這與 G 席「錨在 commit-time 統計判定」一致。

### C. 哪些攻擊可離線 recipe 模擬（不爆範圍）、哪些只能寫 threat model

**繼承硬約束**：不做真人實測、不做 adaptive/最佳化攻擊實驗。判別線＝「是否需要把部署 policy 放進最佳化迴圈或需要人類受試」。

**可 recipe-level 離線納入實驗（靜態資料工序，非 adaptive attack）**：
- **真人開場後切 VC**：把 bona-fide 前綴與 spoof 後綴**離線拼接**成 splice 串流，量測 policy 在切換點後多久才翻成 spoof、以及在切換前是否已 commit 成 clean。這直接壓測 anytime estimand，且只是資料增強，無最佳化迴圈。〔Hypothesis，屬 C-signal / S-sequential 可執行範圍〕
- **刻意短句**：以截斷前綴分佈（模擬短輪次）評估 coverage 崩塌與 `L_CR` 是否失守。與 proposal-final 既有截短 probe 同型，可直接搬。
- **壓噪誘發棄權**：對前綴施加低 SNR/加噪（C-signal 的離線通道模擬），量測**棄權率 vs 攻擊強度曲線**。曲線本身即貢獻，不需人類。

**只能進 threat model 文字（不做實驗）**：
- 最佳化式對抗擾動（adversarial perturbation）——proposal-final 已明文排除 adaptive attack，維持排除。〔Verified 文獻活躍：arXiv:2509.07132 對抗攻擊 benchmark、DeePen arXiv:2502.20427，查證 2026-07-23，但納入即爆範圍〕
- 攻擊者對已部署 policy 的門檻探測（需 query 迴圈）。
- 棄權疲勞的人因閉環（需真人受試，禁區）。

### D. Gate 改錨選項的攻擊面掃描

- **OS-privileged 系統 Phone-app（P/L 主錨，錨 Pixel Scam Detection）**：部署點合法，但**Pixel Scam Detection 是詐騙話術/內容偵測，非深偽語音偵測**——先例只背書「部署位置」，不背書任務。攻擊面殘留：偽造來電號碼冒充已知聯絡人可繞過「僅陌生號碼」觸發；預設關閉使多數使用者無保護。此兩點寫入部署想定 caveat 即可，不影響離線模擬的科學性。〔Inference〕
- **語音訊息事後分析（L 席法律最乾淨）**：**紅隊反對作為主錨**。訊息已完整送達，接收方握有整段音訊，**anytime 早停失去對抗動機**——沒有活人在線適應、沒有「撐過前綴」的攻擊者，「聽到第幾秒」退化為單純的延遲/算力最佳化，RQ 核心（帶風險承諾的棄權）被抽空。法律乾淨換來的是議題塌陷。
- **視訊會議串流**：活人在線、可即時適應，攻擊面與來電同構且更豐富，**保留 RQ novelty**，是次於 OS Phone-app 的可守改錨。
- **擴音側錄**：攻擊者通常不知第二裝置存在 → 適應性**較低**（利多），但音質雙重劣化。作 robustness 附錄可，不作主 estimand。

---

## 對候選研究問題的具體修改

1. 把估計對象從「首次 commit 的前綴長度」改為**「整通全程連續 any-time 偵測」**：spoof 吸收、clean 非吸收、持續監聽至掛斷。
2. RQ 明列 **mid-stream 真實標籤切換**為一級威脅，並以 bona-fide→spoof 離線 splice 納入 confirmatory 評估。
3. 主 endpoint 除 `L_CR` 外，新增**「切換後偵測延遲」**與**「攻擊強度 vs 棄權率曲線」**兩個對抗指標。
4. 部署想定改寫為 OS 級本機瞬態篩選，明文標註「未發現不停止監聽、棄權綁定升級」。

---

## kill conditions（什麼證據出現就放棄我支持的路線）

1. 若形式化無法同時容納「clean 非吸收 + spoof 吸收 + 連續重評」——即無法定義 mid-stream 切換下的乾淨 estimand（交 S 席），則 anytime 前綴框架退化為短音訊評測，應 kill 回 proposal-final。
2. 若離線 splice/截短/加噪三種 recipe 被判定仍算「adaptive attack 實驗」而違反硬約束，則對抗軸整個抽掉，來電相對 proposal-final 無新貢獻，改錨。
3. 若作者採「語音訊息事後分析」為主錨——紅隊視為 RQ 核心塌陷，anytime 棄權失去對抗意義，此路我不支持。

---

## 給下一波的一句話

S 席：請把 estimand 直接定義成「整通全程 any-time 偵測（spoof 吸收、clean 永不停聽）」並證明在 bona-fide→spoof 離線 splice 上仍能給非平凡的相依前綴 anytime 風險保證——做不出來，題目就退回短音訊評測。
