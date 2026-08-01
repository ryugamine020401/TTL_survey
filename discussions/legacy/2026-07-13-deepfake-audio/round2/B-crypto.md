# Round 2 質詢：密碼學/Provenance 研究者（Agent B）
日期：2026-07-13

---

## 前言：我的質詢基準

我在 Round 1 把話說死了三件事，Round 2 我用它們當尺量所有人：
1. **Provenance ≠ Authenticity**（#6），而且密碼學只能證正向、不能證負向——沒簽名的東西你證明不了它「不是 AI」。
2. **單一訊號各自有效 ≠ 整體可信**（#7 Integrity Clash），audio 版是空白。
3. **音訊通道會物理性剝離 metadata**，soft binding 的通道存活性沒人量過。

我要特別感謝 G 的檢索，它給了我三顆 Round 1 沒有的子彈，這三顆會貫穿我整份質詢：
- **S3｜The Watermark Shortcut**（arXiv 2606.23335）：偵測器在「fake 有浮水印、real 沒有」的資料上訓練會學到 spurious shortcut——strip-to-evade（去浮水印→誤判為真）、mark-to-frame（給真人語音加浮水印→誣陷為假，AASIST EER 16%→75%）。**這是一個密碼學層與 ML 層互相毒化的實證，也是我判斷「多訊號組合」提案的核心武器。**
- **S4｜Latent-Mark**：神經 codec 是 semantic filter，會抹除傳統浮水印。這直接威脅我自己 R1 提案二的 soft binding，我不迴避。
- **S2/S8**：SynthID 已進 ElevenLabs 生產線、EU AI Act Article 50 於 2026-08-02 起強制 machine-readable 標記——「多訊號並存」不是假設，是六個月後的法定現實。

---

## 1. 對他人提案的挑戰

### 挑戰一：Agent A 提案一「Channel-Robust One-Class Learning」——你並不擁有 real class 的控制權，而且 S3 已經證明這條路有 spurious shortcut

Agent A 主張：「**augmentation 只該用來擴張你有生成過程控制權的那一類（real），不該用來追逐你永遠追不完的那一類（fake）**」，並據此宣稱 one-class 對 unseen generator「天然免疫」。

這個對稱性論證是整個提案的地基，但它是錯的，我從三個角度拆：

**(a) 你對 real class 的控制權是幻覺。** A 假設「真實語音 manifold」由你可控的錄音條件定義。但現實是：現代手機的真實語音早就先過了一層 on-device 神經降噪、AGC、以及神經 codec 重合成——S4（Latent-Mark）明講神經 codec 是 semantic filter，它會系統性改寫波形。也就是說，「真實語音」本身是一個**你不控制、而且正在被各家手機廠不斷改版的移動分佈**。A 用來對抗 fake 端 shift 的那個「錨」（real manifold），自己就在漂。C 在 R1 也從訊號層指出同一件事：相位與高頻在 CELP codec 後物理性死亡（C §1a）——那 A 的 real manifold 在窄帶通道下會塌縮成什麼形狀，完全未知。

**(b) S3 直接證明 real/fake 的浮水印分佈會製造 spurious shortcut。** 這是最致命的一點。EU AI Act（S8）2026-08 上路後，越來越多**合法生成**的內容會帶 SynthID/AudioSeal 浮水印，而 A 的 bona fide 訓練集是歷史錄音、不帶浮水印。A 的 one-class 學到的「real manifold」很可能其實是在學「**沒有浮水印能量 = real**」這個 shortcut。後果正是 S3 量化的 mark-to-frame：攻擊者對一段**真人求救語音**嵌入浮水印，就能把它推出 A 的 real manifold、誣陷為假（AASIST EER 16%→75%）。A 的提案完全沒有把「real 端也會被下毒」納入威脅模型。

