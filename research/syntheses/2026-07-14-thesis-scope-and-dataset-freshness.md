# 碩士論文方向收斂與資料集新鮮度策略

- 日期：2026-07-14
- 研究模式：Synthesize + Compare + Validate
- 狀態：候選方向建議，尚未代表作者正式決策
- 主要依據：`PROJECT.md`、`DECISIONS.md`、`TASKS.md`、`discussions/legacy/2026-07-14-convergence/04-final-five-directions.md`、相關原始論文與官方資料集頁面

## 1. 本文件要回答的問題

1. 五個候選方向中，哪些能收斂成一年內、單張 RTX 4090、無人體實驗的碩士論文？
2. 第一候選方向應如何縮小，才不會同時做模型、跨域、攻擊、通道與使用者介面？
3. 在語音生成快速進步的情況下，如何讓資料集夠新，又不犧牲可重現性、授權與實驗可控性？

## 2. 結論先行

### 2.1 建議的第一候選題目

**中文暫定題目**

> 未知生成器下語音深偽偵測的可信棄權：不確定性排序與失效邊界的跨資料集研究

**英文暫定題目**

> Reliable Abstention for Audio Deepfake Detection under Unseen Generators: Cross-Dataset Uncertainty Ranking and Failure Boundaries

**一句話研究問題**

> 當測試語音來自訓練時未見、且時間上更新的生成器時，現有偵測器能否用可轉移的不確定性分數，在高風險樣本上選擇棄權，從而降低已接受預測的錯誤率？

### 2.2 為何還需要再縮小

`04-final-five-directions.md` 中排名第一的版本，同時包含：

- 生成器偏移；
- 通訊通道偏移；
- 六種不確定性方法；
- 三種偵測器；
- 十二個 shift cells；
- 對抗式 confident-real 攻擊。

**Inference：** 即使估計 GPU 時數尚可，這仍是多個研究問題疊在一起。真正的風險不是算力，而是實驗矩陣、校準決策、資料洩漏檢查與論文敘事都會膨脹。

因此，核心論文只保留：

- 一種主要 shift：**未見生成器／跨資料集偏移**；
- 兩個公開、可重現的偵測器；
- 三類分數：原始信心基線、校準後信心、至多一種較強的不確定性方法；
- 一個固定開發資料來源、兩個外部測試來源；
- risk–coverage、selective risk、AUROC/EER 與 calibration error；
- 不做人體實驗、不做完整通道矩陣、不在核心研究中做攻擊搜尋。

通道或對抗攻擊只能選一個作為 **stretch experiment**，而且只有在核心結果完成後才啟動。

### 2.3 資料集策略的核心判斷

「越新越好」只對了一半。更精確的原則是：

> **越新的資料，越應該放在外部測試與最終 holdout，而不一定適合拿來訓練。**

舊資料仍有兩個不可替代的用途：提供文獻可比較的基準，以及形成明確的時間差。若訓練、校準與調參都使用最新資料，就無法回答「遇到更晚、未見生成器時是否可信」。

## 3. 五個方向的收斂結果

| 優先序 | 收斂後方向 | 核心貢獻 | 主要風險 | 建議 |
|---|---|---|---|---|
| 1 | 未知生成器下的可信棄權 | 把偵測問題改寫成「何時不應自信作答」，衡量閾值能否跨新生成器轉移 | 與 FADEL、校準及 OOD 文獻的差距仍需完整查證 | 主候選；先做最小可否證 pilot |
| 2 | 有界黑箱洗白的最低攻擊成本 | 不只問攻擊是否成功，而是量化進入 confident-real 區域所需的最小成本 | 泛化的 laundering benchmark 已與 CLAD 等工作重疊 | 安全研究備選；必須限制攻擊集合與深度 |
| 3 | 華語語音中時長 × 情緒的交互失效 | 檢驗短句與情緒是否形成非加成式失效，而非做另一個平均準確率比較 | 情緒語料、TTS 配對與混雜控制困難 | 資料中心備選；限兩個因素，不加入詐騙語意與通道 |
| 4 | 真實通訊與模擬通道的樂觀偏差 | 測量常用 channel simulation 是否高估真實 RTC 表現 | RTCFake 等新工作已直接進入此場景；平台資料取得與重播成本高 | 只有在能取得成對 real/simulated data 時考慮 |
| 5 | 語音浮水印的可靠位元容量 | 在明確通道與延遲限制下，測量真正可保留的 payload | AudioMarkBench、CallShield 等使一般性「浮水印更穩健」題目擁擠；系統工程重 | 不建議作目前主題，除非已有現成管線與明確標準問題 |

