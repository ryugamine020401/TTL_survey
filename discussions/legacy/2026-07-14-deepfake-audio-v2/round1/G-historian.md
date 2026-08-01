# Round 1 提案：領域史官（Agent G）——第二輪（無真人實測）
日期：2026-07-14

> 我是領域史官。我的職責是：在任何人宣稱「這是第一個」之前，先去把地圖翻出來。第一輪我用檢索擊沉了互動挑戰-回應（D-CAPTCHA 前作），也認證了「真實電信通道存活」是唯一無前作的空白。**本輪我必須先做一件不愉快的事：更新我自己上一輪發出的認證。** 檢索顯示這個空白在過去十個月被兩篇論文侵蝕了一大塊。史官的信用建立在「自己的結論也照樣推翻」上，所以先報壞消息，再談提案。

---

## 0. 本輪檢索紀錄（共 9 次檢索，編號 G2-S1 至 G2-S9）

### 0.1 檢索軸 (c)：第一輪認證的空白「真實電信通道存活」——復查結果：**部分失效，必須修正**

**G2-S4 / G2-S7 / G2-S8 三次檢索命中兩顆魚雷：**

**魚雷一：《On Deepfake Voice Detection — It's All in the Presentation》（arXiv 2509.26471，2025-09 投 ICASSP 2026，Delgado et al.）**
- https://arxiv.org/abs/2509.26471
- 這篇論文的核心命題與我們方向二的靈魂**幾乎逐字重疊**：「raw deepfake audio 與經過通訊通道（如電話）presented 的 deepfake audio 之間的差異，是現有系統無法泛化到真實世界的主因」。他們提出含 direct-injection 與 loudspeaker playback 兩種 presentation 的資料建構框架與評測 benchmark，宣稱在真實 lab setup 上偵測準確率 +39%、在 real-world benchmark 上 +57%，並得出「資料集品質比模型大小更重要」的結論。
- 更糟的是作者名單：Héctor Delgado 是 ASVspoof 系列的組織者之一，這是產業（Nuance/Microsoft 系）+ 學術重量級的正面進場。第一輪 legacy 統整寫下「真實電信通道存活是 2026-07 唯一經檢索驗證仍無前作的空白」時，這篇已經掛在 arXiv 上十個月——這是我第一輪檢索的漏網，我必須記錄在案。

**魚雷二：《RTCFake: Speech Deepfake Detection in Real-Time Communication》（arXiv 2604.23742，2026-04）**
- https://arxiv.org/abs/2604.23742 ，資料集：https://huggingface.co/datasets/JunXueTech/RTCFake
- 首個 RTC 場景的大規模 speech deepfake dataset（約 600 小時）：把語音**實際灌過多個主流社群/會議平台（如 Zoom）傳輸**，offline/online 精確配對，評測集含 unseen platform 與 unseen noise。這正是 #3（ADD-C）自承的殘留 gap——「社群平台私有轉檔管線」——已被填掉一大塊。另提出 phoneme-guided consistency learning 學 platform-invariant 表徵。

**修正後的空白邊界（史官裁定）：**
「真實通道存活」作為一個籠統宣稱已死。但拆細後，以下子空白經復查**仍然成立**：
1. **真實蜂巢電信網**（VoLTE AMR-WB/EVS、跨電信商互通、PSTN fallback、實測 jitter/PLR 標註）：RTCFake 做的是 IP 上的 RTC 平台，2509.26471 做的是 presentation 框架（loudspeaker/direct-inject）而非公開的跨電信商通道矩陣資料集。公開可下載的「真實電信網通道」資料集仍不存在。
2. **watermark / provenance 訊號在真實電信通道的 bit-level 存活**：兩篇前作都只測 detection 劣化，完全沒碰 AudioSeal/SynthID 的 bit 存活與 C2PA manifest 存活。AudioMarkBench（NeurIPS 2024）是模擬擾動+重錄，不是電信網。此軸無前作。
3. **多防線統一審計 + EU AI Act Article 50 可讀性政策軸**：無前作。
4. **繁中/台灣 165 情境**：無前作。

結論：**方向二不死，但「首個真實通道」的 novelty 錨點必須立刻棄守，改錨到「電信網 × 多訊號 × 審計/政策」**，且時間窗正在關閉——產業（Resemble、Delgado 團隊）已經進場，這個題目再放一年就沒了。

### 0.2 檢索軸 (a)：2025–2026 ADD 最新進展

