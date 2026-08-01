# 領域史：Audio Deepfake Detection 2010–2026 完整歷史脈絡

日期：2026-07-14
角色：領域史官（智慧 agent），為 v2 討論提供「時間軸基準」——每個階段的歷史事實、當時的痛點、嘗試的解法、殘留的問題，逐一對應具體論文。
定位：本文是 v2 各 agent 提案前的共同參考文件；第一輪 G 史官的 S 系列檢索（`legacy/2026-07-13-deepfake-audio/round1/G-historian.md`）仍然有效，本文吸收並大幅擴充之。

---

## 0. 證據基礎與可信度標記

本文的證據來自本日（2026-07-14）執行的深度研究工作流：5 個檢索角度（挑戰賽主線、架構演進、泛化痛點、主動式防禦、2025–2026 前沿）→ 25 個一手來源（全部為 arXiv/USENIX 原始論文）→ 抽取 120 條 claims → 其中 25 條經三票對抗式查證（24 條通過、1 條被否決）。另整合 `survey/` 資料夾 8 篇 PDF 與第一輪 G 史官的 10 組網路檢索。

每條論述標注證據等級：

| 標記 | 意義 |
|------|------|
| 【甲】 | 本輪三票對抗式查證通過（3-0 或 2-1），引文經逐字核對 |
| 【乙】 | 本輪自一手論文全文抽取（含逐字引文），但未進入查證額度 |
| 【丙】 | 出自 `survey/` 資料夾已收錄的 PDF 全文 |
| 【丁】 | 第一輪 G 史官網路檢索（原文件附 URL），可信度中至高 |
| 【戊】 | 史官背景知識——領域公認事實，但**寫入論文前需自行核對一手文獻** |

⚠️ **本輪被否決的一條 claim（寫論文時不可沿用）**：「ASVspoof 2019 LA 含 19 種攻擊，6 known / 11 unknown」——查證判定此數字拆分錯誤（評測集實為 A07–A19 共 13 種攻擊）。引用 2019 攻擊構成時請直接核對 arXiv:1911.01601 原文。

---

## 1. 一頁時間軸總覽

| 階段 | 年代 | 主導範式 | 定義性事件 | 當代痛點 |
|------|------|----------|------------|----------|
| 前史 | 2010–2014 | 針對已知攻擊的手工對策 | ASV 被證明怕 TTS/VC；SAS 語料庫 | 無共同語料、無共同評測 |
| 制度化 | 2015–2018 | 手工特徵 + GMM/CNN | ASVspoof 2015/2017 | 只防已知攻擊型態 |
| 神經攻擊進場 | 2019–2020 | LFCC-GMM/LCNN 基線 vs 神經 TTS | ASVspoof 2019、t-DCF | 泛化問題首度制度化 |
| 端到端時代 | 2021–2022 | 原始波形深度網路 | RawNet2、AASIST、ASVspoof 2021、In-the-Wild | 通道/壓縮首度入題；in-the-wild 崩跌揭露 |
| SSL 時代 | 2022–2024 | 自監督預訓練前端 | wav2vec 2.0/XLS-R + AASIST、MLAAD、ADD 系列 | in-domain 近乎解決、out-of-domain 依舊 |
| 現實檢驗 | 2024–2026 | 貼近真實條件的大型 benchmark | ASVspoof 5、VoiceWukong、Deepfake-Eval-2024 | 閉源生成器、神經 codec、涵蓋債 |
| 主動訊號（平行軸） | 2023–2026 | 浮水印 + provenance 部署 | AudioSeal、SynthID×ElevenLabs、C2PA、EU AI Act | laundering 全滅、多訊號互相傷害 |

---

## 2. 前史（2010–2014）：問題誕生於 speaker verification

**這個領域不是為了「防詐騙」而生的，是為了保護自動語者驗證（ASV）系統。**這個出身決定了它前十年的問題定義、資料集形態與評測指標，也埋下後來「實驗室成績與真實詐騙場景脫節」的遠因。

發生了什麼【戊——以下皆為領域公認節點，寫入論文前需核對一手文獻】：

- De Leon et al., *Evaluation of Speaker Verification Security and Detection of HMM-Based Synthetic Speech*, IEEE TASLP 20(8), 2012——系統性證明 HMM 合成語音可騙過當時的 ASV，並提出早期偵測對策，是「synthetic speech detection」的奠基作之一。
- Wu et al., *Detecting Converted Speech and Natural Speech for anti-Spoofing Attack in Speaker Recognition*, Interspeech 2012——voice conversion 攻擊面的早期對策。
- Alegre, Amehraye & Evans, BTAS 2013——早期提出 one-class 思路（以真語音為錨）的濫觴之一。
- Wu, Evans, Kinnunen, Yamagishi, Alegre & Li, *Spoofing and countermeasures for speaker verification: A survey*, Speech Communication 66, 2015——為前史收官的權威綜述，明確指出當時最大問題。
- SAS 語料庫（Wu et al., ICASSP 2015）——第一個多攻擊共同語料，直接催生 ASVspoof。

