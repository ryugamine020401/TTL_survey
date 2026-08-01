# ASVspoof 5 / XMAD-Bench lineage manifest 擴充

- 日期：2026-07-18
- 模式：Validate
- 問題：ASVspoof 5 C00 holdout 在換用 LS960-only backbones 後能否進 Phase 0？XMAD-Bench 是否真能作免申請、可切換 fallback？
- 證據基礎：官方 evaluation plan、ASVspoof 5 paper、官方 Zenodo protocol、生成器原始論文；XMAD-Bench paper／repository／dataset card。未下載音訊或模型。

## Executive verdict

- **ASVspoof 5：CONDITIONAL GO。** 精確 LS960-only backbone 的 upstream corpus 對 holdout 的 speaker-overlap 已由官方去除規則解決；C00 counts 也已由官方 protocol 重算。仍須完成「整個 teacher」的 checkpoint/hash/fine-tuning lineage 與音訊層 shortcut probes，才可解除 Stage 0.2。
- **XMAD-Bench：CONDITIONAL compound-shift fallback。** 它是 direct-access 且很新，但 cross-domain split 同時改變 source corpus、speaker、generator，部分語言還改變 generator set；M-AILABS 與 LibriSpeech 同為 LibriVox audiobook lineage，speaker／utterance overlap 未證。它不是 ASVspoof 5 generator-isolated confirmatory test 的無縫替代品。

## 1. ASVspoof 5 protocol provenance

| 項目 | 已固定值 |
|---|---|
| protocol release | Official Zenodo record 14498691 |
| archive | `ASVspoof5_protocols.tar.gz`，約 20.7 MB；未下載 audio |
| official archive MD5 | `865D0E894EA9F686F0F37E5AE3AE3616`，本地驗證 PASS |
| Track-1 evaluation protocol | `ASVspoof5.eval.track_1.tsv` |
| protocol SHA-256 | `62CC6D5E30EB7624AB348EA21713CCE5D814299D723B4CE789EC9C1CF18611F2` |
| full eval row count | 680,774（與官方 README 一致） |
| C00 definition | `CODEC=-`, `CODEC_Q=0`；no encoding，16 kHz |

