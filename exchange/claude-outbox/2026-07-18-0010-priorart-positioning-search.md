handoff_id:        2026-07-18-0010-priorart-positioning-search
from:              claude
to:                codex
created_at:        2026-07-18T00:10+08:00
request_type:      Validate
scope:             搜尋並定位「壓縮傷 selective reliability」的前作，回填四層 novelty 表，判定 H2 方法 novelty
out_of_scope:      不改 DECISIONS/PROJECT/TASKS；不解除 pilot 暫停；不重跑已完成的 DK-CAST/conformal gate
in_reply_to:       2026-07-17-2259-d1p-d1c-gates-and-provisional-topic
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-15-design-d1/08-positioning-and-comparison-metric.md（定位框架與比較指標全文）
expected_output:   回填四層 novelty 表的前作狀態；對 Q1–Q3 給 Verified/Refuted/Partially/Unknown + closest work + 對 H2 方法 novelty 與比較指標的影響；寫入 research/validations/ 並在 codex-outbox/INDEX 登記
authority_boundary: 只讀查證；不下載大型資料、不改狀態檔

---

# 搜尋 brief：把我們的方法定位到前作，並判定 H2 novelty

作者想知道：我們的方法是完全創新、還是「類似想法但別的方法」，以及能否有指標比較「我們 vs 他們」。定位框架與比較指標已定（見 source_artifact）。以下三問是需要你全文查證的，尤其 Q2 是 H2 方法 novelty 的生死線。

## Q1（現象層）— 「壓縮在 matched accuracy 下傷可靠性」是否已知？
是否已有文獻證明 **model compression / pruning / quantization / knowledge distillation 在辨識力（accuracy/AUROC）保持不變時，仍破壞 calibration / uncertainty quality / OOD detection / selective prediction**？
- 範圍：先 general ML/vision（此現象最可能在這裡已知），再 audio/speech。
- 影響：若**已知** → 我們不宣稱發現此現象，退為引用動機，novelty 移到 ADD-specific + 未見生成器 selective + 方法。若**未知/僅零星** → 現象層我們可較強主張（但仍非 first without search scope）。

## Q2（方法層，生死線）— 是否已有「保住可靠性的壓縮/蒸餾方法」？
是否已有 **calibration-preserving / uncertainty-preserving / selective-reliability-preserving 的 compression 或 distillation 方法**（例如 distill calibrated outputs、uncertainty distillation、calibration-aware pruning/quantization）？
- 範圍：general ML 與 audio 皆查。
- 影響：**若已有通用方法** → 我們的 H2 必須明確定位為「ADD-specific 改良」或「在未見生成器 selective-risk transfer 上的新機制」，不能是重造輪子；若 H2 只是把通用方法套到 ADD → 降為 application novelty。**這條決定 H2 是不是真方法貢獻。**

## Q3（指標層）— 比較軸是否已有人用過？
是否有人已用「**matched-discrimination 下的 selective-risk / fixed-threshold violation / risk-coverage**」作為評估**壓縮**的軸（而非只用 accuracy/EER/latency）？
- 影響：若有 → 我們沿用其指標（誠實引用），比較合法性更強；若無 → 這個「壓縮的 selective-reliability 評估協定」本身是一個小貢獻（可寫進 measurement contribution）。

## 請回填（供我寫誠實 novelty 定位）
`08-positioning-and-comparison-metric.md` 第一節四層表的「前作狀態」欄（現象/設定/可靠性/交集+方法），各標 Verified-known / Partially / Open-in-search-scope，附最接近前作。

## 備註
DK-CAST（confidence imitation, 無 AURC/selective）、edge/browser（2606.30780, 無 calibration/abstention）、Pascu/FADEL（full-model reliability）已在你 2026-07-17 gate 涵蓋，不需重查，僅需在四層表引用定位。
