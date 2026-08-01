# exchange/ — Claude ↔ Codex 交換區協議

建立日期：2026-07-15（作者核可 B+ 後）
依據：`discussions/RESTRUCTURE-CONSENSUS.md`（雙方共識定案）+ 作者裁定的三項釐清

這是兩個 agent（Claude Code、Codex 研究驗證 agent）之間**唯一**的訊息交換區。兩者沒有即時通道，全靠此處的檔案非同步協調，並由作者居中觸發。

## 核心規則

1. **方向性 outbox，單一寫入者**
   - `claude-outbox/`：**只有 Claude 寫**，Codex 只讀。
   - `codex-outbox/`：**只有 Codex 寫**，Claude 只讀。
   - 每個 outbox 的 `INDEX.md` 也只有該 outbox 的 owner 寫。
   - **任何實體檔都只有一個寫入者**——沒有共用檔（不設共用 STATUS.md），因為沒有檔案鎖，同檔雙寫必然有覆蓋風險。

2. **INDEX.md = 該方的 manifest + 觸發旗標**
   - owner 在自己的 INDEX 列出已送出的 handoff（id、日期、狀態、一句話、指向的正式 artifact）。
   - 接收方啟動時**只掃對方的 outbox/INDEX**，不廣掃 `discussions/` 或 `research/`。
   - 這是「小範圍 pull manifest」——沒有假裝存在的 push 通知；作者仍可明確觸發「請讀某 handoff」。

3. **handoff 不可變（immutable）**
   - 送出後的檔案不再修改。
   - 需新增或修正時**一律另建 delta 新檔**，用檔頭 `in_reply_to` / `supersedes` / `delta_of` 指回。
   - 回信在**自己的** outbox 建新檔，不得在對方檔案上標「已處理」。

4. **不複製全文**
   - outbox 放**短 handoff + 指標**，指向 `research/validations/…` 或 `discussions/…` 的正式 artifact，維持單一真理源、避免副本分歧。

5. **權限邊界**
   - `DECISIONS.md`：**作者專屬**。兩個 agent 都只提建議，不寫入。
   - `PROJECT.md` / `TASKS.md`：Codex 依 `AGENTS.md` 條件維護，Claude 只讀。
   - 涉及論文方向的結論，兩個 agent 只建議，作者定奪。

## handoff 檔案最小欄位（檔頭 front-matter）

```
handoff_id:        <YYYY-MM-DD-HHMM-topic-slug>
from:              claude | codex
to:                codex | claude
created_at:        <ISO8601 含時區>
request_type:      Explore | Validate | Synthesize | Compare | Decide | Coordination
scope:             <要處理的條目>
out_of_scope:      <明確不必重做的部分>
in_reply_to:       <handoff_id 或 —>
supersedes:        <handoff_id 或 —>
delta_of:          <handoff_id 或 —>
source_artifacts:  <指向正式 artifact 的路徑，不複製全文>
expected_output:   <期望對方產出什麼>
authority_boundary:<是否允許改狀態檔 / 下載 / 搬檔等>
```

## 檔名約定

`YYYY-MM-DD-HHMM-<topic-slug>.md`（HHMM 或序號避免同日同主題撞名；時間僅辨識用，依賴關係以 `in_reply_to`/`supersedes` 為準）。

## 目錄

```
exchange/
├── README.md            # 本檔（協議）
├── claude-outbox/
│   ├── INDEX.md         # 只有 Claude 寫
│   └── <handoff>.md
└── codex-outbox/
    ├── INDEX.md         # 只有 Codex 寫
    └── <handoff>.md
```
