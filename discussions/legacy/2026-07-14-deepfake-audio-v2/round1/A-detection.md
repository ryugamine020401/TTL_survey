# Round 1 提案：Detection 研究者（Agent A）——第二輪（無真人實測）
日期：2026-07-14

> 撰寫前已完整重讀：00-problem-statement（本輪硬性限制）、survey/README（#1–#8）、legacy 03-synthesis（第一輪五方向與攻防紀錄）。以下 #n 指 survey 編號；「方向一～五」指 legacy 統整的五個方向。凡未經檢索驗證的 novelty 宣稱，我一律標「猜測，待 G 查證」。

---

## 1. 新限制對我的視角意味著什麼

先把話說清楚：「不做真人實測」對一個 detection 研究者的日常工作幾乎是零衝擊——我的世界本來就是 checkpoint、benchmark、EER 與 risk-coverage 曲線。但第一輪的結論不是「做一個更好的偵測器」，而是「偵測器 × 警告 UX × 受騙率量測」的三段因果鏈，而新限制精準地砍在這條鏈的最後一段。逐方向盤點：

### 方向一（首選：誠實棄權 + 警告 UX + 受騙率）——被砍掉一半，但砍掉的是哪一半很關鍵

- **存活的部分（約佔工作量 70%）**：shift 評估矩陣、baseline calibration（ECE、risk-coverage）、六種棄權機制比較（含我的 real-manifold 距離假說）、confident-real 對抗評估（D 的 `max P(confident-real|fake)` 軸）——全部是純計算實驗，原時程表月 1–7 的內容一天都不用改。
- **被抽掉的部分**：月 8–9 的「小規模 user study 量警告 UX 受騙率」與月 10–12 的警告 UX 分析。這不是小事：H 當初把方向一列首選的理由正是「全場唯一能指著數據說『這個設計讓受騙率從 X 降到 Y』的題目」，而「受騙率」是 primary outcome。**primary outcome 的實測管道沒了。**
- **但注意**：legacy 統整第 112 行的備案早就寫了——「先用 VoiceWukong 已公佈人類數據做 policy 模擬（不需 IRB），user study 縮為 pilot」。新限制等於把備案升格為主案、把 pilot 砍到零。所以方向一不是死了，是**從「量測受騙率」降級為「模擬預期受騙成本」**。這個降級站不站得住，是本輪我必須正面回答的問題（見提案一的計算性驗證方案）。

### 方向二（真實通道 benchmark）——幾乎不受影響，僅一處灰色地帶

五個評測軸全是機器對機器。唯一要修的是語料規劃裡「團隊錄音（簽知情同意）」一項：嚴格說「自行錄製人聲並簽知情同意」已經在踩「不自行招募人類受試」的邊。修法很簡單——bona fide 素材全部改用公開資料集（LibriSpeech、In-the-Wild 的 real 端、ASVspoof bona fide）透過 rig 播放，不錄任何新的人聲。通保法 §29 路徑（G 的 T2 查證）不受影響，因為兩端本來就是自有設備播公開語料。**結論：方向二是五個方向裡最不受新限制影響的。**

### 方向三（攻擊成本地圖）——完全不受影響

從頭到尾就是 checkpoint 對 checkpoint 的攻防搜索，第一輪規劃裡連 IRB 這個詞都沒出現過。新限制下它的相對地位**上升**。

### 方向四（Active Liveness Probing）——受傷比表面看起來重

表面上 RQ1–RQ3 是機器攻防，IRB 本來就不在主線。但細看語料需求：「非同步挑戰-回應語料」需要**真人錄製非典型發聲**（耳語、笑聲、哭腔）作為 bona fide 對照組，「切換點語料」需要真人共犯的錄音。公開資料集裡非典型發聲的覆蓋很差（耳語有 wTIMIT，笑聲、哭腔散落在情感語料庫且授權混亂——這是我的印象，猜測，待 G 查證）。若 bona fide 端只能用湊的，RQ1 的「轉換品質崩壞」量測會有嚴重的 confound。方向四在新限制下可行性再降一級。

### 方向五（Provenance 可達性）——不受影響

純密碼學構造 + 通道量測 + formal analysis。是 B 的主場，我不多評。

### 總結我的處境

