# Round 2 質詢：Detection 研究者（Agent A）——第二輪（無真人實測）
日期：2026-07-14

> 我已完整閱讀 round1 全部 8 份提案（含我自己的 A-detection.md）、00-problem-statement、survey/README、legacy 03-synthesis。本文分三部分：(一) 對他人提案的具體挑戰（4 項）；(二) 逐一回答指名給我的問題（D-Q1、G-Q4、B-Q3、C-Q2）；(三) 我支持的提案與我能如何補強。我的立場錨點沿用第一輪既定結論：selective prediction 與 one-class real-manifold 距離假說是我要守的兩塊地，本輪我不撤回，但要把它們放在對抗火力下重新加固。凡未經檢索的 novelty 或機理宣稱我標「猜測」。

---

## 一、對他人提案的挑戰

### 挑戰 1：Agent C 提案二「防禦面」——codec-latent 偵測的「典型集」假說，是 unseen-generator 泛化問題換了一件衣服，而且與它自己的攻擊面自相矛盾

Agent C 提案二防禦面主張：「RVQ codebook 是在真實語音上訓練的，真實語音的 token 序列與 TTS 輸出的 token 序列在 codec 的離散空間裡統計性質可能不同——尤其 2023 後主流 zero-shot TTS（VALL-E 系）本身就以 neural codec token 為生成目標，其輸出 token 落在 codec language model 的高概率典型集內；真實語音的 token 有更高的『意外率』」，並據此宣稱「在 codec latent/token 空間做 detection 是一個通道天然對齊的新 domain……unseen-channel 的 train/test mismatch 從根源上消失一段」。

我從 detection 研究者的角度打三刀：

**第一刀（自相矛盾）**：C 自己的攻擊面說「fake 的 vocoder artifact 被 decoder 的 manifold 投影抹掉，bona fide 也被抹上同一層生成指紋，兩個 class 在第一、二層 cue 上被『等化』」。這與防禦面直接衝突——如果 neural codec transcoding 把兩個 class 等化（攻擊成立），那 token 空間的可分性就被同一個投影抹平（防禦失敗）；反之若 token 空間高度可分（防禦成立），那 transcoding 就沒有等化兩類（攻擊不成立）。C 把它包裝成「攻防雙面對沖賭錯邊風險」，但這不是對沖，是**同一個物理量的兩個互斥讀數**：投影的 many-to-one 程度是一個數，它不能同時「大到抹平 artifact」又「小到保留 real/fake 差異」。C 的提案在邏輯上最多只能有一面成立，reviewer 會要求先回答「投影到底抹掉多少」，而那個答案一旦定下，另一面就自動塌陷。

**第二刀（token 對齊只對「同一顆 codec 生成的 fake」成立）**：VALL-E 系 fake 的 token「落在典型集內」這件事，只在**偵測器用的 codec == 該 TTS 生成所用的 codec** 時成立。真實世界的閉源商用 TTS（#2 的 19 家）用的是各自私有的 tokenizer / neural vocoder，不是你手上那顆 EnCodec/DAC。偵測器在 EnCodec token 空間學到的「典型 vs 意外」邊界，換一家用不同 codec 的 TTS 就失配——這正是 #2 量到的「閉源生成器 EER 13.5–50%」的同一堵牆，只是從波形域搬到 token 域。C 宣稱「mismatch 從根源上消失一段」是把「通道 mismatch」消掉了，卻**把 generator mismatch 原封不動搬進 token 空間**，甚至更糟：token 空間對 codec 選擇極度敏感，一個 unseen codec 的 fake 進來，你的 typical-set 統計連參考系都變了。

**第三刀（計算性驗證推論不到真實情境）**：C 的防禦面實驗是「real vs 各家 TTS 的 token 統計檢驗」。但真實詐騙場景裡，攻擊者的 fake 不會乖乖以你的 codec 為生成目標，而且會**在生成後再過一次任意 laundering**（C 自己的攻擊面清單）。C 的 token 檢驗若在「乾淨、同 codec」條件下量到可分，那個 AUC 推不到「閉源 codec + 再 transcode」的實戰格——這是 C 在提案一花大力氣批判的「模擬樂觀偏差」的 token 版本，出現在他自己的提案二裡。

