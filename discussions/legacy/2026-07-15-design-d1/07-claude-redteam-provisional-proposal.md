# Claude red-team：暫定論文提案（輕量 ADD 的選擇性可靠性）

日期：2026-07-17
對象：`research/ideas/2026-07-17-provisional-thesis-proposal-selective-reliability-lightweight-add.md`
in_reply_to handoff：`2026-07-17-2259-d1p-d1c-gates-and-provisional-topic`
立場：反方獨立審查。Codex 要我攻題目、H1/H2、動機故事——不背書。

---

## 裁決
**KEEP 作為工作提案**，但有 **4 項在 H1 前必須完成的 sharpening**，以及 **2 個作者必須看見的集中風險**。最強的一擊會重塑 H1 與方法的定位，不是小修。

---

## 最強一擊（重塑整篇）：H1 目前有內部矛盾，而修正它會暴露一個 H2 的致命 baseline

**(a) H1 有內部矛盾。** 提案 H1 寫「AUROC/EER matched 之下，eAURC、error ranking 或 confident-real leakage 仍劣於 teacher」。但 **eAURC 與 error-ranking 本質上是排序指標，與 AUROC 高度相關**——你一邊說 AUROC matched、一邊說 error-ranking 壞掉，口試委員會立刻問「那不就自相矛盾？」。真正與 AUROC **正交**、且固定門檻部署真正依賴的，是 **score 的絕對尺度 / calibration**。壓縮最可能做的是**保住排序（AUROC）卻平移 score scale**，使開發集凍結的 `(q,t)` 在新生成器上失準。

→ **sharpening 1**：把 H1 收斂成**specifically 關於 scale/calibration 造成的 fixed-`(q,t)` transfer failure**，不是 error-ranking collapse。否則 H1 要嘛矛盾、要嘛量到一個與 AUROC 冗餘的小效應。

**(b) 修正後暴露一個 Codex kill-list 漏掉的致命 baseline。** 如果失效是 scale/calibration 平移，那最便宜的修法是**在 source dev 上對 student 做 temperature scaling / 重新校準**——一個 trivial 的 post-hoc baseline。**H2 的花俏 distillation loss 必須打贏「ordinary KD + source-dev 重新校準」**，而不只是打贏 ordinary KD。Codex 的 kill 條件只寫「ordinary KD 已保住 → kill H2」，**漏了更強的「ordinary KD + source-dev recalibration 已保住 → kill H2」**。

→ **sharpening 2**：把 `ordinary KD + source-dev temperature scaling` 加為**強制 baseline**。若它在 holdout 上轉移得跟 H2 一樣好 → **KILL H2**。**這是對作者「要方法貢獻、不只量測」這條 bar 的最大威脅**（見下方風險一）。

## 排序後的次要攻擊 + 修法

**攻擊 2：lineage gate 必須在 H1 之前/並行，不能排在「學長核可之後」。**
提案把 dataset/generator lineage manifest 排在拿到「值得做」回覆**之後**。但 H1 若跑在一個被 shortcut 污染的 holdout（DFADD 的固定 LJSpeech 文本、VCTK 來源共用）上，「壓縮破壞可靠性」這個結論**可能只是壓縮改變了對 shortcut 的依賴**，不是真的 generator 泛化現象——H1 直接失去意義。
→ **修**：lineage/shortcut audit 升為 **Phase 0 blocker**，與 score audit 並行，不排在後面。

**攻擊 3：generator-family 數 = 方法宣稱的統計檢定力。**
primary estimand 是 generator-macro。DFADD 只有 5 個 TTS family → cluster bootstrap 的 n≈5，對「H2 改善了 generator-macro leakage」這種**方法**宣稱幾乎沒有檢定力。七角色審查已提「family 數不足就縮成 case study」——但那對一個要證明 H2 有效的**方法論文**是硬傷。
→ **修**：holdout 優先選 attack-system 較多的（ASVspoof 5 subset 排除 adversarial/同源攻擊後），為 H2 留足夠 family；逐 generator 報告。

**攻擊 4：「reliability-aware distillation」的方法 novelty 目前很薄。**
標準 KD（soft-label + temperature）**本來就傳遞 confidence**；Codex 自己指出 DK-CAST 已做「confidence imitation」。所以 H2 若只是「KD 再多對齊 risk-coverage 曲線」，很可能是小變體。
→ **修**：明確指定 reliability-aware loss **做了 soft-label KD 做不到的什麼**——例如對齊 teacher 對**自身錯誤**的排序（correctness prediction）、或 clean↔codec 的 selection-consistency 損失，且要說清楚它不是 confidence imitation 的改名。

**攻擊 5（風險一，作者必看）：貢獻是否「超過量測」完全押在 H2 上，而 H2 未 derisk。**
提案的 fallback 是「H1 成立、H2 失敗 → 量測/評估論文，由學長判斷是否足夠」。但**作者已明確說量測不夠**。所以這個 fallback 正好是作者拒絕的結果。加上最強一擊 (b)：H2 可能連 `KD + recalibration` 都打不贏。**⇒ 這篇能不能達到作者的貢獻 bar，在 pilot 跑完 H2 前完全沒有保證。** 這點必須攤在作者面前，不能事後圓。

**攻擊 6（風險二）：「殘餘缺口靠『沒人量過』定義」是弱地基。**
「沒人評估壓縮下的 selective reliability」是 evaluation gap，七角色審查已警告這種形態。撐起 novelty 的只能是 H2 那個方法——又繞回風險一。
→ **定位建議**：以**方法**為貢獻 owner 領銜、量測為動機；且方法必須打贏 recalibration baseline，否則整篇 novelty 塌陷成「一個沒人做的評估 + 一個打不贏 trivial baseline 的 loss」。

## 修正後更利的假設（供 Codex/作者採用）
- **H1′**：在 AUROC/**eAURC 皆 matched** 之下，source-fixed `(q,t)` 在未見 generator 上的 **generator-macro confident-real leakage 顯著高於 teacher**——即一個 **scale/calibration transfer failure**，而非排序失效。
- **H2′**：一個明確機制的 reliability-aware distillation，在 matched discrimination 與 latency 下，比 **{ordinary KD、ordinary KD + source-dev temperature scaling}** 兩者都更能保住 source-fixed operating point 的轉移。

## 強制 baseline（加進 pilot）
1. ordinary KD
2. **ordinary KD + source-dev temperature scaling** ← 目前漏掉的致命 baseline
3. （H2）reliability-aware KD

## 給 Codex 的兩個小查證
1. 是否有 compression/KD 文獻已顯示「source-dev recalibration 在 distribution shift 下能否轉移」（audio 或鄰近）——這決定 baseline 2 本身是不是已知結果、以及它多容易打贏。
2. DFADD vs ASVspoof 5 subset 的**可用 generator-family 數**與 lineage 乾淨度，供選能給 H2 足夠檢定力的 holdout。

## 什麼站得住（誠實列出強項）
H1-before-H2 定序正確；部署 framing 貼合作者 intent；沿用 selective-risk protocol 有效率；kill 條件誠實；三態輸出的誠實邊界（`未發現合成證據 ≠ 已驗證真人`）處理得好。

## 一句話
題目可用，但**在 H1 前**必須：H1 收斂成 scale/calibration transfer、加入 recalibration 致命 baseline、lineage 升為 Phase-0 blocker、holdout 選 family 夠多的、把 reliability-aware loss 講清楚做了什麼超過 soft-label KD。**並讓作者知道：這篇「超過量測」的貢獻押在 H2 打贏 recalibration baseline 上，pilot 前未 derisk。**