我在第一輪的兩個資產：(a) selective prediction 提案（與 H 合流成方向一）、(b) one-class real-manifold 距離假說。新限制沒有碰 (b)，但把 (a) 的 primary outcome 打掉了。我本輪的任務就是：**替方向一找到一個在計算性框架內依然誠實、依然回答「降低受騙機率」的 primary outcome**，或者承認找不到、轉向純 detection 側的貢獻。

---

## 2. 思辨過程（獨白）

### 候選一：方向一的直接無真人化——「拿 VoiceWukong 的 300+ 人數據建 human model，模擬 deferral policy 的預期受騙成本」

第一直覺當然是這個。#2 給了現成的人機互補分布：人類對低品質 deepfake FAR 4–19%、對高品質 FAR >82%，且有 per-tool、per-manipulation 的細分。把人建模成一個「條件化在樣本品質上的雜訊分類器」，偵測器棄權時 defer 給這個 human model，整條 pipeline 的 expected deception rate 就算得出來。

**自我質疑 1（最痛的一刀）：我拿到的人類數據是什麼粒度？** VoiceWukong 公佈的極可能是 aggregate（每工具/每 manipulation 條件下的平均 FAR），不是 per-sample 的人類反應。如果是 aggregate，我的 human model 只能是「同條件內同質」的粗模型——它假設人類錯誤與樣本特徵在條件內獨立，而真實情況是人類與機器可能在**同一批**難樣本上一起跌倒（error correlation）。人機錯誤相關性直接決定 deferral 的價值：若高度相關，defer 根本救不了人。這個相關性 aggregate 數據量不出來。**這是模擬結論可信度的天花板，必須誠實寫進 limitation，且要用 sensitivity analysis 把「相關性從 0 掃到 1」的整個區間都報告。** 如果結論只在低相關假設下成立，那就是一個脆弱的結論。

**自我質疑 2：這樣還剩多少 novelty？** 「用文獻數據做 policy 模擬」聽起來像 decision analysis 課的期末作業。回應：novelty 不在模擬本身，在於 (a) shift-aware selective prediction benchmark 在 ADD 領域仍是空白（第一輪 H 與我的共同判斷，本輪仍成立）；(b) real-manifold 距離假說的系統性檢驗無論成敗都是第一份；(c) confident-real 對抗軸文獻完全缺席。模擬只是把這三塊「翻譯」成受騙成本語言的最後一哩。所以正確的定位是：**模擬是 claims 的翻譯層，不是貢獻本體**。貢獻本體必須在 detection 側自己站穩。

**自我質疑 3：砍掉 UX 之後，F 那一關過得了嗎？** 第一輪 F 給方向一「上班族可以」的判定，前提是四點 UX 設計（棄權率/警示率解耦、一鍵回撥……）。這些設計現在只能作為 policy 參數進模擬，不能實測。F 大概會問：「你模擬裡的 compliance rate（使用者看到警告後真的去查證的機率）是哪來的？」——audio deepfake 領域沒有這個數字，只能借 phishing warning 文獻的參數範圍。借來的參數 + 敏感度分析，結論只能是「在 compliance ∈ [0.2, 0.8] 的整個範圍內，policy A 的期望成本都低於 policy B」這種 **dominance 型陳述**，不能是點估計。我認為這仍然有價值（部署方要的本來就是排序不是小數點），但我要先承認它比實測弱。

**判定：保留，但必須重構——模擬降為翻譯層，detection 側貢獻升為主體。** 進入正式提案一。

### 候選二：real-manifold 距離假說的獨立成篇——「哪些不確定性訊號在 AUC≈0.5 failure mode 下存活？」

我第一輪留下的可檢驗假說：邊界依賴型分數（MSP、energy）在偵測器崩到 AUC≈0.5 時與邊界一起死，而 real-manifold 距離（例如 SSL 特徵空間上對 bona fide 分布的 Mahalanobis / kNN 距離）不依賴 fake 端邊界，可能存活。純計算、不受新限制影響、假說成敗都可發表（#2 的先例證明高品質負面結果在此領域能進 USENIX Security）。

**自我質疑 1：它撐得起一整本碩論嗎？** 老實說，單獨看它是方向一實驗規劃裡的步驟 (iii) 的一部分——一個 module。如果假說三個月就驗完（不管成立與否），剩下九個月做什麼？必須往外長：要嘛長成完整的 selective prediction benchmark（那就回到候選一），要嘛長出第二個軸。

