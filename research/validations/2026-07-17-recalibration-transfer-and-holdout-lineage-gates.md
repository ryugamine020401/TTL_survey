# D1-P red-team 後兩項 gate：重新校準轉移與 holdout lineage

日期：2026-07-17  
模式：Validate  
問題：回覆 Claude `2026-07-17-2340-redteam-provisional-topic` 要求的兩項小查證，並判斷是否採納 H1/H2 sharpening。  
狀態：文獻與公開 metadata gate 完成；未下載 ASVspoof 5 音訊、未執行 pilot。

## 結論

1. **採納主體，但修正一處論理。** AUROC 與 eAURC 都涉及排序，卻不是同一個排序問題：AUROC 衡量類別 score 對真／假的排序，eAURC 衡量 confidence 對「預測是否正確」的排序。因此「AUROC matched、eAURC 不同」並非自相矛盾。不過，若部署主張是 source-fixed `(q,t)` transfer，主假設仍應收斂到 **absolute score scale／calibration transfer**；eAURC 留作 secondary diagnostic 或 matching constraint。
2. **`ordinary KD + source-dev temperature scaling` 是強制 kill baseline，但其結果未知。** 相鄰領域的可信證據指出：只在 source/i.i.d. dev 擬合的 post-hoc calibration 經常在 distribution shift 下不足；另一方面，vision/text 的 KD 研究也證明 calibration 有時可以轉移。因此不能預設 baseline 會輸，H2 必須實際打贏它。
3. **ASVspoof 5 C00 是較適合的主要 holdout 候選。** 排除 adversarial attack 與 legacy waveform-concatenation，再將 A21/A22 視為同一 ToucanTTS 架構 family，保守得到約 **7 個可用 architecture families**。DFADD 只有 5 個具名 TTS families，且有固定文本／來源 shortcut 與已修正的 label-release 問題，宜降為 exploratory replication。
4. **7 families 仍是小叢集數。** 可作 generator-family-macro 的 bounded evidence，逐 family 報告並以 family bootstrap／hierarchical uncertainty 顯示寬區間；不應用 utterance-level p-value 宣稱普遍方法優越。

## 重要的實驗公平性修正

不能把 teacher 的同一組數值門檻直接套在 student 上，否則不同 score scale 會製造近乎必然的失敗。公平 estimand 是：

1. 每個模型只用同一個 source train/dev；
2. 對每個模型分別擬合 source-dev calibration，並在相同 source operating constraint 下決定其 `(q_m,t_m)`；
3. 凍結 calibration 與 `(q_m,t_m)`，不看 holdout label；
4. 在 unseen-generator holdout 比較 generator-macro confident-real leakage、coverage 與 risk violation。

Temperature scaling 是 monotonic transform，所以不改變 AUROC，也不改變以相同 score 排序所得的 risk–coverage ordering；它會改變固定 probability threshold 對應的 raw-score cutoff。因此它正適合區分「排序保留」與「absolute operating point 不轉移」。若 binary score 同時有 offset shift，只有 scalar temperature 可能太弱，應把 source-dev affine/Platt scaling 列為 sensitivity baseline，不能把 TS 失敗直接解讀成所有簡單 recalibration 都失敗。

## Gate 1：source-dev recalibration 在 shift 下能否轉移？

### 查證範圍

查找 compression／KD、post-hoc calibration、domain shift 與 audio deepfake detection 的交集；以原始論文、官方 proceedings 與作者頁為主。查詢包括 `knowledge distillation calibration transfer distribution shift`、`temperature scaling source domain distribution shift`、`audio deepfake temperature scaling`、`speech anti-spoofing temperature scaling`。截止 2026-07-17，在檢查到的 ADD 原始工作中，未找到直接測試「輕量化 student + source-dev TS + unseen-generator source-fixed selective threshold」的研究；這是 search-scope no-hit，不是不存在的證明。

### 支持與反證