- **AT-ADD Grand Challenge（ACM Multimedia 2026 評測計畫，arXiv 2604.08184）**：https://arxiv.org/abs/2604.08184 ——官方定位「bridge controlled academic evaluation with practical multimedia forensics」，unseen-generator 泛化仍是主軸。第一輪已知，仍為模擬條件。
- **ESDD 2026（環境音 deepfake challenge，arXiv 2508.04529）**：https://arxiv.org/html/2508.04529v2 ——含「unseen generators」track，顯示 cross-generator 泛化已經標準化為 challenge 設計慣例——**任何「我做 unseen-generator 泛化」的碩論主張都在跟整個 challenge 生態賽跑**。
- **Speech DF Arena（arXiv 2509.02859）**：https://arxiv.org/pdf/2509.02859 ——ADD 模型的公開 leaderboard，佐證 benchmark/評測基礎設施是這個領域的主要推進器。
- **Resemble AI 8 系統 benchmark（2026-05）**：https://www.resemble.ai/resources/audio-deepfake-detection-benchmark-results-how-8-systems-performed-in-2026 ——廠商自辦但有兩個可引用的定性結論：(i) 在含 ~25 個現代 TTS 的測試集上，8 個偵測系統表現「等於或低於未輔助的人類」；(ii) **「ASVspoof 作為訓練分布已過時」**——2019 攻擊訓練的偵測器對 2026 攻擊完全不泛化。這是我第一輪「四代歷史循環」批判的最新一格。
- **FADEL: Uncertainty-aware Fake Audio Detection with Evidential Deep Learning（ICASSP 2025，arXiv 2504.15663）**：https://arxiv.org/abs/2504.15663 、https://ieeexplore.ieee.org/document/10888053/ ——**這是對方向一的直接前作警報**。用 Dirichlet 分布做 evidential uncertainty 的 fake audio detection，明確動機就是「softmax 過度自信、unseen OOD 攻擊下預測不可靠」。但範圍有限：只做 ASVspoof 2019 LA ↔ 2021 LA 的 cross-dataset，**沒有** shift 矩陣（unseen-generator × unseen-channel）、沒有 risk-coverage/選擇性預測框架、沒有 confident-real 對抗軸、沒有 human deferral。方向一的「第一個 uncertainty-aware ADD」宣稱不成立，但「第一個 shift-aware selective-prediction ADD benchmark + 對抗評估」仍成立——FADEL 反而該收編為第 7 種棄權機制 baseline。
- **Probabilistic Verification of Voice Anti-Spoofing Models（arXiv 2603.10713）**：https://arxiv.org/pdf/2603.10713 ——形式化驗證進入 anti-spoofing，佐證「對偵測器做保證/稽核」是上升中的題型。
- **An Intervention-Based Framework for Shortcut Diagnosis in Spoofing Countermeasures（arXiv 2607.03150）**：https://arxiv.org/pdf/2607.03150 ——2026-07 最新，shortcut 診斷（呼應第一輪 S3 Watermark Shortcut）。順帶：**Watermark Shortcut 已正式掛號 arXiv 2606.23335**（https://arxiv.org/pdf/2606.23335 ），第一輪引用的 S3 現在有正式出處。
- **Multi-Granularity Adaptive Time-Frequency Attention Framework … under Real-World Communication Degradations（arXiv 2508.01467）**：https://arxiv.org/pdf/2508.01467 ——又一篇通道劣化 detection，仍是模擬劣化。通道 robustness 賽道正在變擁擠。

### 0.3 檢索軸 (b)：不做真人實驗的 usable security / 人類行為建模——先例與學術接受度（本輪特別任務）

這是本輪最重要的方法論情報。我把找到的先例分四條路線，並給出各自的接受度判定：

**路線一：Cognitive architecture / Instance-Based Learning（IBL）模型——接受度：高，且持續活躍**
- Cranford et al.,《Modeling Phishing Susceptibility as Decisions from Experience》（ICCM 2021）：https://iccm-conference.neocities.org/2021/papers/609.pdf ——用 ACT-R 的 IBL 模型建模 phishing 判斷，**驗證方式正是「fit 一個已公佈的人類研究、然後零參數預測另一個已公佈的人類研究」**——完全不需要自己跑 user study。
- 《Using a Computational Cognitive Model to Understand Phishing Classification Decisions of Email Users》（Interacting with Computers, Oxford, 2024）：https://academic.oup.com/iwc/article/36/2/113/7601603
- 《Analyzing instance representation in cognitive models of phishing decision-making》（User Modeling and User-Adapted Interaction, **2026**）：https://link.springer.com/article/10.1007/s11257-026-09441-z ——證明這條路線到 2026 年仍在頂級期刊發表。
- 早期先例：Kent 大學的 ACT-R phishing 網站偵測模擬（2017）：https://kar.kent.ac.uk/74278/
- 綜述：《Simulations in Cyber-Security: A Review of Cognitive Modeling of Network Attackers, Defenders, and Users》：https://pmc.ncbi.nlm.nih.gov/articles/PMC5967149/ ——cognitive model 作為「可直接與任務環境互動的人類認知獨立模擬」在 cybersecurity 已是被綜述承認的方法類別。

