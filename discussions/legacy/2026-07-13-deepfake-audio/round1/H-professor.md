# Round 1 提案：指導教授（Agent H）
日期：2026-07-13

---

## 1. 我看到的問題本質

我先把話說重一點：這個題目最大的風險不是「做不出東西」，而是「做出一個看起來能動、實際上無法通過審查的東西」。我審碩論和審稿二十年，deepfake detection 這個領域的投稿有一個共同病灶——**在自己選的測試集上贏，在別人選的測試集上死**。VoiceWukong（文獻 #2）已經用數據把這件事釘死了：AASIST2 原論文報告 EER 0.82%，面對閉源商用生成器實測 13.5%；其餘 SOTA 全部超過 20%，有幾個接近丟銅板。這不是某個模型不夠好，這是**整個領域的評估文化出了問題**。

所以我認為別的討論者可能忽略、但我一定會盯著的面向有四個：

### 1.1 EER 是一個會騙人的指標

EER 假設 false alarm 與 miss 等價、且隱含 50/50 的 prior。真實的詐騙電話情境完全不是這樣：base rate 未知且極度不平衡，而且兩種錯誤的代價天差地遠——「把詐騙判成真」讓阿嬤被騙走退休金，「把真的判成假」讓兒子打電話回家被 App 擋掉。一個 EER 13.5% 的偵測器裝在民眾手機上，依 base rate 不同，可能製造出「絕大多數警報都是誤報」（民眾學會忽略它）或更糟的「絕大多數詐騙都拿到綠勾勾」（**錯誤的安全保證比沒有保證更危險**）。任何提案如果只打算報 EER，我在 proposal defense 就會擋下來。必須報 fixed-operating-point 指標（如 FPR @ FNR=1%）、calibration（ECE）、以及在多個 base rate 假設下的 expected cost。

### 1.2 不要跟生成器軍備競賽——碩士生打不贏 ElevenLabs

閉源生成器每季更新，任何「訓練一個更會泛化的偵測器」的主張，在論文送審到刊出的八個月之間就會過期。VoiceWukong 更狠的一刀是：常見補救（targeted augmentation、multi-domain training）不但沒用，multi-domain training 還把 AASIST2 打到 EER 48–50%（接近隨機）。這告訴我們現有的「加資料」直覺在這個 shift 結構下會失效。碩士論文要選的是**不隨生成器版本失效的貢獻**：評估方法、協定、訊號間的結構性關係、不確定性的量化——這些東西五年後還會被引用。

### 1.3 「小而深、可驗證」的邊界在哪

一年扣掉修課，實際研究時間約 9–10 個月。可行性的紅線：
- **不能依賴自己從頭訓練大模型**——用現成 SSL backbone（Wav2Vec2/WavLM）與現成偵測器（AASIST 系列）當元件。
- **不能依賴外部機構配合**——任何「說服電信商/平台部署」的方案直接出局。
- **資料集必須今天就能下載或一個月內能自建**——ASVspoof 2019/2021、In-the-Wild、MLAAD 可得；VoiceWukong 部分可得；閉源生成樣本可用商用 API（ElevenLabs 等）小規模自建，但要先確認 ToS 與 IRB。
- **baseline 必須存在且可復現**——沒有 baseline 的題目無法寫 experiments 章節。

### 1.4 文獻地圖指出的真空地帶

Survey 的 gap 地圖第 3 點寫得很清楚：provenance、watermark、passive detection 三者各自的極限都被研究透了（#2、#3 打 passive detection；#6、#7 打 provenance），但**三者之間的一致性關係在 audio 領域是系統性的空白**。#7（Authenticated Contradictions）在影像上示範了這條路：不需破解密碼學，只靠 metadata washing 就能製造「經認證的假內容」，而他們提出的跨層稽核在 3,500 張影像上達 100% 分類準確率——這篇進了 CVPR 2026 Workshop。audio 版本沒人做。這種「把已驗證的框架遷移到有實質新困難的模態」正是碩士論文的甜蜜點：novelty 有明確的錨、可行性有前人的路線圖、而 audio 的通道特性（re-recording、電話 codec）帶來影像沒有的真問題。

---

## 2. 思辨過程

以下是我淘汰與修正候選想法的過程，照實記錄。

### 候選 1：訓練一個對 unseen generator 更會泛化的偵測器（新 SSL 特徵組合 / domain generalization loss）

這是最直覺的方向，也是 90% 的學生第一個提的。