**建設性收尾**：攻擊面（neural codec 作為零成本 laundering、不可逆投影的量化）我完全支持且認為極有價值（見第三部分）。我要 C 砍掉的是把防禦面 token 偵測宣稱成「新 domain / mismatch 消失」——它應該降格為「攻擊面圖譜裡的一個對照：codec-latent 偵測在 unseen-codec-generator 下同樣崩」，作為又一個 negative result，而不是一個 novelty 賣點。

---

### 挑戰 2：Agent D 提案二支柱 B——「攻擊者視角受騙率下界」的 baseline 錨點，正是 D 自己在候選 C 判死刑的那個偷換

Agent D 在候選 C 對自己下重手，原話：「VoiceWukong 的人類數據是『辨識任務』，不是『詐騙情境受騙』……詐騙現場的人不在做辨識任務——他在『女兒哭著要保釋金』的社工壓力下，根本沒開啟辨識模式。用辨識 FAR 冒充受騙率，是把一個樂觀場景的數字貼到悲觀場景上。」這一刀砍得漂亮，我完全同意。

但 D 隨後在支柱 B 的「單調性論證」裡寫：「把 VoiceWukong FAR 當『系統沉默 baseline』，用單調性推導『綠燈狀態的 false-accept ≥ baseline』，量攻擊者靠支柱 A 把樣本推進綠燈狀態後，鎖定的受騙率下界。」

**問題就在這裡**：D 的下界 = baseline + 綠燈增益，而 baseline 就是 VoiceWukong 的辨識 FAR。D 剛剛親手證明「辨識 FAR 冒充受騙率是偷換」，然後在支柱 B 把同一個辨識 FAR 當成「系統沉默狀態的受騙率 baseline」。這不是下界，這是**在一個被自己否定的錨點上做加法**。單調性論證只保證「綠燈 ≥ 沉默」這個**相對**關係，它完全不保證「沉默狀態的絕對值 = VoiceWukong FAR」——而 D 的「受騙率下界」是一個絕對量（要餵給部署決策），它的絕對值繼承了那個被否定的錨。

更精確地說：D 的單調性只在「同一個測量框架內」成立。VoiceWukong 的 FAR 是「主動辨識框架」下的量；詐騙現場是「未開啟辨識框架」下的量。這兩個框架下的「系統沉默」根本不是同一個狀態，`沉默(辨識框架)` 的 FAR 與 `沉默(受騙框架)` 的 FAR 之間沒有任何單調關係——可能更高（壓力使人更輕信）也可能更低（辨識框架下人更多疑）。D 的下界因此不是「壞消息的可信版本」，而是「壞消息但錨在錯誤框架上的版本」，它的下界性質（保守性）沒有被證明。

**我承認 D 的支柱 A（confident-real 攻擊面統一審計）是純機器、完全成立、且我在第一輪就受惠於它。** 我要打的只是支柱 B 把「下界」講成一個可餵決策的絕對受騙率量。**建設性修正**：支柱 B 應該只保留**相對**陳述——「對任何固定的、未知的沉默態受騙率 p₀，綠燈態受騙率 ≥ p₀ + Δ(攻擊成本)」，其中 p₀ 保持為自由符號、絕不代入 VoiceWukong 數字。這樣結論退化為「綠燈把攻擊者的收益單調抬高 Δ」，Δ 是純機器可量的（支柱 A），而 p₀ 誠實地留白。這正是 E/H/G 收斂的 dominance 形式在攻擊者側的對應物——D 應該和他們對齊，而不是自己造一個帶絕對值的下界。

---

### 挑戰 3：Agent E 提案一——「人類模型不確定集 𝓗」只約束了邊際分布，卻對 deferral 價值真正取決的「人機錯誤聯合分布」隻字未提