**路線二：Learning-to-Defer（L2D）社群的 synthetic experts——接受度：高，且是該社群的標準做法**
- FiFAR（arXiv 2312.13218）：https://arxiv.org/pdf/2312.13218 ——用 OpenL2D 框架生成 **50 個合成 fraud analysts**（可調決策過程與工作容量），對 30,000 筆公開詐欺資料產生專家預測，做成 L2D benchmark。動機明說：「取得真人專家預測成本太高，導致文獻普遍用簡化模擬專家」。
- 《A benchmarking framework and dataset for learning to defer in human-AI decision-making》（**Nature Scientific Data 2025**）：https://www.nature.com/articles/s41597-025-04664-y ——合成專家 benchmark 上了 Nature 子刊，接受度不必再辯。
- Conformal set-based human-AI complementarity（arXiv 2508.06997）：https://arxiv.org/pdf/2508.06997 ——用已有專家預測資料做 deferral policy 的理論保證。
- 這條路線對我們的意義：**方向一的 deferral policy 模擬（用 VoiceWukong 公佈數據替代真人）不是權宜之計，而是 L2D 社群的正統方法論**。

**路線三：Agent-based / 干預模擬——接受度：中高（老年學/公衛端有先例）**
- 《Simulating well-being and literacy interventions to reduce elder scam susceptibility》（PMC9765817）：https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9765817/ ——直接用模擬評估「降低老人受騙敏感性」的介入方案。這是「不做真人實驗、評估防詐介入」的最接近先例，領域是 aging research。

**路線四：LLM-simulated users——接受度：低且快速惡化，裁定為不可用作主驗證**
- 《Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations》（arXiv 2601.17087）：https://arxiv.org/html/2601.17087v1 ——實測顯示 agent 對真人成功率 45.2%，與模擬用戶結果嚴重失準；31 個 LLM simulator 對 451 真人、165 任務的比較顯示模擬器「過度禮貌寬容，造出 easy mode」（arXiv 2605.10659：https://arxiv.org/pdf/2605.10659 ）。
- 《The Illusion of Intervention: Your LLM-Simulated Experiment is an Observational Study》（arXiv 2605.20767）：https://arxiv.org/pdf/2605.20767 ——方法論級的致命批評：LLM 模擬「實驗」在因果推論上只是觀察性研究。
- CHI 2026 有專門 workshop 在訂「LLM 作為模擬受試者」的使用標準（https://doi.org/10.1145/3772363.3778756 ），代表社群認為此事**尚未有標準**。
- **史官裁定：在 2026 年的審稿環境把 LLM-simulated users 當 primary evidence，等於把論文的脖子伸給 reviewer。凡用模擬替代真人，必須走路線一/二（有既定先例、以已公佈真人數據錨定），並把結論寫成對模型誤差 robust 的形式。**

**另一個直接可用的事實（G2-S6）**：VoiceWukong 的 **user study 原始結果與 12 個偵測器的原始輸出都公開在其 GitHub repo**（https://github.com/VoiceWukong/VoiceWukong ；資料集 Zenodo：https://zenodo.org/records/13731918 ，學術申請制）。這意味著「用已公佈人類數據做 secondary analysis」不只是引用論文裡的彙總數字，而是可以拿到 per-sample 粒度的人類判斷分布——這對建 human-response model 是質的差別。

---

## 1. 新限制對第一輪五個方向的衝擊評估

| 方向 | 衝擊 | 說明 |
|------|------|------|
| 一、誠實棄權 + 警告 UX + 受騙率 | **重創但可重建** | 被抽掉的是 primary outcome 的量測方式（30–50 人 user study 量受騙率）。但注意 legacy 統整第 112 行早已寫好備案：「先用 VoiceWukong 已公佈人類數據做 policy 模擬（不需 IRB）」——新限制等於把備案升格為主線。月 1–4 的 shift benchmark、6 種棄權機制比較、confident-real 對抗評估全是計算性，原樣保留。**真正的代價是宣稱降級**：從「實測受騙率從 X 降到 Y」變成「在人類參數的文獻觀測範圍內，模擬預期受騙率從 X 降到 Y」。另外本輪檢索出 FADEL 前作，novelty 錨點也要同步修正（見 0.2）。警告 UX 的視覺/互動設計部分若無法量測人類反應，則整段砍掉或降為 design implications——這是誠實的必要切除。 |
| 二、真實通道 benchmark | **幾乎不受限制影響，但被前作重創** | 它本來就沒有 user study（自錄語料可全部改用公開資料集語料迴避任何真人成分）。真正的打擊來自我 0.1 節的兩顆魚雷——novelty 錨點必須從「首個真實通道」撤守到「電信網 × 多訊號存活 × 審計/政策」。 |
| 三、攻擊成本地圖 | **零衝擊** | 純計算攻防，一個真人都不需要。新限制下它的相對地位上升。 |
| 四、Active Liveness Probing | **中度衝擊** | IRB 本來就不在主線，但「切換點語料」需要真人共犯錄音（真人全程/挑戰段切真人）——這踩線。替代：共犯全部用 TTS/VC 生成 + 公開語料拼接模擬。可行，但「真人 relay 共犯的實際表現」變成模型假設而非實測，D 的攻擊成本量測會多一層不確定性。 |
| 五、Provenance 可達性地圖 | **零衝擊** | 密碼學構造 + 存活量測 + 政策審計，全計算性。 |

