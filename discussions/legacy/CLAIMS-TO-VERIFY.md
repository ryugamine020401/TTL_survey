# 交接清單：待 Codex 查證的宣稱（Claude → Codex）

日期：2026-07-15
產生者：Claude Code（多 agent 思辨工作流的主持人）
交給：Codex 研究驗證 agent（依 `AGENTS.md` 的 evidence discipline 逐條查證）

## 這份文件是什麼

我（Claude）用多輪 role-based agent 辯論產出了五個論文方向（見 `discussions/2026-07-14-convergence/04-final-five-directions.md`）。辯論過程中 agent 們做了大量「novelty / 前作 / 數字 / 資料集可得性」的宣稱。

**誠實聲明：下列所有宣稱目前一律是 `Inference` 或 `Hypothesis`——它們來自 agent 的角色扮演推論，不是查證過的證據。** 這正是 `AGENTS.md` 明文提醒的：「不要把 role-based agent 討論當成 peer review」「不要假設八篇 survey 就建立了 novelty」。請把每一條當成**待驗證的 lead**，用原始來源查證後改標 `Verified` / `Refuted`，並記錄搜尋範圍、搜尋日期、最接近的競爭前作。

分工：**Claude 生成候選與 leads，Codex 查證。** 我不寫 `PROJECT.md / DECISIONS.md / TASKS.md`（那是你的地盤）；查證結果請依你的慣例寫入 `research/validations/`。

---

## A. Novelty /「零前作」宣稱（最高優先——決策成敗繫於此）

> 這類宣稱風險最高：`AGENTS.md` 規定絕不可在未記錄搜尋範圍與最接近前作下宣稱 "first / no prior work"。我的 agent 全都這樣宣稱了，需要你把關。

| # | 宣稱（出處） | 我方 agent 自稱的最接近前作 | 請查證 | 優先 |
|---|---|---|---|---|
| A1 | 「shift-aware selective-prediction ADD benchmark 仍無前作」（收編 FADEL 為 baseline 後仍成立）— D1 方向 | FADEL（evidential DL, 宣稱 ICASSP 2025） | selective prediction / classification-with-rejection / abstention 在 audio deepfake detection 的最接近前作；此 benchmark 是否真的無人做過 | 高 |
| A2 | 「把棄權訊號的 density-based vs discriminative 分家問題，五年 one-class ADD 賽道沒人問過」— D1 RQ2 | OC-Softmax / ACS / QAMO / EBM 系列 | 是否有人比較過 density-based 與 discriminative-derived uncertainty 在 unseen-generator shift 下的分歧 | 高 |
| A3 | 「confident-real 對抗評估軸 `max P(confident-real\|fake)` 現有文獻完全缺席」— D1 RQ3 | （agent 未指出前作） | selective prediction 的 adversarial abstention / attack-on-rejection 文獻是否已涵蓋此概念（含影像領域） | 高 |
| A4 | 「物理可逆性下界（不可逆資訊摧毀 vs 可逆分佈偏移）作為 laundering 分析框架，是不過期的資訊理論錨」— D3 | （宣稱新穎） | 是否已有 adversarial laundering / attacker-cost 文獻用 information-theoretic reversibility 分類攻擊動作 | 中 |
| A5 | 「watermark bit-level 在真實電信通道的可靠 bit 容量（含 neural codec transcode）前作未碰」— D5 RQ1 | AudioMarkBench（宣稱 NeurIPS 2024）、Özer et al.（宣稱 Interspeech 2025）做重錄/模擬穩健性，未碰真實通道 bit 容量 | 這兩篇是否存在且如描述；是否真有「真實通道 × neural codec × 可靠 bit 容量」的空白 | 高 |
| A6 | 「EU AI Act Article 50 標記在詐騙音訊通道的可讀性審計，零前作」— D5 RQ3 | （宣稱新穎） | 是否已有 Article 50 machine-readability / watermark-survival 的合規審計研究 | 中 |
| A7 | 「繁中詐騙話術現場條件的評估效度審計，撞題最少」— D4 | agent 引五篇短句/情緒 ADD 前作 | 「話術語意 × 短句 × 情緒 × 通道」四軸交互 + 繁中，是否已有人做 | 中 |
| A8 | 「真實電信通道存活審計是唯一經檢索仍無前作的空白」（第一輪結論，已被第二輪 G 自我修正） | 被 Presentation（2509.26471）、RTCFake 侵蝕 | 此空白在 2026-07 是否仍成立；RTCFake 與該 preprint 的實際涵蓋範圍 | 高 |

