# 方向 #1 七角色設計審查：固定棄權規則的跨生成器風險違約

日期：2026-07-15

模式：Validate + Synthesize + Red-team

狀態：**NARROW；promising residual gap，尚未正式定題**

## 1. Inquiry

本審查回答：候選方向 #1「shift-aware selective prediction / uncertainty for audio deepfake detection」在 2026 年最新前作、資料 lineage、部署決策及統計要求下，是否仍有可辯護的碩論形狀？

七個角色分別審查 problem contract、selective-prediction metrics、frozen detectors、dataset/generator lineage、統計設計、closest work 與整體可行性。角色討論本身不是學術證據；重要技術與 novelty 判斷以本文連結的 primary／official sources為依據。

## 2. Bottom line

**Inference（信心中高）：原案必須收窄，不能原樣 KEEP；整個方向尚不必 KILL。**

可以保留的核心是：

> 只用來源 development data 同時固定 classification rule/threshold 與 selection/abstention threshold，在有 lineage 文件的較新 attack-system holdout 上，量測 generator-macro confident-real leakage 的風險違約、coverage 與失效邊界。

不能再宣稱：

- 首次把 uncertainty、rejection 或 selective prediction 用於 audio deepfake detection；
- 首次研究 audio deepfake detector 的 fixed-threshold transfer；
- ASVspoof 2019 LA → DFADD 已構成真正完全 generator-disjoint、source-disjoint 或部署有效的 temporal test；
- AURC、calibration 或 threshold transfer 任一成功可推出另外兩者成功；
- clean English read-speech benchmark 能直接證明 fraud-operations deployment safety。

目前只剩很窄的 **evaluation / measurement gap**。Pascu、Zhou 與 Kwok 已分別覆蓋 rejection curve、fixed-threshold transfer、synthesizer-balanced evaluation；若本研究最後只是把這三者串接，再跑多種 uncertainty scores 畫曲線，貢獻不足，應終止方向。

## 3. 七角色裁決

| 角色 | 核心交付 | 裁決／否決點 |
|---|---|---|
| A. 問題與威脅模型 | 機構式非同步語音分流；`ABSTAIN` 強制人工複核或帶外驗證；`ACCEPT-real` 只表示不因 ADD 升級 | 若沒有明確承接者、處理時限及 review capacity，否決 deployment claim；只能做 measurement thesis |
| B. Selective Prediction | 分開 ranking、calibration、fixed-threshold transfer；主安全量為 `L_CR=P(pred real, accept | fake)`；coverage 為共同效用限制 | 若用 AURC 替 fixed-threshold safety 背書，或將 ECE 改善當 ranking 改善，否決 |
| C. Audio Deepfake | 最小 detector 組合為 frozen SSL-AASIST + RawNet2；AASIST 可作 representation-failure control | 若兩個 representation-diverse detectors 在外部資料皆退化近隨機，否決 selective-threshold thesis，轉研究 detector generalization |
| D. Dataset / Lineage | DFADD 只能稱 `documented attack-system-disjoint, source-overlapping`；須做 L0–L5 lineage、hash、dedup、overlap 與 shortcut probes | ASVspoof19 與 DFADD 共享 VCTK source；DFADD fake/text 與 real/source 耦合。若 shortcut 解釋主結果，停用 DFADD 作 confirmatory evidence |
| E. 統計與量測 | message 為 loss 單位；generator family 是主要泛化與 precision 單位；nested generator/speaker/message bootstrap | 不得把 utterances 當 IID；若 generator family 數不足，縮成 case study，不得用增加同-family utterances補足泛化能力 |
| F. Novelty | fixed-threshold transfer 的 broad novelty 已被 2026 工作否證；只剩 source-fixed `q+t` + lineage holdout + cluster-valid violation 的窄交集 | 若追加檢索找到完整等同 protocol，立即終止；人工 review capacity 只改善 deployment contract，不能單獨救 novelty |
| G. Red-team | 最終 `NARROW`；刪 adversarial、RTC、UX、method zoo；核心產出是 protocol + lineage manifest + failure decomposition | 若最後只剩「多個 uncertainty methods × 多資料集 × 曲線排行榜」，整題 KILL |

## 4. Evidence map 與 closest-work collision