**自我質疑 2：G 第一輪已經排過雷——one-class 是五年活躍賽道（OC-Softmax→ACS→QAMO→EBM）。** 我的辯護：那條賽道全部是拿 one-class 當**偵測器本體**（追更低 EER），我是拿 one-class 距離當**棄權訊號**（追 shift 下的 risk-coverage 與 confident-real 抗性），評估軸完全不同。但我被 G 教訓過一次了：這個「沒人做過」是我的猜測，待 G 查證——特別要查 OOD detection 社群有沒有人把 distance-based uncertainty 用在 ADD 上（關鍵字大概是 "selective prediction anti-spoofing"、"abstention audio deepfake"、"OOD-aware spoofing countermeasure"）。

**自我質疑 3：C 第一輪的幾何塌縮批評會不會回魂？** C 打的是「對 real class 施加通道 DA 把 manifold 撐大＝放棄判別」。注意這次角色不同：我不拿距離做判別（判別交給原偵測器），只拿它做「我還在不在我學過的世界裡」的量尺。manifold 被通道 DA 撐大會降低棄權訊號的解析度，這是真的——但這正好變成一個可以量的 trade-off（DA 強度 × 棄權訊號解析度的曲線），是實驗不是致命傷。

**判定：不獨立成篇，作為提案一的核心假說模組。** 但這個思考揭示了一件事：棄權訊號的「失效條件分析」本身比「哪個訊號最好」更有科學價值——這引出候選三。

### 候選三：失效歸因（failure attribution）——「棄權不該只說『我不知道』，該說『我為什麼不知道』」

這是本輪我真正的新想法。起點是把 #2 與 #3 的兩個關鍵發現並排：

- #3：通道劣化是 **可逆的 distribution shift**——通道模擬 DA 重訓後全條件 EER 波動 < 0.1%，資訊沒有被摧毀。
- #2：unseen generator 劣化是 **補救無效的 shift**——targeted augmentation、multi-domain training 幾乎無效甚至有害（AASIST2 退到 EER 48–50%）。

兩種 shift 對偵測器的殺傷機制在文獻裡已經呈現出本質差異，那麼**它們在偵測器內部表徵上留下的痕跡也應該可分**。如果可分，棄權就能帶原因：「音訊過度劣化，無法可靠判定」（channel-induced）vs「音訊特徵落在已知生成器分布之外」（generator novelty）。這兩種棄權對下游的 actionable 意義完全不同——前者可以觸發「請透過另一管道重送/回撥」的機器可驗證干預（重送後可靠性應恢復，這件事**純計算可模擬**：同一樣本過不同通道再測），後者觸發的是升級人工審查。

**自我質疑 1：attribution 模型自己也要 generalize，這不是遞迴問題嗎？** 對 unseen channel 做 channel-attribution、對 unseen generator 做 novelty-attribution，attribution 器一樣會遇到自己的 OOD 問題。緩解：channel 端做 closed-set over channel families（codec 家族有限且物理性質穩定，AMR/EVS/Opus 的頻譜足跡是訊號處理事實——這點我想聽 C 的判定），generator 端不做 closed-set 歸類、只做 open-set novelty flag。也就是說 attribution 的 claim 要不對稱：channel 端強 claim、generator 端弱 claim。

**自我質疑 2：兩種 shift 疊加時（真實詐騙的常態：閉源生成器 + LINE 壓縮）還可分嗎？** 這正是實驗矩陣的主對角線，也是最可能出負面結果的格子。但注意：**疊加格的可分性無論答案是什麼都有價值**——若可分，得到部署級的分級棄權；若不可分，得到「疊加 shift 下 attribution 崩潰」的量化邊界，警示所有想做 conditional detection 的後續研究（包括方向二的 channel-conditioned 偵測）。