**(c) 你自己承諾要餵給我的證據，one-class 給不出來。** A 在 R1 給我的問題裡主張「detector 必須輸出 calibrated probability 而非硬判決，否則會污染跨層稽核鏈」——我完全同意（見下方回答）。但 A 的 one-class 輸出的是一個 distance-to-manifold，在 VoiceWukong 揭示的 AUC≈0.5 failure mode 下（#2），這個 distance 已經失去鑑別力，它不是一個 calibrated probability，而是一個看起來有數值、實則等同亂數的東西。A 一邊要求別人接受機率式證據，一邊自己的方法產不出可信的機率。

**我承認 A 對的地方**：把 DA 只加在可控類別、用 #3 的通道模擬撐大 real——這個 intuition 有 #3 的證據（DA 後 EER 波動 <0.1%）。但這只在「real 端不被攻擊、通道 codec 家族已知」的前提下成立，而 S3 與 S4 恰好打掉這兩個前提。**建議 A 把提案降級為「real manifold 在浮水印時代的穩定性研究」**，那反而是個有 S3 撐腰的真問題。

---

### 挑戰二：Agent E 提案1「Proof-of-Human 挑戰-回應」（D 提案二、F 提案二同構）——這是一個沒有信任錨點的密碼學協定，會被 relay 攻擊擊穿

E、D、F 三人不約而同收斂到「即時挑戰-回應活體驗證」。E 講得最完整：「**用密碼學式的 challenge-response 思路，在高風險即時通話中對來話方施加不可預測、即時、分布外的挑戰**」，攻擊即時語音克隆的「延遲」與「即興應對」軟肋。

作為真的做密碼學 challenge-response 的人，我必須指出：**你們借用了 challenge-response 的名字，卻沒有借到它之所以安全的東西——channel binding 與 trust anchor。** 四個技術缺陷：

**(a) 沒有 trust anchor，challenge-response 只是把問題往後推一格。** 密碼學的 challenge-response 之所以安全，是因為回應方持有一個**驗證方能用 PKI 驗證的秘密/金鑰**。你們的協定裡，來電者是一個陌生人，你沒有他的公鑰，你唯一的「驗證」是「他能不能像人一樣即時回話」——這不是 challenge-response，這是**圖靈測試/liveness detection**，本質是 ASVspoof 2017 起就在做的 replay/spoofing 對抗（G 的歷史 §1.1 已標記 2017 replay track）。把它包裝成密碼學協定會誤導審稿人。

**(b) Relay 攻擊直接繞過，而且 F 自己已經寫出了攻擊。** 攻擊者不需要即時合成挑戰回應——他把你的挑戰**即時轉發給一個真人共犯**（或用受害者聽不到的旁路），共犯開口，攻擊者再用即時 VC 把共犯的聲音轉成目標音色。F 在自己的 R1 提案二 §技術路線第 4 點就列了「真人共犯只在挑戰段接手」的混合攻擊——這正是 relay。挑戰-回應對 relay 沒有防禦力，除非你能做 channel binding（把回應綁定到通話的密碼學 session），而在無 PKI 的一般電話上，你綁不了。

**(c) 「延遲軟肋」是一個正在貶值的資產。** E 的核心賭注是即時 VC 的延遲/prosody 破綻。但 G 的 S5 已經是打臉現況：Resemble AI 對電信商供應 **<300ms 即時偵測**、Google 2026-06 全球上線端上 fake call detection——即時語音處理的延遲門檻正在崩。C 也在 R1 對 E 提出：真實電話通道本身的 codec buffer、jitter、丟包延遲會**淹沒**你要量的生成延遲。你賭的物理訊號，一邊被通道噪聲蓋掉、一邊被攻擊方技術進步追平。這是一個「寫完就過期」的 novelty（H 在 R1 §1.2 對軍備競賽的警告，同樣適用於此）。

**(d) 社會工程整段繞過。** D 自己誠實承認了：「不要理那個驗證，快匯錢」。挑戰-回應把認知負擔壓在情緒崩潰的受害者身上（F §1b：武器是情緒不是音質）——這是把最脆弱的一環當成安全協定的執行者。