**當時的痛點**：每篇論文各自用私有資料、針對「已知的特定攻擊」設計手工特徵（諧波噪音比、調變特徵、相位特徵等），彼此不可比較；對策學到的是「那一種合成器的 artifact」。**解法**：建共同語料與公開挑戰賽（SAS → ASVspoof）。**殘留**：「對策只認得見過的攻擊」這個根本問題被指出但沒被解決——它將以「generalization to unseen generators」之名貫穿其後十一年。

---

## 3. 制度化（2015–2018）：ASVspoof 誕生與手工特徵時代

發生了什麼：

- **ASVspoof 2015**（Wu, Kinnunen, Evans, Yamagishi et al., Interspeech 2015【戊】）：首屆挑戰賽，聚焦偵測合成與轉換語音（後來稱為 Logical Access, LA）【甲——任務範圍經 3-0 查證，佐證來源 arXiv:2308.14970】。手工特徵 + GMM 就能把 in-domain EER 壓得很低。
- **CQCC**（Todisco, Delgado & Evans, Odyssey 2016 / Computer Speech & Language 2017【戊】）：constant-Q 倒譜係數成為此時代的代表性特徵，與 LFCC 並列。
- **ASVspoof 2017**（Kinnunen et al., Interspeech 2017【戊】）：轉向 replay attack（重播攻擊），LCNN 等輕量 CNN 興起【甲——「2017 僅 replay」經查證佐證】。
- **t-DCF 指標**（Kinnunen et al., Odyssey 2018, arXiv:1804.09618【甲】）：提出 tandem detection cost function，把評測從「偵測器單獨的 EER」轉向「spoofing 與對策對固定 ASV 系統整體可靠性的影響」。

**痛點**：對策跟著挑戰賽的攻擊型態走——2015 防合成、2017 防重播，各自為政。**解法**：把所有攻擊型態放進同一屆挑戰賽（→2019）。**殘留**：評測仍以 ASV 為中心；「乾淨錄音室資料」的傳統在此定型（VCTK、半消音室），十年後被 ASVspoof 5 自己點名檢討【甲】。

---

## 4. 神經攻擊進場（2019–2020）：泛化問題首度制度化

發生了什麼：

- **ASVspoof 2019**（Wang, Yamagishi, Todisco 等, arXiv:1911.01601, Computer Speech & Language 2020）：首屆把三大攻擊型態（語音合成、聲音轉換、重播）納入單一挑戰賽，分 LA（最先進神經 TTS/VC）與 PA（受控模擬重播）兩軌【甲，3-0】。三個此後影響深遠的設計：
  1. **刻意對參賽者隱瞞攻擊細節**——「to reflect as best as possible the practical scenario in which the nature of spoofing attacks is never known in advance」——這是「未見生成器泛化」痛點最早的制度化框架之一【甲，3-0】。
  2. **t-DCF 取代 EER 成為主要指標**【甲，3-0】。
  3. 部分神經 vocoder（WaveNet/WaveRNN 世代）生成的語音**連人類受試者都無法與真語音區分**【乙】——「人耳不可靠」從 2019 年就有一手證據。
- 官方基線定型為 **CQCC-GMM、LFCC-GMM、LFCC-LCNN**（後加 RawNet2），此組合長期作為 ASVspoof 與中文 ADD 系列挑戰賽的基線【甲，3-0；ADD 2022 見 arXiv:2202.08433】。
- 此時代最佳系統在 2019 LA 上把 EER 壓到 0.06%（survey #1【丙】）——**in-domain 問題在帳面上已「解決」**。

**痛點**：帳面完美，但攻擊者不會用你訓練過的生成器。**解法嘗試**：隱瞞攻擊細節、以 unknown attacks 評測。**殘留**：評測內的「unknown」仍與訓練資料同源（同一批錄音、同一種通道）——真正的分布外測試要等 In-the-Wild（2022）才出現。

---

## 5. 端到端時代（2021–2022）：架構革命、通道入題、in-the-wild 崩跌揭露

### 5.1 架構革命

- **RawNet2**（Tak et al., arXiv:2011.01108, ICASSP 2021）：**首次**把端到端原始波形架構帶進 anti-spoofing——「RawNet2 ingests raw audio and has potential to learn cues that are not detectable using more traditional countermeasure solutions」；與基線融合在 2019 LA 全條件達當時已發表第二佳，後成為 ASVspoof 2021 官方基線之一【甲，3-0（合併三條）】。
- **AASIST**（Jung, Heo, Tak, Shim, Chung, Lee, Yu & Evans, arXiv:2110.01200, ICASSP 2022）：異質堆疊圖注意力層在單一端到端系統中聯合建模頻譜與時域 artifacts，目標是取代當時主導的高運算 score-level ensemble；在 2019 LA 上較當時 SOTA 相對改善 20%（pooled min t-DCF 0.0347 vs 0.0443）【甲，3-0】；輕量版 AASIST-L 僅 85K 參數仍勝過所有對手【乙】。AASIST 自此成為此後五年的標準骨幹。