## 4. 候選研究卡

### 4.1 候選一：未知生成器下的可信棄權

**研究問題**

- RQ1：哪些不確定性分數在未見生成器上仍能把錯誤樣本排到高風險區？
- RQ2：在開發集選定的棄權閾值，轉移到更新的外部資料集後，是否仍能滿足預先設定的 accepted-risk 上限？
- RQ3：不同偵測器是否在相同資料上呈現一致的失效邊界，還是棄權能力高度依賴模型？

**可否證假設**

- H1：至少一種非原始 softmax 的分數，在兩個外部測試集上都顯著改善 risk–coverage curve。
- H2：在開發集固定的閾值，可在外部資料上以可接受的 coverage 代價降低 accepted error。
- H3：新生成器造成的「高信心錯誤」比例，能被明確量化，且不同模型不完全相同。

**最小方法**

- 模型：2 個，例如 AASIST 與一個 frozen SSL front-end + 輕量分類頭。
- 分數：MSP／logit baseline、temperature-scaled confidence、1 種 embedding 或 ensemble 型分數。
- 資料：1 個 train/dev 錨點 + 2 個外部測試集；generator-disjoint split 必須在資料層明確定義。
- 重複：3 seeds；主要分析先固定，不因最終 holdout 結果追加調參。

**需要的證據**

- 所有主要結論須同時報告 detection performance 與 selective performance。
- 閾值只可由開發集決定；外部測試集不得用於方法選擇。
- 報告 bootstrap confidence interval，並分 generator family、語言或來源做診斷。

**失敗條件**

- 所有較複雜分數都不優於原始信心；
- 閾值跨資料集完全失效，無法達到風險控制；
- 結果主要由語言、音質或資料來源捷徑解釋，而非生成器偏移。

**有用的負結果**

> 現有偵測器的不確定性無法可靠轉移到較新生成器，因此不能把「低 confidence」直接當作部署時的安全閥。

### 4.2 候選二：有界黑箱洗白的最低攻擊成本

**暫定題目**

> 語音深偽偵測器的有界黑箱洗白：進入高信心真人區域的最低轉換成本

**研究問題與假設**

- RQ：攻擊者在查詢有限、轉換品質有下限時，需要多少次、何種組合的常見音訊處理，才能讓 deepfake 進入 confident-real 區域？
- Hypothesis：原始 detector score 的最低逃逸成本，低於使用可信棄權機制後的最低逃逸成本。

**最小方法**

- 2 個偵測器、2 個資料來源；
- 最多 6 種可解釋轉換；組合深度不超過 2；
- 固定查詢預算；
- 主要輸出為成功率—成本曲線，不追求全攻擊目錄。

**失敗條件／有用負結果**

- 若單一低成本轉換已對所有模型奏效，研究仍可揭露共同脆弱點；
- 若攻擊幾乎無法成功，則得到特定 threat model 下的實證韌性邊界。

### 4.3 候選三：華語時長 × 情緒交互失效

**暫定題目**

> 華語語音深偽偵測中的短句與情緒交互失效：跨生成器的控制實驗

**研究問題與假設**

- RQ：短時長與高情緒表達是否造成非加成式的偵測退化？
- Hypothesis：短句 × 高情緒條件的退化大於兩個主效應的相加，且在未見生成器上更明顯。

**最小方法**

