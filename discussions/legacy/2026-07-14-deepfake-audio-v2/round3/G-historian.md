# Round 3 答辯：領域史官（Agent G）——第二輪（無真人實測）
日期：2026-07-14

> 我是領域史官。Round 1 我用兩顆魚雷（2509.26471 Presentation、RTCFake）擊沉了自己上一輪認證的空白，並把兩個提案（G2-A 選擇性預測、G2-B 電信網多防線審計）重錨在「先承認前作、再守殘存空白」的紀律上。Round 2 全場八人交叉開火，我讀完後的總判斷是：**針對我的挑戰沒有一發是致命傷，但有四發是「我原本站得住、但站得不夠誠實」的修正令**，我全部接受並升級；另有兩發是「你的方法論根基其實比你 Round 1 寫的更硬」的背書，我收下並回填了本輪一次補充檢索的先例。這一輪我不打模糊仗——每一條挑戰我明說接受或反駁，並在最後把兩個提案改寫成合流後的最終形態。
>
> 本輪補充檢索編號 G3-S1、G3-S2，附於文末。

---

## 0. 先把針對我的火力清單列出來（免得漏答被說迴避）

我逐份掃過 Round 2 八個檔案，指向我兩個提案的挑戰與答問如下：

**指向 G2-A（選擇性預測 + 受騙率模擬）：**
- **D 挑戰一（主攻，命中五人含我）**：人類模型不確定集 𝓗 不含「被社工推到集合外的受害者」，robust-over-𝓗 是假保單。+ D 回答我 Round 1 的 Q2：可把社工建成 `A_social(c)` 算子、量 `∂cost/∂c` 斜率，D 願意背書，但警告「社工成本→參數位移」的映射無公開數據錨、只能做結構性上界（「下界的下界」）。
- **C 挑戰一（對 F，但機理同樣打我）**：受騙率模擬把「偵測器過通道後的 recall」當固定輸入餵進鏈，而那個輸入來自模擬 codec，帶著未被掃描的樂觀偏差 γ。掃了人沒掃通道。
- **B 附帶提醒**：受騙率模擬叢集對「人類模型」做全稱量化，對「攻擊者策略」只做列舉存在量化；應升級為 `∀ human model ∀ attacker strategy`。B 願提供「無綠燈原則形式不變量」與「攻擊者可達擾動的類內全稱量化」。
- **E 支持並改框**：把 G2-A 從「L2D synthetic expert（太工程、security venue 會問）」升級為「robust decision making 全稱量化推理形式」。
- **F 家族共同警告**：模擬管線餵的仍是十秒朗讀句，必須換成詐騙現場條件素材（F2 的三秒 × 情緒 × 通道）；θ 要掃到人類貢獻歸零甚至負值（警告接種）；失效邊界按人物×媒介分報；奉送「年齡聽力濾波器」。+ F 回答我 Round 1 的 Q3：所有現場修正方向確定（都比實驗室更糟），並給出公開數據源清單。
- **H 裁定合流 + venue**：G2-A 是撞題群，應與 E1/A1/F1/H1 合成一篇；放行條件＝≥2 獨立錨、可解釋失效邊界、dominance 措辭；security venue 落差真實且不小，主投 INTERSPEECH/ICASSP，別把模擬受騙率送 USENIX/SOUPS。+ A 回答我 Round 1 的 Q4（FADEL：density vs discriminative 的 failure-mode 分辨）。
- **我自己 Round 2 挑戰四的回力鏢**：我當時攻 E「𝓗 錨在品質軸、推論不到壓力軸」，並自承「這對我自己的 G2-A 也部分適用」，還放話「Round 3 我會主張受騙率因變數改採 D 的單調下界」。這筆帳我這一輪必須兌現。

**指向 G2-B（電信網多防線審計）：**
- **C 支持一 + 主張合流**：C1（落差分解 + 模擬器蒸餾 + 可控植入）是它缺的科學靈魂，主張 C1/G2-B/H2 合為一題或明確分工。
- **D 支持二 + 加一個洞**：作為「真實通道武器庫」背書，但點出素材缺陷——bona fide 全用公開朗讀語料量落差，量到的是「朗讀句過電話」不是「詐騙過電話」，要求把 F2 的詐騙現場素材灌進 rig。
- **F 支持二**：通道矩陣權重按真實詐騙分佈排、保留「LINE 文字鋪陳→轉電話收割」混合通道型態。
- **H 支持一（co-首選）**：盛讚史官紀律，補「通行證 framing 立靈魂」「對稱重放設計把關（real/fake 走相同重放路徑、設 C0' 對照臂分離重放 artifact）」「MVP 前置 + watermark 軸護城河」。

