# 最終統整：五個碩士論文方向
日期：2026-07-13

> 主持人統整。本文閱讀了 00-problem-statement、survey/README（8 篇文獻與 Research Gap 地圖）、以及 round1–round3 共 24 份討論紀錄後寫成。全程引用具體發言與文獻編號（#1–#8 對應 survey，S/R/T 系列為 Agent G 的檢索編號）。凡標「猜測」者為未經實測的推論。

---

## 一、討論歷程回顧

### Round 1：六大提案流派浮現

八位討論者各自獨立提案，收斂出六條路線：

1. **被動偵測的方法論翻新**：Agent A 提「Channel-Robust One-Class Learning」（以真實語音為錨、只對 bona fide class 施加 #3 的通道 DA），主張「augmentation 只該用來擴張你有生成過程控制權的那一類（real）」。
2. **誠實棄權 / selective prediction**：Agent A 提案二與 Agent H 提案二獨立同構——接受偵測器在 unseen generator 上就是 EER 13.5–50%（#2）的現實，改讓模型「在不可靠時可靠地說我不知道」，銜接 #2 的人機互補數據（人類對低品質 deepfake FAR 4–19%、對高品質 FAR >82%）。
3. **跨層一致性稽核 / Audio Integrity Clash**：Agent B、G、H 三人（含 A 候選 5、E 候選 A）獨立把 #7 的影像版 Integrity Clash 遷移到 audio，稽核 C2PA manifest × watermark × passive detector 三層訊號。
4. **互動式挑戰-回應 / liveness**：Agent D、E、F 三人獨立提出——把防線從「事後分析攻擊者控制的靜態音訊」移到「攻擊者無法離線預備的即時互動」。
5. **真實通道存活性 benchmark**：Agent C 提案二與 Agent G 的 G-2 獨立提出——現有 benchmark 全是離線模擬通道（#3），沒有人把音訊灌過真實電信/VoIP 通道量測。
6. **邊緣提案**：Agent B 的 watermark-bound soft binding、Agent C 的存活圖譜、Agent D 的攻擊成本曲線、Agent E 的人群層級同源連結、Agent F 的壓力測試警告 UX。

### Round 2：哪些提案被重創、哪些變強

**被重創的提案：**

- **跨層一致性稽核（流派 3）** 遭 Agent D、E、F 三面夾擊，要害一致：**詐騙 deepfake 三層訊號兩層恆缺席**。D 的原話最直白：「我做詐騙電話時當然不會幫我的假音訊簽 C2PA、也不會嵌浮水印」（#6 明載 provenance「對不附 credential 的惡意 deepfake 完全零覆蓋」）；F 補刀「缺席的訊號對一般人不構成警告……我看過的 99.9% 的內容都沒有憑證」；E 用貝氏論證「過渡期 P(fake|無憑證) ≈ 先驗，資訊增益 ≈ 0」，且 EU AI Act Article 50 只綁守法生成器，「對抗性缺席」的鑑別力在對抗場景**原則上到不了**。Agent A 再補一顆 ML 炸彈——S3 Watermark Shortcut 證明三層在 ML 層並不獨立（detector 會偷看 watermark，mark-to-frame 攻擊讓 AASIST EER 16%→75%）。

- **互動式挑戰-回應（流派 4）** 遭 Agent G 的檢索硬證擊沉：**D-CAPTCHA（AsiaCCS 2023）三年前就發表了音訊版挑戰-回應**（準確率 91–100% vs 無挑戰 71%，含 41 人 user study），**D-CAPTCHA++（IJCNN 2024）已攻破一輪**，StreamVC（Google ICASSP 2024）端到端 70.8ms 讓「延遲軟肋」過期。「首個」宣稱與「延遲判別訊號」雙雙不成立。Agent B 再指出它「借了 challenge-response 的名字卻沒有 trust anchor 與 channel binding，relay 攻擊直接繞過」，D 自己 Round 2 就親手把 relay（真人共犯只在挑戰段接手，成本低）標為頭號威脅。

- **Channel-Robust One-Class（流派 1）** 遭 Agent G 檢索排雷（OC-Softmax→ACS→QAMO→EBM 是五年活躍賽道，novelty 只剩「DA 只加 real 類」一個消融等級 twist）、C 的幾何塌縮反駁（把 real manifold 撐大到窄帶＝主動放棄判別）、D 的免費午餐反駁（deepfake 本來就要過這些通道，自然漂進被撐大的 real 區）。

- **人群層級同源連結（Agent E 提案二）** 被六人一致否證：G 指出這就是 source verification（STOPA/2505.14188，Interspeech 2025 special session）且 open-set 下同樣崩；H 指出「同生成器+同參考語者」定義 ground truth 是 label leakage 循環論證；D/F 指出親情詐騙每案聲源本來就不同、跨受害者不重複；A/C 指出 laundering 後 speaker embedding 存活的是身分、被濾掉的正是 generator artifact。

- **通道一致性檢查（Agent C 提案二下游模組）** 被六人判死：攻擊者用 virtual audio cable 或 loopback「先過一次真電話」，通道證據就是真的，一致性檢查全綠燈。

**在質詢中反而變強的提案：**

- **誠實棄權 / selective prediction（流派 2）** 越辯越強。Agent D（紅隊）送出全場最關鍵的一句話：「selective prediction 的危險出口不是 abstain（對攻擊者不利），是 confident-real（系統替攻擊者背書）……攻擊者目標函數是 max P(confident-real|fake)」——這反而幫這個方向補上了真正的對抗評估軸。Agent A 貢獻「one-class real-manifold 距離在 AUC≈0.5 failure mode 下可能存活」的可檢驗假說；Agent F 貢獻「技術棄權率與使用者感知警示率解耦、棄權提示內建一鍵回撥、通訊錄內聯絡人 FRR 單獨報告」四點 UX 設計。

- **真實通道存活性 benchmark（流派 5）** 經 G 的 R5/T3 反覆查證，確認「真實電信通道存活」是 2026-07 全場**唯一經檢索驗證仍無前作**的空白（重錄存活已有 AudioMarkBench/Özer et al./DeAR，Integrity Clash 五人撞題+原作者預告，challenge-response 三年前已發表）。