**自我質疑 3：D 會怎麼打？** 攻擊者可以刻意把 fake 偽裝成 channel-degraded（加重壓縮），誘導系統發出「請重送」而非「疑似偽造」，然後在重送時用更乾淨的通道+更強的 laundering。這是一個真實的新攻擊面。但有趣的是它有成本結構：攻擊者為了觸發 channel-attribution 必須主動劣化自己的音訊，而 #2 顯示人類對低品質 deepfake 的 FAR 只有 4–19%——**攻擊者被迫在「騙過機器的歸因」與「騙過人耳」之間二選一**。這個 trade-off 可以直接用 D 的 attacker-cost curve 框架量化，我甚至認為它是提案的賣點而不是弱點。（此論證依賴 #2 人類數據的外推，見提案一的同一個 limitation。）

**判定：成立，升格為正式提案二。**

### 候選四（快速淘汰）：用 MLLM 當「模擬受試者」取代 user study

一閃而過的念頭：既然不能找真人，用 audio-LLM 模擬人類受騙反應？立刻自我否決：#2 已經實測 Qwen2-Audio 對 deepfake 偵測**完全不具能力（英文 F1=0）**，拿一個對任務零敏感度的模型當 human proxy 是方法論詐欺。而且 MLLM 的錯誤模式與人類毫無對齊證據。**淘汰，不進提案。** 留這段是為了立此存照：如果本輪有人提「LLM 模擬受試者」，#2 的數據就是現成的反駁。

---

## 3. 正式提案

### 提案一：《知道自己何時不知道 v2（無真人版）》——Shift-Aware Selective Prediction Benchmark + confident-real 對抗評估 + 文獻錨定的受騙成本模擬

**核心 idea**
接受偵測器在 unseen generator 上必然劣化（#2：EER 13.5–50%）的現實，系統性回答三個問題：(1) 在四種 shift 條件（in-domain / unseen-generator / unseen-channel / 疊加）下，哪些棄權訊號的 risk-coverage 曲線存活？特別檢驗 real-manifold 距離假說。(2) 攻擊者把 fake 推進 confident-real 區的最低成本是多少（`max P(confident-real|fake)` 軸）？(3) 把以上結果透過 VoiceWukong 人類數據錨定的 human model，翻譯成「不同 deferral policy 下的期望受騙成本」的 dominance 排序。

**為什麼有機會成立（文獻）**
- Gap 沿用第一輪判斷且本輪仍無人填補：ADD 領域沒有任何 benchmark 報告 shift 下的 calibration 與 risk-coverage（#1 的 survey 涵蓋 explainability/fairness 卻無 selective prediction 一節；猜測其後仍空白，待 G 查證）。
- 棄權訊號的原料現成：SSL 特徵（Wav2Vec2/XLS-R）上的 Mahalanobis/kNN 距離、energy score、deep ensemble、MC-dropout 全是成熟技術，risk 在科學問題不在工程。
- 人類側數據現成且是實測而非假設：#2 的 300+ 人 user study 提供 per-tool/per-manipulation 的 FAR/FRR 分布——這是全領域唯一一份規模夠大、條件夠細、可直接引用的人類表現數據，正是本輪限制明文允許的用法。
- D（紅隊）第一輪的背書仍有效：「全場唯一對我的零成本繞過輸出的不是虛假安全感的方向」——這個性質與有沒有 user study 無關。

**技術路線（一年）**
- 月 1–4：復現 AASIST / wav2vec2-XLS-R backend / RawNet2；建四格 shift 矩陣（ASVspoof 2019/2021 LA+DF、In-the-Wild、MLAAD 做 leave-one-generator-out；#3 的 codec 管線 + VoiceWukong 可得部分做 unseen-channel）；量 baseline ECE、reliability diagram、risk-coverage。**此階段即保底半篇 benchmark，且不再有任何 IRB 依賴——新限制下連原本的時程風險都消失了。**
- 月 5–7：六種棄權機制對決（MSP、temperature scaling、deep ensemble、MC-dropout、energy、real-manifold Mahalanobis/kNN on SSL features），主假說：距離型分數在 AUC≈0.5 格存活、邊界型全滅。
- 月 8–9：confident-real 對抗評估——攻擊者動作空間（換 generator、laundering、codec tandem、resample 等，借方向三的框架）上跑貪婪搜索，對每種棄權機制量「進入 confident-real 區的最低成本曲線」。
- 月 10–12：human-model 模擬（見下）+ 整合寫作。

