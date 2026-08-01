# 目錄重構：雙方共識定案 — 待作者裁定

日期：2026-07-15
提出方：Claude Code + Codex（兩份提案收斂而成）
來源：`discussions/RESTRUCTURE-PROPOSAL-claude.md`、`research/RESTRUCTURE-PROPOSAL-codex.md`
性質：**兩個 agent 已達成共識的單一方案。作者核可前，任何一方不動手。**

---

## 0. 一句話

兩個 agent 一致建議採 **B+**：**不搬任何現有目錄**，只新增一個 `exchange/` 交換區與一套「單一寫入者 + 不可變 handoff」協議。變體 A（完整搬成 `claude/` + `codex/`）**暫不做**，只有 B+ 實際運作後出現可量測的痛點才評估。

## 1. 為什麼不採完整分家（變體 A）

作者原傾向把兩個 agent 完全分目錄。兩個 agent 討論後，一致建議先不要，理由（主要由 Codex 提出、Claude 同意）：

1. `research/` 是**按知識用途分類**的長期研究資產，不該語意上綁成「Codex 私有」——驗證結果未來作者或其他工具也會用。
2. `PROJECT.md / TASKS.md / DECISIONS.md` 是**專案治理文件，不是任何 agent 的領地**，放根目錄最清楚；放進 `codex/` 會讓人誤判權限。
3. `AGENTS.md` **和** repository skill（`.agents/skills/develop-thesis-ideas/SKILL.md`）**都**寫死了多個路徑。搬目錄不是改一個檔，要同步改 skill、根目錄索引、既有 artifact 的交叉引用——漏改任一處就會 split-brain（新舊兩套路徑並存）。
4. 大量歷史文件有相對路徑引用，完整搬遷會造成「檔案還在、但證據鏈斷掉」這種難察覺的錯誤。
5. B+ 已能拿到**固定 inbox/outbox、零同檔寫入、增量可追溯**的主要價值。

> 領地其實早就存在（`discussions/` = Claude、`research/` = Codex），真正缺的只有**交換管道**。B+ 補的正是這個。

## 2. 最終目錄結構（B+）

```
Master Thesis/
├── survey/                      # 中立：文獻 PDF + README，兩邊只讀不寫
├── discussions/                 # Claude 的工作區（不動）
├── research/                    # Codex 的研究 artifact（不動；ideas/validations/syntheses）
├── exchange/                    # ★ 新增：唯一的 agent 間交換區
│   ├── README.md                # 協議全文
│   ├── claude-outbox/
│   │   ├── INDEX.md             # 只有 Claude 寫（manifest + 狀態）
│   │   └── YYYY-MM-DD-HHMM-<topic>.md
│   └── codex-outbox/
│       ├── INDEX.md             # 只有 Codex 寫
│       └── YYYY-MM-DD-HHMM-<topic>.md
├── AGENTS.md                    # Codex 設定（不動；另見第 5 節 stale-path 修正）
├── PROJECT.md / TASKS.md        # 專案治理（根目錄，Codex 依 AGENTS.md 條件維護，Claude 只讀）
└── DECISIONS.md                 # 作者的唯一真理源
```

## 3. 交換協議（收斂版）

1. **方向性 outbox，單一寫入者**：`claude-outbox/` 只有 Claude 寫、Codex 只讀；`codex-outbox/` 反之。**任何實體檔都只有一個寫入者**——包含各自的 `INDEX.md`。**取消**先前 Claude 提的共用 `STATUS.md`（會造成同檔雙寫）。
2. **INDEX.md 當該方的 manifest + 觸發旗標**：outbox owner 在自己的 INDEX 列出已送出的 handoff、日期、狀態、一句話。接收方**只掃對方的 outbox/INDEX**，不掃整個 `discussions/` 或 `research/`。這是「小範圍 pull manifest」，比假裝有 push 通知更誠實。
3. **handoff 不可變**：送出後的檔案不再修改。新增或修正**一律另建 delta 新檔**（如 `...-claims-to-verify-delta-f.md`），用檔頭 `in_reply_to` / `supersedes` / `delta_of` 指回。**取消**先前 Claude 提的「原檔追加」（今天 E 節後補已證明有 race）。
4. **回信在自己的 outbox**：收件方以新檔回覆、`in_reply_to` 指回 handoff id，**不得在對方的檔案上標「已處理」**。
5. **handoff 最小欄位**（寫進 `exchange/README.md`）：`handoff_id`、`from`/`to`、`created_at`（含時區）、`request_type`（Explore/Validate/Synthesize/Compare/Decide/Coordination）、`scope`、`out_of_scope`、`in_reply_to`/`supersedes`/`delta_of`、`source_artifacts`（指向正式 artifact，不複製全文）、`expected_output`、`authority_boundary`（是否允許改狀態檔/下載/搬檔）。
6. **不複製全文**：outbox 放**短 handoff + 指標**，指向 `research/validations/…` 或 `discussions/…` 的正式 artifact，避免出現兩份會分歧的副本、維持單一真理源。
7. **作者居中裁決**：涉及論文方向與 `DECISIONS.md` 的結論，兩個 agent 只提建議，作者定奪。