**指標共識**：Agent F、G、H 三方在 Round 2 收斂出「禁用裸 EER、改用固定低 FPR 下的 recall + ECE + risk-coverage + 多 base rate expected cost」的評估公約；H 明言「只報 EER 的 ADD 碩論我在 proposal defense 就會擋」。

### Round 3：合併、修正與跨角色共識

Round 3 的關鍵動作是**大量的自我降級與合流**，這是本次討論最誠實的一輪：

- **Agent H（指導教授）親手撤回自己 Round 1 的頭號提案**（AudioClash），坦言「七個不同視角的人用七套論證擊中同一要害，那不是誤解，是事實」，並回答 F 的必答題：「AudioClash 的用戶是查核組織，不是那個被倒數計時『快匯錢』的阿嬤。」
- **Agent B（密碼學）舉白旗**：「我的兩個提案對阿嬤接到的即時詐騙電話，判定都是救不了」，把 provenance 定義域誠實限縮到「非即時的語音訊息/媒體檔案/關鍵權威來源」，並把 Integrity Clash 降為模組、soft binding 改為「索引不 payload」構造、與 C/G 合流。
- **Agent A** 承認提案一「被打掉的那一半該被打掉」，把 one-class 降為 selective prediction 的一個 uncertainty signal 供應者，兩提案合體。
- **Agent E** 正式撤回人群層級連結，但把「相對一致性」內核轉世為「通話內聲源連續性稽核」，並把挑戰-回應**重新定義**為「OOD 壓力源——把攻擊者輸出從被動偵測器的失效區推回有效區」，改名「Active Liveness Probing」。
- **Agent C、G** 合流為真實通道 benchmark；**Agent D** 用自己的口頭禪砍掉自己的提案二（互動層），降為攻擊成本地圖的一個攻擊維度。

**跨角色共識（特別注意三個把關角色 D 紅隊、F 民眾、H 教授的判定）：**

| 方向 | D（紅隊）判定 | F（民眾）阿嬤那行判定 | H（教授）判定 |
|------|------|------|------|
| 誠實棄權 + 警告 UX | **推薦一**（罕見地推薦防禦方案：「你沒有假裝擋住我，只是不在你擋不住的地方發出確定的聲音」） | 上班族「可以」、阿嬤「有條件」（做對三點接近可以） | **首選**（唯一直接量測受騙率） |
| 真實通道 benchmark | 支持（提供攻擊武器庫） | 有條件（案發現場的上游證據基礎） | 次要（工程+法律風險，靈魂須是「揭露模擬樂觀偏差」） |
| 攻擊成本地圖 | **主提案**（照妖鏡、品管關） | 救不了（當下）但「少害她」 | **次選**（評估型貢獻不過期） |
| Active Liveness Probing | 承認「全場唯一真的提高攻擊成本」，但自己砍為攻擊維度 | 有條件（機構端封死社工繞過） | 不推薦（前作+relay+情緒，殘值是壓力測試） |
| Provenance 可達性 | provenance 對無憑證即時詐騙攻擊成本＝零（B 親自確認） | 救不了阿嬤、上班族/選民有條件 | 不推薦為主軸（偏離硬性要求，但量測+政策審計可） |

三個把關角色的最強共識：**「校準棄權 + 壓力測試警告 UX」是全場唯一把因變數直接設成「受騙率」、且不依賴任何未兌現長期賭注（憑證普及、延遲軟肋、平台配合）的方向。** 這是 A、C、D、E、F、G、H 七個角色在最終推薦中都列為推薦一的方向——近乎全場一致。

---

## 二、五個論文方向（依推薦順序）

---

### 方向一（首選）：會誠實棄權的偵測器 × 壓力測試警告 UX × 受騙率量測

**1. 暫定題目**
中：《知道自己何時不知道——分布偏移下語音深偽偵測的校準棄權框架與壓力情境警告介面之受騙率實證》
英：*Knowing When It Doesn't Know: Shift-Aware Selective Prediction for Audio Deepfake Detection and a Deception-Rate Evaluation of Stress-Tested Warning Interfaces*

**2. 核心研究問題**
給定一個在 unseen generator 上必然劣化（EER 13.5–50%）的偵測器，如何讓它在不可靠時「可靠地棄權」而非「自信地錯」，並設計一個接住棄權結果的警告介面，在模擬詐騙壓力下真正降低受騙率？

**3. 創新點與對應的 research gap**
- 對應 survey Gap 地圖第 1 點（被動偵測的極限）與 #8「可信的使用者體驗為優先方向卻無人做」。#1 指出人類辨識準確率僅約 73%、#2 提供人機互補的實測分布（人類對低品質 deepfake FAR 4–19%、對高品質 FAR >82%）——這是設計 deferral policy 的現成依據，但目前 audio 領域沒有任何 ADD benchmark 報告 risk-coverage 曲線或 shift 下的 calibration（H 提案二、A 提案二的共同判斷）。
- 三個全場獨有的貢獻：(a) 第一個 shift-aware selective-prediction ADD benchmark；(b) 由 Agent D 逼出的 **confident-real 對抗評估軸**（`max P(confident-real | fake)`），這是評估「棄權機制不被零成本繞過」的關鍵，現有文獻完全缺席；(c) 第一個量測「偵測器準確率 × 警告設計 × 使用者壓力 → 實際受騙率」因果鏈的 usable-security 研究。
- Agent A 貢獻的可檢驗假說：邊界依賴型 uncertainty 分數（softmax/energy）在 AUC≈0.5 時與邊界一起失效，而 **real-manifold 距離型分數不依賴 fake 端邊界，可能在此 failure mode 下存活**——無論成立與否都是第一份系統性實證。

**4. 攻防紀錄摘要**
- Agent D（紅隊）本要打它，反而成為最強背書者：「這是全場唯一一個對我的零成本繞過，輸出的不是虛假安全感的方向」。D 唯一的持續攻擊——confident-real 攻擊面——已被 A、F、H 收編為對抗評估主軸。
- Agent E 曾質疑 selective prediction 是否只是「更會泛化偵測器」的變體；H 明確反駁：它的因變數是「可靠棄權 + 受騙率下降」而非更低 EER，不與 ElevenLabs 賽跑，貢獻不隨生成器過期。
- Agent F 曾以「三成來電顯示『無法判定』我會關掉 App」重創其可用性，但隨即給出四點修正（棄權率/警示率解耦、內建一鍵回撥、分媒介上限、通訊錄 FRR 子指標）把它從「救不了」救成「有條件」。
- Agent B 從密碼學角度背書：「它是誠實系統的典範——密碼學最核心的紀律就是精確陳述我證明了什麼、沒證明什麼，這個方向把同樣的紀律帶進 detection」。