### 5.2 ASVspoof 2021：通道與壓縮首度制度性入題

（Yamagishi et al., arXiv:2109.00537；期刊版 Liu et al., arXiv:2210.02437, IEEE/ACM TASLP 2023）

- **首屆不提供任何 matched training/development 資料**——「reflecting real conditions in which the nature of spoofed and deepfake speech can never be predicated with confidence」，直接針對泛化痛點【甲，3-0】。
- **LA 軌**：評測資料經真實電話系統（VoIP 與 PSTN）傳輸（含一個未傳輸參照條件 LA-C1），訓練資料則是未經傳輸的 2019 資料——明確測試 codec 與通道 nuisance variation 下的 robustness【甲，2-1；異議僅在「所有資料」措辭，已依查證建議加註參照條件】。
- **新增 DF 軌**：脫離 ASV 情境（攻擊者用受害者聲音資料欺騙**人類/媒體**而非語者驗證系統），評測資料經媒體儲存常用的有損 codec 處理——**該系列從 speaker verification anti-spoofing 正式擴張為一般性 audio deepfake detection 的標誌**【甲，3-0】。
- **量化結果暴露缺口**：LA 最佳 min t-DCF 0.2177（EER 1.32%）；PA 最佳 min t-DCF 0.6824（EER 24.25%）；**DF 最佳 EER 僅 15.64%**——且 DF 評測集含 progress 階段未見的攻擊、資料來源與壓縮方法，評測成績顯著劣於 progress 成績，顯示過擬合【甲，3-0】。附帶一個生動的一手軼事：DF 評測第 43 天新攻擊/新 codec/新通道上線時，偵測器 EER 瞬間飆升、甚至高於第 0 天——「unseen conditions cause abrupt in-deployment performance collapse」【乙，轉引自 arXiv:2509.20405】。

### 5.3 In-the-Wild：領域第一次照鏡子

- **Müller et al., *Does Audio Deepfake Detection Generalize?*, Interspeech 2022, arXiv:2203.16263**【乙】：
  - 系統性重新實作並統一評測既有架構，發現光是把 melspec 換成 cqtspec/logspec 前端，平均就改善 37% EER——此前各論文的成績差異有相當部分是特徵選擇而非架構貢獻。
  - 釋出 **In-the-Wild 資料集**：37.9 小時名人/政治人物真實流通錄音（含 17.2 小時 deepfake），來自社群網路與串流平台、含背景噪音。
  - **在 ASVspoof 上訓練的偵測器移到真實世界資料，效能劣化可達 1000%**——「the field may have over-optimized for benchmark datasets rather than achieving genuine generalization」。

**本階段痛點**：三個一起爆發——unseen generator、通道/壓縮、in-the-wild。**解法嘗試**：端到端架構、無 matched data 的挑戰賽設計。**殘留**：架構翻新救了 in-domain，救不了分布外；通道問題被「承認」但只以模擬 codec 的形式入題。

---

## 6. SSL 時代（2022–2024）：預訓練特徵接管前端

發生了什麼：

- **wav2vec 2.0 / XLS-R 前端 + AASIST 後端**（Tak et al., Odyssey 2022【戊，經 survey arXiv:2308.14970 轉述——寫論文請核對一手，arXiv:2202.12233】）：把手工/SincNet 前端換成預訓練 SSL 特徵，同一後端下效能大幅提升——2019 LA 達 EER 0.2–0.3%、**2021 DF 從 15%+ 壓到約 2.85–3.4%**【乙】。SSL + data augmentation 自此成為 unseen-generator 泛化的主流做法（survey #1【丙】）。
- **SSL 層選擇研究**（Kang et al., arXiv:2402.17127, 2024【乙】）：不需要全部 Transformer 層——選取左側子集、微調右側部分層即達 2019 LA SOTA；AASIST 是五個被評測後端中的主要代表，確認其標準地位。
- **中文 ADD 挑戰賽系列**（Yi et al., ADD 2022, arXiv:2202.08433；ADD 2023【乙】）：把任務從二元分類推向更實際的情境——低品質偽音（LF）、部分偽造（PF）、audio fake game（FG），ADD 2023 進一步要求**定位**部分偽造語音中被竄改的區段。
- **MLAAD**（Müller et al., arXiv:2401.09512, IJCNN 2024；持續維護至 v10, 2026-05【乙】）：多語言反欺騙資料集——54 種語言、175 個 TTS 模型、1002.9 小時合成語音，直接回應英語偏誤與生成器多樣性痛點。作為訓練資源，跨資料集表現優於 In-the-Wild/FakeOrReal；但在八個評測集上與 ASVspoof 2019 訓練各勝四個——**互補而非取代**。
- Survey 證據（Yi et al., arXiv:2308.14970【乙】）：跨資料集評測 EER 較 in-domain 增加 **2%–52%**；例如 AASIST 在 2021 DF 訓練後，In-the-Wild 上 EER 由 19.77% 升至 34.81%。該綜述把三大未解問題列為：缺大規模 in-the-wild 資料、對未知攻擊泛化差、缺可解釋性。