來源：[ASVspoof 5 Zenodo](https://zenodo.org/records/14498691)、[dataset paper](https://arxiv.org/html/2502.08857)。

## 2. C00 selected-family counts（由官方 TSV 重算）

| attack | utterances | protocol speakers | attack conditions |
|---|---:|---:|---|
| A17 | 8,662 | 367 | AC1, AC2, AC3 |
| A21 | 8,650 | 367 | AC1, AC2, AC3 |
| A22 | 8,645 | 367 | AC1, AC2, AC3 |
| A24 | 8,644 | 367 | AC1, AC2, AC3 |
| A25 | 8,658 | 367 | AC1, AC2, AC3 |
| A26 | 8,653 | 367 | AC1, AC2, AC3 |
| A28 | 8,662 | 367 | AC1, AC2, AC3 |
| A29 | 8,659 | 367 | AC1, AC2, AC3 |
| **selected spoof total** | **69,233** | — | — |
| **A21+A22 merged family** | **17,295** | 367 each | 預註冊為同 architecture family |
| **C00 bona fide** | **35,149** | **737** | — |
| **entire C00** | **171,602** | — | 所有 attack + bona fide |

**Inference：**utterance 數足夠做每-family precision，但獨立的 unseen architecture family 約只有 7 群；大量 utterance 不能消除 cluster 數偏小的推論限制。

## 3. Backbone pretraining corpora → holdout overlap

| exact backbone | pretraining corpus | holdout source | speaker overlap | utterance overlap | verdict |
|---|---|---|---|---|---|
| `facebook/wav2vec2-base` | LibriSpeech 960 h | ASV5 eval 源自 MLS English／LibriVox | 官方移除 eval 中所有 LibriSpeech-overlap speakers | speaker 已 disjoint 即排除同-speaker utterance；未另發布逐檔 cross-corpus hash | **PASS under official plan** |
| `facebook/hubert-base-ls960` | LibriSpeech 960 h | 同上 | 同上 | 同上 | **PASS under official plan** |
| `microsoft/wavlm-base` | LibriSpeech 960 h | 同上 | 同上 | 同上 | **PASS under official plan** |
| XLS-R | multilingual mixture 含 MLS | 同上 | MLS source overlap | 可能直接／近直接 overlap | **FAIL** |
| LL60k／WavLM Base+ | 含 LibriLight；LibriVox-derived | 同上 | 未可排除，且 plan 明文禁止 | 未可排除 | **FAIL** |

**Verified：**ASVspoof 5 paper 說 eval speakers 中出現在 LibriSpeech 者已移除；evaluation plan 因此明文允許 LibriSpeech-pretrained models。這是官方 protocol-level overlap control，不是 Codex 以姓名相似度作的推測。

完整 backbone 證據與 checkpoint 限制見 `research/validations/2026-07-18-backbone-lineage-and-citation-audit.md`。

## 4. Attack-generator upstream lineage

| family | training／pretraining lineage | target speaker／utterance overlap | manifest 判定 |
|---|---|---|---|
| A17 | off-the-shelf ZMM-TTS；含 10 target + 2 non-target eval speakers 的約 2.4k training utterances | **speaker overlap 已知**；paper 說無 utterance overlap，speaker overlap <2% | **special sensitivity family**；結果須同時報含／不含 A17 |
| A21+A22 | ToucanTTS variants；ASV5 提供的 disjoint TTS/VC training protocol | 官方設計為與 eval speaker-disjoint | **PASS**；合併成一 architecture family |
| A24 | ASV5 disjoint training protocol | speaker-disjoint | **PASS** |
| A25 | ASV5 disjoint training protocol | speaker-disjoint | **PASS** |
| A26 | ASV5 disjoint training protocol | speaker-disjoint | **PASS** |
| A28 | pre-trained YourTTS；多語料、多語言；H/ASP speaker encoder pretrained on VoxCeleb2 | authors report no ASV5-eval speaker overlap；逐 utterance hash 未公開 | **PASS with stated evidence** |
| A29 | pre-trained XTTS；public + internal multilingual data；英文含約 1,812.7 h LibriLight 與 541.7 h LibriTTS-R | ASV5 paper 未證 no-overlap；XTTS internal data 亦不可獨立 audit | **UNKNOWN / not lineage-disjoint**；保留作現實 off-the-shelf threat，但不可宣稱全 attack lineage clean |

來源：[ASVspoof 5 paper](https://arxiv.org/html/2502.08857)、[XTTS paper](https://arxiv.org/html/2406.04904)。A29 生成器用過 LibriLight 不等於 detector backbone 洩漏；兩者是不同 exposure path，但必須分欄揭露。

## 5. ASVspoof 5 license、shortcut 與 gate 狀態

| gate | 狀態 | 證據／待辦 |
|---|---|---|
| direct access | PASS | Zenodo 公開下載，無人工申請；音訊仍依作者授權才下載 |
| labels/protocol | PASS | eval protocol 已公開；hash 與 selected-family counts 已固定 |
| dataset license | PASS for planned academic use, attribution required | Zenodo 標示 ODC-By 1.0；仍應保存 release citation／license copy |
| backbone upstream overlap | PASS at exact base-checkpoint level | 只限三個 LS960-only checkpoint；完整 fine-tuned teacher 尚未 PASS |
| attack family lineage | PARTIAL | A17 已知 speaker overlap；A29 external lineage Unknown |
| metadata shortcut mitigation | VERIFIED | 官方已處理 peak amplitude、silence、duration、average energy 等捷徑 |
| empirical audio shortcut probes | PENDING | 需音訊後驗證 duration、silence、level、codec/container、source fingerprints 與 label predictability |

### ASV5 Stage 0.2 entry contract

必須全部成立：

1. 固定 exact teacher base model id、revision、權重 SHA-256、ADD fine-tuning data 與所有 external components；每層皆無 forbidden corpus。
2. 以 protocol 預註冊 C00、selected attacks、A21+A22 family merge、A17 include/exclude sensitivity、A29 lineage caveat。
3. 作者授權必要音訊 shard 後完成 shortcut probes；任一非語音捷徑能高準確預測 label／family 且無法控制，即停用該 slice 或 pivot。
4. teacher reproduction／quality gate 通過；clean lineage 不能取代模型品質。

## 6. XMAD-Bench audit

### 6.1 Access 與 license

- **Verified：**paper §9 將 XMAD-Bench 以 CC BY-NC-SA 4.0 分享。
- **Contradiction：**GitHub README 對 source code／models 寫 CC BY-NC-SA 4.0，但 repository 的 LICENSE／badge 為 Apache-2.0；Hugging Face card 又缺正式 YAML license metadata。
- **Inference：**dataset 應以 paper 的 CC BY-NC-SA 4.0 為保守依據。非商業學術 thesis 大致符合 stated purpose，但需 attribution／share-alike 與 upstream terms；這不是法律意見。
- **Unknown：**paper 說 upstream sources 允許非商業研究與衍生物，但沒有 pinned source-version/license manifest；MASC／YouTube provenance 尤其需要補件。

來源：[XMAD-Bench paper](https://arxiv.org/html/2506.00462)、[repository](https://github.com/ristea/xmad-bench)、[dataset card](https://huggingface.co/datasets/unibuc-cs/XMAD-Bench)。

### 6.2 Cross-domain split confounding

| language | source train → cross-domain real source | cross-domain size／speakers | generator coverage | confound verdict |
|---|---|---|---|---|
| Arabic | Common Voice → MASC | 12,984／1,502 | XTTSv2 only | source + speaker + generator setting 同變 |
| English | Common Voice → M-AILABS | 39,690／3 | multiple | 極少 speakers；source + speaker + generator 同變 |
| German | Common Voice → M-AILABS | 3,100／5 | multiple | 同上 |
| Mandarin | Common Voice → AISHELL-3 | 2,002／95 | 3 methods | source + speaker + generator set 同變 |
| Romanian | Common Voice → VoxPopuli | 6,672／38 | VITS + OpenVoice only | source + speaker + generator set 同變 |
| Russian | Common Voice → M-AILABS | 34,702／3 | VITS + OpenVoice only | 極少 speakers；多重 shift |
| Spanish | Common Voice → M-AILABS | 3,070／3 | multiple | 極少 speakers；多重 shift |

Paper 在各來源內以相同 text／speaker 配 real 與 fake，這能降低 slice 內最直接的 label-vs-source confounding；但 cross-domain 評估仍同時改變 real-source、speaker、generator，有時也改變可用 generator set。因此觀察到的失敗不能唯一歸因為 unseen generator。

### 6.3 LS960 backbone → XMAD target overlap

| XMAD target source | 與 LibriSpeech corpus identity | speaker／utterance overlap | verdict for LS960 backbones |
|---|---|---|---|
| MASC／YouTube | corpus-disjoint | 未提供可比對 manifest；推測較低但未證 | **PARTIAL / Unknown IDs** |
| AISHELL-3 | corpus-disjoint、Mandarin | 未提供 cross-corpus ID/hash；實務風險低 | **PARTIAL** |
| VoxPopuli | corpus-disjoint | 未提供 cross-corpus ID/hash | **PARTIAL** |
| M-AILABS | 與 LibriSpeech 同屬 audiobook／LibriVox lineage | speaker、book、utterance overlap 未排除 | **FAIL until audited** |

**關鍵結果：**英文、德文、俄文、西文 cross-domain targets 都用 M-AILABS，所以 LS960 backbone 不能在沒有 speaker/book/audio-hash audit 時被稱為 XMAD-lineage-clean。非 M-AILABS 的 Arabic／Mandarin／Romanian 較安全，但會改變語言與 estimand，且仍有多重 split confounding。

## 7. 可切換 fallback contract

XMAD 只有在以下兩種寫法之一成立時才可啟用：

1. **Compound-shift fallback（現在可預先指定）：**明確把 RQ 改成 source-frozen selective policy 在 real-source + speaker + generator compound shift 下的 transfer；不得沿用「generator-isolated」因果語句。
2. **Controlled fallback（尚未完成）：**取得 release-level source IDs／speaker IDs／content hashes，排除 LS960 overlap，並設計能把 generator 與 source/speaker shift 分開的配對或分層 protocol。

若堅持英文且保留 generator-isolated claim，M-AILABS lineage Unknown + split confounding 是 **NO-GO**。若接受更窄的 compound-shift claim，可優先考慮 Arabic／Mandarin／Romanian slices，但需預註冊各語言是獨立 setting，不能把語言數當作獨立 generator-family 數。

## 8. Recommendation、kill criteria、未解不確定性

- **Recommendation：**保留 ASVspoof 5 C00 為 primary；XMAD-Bench 降格成條件式 compound-shift fallback／secondary robustness evidence。
- **ASV5 下一步：**先完成 teacher full-lineage manifest；只有作者授權後才下載最小必要 audio shards，作 shortcut probes。
- **XMAD 下一步：**先向 repository／metadata 找 release-pinned license、speaker/book/source identifiers；不需先下載 61 GB audio。
- **Kill ASV5：**完整 teacher lineage 無法排除 forbidden corpora，或 audio shortcut probe 顯示無法控制的 label/family shortcut。
- **Kill XMAD as generator-only confirmatory：**無法拆開 source/speaker/generator shifts，或 M-AILABS 與 LS960 overlap 無法排除。

未解項：A29 internal data、XMAD upstream pinned licenses／IDs、M-AILABS vs LibriSpeech speaker/book/audio overlap、音訊層 shortcut 實測。這些 Unknown 必須保留，不得以「資料很新」代替驗證。

## Project-state 影響

題目方向維持 GO；ASVspoof 5 規格由「XLS-R hard blocker」推進為「LS960-only backbone 可解，但完整 teacher／shortcut gates 未解」的 CONDITIONAL GO。XMAD 不應在共識文件中稱作等價 fallback。待作者接受這份 contract 並由 Claude 統整 plan 後，再更新 `PROJECT.md`／`TASKS.md`；本次不改 `DECISIONS.md`。