**5. 實驗規劃**
- **資料集**：ASVspoof 2019/2021 LA+DF、In-the-Wild、MLAAD（皆可下載）；VoiceWukong 可得部分；閉源商用生成樣本用 ElevenLabs 等 API 小規模自建（先確認 ToS 與 IRB）。可選強化：接方向二的真實通道樣本作為 unseen-channel 軸。
- **Baseline**：AASIST、wav2vec2/XLS-R backend、RawNet2 三套現成偵測器；uncertainty baseline = MSP（max softmax prob）、temperature scaling。
- **方法步驟**：(i) 建 shift 評估矩陣（in-domain / unseen-generator / unseen-channel / 兩者疊加）；(ii) 量測各偵測器 baseline calibration（ECE、reliability diagram）與 risk-coverage 曲線；(iii) 比較 6 種棄權機制（MSP、deep ensemble、MC-dropout、energy score、Mahalanobis on SSL features、+ A 的 one-class real-manifold 距離）；(iv) confident-real 對抗評估（用 D 的 attacker-cost curve 框架量「把 fake 推進 confident-real 區的最便宜路徑」）；(v) deferral policy 用 #2 公佈的人類表現數據做 human model 模擬；(vi) 小規模 user study（30–50 人）量警告 UX 的受騙率。
- **評估指標（全場公約）**：固定 FPR ≤1% 下的 recall（通訊錄內聯絡人另設更嚴子指標）、ECE under shift、risk-coverage、`max P(confident-real|fake)` 攻擊成本、多 base rate expected cost、受騙率（primary outcome）、誤報後信任衰減曲線（alarm-fatigue 閾值作為輸出結論）。禁用裸 EER 為主指標。
- **消融**：棄權訊號種類 × shift 類型的交互；偵測器準確率高低 × 警告形式（刻意用「調爛的偵測器」測警告設計的容錯度）；無綠燈設計 vs 有綠燈的 usability 代價；棄權率/警示率解耦的門控效果。

**6. 一年時程表**
- 月 0（修課期）：IRB 立即送件（最常見的時程殺手，提前拆）。
- 月 1–4（第一季）：復現 3 個偵測器 + 建 shift 評估矩陣 + baseline calibration/risk-coverage——**此階段產出即保底半篇 benchmark 論文，不依賴 IRB**。
- 月 5–7（第二季）：比較 6 種棄權機制（含 real-manifold 距離）+ confident-real 對抗評估。
- 月 8–9（第三季）：deferral policy 模擬 + 小規模 user study（含高齡分層為 stretch goal 而非 blocker）。
- 月 10–12（第四季）：expected-cost 整合、警告 UX 分析、寫作。

**7. 真實情境部署路徑**
主場景為 LINE 語音訊息詐騙（上班族情境，F 判定表中唯一出現「可以」的人物，因為非即時媒介有操作空間）。產出是「偵測器需多低 FPR、警告需怎麼下」的部署準則，可被通訊平台採用。核心機制不是「告訴你這則訊息真假」，而是「在受騙決策時刻製造摩擦、觸發查證行為」——警告內建的「一鍵回撥/改視訊確認」把警政宣導多年、壓力下沒人做得到的查證程序降到一次點擊。對阿嬤情境則需系統端/電信端部署（本論文產出證據與準則，不產出 App）。

**8. 社會福祉貢獻**
直接回答問題陳述的硬性要求「降低民眾受騙機率」——它是全場唯一把「受騙率下降」當 primary outcome 的方向。產出「這個設計讓受騙率從 X 降到 Y」的可引用數據與 alarm-fatigue 部署閾值，服務所有消費端防詐產品的設計。「無綠燈原則」（系統只有「警示」與「沉默」兩態、沉默不是背書）防止偵測器製造新的虛假安全感。

**9. 風險與備案**
最大風險：所有棄權訊號在 AUC≈0.5 failure mode 下全數失效（可能）。備案：論文轉向「嚴謹量化此失效 + calibration benchmark + confident-real 攻擊面 taxonomy」——參照 VoiceWukong（#2）先例，高品質負面結果在此領域可發表，且月 1–4 的 benchmark 已保底半篇。次要風險：IRB/user study 時程——備案為先用 VoiceWukong 已公佈人類數據做 policy 模擬（不需 IRB），user study 縮為 pilot。誠實邊界（寫進威脅模型第一頁）：對「攻擊者叫受害者忽略警告」的社會工程無直接防禦，防禦鏈最後一環是行動化設計與機構端部署。

---

### 方向二（次選）：「活過一通電話嗎？」真實電信通道多防線存活性的獨立審計 Benchmark

**1. 暫定題目**
中：《活過一通電話嗎？真實電信通道下語音深偽偵測、浮水印與溯源訊號存活性的獨立審計 Benchmark（含繁中詐騙情境）》
英：*Does It Survive a Phone Call? An Independent Audit Benchmark of Audio Deepfake Detection, Watermarking, and Provenance Survival over Real Telecom Channels*

**2. 核心研究問題**
現有 audio deepfake 通道 robustness 研究全部建立在離線模擬通道上（#3 用 codec 軟體）；模擬 benchmark 相對真實電信/平台通道的「樂觀偏差」有多大？各防線（偵測器、浮水印、溯源）在真實案發通道上的「不可達區」邊界在哪裡？

