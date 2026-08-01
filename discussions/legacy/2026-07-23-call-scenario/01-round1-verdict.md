# Round 1 對外結論 — 來電場景版研究問題

日期：2026-07-23。裁決席：H-professor（合併收斂法官／算力鷹派職能）。本文件為 round1 七席發言之收斂結論，僅供作者裁定參考；**不寫入 DECISIONS/PROJECT/TASKS**。

---

## 1. 總裁決

**CONDITIONAL**——值得起草來電版 proposal，但須先過三道便宜的門（見 §5）；任一不過即回 proposal-final，回退損失 ≤3 週。

## 2. 收斂後的問題陳述（一段話版）

> 以 OS 特權系統 Phone app 的 on-device 即時篩選為想定部署點（Pixel Scam Detection 為**部署位置**先例、非任務先例），source-frozen 的 sequential selective policy——唯一吸收停止態為「發現合成證據」，「未發現」非吸收、持續監聽至掛斷，棄權綁定升級動作——在 8kHz post-channel 逐秒前綴串流上，其風險承諾（policy-level anytime leakage ≤ α，UCB 有限樣本校準）於 documented lineage-disjoint 未見生成器是否轉移；τ*(α)（最早有資格承諾的秒數）、optional-stopping inflation（逐前綴名目承諾與 policy 實際洩漏之差）與 `Δ_light^seq`（輕量化額外退化的序列版）為主要可報告量。論文全程離線模擬（前綴重評分＋encode-once 通道協定），不部署、不攔聽、不做真人實測。

三個 RQ 共用一套方法論（LTT 式 policy-level 校準＋teacher-relative 隔離＋離線通道模擬）：
- **RQ1**：凍結 sequential policy 的承諾轉移與 `Δ_light^seq`（proposal-final H1a/H1b 的嚴格推廣）。
- **RQ2**：sequential 附加值——peeking inflation、對最佳固定 τ 的 Pareto 支配、τ*(α)。
- **RQ3（條件性）**：future-aware prefix 蒸餾（full-context teacher → prefix student）。

D 席對抗軸（bona-fide→spoof splice、刻意短句、壓噪）作為**預先登記的 stress 條件與 secondary 指標**進入 RQ1/RQ2，不升格為主 endpoint。

## 3. 七席共識與分歧

### 共識（七席一致，無異議採納）

| # | 共識 | 依據席位 |
|---|---|---|
| 1 | 場景不 kill；「第三方 app 攔截來電」敘事死，改錨 OS-privileged 系統 Phone app（Pixel 先例） | P/L 一致 Verified |
| 2 | 法律可守窄門＝「OS 級、本機、瞬態、不留存、預設關閉」；anytime 早停與隱私 minimization 同構（加分論證） | L |
| 3 | gap 錨在 commit-time 統計判定，非短音訊準確率；單畫長度-EER 曲線非貢獻 | G/A/S 一致 |
| 4 | 通道軸零 rig：ASVspoof 5 C08–C11 為主，另加登記套件與 2021 LA γ 校準；EVS 砍除 | C/G 一致 |
| 5 | 離線前綴重評分為串流模擬代理；不做 chunk-based 因果重訓 | A（S/C 無異議） |
| 6 | 前綴時間零點錨 VAD 語音起點，否則靜音捷徑（EER 15.1%）毀掉整個 benchmark | A（唯一守此死角者） |
| 7 | SAVI/e-process 不得宣稱於單通話內成立；主保證走 Learn-then-Test 路線 | S |
| 8 | proposal-final 資產（lineage、gate、KD、UCB 機器、TS no-op）近乎全額繼承 | A/S/H |

### 分歧與裁定

| 分歧 | 立場 | H 裁定 |
|---|---|---|
| clean 是否吸收態 | S 草案「commit 終局」 vs D「clean 必須非吸收否則綠燈機」 | **採 D**。spoof 吸收、clean 非吸收；主 estimand 重定義為 P_fake(整通從未觸發發現且未升級)；S 於 R2 重寫形式化（條件一） |
| splice 攻擊的地位 | D 要求進 confirmatory 一級 vs 範圍控制 | **降為預先登記的 secondary stress**；切換後偵測延遲作 secondary 指標，防止裂成第二個問題 |
| RTCFake | G/A 提名 robustness vs C 查證 gated（違反免申請 hard gate） | **採 C**：critical path 全刪 |
| 語音訊息改錨 | L 列為法律最乾淨首選 vs D 反對（抽掉對抗動機、RQ 塌陷） | **採 D**：不作主錨；僅在來電版三門全敗後重議 |
| encode-once vs 統計重抽樣需求 | C 協定 vs S 疑慮 | 暫採 C（通道隨機性跨通話進入、非通話內）；S 於 R2 驗算相容性 |
| C08–C11 是否在免費包內 | C 列為致命風險（Inference） | **H 已近乎解除**：論文明言條件音檔隨 eval 包發布（arXiv:2502.08857，2026-07-23 查證）；剩 README/protocol 零 GPU 確認＋attack-family × 條件覆蓋矩陣驗算 |

## 4. 預算與比較結論

- **GPU**：全程粗算 ≤750 GPU-h（訓練 50–70＋主評分 <250＋γ 校準 30–50＋splice 20–30＋SNR 20–30＋RQ3 條件性 200–300），為 1,200–1,500 預算之半。GPU 非瓶頸。
- **日曆**：R2 形式化 2 週→Phase-0 一週末→起草 2 週→建置訓練 6–8 週→confirmatory 4 週→RQ3 8–10 週→寫作 8 週≈11–12 個月。**日曆與 S 席方法學風險是真瓶頸**；形式化拖過八月即吃寫作期。
- **與 proposal-final 比較**：改錨損失趨近零（尚未訓練、下載暫停中、來電版為嚴格推廣）；保留現題的機會成本是作者動機落空＋四交集 gap 正被包圍（"Hi!" ICASSP 2026、RTCFake ACL 2026），一年後大概率關閉。決策不對稱性支持現在花一個週末驗證。

## 5. 下一步（三道門，全開才起草）

1. **門一（R2 主戰場，紙上作業，2 週內）**：S 席在「spoof 吸收、clean 非吸收、splice 標籤切換」約束下重寫形式化並給出非平凡有限樣本保證；D/A/C 驗算。做不出 → KILL。
2. **門二（作者，一個週末，~10 GPU-h）**：Phase-0 前綴 probe——現成 checkpoint、VAD 對齊、19LA/ASVspoof5-dev 上量 {1,2,4,8}s 前綴 vs 全長的分數穩定性與效能差。無張力或 artifact 主導 → KILL。
3. **門三（作者，零 GPU）**：讀已下載之 ASVspoof5 protocol/README，確認 C08–C11 條件音檔欄位與 attack-family × 條件覆蓋矩陣。不含 → 不 kill，通道軸降級為自製套件＋2021 LA γ 校準並誠實標注。

**Kill/pivot 條件明確化**：門一或門二失敗 → 回 proposal-final，來電寫進 motivation/future work；門三失敗 → 降級不 kill；另若正式檢索發現「因果前綴＋棄權＋風險保證」ADD 先行工作 → gap 失效即 kill。三門全開 → 起草來電版 proposal 與 proposal-final 並排交作者裁定；在此之前 DECISIONS/PROJECT/TASKS 一字不動。