- 只保留時長與情緒兩個因素；
- 使用同文本或近似配對設計，控制說話者、文字內容、取樣率與 loudness；
- 2 個偵測器、1 個可重現語料來源與少量新 TTS 生成器。

**失敗條件／有用負結果**

- 若交互作用不存在，可否定「詐騙式短情緒句是獨特技術盲點」的假設；
- 若退化由語料來源可完全解釋，則停止把它宣稱為情緒效應。

### 4.4 候選四：真實與模擬通道的樂觀偏差

**暫定題目**

> 語音深偽偵測的通道模擬是否過度樂觀？真實 RTC 與配對模擬條件的比較

**最小方法**

- 問題只限「同一原始音檔的真實 RTC 與模擬轉碼是否等價」；
- 1–2 個平台或使用 RTCFake 的成對設計；
- 2 個 detector，不做平台大全。

**停止條件**

- 無法取得合法、成對且可重現的 real/simulated 音檔；
- RTCFake 已完整回答同一比較，而沒有可辨識的 residual gap。

### 4.5 候選五：可靠位元容量

**暫定題目**

> 低延遲通訊限制下神經語音浮水印的可靠位元容量

**最小方法**

- 固定 2 個開源 watermark system；
- 固定 1 個通道族與 1 個延遲限制；
- 衡量 payload、bit error rate、音質與延遲的 Pareto frontier。

**停止條件**

- 無法在一個月內重現至少一個現有系統；
- 研究問題最後仍只是重做 AudioMarkBench 的 robustness table。

## 5. 資料集「新鮮度」不能只看發表年份

每個資料集至少要分開記錄四個日期：

1. **資料生成／蒐集日期**：最接近真實威脅時間。
2. **生成模型的發布日期與版本**：判斷是否真的代表新一代生成器。
3. **資料集版本發布日期**：可能只是舊資料重新打包。
4. **論文發表日期**：最容易取得，但最不應單獨當作新鮮度代理。

此外還需記錄：

- generator family、checkpoint／商用服務名稱與版本是否可知；
- 語言、說話者、文本與來源；
- 是否經過 codec、社群平台、RTC 或其他 laundering；
- 授權、用途限制、是否需申請與可否重散布；
- real/fake 標註的建立方式與不確定性；
- 與訓練資料、預訓練模型及其他 benchmark 的可能重疊；
- 固定版本、檔案雜湊、下載日期與實際儲存量。

## 6. 截至 2026-07-14 的候選資料盤點

| 資料來源 | 新鮮度與用途 | 存取／授權 | 對本論文的角色 | 目前判定 |
|---|---|---|---|---|
| ASVspoof 2019 LA / 2021 DF | 舊，但有高度可比性與成熟 protocol | 官方公開；2021 頁面提供 ODC Attribution 資料 | 訓練或歷史錨點，不作「當代威脅」證據 | **Verified：保留，但降級為 anchor** |
| ASVspoof 5 | 2023–2024 challenge，規模與攻擊來源較新 | 官方頁面與 Zenodo 可下載；資料庫採 ODC Attribution，但內容權利仍需個別注意 | 現代化 train/dev 候選 | **Verified：可取得；仍要做 overlap 與容量稽核** |
| MLAAD v9 | 官方頁面目前列出逾 1000 小時、50+ 語言、175+ TTS；版本持續演進 | CC BY-NC 4.0；假音訊需搭配 M-AILABS real audio | generator-disjoint 開發集或受控外部測試 | **Verified：很適合做版本化子集，不宜默認全量** |
| DFADD | diffusion／flow-matching TTS；官方資料在 2025-04 修正標籤並更新 ZIP | 官方 GitHub／HF；repo 為 MIT，來源語料另有各自授權 | 受控的新型 generator family 測試 | **Verified：可取得；必須鎖定修正版與雜湊** |
| VoiceWukong v3 | 2025 USENIX Security；中英文、商用與開源工具、多種變形 | Zenodo 說明為限制存取，需學術申請，禁止重散布與商用 | 很有價值的外部測試，但不能成為關鍵路徑 | **Verified：新但存取風險高** |
| Deepfake-Eval-2024 | 蒐集 2024 年實際流通內容；56.5 小時音訊、52 語言 | CC BY-SA 4.0、gated；需分享聯絡資訊；條款只允許 evaluation，不可拿來訓練 | 最適合作為完全未調參的真實世界外部測試 | **Verified：優先 holdout，但需接受條款** |
| AUDETER | 2025 preprint；聲稱 4500+ 小時、300 萬片段、11 種近期 TTS 與 10 vocoder | 論文指向 GitHub；本輪尚未完成資料授權與下載結構稽核 | 若授權可行，只採預先定義、generator-stratified 子集 | **Unknown：非常新但過大，不能直接列為核心依賴** |
| RTCFake | 2026 preprint；約 600 小時，針對 real-time communication 並提供 paired offline/online 情境 | 論文提供 HF 位址；本輪尚未確認 license、檔案與下載穩定性 | 僅在通道方向或 stretch experiment 使用 | **Unknown：新鮮，但會把主題推向 channel shift** |