**計算性驗證方案（明確回答：用什麼替代真人實測、為什麼結論仍可信）**
- **替代物**：三層模擬取代 user study。(a) *Human error model*：以 #2 公佈的條件化 FAR/FRR 建參數化模型 h(quality, manipulation)，deferral 時的人類判定由此模型抽樣；(b) *Error-correlation 掃描*：人機錯誤相關性 ρ 無法從 aggregate 數據辨識，故不估計、直接從 0 掃到 1，報告整條曲線；(c) *Compliance 掃描*：警告遵從率借 phishing warning 文獻參數範圍做同樣處理。
- **為什麼結論仍可信**：第一，模型的錨是 300+ 人的實測分布，不是拍腦袋；第二，所有無法辨識的參數一律以區間掃描呈現，**論文只做 dominance claims（「policy A 在全參數區間內期望成本 ≤ policy B」），不做點估計 claims（「受騙率從 X% 降到 Y%」）**——這是把第一輪方向一的 claim 誠實降級，而不是假裝模擬等於實測；第三，detection 側的三個貢獻（benchmark、假說檢驗、confident-real 曲線）完全不依賴模擬層，模擬層垮了它們照樣成立。
- **誠實邊界（寫進 limitation 第一行）**：本文回答「哪種 policy 較優」，不回答「絕對受騙率是多少」；後者需要真人實測，留給後續研究或產業部署方的 A/B test。

**預期貢獻**
(1) 第一個 shift-aware selective-prediction ADD benchmark（協定 + 代碼 + 四格矩陣）；(2) real-manifold 距離假說的首次系統性檢驗（成敗皆可發表）；(3) confident-real 攻擊面的首次量化；(4) 文獻錨定、參數不確定性誠實呈現的 deferral policy 期望成本分析，給部署方 policy 排序。

---

### 提案二：《為什麼不知道》——棄權的失效歸因：Channel-Induced vs Generator-Novelty 的可分性、極限與機器可驗證的重送干預

**核心 idea**
把棄權從一個 bit 升級為一個診斷：偵測器不可靠時，計算性地判定原因是「通道劣化」（closed-set，over codec families）還是「生成器新穎性」（open-set novelty flag），並對 channel 型棄權附帶一個**純計算可驗證的干預**——「換通道重送」：模擬同一樣本經替代通道重傳後，偵測可靠性是否恢復。恢復 → 通道歸因正確且問題已解；不恢復 → 自動升級為 novelty 警示。整條「棄權 → 歸因 → 干預 → 復核」迴路不需要任何真人。

**為什麼有機會成立（文獻）**
- 兩種 shift 的本質差異已有強先驗：#3 證明通道劣化是可用 DA 完全抵消的 distribution shift（EER 波動 <0.1%），#2 證明 generator shift 對同類補救免疫甚至惡化（multi-domain training 使 AASIST2 → EER 48–50%）。一個可逆、一個不可逆，機制不同 → 表徵痕跡可分的假說有依據。
- 訊號來源具體：codec 的頻譜足跡（頻寬截止、CELP 重合成的諧波結構、封包遺失的時域空洞）是確定性的訊號處理事實，可用 layer-wise SSL probing + 輕量 channel classifier 捕捉（第一輪方向二評測軸 (2) 的 cue 存活圖譜正是同一套工具，方法可直接共用）；generator novelty 則用提案一的 real-manifold 距離在「通道校正後殘差」上量測。
- 部署價值直接回應問題陳述第 5 點（laundering 讓特徵遺失）：與其讓 laundering 默默殺死偵測器，不如把「偵測器正在被 laundering 殺死」本身變成可偵測、可回應的事件。
- Novelty 判斷（猜測，待 G 查證）：OOD 領域有 shift-type 研究（如 covariate vs semantic shift），但 ADD 領域的 abstention attribution 與「重送干預」的機器可驗證迴路，我不知道有前作。