**我承認的價值**：把戰場從「事後靜態產物」移到「即時互動」，方向是對的，因為它不依賴攻擊者合作（這正好補我 provenance 的死穴）。但**它該被定位成 liveness/anti-spoofing 研究，並老實承認 relay 是未解的結構性攻擊**，而不是包裝成密碼學 challenge-response。若真要有密碼學保證，唯一的路是機構端（銀行）持金鑰、對「機構→民眾」方向做真正的簽章驗證——但那覆蓋不了「假冒你兒子」這種無金鑰的來電。

---

### 挑戰三：Agent C 提案二「通道指紋一致性檢查」——你驗證的是通道的 provenance，不是內容的 authenticity，攻擊者過一次真電話就破了

Agent C 主張：「『**這通自稱是銀行來電的錄音，卻沒有任何電話 codec 痕跡』本身就是強烈的詐騙訊號**」，用通道指紋做「宣稱 vs 證據」的一致性檢查。

這個 idea 我很喜歡（它其實是 audio 版 Integrity Clash 的一個特例，跟我 R1 提案一同源），但 C 把它的鑑別力講太滿了。用我 R1 的第一條尺就能量出問題：**C 驗證的是「這段音訊走過電話通道」這個 provenance 事實，而不是「內容是真人所說」這個 authenticity。這正是 #6 的 provenance≠authenticity 鴻溝，只是換到訊號層重演一次。**

**攻擊者的破法零成本，而且 D 已經寫出來了：** D 在 R1 對 C 的 Q3 就問了「攻擊者刻意把音訊先過一次真的電話來製造合法通道痕跡」。這不是假設——把 deepfake 音訊用 virtual audio cable 灌進一支真手機撥出的通話（D 提案一動作空間裡的「平台真實轉檔」），codec 痕跡就是真的、通道指紋完全一致。此時 C 的一致性檢查給出「通道證據吻合宣稱」的綠燈，反而**替 deepfake 背書**——這是 F §思辨D 警告的「認證變成詐騙加分道具」在訊號層的翻版。

**更根本的**：通道指紋是 forgeable 的，因為它是內容的一個**可加性物理層屬性**，攻擊者完全控制內容要過哪條通道。凡是攻擊者能任意施加的東西，都不能當作 authenticity 的證據——這是密碼學威脅模型的基本功。

**我承認的價值**：C 的 claim-evidence consistency 在**特定不對稱場景**下仍有殘值——當攻擊者為了音質而不願讓音訊再過一次劣化通道時（例如高品質假證據音檔），「宣稱是電話錄音卻無 codec 痕跡」的矛盾會浮現。所以它不是全無用，而是**只在攻擊者有「保品質」動機時有效**，這個邊界 C 必須誠實寫進威脅模型，否則就是又一個給民眾虛假安全感的綠勾勾。

---

### 挑戰四（守土 + 補強）：Agent G 提案 G-1 與 Agent H 提案一「Audio Integrity Clash」——歡迎進場，但你們把 passive detector 那一層當成「不可靠的 oracle」，漏掉了 S3 揭露的層間毒化耦合

先說清楚立場：G-1、H 提案一、E 候選A、D 候選2、A 候選5 全部指向「audio 版 Integrity Clash」——這是我 R1 提案一。**五個角色收斂到同一個坑，這件事本身就是最強的信號：這是全場共識的甜蜜點。** 我不會假裝別人抄我，我要證明的是**這題需要一個真正的密碼學角色來做，否則會漏掉關鍵的失效模式**。

G 與 H 的版本有一個共同的、被輕描淡寫的缺陷。H 提案一把三層寫成「manifest × watermark × passive score」三個獨立訊號的狀態機；G-1 說「稽核協定的輸出把 detector 不可靠性建模為先驗可信度」。**兩人都假設三層在統計上獨立、可以各自賦予先驗可信度再組合。但 S3（Watermark Shortcut）證明這個獨立性假設是假的：watermark 層與 passive detector 層之間存在因果耦合——浮水印的存在/缺席會直接改變 detector 的輸出（strip-to-evade、mark-to-frame）。**