**自我質疑：**
- Novelty 極低。文獻 #1 已列出 SSL 特徵 + augmentation 是現行最佳解，這條路上的 incremental work 在 INTERSPEECH 都嫌擁擠。
- VoiceWukong 的實證直接打臉：augmentation 與 multi-domain training「幾乎無效甚至有害」。學生如果宣稱他的 DG loss 能解決這件事，我要問：你的 held-out 閉源生成器測試集哪裡來？如果用 VoiceWukong 測，你其實在對這個 benchmark 過擬合；如果自建，樣本量與多樣性撐不起結論。
- 就算做出 EER 從 13.5% 降到 10%，so what？對「降低民眾受騙機率」這個最終目標，10% EER 的偵測器仍然不可部署（見 1.1 的 base rate 論證）。
- 這是軍備競賽的攻方地形，碩士生沒有勝算。

**裁決：淘汰**（作為論文主軸）。但保留其工程技能：兩個正式提案都需要學生會跑 AASIST/SSL-based detector 當元件。

### 候選 2：為語音通話設計 audio provenance——「電話版 C2PA」

問題陳述第 3 點指出 C2PA 只保證「未被竄改」不保證「非 AI 生成」，那能不能設計一個在通話端點簽署、綁定說話人裝置的 provenance 協定？

**自我質疑：**
- 文獻 #6 是致命的：C2PA 一個資源雄厚的產業聯盟，連自己宣稱的兩項安全目標（claim integrity、weak file integrity）加上作者補充的三項，**五項全部未達成**——timestamp 可無痕替換、revocation 檢查 optional 導致 validator 互相矛盾、憑證過期讓已簽媒體失去可驗證性。一個碩士生要在一年內設計出更完整的信任模型？我不信。
- 更根本的：provenance 是生態系問題不是演算法問題。沒有電信商、手機廠、憑證機構配合，論文只能停在「協定設計 + 模擬」，評估章節會非常空虛。審稿人會問 adoption path，而學生答不出來。
- #6 還示範了用 conforming 裝置替 AI 內容簽出「真實」憑證——就算協定完美，端點被攻破就全毀。這是系統安全問題，超出論文範圍。
- 通話是即時串流不是檔案，C2PA 的 manifest 模型根本沒有對應的簽署點。這其實是個好研究問題，但它是博士等級的。

**裁決：淘汰。** 但它留下一個重要的設計原則：**任何單一訊號都不可獨立信任**（#6、#8 的共同結論），這直接餵養候選 4。

### 候選 3：未知 codec / laundering 管線下的 robustness——盲通道估計 + test-time adaptation

文獻 #3 證明：已知通道下，通道模擬 DA 能把劣化壓到 EER 波動 <0.1%，代表退化主因是 distribution shift 而非資訊被摧毀——這是個樂觀訊號。殘留 gap 是「未知 codec、社群平台私有轉檔管線」。那就做：測試時先盲估通道特性，再做 test-time adaptation 或選擇對應的 expert model。

**自我質疑：**
- 「資訊還在、只是分佈移了」這個結論是在 #3 的六種標準 codec 上得出的，猜測（標明：這是猜測）社群平台的多重轉檔 + 音量正規化 + 降噪管線可能真的不可逆地摧毀高頻 artifacts，屆時 TTA 無藥可救。這個風險在動手前無法排除。
- 真實平台管線資料的取得有 ToS 問題：大量自動上傳/下載 WhatsApp、LINE 語音訊息來建資料集，法務上未必過得了關。
- 變數空間爆炸：unseen codec × unseen generator 的交互作用（#3 自己承認未驗證）意味著完整的 factorial 實驗超出一年時程。
- 這個題目單獨成立時，貢獻的形狀是「又一個 robustness 方法」，novelty 中等。

**裁決：降級併入。** 不作為獨立論文，但它的核心資產——「laundering 管線作為評估軸」——併入提案一的實驗設計：量測各驗證訊號（watermark、manifest、passive score）在 laundering 下的**存活性曲線**，這反而讓提案一有了 audio 特有、影像版 #7 沒有的貢獻。

### 候選 4：Audio 版跨訊號一致性稽核（把 #7 的 Integrity Clash 遷移到 audio）

#7 證明了 C2PA manifest 與 invisible watermark 可被去同步、產生密碼學上皆有效卻互相矛盾的「Authenticated Contradiction」，且跨層稽核可以 100% 分類衝突狀態。audio 領域沒有對應研究（gap 地圖第 3 點明言）。

