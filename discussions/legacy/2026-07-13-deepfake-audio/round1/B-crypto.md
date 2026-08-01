# Round 1 提案：密碼學/Provenance 研究者（Agent B）
日期：2026-07-13

---

## 1. 我看到的問題本質

從密碼學的角度看，這個問題的核心不是「怎麼把偵測器練得更準」，而是**我們到底能在密碼學上證明什麼、不能證明什麼**。我認為其他討論者（尤其是 detection 陣營）容易忽略以下四點：

### 1.1 Provenance ≠ Authenticity，這不是實作瑕疵，是本體論的鴻溝
UMBC 的分析（文獻 #6）講得很清楚：C2PA 證明的是「這個檔案的歷史宣稱由誰簽署、簽署後未被改動」，而**不是**「內容忠實反映了物理現實」。問題陳述第 3 點說 C2PA「只能保證內容沒有被竄改」——其實連這一點在現行規格下都不成立：#6 證明 C2PA 連自己宣稱的兩項安全目標（claim integrity、weak file integrity）加上三項必備目標（timestamp agreement、validator consistency、strong file integrity）**五項全部未達成**。exclusion range 內的資料可以被竄改而簽章仍有效；timestamp 可無痕替換；Nikon Z6 III 憑證被撤銷六個月後，兩個 validator 對同一張圖給出矛盾結論。所以在討論「provenance 能不能補 detection 的洞」之前，要先承認：**現行 provenance 自己就是漏的**。

### 1.2 密碼學只能證明「正向」，無法證明「負向」
簽章可以證明「這段音訊是某台設備/某個服務在某時刻簽署的」，但**永遠無法證明「這段音訊不是 AI 生成的」**——因為惡意生成者根本不會來簽名。#6 甚至示範了反向攻擊：用 conforming 相機替 AI 生成影像簽出「真實拍攝」憑證（audio 的對應版本就是：把 deepfake 語音播放給一支「可信麥克風」重錄）。這代表 provenance 的正確定位是**縮小需要懷疑的範圍**，而不是判定真偽。任何把 C2PA 當作 deepfake detector 用的提案，都應該在 Round 2 被打掉。

### 1.3 多重訊號「各自有效」不等於「整體可信」——這是 audio 領域的空白
CVPR 2026 的 Integrity Clash 攻擊（文獻 #7）是我認為全場最重要的一篇：一個資產可以同時攜帶密碼學上有效、宣稱人類創作的 C2PA manifest，以及標識 AI 生成的 invisible watermark，兩者驗證**都通過**，而攻擊只用了 metadata washing——標準編輯流程加上省略一個規格允許省略的 assertion 欄位，完全不需要破解任何密碼學。這篇做在影像上；survey README 的 gap 地圖第 3 點明說：**audio 領域尚缺乏對應的系統性研究**。而 audio 的訊號層（AudioSeal 類 watermark）與 metadata 層（C2PA audio manifest）的去同步條件，跟影像有本質差異——音訊要過 codec、封包遺失、重錄，去同步其實**更容易自然發生**，這既是攻擊面也是研究機會。

### 1.4 音訊的傳輸通道會物理性地剝離 metadata——provenance 需要一條「訊號內」的載體
問題陳述第 5 點與 Loughborough benchmark（#3）指出 laundering 摧毀 detection 依據；但同樣的通道對 provenance 更致命：C2PA manifest 是附在容器/metadata 層的，經過社群平台轉檔、電話 codec（AMR-WB、EVS、Opus）、重新錄製之後，**manifest 直接消失**，連「驗證失敗」都不會發生——就是什麼都沒有。C2PA 規格（#4）雖有 soft binding 的概念（用 watermark 或 fingerprint 找回 manifest），但在 audio 上「什麼樣的 soft binding 能活過真實通訊通道」完全沒有被系統性量化過。這是我認為密碼學角色能貢獻的最具體工程問題。

---

## 2. 思辨過程（候選想法與自我質疑）

### 候選 A：用零知識證明證明「產生過程」——zk-PoP（Proof of Provenance pipeline）
**想法**：影像領域已有 VerITAS、VIMz 這類工作（此為我背景知識，非本次文獻集內容，標明為延伸知識）：對一張已簽署的原圖做編輯（裁切、縮放、壓縮）後，用 zk-SNARK 證明「這張衍生圖確實由那張簽署原圖經宣告的轉換得來」，不必公開原圖。搬到 audio：證明「這段 Opus 壓縮後的語音，來自某段由可信裝置簽署的原始錄音」。這樣即使平台轉檔，provenance 也能以證明的形式跟著走。