**痛點**：SSL 改善了泛化的「幅度」，沒有改變泛化的「結構」——換一批生成器、換一條通道，劣化模式重演。**解法嘗試**：更大的預訓練模型、更多語言/生成器的訓練資料（MLAAD）、任務細化（定位、低品質）。**殘留**：所有這些仍在「學術生成器 + 乾淨或模擬通道」的世界裡自我評測——下一階段的 benchmark 將戳破這件事。

---

## 7. 現實檢驗時代（2024–2026）：閉源生成器、神經 codec、涵蓋債

這是目前所處的階段，特徵是**一波「貼近真實條件」的大型 benchmark 集體揭露：SOTA 偵測器的帳面成績在真實世界不成立**。

### 7.1 挑戰賽主線的自我革新：ASVspoof 5

（挑戰賽論文 Wang, Delgado 等, arXiv:2408.08739, ASVspoof Workshop 2024；資料庫論文 arXiv:2502.08857, Computer Speech & Language 2025, DOI 10.1016/j.csl.2025.101825；總結論文 arXiv:2601.03944, IEEE TASLP，2026-01 提交）

- 資料來源從錄音室品質（VCTK，約 100 名說話者）轉為**群眾外包語音**（MLS English，約 2,000 名說話者，規模 20 倍；另有 3 萬名說話者輔助集）——資料庫論文自承先前版本「品質高於實務預期」【甲，3-0（合併四條）】。小限定：仍為朗讀式有聲書語音，非自發性語音【甲】。
- 攻擊面全面升級：**32 種生成演算法**（legacy + 當代 TTS/VC），攻擊本身亦群眾外包產生，並**不同程度地以 surrogate 偵測模型優化**——攻擊者明確調校 spoofs 以規避偵測器；**7 種對抗性攻擊為系列首度納入**【甲，3-0（合併三條）】。
- 新指標同時支援 spoofing-robust ASV（SASV）與獨立於 ASV 的 standalone 偵測——評測方法論正式承認「deepfake 偵測」是獨立問題【乙】。
- **53 支參賽隊伍的最佳系統，在對抗性攻擊（Malafide/Malacopula 類）與神經編碼/壓縮下仍顯著劣化**——總結論文把 codec/壓縮 robustness 與 adversarial robustness 明確標定為 open problems【甲，3-0】。
- 一份 ASVspoof 5 參賽報告（Ali, Subramani & Malik, arXiv:2410.01108【乙】）具體展示：即使用 laundering attack 做訓練擴增，系統仍在特定未見攻擊（A18/A19/A20/A26/A30）與 codec 條件（C08–C10）上表現最差。

### 7.2 獨立 benchmark 的三面圍攻

- **VoiceWukong**（Yan et al., USENIX Security 2025, arXiv:2409.06348【乙+丙】）：19 個**商用（閉源）**+ 15 個開源生成工具、6 類後處理共 38 個變體、265,200 英文 + 148,200 中文樣本。12 個 SOTA 偵測器：最佳 AASIST2 EER 13.50%，**其餘全部超過 20%**，數個接近隨機。300+ 人 user study 顯示人機能力互補（人類對低品質 deepfake 優於機器、對高品質遠差於機器）；MLLM（Qwen2-Audio）完全不具偵測能力。survey #2【丙】補充：常見補救（targeted augmentation、multi-domain training）幾乎無效，後者甚至讓 AASIST2 退化到 EER 48–50%。
- **Deepfake-Eval-2024**（arXiv:2503.02857【乙】）：2024 年真實流通的多模態 deepfake（56.5 小時音訊、88 個網站、52 種語言）。**開源 SOTA 音訊偵測器 AUC 相較學術 benchmark 掉 48%**；商用偵測器與微調模型較好，但仍不及人類鑑識專家——「academic benchmarks are out of date and not representative of real-world deepfakes」。
- **通訊通道 benchmark ADD-C**（Shi et al., EUSIPCO 2025, arXiv:2504.12423【乙+丙】）：6 種電信 codec × 5 種封包遺失率；三個基線模型 robustness 顯著下降；通道模擬 data augmentation 可幾乎救回——但解法假設已知目標通道分布，對未知 codec 的泛化未驗證（survey #3【丙】）。

### 7.3 三個結構性診斷（2025）