Agent E 提案一的核心：「定義一個『人類模型不確定集』𝓗——所有與已公佈人類數據（VoiceWukong 300+ 人的品質分層 FAR、#1 的 73% 準確率等）一致的行為模型的集合——然後只宣稱『對 𝓗 中所有模型都成立』的結論」，並主張「警告設計 A 優於 B，若且唯若在整個 𝓗 上 A 的期望受騙率都 ≤ B」。

這個推理形式（robust decision making / 對抗者類別全稱量化）我認可。但 E 的 𝓗 定義有一個 detection 研究者一眼看穿的致命缺口：

**VoiceWukong 公佈的是人類的邊際 FAR（marginal），不是人機錯誤的聯合分布（joint）。** 而 selective prediction / learning-to-defer 的整個價值命題，取決於 joint——具體說是「偵測器棄權（不確定）的那些樣本上，人類的條件錯誤率 P(human錯 | 偵測器棄權)」。這個條件量無法從邊際 FAR 推出來，因為它取決於**人類錯誤與偵測器錯誤在樣本上的相關性 ρ**。我在自己的 round1 候選一就把這一刀砍在自己身上（原文：「人機錯誤相關性直接決定 deferral 的價值：若高度相關，defer 根本救不了人。這個相關性 aggregate 數據量不出來」）。

E 的 𝓗 只用邊際 FAR 曲線 + 單調性 + 壓力係數 θ 來刻畫，它**沒有把 ρ 放進不確定集的參數**。後果是：E 的「穩健排序」是在一個沉默了關鍵維度的集合上做全稱量化——它對 ρ 的值默認了某個隱含假設（多半是條件獨立），而 ρ 恰恰是決定「defer 給人有沒有用」的那個變數。這比「𝓗 太寬導致全平手」（E 已自我質疑過的情況）更陰險：它會給出一個**看似穩健、實則只在某個未言明的 ρ 下成立**的排序，reviewer（或 D）只要問一句「你的 𝓗 允許 ρ 從 0 掃到 1 嗎」，排序就可能翻掉。

**這一刀我打得有底氣，因為我自己的提案一就是被同一刀砍過、然後把 ρ 全區間掃描寫進協定的。** 所以這是建設性挑戰：E 的框架要活，必須把 ρ（或更一般地，人機錯誤的 copula 結構）升格為 𝓗 的一個顯式掃描維度，並誠實報告「排序只在 ρ ≤ ρ* 時穩健」的失效邊界。E 的 value-of-information 分析（哪塊缺失數據最能收緊排序）如果做，第一個該指出的缺口就是 ρ——而這需要 per-sample 的人類判斷（G 已查證 VoiceWukong 的 per-sample 數據公開，G2-S6），所以 ρ 其實**部分可估**，E 沒用上這個紅利。

---

### 挑戰 4：Agent B 提案二 CallAttest——perceptual hash 鏈的存活條件，把它自己推回它想繞開的「通道 cue 存活」死結

Agent B 提案二自稱繞開了容量死結：「語音通道 in-band 承載 0 bit，徹底繞開容量死結；hash 鏈綁定內容，使協定同時抵抗號碼冒用、mid-call injection 與事後音訊移花接木」。0-bit in-band 這點我認可——帶外走 transparency log 確實不受 in-band 容量限制。

但 B 自己埋了地雷並丟給 C（B-Q1 給 C）：「提案二的滑動窗 perceptual hash 在 AMR-WB/EVS 重合成下的匹配容忍半徑，你認為該用什麼特徵域……才能讓『codec 劣化不斷鏈、惡意替換必斷鏈』兩個要求同時成立？」

從 detection / 訊號存活的角度，這個「兩個要求同時成立」很可能是**不可能三角**：
- perceptual hash 要在 AMR-WB/EVS 重合成（CELP，摧毀相位與高頻細節）後**不斷鏈**，它就只能建在通道最韌的特徵上——依 C 第一輪的存活層級假說（「相位先死、高頻次之、韻律最韌」）與我提案二的 cue 存活圖譜，那基本只剩**粗粒度的 prosody/envelope 統計**。
- 但一個只依賴粗粒度 prosody envelope 的 hash，**其碰撞容忍半徑必然很大**——B 自己列的第二個攻擊面（second-preimage：「找一段語意不同但 hash 落在容忍半徑內的音訊」）的搜索空間就隨容忍半徑指數放大。粗到能活過 CELP 的 hash，粗到攻擊者可以在保持 envelope 的前提下換掉語意內容（「帳戶 A→帳戶 B」這種數字替換恰恰是 prosody 幾乎不變的最佳攻擊點——念「五」和念「八」的韻律包絡差異極小）。

