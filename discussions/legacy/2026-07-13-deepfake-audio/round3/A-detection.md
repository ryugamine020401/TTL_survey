# Round 3 答辯：Detection 研究者（Agent A）
日期：2026-07-13

---

## 0. 開場：先交 F 的必答題，再交代我的答辯總立場

F 在 Round 2 結尾要求每個人把「阿嬤那一行的判定」寫在答辯第一段。我照辦：

- **我的提案一（Channel-Robust One-Class，修正前）**：阿嬤情境判定「有條件」，且條件比我 Round 1 承認的更苛——需電信端/手機端替她部署、極端通道 FRR 必須壓到通訊錄聯絡人幾乎零誤傷，而且（接受 C 與 D 的攻擊後）在窄帶＋re-synthesis 的最惡劣鏈上，它的判別力有物理上限，**不棄權就是說謊**。
- **我的提案二（Selective Prediction，修正後與 H/F 合流）**：阿嬤情境判定「有條件、但條件可在一年內做掉」——棄權必須綁定風險語境門控＋一鍵回撥（F 的 2.4），部署形態必須是系統自動觸發或機構端（F 的 2.5），對抗評估必須以 max P(confident-real | fake) 為主軸（D 送我的那句話）。

總立場：Round 2 對我提案一的七路圍攻，**大部分是對的**。我不會為了保住提案編號而硬拗——VoiceWukong 教我們的第一課就是「防守方對自己的失效模式誠實，比多刷 2% EER 有價值」。以下逐條答辯，該認的認、該打的打，最後給出一個比我 Round 1 更強的合體版本。

---

## 1. 逐條答辯

### 1.1 針對提案一（Channel-Robust One-Class Learning）的挑戰

#### 挑戰 A1-①（B 挑戰一(a)）：「你對 real class 的控制權是幻覺——手機端神經降噪/AGC/神經 codec 讓 real manifold 自己在漂」

**裁決：接受並修正。**

B 說得對：我 Round 1 的措辭「augmentation 只該用來擴張你有生成過程控制權的那一類（real）」隱含了「real 的生成過程由我定義」這個過強假設。現代真實語音在抵達任何偵測器之前，已經過 on-device 神經降噪、AGC、甚至神經 codec 重合成（S4 Latent-Mark：神經 codec 是 semantic filter）——real 分佈確實在被各家手機廠持續改版。

但我要把這個修正精確化，而不是照單全收它的悲觀含義：**「real 分佈會漂」對所有 passive detection 方法一視同仁地成立**（supervised binary 也一樣要面對漂移後的 bona fide），它不是 one-class 的專屬死穴；它只是把我的「控制權」修正為「**採樣權**」——我不能定義 real 的生成過程，但我能持續、合法、零成本地採樣到最新的 real 分佈（任何人用當代手機錄音即得），而 fake 端我永遠採樣不全（閉源生成器、地下工具）。**這個不對稱性仍然成立，只是從「控制 vs 不可控」弱化為「可採樣 vs 不可採樣」**。修正後的版本：real class 的 DA 維度必須把「device processing chain」（各代手機的降噪/AGC/神經 codec）與傳輸通道並列納入，且 bona fide 訓練集需含近年真實裝置錄音而非只有錄音室語料。這是實驗設計的修正，不是路線的否定。

#### 挑戰 A1-②（B 挑戰一(b)）：「S3 Watermark Shortcut——EU AI Act 之後合法生成內容帶浮水印，你的 one-class 會學到『無浮水印能量 = real』的 shortcut，被 mark-to-frame 攻擊（真人語音蓋浮水印→誣陷為假，AASIST EER 16%→75%）」

**裁決：接受，這是 Round 2 對我最有價值的一擊，並給出具體修正。**

我 Round 1 完全沒把「real 端被下毒」納入威脅模型，B 抓得準。S3 的教訓在 ML 語言裡是：訓練分佈中 watermark 與 label 的 spurious correlation。而 spurious correlation 有標準解法——**把浮水印作為 nuisance variable 做增強去相關**：對 bona fide 訓練樣本以一定比例主動嵌入 AudioSeal/SynthID（工具全開源，S2），使「浮水印存在與否」在 real class 內部與標籤獨立；再以 mark-to-frame 式的對抗測試集（對真人語音蓋浮水印）驗證 FRR 不因浮水印而爆炸。這個「watermark-decorrelated training + mark-to-frame 壓力測試」本身就是一個 S3 之後沒人在 one-class 設定下做過的消融，我把它列為修正版的必做實驗。順帶回應 B 的「建議降級為 real manifold 在浮水印時代的穩定性研究」：我不接受全面降級，但接受把這個穩定性實驗**內建**為方法成立的前置條件。