- **神經 codec 是新的頭號殺手**（arXiv:2503.17577【乙】）：10 個偵測模型 × 18 種劣化的系統性評測——模型普遍**耐加性噪音，但怕音訊修改與壓縮，神經 codec 破壞力最強**；speech foundation model 在多數劣化下較傳統模型穩健；模型加大有幫助但報酬遞減。
- **生成端範式已跑贏偵測端**（生態系層級 benchmark，17 個生成器 × 8 個偵測器一對一評測，2025【乙——arXiv 編號待核對，引用前請先確認】）：基於神經 codec 與 flow matching 的新世代生成器**穩定逃過所有頂級偵測器**；「no single detector is universally robust」；並指出既有 benchmark 把多樣生成器混成單一資料集評測，掩蓋了逐生成器的真實弱點。
- **「涵蓋債」（coverage debt）——泛化在結構上不可達成**（Berisha, Kadambi & Lenz, arXiv:2509.20405, 2025【乙】）：真實世界條件組合**乘法**增長、訓練資料收集只能**加法**增長，資料盲區增長永遠快於填補；2022 年後的合成器造成階梯式難度跳升，最新系統「erase the legacy artifacts detectors rely on」；結論直白——**高風險決策不應單獨依賴偵測**，應以分層防禦（capture-time attestation、personhood credentials、challenge-response、多通道佐證）為主、偵測器退居監測/分流角色。
- 針對「訓練資料過舊」的基礎設施回應：**AUDETER**（arXiv:2509.04345, 2025【乙】）——4,500+ 小時、300 萬條、11 個新式 TTS + 10 個 vocoder；發現「多樣來源二元訓練會誘發 negative transfer」並以 curriculum learning 緩解；XLS-R 系偵測器在 AUDETER 訓練後 In-the-Wild EER 達 1.87%——**訓練資料的新鮮度與組織方式本身就是泛化變數**。

**本階段痛點**：閉源商用生成器（拿不到訓練樣本）、神經 codec laundering、對抗性優化攻擊、資料涵蓋債。**解法嘗試**：更真實的 benchmark（本身即貢獻）、新資料基礎設施、curriculum learning、以及——把希望轉向主動式訊號（下一章）。**殘留**：見第 10 節 open problems。

---

## 8. 平行軸線（2023–2026）：主動式訊號——浮水印、provenance、部署與反噬

被動偵測撞牆後，領域的重心明顯轉向「生成端合作」的主動訊號。這條軸線在 2023 年前後從論文走向部署，並在 2025–2026 年暴露出全新的失效模式。

### 8.1 浮水印：從論文到生產線

- 技術譜系（浮水印綜述, arXiv:2504.03765, 2025【乙】）：頻域（DFT/DCT/DWT）、時域（振幅/相位/時序）、深度學習神經嵌入三類；時域方案怕 pitch shift、變速與動態範圍壓縮；深度學習方案較耐對抗修改但嵌入/偵測運算成本高，即時部署受限。
- **AudioSeal**（Roman et al., 2024【乙；ICML 2024，arXiv 編號請核對】）：CNN 在頻譜表徵嵌入不可感知浮水印的代表作；Meta 後續開源 AudioSeal 0.2（localized detection、快兩個數量級）【丁, S2】。
- **產業部署**：Google DeepMind SynthID 浮水印進入 ElevenLabs 生產線【丁, S2】；EU AI Act Article 50 於 **2026-08-02** 生效，強制合成音訊以 machine-readable 方式標記【丁, S8】——「多訊號並存」不再是假設。
- **資料端浮水印新流派——AudioMarkNet**（Zong et al., USENIX Security 2025【乙】）：在使用者**原始語音公開前**嵌入浮水印，若被拿去做 speaker adaptation（微調 TTS 克隆聲音），生成的假語音會**遺傳**浮水印——把 deepfake 偵測轉化為可解釋的浮水印偵測，且對**閉源商用克隆服務有效**（PlayHT 17 秒、Speechify 33 秒即偵測，FPR 均為 0）；16-bit 浮水印嵌在 100–1,000 Hz 頻帶，並評測了含 denoising-autoencoder 洗白在內的 adaptive attacks。這是少數直接回應「閉源生成器」痛點的防禦。

### 8.2 浮水印的極限：laundering 與「捷徑反噬」

- **首個被動 vs 主動統一評測**（Wu, Ge, Wang, Yamagishi, Tsao & Wang, NII/中研院, arXiv:2506.14398, 2025【乙】）——此前兩個社群連共同資料庫與協定都沒有：
  - 無擾動時主動方案完勝：Timbre 與 AudioSeal 在 2019/2021 LA 皆 **0% EER**（被動 SSL-AASIST 0.23%/0.84%）。
  - **神經 codec laundering 災難性擊穿浮水印**：AudioSeal 雖用 EnCodec 做過擴增，換成同類 codec DAC/WavTokenizer 後 EER 飆至 **97.40%/60.95%**——EER 超過 50% 意味著「帶浮水印的假音檔比真音檔更像真的」。
  - 17 種傳輸/操弄條件平均下最穩的是頻域方案 Timbre（8.87%/9.02%），但 pitch shift 下仍崩至 52.62%；結論：「robustness against transmission and manipulation is an unsolved issue」——**對被動與主動方案皆然**。
