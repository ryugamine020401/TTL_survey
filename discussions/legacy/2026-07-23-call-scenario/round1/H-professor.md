# H-professor 教授兼收斂法官席 — Round 1 裁決

日期：2026-07-23。已完整閱讀七席發言、00-problem-statement 與 proposal-final。

## 立場摘要（≤5 行）

1. 總裁決：**CONDITIONAL**——值得起草來電版 proposal，但必須先過三道便宜的門（R2 形式化、週末 Phase-0 probe、C08–C11 確認），任一不過即 KILL 回 proposal-final。
2. 「這還是一個問題嗎」測試：**有條件通過**——收斂為一個問題、一套方法論、三個 RQ，前提是採納本席對 D/S 分歧的裁定：spoof-commit 吸收、clean 非吸收，splice 攻擊降為 stress 條件而非主 endpoint。
3. 算力不是約束（粗算全程 ≤750 GPU-h，預算 1,200–1,500），**日曆與 S 席方法學風險才是**。
4. 改錨成本近零（proposal-final 資產幾乎全數繼承，來電版是嚴格推廣），而 gap 正被包圍（"Hi!" ICASSP 2026、RTCFake ACL 2026）——決策不對稱性支持現在試。

## 主體分析

### 1. 「這還是一個問題嗎」測試

七席收斂後的問題：**來電場景（OS-privileged on-device、8kHz、post-channel 逐秒前綴串流）下，source-frozen 的 sequential selective policy 之風險承諾在未見生成器上是否轉移。**一套方法論：LTT 式有限樣本 policy-level 校準（Ringel et al., ICML 2024；S 席 Verified）＋ teacher-relative `Δ_light` 序列版 ＋ 離線前綴重評分（A）＋ encode-once/decode-once 通道協定（C）。三個 RQ 共用此方法論：
- **RQ1（H1a/H1b 推廣）**：凍結 sequential policy 的 family-macro anytime leakage 是否守住 α；輕量化額外退化 `Δ_light^seq` 是否 > ε。
- **RQ2（sequential 附加值）**：optional-stopping inflation 是否非零、自適應停止是否 Pareto-支配最佳固定 τ、τ*(α) 曲線——S 席三測試預先登記。
- **RQ3（條件性 H2）**：full-context teacher → prefix student 的 future-aware 蒸餾（A 席，場景原生）。

判定：**PASS，但脆弱**。唯一會把它裂成兩個問題的力量是 D 席——若「切換後偵測延遲」「攻擊強度 vs 棄權率曲線」升格為主 endpoint，就多出一個對抗評測問題。故裁定（對 D/S 分歧）：**採 D 的語意（唯一吸收停止態是「發現合成證據」，clean 非吸收、監聽至掛斷），主 confirmatory estimand 保持在單標籤通話上**——leakage 重定義為 P_fake(整通至掛斷從未觸發發現且未升級)；bona-fide→spoof splice 作為**預先登記的 secondary stress 條件**進 confirmatory，切換後偵測延遲作 secondary 指標。S 席 R2 必須交出容納此語意的修訂形式化——「commit 後決策終局」草案已被 D 否決，此為條件一〔Inference：此裁定是範圍控制判斷，非事實主張〕。

其餘分歧裁定：RTCFake 從 critical path 全刪（C 席 gated 查證勝過 G/A 的 robustness 提名）；語音訊息改錨**不採**為主錨（D 席論證成立：抽掉 anytime 對抗動機即 RQ 塌陷；L 席的法律乾淨是必要非充分）；OS-privileged 錨採納，但必須誠實寫 D 的 caveat——Pixel Scam Detection 背書**部署位置**（on-device 即時來電音訊處理）非**任務**（它做話術偵測非深偽偵測），論文定位為「在已存在的部署點上超前一步的任務」〔P/L/D 席 Verified 之綜合〕。

### 2. 一年日曆與 GPU 粗算