**自我質疑：**
- **覆蓋率問題**：詐騙集團的 deepfake 根本不會帶 watermark 也不會帶 manifest，稽核什麼？——這是最強的反對，我認真想了很久。回應：稽核層的輸出不是「真/假」二元判定，而是**可信度分級**：「訊號齊全且一致」「訊號缺席」「訊號矛盾」是三種不同的風險等級，而「缺席」本身就是可操作的資訊（如同瀏覽器對無 HTTPS 網站的降級提示）。隨著 EU AI Act 等法規要求生成內容標示、Meta/Google 部署 AudioSeal/SynthID 類浮水印，「本該有訊號卻沒有」的鑑別力會逐年上升。論文的主張要誠實地限定在這個威脅模型內。
- **會不會只是 #7 的複製貼上？** 如果只是把同一套協定換個模態跑一遍，novelty 不夠。回應：audio 有三個影像沒有的實質新困難——(a) re-recording（空氣通道）與電話 codec 是 audio 的常態攻擊面，watermark 存活性完全是另一個問題；(b) audio 的 C2PA 嵌入與 soft binding 成熟度遠低於影像，衝突狀態空間需要重新形式化；(c) 串流/片段擷取（詐騙者只轉發 10 秒片段）破壞 manifest 綁定的方式與影像裁切不同。這三點足以撐起獨立貢獻。
- **元件風險**：audio watermark（AudioSeal、WavMark）與 c2patool 對 audio 格式的支援如果太殘破，工程時間會爆炸。需要第一個月做 feasibility spike，這是可管理的風險。

**裁決：存活，成為正式提案一。**

### 候選 5：知道自己不知道——ADD 的 selective prediction（校準棄權）與人機分工

換個角度接受現實：偵測器在 unseen generator 上就是會爛（#2），那麼與其追求更低的 EER，不如讓偵測器**在它不可靠的輸入上可靠地說「我不知道」**。VoiceWukong 的人機互補數據給了第二層支撐：人類對低品質 deepfake 的 FAR 只有 4–19%（優於偵測器），對高品質 FAR >82%（遠差於偵測器）——這是設計 deferral policy 的實證基礎。

**自我質疑：**
- **Selective prediction / OOD detection 在 CV、NLP 都是老題目，novelty 在哪？** 回應：老方法 × 新領域本身不夠，但這裡有實質的未知：(a) ADD 的 shift 結構很特殊——unseen generator 產生的樣本對模型來說可能落在「自信但錯」的區域（#2 顯示數個偵測器 AUC≈0.5，代表分數完全失去鑑別力而非單純 shift），現成 OOD score 在這種 failure mode 下是否有效，是一個真正 open 的實證問題；(b) 沒有任何 ADD benchmark 報告 risk-coverage 曲線或 shift 下的 calibration——這個評估框架本身就是貢獻。
- **會不會做出來發現「棄權率 80% 才能達到可用的 selective risk」，等於宣告失敗？** 這確實可能。但注意：這個「負面結果」搭配嚴謹的評估框架，本身就是一篇有價值的論文（如同 VoiceWukong 的價值在於量化失效）。而且 deferral 給人類不是死路——VoiceWukong 數據顯示機器最不確定的區域（低品質、經 manipulation）恰好是人類表現較好的區域（此互補性是否在「機器棄權的子集」上成立，正是要驗證的科學問題）。有下檔保護的題目才是好碩論。
- **人機實驗要 user study，IRB 與時程？** 備案：先用 VoiceWukong 已公佈的人類表現數據做 policy 模擬（不需 IRB），行有餘力再做小規模（30–50 人）listening study。

**裁決：存活，成為正式提案二。**

### 淘汰總表

| 候選 | 裁決 | 關鍵理由 |
|------|------|----------|
| 1. 更會泛化的偵測器 | 淘汰 | 軍備競賽攻方地形；#2 證明現行補救無效；novelty 低 |
| 2. 電話版 C2PA | 淘汰 | #6 證明產業聯盟都做不好；生態系問題非演算法問題；不可評估 |
| 3. 未知通道 robustness | 併入提案一 | 單獨成立風險高；「laundering 存活性」作為提案一的評估軸 |
| 4. Audio 跨訊號一致性稽核 | **提案一** | gap 明確（#7 + gap 地圖第 3 點）；audio 特有困難撐起 novelty |
| 5. Selective prediction + 人機分工 | **提案二** | 不隨生成器版本失效；#2 的失效數據與人機互補數據雙重支撐 |

---

## 3. 正式提案

### 提案一：AudioClash——Audio 深偽防禦的跨訊號一致性稽核：衝突狀態形式化、去同步攻擊與 laundering 存活性分析