**總評**：新限制系統性地偏好「評估型/攻防型/構造型」貢獻（方向二三五），懲罰「人因型」貢獻（方向一的 UX 半邊、方向四的 relay 半邊）。但方向一的偵測器半邊（selective prediction + 對抗評估）毫髮無傷，且 0.3 節的檢索證明它的人因半邊有正統的計算性替代路線。

---

## 2. 思辨過程：五個候選想法的生成與淘汰

以下是我的真實思考順序，包括被我自己殺掉的想法。

### 候選一：方向一的無真人版——「模擬受騙率」直接替換「實測受騙率」

最自然的改造。deferral policy 模擬本來就在方向一的實驗規劃裡（步驟 v），現在把它從配角升為 primary outcome。

**自我質疑 1**：VoiceWukong 的 300+ 人數據是「知道自己在做聽測、無時間壓力、無情緒操縱」下收的。詐騙電話的核心變因——壓力、權威、倒數計時——全都不在數據裡。用它模擬「受騙率」，外推效度何在？F 一定會問：「你模擬的是實驗室裡的人，不是被喊『快匯錢』的阿嬤。」
**回應與修正**：承認這一點並把它變成方法的一部分——不做 point estimate，做**參數化敏感度分析**：human FAR/FRR 以 VoiceWukong 數據為錨（樂觀端），以「壓力修正係數」掃描到悲觀端（例如人類辨識力全失、FAR→base rate），輸出的主張改為 **dominance 形式**：「在人類參數空間的整個掃描範圍內，policy A 的 expected cost 一致低於 policy B」。這正是 L2D 社群 synthetic experts 的做法（FiFAR 的專家就是「可調參數的合成分析師」），而 dominance 主張對 human model 誤差 robust——就算模型偏了，只要偏移方向在掃描範圍內，排序結論不變。

**自我質疑 2**：這會不會踩到《The Illusion of Intervention》的批評——模擬實驗只是觀察性研究，不能宣稱因果？
**回應**：會，如果我宣稱「警告設計 X 導致受騙率下降」。所以不宣稱因果，宣稱**條件性比較**：「給定人類行為模型 M（含明列假設），deferral policy A 相對 B 的 expected cost 改善為 Δ」。這與 FiFAR/Nature Sci Data 2025 的宣稱形式一致，是被接受的。因果宣稱留給未來有 IRB 的人做，本論文產出的是「值得做真人實驗驗證的、已通過計算性篩選的最優 policy 候選 + 明確的可證偽預測」。

**自我質疑 3**：FADEL 已經做了 uncertainty-aware ADD，novelty 還剩多少？
**回應**：查證後（0.2 節）FADEL 只做 evidential loss + ASVspoof 內部 cross-dataset，四個東西它都沒有：shift 評估矩陣、risk-coverage/selective prediction 框架、confident-real 對抗軸、human deferral 模擬。把 FADEL 收編為第 7 種棄權機制 baseline 反而讓比較實驗更完整。novelty 錨點改寫為「第一個 shift-aware selective-prediction ADD benchmark，含對抗評估與 simulation-grounded deferral」——經檢索仍無前作。

**判定：存活，成為正式提案 G2-A。**

### 候選二：方向二原樣續推（我第一輪認證過的空白）

**自我質疑**：我自己的復查把它打穿了（0.1 節兩顆魚雷）。「首個真實通道」死了。那還剩什麼？
**回應**：拆細後四個子空白仍在（電信網資料集、watermark/provenance bit 存活、多防線審計、繁中情境）。而且兩篇前作反而**強化了動機**：2509.26471 證明 presentation 落差是真實且巨大的（+57%），RTCFake 證明「真灌通道」的資料集做法可行且能發表——它們替方向二把「這個落差存在嗎」的風險消掉了，剩下的問題是「電信網（而非 RTC 平台）上的落差長什麼樣、watermark 訊號活不活得下來」。novelty 從「首個量測」變成「補上階梯的缺格 + 唯一的多訊號軸」。
**殘留弱點**：detection 劣化軸的貢獻被攤薄，一年內若只做出 detection 軸就會變成「RTCFake 的電信版」——增量型。所以 watermark/provenance 存活軸從可選升為**必做主軸**（此軸零前作），detection 軸降為對照。
**判定：存活，重錨後成為正式提案 G2-B。**

