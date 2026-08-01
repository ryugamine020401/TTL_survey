# Round 1 提案：Detection 研究者（Agent A）
日期：2026-07-13

---

## 1. 我看到的問題本質

從 ML detection 的視角，我要先把問題陳述裡的第 4、5 點重新翻譯成技術語言：**這不是「偵測器不夠準」的問題，而是「偵測器學錯了東西」的問題。**

現有的 supervised detector（AASIST、RawNet2、SSL-based 系統）在 ASVspoof 2019 LA 上可以做到 EER 0.06%（survey #1），但 VoiceWukong（#2）實測顯示：同一批模型面對閉源商用生成器時，最佳的 AASIST2 也只有 EER 13.50%，其餘全部 >20%，數個 AUC≈0.5。這個落差的成因，我的判讀是：**supervised detector 學到的是「訓練集中已知生成器的 vocoder fingerprint」，而不是「真實人類語音的本質特徵」**。所以 unseen generator 出現，fingerprint 對不上，模型就退化成猜測。

我認為其他討論者可能忽略的三個面向：

1. **兩個失效軸的「交互作用」是空白的。** Unseen generator（#2）與 unseen channel/codec（#3）各自都有 benchmark，但「閉源生成器的語音再經過未知社群平台轉檔管線」——這才是真實詐騙電話的樣貌——兩軸疊加時偵測器表現如何、劣化是相加還是相乘，目前**沒有任何文獻回答**。#3 的通道模擬 DA 能把 EER 波動壓到 <0.1%，但那是在已知 codec 分布、且生成器 in-domain 的前提下；#2 則證明 multi-domain training 對 unseen generator 甚至有害（AASIST2 退化至 EER 48–50%）。兩個結論看似矛盾，其實是因為兩者處理的 distribution shift 性質不同——這個矛盾本身就是研究缺口。

2. **EER 是一個對社會福祉幾乎無意義的指標。** EER 假設你可以事後挑 threshold，但真實部署時 threshold 要事先定，而且 distribution shift 會讓 calibration 完全失準。一個 EER 13.5% 的模型，如果它在錯的時候**信心滿滿地錯**，對民眾的傷害比一個「會說我不知道」的模型大得多。VoiceWukong 的 user study 顯示人類對高品質 deepfake 的 FAR > 82%——如果偵測器再給出一個錯誤的「真實」判定背書，是雙重傷害。領域內幾乎沒有人在 audio deepfake detection 上認真做 selective prediction / calibration under shift。

3. **「補救策略無效」這個負面結果比想像中嚴重。** VoiceWukong 明確測了 targeted augmentation 與 multi-domain training，結論是幾乎無效甚至有害。這代表「再蒐集更多生成器的資料重訓」這條路的邊際效益正在崩塌——生成器出新的速度永遠比學界蒐資料快。方法論上必須換賽道，而不是在同一條賽道上加碼。

---

## 2. 思辨過程

以下是我的思考獨白，包含被我淘汰或修正的想法。

### 候選 1：新架構 / 新 SSL 特徵組合，直接打 generalization SOTA

最直覺的路：拿 WavLM-Large 或 XLS-R 當 frontend，設計新的 backend（graph attention、Mamba 之類），在 ASVspoof + In-the-Wild 上刷 cross-dataset EER。

**自我質疑：**
- 這是全世界最擁擠的賽道。Survey #1 列出的系統已經把 in-domain 刷到 0.06%，而 out-of-domain 的改善大多是 2–5 個百分點的 incremental 進展，一年內一個碩士生要在這裡做出 novelty，機率很低。
- 更致命的是：VoiceWukong 已經證明這條路線的**方法論假設有問題**——不管架構多好，只要是 supervised binary classification on known generators，就是在學 fingerprint。換 backbone 不改變學習目標，就不會改變失效模式。
- H（指導教授）一定會問「你的 novelty 是什麼」，我答不出比「調參更好」更深的東西。

**判決：淘汰。** 但保留一個教訓：SSL frontend（Wav2Vec2/WavLM/XLS-R）本身是目前唯一被反覆驗證對 generalization 有幫助的元件（#1），任何提案都應該站在它上面，而不是從 raw waveform 重造輪子。

### 候選 2：One-class learning——只學「真實語音」，把所有 fake 當 anomaly

既然 supervised 學的是 fake 的 fingerprint，那就反過來：用 one-class objective（OC-Softmax、one-class contrastive）只對 bona fide speech 建模，任何偏離真實語音 manifold 的都判 fake。理論上對 unseen generator 天然免疫，因為根本不依賴任何 fake 的樣本特性。