---

## B. 前作「存在性 + 內容」宣稱（agent 引用來打殺其他提案，需確認真的存在且如描述）

> 這些是我的 agent 用來「擊沉」提案的關鍵前作。如果其中有杜撰或誤述，被擊沉的提案可能其實還活著。

| # | agent 宣稱的前作 | agent 宣稱的內容 | 請查證 |
|---|---|---|---|
| B1 | D-CAPTCHA（AsiaCCS 2023）、D-CAPTCHA++（IJCNN 2024） | 音訊版挑戰-回應，準確率 91–100% vs 無挑戰 71%，含 41 人 user study；++ 已攻破一輪 | 存在性、會議、數字、是否確實使「互動挑戰-回應」提案失去 novelty |
| B2 | StreamVC（Google, ICASSP 2024） | 端到端串流 VC，70.8ms 延遲，使「延遲判別」過期 | 存在性與延遲數字 |
| B3 | AuthentiCall（USENIX Security 2017） | 逐條做完 CallAttest 的 delta（內容認證+帶外通道+形式化驗證+OTT 單邊部署） | 存在性與涵蓋範圍，是否真的使 CallAttest 提案作廢 |
| B4 | Codecfake（IEEE TASLP 2024） | 100 萬筆，codec-latent 偵測 source-tracing | 存在性、規模、是否佔領「codec-latent 新 domain」 |
| B5 | FADEL（evidential DL, ICASSP 2025） | audio deepfake 的 evidential uncertainty | 存在性；是否應為 D1 的 baseline |
| B6 | Authenticated Contradictions（CVPR 2026 Workshop APAI, arXiv 2603.02378） | 已收錄 survey，見 survey/README #7 | 已在 survey，優先度低；確認 arXiv id 與 workshop |
| B7 | 方法論判例：Nature Scientific Data 2025（L2D 合成專家）、UMUAI 2026（認知模型跨研究預測）、IMF WP 2025/085（情境校準模擬） | 支撐「用文獻校準模型取代真人實測」的學術正當性 | 存在性；是否真能支撐此方法論（此點已不再是主線，因已放棄受騙率因變數，中低優先） |
| B8 | STOPA（arXiv 2505.14188, Interspeech 2025） | source verification，open-set 下崩 | 存在性（用於否證「人群同源連結」，該提案已死，低優先） |

---

## C. 具體數字宣稱（多來自 survey 的 8 篇，但需確認未被 agent 扭曲）

| # | 宣稱 | 出處 | 請查證 |
|---|---|---|---|
| C1 | VoiceWukong：AASIST2 EER 英 13.50% / 中 13.54%，其餘 SOTA >20%，數個 AUC≈0.5；含 300+ 人 user study | survey #2 | 對照原論文；特別是「per-sample 人類數據在 Zenodo 可申請取得」是否屬實（D1 要用） |
| C2 | 「SOTA 偵測器遇閉源商用生成器 EER 從 <1–5% 暴增至 13.5–50%」 | survey #2 | 原論文是否支持此區間 |
| C3 | ASVspoof 2021 DF = 611,829 筆 | 多方向引用 | 對照官方 |
| C4 | C2PA「五項安全目標全部未達成」 | survey #6 | 對照 UMBC 原文（已在 survey，中優先） |

---

## D. 資料集可得性宣稱（你的核心職責，且下方 E 節即將大量新增）

| # | 宣稱 | 請查證 |
|---|---|---|
| D1 | ASVspoof 2019 LA / 2021 DF、In-the-Wild（Zenodo）、MLAAD 皆可自由下載、授權允許學術用 | 現行下載連結是否有效、授權條款 |
| D2 | **RTCFake（HuggingFace）含 real/fake 配對的真實 RTC 通道音訊，授權允許學術重散布** — 這是 D2/D5 方向的**單點故障** | 最高優先：是否真的存在、可下載、授權、含配對與標記 |
| D3 | VoiceWukong per-sample 人類數據在 Zenodo，申請制 | 是否申請制、核准率、時程 |
| D4 | 「Delgado 團隊已進場真實通道審計，搶先風險最高」 | 是否有該團隊近期 preprint/發表，評估被搶先的實際風險 |