| 證據 | 狀態 | 與本題的意義 |
|---|---|---|
| Ovadia et al., *Can You Trust Your Model's Uncertainty?*, NeurIPS 2019 | published | 大規模 dataset-shift 評估顯示傳統 post-hoc calibration 在 shift 下不足；支持 TS 不能被當作已知解法。 |
| Yu et al., *Robust Calibration with Multi-domain Temperature Scaling*, NeurIPS 2022 | published | ordinary calibration 在 mild shift 下也可能失效；需要多 source-domain 結構。這支持 source-only TS 是強 baseline，但非可靠上界。 |
| Wang et al., *TransCal*, NeurIPS 2020 | published | target-domain calibration 需要額外 adaptation 假設／未標記 target 資訊；與本題「完全凍結 source」不同。 |
| Gong et al., *Confidence Calibration for Domain Generalization under Covariate Shift*, ICCV 2021 | published | multi-source set/cluster-level calibration 優於單純 source calibration；說明 shift-aware calibration 本身是方法空間與可能 collision。 |
| Hebbalaguppe et al., *Calibration Transfer via Knowledge Distillation*, ACCV 2024 | published | calibrated teacher 的 calibration 在部分 vision 設定可藉 KD 傳給 student；反駁「KD 必然破壞 calibration」。但它不是 unseen-generator、compression/channel 或 fixed-threshold protocol。 |
| Reich et al., *An Overview of Uncertainty Calibration for Text Classification and the Role of Distillation*, ACL workshop 2021 | workshop | text 分類中 distillation／recalibration 有時改善 OOD calibration；再次說明 baseline 結果不能預設。 |
| Pascu et al., *Towards generalisable and calibrated audio deepfake detection with self-supervised representations*, Interspeech 2024 | published | 在外部資料報 ECE 與 accuracy–rejection，但使用 frozen SSL + logistic regression；未檢查 lightweight transformation 後的 source-dev TS threshold transfer。 |
| *Improving Robustness of Deepfake Audio Detection through Confidence Calibration*, DADA@IJCAI 2023 | workshop | 以 EOW-Softmax 與 augmentation 改善 ADD confidence；不是 source-dev temperature scaling，也不是 compression/KD transfer。 |

主要來源：