#### 挑戰 A1-③（B 挑戰一(c)）：「你要求別人接受 calibrated probability，自己的 one-class distance 在 AUC≈0.5 failure mode 下只是看起來有數值的亂數」

**裁決：一半接受、一半反駁。**

接受的一半：distance 不是機率，接進任何稽核鏈或警告系統前必須過一層 post-hoc calibration（在 held-out、經通道 shift 的 bona fide 上做 density calibration / conformal 化）。這在我修正版裡是硬性步驟。

反駁的一半：B 引用的「AUC≈0.5 failure mode」是 #2 對 **supervised binary detector** 在 unseen generator 上的實測，**沒有任何證據顯示 one-class distance 在同一條件下也 AUC≈0.5**——把 supervised 的失效直接外推到 one-class，恰好犯了跟「把 #3 的樂觀外推到雙重未知」對稱的錯誤（C 打我的那一招，我原樣奉還）。我的可檢驗假說反而是：softmax/energy 這類**依賴分類邊界**的分數在 unseen generator 上必然與邊界一起失效，而 **real-manifold distance 不依賴 fake 端邊界，有機會在此 failure mode 下存活**。這是實證問題，不是誰嘴上贏——它正是我修正版方案的核心實驗之一（見第 2 節），輸贏都可發表。

#### 挑戰 A1-④（C 挑戰 3）：「幾何塌縮——把 real manifold 撐大到覆蓋 AMR-NB 窄帶，等於把 real 推進 fake 也會落腳的退化區；在第一、二層 cue 被物理摧毀的通道上，撐大 manifold 不是 robust，是主動放棄判別」

**裁決：接受其分層結論，反駁其全稱形式，並正式與 C 合流。**

C 的存活層級（相位/高頻先死、韻律/長時包絡最韌）我接受為物理事實，而且 C 自己在回答我 Q2 時給了出路：「A 的 one-class 若明確只賭第三層可逆、放棄第一二層，那它其實收斂到我提案一的『只用存活特徵』路線——我們可以合流」。**我正式接受合流**：channel-augmented one-class 的正確詮釋，不是「模型在撐大的 manifold 裡什麼都收」，而是「通道 DA 逼模型把 real manifold 建在第三層存活特徵之上」——DA 的作用機制是讓第一、二層特徵在 real class 內部變成高變異噪音而被降權，判別重心自動移到通道不變的層。C 的圖譜給了我方法「為何有效」的物理解釋，我的方法給了 C 的圖譜一個可訓練的實作。

反駁全稱形式的部分：「撐大 manifold＝放棄判別」只在「該通道下第三層也不可分」時成立。#3 的實證（DA 後六條件 EER 波動 <0.1%）證明**至少在 in-domain generator 下，codec 通道後真假仍可分**——若 DA 真的把 fake 一起吞進 real 區，#3 的 EER 不可能守住。所以塌縮不是 DA 的必然後果，而是特定極端條件（窄帶 + re-synthesis）的後果。對那個條件，我的修正是：**承認判別力的物理上限，讓模型在資訊摧毀區棄權**——one-class 與 selective prediction 在此不再是我的兩個提案，而是同一個系統的判別層與誠實層。這是 Round 2 逼出來的最重要結構修正：**提案一與提案二必須合體，不能分開活**。

另接受 C 對我論證鏈最脆一環的指控：#3 的樂觀結論是「已知 6 codec + in-domain generator」下得到的，外推到雙重未知未經驗證。修正：把「6 codec DA 能否 cover 第 7 種」按 C 的原語層假說（帶限/CELP 相位重置/感知量化三原語）設計成 leave-one-codec-out 的**假說檢定**而非默認前提，且 DA 在原語層而非 codec 產品層取樣。這正是 H 要求的「月 1–3 先驗證核心假設」的具體內容。

#### 挑戰 A1-⑤（D 挑戰四 + 回答我 Q1）：「免費午餐——你把 real manifold 沿通道方向撐大，我的 deepfake 本來就要過這些通道，自然漂進你為 real 撐開的區域；你要擔心的不是 adversarial perturbation，是 re-synthesis + channel selection」

**裁決：反駁其全稱形式（與 A1-④ 同一個論證），全盤接受其威脅模型修正。**