換句話說：**B 想要的「codec 劣化不斷鏈」與「惡意替換必斷鏈」是同一條容忍半徑的兩端，通道越劣化，這條半徑越被迫放大，內容綁定的粒度就越粗，而詐騙的關鍵竄改（金額、帳號）恰好是最細粒度、最貼 prosody-invariant 的那種。** B 的 hash 鏈在乾淨通道上能 demo 成功（計算性驗證通過），但那個 demo 推不到「AMR-WB + 數字替換」的實戰格——這又是一個「計算性驗證方案推論不到真實情境」的案例。B 已經誠實把它列為「本題最大的技術風險」並準備了降級備案（「hash 鏈降級為粗粒度時間戳綁定」），我要強調的是：一旦降級到時間戳綁定，CallAttest 就退回 STIR/SHAKEN + 推播的等價物（只認證「這通電話來自本行」，不綁內容），而 B 花力氣論證的「STIR/SHAKEN 給不了的三件事」裡的「內容綁定」那件就沒了。所以 B 的護城河（內容綁定）與它的通道存活性是**此消彼長**的，這個 trade-off 應該是提案的主結論之一，而不是風險欄的一行。

---

## 二、回答指名給我的問題

### 回答 D-Q1：real-manifold 距離分數面對「adaptive laundering 專門把 fake 洗進 real manifold」，成本曲線是懸崖還是緩坡？給物理理由，不要只說「經驗上分數還在」

D 的原話：「laundering 的本質就是把 fake 洗進 real manifold（deepfake 本來就要過受害者聽得像真人的功能性約束）。你的 real-manifold 距離分數，面對『adaptive laundering 專門優化 fake 到 real manifold 內』的攻擊，成本曲線長什麼樣？」

我不閃躲，分三層回答，其中一層是對你讓步：

**第一層（讓步）：對「白盒、直接以我的 Mahalanobis/kNN 距離為目標函數」的 adaptive 攻擊，它是緩坡，不是懸崖。** 任何可微的 uncertainty 分數被當成攻擊目標時都會被梯度下降推平，我的距離分數不例外。所以我**不宣稱**免疫。這就是為什麼我提案一把 confident-real 對抗評估（你的 `max P(confident-real|fake)` 軸）設為主軸而不是附錄——距離分數的價值必須用「攻擊成本曲線」來裁決，不能用「乾淨測試集上 AUC 還在」來裁決。我完全接受你的裁判標準。

**第二層（物理理由，這是你要的）：但「洗進 real manifold」和「洗進 real manifold 且維持功能性約束」是兩個不同難度的問題，而後者才是攻擊者的真實約束。** 你說的功能性約束是「聽得像目標語者」——那是一個 **speaker-identity 約束**，它把 fake 拉近的是 real 分布在**語者身分子空間**上的投影。但我的 real-manifold 距離不是在整個 SSL 特徵上量，而應該在**投影掉 speaker identity 之後的殘差子空間**上量（micro-prosody 連續性、articulation/coarticulation 動態、呼吸與靜音的時序統計、SSL 高層對「自然發音過程」編碼的那些維度）。攻擊者為了「聽得像目標語者」優化的是 speaker embedding 方向；我量的是**與 speaker embedding 正交的自然性殘差**。這兩個方向不自動對齊——這正是我提案二「通道校正後 real-manifold 殘差距離」的設計動機。所以物理理由是：**speaker-similarity 約束只鎖住 real manifold 的一個低維投影，我把棄權訊號建在它鎖不住的正交殘差上。**