**核心 idea**：將 #7 在影像上驗證的「Integrity Clash」框架系統性地遷移並擴充到 audio：形式化 C2PA manifest、invisible audio watermark（AudioSeal / WavMark）、passive detector score 三種驗證訊號的一致/衝突狀態空間；實作 audio 版去同步攻擊（metadata washing、re-encode、片段擷取、re-record）證明「經認證的假語音」可行；提出跨層稽核協定輸出可信度分級；並以 laundering 管線（#3 的 codec×PLR 條件 + #2 的 manipulation 變體）量測每種訊號的**存活性曲線**與稽核協定的分級準確率。

**為什麼有機會成立**：
- Gap 有直接文獻錨定：#7 證明影像版可行且可發表（CVPR 2026 Workshop），gap 地圖明言「audio 領域尚缺乏對應的系統性研究」；#8 的結論「沒有任何單一手段充分、分層防禦是唯一實際做法」提供動機，但分層防禦的「層間如何互檢」正是無人做的部分。
- 不與生成器軍備競賽：貢獻是訊號間的**結構性關係**與稽核**協定**，不隨 TTS 模型更新而失效。
- 元件全部現成：AudioSeal/WavMark 開源、c2patool 開源、AASIST/SSL-based detector 開源、laundering 條件可用 ffmpeg 重現 #3 的管線。學生不需訓練任何大模型。
- Audio 特有貢獻（超越 #7 的部分）：re-recording 與電話 codec 下的 watermark 存活性、串流片段的 manifest 綁定失效模式，這些是影像版沒有的真問題。

**技術路線（10 個月）**：
1. 月 1：feasibility spike——AudioSeal/WavMark 嵌入與偵測、c2patool 對 WAV/MP3 的 manifest 操作、AASIST 推論管線全部打通；任一元件不可用即啟動備案（換 watermark 方案或縮減訊號組為兩訊號）。
2. 月 2–3：形式化衝突狀態空間（參考 #7 的四種衝突狀態，擴充 audio 特有狀態如「watermark 部分存活」）；實作去同步攻擊集。
3. 月 4–6：建構評估資料集——real（ASVspoof bonafide、In-the-Wild real）× fake（開源 TTS + 小規模商用 API 樣本）× 訊號配置 × laundering 條件（6 codec × PLR，加 re-record 子集）；跑存活性量測。
4. 月 7–8：設計並評估稽核協定（規則式 baseline → 學習式分級器），指標：分級準確率、各 laundering 深度下的退化曲線、對「訊號缺席」情境的風險分級行為。
5. 月 9–10：對抗性分析（自己當紅隊：知道協定的攻擊者的最便宜繞過）、寫作。

**預期貢獻**：(1) audio 領域第一個跨訊號衝突狀態的形式化與實證（對應 #7 在影像的地位）；(2) 第一份 watermark/manifest/passive score 在 laundering 下的存活性對照表——這對後續所有分層防禦研究都是基礎設施；(3) 一個可信度分級稽核協定與公開資料集。目標 venue：USENIX Security / ICASSP / INTERSPEECH。

**風險與備案**：最大風險是 audio 的 C2PA 工具鏈太不成熟。備案：把 manifest 層降級為「規格層模擬」（依 v2.4 spec 自行實作最小 manifest 驗證），論文重心移向 watermark × passive detection 的雙訊號一致性 + 存活性分析——仍是完整可發表的貢獻。

### 提案二：知道自己不知道——Distribution shift 下 deepfake 語音偵測的 selective prediction 框架與人機協作 triage

**核心 idea**：接受「偵測器在 unseen generator/channel 上必然劣化」的現實（#2、#3），把問題從「更準」重構為「在不可靠時可靠地棄權」：系統性量測現有 SOTA 偵測器在 shift 下的 confidence calibration 與 risk-coverage 行為（目前文獻完全缺席的評估維度）；比較並改良棄權機制（MSP、energy score、SSL 特徵空間 OOD 距離、ensemble disagreement、test-time augmentation 一致性）；最後基於 VoiceWukong 的人機互補實證設計 deferral policy——機器棄權的樣本轉交人類，並以模擬 + 小規模 listening study 驗證整體 triage 系統的 expected cost 是否低於純機器或純人類。

**為什麼有機會成立**：
- 動機有硬數據：#2 顯示 SOTA 在閉源生成器上 EER 13.5–50%、數個 AUC≈0.5，而這些系統仍會輸出高信心分數——「自信地錯」正是造成「錯誤安全保證」的機制，直接對應問題陳述的「降低民眾受騙機率」：對民眾而言，「本 App 無法判定，請掛斷後用已知號碼回撥」遠比一個錯的綠勾勾有價值。
- 人機分工有實證基礎：#2 的 user study 顯示人類與機器的強弱區域互補（人類對低品質 FAR 4–19%、機器對高品質佔優），且 #1 指出人類整體準確率僅約 73%——單靠任何一方都不夠，這正是 triage 的立論。
- 可行性高：全部使用現成偵測器與公開資料集（ASVspoof 2019/2021、In-the-Wild、MLAAD；VoiceWukong 可得部分；自建小規模商用 API 測試集），方法元件（OOD scores、conformal prediction）皆有成熟實作。評估協定「train on A, calibrate on A', abstain-test on B」清晰可復現。
- 貢獻不隨生成器過期：risk-coverage 評估框架與「哪類棄權訊號在 ADD 的 shift 結構下有效」的實證結論是持久的。