**3. 創新點與對應的 research gap**
- 對應 survey Gap 地圖第 1 點殘留 gap：#3 自承「對未知 codec（社群平台私有轉檔管線）的泛化未驗證」。Agent G 用 R5/T3 三重查證確認：**「真實電信通道存活」是 2026-07 全場唯一經檢索驗證仍無前作的空白**（ADD-C=模擬、AT-ADD 2026=模擬+unseen generator、RADAR 2026=模擬 transformation、Resemble AI 8-系統 benchmark=私有測試集廠商自辦；重錄存活已被 AudioMarkBench/Özer et al./DeAR 做過，故 novelty 嚴格錨定「真實電信通道」而非「重錄」）。
- Deepfake-Eval-2024（G 檢索 S10）證明真實流通樣本 audio AUC 掉 48%，給「真實 vs 模擬落差」強烈先驗。台灣 165 情境（VoLTE AMR-WB/EVS、LINE Opus、繁中話術）是產業英語系部署與學術資料集的雙重真空。
- 五個評測軸整合了全場多個角色的貢獻，是單篇提案做不到的基礎設施。

**4. 攻防紀錄摘要**
- Agent H 質疑三重風險（工程混淆變因、法律、產業已部署）。Agent G 於 Round 3 用 T2 反駁法律風險：台灣《通訊保障及監察法》第 29 條第 3 款「監察者為通訊之一方且非出於不法目的者，不罰」——rig 通話兩端皆為研究團隊自有設備、播放公開資料集語料，走的是全場最安全的法律路徑。工程混淆變因用「固定 UE + 記錄協商 codec/PLR/jitter 為標註維度」解決。
- Agent H 質疑「資料集只是配菜」，但自己也承認「這個領域的推進器歷來就是 benchmark（ASVspoof、In-the-Wild、VoiceWukong 都進頂會）」，並給通行證：主 claim 須是「揭露模擬的樂觀偏差」而非「我收了很多資料」。
- Agent C 的下游「通道一致性檢查」模組被六人判死（D 的 loopback 攻擊零成本繞過），C 於 Round 3 全盤接受並撤回，僅保留「單向紅燈有效、綠燈無意義」的查核組織排除工具。
- Agent D 支持它作為攻擊成本地圖的「真實通道武器庫」；Agent B 認領浮水印 bit-level 存活軸並提供「索引不 payload」構造；Agent A 認領 unseen-generator × unseen-channel 雙軸交互矩陣。

**5. 實驗規劃**
- **資料集**：自建（避開拿不到的資源）。素材 = TTS 生成音訊（3–5 家含閉源商用）+ 團隊錄音（簽知情同意）+ 165 公開話術腳本。通道矩陣依 F 給的真實分佈加權：VoLTE（AMR-WB/EVS）≥ LINE 語音訊息 > LINE 通話 > Messenger > 社群平台轉檔；轉傳深度上修到 5；納入「混合通道」型態（LINE 文字鋪陳→轉電話收割）。每通記錄協商 codec、實測 PLR/jitter。
- **Baseline**：#3 模擬通道訓練的公開模型（AASIST、wav2vec2 系）；比較對象是文獻方法而非 Google/Resemble 商用系統（避開 H 紅線 1.3）。
- **五個評測軸**：(1) 偵測器劣化（真實 vs 模擬的 fixed-FPR recall 落差）；(2) cue 存活圖譜（SSL layer × channel 的 probing AUC 熱圖，採 A 的方法建議，檢驗「相位先死、高頻次之、韻律最韌」的存活層級假說）；(3) 浮水印可靠容量（AudioSeal/SynthID 的 bit-level I(embedded;recovered) 掃描，回答 EU AI Act Article 50 的標記在案發通道可不可讀）；(4) 通道指紋（closed-set 路徑分類器，輸出 channel-conditioned 條件向量 + 單向宣稱-證據矛盾偵測）；(5) 攻擊者視角切分（加收 tandem 串接、loopback re-injection、re-synthesis laundering + 平台轉檔）。
- **評估指標**：fixed FPR ≤1% 下的 recall（全場公約）、模擬 vs 真實落差、bit-level 存活率、通道指紋準確率。
- **消融**：channel-conditioned detection vs #3 已知分佈 DA vs #2 證明有害的 multi-domain training；unseen-generator × unseen-channel 雙軸交叉（leave-one-generator-out × leave-one-codec-out）。

**6. 一年時程表**
- 月 0：IRB 送件 + 法律意見（通保法 §29 路徑）+ 工具鏈復現。
- 月 1–3（第一季）：語料定稿、rig 定案。
- 月 3–6（第二季）：**MVP 通道錄製（單電信商 VoLTE + LINE 兩型態）→ 保底可發表單元**。
- 月 6–9（第三季）：四軸評測 + stretch 通道（第二電信商、Messenger）。
- 月 9–11（第四季）：條件化偵測對照 + 交互矩陣。
- 月 11–12：資料集去識別化開源、寫作。

**7. 真實情境部署路徑**
不直接擋詐騙，而是決定「電信端/平台端該部署什麼、165 該信什麼」的上游證據基礎（F 判定表：「阿嬤那一行所有上游決策的證據基礎」）。獨立公開審計填補「產業系統全閉源、零第三方評測」的消費者知情權空白（F：「民眾正在被要求信任這些系統，卻沒人告訴我們它們在真實通道上到底行不行」）。

**8. 社會福祉貢獻**
繁中/台灣 165 情境的第一份公開資源；「模擬樂觀偏差」的量化警示所有後續 ADD 研究的評估效度；浮水印存活軸的負面結果（若全滅）即對 EU AI Act Article 50（2026-08-02 生效）「machine-readable 標記」政策路線的重要否證——法規要求的標記在詐騙實際發生的通道上不可讀，有政策發表價值。

**9. 風險與備案**
最大風險：真實通道錄製的工程工時（體力活）與規模。備案：MVP 分階段設計，月 6 前完成單電信商兩通道即為保底可發表單元；stretch 全砍仍是首個真實通道公開資料集。若落差測出「模擬其實夠好」（H0），也是對社群省下真實收集成本的可發表否證。法律風險已由通保法 §29 路徑排除，但平台 ToS（LINE/Messenger 自動化收發）殘留灰色地帶，緩解為控制速率、半自動人工操作。

---

### 方向三：Adaptive-Laundering 攻擊成本地圖——三類防線的統一「照妖鏡」

**1. 暫定題目**
中：《攻擊者要付多少？被動偵測、溯源與活體驗證三類防線的 Adaptive-Laundering 攻擊成本地圖與物理可逆性標註》
英：*What Does the Attacker Pay? An Adversarial-Laundering Attacker-Cost Map across Passive Detection, Provenance, and Liveness Defenses with Physical Reversibility Bounds*