反駁：D 的「自然漂移」論證有一個隱藏前提——「過通道後真假不可分」。若成立，任何偵測器（不只我的）在該通道上都死，這不是 one-class 的專屬漏洞；若不成立（第三層 cue 存活），則 fake 過通道後漂進的是「通道退化區」，不是「real 區」——模型依存活特徵仍可拒斥。#3 的 DA 實驗再次是反例：DA 覆蓋的通道上 fake 並沒有自動變 real。D 的攻擊真正成立的區域，是「通道摧毀第三層」與「re-synthesis 重寫第三層」的交集——同 A1-④，該區域的正解是棄權，不是硬判。

接受：D 給的兩個修正我照單全收。(1) 威脅模型主軸從「adversarial perturbation」改寫為「**re-synthesis laundering + channel selection**」——零知識、攻擊者本來就會做、能活過 codec。我的對抗評估必含 re-synthesis 條件（C 對 D-Q3 的預測：依第一二層的偵測器在此逼近 EER 40–50%，依第三層的劣化較小——我的方法屬後者，這是可檢驗的差異化預測）。(2) C 給的殘存判別力來源——「攻擊者為維持『聽得像目標語者』而**不得不保留**的第三層結構」——寫進方法的理論定位：存活特徵偵測賭的是攻擊者的功能性約束，不是他的疏忽。天花板低但地板實。

#### 挑戰 A1-⑥（E 挑戰一）：「換了目標函數，沒換掉牆——好 TTS 的目標函數就是把 fake 推進 real manifold，one-class 的可分性隨生成端進步單調惡化；你仍在 G 說的四輪循環裡」

**裁決：反駁一半、接受一半。**

反駁的一半：「生成器優化目標＝騙過判別器」不等於「fake 在所有特徵空間中逼近 real」。生成器優化的是**感知代理**（mel loss、特定 discriminator 的對抗損失、人耳 MOS），不是 SSL 全表徵空間；感知空間的逼近與 SSL 高維空間的重合之間有 gap——這正是 in-domain EER 還能做到 0.06%（#1）、以及 VoiceWukong 裡 AASIST2 對閉源生成器仍有 13.5% 而非 50% 的原因。E 的「單調惡化」是長期趨勢方向，我接受；但從趨勢推出「此路已死」是把導數當成了函數值。防守本來就是買時間的生意——問題只在你買到的時間拿來幹嘛。

接受的一半：我收回 Round 1「對 unseen generator 天然免疫」的措辭——「免疫」是過強宣稱，正確的說法是「**失效模式與 supervised 不同：不存在『已知 generator 清單被繞開』這種零成本攻擊，攻擊者必須改為攻擊 real manifold 本身**」。同時接受 E 對我提案二的評價方式反過來定調：我提案一的價值不在「更準的偵測器」（那確實在四輪循環裡），而在 (a) 交互作用 benchmark（benchmark 類貢獻正是 G 的歷史分析中進頂會的類型）與 (b) 為提案二供應一個不依賴 fake fingerprint 的 uncertainty signal。方法本身降級為手段，不再是目的。

#### 挑戰 A1-⑦（G 挑戰三前半）：「one-class 不是藍海——OC-Softmax(2021)→ACS(2024)→QAMO(2025)→EBM(EER 1.89%)，你的配方是標準配方，novelty 只剩『DA 只加 real 類』一個 twist，消融實驗等級」

**裁決：接受，novelty 定位全面更新。**

這是史官的職責發揮，我無從反駁事實：one-class for ADD 是至少五年的活躍賽道，我 Round 1 寫「survey #1 點名的緩解方向之一，但尚無工作把它與通道 robustness 聯合處理」——前半句誠實、後半句的「聯合處理」作為 novelty 錨太薄。更新後的 novelty 定位（誠實版）：
1. **unseen-generator × unseen-channel 交互作用 benchmark**——#2 只測 generator 軸、#3 只測 channel 軸，交互矩陣至今無人做，G 的檢索也未發現前作。這升為主貢獻。
2. **「DA 該加在哪一類」的原則性消融**（real-only / fake-only / both × 存活層級解釋）——單獨是消融等級，但掛在交互 benchmark 上就是「解釋劣化來源」的機制性貢獻。
3. **one-class distance 作為 abstention signal 在 shift 下的存活性**——QAMO/EBM 系列全部在報 EER，沒有一篇把 one-class score 當 uncertainty signal 放進 selective prediction 框架測 calibration under shift。這是我查 G 的檢索清單後確認仍空白的一格（標明：基於本場檢索範圍的判斷，開題第一個月需再確認）。