### 6.1 這張表帶來的直接決策

- **Deepfake-Eval-2024 不可用於訓練**；它的 evaluation-only 條款反而很適合把它固定為外部 holdout。
- **VoiceWukong 不可成為論文能否完成的必要條件**，因為需要申請且用途受限。
- **AUDETER 不應整套使用**。4500 小時／300 萬片段會讓資料搬運、特徵儲存與實驗治理成為主工作；需先驗證 license，再用預註冊抽樣。
- **RTCFake 雖然是目前表中最新的資料，但它的新穎性主要是 RTC 場景**。若主題是 unseen generator，就不該因年份新而讓它改寫研究問題。
- **MLAAD 是持續更新的版本化資料集**。使用時必須記錄 v9、下載日期與檔案清單，不能只寫「使用 MLAAD」。

## 7. 第一候選題目的建議資料配置

### 7.1 最小可行配置

1. **歷史訓練錨點**：ASVspoof 2019 LA，或其公開 checkpoint。
2. **現代開發資料**：ASVspoof 5 與 MLAAD v9 二選一；以 generator family 切 train/dev，禁止同模型家族洩漏。
3. **受控外部測試**：DFADD 2025-04 修正版，測 diffusion／flow-matching family。
4. **真實世界 holdout**：Deepfake-Eval-2024 audio，只評估一次，不調參。

這個配置刻意同時保留：

- 文獻可比性；
- 相對現代的開發條件；
- 明確 generator-family shift；
- 真實世界、評估限定的資料。

### 7.2 最新資料的 final freshness holdout

為避免做到一半又不斷追新資料，預先設定一次更新窗口：

- 核心資料與方法凍結後，不再更換 train/dev。
- 在正式最終實驗前約 3 個月，做 **一次且只有一次** 的新資料掃描。
- 候選資料必須在預定截止日前公開，並通過：合法研究用途、可取得、generator 或場景 metadata 足夠、無明顯 train overlap、可在固定資源內完成推論。
- 若 AUDETER 的 license 與結構完成稽核，可抽取一個預先定義的新生成器子集作 final holdout。
- 若只有 RTCFake 通過，則它只能被標成「跨 RTC 場景診斷」，不能拿來替代 unseen-generator 主結論。
- final holdout 只跑一次；結果不理想也不得回頭調方法。

**Inference：** 這比每次看到新資料就重做實驗更能代表真正的時間外泛化，也能避免 moving target。

## 8. 一年可執行方案

### Phase 0：資料與先前研究稽核（第 1 個月）

- 完成 FADEL、selective classification、audio OOD／calibration 的 closest-work matrix。
- 對 ASVspoof 5、MLAAD v9、DFADD、Deepfake-Eval-2024、AUDETER 做 dataset card 稽核。
- 只下載小型 metadata／sample；先確認授權、大小、欄位與 generator split 可行性。

**Gate A：** 若沒有兩個可合法取得、可定義 generator-disjoint 的外部測試來源，停止此題或改成資料稽核型研究。