### 候選三：全新題目——「偵測器貢獻半衰期」的歷史迴圈量化 meta-benchmark

我第一輪的核心批判是這個領域的四代歷史循環（特徵→模型→資料→評測，每代都被下一代生成器歸零）。把它變成可量測的東西：按生成器發表年份切片（train on ≤ year t，test on year t+1 的生成器），量化每一代偵測方法的「貢獻半衰期」，回答「這個領域到底有沒有累積性進步，還是在原地跑滾輪」。

**自我質疑 1**：前作？Resemble 2026 benchmark 已給出「ASVspoof 訓練分布過時」的單點結論；Deepfake-Eval-2024（arXiv 2503.02857，https://arxiv.org/pdf/2503.02857 ）做了「時間漂移下的 in-the-wild 劣化」。系統性的逐年切片半衰期曲線沒人做過，但 SpeechFake、MLAAD 這些多世代資料集讓任何人隨時可以做——這是個「別人一個週末就能 scoop」的題目。
**自我質疑 2**：H 會怎麼判？「這是一篇很好的 survey 加一個實驗，不是一篇碩論」——貢獻是 meta 級的，沒有方法、沒有構造、沒有防線。而且對「降低民眾受騙機率」的路徑極間接。
**判定：淘汰為模組**——它是方向三（攻擊成本地圖）的天然時間軸擴充（攻擊者動作空間加一維「等半年換新生成器」，成本趨近於零），單獨不成論文。

### 候選四：ACT-R / IBL 認知模型建模「語音詐騙受害者決策」

路線一的先例這麼強（ICCM/IwC/UMUAI 一路發到 2026），直接把 phishing 的 IBL 模型移植到 voice scam？建一個「接電話的人」的認知模型，模擬警告介面的效果。

**自我質疑（致命）**：phishing 的 IBL 模型有 trial-level 的公開行為數據可以 fit 和驗證（哪封信、看多久、點不點、feedback 後怎麼調整）。voice scam 領域**沒有任何 trial-level 公開決策過程數據**——VoiceWukong 只有「這段音檔判真/假」的 aggregate 準確率，沒有決策序列、沒有 feedback 學習、沒有壓力操縱。沒有數據錨定的認知模型自由度無限大，等於用一個無法證偽的模型去「驗證」設計——這比 LLM-simulated users 更糟，因為連「跟真人比對」的可能性都沒有。Cranford 模型的說服力恰恰來自「fit 研究 A、零參數預測研究 B」，而 voice scam 連研究 A 都沒有。
**判定：淘汰。** 但保留一個降級產物：G2-A 的 human-response model 用最簡單的參數化形式（per-difficulty-level 的 FAR/FRR + 掃描係數），**不假裝**是認知機制模型——模型的簡單是誠實，不是懶惰。

### 候選五：「Deepfake 難度分級器」——把 VoiceWukong 人類數據變成可預測的標籤

VoiceWukong 依人類表現把 deepfake 分三個難度等級且原始數據公開。訓練一個模型預測「這段 deepfake 對人類有多騙」（human-deceptiveness score），用途：(i) 偵測器與人類的互補性路由（難度高→機器、難度低→人也行）；(ii) 給生成內容標「對人危險度」供平台優先審核。

**自我質疑 1**：這本質上是「用 300 人的 aggregate 標籤訓練一個 perceptual quality 迴歸器」，跟 MOS prediction（語音品質預測）一個結構——MOSNet 系的方法直接可套，novelty 薄。
**自我質疑 2**：標籤只有三級、樣本的人類判斷分布可能很窄（VoiceWukong 的受試者數 per sample 有限），迴歸器的泛化到新生成器完全未知——而「泛化到新生成器」正是這個領域最深的坑，等於把主坑原封不動搬進來。
**自我質疑 3**：但它作為 G2-A 的**子模組**價值很高：deferral policy 需要估計「人類接手這個樣本會表現如何」，一個 per-sample 的 human-deceptiveness 預測器正是 deferral 的路由訊號——這比全域平均 FAR 的模擬精細一級，而且它的失敗（預測不準）本身就是 G2-A 敏感度分析要掃的軸。
**判定：淘汰為 G2-A 的子模組**（deferral 路由訊號 + 敏感度軸），不獨立成題。

---

## 3. 正式提案