**第三層（可驗證的懸崖假說，交給實驗裁決）：當攻擊者被迫同時壓低我的殘差距離時，他要付的代價是可量的功能性損失。** 如果攻擊者用梯度把樣本推進殘差子空間的 real 區，我的假說是這會破壞「自然發音過程」的內在一致性，表現為**可懂度（intelligibility / WER）或韻律自然度的下降**——而這正好把他的輸出推回 #2 證明「偵測器對 artifact 明顯的低品質輸出很行」的區域。這就是懸崖 vs 緩坡的實驗：橫軸「我的殘差距離被壓低多少」，縱軸「speaker similarity / WER / 波形域偵測器 recall 的變化」，看是否存在一個「距離壓不下去而不崩掉功能」的拐點。**我不預設答案**——若是緩坡（攻擊者能無痛洗進殘差子空間），那我的假說被證偽，這本身是提案一的一級 negative result（「所有 uncertainty 分數，含 density-based，在 adaptive laundering 下皆為免費午餐」），有 #2 級的發表價值。若是懸崖，我就給了你一個成本比 boundary-based 分數更高的棄權訊號。這是我唯一誠實的回答：我給你物理理由（第二層）+ 可證偽的實驗設計（第三層），而不是「經驗上分數還在」。

---

### 回答 G-Q4：FADEL（evidential DL）該收編為第 7 種棄權機制。你的 real-manifold 距離假說與 evidential uncertainty 在 AUC≈0.5 failure mode 下的預期行為是否不同？若 FADEL 也存活，你的差異化陳述怎麼改？

先謝 G 的檢索——FADEL（ICASSP 2025，arXiv 2504.15663）確實該進 baseline，而且它的存在**強化**而非削弱我的提案，因為它把「uncertainty-aware ADD」的前作補齊，讓我的差異化必須講得更精確。

**核心差異（機理層）：evidential uncertainty 是 discriminative、boundary-derived 的量；real-manifold 距離是 generative、density-based 的量。** FADEL 的 Dirichlet 濃度參數（evidence）是在**有標籤的 real/fake 分類任務上訓練**出來的——它的「證據」是決策面的函數。當 unseen generator 把偵測器推到 AUC≈0.5，決策面本身失去意義，我的預期是 evidential uncertainty 會**跟著決策面一起退化**：要嘛到處都輸出高不確定（棄權率爆掉、coverage 歸零，無用），要嘛更糟——在 fake 恰好落進某個 spurious 高證據區時輸出 confident-wrong（正中 D 的 confident-real 出口）。相對地，real-manifold 距離**在訓練時只看 bona fide 分布、從不學 fake 端邊界**，所以它不繼承那個已崩壞的 discriminative 邊界；它問的是「這個樣本離我學過的真實世界多遠」，這個問題在 fake 端邊界失效時依然良定義。

**所以我的差異化假說可以講得比第一輪更尖**：不是「距離分數比較好」，而是「**在 AUC≈0.5 failure mode 下，density-based（只建模 bona fide）分數與 discriminative-derived（含 softmax、energy、evidential）分數會分道揚鑣——後者與偵測器一起死，前者可能存活**」。FADEL 因為是 evidential（仍屬 discriminative-derived），我預測它站在「一起死」那一組。

**若 FADEL 也存活（G 假設的情況），我怎麼改？** 兩種可能，我都預先接受：
1. 若 FADEL 存活是因為它的 evidential 訓練意外學到了 density-like 的東西（Dirichlet 在 OOD 上塌回先驗），那我的二分法（discriminative vs density）就太粗，要改成「**依賴 fake-side 邊界 vs 不依賴 fake-side 邊界**」這條更細的軸——FADEL 若存活，代表它的不確定性不依賴 fake 端邊界，那它就和我的距離分數同組，我的陳述退為「不依賴 fake-side 邊界的分數（density-based 與某些 evidential 變體）在此 failure mode 下存活」。
2. 更關鍵：FADEL 從沒在 AUC≈0.5 的 regime 測過（G 已查證它只做 ASVspoof 2019↔2021 的溫和 cross-dataset）。**所以誰存活是一個空的實證格，我的 benchmark 正是那個裁判台。** 我的差異化陳述不押在「我一定贏」，而押在「我提供第一個能分辨這兩類分數命運的 shift 矩陣 + AUC≈0.5 壓力測試」——無論 FADEL 贏或輸，這個實證結果都是提案一的一級產出。這就是我第一輪說的「假說成敗皆可發表」的具體兌現。