好，開始逐條答辯。

---

## 一、逐條答辯

### 答辯 1｜D 挑戰一（社工把人推出 𝓗）——【接受並修正，且這是本輪對 G2-A 最重要的一次升級】

D 說得對，而且這一刀我早在 Round 2 挑戰 E 時就親手砍過同一個位置，只是當時砍在別人身上、這輪必須砍在自己身上。我 Round 1 的 G2-A 把「人」建成「錨定 VoiceWukong 品質-FAR 曲線 + 壓力折損係數 θ∈[0,1] + 服從率 φ」的參數化模型，而這整個集合描述的是「一個知道自己在做辨識任務、電話裡沒有孫子在哭的人」。社工做的事——權威、倒數、親情綁架、警告接種（「等下手機會跳詐騙警告，那是系統誤判別理它」）——是把 φ 推到 **負值語意**（受害者主動幫攻擊者繞過驗證），那個點原則上在 θ∈[0,1] 的自然變異區間之外。robust-over-𝓗 對「自然人類變異」穩健，對「意志被接管」不穩健。這是實話。

**我不反駁，我升級，且吸收 D 自己提供的補救、B 要求的形式、以及我 Round 2 對自己的承諾，三合一：**

修正後 G2-A 的受騙率因變數改為**雙層結構**：

1. **主承載層＝D 的單調下界（受騙率的「符號」，對壓力/品質軸都免疫）**。只宣稱「confident-real 綠燈狀態的受騙率 ≥ 系統沉默 baseline，且綠燈把它單調抬高」，唯一假設是「綠燈不會讓人更警覺」——這條與品質軸、壓力軸都無關，是全場對「推論不到詐騙現場」這一擊最 robust 的因變數。**但我要同時接受 A（Round 2 挑戰 2）與 F（Round 2 挑戰 3）對 D 下界的修正**：baseline 保持為自由符號 `p₀`，**絕不代入 VoiceWukong 的辨識 FAR**（那是「辨識框架」的量，不是「受騙框架」的量，兩者無單調關係）；下界只出「方向（≥）＋到達綠燈的攻擊成本 Δ（純機器可量）」，不出「幅度區間」（無錨、僅供敏感度展示並明標）。

2. **對抗擾動層＝D 的 `A_social(c)` 算子（B 要求的 `∀ attacker` 全稱量化的具體實作）**。把社工建成「攻擊者付成本 c、可沿惡化方向推 (φ, δ, 權威服從 a)」的算子，量的不是固定 human model 下的 expected cost，而是 **`∂(expected cost)/∂c` 斜率**——斜率大＝這個防禦的人因環節是攻擊者的免費槓桿；斜率小＝安全不靠使用者定力。這正是 B 要的「robust over 𝓗 × 攻擊者可達擾動」，也正是 D 願意背書的東西。**接受 D 的誠實警告**：`c → 參數位移` 的映射無公開數據錨，所以只做**結構性上界**——假設 φ 可被推到 0（受害者完全被接管），量「警告 100% 被繞過時這個防禦還剩多少殘值」。結論是「下界的下界」，保守到近乎悲觀，但因此**無法被 reviewer 用『你的 human model 憑什麼可信』打穿**。

**史官補一個本輪檢索的先例（G3-S1），把這個修正從「D 的巧思」升格為「有判例的正統方向」**：把「攻擊者對人類決策模型的操縱」納入 adversary model，不是我們拍腦袋——arXiv 2509.21436《Position: Human Factors Reshape Adversarial Analysis in Human-AI Decision-Making Systems》正是主張「當前 adversary model 未捕捉真實人類攻擊者的動態適應性，給防守方假信心」；arXiv 2602.04003《Adversarial Explanation Attacks on Human Trust》把「AI→人的溝通通道」列為顯式攻擊面（攻擊者不改模型/資料，只操縱 reasoning 的呈現就能誘發信任誤校準）；更早有 biorxiv 2020《Adversarial manipulation of human decision-making》。**所以 `A_social(c)` 這條路線在 2025–2026 已是上升中的可發表範式**，我把它們列進 G2-A 的相關工作，讓「把社工塞進計算框架」有judicial anchor 而非孤兒宣稱。順帶一個現實錨（G3-S2，Mandiant M-Trends 2026）：**voice phishing 已在 2026 超越 email 成為社工首要載體**——這讓「語音詐騙的社工維度必須進模型」從學術潔癖變成領域現實。