**技術路線（10 個月）**：
1. 月 1–2：復現 3 個偵測器（AASIST、SSL-based、RawNet2 系）；建立 shift 評估矩陣（in-domain / unseen-generator / unseen-channel / 兩者疊加）。
2. 月 3–4：量測 baseline calibration（ECE、reliability diagram）與 risk-coverage 曲線——此階段產出即是一個可發表的 benchmark 結果。
3. 月 5–7：實作與比較 5+ 種棄權機制；重點科學問題：在「分數整體失去鑑別力」（AUC≈0.5）的 failure mode 下，特徵空間訊號是否仍保有「這個輸入很陌生」的資訊。嘗試 conformal prediction 給出有理論保證的錯誤率控制。
4. 月 8–9：deferral policy 模擬（用 #2 公佈的人類表現數據建 human model）；小規模 listening study（30–50 人，先送 IRB）驗證「機器棄權子集上人類是否確實較強」。
5. 月 10：整合為 expected-cost 分析（多個 base rate 與 cost 假設下的敏感度分析）、寫作。

**預期貢獻**：(1) ADD 領域第一個 shift-aware 的 selective prediction benchmark 與評估協定；(2) 關於「何種不確定性訊號在 unseen-generator shift 下存活」的實證結論（正面或負面都有價值）；(3) 一個以人機互補實證為基礎、以 expected cost 評估的 triage 框架——直接可轉譯為消費端防詐產品的設計原則。目標 venue：INTERSPEECH / ICASSP，triage 部分可投 usable security workshop。

**風險與備案**：最大風險是所有棄權訊號在 AUC≈0.5 的 failure mode 下全部失效。備案：論文轉向「嚴謹量化此失效 + calibration benchmark」——參照 VoiceWukong 的先例，高品質的負面結果在這個領域是可發表的；且月 3–4 的 benchmark 產出已保底半篇論文。

### 兩案關係

兩案可獨立成篇，也存在自然的銜接：提案一的「passive score」訊號可直接採用提案二的校準後輸出，「訊號矛盾/缺席」的分級與「棄權」在系統層面同構——若團隊有兩位學生，這是一組互補題目；單一學生則二擇一，我個人認為提案一 novelty 錨點更硬，提案二可行性下檔更穩。

---

## 4. 我留給其他討論者的問題

1. **給 Agent D（紅隊）**：針對提案一——假設攻擊者完全知道稽核協定，最便宜的繞過是什麼？我尤其想知道：re-recording（空氣通道翻錄）是否讓 watermark 與 manifest **同時**消失，使稽核優雅地退化成單靠 passive detector（此時分級是否仍有價值），還是存在讓訊號「選擇性存活」以偽造一致性的更聰明攻擊？另外，提案二的棄權機制是否會開啟新攻擊面——攻擊者刻意把樣本推入「高信心真人」區而非僅僅逃避偵測？

2. **給 Agent B（Provenance 研究者）**：C2PA v2.4 對 audio 的實際成熟度到底如何——soft binding、durable credentials 在 WAV/MP3/Opus 上有沒有可用的參考實作？以及一個更根本的問題：對「即時通話」這種串流情境，你認為存在任何在協定上站得住的簽署點嗎？如果答案是否定的，那所有 provenance 方案對「詐騙電話」這個核心情境是否先天缺席，只能覆蓋「語音訊息/媒體檔案」？這決定了提案一的威脅模型邊界該怎麼誠實地寫。

3. **給 Agent F（一般民眾代表）與 Agent C（訊號處理研究者）**：給 F——如果防詐 App 對三成的來電顯示「無法判定，建議掛斷後用已知號碼回撥」，你會照做，還是嫌煩直接關掉 App？棄權率的可用性上限在哪？這個數字直接決定提案二的 coverage 目標。給 C——你手上有沒有 audio watermark（AudioSeal 類）經過「喇叭播放 → 手機翻錄」空氣通道後存活率的實測或文獻數據？這是提案一風險評估中我最缺的一塊拼圖，若存活率近零，提案一的攻擊章節就要改寫。