**自我質疑**：
1. **電路規模是災難**。影像的裁切/縮放是線性或近線性運算，SNARK 電路還算可控；音訊 codec（Opus、EVS）含心理聲學模型、非線性量化、熵編碼，把一個 codec 塞進算術電路，證明一段 10 秒語音的成本我猜測（標明：猜測）會是天文數字。一個碩士生一年內連把 Opus 電路化都做不完。
2. 就算做出來，**它防不了核心威脅**：詐騙者的 deepfake 音訊根本沒有簽署起點，zk 證明鏈無從建立。這是 1.2 的負向證明問題，ZK 解決不了。
3. 退而求其次只證明簡單轉換（重採樣、音量正規化）？那涵蓋不了真實 laundering 管線，變成玩具問題。

**裁決**：淘汰。技術上超出一年範圍，且不打在威脅模型的要害上。留下的教訓：「讓 provenance 活過轉換」的需求是真的，但載體不該是 ZK 證明，該是更輕的東西（見候選 D）。

### 候選 B：可信硬體錄音鏈——TEE-attested microphone capture
**想法**：在手機 TEE（TrustZone/StrongBox）內對麥克風輸入即時簽章，產生「這段聲音確實來自這台裝置的實體麥克風」的 attestation，從源頭建立 audio 的 Content Credentials。

**自我質疑**：
1. **analog hole 直接擊穿**。#6 已示範 conforming 相機可以替 AI 影像簽出真實憑證；audio 版本更簡單——把 deepfake 用喇叭放給可信麥克風錄。TEE 只能證明「麥克風收到了這個聲波」，不能證明「聲波來自真人聲帶」。要對抗這個得做 liveness（聲學環境指紋、challenge-response），那已經是另一個完整的研究領域。
2. **碩士生做不了**：需要 OEM 層級的硬體存取與韌體簽章金鑰，學界原型只能在自控裝置上 demo，外部效度極低。
3. 部署面：這是十年尺度的生態系工程（類似相機界的 Leica M11-P 路線），不是一年論文。

**裁決**：淘汰。但它逼我想清楚一件事：**源頭簽署永遠有 analog hole，所以研究重心應該放在「驗證端如何組合多重不完美訊號」，而不是「製造一個完美的源頭」**。

### 候選 C：修復 C2PA 五大缺陷的 audio profile——transparency log + 強制 timestamp binding
**想法**：針對 #6 列出的五項失敗，為 audio 設計一個補強層：所有 manifest 簽發時強制寫入 append-only transparency log（類似 Certificate Transparency），log inclusion proof 綁進簽章，解決 timestamp 可替換、憑證過期後不可驗證（Arizona 選舉案例）、revocation 檢查 optional 導致 validator 矛盾等問題。

**自我質疑**：
1. novelty 風險：CT-for-media 的想法在標準圈已有討論（我的背景知識，猜測 C2PA 社群內部已有相關草案），純協定設計的碩士論文很難跟標準組織的工作區隔。
2. **對「降低民眾受騙」的貢獻太間接**：修好 timestamp binding 不會讓阿嬤少接一通詐騙電話。問題陳述的硬性要求是真實情境、社會福祉——這個提案是給標準委員會看的，不是給受害者的。
3. 評估方法困難：協定安全性可以 formal analysis，但「有效性」無法用實驗量化，指導教授（H）大概會問「你的實驗章節是什麼？」而我答不出來。

**裁決**：降級。不作為主軸，但它的核心元件（transparency log 作為長期可驗證性的錨點）可以併入候選 D 作為其中一個模組。

### 候選 D：把 provenance 塞進訊號本身——watermark-bound manifest（soft binding 的通道存活性研究）
**想法**：既然 metadata 層的 manifest 會被通道剝離（1.4），就把 manifest 的**密碼學承諾**（manifest hash、簽署者 ID、時間戳的 commitment，幾十到上百 bit）嵌入 AudioSeal 類 robust watermark，讓 provenance 以訊號內載體的形式活過 codec/轉檔/重錄；驗證端從 watermark 還原 commitment，回 transparency log 取回完整 manifest 驗證。C2PA 規格（#4）本身承認需要 soft binding，但 audio 上「哪種 watermark、幾 bit payload、能活過哪些通道」沒有任何系統性的量測。