**判定：接受，G2-A 受騙率因變數改為「單調下界（主）＋ `A_social(c)` 斜率結構性上界（對抗層）」，品質軸 VoiceWukong 模擬降為輔助敏感度層與 deferral 路由訊號。** 這一步同時兌現了我 Round 2 對自己的承諾、吸收了 D 的補救、實作了 B 的全稱量化、回填了 G3-S1 的先例。

### 答辯 2｜C 挑戰一（掃了人沒掃通道，γ 未進掃描維度）——【接受並修正】

C 打在要害上：G2-A 的受騙鏈把「偵測器過通道後的 recall」當固定輸入，而那個輸入若來自模擬 codec，就帶著未被任何敏感度掃描覆蓋的樂觀偏差 γ（C/H 檢索的 Deepfake-Eval-2024 量級：audio AUC 掉 48%）。一個「掃人掃得很仔細、地基卻沒驗過」的 dominance 排序，在真實通道讓 recall 掉 20–40 點時可能整個翻轉。

**修正**：把 γ（通道樂觀偏差）升格為與 δ（壓力）、φ（服從率）平起平坐的**第三個掃描維度**，其上界直接用 **G2-B/C1 實測的真實通道落差**來標定，而非拍腦袋。dominance 只保留在 δ × φ × γ 三維全區間都不翻轉的部分。這正好把我的兩個提案**焊成一條證據鏈**：G2-B 量出 γ 的真實上界，G2-A 消費它當掃描界——這不是巧合，是本輪限制自然逼出的分工，也是我在最終主張裡主張「兩個方向該由同實驗室分工共構」的技術根據。此外，unseen-channel 一格我 Round 1 已指出可直接用 RTCFake 現成真實通道測試集，這是把 γ 從「模擬值」拉到「至少一個實測源」的最省工路徑。

**判定：接受，γ 進掃描維度，上界錨定 G2-B/C1 實測落差 + RTCFake。**

### 答辯 3｜B 附帶提醒（對人全稱、對攻擊者只列舉）——【接受，且與答辯 1 同一補丁】

B 的密碼學紀律講得比誰都準：一個穩健結論應是 `∀ human model ∀ attacker strategy`，而我 Round 1 做的是 `∀ human model ∃(列舉) attacker`。這條與 D 挑戰一是同一個縫的兩種措辭——B 從形式化語言進、D 從攻擊成本進。答辯 1 的 `A_social(c)` 算子 + `∂cost/∂c` 斜率就是這個補丁的實作：它把攻擊者對人類參數的操縱納入類內全稱量化。**我另外接受 B 提出、我認為 G2-A 該直接收編的一件事**：把「無綠燈原則」從設計哲學寫成 B 所說的 **safety 不變量**（「輸出狀態空間中不存在一個狀態，使得對 fake 輸入輸出正向信任訊號」），且只針對 detector 一種訊號、不硬扯 provenance（避開 D 提案二把三種信任模型焊在一起的可通約性問題）。這讓 confident-real 對抗軸有一個形式化的靶，而不只是攻擊成本 scalar。

**判定：接受，B 認領的「無綠燈形式不變量 + adversary 類內全稱量化」納入 G2-A 合流版，B 為此章共同作者級貢獻者。**

### 答辯 4｜E 改框（robust decision making vs L2D synthetic expert）——【接受升級，但史官加一條保留：兩者不是二選一，我要 both】

E 的升級是對的：「synthetic expert」的宣稱是「在我這族 expert 下 policy A 的 cost 是 X」，會被 reviewer 攻「你的 expert 憑什麼像真人」；「robust decision making」的宣稱是「凡與已公佈數據一致的**所有**人類模型，A 的 cost 都 ≤ B，除非折損超過門檻 θ*」——後者從不主張模型像真人，只主張結論對模型選擇不敏感，殺不死。這個宣稱形式我全盤接受，它比我 Round 1 的措辭強。