**2. 核心研究問題**
對每個候選防線，不問「平均 robustness」，而問：攻擊者要讓它突破可用門檻，最便宜的路徑是什麼、需要幾步、其中哪些步驟踩到「不可逆資訊摧毀」的物理下界？

**3. 創新點與對應的 research gap**
- 對應 Gap 地圖第 1、2 點。現有 benchmark（VoiceWukong #2 的 38 變體、Loughborough #3 的 C0–C5）把 laundering 當「隨機後處理/distribution shift」（防禦者視角）；本方向把它形式化為 **adversarial laundering search（攻擊者最佳化視角）**，提出「攻擊成本」作為評估指標——這個成本軸在 audio ADD 文獻中不存在（H 確認）。
- Agent C 的關鍵補強讓它從「純否定性拆除令」升級：每個 laundering 動作標註「不可逆資訊摧毀」（第一二層 cue，做了永久失效）vs「可逆 distribution shift」（第三層，補 DA 可抵消），決定曲線是「懸崖」還是「緩坡」，並產出正面設計指導——「依賴第三層存活特徵的偵測器攻擊成本曲線最陡，因為攻擊者要洗掉第三層就必須破壞『聽得像目標語者』這個功能性約束」。物理可逆性是資訊理論事實、不隨月份過期。

**4. 攻防紀錄摘要**
- Agent E 挑戰「純否定性 + 成本軸會過期」。Agent D 於 Round 3 反駁：純否定性已被 C 的物理下界補上正面產出；「過期的是數字不是方法論」（VoiceWukong 的 13.5% EER 明年也會變，但被引用的是評估協定），而 C 的物理可逆性下界不過期。
- Agent H 給次選（Round 2 排名第 3，16 分），評「評估型貢獻不過期、可行性極高、可當任何偵測器論文的對抗評估層」。
- 它與方向一深度耦合：方向一的「棄權機制不被繞過」正需要這張照妖鏡來證明（H：「這是它比 C2/G2 更適合作為第二推薦的原因」）。

**5. 實驗規劃**
- **資料集**：現成生成器（開源+閉源 API）+ 現成 codec/VC 工具 + 現成 SOTA 偵測器 checkpoint；不訓練任何大模型。可接方向二的真實通道武器庫。
- **Baseline**：VoiceWukong 的「平均劣化」量測（作為對照，證明「攻擊者最佳化的最壞情況」比平均嚴重）。
- **方法步驟**：(i) 定義攻擊者動作空間（換 generator、re-synthesis laundering、codec tandem、平台真實轉檔、loopback re-injection、resample/time-stretch/replay），每個動作標成本代理指標 + C 的物理可逆性標註；(ii) 對 3–5 個公開偵測器（含方向一的 selective-prediction 偵測器、A 的 one-class、C 的存活特徵偵測器）跑貪婪/beam search 找最便宜繞過；(iii) 涵蓋三類防線維度——被動偵測、provenance（B 確認無憑證即時詐騙攻擊成本＝零 + soft-binding commitment 存活率）、liveness（對 D-CAPTCHA 類防線量 relay/社工抽回的成本 + D-CAPTCHA++ adversarial 攻擊在真實通道是否存活）。
- **評估指標**：attacker-cost curve（x=攻擊投入、y=偵測器 EER/recall）、最便宜繞過配方、成本被人力/社工抽回量、物理不可逆下界標註。
- **消融**：哪些防禦設計選擇讓曲線變陡（反向產出）；成本代理指標定義的敏感度分析。

**6. 一年時程表**
- 月 1–3：定義攻擊者動作空間 + 物理可逆性標註框架（與 C 合作）。
- 月 4–7：對被動偵測維度跑 beam search、畫曲線。
- 月 8–10：provenance 與 liveness 維度 + 真實通道武器庫（接方向二）。
- 月 11–12：跨三類防線的 attacker-cost map 整合、寫作。

**7. 真實情境部署路徑**
給部署方（銀行、電信、165）的「照妖鏡」：量化每個候選防線「攻擊者實際要付多少」，阻止機構部署「EER 0.06% 但零成本可繞過」的偵測器。F 判定：對阿嬤是「少害她」而非「救她」——它是其他所有「宣稱能保護民眾」方案的共同品管關。

**8. 社會福祉貢獻**
戳破虛假安全感（D：「一個 EER 0.06% 但被一次換 generator 就崩到 40% 的偵測器，給民眾的是虛假的安全感，這比沒有防禦更危險」）。一個可重複、可擴充的紅隊評估協定，成為後續防禦研究的標準壓力測試。

**9. 風險與備案**
最大風險：成本代理指標的可辯護性（如何把工具難度/金錢/時間/技術等級量化成可比較 scalar，reviewer 必攻）。備案：以 C 的物理可逆性（資訊理論事實）作為不可爭議的錨，主觀成本代理只作輔助排序。若某防線測不出清晰懸崖，「緩坡」本身也是可發表的結論。

---

### 方向四（較高風險，被打殘後重建）：Active Liveness Probing——機構端互動活體驗證的真實通道壓力測試

**1. 暫定題目**
中：《主動活體探測——以 OOD 挑戰放大生成 artifact 與通話內聲源連續性稽核，對既有 liveness 防線的真實電信通道與 relay 壓力測試》
英：*Active Liveness Probing: Using OOD Challenges to Amplify Generation Artifacts and Intra-Call Source-Continuity Auditing, Stress-Tested against Real Telecom Channels and Relay Attacks*

**2. 核心研究問題**
把互動挑戰從「圖靈測試」重新定義為「OOD 壓力源——把攻擊者輸出從被動偵測器的失效區（高品質乾淨）推回有效區（OOD 轉換、artifact 明顯）」；在 relay 攻擊（真人共犯只在挑戰段接手）與真實電信通道下，這條 2023 年的 D-CAPTCHA 防線還剩多少存活率？