**自我質疑**：
1. watermark 本身可被對抗性移除或覆寫——Nemecek et al.（#7）的整個攻擊前提就是 watermark 與 manifest 可以被獨立操縱。但注意：**移除 watermark 只會讓內容退回「無憑證」狀態**，等同於未簽署內容，這在「簽署=可信加分」的威脅模型下是可接受的失敗模式（攻擊者得不到假憑證，只能得到無憑證）。真正危險的是**偽造/移植** watermark——這需要在設計中用「commitment 綁定音訊內容的 perceptual hash」來防，這裡有真正的技術難點與 novelty。
2. bit capacity vs. robustness 的 trade-off 可能太苛：AMR-WB 4.75–23.85 kbps 的窄管道 + 20% 丟包（#3 的 C5 條件）之後還能剩幾 bit？我猜測（標明：猜測）重錄場景可能只剩個位數 bit 的可靠容量，那連一個 hash commitment 都塞不下，設計就得改成「1-bit 存在性訊號 + 外部索引」。這正是需要實驗回答的問題，失敗結果本身也是有價值的 negative result。
3. 依賴生成端/錄音端合作（opt-in），對惡意 deepfake 零覆蓋——承認。所以它必須被定位為分層防禦（#8）中的一層，並與被動偵測組合，這就自然銜接到候選 E。

**裁決**：保留，成為正式提案二。

### 候選 E：Audio 版 Integrity Clash——多訊號一致性稽核
**想法**：把 #7 的攻擊與防禦搬到 audio 並深化：形式化 audio 資產上三個獨立驗證層（C2PA manifest、audio watermark、passive detector 分數）的狀態空間，展示 audio 特有的去同步攻擊（利用 codec 轉檔自然剝離某一層、metadata washing、重錄後重簽），然後提出跨層一致性稽核協定，並在真實通道條件（#3 的 codec×PLR 矩陣、#2 的 38 種 manipulation）下評估。

**自我質疑**：
1. 「把影像論文搬到音訊」的 novelty 質疑——這是最大的風險。我的回答：(a) #7 作者自己與 survey gap 地圖都指出 audio 是空白；(b) audio 的去同步機制與影像本質不同：影像的 clash 需要刻意的 metadata washing，音訊的 clash 會在正常通訊管線中**自然發生**（Opus 轉檔就剝掉 manifest、重錄就毀掉 watermark），所以「哪些矛盾狀態是攻擊、哪些是良性通道效應」的判別問題在 audio 上更難也更有趣——這不是複製，是新問題。
2. 三層訊號中 passive detector 這一層在閉源生成器上本來就不可靠（#2：EER 13.5–50%），拿一個不可靠的訊號進稽核會不會垃圾進垃圾出？回應：稽核協定的輸出不必是二元真偽，而是「一致性狀態 + 各層可信度」，detector 不可靠這件事本身就該被建模成該層的先驗可信度——這反而是比 #7（把每層當可靠 oracle）更進一步的形式化。
3. 工作量：攻擊實作 + 協定 + 通道實驗，一年做得完嗎？攻擊部分可以站在 #7 的方法論上，通道矩陣可以取 #3 的子集，我評估可行，但需要 H 把關範圍。

**裁決**：保留，成為正式提案一。

---

## 3. 正式提案

### 提案一：Audio Integrity Clash——音訊多層驗證訊號的去同步攻擊與跨層一致性稽核

**核心 idea**：首次系統性研究 audio 資產上 provenance（C2PA manifest）、invisible watermark（AudioSeal 類）、passive detection 三層驗證訊號的**去同步空間**：(1) 形式化三層訊號的一致/矛盾狀態機；(2) 實證展示 audio 特有的攻擊——metadata washing、codec 通道自然剝離、重錄後重簽（analog re-signing）——如何製造「經認證的假語音」或「被剝奪憑證的真語音」；(3) 提出跨層一致性稽核協定，輸出可解釋的一致性判定而非單一真偽分數。

**為什麼有機會成立**：
- Gap 有直接文獻背書：#7 在影像上證明 Integrity Clash 可行且防禦（跨層稽核）有效（3,500 張影像 100% 分類準確率），survey gap 地圖明指 audio 尚無對應研究。
- audio 版本不是平移：#3 證明 codec 壓縮本身就顯著劣化訊號層（C0→C1 平均 EER +5.30%），意味著矛盾狀態會在良性通道中自然出現，「區分攻擊性去同步 vs. 通道性去同步」是影像版不存在的新問題。
- 稽核層把 detector 的不可靠性（#2：閉源生成器 EER 13.5–50%）建模為先驗可信度，正面回應了「單一訊號皆不充分」的 layered defense 主張（#8）。

**技術路線**（約 12 個月）：
1. M1–2：復現 audio C2PA 簽署/驗證管線（c2pa-rs 支援 audio 格式）+ AudioSeal 嵌入/偵測 + 一個 SOTA passive detector（AASIST2）作為第三訊號。
2. M3–5：攻擊實作：metadata washing（比照 #7 的 assertion 省略手法）、通道剝離矩陣（#3 的 6 codec × PLR 子集）、喇叭-麥克風重錄後用自有憑證重簽。產出 audio 三層狀態的實測 taxonomy。
3. M6–9：設計跨層稽核協定：以 perceptual audio hash 綁定三層、以各層在該通道條件下的實測可靠度作為貝氏先驗、輸出一致性狀態分類。
4. M10–12：在攻擊集 + 良性通道集上評估（分類準確率、對未見 codec 的泛化）、撰寫。