**但作為史官我必須加一條 E 沒講、卻決定審稿生死的話**：宣稱形式（robust decision making）和方法論正當性（simulation-grounding 可不可發表）是兩件事，**我兩個都需要，不能用 E 的形式替換掉我的先例**。E 的全稱量化告訴 reviewer「我的結論不賭模型對」；但 reviewer 下一句會問「那你用模擬替代真人這件事本身，學界買帳嗎」——回答這句的是**我 Round 1/Round 2 檢索的先例牆**：L2D 合成專家上了 Nature Scientific Data 2025、FiFAR；認知模型「fit 研究 A、零參數預測研究 B」發到 UMUAI 2026；IMF WP 2025/085 用情境校準模擬做金融壓力測試；LLM-simulated users 經實測判為不可靠（arXiv 2601.17087、2605.10659）故本框架明確不採用。**E 給邏輯形式，我給判例，缺一不可**：只有形式沒判例，reviewer 用「simulation is not evidence」一句打死；只有判例沒形式，reviewer 用「你的模型錯了」一句打死。合流版要同時掛這兩層盔甲。

**判定：接受 E 的宣稱形式升級為 primary claim 的措辭骨架，我的先例牆作為方法論正當性的並列盔甲，兩者都寫進第一頁。**

### 答辯 5｜F 家族共同警告（考卷素材、θ 掃到負、聽力濾波器）——【接受材料修正，但史官附一條 novelty 收窄令】

F 的核心指控成立：在錯的考卷（十秒朗讀句）上做出再穩健的排序也是錯的。G2-A 的模擬管線輸入層必須換成**詐騙現場條件素材**（短句 × 情緒韻律 × 通道劣化）。θ 掃描接受 F 的要求掃到人類貢獻歸零、並文字化「警告接種」機制（φ=0 的格子涵蓋其後果，但必須明寫，否則 reviewer 以為 φ=0 不現實）。年齡聽力濾波器（把年齡別聽力衰退做成可計算的訊號變換套在音訊上）我接受為一件漂亮的計算性物件——它把「高齡」從拍腦袋係數變成有生理學出處的變換。

**但史官必須對 F 的材料層附一條收窄令，這正是我 Round 2 挑戰三對 F2 下的裁定，Round 3 我維持並把它綁進 G2-A 的材料層**：短句軸與情緒軸**各自都已有前作**——短句：AASIST2 for Short Utterance（arXiv 2309.08279）、《ADD at the First Greeting "Hi!"》（arXiv 2601.19573）、Fake-Mamba（arXiv 2508.09294，<3 秒 EER 9.44%）；情緒：HuLA（arXiv 2509.21676）、Phoneme-Level across Emotional Conditions（arXiv 2605.03079）。**所以合流版引用 F2 的材料時，必須把 novelty 錨在「165 繁中詐騙話術語意 × 短 × 情緒 × 通道的四軸交互」，而非宣稱「揭露了一個新的素材偏差軸」**——後者會被上述五篇直接反駁。至於年齡聽力濾波器需要的 ISO 年齡別聽力常模，F 請我查證的這筆我尚未在本輪落實（Round 2 附錄未列具體標準編號），**我標為未結清的檢索債（猜測其存在為 ISO 7029 系年齡聽力常模，需 Round 3 後補查證再引用，不得當已證事實寫）**。

**判定：接受材料修正（考卷換素材、θ 掃到負、聽力濾波器），但材料層 novelty 收窄到「繁中話術 × 四軸交互」並誠實列前作；ISO 常模列查證債。**

### 答辯 6｜H 裁定合流 + venue 策略——【全盤接受】

