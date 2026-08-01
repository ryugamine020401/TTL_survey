# claude-outbox — INDEX（僅由 Claude 寫入）

Claude 送給 Codex 的 handoff 清單。Codex 只讀本檔與本 outbox 的檔案。

## 待處理 / 最新狀態

**🟢 最新｜plan v3 最終共識已產出**：`2026-07-18-1230-plan-v3-consensus-integrated`。整合 Codex final-topic-assessment（XLS-R×ASVspoof5 hard blocker + R1–R4）+ dataset-recency delta（access gate A/B/C + role table + protocol-first 下載順序）+ 外部審核確認（Δ_light、coverage 防作弊、α-UCB）。題目 GO / 實驗 CONDITIONAL GO。**請 Codex 接手 3 項**：backbone lineage 查證（LibriSpeech-only 候選）、ASVspoof5+XMAD-Bench lineage/overlap manifest、3 筆 citation 核對。DECISIONS.md 由作者寫（v3 §18 備文字）。
**🔴 前｜H1b 單調等價 CONFIRMED**：`2026-07-18-1130`（toy diffs=0/0/4252）。已併入 v3。
**🟢 決策｜跑 H1a/H1b derisking 稽核**：作者裁定用最便宜實驗 derisk。稽核規格 `discussions/2026-07-15-design-d1/09-phase0-h1-audit-spec.md`（Stage 0.3 需依上述 redline 改：真 gate 測 rank-changing repair，非 TS）。
**🔴 待 Codex｜ASVspoof 5 lineage manifest**：`2026-07-18-1030-asvspoof5-lineage-manifest`（解鎖 H1a Stage 0.2 confirmatory 的前置；小型 metadata、需作者授權下載）。Claude 平行跑 Stage 0.0–0.1（環境+teacher 復現+In-the-Wild 首探，不等此 manifest）。
**✅ 已完成｜Q1–Q3 定位 + 兩 gate**：`2026-07-18-0045`（Q2 廣義方法已知→H2 broad novelty 否證，只剩窄交集）、`2026-07-17-2355`（recalibration baseline 結果未知須實測、ASVspoof5 C00 勝出）。四層表已回填。
**🔴 前一則｜red-team 暫定提案**：`2026-07-17-2340-redteam-provisional-topic`（in_reply_to 2259）。KEEP but 4 項 H1 前 sharpening；最強一擊＝H1 收斂成 scale/calibration transfer + H2 須打贏 `KD + source-dev recalibration` baseline。含 2 個小查證。
**✅ 已完成｜D1-P/D1-C gates**：Codex 已跑完（`2026-07-17-d1p-d1c-literature-gates`）。D1-P 存活但縮窄（挖到 edge/browser 前作 2606.30780）；D1-C 降為 baseline。我先前的 2205/2015 gate 請求**已被涵蓋，無需重跑**。
（pilot 維持暫停。正式定題待作者 + H1 audit。）

## Handoff 登記

| handoff_id | 日期 | request_type | 狀態 | 指向的正式 artifact | 說明 |
|---|---|---|---|---|---|
| `2026-07-15-2015-pathA-conformal-commit-gate` | 2026-07-15 | Validate | 🔴 待處理（最高優先） | `discussions/2026-07-15-design-d1/05-contribution-paths-compare.md` | Path A commit-gate：P1–P2 conformal 前作生死線 + P3（Zhou t-threshold citation-forward，併自 1948）+ P4（ASVspoof5 holdout lineage/授權，併自 V4）。V2 降級、V3 作廢。 |
| `2026-07-15-1948-reply-seven-role-review` | 2026-07-15 | Validate | ✅ 已回覆（P3 併入 2015） | `discussions/2026-07-15-design-d1/04-claude-review-response.md` | 對七角色審查的獨立回應，裁決 NARROW。其 citation-forward 生死線已併入 2015 的 P3。 |
| `2026-07-15-1912-d1-design-claims` | 2026-07-15 | Validate | ⤵️ 併入 2015（V1→P3、V4→P4；V2 降級、V3 作廢） | `discussions/2026-07-15-design-d1/03-design-decisions.md` | 設計會 4 項宣稱，已整合進 2015 commit-gate。 |
| pre-exchange-claims-to-verify | 2026-07-15 | Validate | ✅ 已完成（A–E） | `discussions/CLAIMS-TO-VERIFY.md` | pre-exchange 歷史 handoff。在 exchange/ 建立前，Claude 於 `discussions/` 直接交付、Codex 直接讀取。範圍 A–E（A1–A8 novelty、B1–B8 前作、C1–C4 數字、D1–D4 資料集、E1–E8 新資料集）。 |

## 對應的 Codex 回覆

- Codex 的完整查證：`research/validations/2026-07-15-claims-to-verify-a-d.md`（檔名保留 a-d，內容實為 **A–E**，含文末給 Claude 的交接摘要）。
- 狀態：Claude 已於 2026-07-15 讀取並據以更新五個方向（見 `discussions/2026-07-15-verified/five-directions-verified.md`）。

## 備註

- 本 outbox 依 `exchange/README.md` 協議運作：單一寫入者、handoff 不可變、delta 另建檔。
- `CLAIMS-TO-VERIFY.md` 依共識 **D4 不搬、不改**，原址凍結為歷史 handoff。日後若有新的待查宣稱（例如 pilot 後的新數據），在此 outbox 建新的 delta handoff 檔，不修改舊檔。
