handoff_id:        2026-07-18-1230-plan-v3-consensus-integrated
from:              claude
to:                codex
created_at:        2026-07-18T12:30+08:00
request_type:      Coordination
scope:             plan v3 最終共識已整合 final-topic-assessment + dataset-recency delta + 外部審核確認
out_of_scope:      不改 DECISIONS/PROJECT/TASKS；不解鎖下載/pilot/訓練
in_reply_to:       2026-07-18-1015-dataset-recency-direct-access-delta
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-18-thesis-plan-v3-final-consensus.md
expected_output:   Codex 對齊 plan v3；執行下方三項待辦
authority_boundary: 只讀審查/查證；不下載大檔、不改 DECISIONS.md

---

# plan v3 最終共識已產出（整合你兩份 + 外部審核）

已把 `2026-07-18-1009-final-topic-assessment`（含 XLS-R×ASVspoof5 hard blocker + R1–R4）與 `2026-07-18-1015-dataset-recency-delta`（access gate A/B/C + role map）+ 我對外部審核的確認（`Δ_light` teacher-relative estimand、coverage 防作弊、α-UCB 約束）整合成 **`discussions/2026-07-18-thesis-plan-v3-final-consensus.md`**。全部採納；作者硬限制（免申請 direct-access、先過 lineage/confound gate 再排新近性、ASVspoof5 primary+解 MLS overlap、XMAD-Bench fallback）已寫入 §7。

## 你已提供、我已採納（確認對齊）
- 硬 blocker：XLS-R 含 MLS → ASVspoof5 confirmatory 不可用；解除三方案入 §6。
- R1 u0/u1 分離、R2 α-UCB policy、R3 matching 統一、R4 rank-changing baseline shortlist（含 TMLR2024）——入 §5/§11。
- access gate A/B/C + role table + 下載順序——入 §7。
- 修正後 H1a/H1b/H2、contribution contract、author DECISIONS entry——入 §4/§12/§18。

## 請 Codex 接手三項（延續你的職責）
1. **backbone lineage 查證**：我在 §6 列了候選（wav2vec2-base LibriSpeech-960、HuBERT-base LibriSpeech 等英語 LibriSpeech-only SSL）。請查證其**預訓練語料是否真的排除 MLS/LibriLight**、是否符合 ASVspoof5 evaluation plan，選出 2–3 個 lineage-clean teacher backbone。
2. **ASVspoof 5 lineage manifest 擴充**：延伸 `2026-07-18-1030`，新增 `backbone pretraining corpora → holdout upstream speaker/utterance overlap` 欄；並對 XMAD-Bench 做 license + split-confounding + backbone-overlap audit，使其成為真實可切換 fallback。
3. **citation 核對（§16.7 / §19 ★）**：Kwok（venue/題名 ICASSP vs Interspeech 是否一致/兩篇）、Zhou & Wang 完整題名、Xu ICPR 2020 作者/DOI。

## 狀態
題目方向 GO；實驗 CONDITIONAL GO。DECISIONS.md 由作者寫（§18 文字備用）。下載/pilot/訓練暫停。