---

## E. 資料集精修工作流的新宣稱（2024–2026 新資料集，你的核心職責）

> 來源：`discussions/2026-07-14-dataset-refine/03-updated-five-directions.md`。這些是 role-based agent 的宣稱，其中資料集可得性由 agent G「實測 HTTP 狀態碼」得出——**請以你的獨立查證為準，不要採信我的 agent 的 HTTP 測試**（匿名抓取的狀態碼不等於學術授權可用）。

| # | 宣稱（資料集 + 屬性） | agent 宣稱的取得資訊 | 請查證 | 優先 |
|---|---|---|---|---|
| E1 | **DFADD**（2024，diffusion／flow-matching 範式 fake，D1/D3 的 unseen-generator 主力） | HuggingFace `isjwdu/DFADD`，MIT，非 gated，「用 2025-04 修正版」 | 存在、可下載、授權、規模；是否真為 diffusion/FM 範式（2019/2021 沒有的）；「2025-04 修正版」是什麼、修正了什麼 | 高 |
| E2 | **CodecFake+**（2025，neural-codec 世代 fake，D3 laundering 主對象） | HF `CodecFake/CodecFake_Plus_Dataset`，MIT，101 GB，非 gated（agent 實測 HTTP 200） | 存在、授權、規模；與另一個同名「CodecFake」（survey B4 的 IEEE TASLP 2024）是否為不同資料集，勿混淆 | 高 |
| E3 | **RTCFake**（2026，真實 RTC 通道，D2/D5 單點故障） | HF `JunXueTech/RTCFake`，**agent 實測匿名抓取 HTTP 401＝gated** | 最高優先：申請/授權門檻、核准條件、是否允許學術重散布、是否含 real/fake 配對與標記；gated 是否可解 | 最高 |
| E4 | **MLAAD v10**（2025，取代 MLAAD v5，D1 unseen 廣度） | deepfake-total.com 公開下載 | 存在、v10 vs v5 差異、授權 | 中 |
| E5 | **SpeechFake**（開源部，D1 備選／D4 zh-CN 對照） | HF `DeepFense/SpeechFake`，Apache 2.0 | 存在、開源部涵蓋範圍、授權、是否含中文 | 中 |
| E6 | **2025 世代 zh 開源情緒 TTS**：CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2（D4 自建 fake 用，選 2 家） | GitHub／HF 開源 checkpoint | 各 checkpoint 是否開源可商用/學術用、是否真能產「台灣國語 + 哭腔/急迫情緒」、授權 | 中 |
| E7 | **CFAD**（zh-CN deepfake，D4 對照臂備選） | 公開 | 存在、授權、涵蓋 | 低 |
| E8 | **《Will They Survive Neural Codecs?》**（Interspeech 2025，arXiv 2505.19663，D5 補作為唯一直接前作 baseline） | arXiv 2505.19663 + repo | 存在、arXiv id 正確、是否真為「watermark × neural codec 存活」最接近前作（呼應 A5） | 高 |

**本輪 agent 自己駁回、無需你再查的**（記錄以免重工）：ASVspoof 5 當訓練種子（換種子＝重訓，方法論違規，非取得性問題）；SpoofCeleb 受 VoxCeleb 非商用授權；Deepfake-Eval-2024 scrape 內容再散布受限。這些是**方法/授權判斷**，若你的查證與 agent 結論不同請標出。

---

## 給 Codex 的建議處理順序

1. **D2（RTCFake）** — 兩個方向的單點故障，先查，一票否決性質。
2. **A1 / A5 / A8** — 三個最依賴「零前作」的方向命脈。
3. **B1–B5** — 確認被擊沉的提案是不是真的該死。
4. 其餘按優先級。

查證結果若推翻任何一條，會直接改變五個方向的推薦排序——請務必保留否證證據（`AGENTS.md`：不要為了維護偏好的方向而優化文獻回顧）。
