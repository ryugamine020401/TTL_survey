# 五個方向：題目、單獨貢獻、RQ、指標與勝過前作的論證方式

> **[SUPERSEDED 2026-07-23]** 本文件多項主張已被 `research/validations/2026-07-23-five-directions-contributions-rq-metrics-audit.md` 反證或縮限（D5 核心 novelty 遭反證、D3 需大修、D4「單軸前作」為假、D1-B inflation 指標方向錯誤）。請改用 **`2026-07-23-five-directions-contributions-rq-metrics-v2.md`**。本檔僅作歷史紀錄保留。

日期：2026-07-23
性質：`2026-07-23-five-directions-decision.md` 的姊妹篇。決定書回答「選哪個、為什麼」；本文件回答「每個方向如果單獨成為論文，它的題目、貢獻、RQ、指標與比較策略長什麼樣」。五個方向＝目前存活的五個選項（D1 兩形態＋D3＋D4＋D5）；D2 已建議除役，不列。
所有內容整理自既有定稿與查證紀錄，未新增未經查證的主張。

---

## 方向一｜D1-B 來電場景 sequential 版（主線優先形態）

### 1. 論文題目（草案，起草 proposal 時定稿）
- 中：《來電串流下輕量音訊深偽偵測器之凍結序列選擇策略轉移》
- 英：*Source-Frozen Sequential Selective-Policy Transfer of Lightweight Audio Deepfake Detectors for On-Device Call Screening under Unseen Generators*

### 2. 單獨貢獻
1. **框架貢獻（無條件成立）**：第一個把 ADD 的接受／棄權／判定策略放進**串流前綴 sequential 決策**的框架——spoof 為唯一吸收停止態、clean 非吸收監聽至掛斷、棄權綁升級動作，並以 Learn-then-Test 式有限樣本校準給出 policy-level 風險保證（在已記錄搜尋範圍內無 ADD 先作；bounded wording）。
2. **量測貢獻**：三個新的可報告量——τ*(α)（最早有資格承諾的秒數）、optional-stopping inflation（逐前綴名目承諾與 policy 實際洩漏之差）、`Δ_light^seq`（輕量化在 sequential policy 上的額外退化，teacher-relative 隔離）。
3. **部署錨定貢獻**：estimand 錨在經查證的真實部署點（OS 特權 on-device、8kHz post-channel、不留存），法律與平台可行性有 round-1 查證背書。
4. **條件性方法貢獻**：future-aware prefix 蒸餾（full-context teacher → prefix student），僅在 RQ1 揭露失效且便宜修法不足時啟動。
5. **有用負結果**：若 sequential 無附加值（inflation≈0、不支配固定 τ），留下「串流 ADD 評測只需固定截斷」的 bounded 否證。

### 3. 研究問題（RQ）
- **RQ1（承諾轉移）**：source-dev 凍結的 sequential selective policy，在 lineage-disjoint 未見生成器上，其 anytime 風險承諾（整通洩漏 ≤ α）還守不守得住？輕量化造成多少額外退化（`Δ_light^seq`）？
- **RQ2（sequential 附加值）**：相對最佳固定截斷長度 τ，資料相依停止是否 Pareto 支配（同 α 下更早或更高 coverage）？peeking inflation 有多大？τ*(α) 落在第幾秒？
- **RQ3（條件性修復）**：若 RQ1 揭露失效且 rank-changing 便宜修法不足，future-aware prefix 蒸餾能否在同部署預算與 matched 辨識力下把承諾修回？

### 4. 指標與「比別人更好」的論證方式
**主指標**：policy-level anytime leakage `L_CR^seq = P_fake(整通從未觸發「發現合成證據」且未升級)`（generator-family macro）；聯合約束：coverage、E[停止時間]、bona-fide FPR ≤ β。
**次指標**：τ*(α)、peeking inflation、mid-stream 切換後偵測延遲、攻擊強度 vs 棄權率曲線；配平變數：AUROC/EER equivalence tolerance＋部署預算（參數量/RAM/RTF）。