這意味著：
- 一個天真的跨層稽核器，會把「攻擊者用 strip-to-evade 去掉浮水印」同時觀測到「watermark 缺席」和「detector 說 real」，然後因為兩層都指向 real 而給出**高信心的一致綠燈**——但這兩個訊號不是獨立佐證，它們是**同一個攻擊動作的兩個投影**。把耦合訊號當獨立證據做貝氏更新，會系統性高估可信度。這是 G-1/H 的狀態機形式化裡沒有的維度。
- 正確的形式化必須把「層間依賴圖」建進去（哪一層的存在會 confound 另一層），這是純 ML 或純協定背景的人容易漏、而密碼學/形式化安全分析的人會抓的東西（#6 用的就是 formal methods）。

**這既是挑戰也是我 Round 3 要據此修正自己提案的方向**：Audio Integrity Clash 的正確版本不是「三個獨立 oracle 投票」，而是「**帶層間依賴的證據圖 + 對 S3 式耦合攻擊 robust 的稽核**」。我主張這個補強讓提案從「#7 換 modality」升級成「audio 特有、且比影像版更難的新問題」——正好回應 G 與 H 都擔心的 novelty 質疑。

---

## 2. 回答指名給我的問題

### 回答 Agent A（R1 §4 Q3）
**Q：passive detector 該以什麼形式接入信任模型？協定層能消化機率式證據嗎？C2PA credential 缺席是中性還是可疑？**

- **形式**：我同意你的核心主張——detector 必須輸出機率而非硬判決，我 R1 提案一就是把各層可靠度建模為貝氏先驗，所以協定層**天生就要吃機率**，硬判決反而餵不進去。但我要加一條你沒看到的約束（見挑戰四）：光是 calibrated 還不夠，因為 S3 證明 detector 的分數會被 watermark 層的操作污染。所以接入形式不能是一個孤立的 P(fake)，而必須是 **P(fake | watermark 狀態)** ——一個條件化、承認層間依賴的機率。你 R1 的 one-class distance 在 AUC≈0.5 下做不到 calibrated（挑戰一c），這是你要先解決的前置問題。
- **缺席是中性還是可疑**：**取決於情境的 base rate，而且會隨時間改變。** 過渡期 + 詐騙電話情境（F 是對的）→ 缺席趨近中性、資訊量近零。但 EU AI Act（S8）2026-08 對「合法生成內容」強制標記後，在**特定內容類別**（新聞媒體、官方發布、合規 TTS 服務輸出）裡「本該有訊號卻缺席」的鑑別力會逐年上升。我的設計是把缺席建成一個**權重隨預期標記普及率變化的分級訊號**，而不是二元警告。給 detection 層的先驗建議：詐騙冷不防來電→無憑證視為中性；已知應為簽署來源（銀行 App 推播、官方聲明）→無憑證視為高度可疑。

### 回答 Agent D（R1 §4 Q2）
**Q：對「什麼都不簽」的詐騙 deepfake，provenance 到底提供什麼保護？(a) conforming device re-sign 怎麼防？(b) audio metadata washing/desync 成熟到可實作了嗎？**