**3. 創新點與對應的 research gap**
- 對應 Gap 地圖第 1 點與 #8 的「互動層是分層防禦缺席的一層」。Agent D 承認這是「全場唯一真的提高攻擊成本的方向」，因為它攻擊生成端的真實功能性瓶頸（即時 arbitrary-content 音色轉換）而非攻擊者可洗掉的痕跡。
- Agent E 的三個重新定義撐起 novelty（在 D-CAPTCHA 已存在的前提下）：(a) 不再宣稱「證明對方是人」（relay 下無意義），改為「偵測語音鏈上是否存在即時音色轉換層」；(b) 挑戰是 OOD 壓力源而非圖靈測試——非典型發聲挑戰（耳語、笑聲、哭腔）之所以有效，是即時 VC 對訓練分布外輸入的音色轉換品質會崩，把攻擊者輸出推回被動偵測器的有效區（#2 證明偵測器對 artifact 明顯的低品質輸出很行）；(c) 通話內聲源連續性稽核（E 撤回的人群連結內核轉世）作為反 relay 防線。
- 真正的 gap：D-CAPTCHA/D-CAPTCHA++ 的攻防都在乾淨/模擬條件下跑，**relay/真人共犯/社工繞過**與 **D-CAPTCHA++ adversarial 攻擊在真實電信通道（AMR-WB/EVS + 重錄）是否存活**，兩篇都沒碰——依 C 的存活層級，imperceptible perturbation 很可能被 CELP 重合成投影掉（D 自己確認），這個空白對防守方可能是好消息。

**4. 攻防紀錄摘要**
- 這是全場被打最慘的方向：Agent G 用 D-CAPTCHA（AsiaCCS 2023）+ D-CAPTCHA++（IJCNN 2024）+ StreamVC（70.8ms）三顆硬證擊沉「首個」與「延遲軟肋」；Agent B 指出無 trust anchor/channel binding + relay；Agent A/C 確認延遲被通道抖動淹沒；Agent H 排名墊底（第 10，11 分）指出產業已全球部署（Google 2026-06、Resemble AI <300ms）+ 防不了情緒。
- 存活的關鍵在 Agent E、D、F 三方合流的重構：判別訊號從延遲換成「韻律即時可控性 + 非典型發聲」（C 背書為第三層存活特徵）；命名改為「互動式活體驗證/主動活體探測」不再冒充密碼學；部署形態由 F 的機構端強制（銀行放款/165 代匯款前）封死「叫受害者跳過驗證」的社工攻擊——F 反駁 A/H 的「降級成恐慌中人分辨」：驗證者是機器/機構端流程，阿嬤零操作。
- 誠實殘留：relay 是結構性攻擊，本方向量測其成本而不宣稱消除（D：「這是一場我不確定防守方能贏的硬仗，但這是唯一的方向」）。

**5. 實驗規劃**
- **資料集**：自建「非同步挑戰-回應語料」（挑戰指令固定後離線驅動 streaming VC 生成回應 + 真人錄回應）+「切換點語料」（真人全程/VC 全程/挑戰段切真人共犯）。通道條件借用方向二的基礎設施。
- **Baseline**：D-CAPTCHA（2023）協定重現；被動偵測器（AASIST）在無挑戰條件的 EER。
- **方法步驟（三個 RQ）**：RQ1 挑戰效力圖譜——非典型發聲/prosody 指令/開放語意三族挑戰對 2026 世代 streaming VC（StreamVC、seed-VC）造成多少「轉換品質崩壞」，以 (a) 被動偵測器 EER 恢復量、(b) 對目標語者 speaker similarity 下降量兩軸量測；RQ2 反 relay 連續性稽核——通話內挑戰段 vs 主體段的 speaker embedding 一致性，量共犯接手的成本抬升（共犯用 VC 維持音色時是否被夾回 RQ1 的 OOD 崩壞區）；RQ3 通道存活——RQ1/RQ2 訊號與 D-CAPTCHA++ adversarial 攻擊能否活過 AMR-WB/EVS/Opus。
- **評估指標**：D 的 attacker-cost curve 為主對抗軸（每族挑戰 × 每種攻擊策略：預生成題庫/streaming VC/relay/relay+VC）；fixed low FPR 下的 recall（全場公約）。
- **消融**：挑戰題型 × 攻擊策略 × 通道條件的效力/成本圖譜；封閉 vs 開放挑戰集的可預生成性。

**6. 一年時程表**
- 月 1–2：復現 D-CAPTCHA 設定 + 架 streaming VC 攻擊組。
- 月 3–5：非同步挑戰-回應語料 + RQ1 量測。
- 月 6–8：切換點語料 + RQ2 連續性稽核。
- 月 9–10：接方向二通道管線跑 RQ3。
- 月 11–12：攻擊成本曲線整合、寫作。保底：RQ1+RQ3 單獨成篇（2026 條件下的 D-CAPTCHA 重新評測）。IRB 不在主線（機器攻防量測為主，user study 交給方向一）。

**7. 真實情境部署路徑**
部署於機構端高風險金流決策流程（銀行放款/大額轉帳前、165 處理代匯款求助時強制執行 liveness challenge），阿嬤零操作、社工繞過對機構端無效。覆蓋範圍收窄為「進入機構流程的金流決策時刻」——台灣大額金流幾乎必經銀行臨櫃或轉帳系統，攔截面實際上很寬（R6：2026 年 1–4 月財損 215.3 億，大宗涉金融通路）。

**8. 社會福祉貢獻**
它是全場唯一攻擊攻擊者真實瓶頸的方向，對「即時語音詐騙」這個 provenance 與被動偵測都覆蓋不到的情境提供機構端防線。對「回撥/暗號」這條全球防詐宣導的技術化實證檢驗——就算結論是負面的（即時 VC 已能應對挑戰），也是對現行政策的重要輸入。

**9. 風險與備案**
最大風險（H 已點名）：D-CAPTCHA 前作 + relay + 社工三重打擊，是全場最擁擠、最被攻過的領域，適合風險承受度較高的學生。備案：把定位從「防禦設計」重構為「對既有防線的紅隊壓力測試」（G 指出的唯一活路），RQ1+RQ3 單獨成篇為「2026 條件下的 D-CAPTCHA 重新評測」。誠實邊界：relay 未解、純延遲訊號 2–4 年內失效、產業已重兵部署——三條寫在威脅模型第一頁。

---

### 方向五（較高風險，crypto/政策角度）：Provenance 可達性地圖——真實通道多層訊號存活量測、索引式 Soft Binding 與 Article 50 可讀性審計