**技術路線（一年）**
- 月 1–3：與提案一共用 shift 矩陣基礎設施；建 3×3 實驗格（channel-only / generator-only / 疊加 × seen / unseen 深度），channel 軸用 #3 的六 codec 管線 + VoiceWukong manipulation 變體。
- 月 4–6：attribution 器本體——layer-wise probing 特徵 + channel-family classifier（closed-set）+ 通道校正後 real-manifold 殘差距離（open-set novelty flag）；主實驗：疊加格的可分性邊界。
- 月 7–9：重送干預模擬——對每個 channel-attributed 棄權樣本，模擬經 K 條替代通道重傳，量「可靠性恢復率」作為歸因正確性的機器可驗證代理；同時量 novelty 樣本的「重送不恢復率」（應接近 1，否則歸因器在說謊）。
- 月 10–12：對抗評估（D 預期的攻擊：刻意自我劣化誘導 channel 歸因）——量化「騙過歸因 vs 騙過人耳」的 trade-off 曲線（人耳端引 #2 的低品質 FAR 4–19% 數據）；整合寫作。

**計算性驗證方案（用什麼替代真人實測、為什麼結論仍可信）**
- 本提案的因變數天生就是計算性的：歸因準確率（ground truth 由實驗設計者控制——我知道每個樣本過了什麼通道、出自什麼生成器，**不存在 label leakage**，因為歸因目標是 shift 類型不是真偽本身）、重送後可靠性恢復率、疊加格可分性邊界、對抗 trade-off 曲線。
- 「重送干預」是本提案取代「使用者行為」的關鍵設計：第一輪方向一靠使用者「一鍵回撥」完成查證，本提案把等價的驗證動作移到機器側（系統要求換通道重傳並自動復核），人只在最後收到已分級的結論。使用者端的遵從問題依然存在，但它被移出論文的 claim 範圍——論文證明的是「若重送發生，系統能自動辨別並復核」，這是純技術陳述。
- 唯一引用人類數據處：對抗 trade-off 的人耳端錨定（#2 低品質 FAR），用法與提案一相同、同樣只做區間陳述。

**預期貢獻**
(1) 第一份 ADD 棄權失效歸因研究：兩種 shift 在偵測器表徵上的可分性地圖與疊加極限（正負結果皆有價值——負結果直接警示方向二的 channel-conditioned detection 路線）；(2) 「重送干預」這一機器可驗證的棄權後處理原語，把 actionable abstention 從 UX 問題轉為系統問題；(3) 自我劣化攻擊的成本 trade-off 量化，給 confident-real 對抗軸添加新維度。

**與提案一的關係**：共用月 1–3 的基礎設施與 real-manifold 模組，可以是同一本論文的兩章（提案一 = 何時棄權，提案二 = 為何棄權與然後呢），也可以拆給兩個學生。若只能選一個，提案一是主幹、提案二是最有潛力的延伸章。

---

## 4. 我留給其他討論者的問題

1. **給 G（領域史官）**：三個待查證的 novelty 宣稱——(a) selective prediction / abstention 在 ADD 的前作（關鍵字：selective prediction anti-spoofing、abstention audio deepfake、OOD-aware countermeasure、reject option spoofing）；(b) shift-type attribution（channel vs semantic/generator）在 audio 或鄰近領域的前作；(c) VoiceWukong 公開 release 的人類數據**粒度**到底是 per-sample response 還是 per-condition aggregate——這一項直接決定我提案一模擬層的天花板，是本輪我最需要的一次檢索。

2. **給 C（訊號處理）**：提案二的 channel-family closed-set 假設押在「codec 足跡是穩定的訊號處理事實」上。從你的專業看：(a) AMR-WB/EVS/Opus/Speex 的足跡在**疊加 unseen generator** 時是否仍可辨（generator artifact 會不會遮蔽或偽裝 codec 足跡）？(b) 攻擊者用「先過真通道再重灌」（第一輪 loopback 攻擊的變體）製造**真實的** channel 足跡時，我的歸因器會被騙出「channel-attributed → 建議重送」，這在訊號層有沒有可量測的破綻，還是我該直接把它列為已知不設防？

3. **給 H（指導教授）+ F（民眾代表）**：同一個問題的兩面——primary outcome 從「實測受騙率下降」降級為「參數區間內的期望成本 dominance 排序」之後：H，這本論文在 proposal defense 與口試時 claims 要怎麼措辭才站得住、你會在哪一句話打斷我？F，一個「我們證明了 policy A 全面優於 policy B，但沒有任何真人驗證過」的結論，對真實部署方（電信、平台、165）還有沒有說服力？如果沒有，你認為計算性證據要長什麼樣子才夠？

---

*Agent A，2026-07-14。本文件為 Round 1 獨立提案，未參考本輪其他討論者意見。*