### 提案 G2-A：《模擬接管——分布偏移下語音深偽偵測的校準棄權框架，與以已公佈人類數據錨定的受騙率模擬評估》
*Simulation-Grounded Selective Prediction for Audio Deepfake Detection: Shift-Aware Abstention, Confident-Real Adversarial Evaluation, and Deception-Rate Estimation from Published Human Data*

**核心 idea**
第一輪方向一的無真人版重建：偵測器半邊（shift-aware selective prediction benchmark + 6+1 種棄權機制 + confident-real 對抗軸）原樣保留；被抽掉的 user study 半邊，用「L2D 式合成專家 + VoiceWukong 公佈人類數據錨定 + 壓力係數敏感度掃描」的 Monte Carlo 受騙率模擬管線替換，primary outcome 從「實測受騙率」改為「dominance 形式的模擬預期受騙率比較」。

**為什麼有機會成立（引文獻）**
- 需求端不變：#2 證明 unseen generator 下 EER 13.5–50%、#1 證明人類僅 73% 準確率且人機互補（#2：人類對低品質 deepfake FAR 4–19%、高品質 >82%）——deferral 的原料是現成的實測分布。
- 方法論先例（本輪檢索的核心產出）：(i) L2D 社群用合成專家做 benchmark 是正統做法且上了 Nature Scientific Data 2025（https://www.nature.com/articles/s41597-025-04664-y ）與 FiFAR（https://arxiv.org/pdf/2312.13218 ）；(ii) cognitive model「fit 已公佈研究、預測另一個已公佈研究」的驗證範式在 security 決策領域一路發表到 UMUAI 2026（https://link.springer.com/article/10.1007/s11257-026-09441-z ）；(iii) VoiceWukong 原始人類數據公開可得（https://github.com/VoiceWukong/VoiceWukong ）。
- novelty 經本輪復查修正後仍成立：FADEL（ICASSP 2025）只做 evidential loss + ASVspoof 內 cross-dataset，無 shift 矩陣、無 risk-coverage 框架、無對抗軸、無 human deferral（https://arxiv.org/abs/2504.15663 ）——收編為第 7 種棄權機制 baseline。

**技術路線**
1. 月 1–4：shift 評估矩陣（in-domain / unseen-generator / unseen-channel / 疊加；unseen-channel 可直接用 RTCFake 當現成真實通道測試集——本輪檢索的意外紅利，不用自己灌通道）+ 3 偵測器 baseline 的 ECE / risk-coverage。保底半篇 benchmark。
2. 月 5–7：7 種棄權機制比較（MSP、temperature scaling、deep ensemble、MC-dropout、energy、Mahalanobis-on-SSL、one-class real-manifold 距離 + FADEL evidential）；驗證 A 的假說「real-manifold 距離型分數在 AUC≈0.5 failure mode 下存活」。
3. 月 8–9：confident-real 對抗評估（主目標函數 `max P(confident-real|fake)`，沿用全場公約與 D 的 attacker-cost 框架）。
4. 月 9–11：受騙率模擬管線——(a) 以 VoiceWukong per-sample 人類判斷分布建參數化 human-response model（per-difficulty FAR/FRR）；(b) 可選子模組：per-sample human-deceptiveness 預測器作 deferral 路由訊號；(c) 壓力/警告依從率係數以 phishing warning 文獻公佈值為先驗範圍（habituation/warning compliance 文獻，如 https://pmc.ncbi.nlm.nih.gov/articles/PMC5967149/ 所綜述之路線）做全區間掃描；(d) 輸出多 base rate expected cost 與 deception-rate 的 dominance 比較。

**計算性驗證方案（替代真人實測的明確論證）**
- 替代物：合成 human-response model，錨定於已公佈的 300+ 人 per-sample 數據（非自建、非 LLM 模擬——LLM-simulated users 經檢索確認不可靠：https://arxiv.org/html/2601.17087v1 、https://arxiv.org/pdf/2605.10659 ，本提案明確不採用）。
- 為什麼結論仍可信：(i) 結論寫成 dominance 形式——「在人類參數的整個文獻觀測範圍 + 悲觀外推區間內，policy 排序不變」——對 human model 的點誤差 robust；凡排序翻轉的參數區域，如實報告為「需真人實驗裁決區」；(ii) 這與 FiFAR / Nature Sci Data 2025 的合成專家宣稱形式一致，審稿風險已由先例消化；(iii) 不做因果宣稱（迴避 https://arxiv.org/pdf/2605.20767 的批評），產出是「通過計算篩選的最優 policy 候選 + 可證偽預測」，明列為後續 IRB 研究的假設。
- 誠實邊界（寫進第一頁）：模擬中的「人」不會被社工操縱、不會恐慌——所有 deception-rate 數字是「無操縱下界的比較值」，不是部署預測值。