## 4. 所有權與權限（確認，無異議）

| 區域 | 寫入者 | 其他方 | 備註 |
|---|---|---|---|
| `survey/` | 作者 | 兩 agent 只讀 | 中立文獻 |
| `discussions/` | Claude | Codex 依 handoff 引用才讀 | 非 inbox，不預設全掃 |
| `research/` | Codex | Claude 依指標才讀 | 知識資產，非「私有」 |
| `exchange/*-outbox/` | 各自 owner | 對方只讀 | 單一寫入者 |
| `PROJECT.md`/`TASKS.md` | Codex（依 AGENTS.md 條件） | Claude 只讀 | 治理文件，非 agent 私有 |
| `DECISIONS.md` | **作者** | 兩 agent 只讀/建議 | 唯一真理源 |

## 5. 一個獨立的既有缺陷（與 A/B 無關，建議一併核可修正）

`AGENTS.md` 與 `PROJECT.md` 仍指向 `discussions/2026-07-13-deepfake-audio/03-synthesis.md`，但該檔已被搬到 `discussions/legacy/2026-07-13-deepfake-audio/03-synthesis.md`（Claude 於歸檔第一輪討論時所致）。**這是 Claude 造成的 stale path**，風險是 Codex 可能略過早期 ideation history、在不完整脈絡上工作。建議作者核可後修正——由 Codex 更新它自己的 `AGENTS.md`/`PROJECT.md`（Claude 不寫 Codex 的檔），或 Claude 出草稿、作者套用。

## 6. 給作者的裁定清單

請逐條核可（或退回）：

- [ ] **D1**：採 B+（只加 `exchange/`，不搬現有目錄）。
- [ ] **D2**：交換協議如第 3 節——單一寫入者 outbox + 各自 INDEX.md、取消共用 STATUS.md、handoff 不可變、delta 另建檔。
- [ ] **D3**：`PROJECT/TASKS/DECISIONS` 留根目錄；Claude 對三者維持只讀；`DECISIONS.md` 作者專屬。
- [ ] **D4**：既有 `discussions/CLAIMS-TO-VERIFY.md` 與 `research/validations/2026-07-15-claims-to-verify-a-d.md` **不搬、不改**，在首份 `claude-outbox/INDEX.md` 登記為「pre-exchange 歷史 handoff（已查證 A–E）」。
- [ ] **D5**：授權修正第 5 節的 stale synthesis 路徑（獨立缺陷）。
- [ ] **D6**（保留）：變體 A 僅在 B+ 運作後出現可量測痛點、且作者另行核可完整 migration plan（path map + patch set + rollback + smoke test）時才做。

## 7. 核可後的執行分工

- **`exchange/` 骨架**（README、兩個 outbox、兩份空 INDEX）：中立且純新增，**Claude 或 Codex 任一方可建**（建議 Claude 建，因純新增、不碰 Codex 設定）。
- **stale-path 修正（D5）**：**Codex** 改它自己的 `AGENTS.md`/`PROJECT.md`（或 Claude 出草稿、作者套用）。
- **首份 INDEX 登記歷史 handoff（D4）**：Claude 建 `claude-outbox/INDEX.md`。

## 8. 附帶：一則好消息（與結構無關）

Codex 的驗證檔 `research/validations/2026-07-15-claims-to-verify-a-d.md` 檔名雖保留 `a-d`，**內容其實已更新涵蓋 A–E**（含後補的 E1–E8 資料集查證 + 文末給 Claude 的 12 點交接摘要）。也就是**我補的資料集宣稱 Codex 也已一併查完**。因此結構定案 + pilot 完成後，Claude 可**一次性**更新五個方向（含資料集），不需再等一輪查證。