用 A/C 數字：訓練 3 模型 50–70 h；主前綴評分含 bootstrap 緩衝 <250 h（bootstrap 重擬合在預計算分數上跑 CPU，不加 GPU）；2021 LA γ 校準（C 席新增）約 30–50 h；splice stress 集 20–30 h；SNR 曲線 20–30 h；RQ3 條件性蒸餾＋重評 200–300 h。**總計 ≤750 GPU-h，預算 1,200–1,500 的一半**〔Inference，基於 A 席 RTF~0.02 之 Verified 估計〕。GPU 不是瓶頸。日曆：R2 形式化 2 週（無 GPU）→ Phase-0 一個週末→起草 2 週→建置訓練 6–8 週→confirmatory＋splice＋γ 4 週→RQ3 條件性 8–10 週→寫作 8 週，含緩衝約 11–12 個月——**可行但無揮霍空間**，S 席形式化若在 R2 拖過八月，日曆開始吃寫作期。

### 3. 與 proposal-final 並排比較

**繼承（近乎全額）**：lineage 稽核與 wav2vec2-base 選型、資料集 gate 與 ASVspoof5 primary、KD 管線、UCB/L_CR/coverage 機器、TS no-op 定理、family bootstrap 原則——proposal-final 是來電版在 τ→全長時的特例，**改錨損失趨近零**（尚未訓練任何模型，下載本就暫停）。**新增成本**：S 的統計層、VAD 對齊（A 席 Verified：19LA 靜音捷徑 EER 15.1%，arXiv:2106.12914，2026-07-23）、通道協定、splice 工序、寫作複雜度。**保留現題的機會成本**：作者真實動機落空，且 G 席 Verified 的包圍態勢（"Hi!" arXiv:2601.19573 佔超短音訊、RTCFake arXiv:2604.23742 佔通道，均 2026-07-23 查證）意味四交集 gap 一年後大概率關閉；proposal-final 的 gap 較窄但安全。**決策不對稱**：三道門總成本一個週末＋紙上作業，失敗回退僅損失 ≤3 週——期望值明確支持試。

另本席自行查證：ASVspoof 5 論文明言 eval 資料以 16kHz 統一發布、C08–C11 於編碼後升採樣、條件施加於 eval 子集——**條件音檔隨免費包發布**〔Verified：https://arxiv.org/pdf/2502.08857 與 https://www.sciencedirect.com/science/article/pii/S0885230825000506 ，2026-07-23，搜尋詞「ASVspoof 5 evaluation set codec conditions C08 C09 C10 C11 included eval flac_E」〕；C 席致命風險一大幅降級，剩 README/protocol 欄位的零 GPU 確認。惟注意：每 utterance 僅一種條件，各條件子集較小，attack-family × 條件的覆蓋矩陣須在 protocol 上先驗算。

## 對候選研究問題的具體修改或否決

不否決。收斂版問題陳述（起草用）：**「以 OS 特權系統 Phone app 的 on-device 即時篩選為想定部署點（Pixel Scam Detection 為部署位置先例、非任務先例），source-frozen 的 sequential selective policy——spoof-commit 吸收、clean 非吸收、棄權綁升級——在 8kHz post-channel 前綴串流上，其風險承諾（policy-level anytime leakage ≤ α）於 documented lineage-disjoint 未見生成器是否轉移；τ*(α)、optional-stopping inflation 與 `Δ_light^seq` 為主要可報告量。」**

## Kill conditions（裁決的撤銷條件）

1. S 席 R2 無法在「clean 非吸收＋splice 標籤切換」下給出乾淨 estimand 與非平凡有限樣本保證 → KILL 回 proposal-final。
2. Phase-0 probe（VAD 對齊後）顯示 1s 前綴 ≈ 全長效能，無「多聽有益」張力 → KILL。
3. VAD 對齊後前綴分數仍被靜音/起點 artifact 主導 → KILL。
4. README/protocol 確認免費包不含 C08–C11 音檔 → 不 kill，通道軸降級為自製套件＋2021 LA γ 校準，公信力誠實降級。
5. 正式檢索發現「因果前綴＋棄權＋風險保證」ADD 先行工作 → gap 失效，KILL。

## 給下一波的一句話

R2 只有一個主戰場：S 席在 D 的語意約束下重寫形式化、其餘席位驗算它——作者請同步跑週末 Phase-0 probe 與 protocol 確認，三door全開才動筆起草，DECISIONS 在此之前一字不動。