H 裁定 G2-A 與 E1/A1/F1/H1 是同一篇論文的不同措辭，一個學生做一篇，採「E 框架邏輯 + G 方法論判例錨定 + F 攻擊者引擎與素材 + D confident-real 對抗軸 + A real-manifold 距離模組」。**我不為 G2-A 的獨立性辯護——它本來就不該獨立**，五人撞題是「這條路是對的」的證據，不是搶碗。我在合流版裡的定位很清楚且不與人重疊：**我提供 novelty 防雷（FADEL 收編為第 7 棄權 baseline、shift-aware selective-prediction 錨點經復查仍無前作）、方法論判例牆（答辯 4）、現成紅利（RTCFake 當 unseen-channel 一格省一條工程線）、venue 策略、以及 G3-S1 的 adversary-over-human 先例。** venue 策略我照 H 的裁定執行：方法 + benchmark 主體投 INTERSPEECH/ICASSP，confident-real 對抗軸單獨拆 security workshop，**不把「模擬受騙率」往 USENIX/SOUPS 送**（那是把我自己查到的 LLM-simulated 反感情緒引到自己頭上）。

**判定：接受合流，G2-A 併入選擇性預測叢集，我認領五個不與人重疊的補強位。**

### 答辯 7｜G2-B 的四發（C 合流、D 素材、F 通道矩陣、H 對稱重放）——【全盤接受，且這是我本輪信心最高的方向】

這四發沒有一發是攻擊，全是「讓它更強」的建設。逐一收下：

- **C 主張 C1/G2-B/H2 合流**：接受。C1 的「落差分解 + 模擬器蒸餾 + 可控植入」是 G2-B 缺的科學靈魂——不只說「模擬樂觀了 X%」，而是用受控消融**指認樂觀來自哪一層**（實網 burst 丟包 / jitter buffer / 端點 always-on DSP：AGC、降噪、回聲消除——這些在所有離線模擬裡集體缺席），再封裝成開源通道模擬器讓後人免架 rig。這回應了 H 的紅線「靈魂必須是揭露樂觀偏差、不是收資料」。分工沿用 legacy synthesis：C＝量測/模擬器蒸餾、我＝watermark/provenance bit 存活軸 + Article 50 審計、B＝索引式構造。
- **D 的素材洞**：接受。bona fide 全用公開朗讀語料會量到「朗讀句過電話」不是「詐騙過電話」，必須把 F2 的詐騙現場條件素材（165 話術 × 情緒 × 短句長）灌進 rig。這同時讓 F2 有 rig 可用——雙贏，且把 G2-B 的落差量測綁到真實內容分布上（也讓答辯 2 的 γ 上界是「詐騙過電話」的 γ，而非「朗讀過電話」的 γ）。
- **F 的通道矩陣權重**：接受。通道矩陣按真實詐騙分佈排（VoLTE ≥ LINE 語音訊息 > LINE 通話 > Messenger），保留「LINE 文字鋪陳→轉電話收割」混合通道型態。
- **H 的對稱重放設計**：接受，這是我 Round 1 規劃裡最需要補的方法論漏洞。「real/fake 走完全相同重放路徑使 artifact 成共有常數項、主 claim 是差分量、另設 C0' 重放對照臂分離重放效應」——這防止「砍掉團隊錄音、bona fide 全改公開語料重放」注入的重放 artifact 污染 real 類。

**判定：G2-B 併入真實通道審計叢集（C1/G2-B/H2 合流），我認領 watermark/provenance bit 存活軸 + Article 50 審計這塊零前作護城河，並吸收 C/D/F/H 四項設計修正。**

---

## 二、修正後的最終主張

我把兩個提案改寫成**合流後**的形態，並註明每個零件合併自誰。這兩篇不是我一個人的，是全場 Round 2 收斂的結晶——史官的職責是確保每個零件都掛對前作、標對誠實邊界。

### 最終主張 G3-A（合流版）：《不賭人是什麼樣——分布與社工雙重偏移下語音深偽偵測的穩健棄權決策框架》
*Robust Abstention Decisions for Audio Deepfake Detection under Distribution and Social-Engineering Shift*

**合流自**：E1（宣稱形式：robust decision making 全稱量化）+ G2-A（方法論判例牆 + FADEL 收編 + shift benchmark 骨架）+ F1（攻擊者引擎 + 素材真實性）+ H1（期望損害界 + 部署約束參數 + 三條紅線）+ D1/D2（confident-real 對抗軸 + 單調下界 + `A_social(c)` 算子）+ A1/A2（real-manifold 距離的 density-vs-discriminative failure-mode 假說 + channel/generator 失效歸因）+ B（無綠燈形式不變量 + adversary 全稱量化）+ C（γ 通道偏差掃描維度）。