### Phase 1：最小 pilot（第 2–3 個月）

- 1 個 detector；
- MSP 與 1 個替代分數；
- 1 個開發資料 + 1 個外部資料的 10–20% 預註冊子集；
- 先確認高信心錯誤存在，以及 risk–coverage 分析可穩定重現。

**Gate B：** 若替代分數不優於 MSP，且 threshold transfer 沒有可分析結構，立即降級為負結果或轉向候選二。

### Phase 2：完整核心實驗（第 4–7 個月）

- 擴充至 2 detectors、3 score families、3 seeds；
- 固定 train/dev、完成 controlled external test；
- 做語言、來源、generator family 與音質 confound 診斷；
- 不加入 attacks 或完整 RTC matrix。

### Phase 3：凍結與最終外部測試（第 8–9 個月）

- 凍結方法、閾值與分析程式；
- 進行一次資料更新掃描；
- 執行 Deepfake-Eval-2024 與核准的 final freshness holdout；
- 保存 dataset version、hash、split manifest 與 environment。

### Phase 4：論文與選配實驗（第 10–12 個月）

- 先完成核心論文；
- 僅在主結果完整後，從「單一 RTC 診斷」或「小型有界攻擊」中選一個 stretch experiment；
- 不把 stretch experiment 變成新的主論文。

### 粗略資源估計

**Inference，待 pilot 校正：** 縮小後的核心研究約需 220–350 GPU 小時；主要瓶頸更可能是資料下載、音訊解碼、特徵儲存與 split 治理，而非純訓練。原本 430–520 GPU 小時的第一方向預算可視為上限，不應當作必須用滿的規模。

## 9. Red-team：最可能讓題目失敗的地方

1. **新資料不等於新生成器。** 新發布的 benchmark 可能重用較舊 TTS；必須查 generator version。
2. **資料來源捷徑。** 模型可能辨識錄音品質、語言、平台或 real/fake collection pipeline，而非合成痕跡。
3. **校準洩漏。** 若外部測試資料參與 temperature、threshold 或方法選擇，就不再是有效 holdout。
4. **限制存取資料成為單點失敗。** 需申請的資料只能加分，不能決定論文是否能完成。
5. **超大資料吞噬論文時間。** 全量 AUDETER 類資料會讓工程治理壓過研究問題。
6. **與 FADEL 的 novelty 邊界。** FADEL 已處理 fake-audio OOD uncertainty；目前可辯護的剩餘問題是 per-sample selective risk、threshold transfer 與時間較新的失效邊界，但仍需系統化查證。
7. **結果只顯示 detector 本身太差。** 若 base model 在新資料接近隨機，棄權分析的意義有限；需預先設定最低 base-performance gate。

## 10. 最小驗證合約

### 下一個最小驗證

先做一份 dataset audit matrix，不急著下載全量資料。每列至少填入：

- dataset/version；
- collection/generation/release date；
- generator family/version；
- real/fake construction；
- language/speaker/text；
- channel/manipulation；
- license/terms/access；
- size/storage；
- permissible train/dev/test role；
- overlap risk；
- fixed hash/manifest availability。

### 成功標準

- 至少找到 1 個可作開發、2 個可作完全外部測試的資料來源；
- 至少一個外部來源反映 2024 年後的生成器或實際流通資料；
- split 能在 generator family 層級避免洩漏；
- 估計儲存與推論成本符合單卡、2 TB 儲存與一年時程。

### 停止或轉向條件

- 兩週內無法確認授權／取得方式的資料集，從關鍵路徑移除；
- generator metadata 不足者，不可支撐 unseen-generator 主張；
- 若 closest-work search 顯示已有同樣的 risk–coverage + threshold-transfer protocol，則轉向有界攻擊成本或華語交互失效方向；
- 若 pilot 中所有方法都無法在外部集保持最低可用 coverage，將研究問題改寫成「可信棄權為何失敗」，而不是隱藏負結果。

## 11. 證據地圖與限制