**1. 暫定題目**
中：《Provenance 可達性地圖——真實電信通道上的多層驗證訊號存活量測、索引式 soft binding 構造與 EU AI Act Article 50 可讀性審計》
英：*A Provenance Reachability Map: Multi-Layer Signal Survival Measurement over Real Telecom Channels, an Index-Based Soft-Binding Construction, and an EU AI Act Article 50 Readability Audit*

**2. 核心研究問題**
量出 provenance 與 watermark 在真實通訊管線上「活到哪裡、死在哪裡」的邊界，並給出一個能在邊界內工作、對移植/局部剪接攻擊 robust 的密碼學構造；EU AI Act Article 50 強制的 machine-readable 標記在詐騙實際發生的通道上到底可不可讀？

**3. 創新點與對應的 research gap**
- 對應 Gap 地圖第 2、3 點（密碼學溯源的極限 + 多訊號整合）。C2PA 規格（#4）明載 soft binding 為 manifest 復原機制但未給 audio 構造；#7 證明 watermark 與 manifest 若不互相綁定就會被去同步；#6 列出 C2PA 五大缺陷（timestamp 可替換、revocation optional、exclusion range 可竄改等）。
- 三個構造創新：(a) **索引不 payload**——波形內只承載 k-bit transparency-log 索引 + ECC（20 bit 存活容量即可索引 2^20 筆完整 manifest），繞開 C 判決的「電話通道可靠 payload 逼近 0 bit、一個 hash 要 128 bit 塞不進去」死結；(b) **時序鏈式 perceptual-hash 綁定**（滑動窗 hash 鏈）防 D 的移植攻擊（局部替換「帳戶 A→帳戶 B」會破壞被替換窗及其後所有窗的鏈驗證，拼接點就是鏈斷點）；(c) **帶層間依賴的證據圖稽核**（B 從 Integrity Clash 搶救的殘值，把 S3 Watermark Shortcut 的 watermark×detector 因果耦合建進形式化，用 #6 的 formal methods 做安全論證）。
- 政策軸：Article 50（2026-08-02 生效）可讀性的第一份審計——無前作。

**4. 攻防紀錄摘要**
- Agent B 是全場立場移動最大的角色：Round 1 兩個提案（Integrity Clash 稽核、watermark soft binding）→ Round 2/3 被 D（零成本繞過）、C（容量歸零）、A/G/H（scoop 風險）打出三個結構性事實，於 Round 3 全面改窄：Integrity Clash 降為稽核模組、soft binding 改為索引構造、社會福祉宣稱從「防轉傳詐騙語音」改為「保護願意簽署的真實內容 + 高風險機構的在場驗證契約」。
- Agent F 曾以「你的社會福祉宣稱與你承認的零覆蓋矛盾、驗證端是誰」重創 B2，但隨即獨立提出「局部正面契約」設計（銀行來電必有綠標、契約範圍內普及率 100%、不依賴社會整體普及）——B 與 F 兩個角色獨立收斂到同構設計，是通過可用性檢驗的最強訊號。
- Agent H 承認 Integrity Clash 的 formal-methods 修正「B 做得比任何純 ML 角色好」，把主導權讓給 B，但明言它「服務查核生態而非阿嬤，不是本問題陳述的推薦主軸」。
- 誠實邊界（B 親自寫進第一頁）：對阿嬤的即時詐騙電話「救不了」；provenance 定義域是「非即時的語音訊息/媒體檔案/關鍵權威來源」。

**5. 實驗規劃**
- **資料集**：與方向二共享真實通道基礎設施（B 認領浮水印 bit-level 存活軸）；C2PA 簽署樣本用 c2patool/c2pa-rs（WAV/MP3 可用，Opus 需月 1 feasibility spike）；AudioSeal/SynthID 開源、Latent-Mark 類 latent-space watermark 作對照組（S4）。
- **Baseline**：AudioMarkBench（NeurIPS 2024）、Özer et al.（Interspeech 2025）的重錄協定作對照，劃清界線。
- **方法步驟**：(i) 真實電信通道矩陣上量 C2PA manifest 容器存活 + 傳統 vs latent watermark 的 bit-level I(embedded;recovered)；(ii) 各通道對三層訊號的良性自然去同步率；(iii) 索引式 soft binding 端到端 demo（簽署→平台轉檔→無 metadata 復原並驗證）；(iv) 帶層間依賴證據圖的稽核協定，對 strip-to-evade/mark-to-frame/選擇性存活/局部剪接移植攻擊做安全評估。
- **評估指標**：bit-level 存活率、局部剪接最小可偵測粒度 vs 合法片段轉發誤警率（兩條曲線交叉點＝構造的誠實能力邊界）、稽核協定對耦合攻擊的 robustness、#6 五目標對照表。
- **消融**：索引 vs payload 構造在低容量通道的有效資訊量；時序鏈式 vs 單一 perceptual hash 對移植攻擊的抵抗；latent vs 傳統 watermark 在 neural codec 通道的存活差。

**6. 一年時程表**
- 月 0：IRB + 法律 + 工具鏈 feasibility spike（任一元件不可用即啟動備案）。
- 月 1–3：量測基線（真實通道 watermark/manifest 存活）——保底可發表產出。
- 月 4–6：依容量設計索引式編碼 + 時序鏈式綁定。
- 月 7–9：transparency log 原型 + 端到端 demo + 層間依賴稽核。
- 月 10–12：安全評估（D 的攻擊清單）+ Article 50 政策審計 + C2PA audio profile 建議、寫作。

**7. 真實情境部署路徑**
不救阿嬤的即時電話（B 舉白旗），但救 F 的另兩個人物：上班族（LINE 語音訊息在 provenance 可達域內，機構簽章契約 + 銀行 App 內驗證，不要求 LINE 整合、不踩平台紅線）、選民（查核組織的來源驗證工具、真錄音被誣陷時的自證清白）。應用故事採 F 的局部正面契約：高風險機構承諾其語音必簽、驗證入口在機構自己的 App。