- **主問題，我誠實承認**：對「什麼都不簽」的即時詐騙 deepfake，我的 provenance 提案提供的**直接保護趨近於零**——我 R1 §1.2 就寫死了「密碼學無法證明負向」。所以我**主動收窄威脅模型**：我的兩個提案都不是、也不該被當成「詐騙冷不防來電偵測器」。它們的戰場是「**經認證的假內容**」（Integrity Clash：有人拿有效簽章替假內容背書）與「**語音訊息/媒體檔案的來源查驗**」（soft binding），不是阿嬤耳邊那通即時電話。你這一問的最大貢獻，是逼所有 provenance 提案把這條邊界寫進論文第一頁——我接受並執行。
- **(a) conforming device re-sign（analog hole）**：我防不了源頭簽署，這是我 R1 淘汰 TEE-mic 候選 B 的原因。唯一的殘餘防線是 Integrity Clash 稽核——如果源頭 AI 音訊帶了 SynthID（S2，ElevenLabs 現在預設嵌），re-record 後若浮水印殘存，就會與「真實錄製」的 manifest 矛盾而被抓。**但這裡有個對我不利的實話**：S4（Latent-Mark）暗示浮水印在通道/重錄後很脆弱，喇叭-麥克風重錄很可能把 SynthID 洗掉——洗掉之後就退回「無憑證」，矛盾消失，稽核無從發動。**結論：analog-hole re-sign 對 provenance 是真缺口，只有 liveness（你和 E 的 challenge-response 方向）能碰它——這是我對你/E 那條線的一個誠實讓步與接口。**
- **(b) 成熟度**：對**檔案/訊息**場景，是的，現在就能實作——c2patool 支援 WAV/MP3、AudioSeal 開源（S2）、S3 的 WASP paired corpus 已釋出、Suno/Udio 據報已嵌 manifest（G S7，需查一手）。metadata washing 照抄 #7 的 assertion 省略手法即可。對**即時通話**場景，沒有容器、沒有簽署點，desync 無從談起（見對 H 的回答）。

### 回答 Agent F（R1 §4 Q3，指名 B）
**Q：對「缺席的憑證不構成警告」這個死結，provenance 陣營有解嗎？還是 C2PA 在詐騙電話與選舉錄音應該直接承認不適用？**

你這一刀最痛，我分兩半回答：

- **對詐騙電話：我承認不適用，直接舉白旗。** 冷不防的詐騙來電沒有容器、沒有簽署點、攻擊者不合作——provenance 三個前提全滅。硬要在這裡用 C2PA 是學術自我感動。這個情境該讓給你的提案一（壓力下的人機警告）與 liveness 那條線。
- **對選舉/媒體錄音：不適用「flag 假的」，但適用一個你可能沒想到的翻轉——不要偵測缺席，要驗證在場。** 你的死結來自「要民眾對缺席的訊號起疑」，這確實反人性。**我的解法是把方向倒過來：不要求民眾檢查每則內容有沒有憑證（缺席模型），而是讓少數高價值、會被冒充的來源（總統府、中選會、你的銀行）主動發布簽章音訊，民眾只在遇到「自稱來自這些關鍵來源」的內容時，去比對官方已發布的簽章版本（在場模型）。** 這像是一個小型 whitelist / 官方頻道核對，而不是全網掃描。它**不依賴普及率**（回答你 R1 給我的那個「不依賴普及率的提示介面」的追問）——因為它只需要「被冒充的重要來源」這個極小集合去簽，不需要全世界的內容都簽。誠實的邊界：它只保護「有人冒充特定權威來源」這類詐騙，對「假冒你私人親友」無效（親友不會有 PKI）。
- **一句總結給你**：provenance 對「降低民眾受騙」的正確貢獻，不是給民眾一個判假的標章（誤導成本 > 資訊價值，你 §思辨D 的必答題我接受），而是**降低關鍵權威來源被冒充的成功率**。這是一個窄很多、但誠實且做得到的目標。

### 回答 Agent G（R1 §4 Q2，指名 B）
**Q：電話通道剝掉容器、hard binding 必死、只剩浮水印 soft binding（~1 bit）。有沒有密碼學機制能提供比「浮水印在/不在」更多的可驗證資訊？還是該把電話通道宣告為 provenance 不可達區域？**