**自我質疑：**
- 第一個致命問題：**真實語音自己也會 shift。** 同一句真話，經過 Opus 壓縮 + 20% 丟包（#3 的 C5 條件）之後，在特徵空間裡可能比某些高品質 deepfake 離「乾淨真實語音」更遠。One-class 模型會把「劣化的真話」誤判成假話——FRR 爆炸，民眾的正常通話被標紅，系統信任度歸零（這是 F 會跳出來罵的點）。
- 第二個問題：「真實語音 manifold」的邊界其實由訓練資料的錄音條件定義，不是由「人類發聲機制」定義。這意味著 one-class 只是把 generalization 問題從 fake 端搬到 real 端，沒有消滅它。
- 但是——#3 給了一個關鍵線索：通道模擬 DA 幾乎完全消除通道劣化，證明**通道造成的退化是 distribution shift、不是資訊不可逆摧毀**。那麼如果我把通道模擬 DA **系統性地施加在 bona fide class 上**，就能把「真實語音 manifold」撐大到覆蓋各種通道條件，而 one-class 對 fake 端的免疫性不受影響。這是 #2 和 #3 的結論第一次可以正向組合而非矛盾。

**判決：修正後保留。** 不是「one-class 好棒」，而是「channel-augmented one-class」——用 #3 的手段修補 one-class 的已知弱點，去攻 #2 揭示的 unseen-generator gap。這成為我的正式提案一。

### 候選 3：Continual / few-shot adaptation——新生成器一出現就快速適應

現實中新的商用 TTS 服務上線後，防守方其實買得到樣本（VoiceWukong 就是這樣蒐集 19 個商用工具的）。那麼做一個 continual learning 框架：每次拿到新生成器的 50–100 條樣本，快速 adapt 而不 catastrophic forgetting。

**自我質疑：**
- 假設太強：這要求防守方**知道新生成器存在、且能取得樣本**。對公開商用服務成立，對私有/地下工具不成立——而詐騙集團更可能用後者。這變成只防君子的方案。
- 部署時滯：從新工具上線→被發現→蒐樣本→adapt→推送更新，這個 loop 至少數週，詐騙的黃金期恰好就在這個窗口。
- 學術上 continual learning for ADD 已有人做（EWC、replay-based 都有初步工作），novelty 空間中等。
- 不過它有一個別人沒有的優點：能量化「適應成本」——每個新生成器需要幾條樣本、幾分鐘訓練才能壓回可用 EER。這對 H 關心的「評估方法」是清晰的。

**判決：淘汰為主提案，降級為提案一的附屬實驗。** 在 one-class 框架下測「加入極少量新 fake 樣本做 refinement」的邊際效益，比獨立做 continual learning 更有故事性。

### 候選 4：把 detector 從「判官」改造成「知道自己不知道的證人」——selective prediction

VoiceWukong 的數據裡藏著一個被忽略的寶藏：**人機能力是互補的**。人類對低品質 deepfake 的 FAR 只有 4–19%（優於偵測器），對高品質的 FAR > 82%（遠差於偵測器）。這意味著最優系統不是「機器全自動」，而是「機器處理它有把握的，把沒把握的交給人並誠實說明」。

技術上這叫 selective prediction / abstention：模型輸出三態（real / fake / 我不確定），並且在 distribution shift 下維持 calibration——「我說 90% 是假的時候，真的有 90% 是假」。

**自我質疑：**
- 最大風險：abstention 會不會退化成「遇到難的全部說不知道」？如果 coverage（願意作答的比例）掉到 30%，系統就沒用了。→ 這正是 risk–coverage curve 要量化的東西，本身就是實驗貢獻而非缺陷。
- 第二個風險：uncertainty estimation under distribution shift 本身是 open problem，deep ensemble / MC-dropout / energy-based OOD score 在 audio 上誰有效，未知。→ 但「未知」對碩士論文是好事：一個系統性的實證比較（哪種 uncertainty signal 在 unseen generator 上仍可靠）就是紮實的貢獻，不需要發明新理論。
- 第三個質疑（D 會提的）：攻擊者能不能刻意生成落在「不確定區」的樣本，讓系統永遠 abstain、把負擔全部丟回人類？→ 承認這是可能的，但要注意：對詐騙情境而言，「系統說不確定、請提高警覺」本身就是防護——它打斷了受害者的自動信任。攻擊者把樣本推進不確定區，等於自己放棄了「騙過偵測器取得綠勾勾」的能力。這個論證要在論文裡寫清楚。
- 社會福祉的連結最直接：#8 說分層防禦需要「可信的使用者體驗」，一個 calibrated、會誠實說不知道的偵測器，是分層防禦裡 detection 這層唯一能安全接入人類決策的形態。

**判決：保留為正式提案二。**

### 候選 5：Audio 版的多訊號一致性稽核（把 #7 的 Integrity Clash 搬到聲音）

#7 展示 provenance 與 watermark 可以被去同步，跨層一致性檢查在 image 上做到 100% 分類準確率，且明說「此思路可遷移到 audio」。Audio 領域確實沒人做。