- **Watermark Shortcut**（Müller & Debus, arXiv:2606.23335, 2026【乙+丁, S3】）：部署浮水印會**毒化**偵測器訓練——若訓練資料呈「fake 有浮水印、real 沒有」，偵測器學到捷徑，產生三重失效：strip-to-evade（去浮水印 → AASIST FNR 37%→80%）、mark-to-frame（給真人語音加浮水印誣陷為假 → FPR 0.3%→58%；已部署商用 API 實測 4%→13%）、out-of-domain 泛化劣化約 9 個百分點（14.3%→23.0%）。緩解：訓練時對兩類都加浮水印；作者結論——**provenance 方案與偵測器必須共同評測，不能各自為政**。
- 浮水印移除攻擊生態已成形【丁, S4】：AudioMarkBench（NeurIPS 2024）定義 removal/forgery 攻擊分類；神經 codec 作為 semantic filter 抹除傳統浮水印（Latent-Mark, arXiv:2603.05310）；diffusion 黑箱移除（arXiv:2605.30614）；self voice conversion 攻擊（arXiv:2601.20432）。

### 8.3 密碼學 provenance：C2PA 及其誠實邊界

- C2PA Content Credentials v2.4（2026）為現行標準【丙, #4/#5】。
- **獨立安全分析證明五項安全目標全數未達成**（UMBC, Golaszewski, Krawetz, Sherman et al.【丙, #6】）：timestamp 可無痕替換、revocation 檢查 optional（同一張圖在兩個 validator 得出矛盾結論）、exclusion range 內資料可竄改、憑證過期使已簽署媒體失去可驗證性、conforming 相機可替 AI 影像簽出「真實拍攝」憑證。核心澄清：**C2PA 證的是 provenance（檔案歷史），不是 authenticity（內容真實性）**；且對不附 credential 的惡意 deepfake 零覆蓋。
- **Integrity Clash**（Nemecek et al., CVPR 2026 Workshop APAI, arXiv:2603.02378【丙, #7】）：C2PA 與 invisible watermark 兩層驗證訊號可被「去同步」而互相矛盾——僅用標準編輯流程即可產生「經認證的假內容」，完全不需破解密碼學；audio 對應的系統性研究仍空白。
- 電信身分層的制度性縫隙【丁, S6】：STIR/SHAKEN 簽章驗的是「號碼」不是「聲音內容」——FCC 對 Lingo Telecom 的裁罰（Biden deepfake robocall 拿到 A 級 attestation）是活教材。
- 相鄰新興子領域：**source tracing**（指認生成器）已有 Interspeech 2025 特別場次、STOPA 資料集、open-set 與 multilingual benchmark【丁, S9】——此方向已非空白，且繼承 detection 的全部弱點。

**本軸線痛點**：主動訊號依賴生成端合作（惡意者不合作）、活不過 laundering、與被動偵測互相傷害。**解法嘗試**：資料端浮水印（AudioMarkNet）、共同評測框架（2506.14398）、跨層一致性稽核（影像已有、audio 空白）。**殘留**：見第 10 節。

---

## 9. 歷史規律：同一個劇本跑了四輪

把六個階段排在一起，可以看到一個已經跑了四輪的循環【史官綜合判斷，各節點皆有上文論文支撐】：

> **新 benchmark 揭露崩跌 → 新方法救回 in-domain → 下一個更貼近現實的 benchmark 再揭露崩跌**

| 輪次 | 「解決」的宣稱 | 被誰打回原形 |
|------|----------------|--------------|
| 1 | 2015：CQCC/LFCC+GMM 壓低 in-domain EER | ASVspoof 2019 的神經 TTS |
| 2 | 2019–2021：RawNet2/AASIST 把 2019 LA 壓到 <1% | ASVspoof 2021 的電話通道與 DF codec（15.64%） |
| 3 | 2022：SSL 前端把 2021 DF 壓到 ~3% | In-the-Wild（劣化至 1000%）、VoiceWukong（13.5–50%） |
| 4 | 2024–2025：SSL ensemble/更大模型/新資料 | Deepfake-Eval-2024（AUC -48%）、神經 codec、對抗優化攻擊、涵蓋債論證 |

三個結構性觀察：

1. **痛點從未被解決，只是被更精確地量測。**「泛化到未見攻擊」從 2015 年的 SAS 語料動機、2019 年的隱瞞攻擊細節、2021 年的無 matched data、到 2025 年的涵蓋債形式化——同一個問題，25 年來換了四種說法。coverage debt 論文（2509.20405）給出的是第一個「為什麼它在結構上不可解」的論證，而非又一次經驗性哀嘆。
2. **每一代的「救星」都成為下一代的「基線」**：GMM → LCNN → RawNet2 → AASIST → SSL+AASIST——AASIST 在 2022 年是 SOTA，2024 年是標準後端，2025 年是被 benchmark 打靶的代表。單點架構貢獻的半衰期約兩年。
3. **典範轉移發生在 2024–2026 交界，但方向不是「更強的偵測器」，而是兩個：**(a) 評測本身成為一等貢獻（VoiceWukong 進 USENIX Security、Deepfake-Eval-2024、ASVspoof 5 的自我革新）；(b) 生態系開始部署主動訊號，而部署立刻製造了新的研究對象（Watermark Shortcut、Integrity Clash、laundering 攻防）——**防禦方的兩條防線第一次被實證互相傷害**。