**比較策略——不比 EER，比「前人沒量的維度」＋在共同維度配平**：
1. 對頭號 closest work "Hi!"（ICASSP 2026，0.5–2s 固定長度、無棄權、無風險保證）：在相同資料與 matched 辨識力下，展示固定長度評測**掩蓋**的 policy 失效——它回答「短音訊能不能分」，本論文回答「第幾秒有資格承諾」；預先登記的三測試（結果不可由固定長度裁切重生成、自適應停止 Pareto 支配最佳固定 τ、主 endpoint 是凍結 policy 的外部轉移）保證這不是把音訊切短的數值遊戲。
2. 對 generic selective classification baselines（TMLR 2024 系）：預先登記 rank-changing shortlist，只用 source 調參，在 commit-time 維度對決。
3. 對 proposal-final 形態 A：B 是 A 的嚴格推廣（τ→∞ 退化回 A），繼承其全部 lineage/protocol 嚴謹性。

---

## 方向二｜D1-A 完整語音版（proposal-final，主線退路形態）

### 1. 論文題目
- 中：《未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留》
- 英：*Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators*

### 2. 單獨貢獻
1. **Replication 貢獻**：忠實重現 lightweight／calibration-aware KD baselines（DK-CAST、KD(C) 系）。
2. **評測協定貢獻**：source-frozen、lineage-audited（含 backbone 預訓練語料層）、generator-family macro 的 external selective-policy transfer protocol——現行輕量化研究只報 EER/延遲，全部沒量這一層。
3. **診斷貢獻**：把失效拆解為 discrimination／score ordering／operating-point transfer／calibration 四個來源；含已數值驗證的「TS/Platt 對 rank-based policy 是 no-op」定理級 control。
4. **條件性方法貢獻**：error-aware policy-preserving 蒸餾（H2），僅在 H1a 成立且 H1b 失敗時啟動。
5. **有用負結果**：若 H1a null，留下 edge ADD 評測規格的 bounded audit。

### 3. 研究問題（RQ）
- **RQ1（H1a）**：matched 辨識力與部署預算下，ordinary lightweight student 的未見生成器 family-macro 洩漏，相對 teacher 是否增加超過預定實質差異 ε（`Δ_light > ε`）？
- **RQ2（H1b）**：只用 source 擬合、student 端可廉價推論的 rank-changing selector，能否把外部 policy transfer 修回 tolerance？（TS/Platt 僅作 control。）
- **RQ3（H2，條件性）**：由失效診斷導出的蒸餾機制，能否在同 student、同預算、matched 辨識力下勝過 ordinary KD 與最強合法修法？

### 4. 指標與「比別人更好」的論證方式
**主指標**：`L_CR,g = P(accept ∧ 判真 | fake, family g)` 的 family-macro；主 comparative estimand `Δ_light = G_student − G_teacher`（teacher-relative 雙重差分，隔離 teacher 自身失效）。
**次指標**：coverage（overall/fake/bona-fide）、eAURC/error-AUROC（diagnostic，不作配平）、ECE/Brier（control）；配平：AUROC/EER tolerance＋部署預算。

**比較策略**：
1. 對輕量化前作（DK-CAST/FTDKD/edge 外掛，只報 EER/延遲）：頭號可引用數字是「**ΔEER≈0 但 Δ_light>0**」——同樣的辨識力，凍結策略卻沉默失效；這是他們的評測維度看不見的。
2. 對 threshold-transfer 前作（Zhou & Wang）：他們只稽核分類門檻、未含棄權、未做輕量化——本論文加入 `q` 與 policy 整體、加入 student vs teacher 比較。
3. 對 Cattelan & Silva 的反向證據：以 matched-accuracy 設計正面迎戰——若配平後退化消失，誠實報 null（早停 gate 預先登記）。

---

## 方向三｜D3 攻擊成本上界評估（第一備援）

### 1. 論文題目
- 中：《被動語音深偽偵測之適應性洗刷（adaptive laundering）攻擊成本上界評估》
- 英：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

### 2. 單獨貢獻
1. **評估軸貢獻**：把 laundering 從「防禦者視角的隨機後處理」形式化為「攻擊者視角的 recipe-level greedy 搜尋」，輸出攻擊成本**上界**——「攻擊成本」這個軸在 audio ADD 文獻此前不存在。
2. **物理錨貢獻**：以可控植入實驗給每個 laundering 動作標**物理可逆性下界**，認證 neural codec transcode 為「零金錢、一行指令、不可逆」的必殺動作——資訊理論事實，不隨生成器世代過期（全五方向 novelty 最耐久的錨）。
3. **幾何地圖貢獻**：攻擊成本–recall 曲線的懸崖／緩坡地圖，作為部署方照妖鏡與後續防禦研究的標準壓力測試。