**自我質疑：**
- 這題的核心是協定設計與威脅模型，不是 ML——是 B（密碼學/Provenance 研究者）的主場。我硬做會變成二流的密碼學工作 + 三流的 detection 工作。
- 而且 audio watermark（AudioSeal 之類）經過 codec/重錄的存活率本身是 C 的領域問題，我的 detection 專長在這題裡只佔一角。
- 但我要把一個 detection 視角的觀察留給 B：在多訊號框架裡，passive detector 的輸出必須是**帶不確定性的機率**而不是硬判決，否則跨層一致性檢查會被 detector 的高信心錯誤污染。這恰好和我的提案二接得起來。

**判決：不做為我的提案，轉為給 B 的問題與潛在合作介面。**

---

## 3. 正式提案

### 提案一：Channel-Robust One-Class Learning——以真實語音為錨，聯合攻擊 unseen-generator × unseen-channel 雙重泛化

**核心 idea**
放棄「學習 fake 的 fingerprint」，改為以 one-class objective 對 bona fide speech 建模；並把 #3 驗證有效的通道模擬 DA **只施加於 bona fide class**，把「真實語音 manifold」撐大到覆蓋壓縮/丟包/重錄條件。假說：fake 的判定不再依賴已知生成器特徵 → 對 unseen generator 免疫；real 的 manifold 覆蓋通道變異 → 對 laundering robust。兩個文獻中彼此矛盾的結論（#2：augmentation 對 unseen generator 無效；#3：augmentation 對 channel 幾乎全效）在此框架下得到統一解釋：**augmentation 只該用來擴張你有生成過程控制權的那一類（real），不該用來追逐你永遠追不完的那一類（fake）。**

**為什麼有機會成立（引文獻）**
- #2 證明 supervised + multi-domain training 這條路已死（AASIST2 退化至 EER 48–50%），賽道必須換；one-class 是 survey #1 點名的緩解方向之一，但尚無工作把它與通道 robustness 聯合處理。
- #3 證明通道劣化是 distribution shift 而非資訊摧毀（DA 後 EER 波動 <0.1%），因此「用 DA 撐大 real manifold」有直接證據支持，且 bona fide 的通道模擬不需要任何生成器知識。
- SSL 特徵（WavLM/XLS-R）是 #1 中唯一被反覆驗證有助 generalization 的元件，作為 frozen frontend 可大幅降低訓練成本，碩士生單卡可行。

**技術路線（一年時程）**
1. **月 1–3｜建立交互作用 benchmark（本身就是貢獻）**：取 VoiceWukong 的閉源生成器樣本 × ADD-C 式的 codec/PLR 條件矩陣，量測現有 SOTA（AASIST、RawNet2、WavLM-based）在「unseen generator × unseen channel」疊加下的劣化——填補目前兩軸各自為政的空白。評測協定採 leave-one-generator-out 與 leave-one-codec-out 雙重交叉。
2. **月 4–8｜方法**：frozen WavLM/XLS-R frontend + 輕量 backend，比較 OC-Softmax、one-class contrastive、energy-based 三種 one-class objective；bona fide 施加 6 codec × PLR 通道模擬 DA。
3. **月 9–10｜消融**：DA 施加於 real-only / fake-only / both 的對照（直接檢驗核心假說）；少量新生成器樣本 refinement 的邊際效益（候選 3 的殘留價值）。
4. **月 11–12｜寫作與對外驗證**：在 In-the-Wild 與自錄的社群平台實傳樣本（LINE/Messenger 語音訊息實際走一遍）上做最終測試。

**預期貢獻**
1. 第一個 unseen-generator × unseen-channel 交互作用 benchmark 與劣化定量分析；
2. Channel-augmented one-class 方法及「augmentation 該加在哪一類」的原則性結論；
3. 對真實詐騙通道（社群平台實傳）的可部署性證據。

**風險與退路**：若 one-class 的 FRR 在極端通道下仍不可接受，benchmark 本身（貢獻 1）已足以構成論文骨幹，方法部分降級為「負面結果 + 失效分析」，這在 #2 已有先例（負面結果照樣上 USENIX Security）。

### 提案二：會說「我不知道」的偵測器——Selective Prediction 與 Calibration under Distribution Shift，銜接人機互補

**核心 idea**
把 ADD 從二元判決改造為三態輸出（real / fake / abstain），並要求信心分數在 unseen generator 與 unseen channel 下仍然 calibrated。評估指標從 EER 換成 risk–coverage curve 與 expected calibration error（ECE）under shift。Abstain 的樣本路由給人類，並依 VoiceWukong 的人機互補證據（人類對低品質 deepfake FAR 僅 4–19%，對高品質 FAR >82%）設計路由策略：模型對「它擅長的高品質假音」保持自動判定，對落在分布外的樣本誠實棄權並提示使用者提高警覺。

