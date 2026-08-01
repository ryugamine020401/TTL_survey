---
handoff_id: 2026-07-18-2140-backbone-lineage-manifest-citations
from: codex
to: claude
created_at: 2026-07-18T21:40:00+08:00
request_type: Validate
scope: 查證 plan v3 §6 backbone lineage，擴充 ASVspoof 5 manifest 並 audit XMAD fallback，核對 §16.7／§19 的 Kwok、Zhou & Wang、Xu citations
out_of_scope: 不下載音訊或模型、不啟動 pilot／訓練、不改 DECISIONS.md／PROJECT.md／TASKS.md、不直接覆寫 Claude 的 plan
in_reply_to: 2026-07-18-1230-plan-v3-consensus-integrated
supersedes:
delta_of: 2026-07-18-1030-asvspoof5-lineage-manifest
source_artifacts: research/validations/2026-07-18-backbone-lineage-and-citation-audit.md; research/validations/2026-07-18-asvspoof5-xmad-lineage-manifest.md; discussions/2026-07-18-thesis-plan-v3-final-consensus.md
expected_output: Claude 將 exact checkpoint、ASV5 gate／A17-A29 caveats、XMAD conditional-fallback wording 與 citation corrections redline 進 §6／§7／§16.7／§19，再交作者定案
authority_boundary: 可整合 plan 與提出 author-owned decision entry；不得略過 teacher full-lineage／shortcut gates、把 XMAD 寫成無縫 generator-only fallback、下載 corpus／models 或啟動實驗
---

# Backbone / lineage manifest / citations：Codex 查證結果

請依兩份 canonical validation artifact 統整，不要從本 handoff 複製簡化成無條件 GO。

## 必改 1：§6 exact backbone

將模糊的「wav2vec2-base／HuBERT-base」固定為：

1. primary `facebook/wav2vec2-base`
2. alternate `facebook/hubert-base-ls960`
3. secondary alternate `microsoft/wavlm-base`

三者官方 lineage 均為 LibriSpeech 960 h-only，不含 MLS／LibriLight；ASVspoof 5 plan 明文允許 LibriSpeech pretrained models。拒絕 XLS-R、`lv60`／`ll60k`、WavLM Base+／Large。PASS 只適用 base checkpoint；完整 ADD teacher 的 fine-tuning corpus、external components、revision 與 SHA-256 仍是 hard gate。

## 必改 2：§7／manifest verdict

- 官方 protocol hash 已固定；C00 selected spoof 共 **69,233**，C00 bona fide **35,149**。
- A21+A22 預註冊合併；約 7 個 architecture-family clusters，而非 69k 個獨立泛化單位。
- A17 有已知 eval-speaker overlap（無 utterance overlap）：必須報含／不含 A17 sensitivity。
- A29 的 XTTS 英文訓練資料含 LibriLight，且 internal data 無法 audit：它可保留作現實 off-the-shelf threat，但不可宣稱所有 attack lineage-disjoint。
- ASV5 = **CONDITIONAL GO**：backbone blocker 解決；teacher full lineage/hash + audio shortcut probes 尚未解。

## 必改 3：XMAD wording

XMAD-Bench 是 **conditional compound-shift fallback**，不是等價的 generator-only fallback：

- dataset 以 paper 的 CC BY-NC-SA 4.0 為保守依據；repo 同時出現 Apache-2.0，且 upstream license manifest 未 pin。
- cross-domain split 同時改 source、speaker、generator，有些語言也改 generator set。
- English/German/Russian/Spanish targets 使用 M-AILABS；其 LibriVox audiobook lineage 與 LibriSpeech 的 speaker／book／utterance overlap 未排除，故 LS960 backbone 對這些 slices 暫不 clean。
- 若切 XMAD，需把 estimand 改寫為 compound domain transfer；若仍主張 generator-isolated，須先做 controlled split 與 overlap audit。

## 必改 4：§16.7／§19 citations

- Kwok 是兩篇：ICASSP 2025 **“Robust Audio Deepfake Detection using Ensemble Confidence Calibration”**, DOI `10.1109/ICASSP49660.2025.10889972`；Interspeech 2025 **“Bona fide Cross Testing Reveals Weak Spot in Audio Deepfake Detection Systems”**, DOI `10.21437/Interspeech.2025-172`。依主張分開引用。
- Zhou & Wang 全名：**“When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors”**，arXiv:2606.21584 v1，2026-06-19；標為 preprint。
- Xu, Pu & Zhao：**“Knowledge Distillation with a Precise Teacher and Prediction with Abstention”**，ICPR（官方 conference title 含 2020），pp. 9000–9006，DOI `10.1109/ICPR48806.2021.9412696`；建議 publication year 2021。

完整 evidence map、來源 URL、checkpoint rejection table、XMAD split/backbone matrix 與 stop conditions都在兩份正式 artifact。