**兩塊主體，宣稱強度嚴格分層：**

**機器側（零人類假設，保底半篇 benchmark，一根寒毛都沒掉）**
1. shift 評估矩陣（in-domain / unseen-generator / unseen-channel / 疊加；unseen-channel 用 RTCFake 現成真實通道 + G3-B 實測落差）+ ECE / risk-coverage。
2. 7 種棄權機制系統比較（MSP、temperature scaling、deep ensemble、MC-dropout、energy、Mahalanobis-on-SSL、one-class real-manifold 距離），**FADEL evidential DL 收編為第 7 種 baseline**。驗證 A 的 density-vs-discriminative 假說：在 AUC≈0.5 failure mode 下，只建模 bona fide 的 density-based 分數與 discriminative-derived（含 evidential）分數是否分道揚鑣。無論誰存活都是一級產出——這是全場第一個能分辨兩類分數命運的 shift 矩陣 + AUC≈0.5 壓力測試。
3. confident-real 對抗評估（目標 `max P(confident-real|fake)`，沿用全場公約 + D 的 attacker-cost 框架），並以 B 的**無綠燈形式不變量**為靶。
4. 失效歸因（channel-induced vs generator-novelty 可分性地圖，A2 的紮實半邊）——**接受 A/B/E/H/F 一致意見，砍掉「重送干預能救人」的敘事，重送降為評估探針（測歸因器有沒有說謊），不是部署防線**（無 source binding 的重送迴路會變成攻擊者的 laundering oracle，B/C/E/H/F 五人都拆穿了這點）。

**人側（宣稱嚴格退到「符號 + 排序 + 斜率」，絕不出絕對受騙率）**
5. **受騙率因變數＝D 單調下界（主，對品質/壓力軸免疫）**：「綠燈受騙率 ≥ 自由符號 p₀，綠燈單調抬高 Δ」，p₀ 絕不代入辨識 FAR，只出方向 + 攻擊成本 Δ。
6. **對抗擾動層＝`A_social(c)` 斜率的結構性上界**（B 的 `∀ attacker` 全稱量化實作，D 背書，G3-S1 先例）：φ 推到 0 時的殘值 = 「下界的下界」。
7. **輔助敏感度層＝品質軸 VoiceWukong 模擬**（per-sample 分層建模 + 年齡聽力濾波器 + per-difficulty human-deceptiveness 預測器當 deferral 路由訊號），掃描維度 δ × φ × **γ（通道偏差，答辯 2）**，宣稱形式為 E 的 dominance 偏序 + 失效邊界，按**人物 × 媒介**分報（F 要求），失效區如實標為「需真人 pilot 裁決區」。

**計算性驗證方案（替代真人的明確論證，已吸收全部 Round 2 修正）**
- 主承載受騙率宣稱的是 D 單調下界（唯一假設「綠燈不讓人更警覺」，與壓力/品質/素材都無關），不是品質軸模擬——這使 primary claim 對「推論不到詐騙現場」這一擊結構性免疫（我 Round 2 對 E 下的刀，這輪用在保護自己）。
- 品質軸模擬明確定位為**輔助**，其結論一律 dominance 形式（對 human model 點誤差 robust），LLM-simulated users 明確不採用（arXiv 2601.17087、2605.10659）。
- 不做因果宣稱（迴避 arXiv 2605.20767《The Illusion of Intervention》）；產出是「通過計算篩選的最優 policy 候選 + 可證偽 pilot 預測（最低所需服從率、警示率上限、失效邊界）」，明列為後續 IRB 研究的假設。
- venue：主體投 INTERSPEECH/ICASSP，對抗軸拆 security workshop（H/我一致）。
- 誠實邊界寫進第一頁：本框架的穩健性主層對社工可達擾動以「結構性上界」覆蓋，品質軸輔助層不覆蓋高壓社工情境（無此軸公開錨），射程按 F 判定表的人物×媒介標定。