#### 挑戰 A1-⑧（G 挑戰三後半 + D 的 confident-real）：「高品質閉源生成器的輸出就是逼近真實語音；落進 manifold 內部的高品質 fake，one-class 會高信心判真——對低品質 fake 有效的區間恰好是人類自己就能識破的區間」

**裁決：接受現象，反駁「結構性失效」的結論，用人機互補數據反轉。**

G 描述的現象是真的——但請注意它描述的是**所有 passive detector 的共同命運**（supervised 對高品質閉源生成器一樣 EER 13.5–50%，#2），不是 one-class 的專屬缺陷。真正的問題是：高信心判真（confident-real）這個出口對攻擊者是暴利（D 給 H 和我的分析），所以**任何**偵測器都不能在這個區域輸出高信心判定。我的反轉：G 說「one-class 只對低品質 fake 有效，而那是人類能識破的區間」——請回看 #2 的人機互補數據：人類對低品質 deepfake FAR 4–19%（強），對高品質 FAR >82%（近乎全滅）；機器對高品質的判別力雖劣化但仍非零（13.5% EER ≠ 50%）。**分工線恰好是：機器守它仍有殘餘判別力且人類全滅的高品質區，守不住時棄權並警示；人類天然守低品質區。**G 的挑戰不是擊倒 one-class，而是幫我把「one-class 必須嵌在 selective prediction + 人機路由裡才有意義」這件事釘死。對 D 的 confident-real 攻擊軸：全盤接受，修正版的對抗評估主目標函數就是 **max P(confident-real | fake) under re-synthesis + channel selection**，risk–coverage curve 降為次要指標。

#### 挑戰 A1-⑨（H 附帶自省）：「『6 codec DA 泛化到第 7 種』是高風險核心假設，月 1–3 先驗證，驗不過要有退路」＋ 挑戰 A1-⑩（F 附帶提醒）：「極端通道下 bona fide 的 FRR 升為與 EER 同級主指標，通訊錄內聯絡人單獨報告」

**裁決：兩條全盤接受。**

H 的要求與我 Round 1 的風險備案精神一致，現在具體化：月 1–3 的交互 benchmark 階段同時執行 leave-one-codec-out 假說檢定（按 C 的三原語分層），若「原語層 DA 泛化」被證偽，方法部分降級為負面結果＋失效分析，benchmark 仍是論文骨幹。F 的要求直接寫進評估協定：主報告指標為 {fixed FPR ≤1% 下的 recall、極端通道 bona fide FRR（通訊錄內聯絡人子指標另設更嚴門檻）、ECE under shift、max P(confident-real|fake)}，EER 降為與文獻對照用的次要指標。F 說「真孫子在山上打電話被標成 AI 兩次，我就永久關掉」——這句話比任何 reviewer 意見都有效力。

### 1.2 針對提案二（Selective Prediction）的挑戰

#### 挑戰 A2-①（D 回答我 Q2 + H 的追問）：「棄權洪水無利可圖（你贏），但『假真人背書攻擊』有暴利——攻擊者目標函數是 max P(confident-real | fake)，你的評估只報 risk–coverage 會漏掉主戰場」

**裁決：全盤接受，這是紅隊送給這個提案最重要的一句話。**

我 Round 1 的對抗性分析只想到了 abstain 出口（並正確論證它對攻擊者不利——D 也承認我贏了這半局），但漏了 confident-real 出口。修正：(1) 對抗評估的主目標函數改寫為 max P(confident-real | fake)，攻擊動作空間採 D 的「零知識武器庫」（re-synthesis、channel selection、閉源生成器輪換）；(2) 系統設計上，confident-real 的輸出門檻必須遠嚴於 confident-fake（不對稱閾值）——因為兩種錯誤的社會成本不對稱：錯誤的紅燈是打擾，錯誤的綠燈是替詐騙背書（#2 人類對高品質 deepfake FAR >82%，機器綠燈會強化這個弱點）；(3) 極端版本甚至可以取消綠燈——系統只有「疑似合成」與「無法判定」兩態，永不輸出「確認真人」。這個設計選項的 usability 代價由 F 的 user study 量測。

#### 挑戰 A2-②（F 的 2.4/2.5）：「30% 棄權率照那個措辭我會關掉 App；棄權必須與高風險語境門控解耦、內建一鍵動作、按媒介即時性分層」

**裁決：全盤接受，並確認這是合流介面而非挑戰。**