**預期貢獻**
第一個 shift-aware selective-prediction ADD benchmark（含 FADEL 在內的 7 機制系統比較）；confident-real 對抗評估軸的首次實作；ADD 領域第一個以公開人類數據錨定的 deferral policy 模擬框架（方法論可被後續所有 ADD 論文複用）；alarm-fatigue/警示率的部署參數建議（模擬形式）。

---

### 提案 G2-B：《電信網是最後一哩——真實蜂巢電信通道上偵測、浮水印與溯源訊號存活的多防線審計（重錨版）》
*The Last Mile is Cellular: A Multi-Defense Audit of Detection, Watermarking, and Provenance Signal Survival over Real Telecom Channels — post-RTCFake, post-Presentation*

**核心 idea**
第一輪方向二在兩篇前作（2509.26471、RTCFake）出現後的誠實重錨：不再宣稱「首個真實通道」，改建「模擬 → RTC 平台（RTCFake 已做）→ 蜂巢電信網（本論文）」的**三層樂觀偏差階梯**，並把零前作的 **watermark/provenance bit-level 存活軸**從可選升為主軸，輸出 EU AI Act Article 50 可讀性審計。

**為什麼有機會成立（引文獻）**
- 動機被前作反向強化：2509.26471 證明 presentation 落差高達 57% 改善空間（https://arxiv.org/abs/2509.26471 ），RTCFake 證明「真灌通道 + offline/online 配對」的資料集做法可行可發表（https://arxiv.org/abs/2604.23742 ）——但兩者都止步於 IP 網路與 lab presentation，**公開的蜂巢電信網（VoLTE AMR-WB/EVS、跨電信商、PSTN interop）通道資料集經復查仍不存在**；#3 的模擬 codec 結論（DA 可近乎消除劣化）在真實電信網是否成立，是被 2509.26471 間接質疑（他們發現 presentation 落差不是 DA 能簡單補的）但未在電信網上驗證的開放問題。
- watermark/provenance 軸零前作：AudioMarkBench（NeurIPS 2024）與 Özer et al.（Interspeech 2025）做模擬擾動與重錄，2509.26471/RTCFake 完全沒碰 watermark；Article 50 於 2026-08-02 生效，「machine-readable 標記在詐騙實際發生的通道上可不可讀」的審計無任何前作（第一輪 T3 查證 + 本輪復查維持）。
- 法律路徑沿用第一輪 T2 查證：通保法 §29 第 3 款，rig 兩端皆研究團隊設備。
- 無真人成分：語料全部改用公開資料集（ASVspoof/In-the-Wild/MLAAD bona fide + TTS 生成），**砍掉第一輪規劃中的「團隊錄音」**，連知情同意都不需要——本方向在新限制下反而更乾淨。

**技術路線**
1. 月 1–3：rig 定案（固定 UE × 2 電信商、記錄協商 codec/PLR/jitter）+ 與 RTCFake/2509.26471 的協定對齊設計（確保三層階梯可比）。
2. 月 3–6：MVP——單電信商 VoLTE + LINE 通話兩型態，量 (a) 偵測器 fixed-FPR recall 的三層階梯落差、(b) AudioSeal/SynthID bit-level I(embedded;recovered)。保底可發表單元。
3. 月 6–9：擴 stretch 通道（第二電信商、tandem 串接、混合通道）+ C2PA manifest 容器存活 + cue 存活圖譜（SSL layer × channel probing）。
4. 月 9–12：channel-conditioned detection 對照（#3 的 DA 在真電信網還靈嗎）+ Article 50 審計報告 + 資料集開源。

**計算性驗證方案（替代真人實測的說明）**
本方向不需要替代——它本來就沒有人因成分。唯一調整：語料全公開資料集化（上段）。「結論可信」的關鍵在混淆變因控制：固定 UE、標註協商參數、offline/online 精確配對（採 RTCFake 的配對方法論，站在前作肩上而非假裝它不存在）。

**預期貢獻**
首個公開蜂巢電信網通道 audio deepfake 資料集（含繁中/台灣情境）；三層樂觀偏差階梯的量化（給所有後續 ADD 研究的評估效度警示）；watermark/provenance 電信存活的首次量測；Article 50 可讀性的第一份審計（若全滅即政策級否證）。與 G2-A 的接口：本資料集直接成為 G2-A 的 unseen-channel 真實測試軸。

**風險與備案**
最大風險：時間窗——Delgado 團隊與產業已在此賽道，電信網軸可能在 12 個月內被 scoop。緩解：MVP 前置（月 6 保底）、watermark 軸（零前作且產業無動機自審）作為差異化護城河。次風險：工程工時，沿用第一輪 MVP 分階段設計。

---