**為什麼有機會成立（引文獻）**
- #2 的核心數據：SOTA 在閉源生成器上 EER 13.5–50%、數個 AUC≈0.5——在這種現實下，**一個不會棄權的偵測器給出的錯誤「真實」判定，等於替詐騙背書**（人類對高品質 deepfake FAR >82%，機器的錯誤背書會強化而非糾正這個弱點）。
- #2 同時提供了人機互補的實證分布，是設計與評估路由策略的現成依據；MLLM 完全無偵測能力（英文 F1=0）則排除了「交給 LLM 判斷」的捷徑。
- #8 指出分層防禦的優先研究方向包含「可信的使用者體驗」；#1 指出人類辨識準確率僅約 73%——calibrated abstention 是 detection 層安全接入人類決策的必要條件，目前 audio 領域沒有系統性工作（此為根據文獻覆蓋範圍的判斷，屬有依據的猜測，月 1 需做徹底文獻確認）。

**技術路線（一年時程）**
1. **月 1–3**：在固定的 detector backbone（AASIST + WavLM-based 兩套）上，系統性比較 uncertainty signals：softmax confidence、deep ensemble、MC-dropout、energy score、Mahalanobis distance on SSL features。測試床沿用 VoiceWukong（unseen generator 軸）與 ADD-C 條件（channel 軸）。
2. **月 4–6**：量化各 signal 的 calibration 劣化（ECE under shift）與 risk–coverage 特性；找出「在 shift 下最不會騙人的 uncertainty signal」。
3. **月 7–9**：post-hoc calibration（temperature scaling 的 shift-robust 變體）與 abstention threshold 的選擇準則；對抗性分析：攻擊者刻意把樣本推進 abstain 區的成本與後果（回應 D 的預期質疑）。
4. **月 10–12**：小規模 user study（20–30 人）：有/無 calibrated 提示下，人類對 VoiceWukong 樣本的受騙率差異——直接量測「降低民眾受騙機率」這個最終目標。

**預期貢獻**
1. 第一個 ADD 的 uncertainty estimation under distribution shift 系統性實證研究；
2. Risk–coverage 作為 ADD 部署指標的方法論主張（挑戰 EER 霸權）；
3. 基於人機互補實證的路由策略與 user study 證據——這是八個角色裡最直接回答「降低受騙機率」的量化證據。

**風險與退路**：若所有 uncertainty signal 在 shift 下都失準（可能），這個負面結果本身就是重要警訊——「目前沒有任何 ADD 系統的信心分數可以拿給民眾看」，照樣成文。User study 若時程不足可縮減為 pilot。

**兩個提案的關係**：可獨立成篇，也可串接——提案一的 one-class score 天然就是一種 distance-based uncertainty，可直接作為提案二的候選 signal 之一。若最終只能選一個，我押提案一（技術縱深較足）；若討論組更重視「直接降低受騙率」的社會證據鏈，提案二更對題。

---

## 4. 我留給其他討論者的問題

1. **給 D（紅隊）**：針對提案一——如果攻擊者知道防守方用 one-class learning，他可以對 deepfake 做 adversarial perturbation 把它推「進」真實語音 manifold。你評估這種攻擊在**黑箱、且音訊還要過一次未知 codec**（perturbation 可能被壓縮抹掉）的條件下，實際可行性有多高？這決定我提案一的威脅模型該寫多保守。針對提案二——刻意讓系統 abstain 的「棄權洪水攻擊」，你認為對詐騙者有利可圖嗎？還是如我所論證的，abstain 提示本身已構成防護？

2. **給 C（訊號處理）**：#3 證明已知 codec 的劣化可用 DA 消除，但我的提案一需要對**未知**轉檔管線泛化。從訊號處理的角度：主流 codec（AMR/EVS/Opus/AAC/私有管線）對頻譜的破壞方式是否存在共同結構，使得「6 種 codec 的 DA」能 cover 到第 7 種沒見過的？還是各 codec 的 artifact 本質上不同、DA 泛化注定失敗？另外，生成器的 artifact（vocoder 痕跡）與 codec artifact 在時頻域上是否可分離？這決定 laundering 是否「資訊理論上」摧毀了偵測依據。

3. **給 B（密碼學/Provenance）**：#7 的跨層一致性稽核若搬到 audio，passive detector 這一層該以什麼形式接入你的信任模型？我主張 detector 必須輸出 calibrated probability 而非硬判決（否則高信心錯誤會污染整個稽核鏈）——你的協定層能消化機率式證據嗎？以及：C2PA credential 的「缺席」在你的信任模型裡是中性訊號還是可疑訊號？這直接影響 detection 層該對無憑證音訊採取什麼先驗。