### 3. 研究問題（RQ）
- **RQ1（成本上界）**：讓固定 FPR≤1% 的 recall 跌破可用門檻，最便宜的 laundering 配方是什麼？（greedy 搜尋終點）
- **RQ2（可逆性下界）**：配方中哪些動作是 channel-aware DA 追得回的可逆偏移、哪些踩到不可逆資訊摧毀？（逐步可控植入標註）
- **RQ3（曲線幾何）**：成本–recall 曲線是懸崖還是緩坡？哪些偵測器設計讓曲線變陡？（同一次搜尋的軌跡形狀）

### 4. 指標與「比別人更好」的論證方式
**主指標**：fixed-FPR≤1% selective recall；攻擊成本代理（金錢／計算／指令步數，預先定義並敏感度分析）；可逆性標註（DA 恢復率、可控植入 artifact 存活）。
**次指標**：曲線斜率／拐點位置；跨偵測器（4 個，SSL vs 手工特徵）一致性。

**比較策略**：
1. 對 robustness 前作（隨機後處理、平均劣化）：證明「**最壞情況嚴格重於平均**」——同一組動作空間下，greedy 找到的最便宜配方造成的 recall 崩落顯著深於隨機平均，前作的評測系統性低估攻擊者。
2. 上界主張的自我保護：任何更強的攻擊者只會更便宜（真實成本 ≤ 本文上界），結論方向不會被未來攻擊推翻。
3. 對 adversarial-audio 前作（per-sample 白盒擾動）：本文的 recipe-level 動作（ffmpeg 一行指令）才符合詐騙者的實際能力模型——威脅模型的生態效度是比較的主戰場。

---

## 方向四｜D4 詐騙情境評估效度審計（第二備援）

### 1. 論文題目
- 中：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》
- 英：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*

### 2. 單獨貢獻
1. **資源貢獻**：第一份詐騙情境條件的**繁體中文（zh-TW）** ADD 測試語料（可重現配方＋checksum 發布，不散布合成詐騙語音本體）——話術語意、句長、情緒韻律、通道四軸受控分層。
2. **量化貢獻**：「素材真實性樂觀偏差」的總量與**多因子交互**分解——現有前作全部單軸（短句、情緒、通道各自為政），交互效應無人量；「話術語意是否讓 TTS 露餡」是零前作的自變數。
3. **效度協定貢獻**：UTMOS＋speaker-similarity 品質配對協定，把「偵測器對現場失效」與「情緒/短句 TTS 品質本來就差」解耦——這是所有單軸前作共同的效度漏洞。

### 3. 研究問題（RQ）
- **RQ1（總量）**：標準朗讀素材 → 詐騙現場素材，fixed-FPR≤1% recall 落差多大？
- **RQ2（分解）**：話術語意／句長／情緒／通道的主效應與交互效應各占多少？
- **RQ3（效度）**：品質協變量配對後，淨落差還剩多少？

### 4. 指標與「比別人更好」的論證方式
**主指標**：fixed-FPR≤1% recall 落差矩陣；析因效應量（主效應＋交互項）；品質配對後淨落差。
**協變量**：UTMOS（自然度）、ECAPA speaker similarity——全機器計算，零人工聽測。

**比較策略**：
1. 對單軸前作（AASIST2 短句、情緒 TTS 偵測、通道劣化各一票）：本文不是加一軸，而是**量他們互相掩蓋的交互項**——若交互顯著，單軸結論全部要重新解讀；若不顯著，也是對「單軸評測已足夠」的可發表驗證。
2. 對 benchmark 生態：立一個可審計的門檻——「以後宣稱能防詐的偵測器，得先過詐騙現場條件這關」；zh-TW 語料填補的是語言×場景雙重空白，不與英語 benchmark 正面競數字。
3. 效度武器：品質配對是本文獨有的裁判機制——前作的落差可能只是「現場 TTS 品質差被抓到」，本文能區分，前作不能。

---

## 方向五｜D5 浮水印可靠位元容量審計（第三備援）