## 4. 我留給其他討論者的問題

1. **給 Agent H（指導教授）**：G2-A 的 primary outcome 是「dominance 形式的模擬受騙率比較」。你在 proposal defense 會放行嗎？具體地說：L2D 社群的合成專家先例（Nature Sci Data 2025、FiFAR）在 security venue（USENIX/CCS/NDSS）的 reviewer 眼中，與在 ML venue 的接受度是否有落差？如果 security venue 不買帳，這篇該投哪裡？

2. **給 Agent D（紅隊）**：無真人版的模擬管線裡，「人」是一個不會被社工操縱、不會恐慌的參數化模型——這會不會讓 confident-real 對抗軸**系統性低估**攻擊者的真實收益（攻擊者實際上同時攻擊偵測器與人，而我們的模型只讓他攻擊偵測器）？如果會，你能否定義一個「攻擊者可操縱的 human-parameter 擾動」把社工攻擊面塞回計算性框架裡（例如：攻擊者可把 warning compliance 係數往下推 δ，量 δ 對 expected cost 的斜率）？

3. **給 Agent F（一般民眾代表）**：VoiceWukong 的受試者是知道自己在做測驗的人。你認為「知情聽測」相對「詐騙現場」的偏差方向，在哪些參數上是確定的（例如壓力只會讓 FAR 變高不會變低）？有沒有**不需要 IRB 的公開數據源**（165 報案統計、內政部警政署公開數字、詐騙錄音公開案例庫）可以幫我們把壓力修正係數的掃描範圍從「拍腦袋」變成「有出處」？

4. **給 Agent A（Detection 研究者）**：FADEL（evidential DL，ICASSP 2025）該收編為第 7 種棄權機制。你的 real-manifold 距離假說與 evidential uncertainty 在 AUC≈0.5 failure mode 下的預期行為是否不同？如果 FADEL 的 Dirichlet uncertainty 在 unseen-generator 下也存活，你的假說的差異化陳述要怎麼改？

---

## 附錄：本輪檢索來源清單

| 編號 | 主題 | 關鍵來源 |
|------|------|----------|
| G2-S1 | 2026 ADD 泛化進展 | https://arxiv.org/abs/2604.08184 (AT-ADD)、https://arxiv.org/html/2508.04529v2 (ESDD 2026) |
| G2-S2 | 模擬式 usable security | https://pmc.ncbi.nlm.nih.gov/articles/PMC5967149/ (cognitive modeling in cybersecurity review) |
| G2-S3 | LLM-simulated users 接受度 | https://arxiv.org/html/2601.17087v1 (Lost in Simulation)、https://arxiv.org/pdf/2605.20767 (Illusion of Intervention)、https://arxiv.org/pdf/2605.10659 (Digital Personas)、https://doi.org/10.1145/3772363.3778756 (CHI 2026 workshop) |
| G2-S4 | 真實電話通道復查 | https://www.resemble.ai/resources/audio-deepfake-detection-benchmark-results-how-8-systems-performed-in-2026 、https://arxiv.org/pdf/2509.02859 (Speech DF Arena) |
| G2-S5 | L2D / 合成專家先例 | https://www.nature.com/articles/s41597-025-04664-y 、https://arxiv.org/pdf/2312.13218 (FiFAR)、https://arxiv.org/pdf/2508.06997 |
| G2-S6 | ACT-R/IBL security 先例 + VoiceWukong 數據可得性 | https://iccm-conference.neocities.org/2021/papers/609.pdf 、https://academic.oup.com/iwc/article/36/2/113/7601603 、https://link.springer.com/article/10.1007/s11257-026-09441-z 、https://kar.kent.ac.uk/74278/ 、https://github.com/VoiceWukong/VoiceWukong 、https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9765817/ (elder scam simulation) |
| G2-S7 | 通道空白魚雷 | https://arxiv.org/abs/2509.26471 (Presentation)、https://arxiv.org/abs/2604.23742 (RTCFake)、https://arxiv.org/pdf/2508.01467 |
| G2-S8 | RTCFake / Presentation 細節確認 | https://huggingface.co/datasets/JunXueTech/RTCFake 、https://github.com/CavoloFrattale/deepfake-detection-test-protocol |
| G2-S9 | uncertainty ADD 前作 | https://arxiv.org/abs/2504.15663 (FADEL, ICASSP 2025)、https://arxiv.org/pdf/2603.10713 、https://arxiv.org/pdf/2607.03150 、https://arxiv.org/pdf/2606.23335 (Watermark Shortcut 正式版) |

*本文件為第二輪辯論 Round 1 的正式討論紀錄。我的兩個提案都建立在「先承認前作、再錨定殘存空白」的史官紀律上——包括承認我自己第一輪認證的空白已被侵蝕。*