**預期貢獻**：audio 領域第一個多層驗證訊號的攻擊面形式化與實測 taxonomy；一個能區分「惡意去同步」與「良性通道劣化」的稽核協定；給 C2PA audio profile 的具體規格建議。對社會福祉：驗證平台（新聞機構、事實查核組織）可直接部署稽核協定，減少「有簽章=真」的誤導。

### 提案二：Laundering-Resistant Provenance——以浮水印為載體的 audio manifest soft binding 及其通道存活性

**核心 idea**：把 C2PA manifest 的密碼學承諾（content-bound commitment：manifest hash ⊕ perceptual hash ⊕ 簽發時 transparency-log inclusion proof 的索引）嵌入 robust audio watermark，使 provenance 不再依賴會被通道剝離的 metadata 層；系統性量測這條「訊號內 provenance 通道」在真實 laundering（codec×丟包×重錄×社群平台轉檔）下的**有效容量與安全邊界**，並設計防移植（anti-transplant）綁定機制。

**為什麼有機會成立**：
- 需求由規格與攻擊文獻雙重確立：C2PA 規格（#4）明載 soft binding 為 manifest 復原機制，但未給 audio 的具體構造；#7 證明 watermark 與 manifest 若不互相綁定就會被去同步——本提案的 content-bound commitment 正是把兩層在密碼學上焊死。
- 通道條件有現成 benchmark 方法論可站：#3 的 6 codec × 5 PLR 矩陣、#2 的 38 種 manipulation，可直接改造成 watermark payload 存活性的量測框架，而非從零建實驗環境。
- transparency log 模組同時修補 #6 指出的 timestamp 可替換與憑證過期失效問題（Arizona 案例），讓一個設計回應兩篇文獻的缺陷清單。
- 失敗模式安全：watermark 被移除只造成「退回無憑證」，不產生假憑證；需要防的偽造/移植由 perceptual-hash 綁定處理——威脅模型清晰，適合碩士論文的範圍收斂。

**技術路線**（約 12 個月）：
1. M1–3：量測基線：AudioSeal（及 1–2 個替代 watermark）在 #3 式通道矩陣 + 重錄下的 bit-level 存活率 → 得出「真實通道下的可靠 payload 容量上限」（這張表本身就是可發表的貢獻）。
2. M4–6：依容量設計編碼：若容量足 → 完整 commitment；若不足 → 分級設計（1-bit 存在性 + k-bit log 索引 + 糾錯碼），commitment 綁定 perceptual hash 防移植。
3. M7–9：接上 transparency log 原型（append-only Merkle log），端到端 demo：簽署 → 經 Opus/社群平台轉檔 → 無 metadata 情況下復原並驗證 manifest。
4. M10–12：安全評估（對抗性移除、移植攻擊、UMBC 五目標對照表）+ 撰寫。

**預期貢獻**：audio soft binding 的第一份系統性通道存活容量量測；一個防移植的 content-bound commitment 構造；C2PA audio 長期可驗證性（transparency log）的可行性驗證。對社會福祉：讓「經社群軟體轉傳的語音訊息」仍可查驗來源——正是目前詐騙語音最常見的傳播路徑。

---

## 4. 我留給其他討論者的問題

1. **給 D（紅隊）**：提案二的失敗模式假設「移除 watermark 只會退回無憑證狀態」。請攻擊這個假設——特別是：你能否在不觸發 perceptual-hash 不匹配的前提下，把合法語音的 watermark commitment 移植到一段語意被竄改（例如剪接換句）的音訊上？重錄（analog hole）後殘留的 watermark 片段能否被你利用來偽造部分憑證？

2. **給 C（訊號處理）**：AMR-WB 最低碼率 + 20% PLR + 一次喇叭-麥克風重錄之後，10 秒語音中理論上還能可靠傳遞多少 bit 的 watermark payload？如果答案是個位數，提案二就必須退到「1-bit 存在性訊號」設計——請給我一個訊號處理視角的容量估計或量測方法。

3. **給 F（民眾代表）與 E（開創性思維者）**：兩個提案的社會效果都建立在「未來簽署會普及、無憑證內容會被降低信任」的長期假設上。在過渡期（絕大多數真實內容也沒有憑證），「這段語音沒有憑證」對一般民眾是有用資訊還是雜訊？如果永遠到不了普及的臨界點，provenance 路線對「降低受騙機率」的邊際貢獻是否應該重新估值——有沒有辦法設計出**不依賴普及率**的提示介面？