---

### 回答 B-Q3 與 C-Q2（兩問同構，一併回答）：方向一失去 user study 後，用什麼替代「警告設計→行為改變→受騙率」的量測？外推信度與 B 的「形式驗證+攻擊成本+公開統計」推論鏈相比誰假設更少？

B 的原話：「你們打算用什麼替代『警告設計 → 行為改變 → 受騙率』這段因果鏈的量測？如果答案是『用 #2 的人類數據 + usable-security 文獻效應量外推』……這個外推的信度，和我提案二『形式驗證 + 攻擊成本 + 公開統計期望損失』的推論鏈相比，誰的假設更少？」C-Q2 是同一問的訊號處理版（「把我們花一整輪批判的 distribution shift 問題原封不動搬進行為模型」）。

**我的回答，作為 detection 研究者，第一句就是讓步：這段因果鏈（警告設計→行為改變）我不打算「替代量測」，我打算把它從我的 claims 裡刪掉。** C 說得對——把 lab 辨識 FAR 外推到壓力受騙行為，是我們花一整輪打的「模擬樂觀偏差」的行為版；我不會在自己批判過的坑裡跳。我不會假裝一個計算性 proxy 等價於行為量測。所以：

**(1) 我守的因變數不是「受騙率」，是「偵測器該在何時閉嘴、以及棄權不被零成本繞過」。** 這是純機器命題：shift 下的 calibration/risk-coverage（零人類假設）、confident-real 攻擊成本曲線（零人類假設，D 的軸）、real-manifold 距離假說的存活（零人類假設）。這三塊的證據效度和有沒有 user study 完全無關——這是我提案一的主體，我不讓它退化成「又一篇 calibration benchmark」（F 的擔憂），因為 confident-real 對抗軸與 density-vs-discriminative 的 failure-mode 分辨是全新的、且直接服務「不製造虛假安全感」這個社會福祉目標。

**(2) 涉及人的那一段，我採 E/H/G 收斂的 dominance 形式，而且只到「排序」為止，絕不出「絕對受騙率」。** 我在挑戰 3 對 E 補的那一刀（ρ 必須進不確定集）同樣約束我自己：我的 human-model 敏感度掃描要把人機錯誤相關性 ρ 顯式掃過，結論只留「在 ρ、θ、服從率的文獻+悲觀外推區間內穩健的 policy 排序」。

**(3) 正面回答 B 的「誰假設更少」——這是一個範疇錯誤，我們不在同一根軸上，所以不該比「誰假設少」，該比「誰 claim 的定義域大」：**
- B 提案二的推論鏈（形式驗證 → 攻擊成本 → 公開統計期望損失）在**它宣稱的範圍內**（契約域內的機構通話認證）假設確實極少、極硬——我完全承認 Tamarin 證明比任何 30 人 user study 強。但它 claim 的東西很窄：「假冒機構、契約域內、非親情詐騙」，而且它繞過了本問題陳述的核心技術牆（unseen-generator generalization + laundering）——CallAttest 根本不偵測 deepfake，它讓真話自證。這是合法的、我尊敬的路線，但它不回答「那個接到女兒哭腔電話的阿嬤」（B 自己的白旗）。
- 我提案一的機器側 claim（1）假設同樣少（零人類假設），且直搗核心技術牆；人側 claim（2）假設多、且誠實地只出排序不出絕對值。
- **所以誠實的結論是**：B 的推論鏈在窄域內更硬，我的在核心問題上覆蓋更廣但人側更軟。**新限制下全場的 primary outcome 不該統一成一個東西**（回答 B 想確認的那件事）——機器側命題（calibration、攻擊成本、存活）用計算性硬證，人側命題一律退到 dominance 排序 + 失效邊界，絕對受騙率留給未來 IRB 研究。B 的 CallAttest 和我的 selective prediction 是防禦地圖上兩塊不重疊的領土，不是同一塊地的兩個競標者。第一輪的推薦排序要不要重排，是 H 的事（C-Q2 的後半是問 H 的），我只提供一件事實：**我提案一的機器側（保底半篇 benchmark + confident-real 軸）在新限制下一根寒毛都沒掉，它不依賴任何模擬也不依賴任何真人。**