### 1. 論文題目
- 中：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》
- 英：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*

### 2. 單獨貢獻
1. **量測貢獻**：第一張跨傳統與 neural codec 通道的 watermark provenance **可靠 bit 容量地圖**，以可控植入取 ground truth（避開高維互資訊估計的不可靠），指認可逆／不可逆容量塌陷點。
2. **構造貢獻**：「索引不 payload」soft-binding 構造（碼率 ≤ 實測容量的 ECC 索引＋本地簽章承諾表）的單機生死判定——正面工程貢獻，不是純批評。
3. **政策貢獻**：第一份 EU AI Act Article 50 音訊機器可讀性審計（2026-08-02 生效，零前作）——把 bit 數字對照兩階操作型門檻逐通道宣判。

### 3. 研究問題（RQ）
- **RQ1（容量地圖）**：各 watermark 家族（AudioSeal/WavMark/SilentCipher）在 codec×PLR 與 neural-codec×bitrate 矩陣上各剩幾個可靠 bit？塌陷點在哪？
- **RQ2（構造生死）**：在實測容量內，soft-binding 索引構造能否端到端存活？k 在哪個通道歸零？
- **RQ3（Article 50 判定）**：這些 bit 數夠不夠「machine-readable」？逐通道判可讀／不可讀。

### 4. 指標與「比別人更好」的論證方式
**主指標**：可靠 bit 數（可控植入校準後的 bit 存活率）；容量塌陷點位置（哪個 codec/bitrate 歸零）；ECC 修正後可承載索引位元 k；兩階操作型門檻（detection-readable / provenance-readable）。

**比較策略**：
1. 對 AudioMarkBench（2024，只做模擬擾動）與《Will They Survive Neural Codecs?》（Interspeech 2025，最近直接前作）：前作報「存活率百分比」，本文報「**剩幾個可靠 bit、還能承載什麼**」——從 robustness 敘事升級為容量／構造／法律三層可消費結論，且可控植入 ground-truth 錨是方法學差異。
2. **反脆弱比較位**：若 bit 在最溫和通道就歸零，結論不是實驗失敗，而是對 Article 50 的政策級否證——假設越崩、發現越硬，前作沒有這個承載結構。
3. 誠實邊界即護城河：明文界定「非即時語音訊息／媒體檔案」定義域，不與偵測類論文比 EER。

---

## 附：一頁對照表

| | D1-B 來電 sequential | D1-A 完整語音 | D3 攻擊成本 | D4 現場考卷 | D5 provenance bit |
|---|---|---|---|---|---|
| 一句話貢獻 | 第一個 ADD 串流前綴 sequential selective policy 框架＋τ*(α) | 第一個 source-frozen 輕量化 policy-transfer 協定 | 攻擊成本軸＋物理不可逆下界 | zh-TW 詐騙語料＋交互分解＋品質配對 | 可靠 bit 容量地圖＋Article 50 判定 |
| 主指標 | `L_CR^seq`、τ*(α)、`Δ_light^seq` | `Δ_light`、family-macro `L_CR` | 攻擊成本上界、fixed-FPR recall | recall 落差、交互效應量、配對淨落差 | 可靠 bit 數、塌陷點、k |
| 打贏誰 | "Hi!" ICASSP 2026（固定長度無棄權） | DK-CAST/FTDKD（只報 EER）、Zhou & Wang（無棄權無壓縮） | 隨機後處理 robustness 前作（平均 vs 最壞） | 單軸前作（短句/情緒/通道各自為政） | AudioMarkBench、Interspeech 2025（存活率 vs 容量） |
| 勝負維度 | 何時有資格承諾（前人沒量） | 凍結策略沉默失效（前人沒量） | 最壞情況嚴格重於平均 | 交互項＋品質解耦（前人做不到） | bit 容量＋法律門檻（前人沒接） |
| 負結果價值 | 「固定截斷已足夠」否證 | edge 評測規格 audit | 「全是緩坡＝裸奔」警告 | 「單軸已足夠」驗證 | Article 50 政策否證 |
| novelty 耐久度 | 中高（gap 一年內恐關閉） | 中（窄交集） | **最高（物理事實不過期）** | 中低（護城河收縮中） | 中（政策時效紅利） |