---

## 10. 2026 年 7 月的 open problems 清單

依「有多少人正在做」由紅海到空白排序：

1. **unseen-generator 泛化**（紅海）：ASVspoof 5 有 53 隊在做；SSL ensemble、MoE、continual learning 全有人做。涵蓋債論證（2509.20405）暗示這條路有結構性上限。
2. **神經 codec / 壓縮 robustness**（升溫中）：ASVspoof 5 總結論文明確標定【甲】；2503.17577 證明是 18 種劣化中最致命的；ADD-C 的 DA 解法只對已知通道有效。
3. **對抗性攻擊 robustness**（升溫中）：ASVspoof 5 首度納入即證明現有系統擋不住【甲】。
4. **浮水印在 laundering 下的存活**（活躍攻防）：DAC/WavTokenizer 97%/61% EER（2506.14398）；移除攻擊武器庫快速累積【丁, S4】。
5. **多訊號互動的失效模式**（新開的縫隙）：Watermark Shortcut 證明浮水印毒化偵測訓練；Integrity Clash 證明 provenance × watermark 可被去同步——**audio 的系統性對應研究仍空白**，且 EU AI Act 2026-08 生效使衝突必然大量發生。
6. **評測方法論**：既有 benchmark 聚合評測掩蓋逐生成器弱點（生態系 benchmark 的批評）；裸 EER 不反映部署風險（第一輪已收斂出「固定低 FPR recall + calibration + risk-coverage」公約）；calibration 首度進入 ASVspoof 5 總結論文的議程【乙】。
7. **真實通道存活性**（經第一輪 G 反覆查證仍無前作的空白）：所有通道 robustness 研究（2021 LA、ADD-C、RADAR）都是模擬或受控傳輸；沒有公開研究把偵測器、浮水印、provenance 一起灌過真實電信/VoIP/平台管線量存活率。
8. **偵測器的「誠實失效」**：涵蓋債論文建議偵測器退居分流角色、高風險決策需分層防禦——但「如何讓偵測器在不可靠時可靠地說不知道」（selective prediction/calibration under shift）在 audio 領域幾乎無人系統性做過——此即 v2 首選方向的立足點。
9. **人機互補的形式化**：VoiceWukong 的 300+ 人數據證明人機在不同品質區間互補，但 deferral policy 如何設計、警告如何下才降低受騙率，仍是文獻空白（v2 限制下只能用已公佈人類數據做模擬）。

未來展望（史官推測，標注為猜測）：(a) 2026-08 EU AI Act 生效後，「標記存在但讀不到/互相矛盾」將成為新常態，多訊號稽核需求會被法規強制催生；(b) 神經 codec 在通訊軟體的普及會同時殺死被動偵測依據與傳統浮水印，把戰場推向 latent-space 浮水印與資料端浮水印；(c) 挑戰賽主線會繼續向「真實條件」逼近，但受限於可控性，真實通道量測的空白預計仍會存在 1–2 年——這是碩論的時間窗。

---

## 11. 對本輪（v2）討論的含義

1. **首選方向（校準棄權）站在歷史的順風處**：它不與循環賽跑（不承諾更低 EER），而是把「循環必然再來」當作公理來設計系統——這正是 2509.20405（涵蓋債 + 偵測器退居分流）與 ASVspoof 5 總結論文（calibration 議程）在 2025–2026 同時指向的方向。v2 硬性限制（不做真人實測）下，VoiceWukong 公佈的人類表現數據是 deferral policy 模擬的現成材料。
2. **次選方向（真實通道 benchmark）的空白經雙輪查證仍成立**：本輪 25 個一手來源中，通道相關研究（2021 LA、ADD-C、2503.17577、2506.14398 的 17 條件）全部是模擬/受控傳輸，無一是真實電信通道實測。
3. **多訊號稽核方向的「兩層恆缺席」判決不因新證據翻案**：本輪新抽取的 AudioMarkNet 與 2506.14398 都印證主動訊號依賴生成端/資料端合作；詐騙場景的訊號缺席問題原樣存在。但 Watermark Shortcut 的「共同評測」呼籲支持把多訊號互動作為**評測軸**（而非主軸）納入任何方向。
4. **寫論文的引用紀律**：本文【甲】級 claims 可直接引用（附原論文）；【乙】級請在引用前開一次原文核對數字；【戊】級與標注「待核」的 arXiv 編號（Tak et al. Odyssey 2022、AudioSeal、AudioMarkBench、生態系 benchmark）必須先驗證。