**預期貢獻**：第一個 shift-aware 選擇性預測 ADD benchmark（含 FADEL 的 7 機制系統比較 + density-vs-discriminative failure-mode 分辨）；confident-real 對抗評估軸 + 無綠燈形式不變量的首次實作；ADD 領域第一個把「攻擊者對人類模型的社工操縱」以 `A_social(c)` 斜率納入計算框架的 robust-decision 分析（方法論可被後續所有 ADD 論文複用）。

### 最終主張 G3-B（合流版）：《電信網是最後一哩——真實蜂巢通道上偵測、浮水印與溯源訊號存活的多防線審計》
*The Last Mile is Cellular: A Multi-Defense Audit of Detection, Watermarking, and Provenance Survival over Real Telecom Channels*

**合流自**：C1（落差分解 + 模擬器蒸餾 + 可控植入，科學靈魂）+ G2-B（電信網資料集 + watermark/provenance bit 存活軸 + Article 50 審計）+ H2（對稱重放設計 + 通行證 framing + MVP 前置）+ F2（詐騙現場條件素材灌進 rig）+ D（攻擊者視角切分：tandem / loopback / neural codec transcode）。

**核心 idea（重錨後的誠實形態，前作全部承認）**：建「模擬 → RTC 平台（RTCFake 已做）→ 蜂巢電信網（本論文）」的三層樂觀偏差階梯，用 C1 的落差分解指認樂觀來自哪一層，並把**零前作的 watermark/provenance bit-level 存活軸**設為主軸與護城河，輸出 EU AI Act Article 50（2026-08-02 生效）可讀性審計。

**史官復查後仍成立的殘存空白（前作牆已在 Round 1/2 建好）**：
- 前作：2509.26471 Presentation（做 loudspeaker/direct-inject 框架）、RTCFake（做 IP-RTC 平台通道）、Codecfake（做 neural codec 離線分類）、AuthentiCall（2017 做內容認證但假設雙方真人）——全部承認、全部列相關工作。
- 殘存空白：(i) 公開蜂巢電信網通道資料集（VoLTE AMR-WB/EVS、跨電信商、PSTN interop，前作全在 IP 網/lab presentation，仍空）；(ii) **watermark/provenance bit-level 電信存活（此軸零前作，AudioMarkBench 做模擬擾動、通道前作完全沒碰 watermark，產業無動機自審——這是護城河）**；(iii) Article 50 可讀性審計（零前作，若 bit-level 全滅即政策級否證）；(iv) 繁中/165 情境。

**技術路線（吸收全部修正）**：MVP 前置（月 6 前單電信商 VoLTE + LINE 兩型態＝保底可發表單元）；對稱重放設計（H：real/fake 同路徑 + C0' 對照臂）；素材用 F2 詐騙現場條件（D 要求）；通道矩陣按真實詐騙分佈 + 混合通道型態（F）；可控植入實驗給 watermark bit 存活一個 ground-truth 錨（C）。

**計算性驗證方案**：本方向原生無人因成分，語料全公開資料集化 + TTS 生成，連知情同意都不需要（新限制下反而更乾淨）。結論可信的關鍵在混淆變因控制：固定 UE、標註協商 codec/PLR/jitter、offline/online 精確配對（採 RTCFake 配對方法論，站在前作肩上）、對稱重放分離 artifact。

**與 G3-A 的接口**：G3-B 實測的真實通道落差 = G3-A 答辯 2 的 γ 掃描上界；G3-B 的 RTCFake/電信網測試集 = G3-A 的 unseen-channel 一格。**兩篇是一條證據鏈的量測端與消費端，主張同實驗室分工共構。**

**風險與時間窗**：Delgado 團隊（ASVspoof 組織者）與產業已進場，這題再放一年就沒了——MVP 前置 + watermark 軸（零前作 + 產業無動機自審）作為差異化護城河，是我對這個時間窗的止損設計。

---

## 三、最終推薦（以領域史官立場，從全場所有提案中推薦 1–2 個）

我的裁判尺只有兩把：**(甲) novelty 不隨生成器版本過期**（我 Round 1 的四代歷史循環批判——特徵→模型→資料→評測，每代被下一代生成器歸零；Resemble 2026 已證「ASVspoof 訓練分布過時」）；**(乙) 空白經兩輪復查仍無前作**。用這兩把尺，我推薦：

### 第一推薦：G3-B 真實電信通道多防線審計（C1/G2-B/H2 合流版），主軸押 watermark/provenance bit 存活 + Article 50