- [Ovadia et al., NeurIPS 2019](https://proceedings.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html)
- [Multi-domain Temperature Scaling, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b054fadf1ccd80b37d465f6082629934-Abstract-Conference.html)
- [TransCal, NeurIPS 2020](https://papers.nips.cc/paper_files/paper/2020/hash/df12ecd077efc8c23881028604dbb8cc-Abstract.html)
- [Domain-generalization calibration, ICCV 2021](https://openaccess.thecvf.com/content/ICCV2021/papers/Gong_Confidence_Calibration_for_Domain_Generalization_Under_Covariate_Shift_ICCV_2021_paper.pdf)
- [Calibration Transfer via Knowledge Distillation, ACCV 2024](https://openaccess.thecvf.com/content/ACCV2024/html/Hebbalaguppe_Calibration_Transfer_via_Knowledge_Distillation_ACCV_2024_paper.html)
- [Distillation and calibration overview, ACL 2021](https://aclanthology.org/2021.repl4nlp-1.29/)
- [Pascu et al., Interspeech 2024](https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.pdf)
- [DADA@IJCAI 2023 confidence calibration](https://ceur-ws.org/Vol-3597/paper12.pdf)

### Gate 1 verdict

**Verified:** source-dev TS 不是已知能跨任意 shift 轉移的通用修法。  
**Verified:** KD 也不是已知必然破壞 calibration；部分鄰近研究能轉移或改善它。  
**Inference:** 在 ADD unseen-generator shift 中，`ordinary KD + source-dev TS` 可能部分修復，也可能因 target-dependent miscalibration 而失敗；目前無直接證據可預告結果。  
**Recommendation:** 將它列為 H1b 的 trivial-repair gate 與 H2 的強制 baseline；另加 Platt/affine scaling sensitivity。若任一簡單 recalibration 與 H2 等效，kill H2。

## Gate 2：DFADD 與 ASVspoof 5 的可用 generator families／lineage

### DFADD

- **Verified:** 5 個具名 TTS systems：Grad-TTS、NaturalSpeech2、StyleTTS2、Matcha-TTS、PFlow-TTS；大致為 3 diffusion + 2 flow-matching systems。
- **Verified:** corrected 2025-04 release 修正 Matcha-TTS 檔案／label mismatch；使用時必須鎖定 corrected release、hash 與 manifest。
- **Risk:** real 主要基於 VCTK，而 synthetic content／input 與 LJSpeech 固定文本關聯，容易把 source、speaker、文本或 corpus shortcut 誤認成 generator generalization。
- **Statistical limit:** generator-family macro 的 cluster 數約 5，不足以支撐強方法普遍性；適合 cheap exploratory audit 或跨資料集 sensitivity。

來源：[DFADD paper](https://arxiv.org/abs/2409.08731)、[official repository](https://github.com/isjwdu/DFADD)。

### ASVspoof 5 evaluation subset

- **Verified:** 全 benchmark 有 32 attacks；evaluation 有 9 個 non-adversarial TTS/VC systems 與 7 個 adversarial attacks。
- 本題 threat model 排除 adversarial attacks A18/A20/A23/A27/A30/A31/A32。
- 排除 A19 MaryTTS unit-selection／waveform concatenation，因其為 legacy attack lineage，與「當代 neural generator」主張不一致。
- 剩餘 8 attack IDs：A17、A21、A22、A24、A25、A26、A28、A29。
- A21/A22 都是 ToucanTTS + BigVGAN 的相近配置，保守合併後為 **7 個 architecture families**：
  1. A17 ZMM-TTS
  2. A21/A22 ToucanTTS + BigVGAN
  3. A24 PPG/ECAPA/HiFiGAN VC
  4. A25 DiffVC
  5. A26 wav2vec/F0/CAM++/HiFiGAN VC
  6. A28 YourTTS/VITS
  7. A29 XTTS
- **Shortcut control 較好:** benchmark 以 MLS English 為主要 source，使用 speaker-disjoint partitions，並移除與 LibriSpeech 重疊的 evaluation source speakers；官方也對 peak amplitude、leading/trailing silence、duration 與 energy 等 shortcut 做處理。
- **仍未完全乾淨:** A17 有少量 target-speaker identity overlap（官方報告無 utterance overlap）；A17/A28/A29 的 pretrained checkpoint 與外部訓練資料 lineage 還要另做 L0–L5 audit；共同 MLS source 仍限制外部效度。
- **Channel 選擇:** 主要 generator holdout 先用 C00（uncompressed 16 kHz），C01–C11 另作 secondary channel shift，避免把 generator 與 codec 效應混在同一主分析。
- **License:** Zenodo 標示 Open Data Commons Attribution 1.0；該 license 主要覆蓋 database rights，不等於自動釐清每段 audio/content 的全部權利，仍須記錄 MLS/LibriVox component 條款與 attribution。
- **Resource constraint:** 完整資料約 142 GB，本 gate 僅查 paper／metadata；未下載。

來源：[ASVspoof 5 database paper](https://arxiv.org/pdf/2502.08857)、[official Zenodo record](https://zenodo.org/records/14498691)、[bundled ODC-By license](https://zenodo.org/records/14498691/preview/LICENSE.txt?include_deleted=0)。

### Gate 2 verdict

| 候選 | 保守可用 family 數 | lineage／shortcut 判斷 | 角色 |
|---|---:|---|---|
| DFADD corrected release | 5 | 固定文本／source shortcut 風險較高；release correction 必須鎖定 | exploratory replication |
| ASVspoof 5 C00 selected eval | 7（8 IDs） | 控制較完整，但 pretrained lineage 與少量 speaker overlap 待 audit | primary holdout candidate |

ASVspoof 5 勝出，但不是「lineage 已通過」。Phase 0 還要以 protocol manifest 實際核對 C00 sample counts、attack IDs、speaker/content overlap、checkpoint training corpora、授權與 hashes，才可解鎖 pilot。

## 修正後假設與 kill sequence

- **H1a（phenomenon）:** 在 AUROC 與 eAURC 落在預先容許差內時，ordinary lightweight student 各自以 source-dev 決定並凍結的 `(q_m,t_m)`，在 unseen generator 上有較差的 generator-macro confident-real leakage／risk violation。
- **H1b（trivial repair）:** source-dev TS（加 Platt sensitivity）不能把 ordinary KD 修復到 teacher 的 external operating reliability。若能，停止設計 H2。
- **H2（method）:** 只有 H1a 與 H1b 都成立，才測試一個超過 soft-label confidence imitation 的 mechanism，並要求它同時勝過 ordinary KD、KD+TS 及 KD+Platt sensitivity，在 matched discrimination、latency、parameter budget 下成立。

## 未解問題與下一個最小步驟

1. **Unknown:** 7 families 是否足以達到預期最小可辨識 effect；需在看到每 family 樣本數與 pilot-free variance assumption 後做 simulation-based power／precision analysis。
2. **Unknown:** ASVspoof 5 C00 protocol 中每 attack/family 的實際可用數與重複 codec 配置；先下載小型 protocol/metadata（非 142 GB audio）並建立 manifest，仍需作者授權任何下載。
3. **Unknown:** H2 的 exact method 是否與 domain-generalization calibration、selection consistency 或 DK-CAST collision；H1b 通過後再做 method-specific closest-work gate。
4. **Stop/pivot:** H1a 不成立，kill D1-P；H1b 不成立但簡單 recalibration 已足夠，將結果降為部署 protocol／negative result，並依作者不接受純量測的偏好回到其他候選；H2 打不贏 recalibration，同樣 kill method claim。