### Verified

- FADEL 已直接研究 fake-audio detection 的 evidential uncertainty 與 OOD 過度自信；因此不能宣稱「首次把不確定性用於語音深偽」。
- Deepfake-Eval-2024 的資料卡明訂只允許 evaluation，不可用於訓練，且需接受 gated access 條款。
- MLAAD 官方頁面標示 v9、1000+ 小時、50+ 語言、175+ TTS 與 CC BY-NC 4.0。
- DFADD 官方 repo 記錄 2025-04 標籤修正與資料更新。
- VoiceWukong 具限制存取條款，因此有排程風險。
- RTCFake 是 2026 preprint，主打約 600 小時的 RTC 場景資料。

### Inference

- 第一方向的最強論文貢獻應是「跨時間／跨生成器的 selective-risk 與 threshold-transfer 失效邊界」，不是再提出一個 detector。
- 最新資料最適合 final holdout，而非全面取代歷史 anchor。
- 對單卡碩論，版本化抽樣與嚴格 holdout 比全量追逐最大資料集更有研究價值。

### Hypothesis

- 校準或 embedding-based uncertainty 能比 MSP 更穩定地跨新生成器排序錯誤。
- 即使偵測 AUROC 尚可，固定的棄權閾值仍可能在新資料上失效。

### Unknown

- AUDETER 的實際資料授權、下載穩定性、完整 metadata 與可抽樣性。
- RTCFake 的 license、檔案結構與是否可穩定直接取得。
- FADEL 以外是否已有 2025–2026 工作完整評估 audio-deepfake 的 risk–coverage 與 threshold transfer。
- 各資料集之間及 SSL 預訓練語料中的說話者／內容重疊程度。

## 12. 目前建議

**Recommendation：** 先以候選一作為工作題目，但只批准 Phase 0 與 Phase 1，不把它視為已選定論文方向。完成 dataset audit、closest-work matrix 與小型 pilot 後，再與候選二、三進行正式決策。

這項建議對資料新鮮度的具體回答是：

> 使用舊資料建立可重現基準，使用較新資料做受控開發，並把截至固定日期能取得的最新合格資料保留為一次性的外部測試。論文的價值不在於「用了最新資料」本身，而在於證明方法面對更新資料時是否仍值得信任。

## 參考資料

- [FADEL: Evidential Learning for Trustworthy Audio Deepfake Detection](https://arxiv.org/abs/2504.15663)
- [ASVspoof 5 官方頁面](https://www.asvspoof.org/)
- [ASVspoof 5 資源與授權（Zenodo）](https://zenodo.org/records/14498691)
- [MLAAD v9 官方資料頁](https://deepfake-demo.aisec.fraunhofer.de/mlaad)
- [DFADD 官方 repository](https://github.com/isjwdu/DFADD)
- [VoiceWukong（USENIX Security 2025）](https://www.usenix.org/conference/usenixsecurity25/presentation/yan-ziwei)
- [VoiceWukong v3 存取條款（Zenodo）](https://zenodo.org/records/14862059)
- [Deepfake-Eval-2024 論文](https://arxiv.org/abs/2503.02857)
- [Deepfake-Eval-2024 官方資料卡](https://huggingface.co/datasets/nuriachandra/Deepfake-Eval-2024)
- [AUDETER](https://arxiv.org/abs/2509.04345)
- [RTCFake](https://arxiv.org/abs/2604.23742)
- [CLAD: Robust Audio Deepfake Detection Against Manipulation Attacks](https://arxiv.org/abs/2404.15854)
- [AudioMarkBench](https://openreview.net/forum?id=t6LQXcFTEn)
- [CallShield](https://arxiv.org/abs/2601.09327)
- [Short Utterance AASIST2](https://arxiv.org/abs/2309.08279)
- [Emotional Conditions in Speech Deepfake Detection](https://arxiv.org/abs/2605.03079)
- [Emotional Speech Dataset（含華語）](https://github.com/HLTSingapore/Emotional-Speech-Data)