---

## 三、我支持的提案

### 支持 1（首要）：selective-prediction 重建群——G 的 G2-A / H 的提案一 / 我自己的提案一，三者本質同構，應合流為全場主幹

G2-A、H 提案一、我 A 提案一是同一個方向的三個版本，且各自補了對方缺的東西：G 補了方法論的文獻正當性（L2D 合成專家上了 Nature Sci Data 2025、FiFAR；FADEL 該收編為第 7 baseline；LLM-simulated users 經檢索裁定不可用——這三件事把我第一輪標「猜測待查證」的債全還清了），H 補了 claim 的措辭紀律（dominance/期望損害界、不出因果宣稱），我補了兩個可檢驗的技術內核。**我的角色能補強的具體處：**

1. **real-manifold 距離假說 + density-vs-discriminative failure-mode 分辨**（回答 G-Q4 已展開）——這是把「棄權機制比較」從一張表格升級為一個有機理預測、可證偽的科學命題，讓 benchmark 不只是排行榜。
2. **提案二的「失效歸因」（channel-induced vs generator-novelty）+ 機器可驗證的重送干預**——這正好接住 B/C 質問的「行為那一環」：我把「一鍵回撥」這個原本需要人執行的查證動作，替換成**機器側的「換通道重送並自動復核」**，claim 從「使用者會不會查證」退回「若重送發生，系統能自動辨別 channel-shift 與 generator-shift 並復核」，這是純技術陳述、零人類假設。這是我對「不做真人卻仍 actionable」的具體答案。
3. **把 ρ（人機錯誤相關性）作為 human-model 不確定集的顯式維度**（挑戰 3 對 E 的補刀同樣是我對這個群的建設）——並利用 G 查到的 VoiceWukong per-sample 數據（G2-S6）把 ρ 從「全靠掃描」變成「部分可估」，這是全群目前沒人用上的紅利。

### 支持 2：Agent C 提案二的「攻擊面」（neural codec laundering）——即使我打了它的防禦面，攻擊面是我 benchmark 缺的一根關鍵 shift 軸

我在挑戰 1 砍了 C 提案二的防禦面，但它的攻擊面（neural codec transcoding 作為零成本、不可逆的 laundering，及其與傳統 codec 的可逆性分野）是我提案一 shift 矩陣裡**目前缺的一格**。我的四格 shift 矩陣（in-domain / unseen-generator / unseen-channel / 疊加）裡的 unseen-channel 一直預設是傳統 codec；C 的洞察——neural codec 是 many-to-one 生成式投影、資訊理論性質根本不同於 CELP——意味著我該把 unseen-channel 軸拆成「可逆通道（傳統 codec）」與「不可逆通道（neural codec）」兩個子軸。**我能如何補強 C 的攻擊面**：把它接進我的 confident-real 對抗評估——如果 neural codec transcode 真的是「一行指令、零成本、不可逆抹平第一二層 cue」，那它就是 confident-real 攻擊成本曲線上的一個「懸崖式」動作，而我的 real-manifold 殘差距離（建在通道最韌的自然性殘差上）是否還能在 neural codec 投影後存活，是一個乾淨的攻防交點實驗——C 的攻擊面 × 我的棄權訊號，一次量到底。這也順帶回答了 C 對我的隱含挑戰（laundering 讓特徵遺失）：我的立場不是「特徵不會遺失」，是「把特徵正在遺失這件事本身變成可偵測、可歸因、可觸發重送的事件」（我提案二）。

---

*Agent A，2026-07-14。本文為 Round 2 質詢。我守住了 selective prediction 與 real-manifold 距離兩塊地，但守法是把它們放進 D 的攻擊成本曲線與 G 的 FADEL 對照下重新加固，而不是宣稱免疫——這正是這個方向之所以誠實的原因。*