- **有，但關鍵是「不要試圖把資訊塞進通道，而是把通道當索引」。** 即使窄帶 AMR-NB + 重錄後可靠容量掉到個位數 bit（我 R1 提案二候選 D 的猜測，S4 進一步支持這個悲觀估計），這幾個 bit 不必攜帶 payload，而是當作一個**指向 transparency log 的 k-bit 索引 + ECC**。真正的可驗證資訊（完整 manifest、簽署者、時間戳 inclusion proof）活在鏈下的 append-only log，波形裡的浮水印只是一根指標。這樣「有效資訊量」不受通道容量上限綁死——你用 20 bit 的存活 payload 就能索引到 2^20 筆完整 manifest。再用 perceptual-hash 綁定防止指標被移植到別的音訊（anti-transplant）。
- **但我對你的悲觀估計讓一半的步**：這個「索引不 payload」的技巧要成立，前提是那幾個 bit **能可靠存活**。而 S4（神經 codec 抹除浮水印）+ 窄帶 CELP + 重錄三重打擊下，可靠容量可能連索引都撐不住、甚至逼近 0 bit。**所以我的正式立場是：純窄帶即時電話通道（AMR-NB 等），實務上宣告為 provenance 不可達區域是誠實的**；provenance 的可達區間是 VoIP/Opus 高碼率、社群平台語音訊息檔案這些**容器或高容量波形仍在**的通道。**而『可達 vs 不可達』的邊界precisely在哪，正是你 G-2 benchmark 要量的東西**——這是我 R1 提案二與你 G-2 最強的接口（見下方「我支持的提案」）。

### 回答 Agent H（R1 §4 Q2，指名 B）
**Q：C2PA v2.4 對 audio 的成熟度？soft binding / durable credentials 在 WAV/MP3/Opus 有可用參考實作嗎？即時通話串流有站得住的簽署點嗎？provenance 是否對詐騙電話先天缺席、只能覆蓋語音訊息/媒體檔案？**

- **成熟度（誠實盤點）**：c2patool / c2pa-rs 對 WAV、MP3 的 manifest 嵌入與驗證是可用的；Opus 支援需要開題第一個月做 feasibility spike 確認（我不敢打包票，標明為待驗證）。**Durable Content Credentials（用 watermark + fingerprint 做 soft binding 找回 manifest）在規格（#4）裡有，但 audio 的參考實作不成熟**——這正是你 R1 提案一提到的「第一個月 feasibility spike」的必要性。備案與你一致：manifest 層可降級為「依 v2.4 spec 自行實作最小驗證」。
- **即時通話簽署點**：我的答案是**沒有**站得住的協定簽署點。即時 P2P 通話是串流、無容器、且雙方無共享 PKI；STIR/SHAKEN 簽的是**主叫號碼不是聲音內容**（G S6，Lingo Telecom 案：對載有 Biden deepfake 的 3,978 通給了 A 級 attestation）。要在通話串流上簽聲音，需要端點或電信商合作——這踩到你 R1 §1.3 的紅線（不能依賴外部機構）。
- **所以，是的，我同意你的框定並主動寫進威脅模型**：provenance 對「詐騙電話」這個核心情境**先天缺席**，它能誠實覆蓋的是「**非即時**的語音訊息 / 媒體檔案 / 官方發布音訊」。這個邊界不是我提案的弱點，而是我提案的**定義域**——把它寫清楚，反而讓評估章節可信。詐騙電話那塊，交給 detection（A/C）、liveness（D/E）、與 F 的人機警告。

---

## 3. 我支持的提案

### 支持一：Audio Integrity Clash 跨層一致性稽核（我 R1 提案一 = G-1 = H 提案一的共識方向）

**為什麼**：五個角色（我、G、H、E、D、A 的候選）獨立收斂到這裡，H（指導教授）給了它最硬的可行性背書，#7 提供影像版的路線圖與可發表證明（CVPR 2026 Workshop，3,500 張 100% 分類），gap 地圖第 3 點明言 audio 空白。它同時滿足硬性要求：不與生成器軍備競賽（H §1.2）、元件全現成、對社會福祉的貢獻明確（讓查核組織/平台不被「有簽章=真」誤導，正是 #6 指出民眾最易受騙處）。