以史官立場這是全場最強的選擇，理由三條，每條都對著我的尺：**(甲) 不過期**——「相位 cue 過 CELP 重合成的互資訊掉多少」「AudioSeal/SynthID bit 在真實電信網活不活得下來」是資訊物理與政策事實，不隨生成器換版本歸零，恰好豁免我最狠的歷史循環批判；**(乙) 護城河零前作**——watermark 電信存活軸經我兩輪復查（AudioMarkBench 只做模擬擾動、2509.26471/RTCFake/Codecfake 完全沒碰 watermark、產業無動機自審）仍無前作，Article 50 於 2026-08-02 生效更是給了一個「法規要求的標記在詐騙實際發生的通道上可不可讀」的政策級靶；**(丙) 它是全場的共同地基**——在一個人人靠模擬撐影響力的輪次，這是唯一產出「不需要辯護模擬可不可信」的實測數據、能量出「模擬到底樂觀多少」的方向，F 的 γ、E/H 的 dominance、B 的容量預算、D 的成本地圖全部要消費它。唯一風險是工程工時與時間窗，兩者都有解（MVP 前置 + 分工）。

### 第二推薦：G3-A 穩健棄權決策框架（選擇性預測叢集合流版），前提是受騙率因變數採 D 單調下界為主層

它過我兩把尺的方式與 G3-B 不同但同樣硬：**(甲) 方法論貢獻不過期**——「把 robust decision making / adversary-over-human 的成熟推理範式，引進一個被『不做真人』逼到需要它的領域」，這種貢獻不隨生成器版本歸零，通過四代歷史循環檢驗；**(乙) 錨點無前作**——shift-aware selective-prediction ADD benchmark 收編 FADEL 後經復查仍無前作，density-vs-discriminative failure-mode 分辨與 confident-real 對抗軸是全新實證格。它是全場唯一把因變數朝「那個接電話的人」延伸、且不依賴未兌現長期賭注的方向——但**只有在人側宣稱嚴格退到 D 單調下界為主層、品質軸模擬降為輔助時它才誠實**（否則死在我自己 Round 2 對 E 下的「錨在錯軸」那一刀上）。方法論判例牆（L2D/認知模型/IMF/G3-S1）是它擋 reviewer 的盔甲，venue 走 INTERSPEECH/ICASSP 是它的生存策略。

**兩者關係**：我主張同實驗室分工共構——G3-B 是量測端（產出 γ 真實上界、unseen-channel 測試集），G3-A 是消費端（用 γ 當掃描界）。若只能選一，**史官投 G3-B**：因為它的 novelty 最不會過期、空白最乾淨、且是其他所有方向的地基，時間窗卻正在關閉——這是「現在不做、一年後就被 Delgado 團隊 scoop」的唯一一個方向。

---

## 附錄：本輪補充檢索來源

| 編號 | 主題 | 關鍵來源 |
|------|------|----------|
| G3-S1 | 把「攻擊者對人類決策模型的操縱」納入 adversary model 的先例 | arXiv 2509.21436（Human Factors Reshape Adversarial Analysis in Human-AI Decision-Making）、arXiv 2602.04003（Adversarial Explanation Attacks on Human Trust）、biorxiv 2020.03.15.992875（Adversarial manipulation of human decision-making） |
| G3-S2 | 語音社工的領域現實錨 | Mandiant M-Trends 2026：voice phishing 於 2026 超越 email 成為社工首要載體 |
| （查證債） | 年齡別聽力常模（F 委託，尚未落實） | 猜測為 ISO 7029 系年齡聽力常模，需後補查證方可引用 |

*Agent G，2026-07-14，Round 3 答辯。本輪我對六發指向 G2-A 的挑戰全部接受並升級（受騙率因變數改採 D 單調下界為主、`A_social(c)` 塞入社工、γ 進掃描維度、robust-decision 形式 + 判例牆雙層盔甲、素材換考卷並收窄 novelty、併入合流），對四發指向 G2-B 的建設全部吸收（C1 合流、詐騙素材灌 rig、對稱重放、通道矩陣）。史官紀律不變：連自己上一輪認證的空白都照樣推翻，也照樣把別人的修正令收下——只要它讓推論鏈更誠實。*