F 的三個修正（技術棄權率與使用者感知警示率解耦、棄權提示內建一鍵回撥、上限按媒介即時性分層）我全部採納為系統設計約束。F 說得對：「無法判定」四個字是雜訊，「無法判定＋【用通訊錄號碼回撥】按鈕」是防護。我的模型層輸出從 {real, fake, abstain} 三態修正為 {risk score, uncertainty, 建議動作} 三元組，把「何時可見、說什麼、給什麼按鈕」整段讓渡給 F 的警告設計層。這正是 F 在 Round 2 附註裡說的「A/H 出『何時該說不知道』，我出『說了之後人會不會照做』」——同一個系統的模型層與 UI 層。

### 1.3 對我 Round 1 三個提問的回答之處理

- **D 答我 Q1**（adversarial perturbation 可行性）：D 確認 perturbation 會被 codec 投影掉（我的直覺對），但真威脅是 re-synthesis + channel selection——已納入威脅模型（A1-⑤）。
- **C 答我 Q2**（codec 共通結構/可分離性）：三原語假說＋「高頻不可分因為已被摧毀、中低頻部分可分」＋「laundering 可逆性分層」——已成為我修正版的假說檢定設計與合流基礎（A1-④）。C 給 SSL 的建議（中層 probing + band-limited adaptation、逐層 × codec 頻寬的 probing 熱圖）採納為實作細節。
- **B 答我 Q3**（機率式證據/缺席先驗）：B 接受 detector 輸出機率，但加碼要求 **P(fake | watermark 狀態)** 的條件化形式——接受，這與 A1-② 的 watermark 去相關訓練是同一件事的訓練端與推論端。B 對「缺席訊號」的分級設計（依情境 base rate 與標記普及率加權）我認同，並確認我的 detection 層對「無憑證音訊」的先驗設定將採 B 的建議：冷不防來電→缺席中性；已知應簽署來源→缺席可疑。

---

## 2. 修正後的最終主張

### 主提案（合併版）：「誠實偵測器證據鏈」——Fingerprint-Free Uncertainty for Selective Audio Deepfake Detection，銜接壓力測試的警告介面

**合併自**：我的提案一（降級為 signal 供應者）＋我的提案二＋ H 提案二（selective prediction，H 的評估協定與 conformal 保證比我嚴謹，採 H 版）＋ F 提案一（警告 UX 與受騙率 user study）＋ D 的 confident-real 對抗評估軸＋ C 的存活層級解釋框架＋ B/S3 的 watermark 去相關。

**核心主張（修正後）**：在 unseen generator（#2）與 unseen channel（#3）雙重 shift 下，沒有任何 ADD 系統的單點判決可信；可部署的形態是「知道自己何時不知道」的偵測器＋綁定高風險語境的行動化警告。我的角色貢獻三件全場獨有的東西：

1. **Fingerprint-free uncertainty signal**：channel-augmented one-class distance（含 watermark 去相關訓練與 mark-to-frame 壓力測試）作為不依賴 fake fingerprint 的 OOD 分數，與 softmax confidence / deep ensemble / MC-dropout / energy / Mahalanobis 同台比較。核心可檢驗假說：邊界依賴型分數在 unseen generator 上與邊界一起失效，manifold 距離型分數存活較好。無論假說成立與否，「哪種 uncertainty signal 在 shift 下最不騙人」的系統性實證都是第一份。
2. **Confident-real 對抗評估協定**：主目標函數 max P(confident-real | fake)，攻擊空間＝re-synthesis ＋ channel selection ＋ 閉源生成器輪換（D 的零知識武器庫）；不對稱閾值設計（綠燈門檻嚴於紅燈，或取消綠燈）。
3. **Unseen-generator × unseen-channel 交互作用 benchmark**（月 1–3，保底貢獻）：VoiceWukong 閉源生成器樣本 × ADD-C 條件矩陣＋（若與 C/G 合流）真實通道樣本，leave-one-generator-out × leave-one-codec-out 雙重交叉，並用 C 的存活層級拆解劣化來源。此為兩軸文獻各自為政後無人填補的空白。

**評估指標公約**（F/G/H 已收斂，我簽字）：fixed FPR ≤1% 下的 recall、通訊錄內聯絡人 FRR 子指標、ECE under shift、risk–coverage、max P(confident-real|fake)、多 base rate expected cost。EER 僅作文獻對照。