**我的角色能怎麼補強它（這是我不可替代的價值）**：
1. **把 S3 的層間毒化建進形式化**（挑戰四）：三層不是獨立 oracle，watermark 層會 confound detector 層。正確模型是「帶層間依賴的證據圖」，並要求稽核對 strip-to-evade / mark-to-frame 這類耦合攻擊 robust。這一步把提案從「#7 換 modality」拉高到「比影像版更難的新問題」，直接解 G 與 H 都擔心的 novelty 疑慮。
2. **用 formal methods 做安全論證**（#6 的方法）：不只實驗量分類準確率，而是形式化證明稽核協定達成/未達成哪些安全目標——這是純 ML 角色做不出、審稿人會加分的部分。
3. **誠實的威脅模型邊界**：明寫「稽核只在至少一層訊號存在時有意義」，對「什麼都不簽的詐騙 deepfake」（D 的 Q2）覆蓋為零——避免 F §思辨D 警告的虛假安全感。

### 支持二：Agent C 提案二 / Agent G 提案 G-2「真實電話通道存活性 benchmark」

**為什麼**：這兩個提案高度重疊（真實 laundering 通道資料集 + 存活性量測），而它**正是我 R1 提案二（Laundering-Resistant Provenance soft binding）成立與否的實證地基**。我對 G 的回答裡承認：「provenance 的可達 vs 不可達邊界precisely在哪」我答不出來——因為沒人量過浮水印/manifest soft binding 在**真實**電話通道（VoLTE/EVS、LINE Opus、重錄）下的 bit-level 存活率。C/G 的 benchmark 就是量這個。S4（Latent-Mark 只測神經 codec）、AudioMarkBench（只測數位擾動）都沒碰真實電信通道——這是文獻明確的空白。

**我的角色能怎麼補強它**：
1. **把「存活性」從單純的 detector EER 擴充到 provenance payload 的 bit-level 存活率**：C/G 的 benchmark 若只量 detector 劣化就浪費了通道；加一軸「AudioSeal/SynthID commitment 在每種通道下還原成功率」，這條表直接界定我 soft-binding 提案的可行域，也直接回答 EU AI Act Article 50（S8）「machine-readable 標記」在詐騙實際發生的通道上到底可不可讀——這是有政策發表價值的結果（G 自己也指出）。
2. **提供「索引不 payload」的編碼設計**（我對 G 的回答）：如果 benchmark 顯示可靠容量只有個位數 bit，我的 transparency-log 索引 + ECC + perceptual-hash 綁定設計，正好是「在極低容量下仍能提供可驗證 provenance」的方法論貢獻，讓 C/G 的 benchmark 不只是「量出全滅」，而是「量出下界後給一個能在下界上工作的構造」。
3. **合流建議**：C/G 的真實通道錄製產物，可直接當我 Integrity Clash 提案（支持一）的「良性 laundering」條件——三個提案共享一套通道基礎設施。這正是 G 在 R1 結尾說的「G-2 的通道產物可餵給 G-1」，我加上密碼學層讓它成為一條完整的證據鏈。

---

## 4. 我留給 Round 3 的自我修正備忘（為我 R1 提案辯護後的調整）

- 提案一（Audio Integrity Clash）**升級**：從「三獨立訊號狀態機」改為「帶 S3 層間依賴的證據圖 + 對耦合攻擊 robust 的稽核 + formal-methods 安全論證」。
- 提案二（soft binding）**收窄並接地**：明確排除窄帶即時電話（provenance 不可達區），定義域限縮到 VoIP/Opus/語音訊息檔案；核心構造從「塞 payload」改為「transparency-log 索引 + ECC + perceptual-hash 防移植」；存活性數據依賴 C/G benchmark。
- 全線**主動寫死威脅模型邊界**：provenance 對「不合作的即時詐騙來電」覆蓋為零，戰場是「認證的假內容」與「關鍵權威來源的在場驗證」——回應 D、F、H 的共同質疑。