**8. 社會福祉貢獻**
拆解「有簽章＝真」的話術（#6 指出這正是民眾最易受騙處）；給標準與立法者第一份 Article 50 可讀性審計與 C2PA audio profile 修補建議；給高風險機構一個不依賴社會整體普及率的在場驗證構造。負面結果（電話通道全滅）即政策級發表價值。

**9. 風險與備案**
最大風險：audio C2PA 工具鏈成熟度（Opus soft binding 參考實作不成熟）。備案（B 與 H 一致）：manifest 層降級為「依 v2.4 spec 自行實作最小驗證」，論文重心移向 watermark×detector 雙訊號一致性 + 存活量測。次要風險：與方向二高度共享基礎設施——若同一實驗室同時做兩題須明確分工（方向二＝量測/benchmark，方向五＝構造/政策/稽核協定）。索引式 soft binding 若被更聰明的攻擊繞過，失敗模式仍是「帶警示狀態的檔案」或「無憑證檔案」而非「乾淨假憑證」——安全失敗模式在修正後仍成立，範圍更窄、陳述更精確。

---

## 三、五方向比較表

評分 1–5（5 最佳）。novelty / 一年可行性 / 資料集可得性 / 發表潛力四欄取用 Agent H 於 Round 2 的排名表評分並註明調整；「真實情境影響力」一欄為主持人新增（H 原表未含此軸），依三個把關角色的判定綜合評定。

| 方向 | novelty | 一年可行性 | 資料集可得性 | 真實情境影響力* | 發表潛力 |
|------|:---:|:---:|:---:|:---:|:---:|
| 一、誠實棄權 + 警告 UX + 受騙率 | 3.5 | 4 | 5 | **4.5** | 4 |
| 二、真實通道存活 benchmark | 3.5 | 3† | 4† | **3** | 4 |
| 三、Adaptive-Laundering 攻擊成本地圖 | 4 | 4 | 4 | **2.5** | 4 |
| 四、Active Liveness Probing（重建版） | 3† | 3† | 3 | **3** | 3 |
| 五、Provenance 可達性地圖 + 政策審計 | 3.5 | 3 | 4 | **2.5** | 3.5 |

**主持人對 H 評分的調整說明：**
- **†方向二「一年可行性」由 H 原本的 2.5 上修為 3、「資料集可得性」由 2 上修為 4**：採納 Agent G 於 Round 3 的反駁——法律風險已由通保法 §29 查證排除（T2）、MVP 分階段設計降低工程風險、且語料是自建而非依賴拿不到的外部資源（H 原本的 2 分適用於「依賴外部資料集」的題目，對自建語料是兩格重複扣分）。
- **†方向四「novelty」與「一年可行性」由 H 原本墊底的 2.5/2.5 各上修為 3**：H 的墊底評分針對的是「做一個 challenge-response 系統」（D-CAPTCHA 已做），但 Agent E 於 Round 3 把定位重構為「對既有防線做真實通道 + relay 壓力測試 + OOD 壓力源重定義」，並砍掉自建即時平台與 user study（交給方向一）——重構後 novelty 錨點與可行性都提升。仍維持相對低分以反映它是全場最擁擠、被攻最慘的領域。
- **真實情境影響力**：方向一最高（唯一直接量測受騙率、對上班族「可以」）；方向二/四中等（前者是上游證據基礎、後者機構端攔截面寬但 relay 殘留）；方向三/五偏低（前者是「少害她」的品管關而非直接救人、後者對阿嬤「救不了」只覆蓋上班族/選民與政策層）。

---

## 四、給作者的建議

**如果只能選一個，選方向一：會誠實棄權的偵測器 × 壓力測試警告 UX × 受騙率量測。**

**為什麼**：它是這場八人、三輪、二十四份文件的辯論裡，唯一被七個角色（A、C、D、E、F、G、H）在最終推薦中都列為推薦一的方向，而且三個把關角色的判定罕見地一致——**紅隊 D 主動推薦一個防禦方案**（「你沒有假裝擋住我，只是不在你擋不住的地方發出確定的聲音」）、**民眾 F 判定它是阿嬤那一行最接近『可以』的方向、上班族情境直接『可以』**、**教授 H 列為首選**（「全場唯一能指著數據說『這個設計讓受騙率從 X 降到 Y』的題目」）。它同時滿足問題陳述的全部硬性要求：直接降低受騙機率（唯一把「受騙率」設為 primary outcome）、對社會福祉有貢獻（產出可引用的部署準則與 alarm-fatigue 閾值）、一年做得完（元件全現成、不訓大模型、每階段有不依賴 IRB 的保底產出）。它也對這個領域最深的兩堵牆免疫：不與生成器軍備競賽（貢獻是評估框架與人機分工原則，不隨 ElevenLabs 版本過期，Agent G 的四輪歷史循環批判對它無效），也不依賴任何未兌現的長期賭注（憑證普及、延遲軟肋、平台配合）。

**第一步先做什麼**：**月 0 立刻送 IRB**（H 反覆強調這是最常見的碩士生時程殺手），同時並行啟動月 1–4 的「shift-aware calibration benchmark」——復現 AASIST / wav2vec2 / RawNet2 三個偵測器，在 in-domain / unseen-generator / unseen-channel / 疊加四種條件下量 baseline 的 ECE 與 risk-coverage 曲線。這一步的產出本身就是一篇可獨立發表的 benchmark（保底半篇論文，不依賴 IRB），也是後續所有棄權機制比較與 confident-real 對抗評估的地基。把 Agent D 送的那句話刻在評估協定第一行：**對抗評估的主目標函數是 `max P(confident-real | fake)`，不是 risk-coverage curve**——因為攻擊者要的不是讓系統棄權，是讓系統自信地替他背書。

**若行有餘力做第二題或有第二位學生**：選方向三（攻擊成本地圖），它是方向一驗收「棄權不被繞過」的必要對抗評估層，兩者合成一條完整的紅藍對抗證據鏈（偵測器誠實棄權 → 攻擊成本地圖證明棄權不被繞過 → 警告 UX 量測受騙率）。方向二（真實通道 benchmark）則是可選的「unseen-channel 真實素材」基礎設施，但工程工時較重，適合工程能力強的學生。

---

*本統整完成於 2026-07-13，依 00-problem-statement 交付的唯一考題——「降低那個接電話的人受騙的機率」——為最終裁決標準。*