| Claim / issue | Evidence | Status | Implication |
|---|---|---|---|
| ADD reliability/rejection 不是空白 | [Salvi et al., ICASSP 2023](https://doi.org/10.1109/ICASSP49357.2023.10095524)；[Pascu et al., Interspeech 2024](https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html) | Verified，已出版 | 不得宣稱首次 rejection/selective ADD |
| Evidential uncertainty 已直接用於 fake-audio detection | [FADEL, ICASSP 2025](https://doi.org/10.1109/ICASSP49660.2025.10888053) | Verified，已出版 | FADEL 是 closest work／baseline，不是唯一 novelty 對手 |
| 事先設定 threshold 在 real-world holdout 失效已有前作 | [Schäfer & Steinebach, ICWSM 2026](https://ojs.aaai.org/index.php/ICWSM/article/view/42803) | Verified，已出版 poster | Kill「首次 fixed-threshold real-world ADD evaluation」 |
| ASVspoof19 → ITW/ASVspoof21 DF 的 threshold transfer 已被直接稽核 | [Zhou & Wang, arXiv:2606.21584](https://arxiv.org/abs/2606.21584) | Verified，2026-06 preprint | 最強直接碰撞；classification-threshold transfer 本身不能作核心 novelty |
| 更近期、多語與商業生成器的 fixed-threshold evaluation 已出現 | [Borodin et al., arXiv:2603.02364](https://arxiv.org/abs/2603.02364)；[Huang et al., ACL 2026](https://aclanthology.org/2026.acl-long.796/) | Verified，前者 preprint、後者已出版 | 「newer generator holdout」也不是單獨的新意 |
| Synthesizer pooling 會掩蓋少數 family | [Kwok et al., Interspeech 2025](https://www.isca-archive.org/interspeech_2025/kwok25_interspeech.html) | Verified，已出版 | generator-balanced evaluation 不是新概念；新意只能來自與 source-fixed selection-risk protocol 的聯合 |
| DFADD 的 exact named attack systems 較新且與 ASVspoof19 不同 | [DFADD paper](https://arxiv.org/abs/2409.08731)；[official repository](https://github.com/isjwdu/DFADD) | Verified | 可稱 documented attack-system-disjoint |
| DFADD 與 ASVspoof19 是否完全 lineage-disjoint | 兩者皆使用 VCTK；DFADD checkpoint/hash/seed 不完整，且 fake 使用固定 LJSpeech texts | Partly verified / Unknown | 不得稱 `truly unseen`；必須做 overlap 與 shortcut audit |

### Novelty 的安全措辭

> Within the documented search scope as of 15 July 2026, prior audio-deepfake studies separately evaluate uncertainty-based rejection, source-threshold transfer, and synthesizer-balanced robustness. We found no inspected work that jointly freezes both classification and selection thresholds using source-only fit/select/cert splits, then audits generator-macro confident-real selective-risk violations and coverage on a lineage-documented temporal attack-system holdout.

這句仍是受限搜索範圍內的暫時結論，不是「first」主張。Zhou、Borodin 等工作很新，正式定題前須再做 citation-forward search。

## 5. 收窄後的 problem contract

### Stakeholder 與 decision

- 系統使用者：有人工複核或帶外驗證能力的平台 trust-and-safety／企業 fraud operations。
- 自動決策單位：完整語音訊息。若模型切 windows，須以預註冊 aggregation 回到 message level。
- `ACCEPT-real`：只代表不因 ADD 訊號升級；不得顯示成「已驗證真人」。
- `ACCEPT-fake`：送高優先政策／人工複核；不直接作永久移除或法律判定。
- `ABSTAIN`：強制送人工複核或帶外身分驗證；不得靜默放行。
- 若沒有承接者、review capacity、處理延遲與替代驗證流程，論文只能主張 benchmark measurement，不能主張部署安全。

### Main RQ

> 當 detector、classification threshold (q)、selection rule 與 abstention threshold (t) 全部只由來源 development data 決定，且完全不以外部資料調整時，它們在有文件支持的 attack-system-disjoint holdout 上，是否仍同時滿足預先指定的 generator-macro false-real risk 上限與最低 coverage？

### Primary estimand

對 generator family (g)：

\[
L_{CR,g}(t)=P(\hat Y=\mathrm{real}, A_t=1\mid Y=\mathrm{fake},g)
\]

主要量為等權 generator-macro：

\[
L_{CR}^{macro}(t)=|G|^{-1}\sum_{g\in G}L_{CR,g}(t)
\]

主要 transfer violation：

\[
\Delta_{transfer}=L_{CR}^{macro,H}(t_{dev})-\alpha
\]

同時報告 overall、real 與 fake coverage；以 risk 的 one-sided UCB 與 coverage 的 one-sided LCB 判斷。\(\alpha\)、最低 coverage \(c_{min}\)、最小有意義改善 \(\delta\) 與可接受 CI 半寬 \(h\) 尚為 Unknown，必須由 stakeholder／review capacity 或明確的 measurement objective 決定，不能任意固定 30% coverage、20% improvement 或 AUROC 0.65。

### 必須分開的三層

| Layer | Question | Metrics |
|---|---|---|
| Ranking | score 能否把錯誤排在低信心端？ | error-AUROC、RC、AURC/eAURC、AUGRC |
| Calibration | 機率數值是否對應事件頻率？ | Brier、NLL、reliability diagram；ECE 僅輔助 |
| Threshold transfer | source-fixed 數值門檻是否在 holdout 守住風險與 coverage？ | generator-macro `L_CR` violation、coverage shift、UCB/LCB |

## 6. 一年期 minimum thesis

### 保留

1. Frozen SSL-AASIST 與 RawNet2，含 checkpoint/hash、official-score reproduction 與統一 preprocessing。
2. 一個 confirmatory selection score、一個 baseline、一個 primary holdout；其他方法與資料皆 exploratory。
3. Source `dev-fit / dev-select / dev-cert`；分類門檻、calibration、score direction、selection threshold 全凍結。
4. 一份 L0–L5 generator lineage、license、file hashes、overlap、dedup 與 shortcut manifest。
5. Message-level analysis；nested generator/speaker/message bootstrap，threshold-selection uncertainty 納入。
6. Failure decomposition：detector discrimination collapse、ranking collapse、calibration/scale shift、classification-threshold failure、selection-threshold failure。
7. 可重用 score files、split IDs、preprocessing spec 與 analysis code；不重散布未確認權利的 audio。

### 刪除／future work

- 新 backbone 或 foundation model 訓練；
- deep ensemble、MC-dropout 與六種以上 uncertainty method 排行榜；
- adversarial confident-real attack RQ；
- RTC/channel 大網格與 laundering；
- warning UX、user study、IRB；
- 真實詐騙率或受騙率主張；
- 任何以 target labels 選 score、temperature、threshold、normalization 或 preprocessing 的步驟。

## 7. Dataset verdict

### DFADD

採用前必須 pin 2025-04 corrected release，保存 revision/hash，將重複的 VCTK bona fide 檔去重，並建立：

- speaker、prompt、exact-utterance 與 content overlap report；
- acoustic model／vocoder／decoder／checkpoint／source corpus lineage；
- duration、silence、RMS/peak、spectral、ASR text-ID、speaker/source-ID shortcut probes；
- 每 generator 分開的 base discrimination、risk 與 coverage。

DFADD 只能先作 `source-overlapping newer attack-system case study`。若 text/source shortcut 能高準確預測 label，或 matched sensitivity 後主結論消失，DFADD 不得作 confirmatory evidence。

### Pivot holdout

可審計 ASVspoof 5 subset 是否比 DFADD 更適合；排除與 ASVspoof19 同 lineage 的 MaryTTS/waveform-concatenation attack 及不屬主 threat model 的 adversarial attacks，再將 source/generator/channel shift 分層，而非混成單一「unseen」標籤。

## 8. Preregistration skeleton

| Field | Freeze before holdout |
|---|---|
| Decision unit | 完整 message；window aggregation=`[...]` |
| Detectors | SSL-AASIST、RawNet2；checkpoint/code hash=`[...]` |
| Primary score / baseline | `[一個 confirmatory score]` vs `[MSP/logit-margin baseline]` |
| Source data | train / dev-fit / dev-select / dev-cert=`[...]` |
| Primary holdout | dataset/version/hash=`[...]`；lineage claim level=`[...]` |
| Primary estimand | equal-generator-family `L_CR_macro(t_dev)` |
| Risk / utility requirements | `alpha=[...]`, `c_min=[...]` |
| Threshold rule | 最大化 dev coverage，且 dev risk UCB ≤ alpha、coverage LCB ≥ c_min |
| Resampling | nested generator/speaker/message bootstrap；派生 variants 綁定 |
| Primary inference | risk one-sided 95% UCB；coverage one-sided 95% LCB |
| Cross-detector claim | 兩 detectors 都成立才宣稱跨 representation-family；一個成立則縮成 detector-specific |
| Multiple comparisons | 只有一個 confirmatory contrast；其他 exploratory，必要時 Holm |
| Missing scores | intention-to-deploy 視為 abstain；另報 complete-case sensitivity |
| Precision basis | pilot generator-level SD/ICC + simulation；不用 utterance-IID power |

## 9. Validation contract

### Gate 0：不跑大實驗前

1. 明確寫出 abstention 後誰在多久內做什麼；若無真實部署 owner，正式降級為 measurement thesis。
2. 決定 \(\alpha,c_{min},\delta,h\) 的來源；無法正當化時，不宣稱 deployability。
3. 對 Zhou、Schäfer、Borodin、Huang 與後續 citing/related works 再做 citation-forward search。
4. 建立 DFADD 與候選 ASVspoof 5 subset 的 lineage/overlap/license/shortcut feasibility table。
5. 驗證 frozen checkpoint 沒有用 holdout、ASVspoof19 eval 或後續資料調參。

### 最小 score-only pilot

- 兩個 frozen detectors：SSL-AASIST、RawNet2；
- 一個 source dev，凍結 (q+t)；
- 一個小型但涵蓋多個可稽核 attack families 的 holdout；
- MSP/logit-margin + 一個 representation-distance selector；
- random abstention（matched class-conditional coverage）與 target-oracle selector（僅診斷）；
- `L_CR_macro`、overall/real/fake coverage、ranking/calibration診斷、cluster interval；
- 同步跑 lineage、dedup 與 shortcut probes。

### Strengthen / keep signal

- joint protocol residual gap 經追加檢索仍存活；
- 兩 detector 外部 discrimination 不退化；
- generator family 數能達預先指定 precision；
- fixed (q+t) 揭示不能由 classification-only FAR 或 pooled curve直接推出的失效；
- generator-macro 與 pooled 分析有實質且可解釋差異；
- 結果在 shortcut-matched sensitivity 下保留。

### Kill / narrow conditions

- 找到相同 source-fixed (q+t) + lineage holdout + cluster-valid risk-violation protocol；
- lineage 不足卻仍需 `unseen generator` 作核心主張；
- 兩 detectors 有足夠 precision 地顯示外部近隨機；
- DFADD 結果主要由 text/source/speaker/duration/silence shortcut 解釋；
- 有效 generator family 數不足；
- 必須查看 holdout 才能選 score、threshold 或 preprocessing；
- selection threshold 的 failure ordering 與 Zhou-style classification FAR 完全相同，generator-macro 與 pooled 結論也無實質差異；
- 最後只剩 uncertainty method leaderboard。

### Useful negative result

最有價值的負結果是：base detector 仍有非退化 discrimination、uncertainty 尚能排序錯誤，但 source-fixed selection threshold 在多個可稽核 generator families 上系統性違反預先風險限制；此結果在適當 coverage、cluster-valid inference 與 shortcut controls 下仍成立。

若 \(\alpha\) 與 \(c_{min}\) 無法正當化，只能說「量測到 threshold instability」，不能說「部署安全閥失敗」。

## 10. Search scope and limitations

搜尋日為 2026-07-15。使用 IEEE／ICASSP、ISCA Archive、AAAI ICWSM、ACL Anthology、arXiv、官方 dataset pages 與作者 repositories；query families 涵蓋 audio/speech deepfake selective prediction、abstention/rejection、risk-coverage/AURC、uncertainty/calibration、fixed/pre-set/transferred threshold、unseen generator、generator-macro/synthesizer-balanced evaluation。

限制：2026 preprints 很新，引用索引不完整；未做專利、學位論文與非英語資料庫的 exhaustive search；Salvi 的官方全文存取受限；ITW/SocialDF 的完整 generator lineage 仍不透明。因此不得使用絕對 novelty 語言。

## 11. Project-state impact

- `DECISIONS.md`：**不修改**；方向 #1 尚未正式定題。
- `PROJECT.md`：本輪未獲作者批准改 scope，暫不修改；若 Gate 0 與 pilot 通過，可提案把方向名稱收窄為「source-fixed abstention risk violation under documented newer attack systems」。
- `TASKS.md`：應更新近期工作，把 2026 novelty collision、problem contract、lineage/shortcut gate 與 score-only pilot 放在 full benchmark 之前。