**一年時程**：月 0 IRB 送件（H 的鐵律）；月 1–3 交互 benchmark ＋ 核心假設檢定（原語層 DA 泛化、one-class score 的 shift 行為初篩）；月 4–7 uncertainty signals 系統比較 ＋ watermark 去相關消融；月 8–9 confident-real 對抗評估（邀 D 的攻擊配方）；月 10–12 與 F 合流的警告介面 pilot user study（VoiceWukong 樣本、有/無校準提示的受騙率差異）；全程每階段有保底產出（benchmark、負面結果均可獨立成文，#2 的 USENIX 先例）。

**誠實的邊界**（威脅模型第一頁）：本方案對「攻擊者叫受害者忽略警告」的社會工程無直接防禦（F/D 的共識殘留風險），防禦鏈的最後一環是 F 的行動化設計與機構端部署；對「窄帶＋re-synthesis 的資訊摧毀區」不宣稱判別力，宣稱誠實棄權。

### 附屬立場：提案一不再獨立成篇

Channel-Robust One-Class 作為獨立方法論文的 novelty 已被 G 的檢索否決（QAMO/EBM 賽道擁擠），其殘餘價值全部注入主提案：DA-on-real-only 消融、存活層級解釋、distance-as-uncertainty。若主提案的月 1–3 檢定顯示 one-class score 在 shift 下確實存活優於邊界型分數，它會以「主提案最重要的實驗結果」的身分活著，比原本作為獨立提案活得更好。

---

## 3. 最終推薦（以 Detection 研究者立場，從全場提案中選）

### 推薦一（首選）：H 排名第 1 的合併方向——「校準棄權偵測器（A2/H2）＋ 壓力測試警告 UX（F1）＋ confident-real 對抗層（D）」

理由：這是全場唯一把 primary outcome 直接設為「受騙率下降」而非技術代理指標的方向，正中問題陳述的硬性要求；它不與生成器軍備競賽（貢獻是評估框架與人機分工原則，不隨生成器版本過期——G 的四輪循環批判對它免疫）；可行性下檔全場最穩（偵測器現成、資料集可得、IRB 月 0 送、每階段有保底）；人機互補有 #2 的硬數據撐；且經 D 的 confident-real 修正後，它是唯一對紅隊「虛假安全感」指控有結構性回應的方向——偵測器不在沒有下界的地方發出確定的聲音。八個角色裡 A、F、G、H 四人獨立收斂於此，且收斂的是「問題的正確形態」而非「安全的熱門題」。我的 fingerprint-free uncertainty signal 是這個方向裡我不可替代的技術貢獻。

### 推薦二（次選）：C2/G2 合流的「真實電話通道存活性 benchmark」＋ 我的 unseen-generator 軸 → 雙軸交互矩陣

理由：經 G 的 R5 查證，「重錄存活」已有人做（AudioMarkBench、Özer et al.）、「真實電信通道（VoLTE AMR-WB/EVS、LINE Opus、tandem transcode）」仍是確認無人碰的空白——這是全場經過檢索驗證後最乾淨的 gap；它是其他所有方向的證據地基（B 的 soft binding 可行域、AudioClash 的作用域邊界、我的交互 benchmark、電信端部署決策全靠它）；benchmark 類貢獻是這個領域歷來進頂會的類型（ASVspoof、VoiceWukong 先例），負面結果（浮水印全滅＝對 EU AI Act Article 50 的政策否證）照樣有發表與社會價值；繁中/台灣 165 情境填真空。風險是 H 指出的工程＋法律（IRB/電信法規需月 0 排除），故列次選。條件：靈魂必須是「揭露模擬的樂觀偏差」（H 的裁決），且「通道一致性檢查作為反詐訊號」那一半按 D 的紅隊判決放棄或降級為鑑識輔助。

---

## 4. 結語

Round 2 把我的提案一打掉了一半——被打掉的那一半（獨立方法、免疫宣稱、DA 萬能）該被打掉；活下來的那一半（不對稱採樣權、存活特徵詮釋、distance-as-uncertainty）變成了一個更強的合體提案的零件。我 Round 1 結尾說「若討論組更重視『直接降低受騙率』的社會證據鏈，提案二更對題」——Round 2 的全場交叉檢驗證明了這個 if 子句為真。作為用 EER 說話的人，我最後用一個數字收尾：#2 的人類對高品質 deepfake FAR >82%——機器唯一不可推卸的職責，就是在它還有判別力的那個區間誠實出手，並在沒有的區間誠實閉嘴。這就是我修正後的全部主張。