---

## 附錄：論文清單（依年份；★ = 建議納入 survey/ 資料夾）

**前史與制度化（2010–2018）**【戊，均需核對一手】
- De Leon et al., IEEE TASLP 20(8), 2012 — HMM 合成語音對 ASV 的威脅與偵測
- Wu, Chng & Li, Interspeech 2012 — converted speech 偵測
- Wu, Evans, Kinnunen, Yamagishi, Alegre & Li, Speech Communication 66, 2015 — 前史收官綜述 ★
- Wu et al., ICASSP 2015 — SAS 語料庫
- Wu, Kinnunen, Evans, Yamagishi et al., Interspeech 2015 — ASVspoof 2015
- Todisco, Delgado & Evans, CSL 2017 — CQCC
- Kinnunen et al., Interspeech 2017 — ASVspoof 2017（replay）
- Kinnunen et al., Odyssey 2018, arXiv:1804.09618 — t-DCF【甲】

**神經攻擊與端到端時代（2019–2022）**
- Wang, Yamagishi, Todisco et al., arXiv:1911.01601, CSL 2020 — ASVspoof 2019 資料庫【甲】★
- Tak et al., arXiv:2011.01108, ICASSP 2021 — RawNet2 anti-spoofing【甲】
- Yamagishi et al., arXiv:2109.00537 — ASVspoof 2021【甲】★
- Jung et al., arXiv:2110.01200, ICASSP 2022 — AASIST【甲】
- Müller et al., arXiv:2203.16263, Interspeech 2022 — In-the-Wild【乙】★
- Tak et al., Odyssey 2022（arXiv:2202.12233 待核）— wav2vec 2.0 + AASIST【戊】
- Yi et al., arXiv:2202.08433 — ADD 2022【甲（作為基線佐證）】
- Liu et al., arXiv:2210.02437, IEEE/ACM TASLP 2023 — ASVspoof 2021 期刊版【甲】

**SSL 時代與資料基礎設施（2023–2024）**
- Yi et al., arXiv:2308.14970 — Audio Deepfake Detection survey【甲/乙】★
- Kang et al., arXiv:2402.17127 — SSL 層選擇【乙】
- Müller et al., arXiv:2401.09512, IJCNN 2024（v10 2026-05）— MLAAD【乙】★
- AudioMarkBench, NeurIPS 2024（arXiv:2406.06979 待核）— 浮水印攻擊分類【丁】

**現實檢驗時代（2024–2026）**
- Wang, Delgado et al., arXiv:2408.08739, ASVspoof Workshop 2024 — ASVspoof 5 挑戰賽【甲】★
- ASVspoof 5 資料庫, arXiv:2502.08857, CSL 2025, DOI 10.1016/j.csl.2025.101825【甲】
- ASVspoof 5 總結, arXiv:2601.03944, IEEE TASLP（2026-01 提交）【甲】★
- Yan et al., USENIX Security 2025, arXiv:2409.06348 — VoiceWukong【乙+丙】（已在 survey/）
- Deepfake-Eval-2024, arXiv:2503.02857【乙】★
- Shi et al., EUSIPCO 2025, arXiv:2504.12423 — ADD-C【乙+丙】（已在 survey/）
- Ali, Subramani & Malik, arXiv:2410.01108 — laundering 擴增的極限【乙】
- arXiv:2503.17577 — 10 模型 × 18 劣化 robustness 評測【乙】★
- Berisha, Kadambi & Lenz, arXiv:2509.20405 — coverage debt【乙】★
- AUDETER, arXiv:2509.04345【乙】
- 生態系層級 benchmark（17 生成器 × 8 偵測器，2025，arXiv 編號待核）【乙】

**主動式訊號軸（2023–2026）**
- Roman et al., 2024 — AudioSeal（ICML 2024，編號待核）【乙/丁】
- 浮水印綜述, arXiv:2504.03765, 2025【乙】
- Wu, Ge, Wang, Yamagishi, Tsao & Wang, arXiv:2506.14398 — 首個被動 vs 主動統一評測【乙】★
- Zong et al., USENIX Security 2025 — AudioMarkNet【乙】★
- Müller & Debus, arXiv:2606.23335 — The Watermark Shortcut【乙+丁】★
- Latent-Mark, arXiv:2603.05310；Audio Pirates, arXiv:2605.30614；self-VC removal, arXiv:2601.20432【丁】
- C2PA v2.4 規格與導讀（2026）【丙】（已在 survey/）
- Golaszewski et al.（UMBC）— C2PA falls short【丙】（已在 survey/）
- Nemecek et al., arXiv:2603.02378, CVPR 2026 Workshop — Integrity Clash【丙】（已在 survey/）
- Erokhin & Komendantova, Information 17(4):347, 2026 — 分層防禦 review【丙】（已在 survey/）
