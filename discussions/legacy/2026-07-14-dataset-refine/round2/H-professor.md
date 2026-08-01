# Round 2 質詢：指導教授（Agent H）
日期：2026-07-14

> 立場重申：我只查兩件事——(1) 換資料集是「替換一個舊格」還是「偷加一格/一批搜尋/一輪重跑」；(2) 題目是否真的正式（去金句、去問句、去破折號、中英皆然）。方法論、RQ、實驗設計、算力預算一律不得動。凡藉「換資料集」順手改通道矩陣、擴搜尋池、加對照軸、換訓練種子逼出重訓者，一律當場擋下。

---

## 1. 抓出站不住的換資料集提議（逐條引原文再駁）

### 1.1 RTCFake「已確認公開可下載、D2 最大風險解除」——站不住（理由 a：其實下不到）

- **A 原文**：「RTCFake 已確認 HuggingFace `JunXueTech/RTCFake` 公開可下載……D2 的最大單點故障事實層下降。」
- **F 原文**：「RTCFake 是好消息不是風險（公開可下載）。」
- **B/C/D 及 landscape** 同調：「已確認公開可下載」「D2 最大風險就此下降」。
- **駁**：G 這輪實際去抓頁面，**匿名抓取 RTCFake 回 HTTP 401，而同時 CodecFake+ 回 200**——這是 RTCFake 被 gate（需登入＋同意條款才下載）的強訊號，且 repo **未明標學術重散布授權**。六位角色（含 landscape）一致把定稿的「月 0 才知能否取得的單點故障」下修為「風險解除」，**是建立在一個未經驗證的樂觀假設上**。**教授裁定：定稿把 RTCFake 當單點故障是對的，維持月 0 go/no-go，且門檻是雙重——(a) 能否通過 gate 下載、(b) 授權是否允許學術重散布。** 在月 0 實際過關前，任何「風險已解除」的敘述不予採信。這不否定 RTCFake 作為 D2 唯一真實 RTC 錨的地位，只否定「已解除風險」這句話。

### 1.2 B 的 D1「2024–2025 世代四件套 ＋ Deepfake-Eval-2024」——站不住（理由 b：超算力＋偷加格）

- **B 原文**：「unseen-generator 軸（核心，必換）：ASVspoof 2021 DF + MLAAD v5 → 換上 2024–2025 世代四件套」，列出 **DFADD ＋ CodecFake+ ＋ SpeechFake 開源部 ＋ MLAAD v10**，再加 **Deepfake-Eval-2024 eval-only 錨**——共**五個新集去填兩個舊格**，卻宣稱「GPU-hour 430–520 不變」。
- **駁**：定稿 D1 的 grid 是 **4 source × 3 channel = 12 格**，其中 unseen-generator 只有兩格（2021 DF、MLAAD v5）。五個新集塞不進兩格；真要全上就是 4 source→7–8 source，**評估前向、RQ3 confident-real 對抗搜尋、悲觀重跑全部翻倍**。「每集抽 20k」不能救——**格數本身翻倍，20k×更多格＝總前向翻倍，GPU 不可能不變**。這正是我 Round 1 已釘死的偷加。**替換後必須仍是 4×3。** 只准挑兩個新集填掉兩個舊格。

### 1.3 ASVspoof 5 當「訓練種子」升為主力（D3 由 D 提，D1 由部分人可選）——站不住（理由 c＋e：等於重訓、動 in-domain 定義）

- **D（紅隊）原文（D3）**：「種子池 `ASVspoof 2019/2021 → ASVspoof 5(2024, 抽 20k)`」，語氣是主力替換。
- **駁**：換訓練種子 = 偵測器 checkpoint 要對新分布**重訓或至少重驗 EER**，D1「日曆是唯一瓶頸」、D3「偵測器 checkpoint 語意不動」都會被打破——**這是改方法論、不是換餵進去的資料**。且 A/B/G 都正確指出換種子會改變「in-domain（seen 分布）的定義」。**教授裁定：ASVspoof 2019 LA 訓練種子維持，ASVspoof 5 至多列可選對照、不進主線**；且 G 已考證 ASVspoof 5 的 LICENSE.txt 非乾淨 CC tag、重散布須讀條款，連「可取得」都只到備選級，不夠格當主力種子。（紅隊 D 自己也在同頁警告「換訓練種子＝預先接種＝攻擊面過度樂觀」，卻在一行版把它寫成主力替換，自相矛盾——以其保守論為準。）

### 1.4 Deepfake-Eval-2024 當 D1 的 source 格——站不住（理由 a＋d：散布受限、且非更貼近本方向的真實）

- **A/B/D/F** 皆想把它拉進 D1（A 列「可選 stretch」、B 列「eval-only 錨」入四件套、D 直接進五項驗收表、F 列「加 Deepfake-Eval-2024」）。
- **駁**：(a) 內容多為社群 scrape，**再散布授權受限**，碩士生不能當可散布資料處理；(d) 它 52 語、非繁中，對 D1 這個通用 benchmark 是「多一格」而非「換一格」——G 已正確算出「12 格→15 格」。**唯一可接受用法**：若真要放，必須**替換掉某一格**、不得新增，且僅 eval-only。以本輪「替換不新增」紀律，**我裁定不進 D1 網格，只在 discussion 用一句話標明「未涵蓋閉源商用世代」。** A 把它壓成可選、G/H 拒進網格是對的；B/D/F 想扶正的不採。

### 1.5 （補充）SpoofCeleb 作 D2 real 臂、ADD-C 作 D2 模擬臂——站不住（理由 a＋c）

- **SpoofCeleb**：衍生自 VoxCeleb1（Oxford VGG 非商用研究授權），再散布受限——B/C/G 都已正確標 🟡 備選，**維持備選、不採主力**即可。
- **ADD-C 作模擬臂**：G 寫「可（選擇性）以 ADD-C 當模擬臂的公開基準……是既有 Opus/AMR-WB 模擬管線的**替代**」。**駁**：C（訊號）已正確指出 D2-RQ3 的逐因子落差分解**需要模擬側是我方能逐項開關的受控自變數**，ADD-C 的固定條件無法逐因子拆——**拿它替換自建模擬臂＝改方法論**。至多 discussion 引用，不進實驗、不替換自建臂。

---

## 2. 抓出偷渡的範圍擴充（逐一點名，本輪最需防的）

| # | 角色 | 偷渡動作 | 為何算擴充 | 裁定 |
|---|---|---|---|---|
| 1 | **B（D1）** | unseen 兩格 → 塞五個新集（四件套＋Deepfake-Eval） | 4×3 grid 撐成 7–8×3，前向/搜尋/重跑翻倍 | **擋**：只准兩集填兩格 |
| 2 | **C（D1）** | 「三格新負領土各補一種」DFADD＋CodecFake+＋SpeechFake | 原只兩格 unseen，補「三格」＝加一格＝4 source→5 source | **擋**：收回為兩格替換 |
| 3 | **A/B/D（D3）** | unseen 軸加 **SpeechFake 開源部** | G 已明講「CodecFake+＋DFADD 已覆蓋 codec 與 diffusion/FM 兩範式，再加＝擴搜尋池，違反不因換資料順便擴充」 | **擋**：D3 只用 CodecFake+＋DFADD，SpeechFake 不進 |
| 4 | **D（D3）** | ASVspoof 5 種子升主力 | 換種子＝重訓/重驗 EER＝改方法 | **擋**：降為可選對照 |
| 5 | **C（D4）** | 「自傳統 codec 集移除 EVS」 | **動的是通道矩陣＝實驗設計**，不在「換餵進去的資料」範圍內；即使是縮減，也越出本輪唯二授權動作 | **擋**：D4 通道矩陣維持定稿，EVS 去留是另案（本輪不碰）；C 稱「與 D2/D3/D5 一致化」不成立——一致化本身就是動設計 |
| 6 | **C/G（D2）** | ADD-C 作模擬臂替代/對照基準 | 替換自建受控模擬臂＝破壞逐因子分解方法 | **擋**：至多 discussion 引用 |
| 7 | **B/D/F（D1）** | Deepfake-Eval-2024 進網格 | 多一 source 格 | **擋**：不進網格，僅文字提及 |

**三個最危險、我 Round 1 已點名、本輪有人再犯的，必須釘死**：
- **D3 的 ASVspoof 5 adversarial 子集**：一旦種子換 ASVspoof 5，其 Malafide/Malacopula adversarial 條件**嚴禁**進 laundering 評估——否則等於復活定稿已砍的白盒 PGD 軸。D（紅隊）自己也標了這個 caveat，很好，但既然種子本來就不升主力，這條連根拔除最乾淨。
- **D4 的 zh-CN 對照臂升格**：SpeechFake ZH / CFAD 只准服務「證明落差非單一腔調 artifact」一句話，**嚴禁**升為 zh-CN 主軸或第二實驗，且腔調非 zh-TW 的外部效度限制須明標。
- **D1/D3 的「多集齊上」**：這是本輪最普遍的偷加型態，B、C、A、D 都犯了不同程度。**替換不新增，一格換一格。**

---

## 3. 題目正式化複審（指出仍不夠正式/不準確者，給修正）

### 仍帶問題的提議

| 方向 | 提議者 | 問題 | 修正 |
|---|---|---|---|
| **D4** | **F** | 中文標題用 **破折號「——以繁體中文語料為例」**——破折號式副標正是本輪明令要去除的花俏 hook 形式，內容雖正式，形式違規 | 改冒號：《……評估效度審計：以繁體中文語料為例》 |
| **D1** | **A** | 英文 *A Shift-Aware Benchmark … under Distribution Shift*——**shift 出現兩次**（A 自己也承認冗餘）；中文「選擇性預測可靠性基準研究」堆疊三個名詞略累贅 | 去重：主標即 *Shift-Aware Selective-Prediction Benchmark*，不再於句尾補 under Distribution Shift |
| **D1** | **G** | 中文《面向未見生成器與通道之語音深偽偵測選擇性預測可靠性基準研究》——「面向……之……基準研究」句法過長、中段無停頓、可讀性差 | 簡化為《分布偏移下……的選擇性預測基準》 |
| **D3** | **A/B** | 中文標題內嵌英文「adaptive-laundering」與純中文混排，且 **B 用「地圖 / Map」作 deliverable**——「地圖」是隱喻，對學位論文標題偏花俏 | 中文用「適應性洗刷」統一；deliverable 改「評估 / Assessment」（比「地圖」正式） |
| **D3** | **D** | 「適應性**洗白**」——「洗白」偏口語 | 改「適應性洗刷」 |
| **D2** | **C** | 主標《離線模擬與真實通訊通道之落差：……》以「落差」當主標仍帶對比 hook 味；英文過長 | 以「審計」為學位論文類型名收束（見下方定案） |

### 判定為合格、可直接用的
- **H(R1) D5**、**C D5**：兩者皆正式，我採 H(R1) 版（全名「歐盟人工智慧法」比縮寫「歐盟 AI 法」更正式）。
- **D/F D4 的英文** *An Evaluation-Validity Audit …*：正式、名詞收尾、繁中定位清楚，合格（英文用 Scam-Scenario 比 Scam-Scene 順）。

---

## 4. 我背書的最終換法（五方向定案，含維持不換）

> 通則：每個新集都是**填掉一個舊格**，不是多開一格；所有大集沿用 20k 分層抽樣；GPU 帳一格不動；閉源商用世代維持不自建。授權以 G 的實測考證為準（CodecFake+ MIT 非 gate、DFADD MIT＋須用 2025-04 修正版、ASVspoof 5 須讀 LICENSE.txt、RTCFake 疑 gated）。

### D1（維持 4 source × 3 channel = 12 格）
- **2021 DF 這一格 → DFADD（2024, diffusion/FM, MIT, 用修正版）**
- **MLAAD v5 這一格 → CodecFake+（2025, neural-codec, MIT 非 gate）**（與 C_neural 通道軸同構；若想保留 MLAAD 血統，改用 MLAAD v10 drop-in 亦可，二擇一，不得兩個都上）
- **維持**：ASVspoof 2019 LA in-domain 訓練種子＋對照格、In-the-Wild real 格
- **不進網格**：SpeechFake、Deepfake-Eval-2024、ASVspoof 5（至多 discussion 一句話）

### D2
- **fake XTTS/VITS/YourTTS（2022–2023）→ 等量替換 3 家 2025 世代開源 TTS**（如 F5-TTS / CosyVoice 2 ＋一個 codec-based 生成器；**維持 3 家，不擴 5 家**）
- **RTCFake：維持為唯一真實 RTC 錨，但風險敘述維持定稿——月 0 go/no-go 不解除**（G 實測 401 gated＋授權未標；門檻＝能否過 gate＋能否學術重散布）
- **維持**：real 類、AudioSeal 單一、Opus/AMR-WB 自建模擬臂
- **不採**：SpoofCeleb（備選）、ADD-C 進實驗（至多引用）

### D3
- **laundering 對象 2021 DF ＋ MLAAD → CodecFake+（2025）＋ DFADD（2024）兩者**（CodecFake+ 與 RQ2 neural-codec 不可逆論證直接同構）
- **SpeechFake 不進**（避免擴搜尋池）
- **ASVspoof 5：可選種子對照，非主力；若用，只取 TTS/VC＋codec 條件，嚴禁 adversarial 子集**（復活白盒軸）
- **維持**：laundering 動作空間 ≤8、4 偵測器、20k 確認池 / 10k 搜尋池、可控植入可逆性標註
- **caveat**：CodecFake+ fake 本身即 codec 產物，可控植入可逆性標註須以「植入已知 artifact→過動作」為準，不受生成端 codec 污染（D 已正確標）

### D4
- **fake 2 家開源（2022–2023）→ 2 家 2025 世代 zh 開源情緒 TTS**（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 選 2 家；**維持 2 家**）
- **維持自建 zh-TW 定位**（無現成 zh-TW 集，事實）
- **維持通道矩陣（含 EVS）、real 類、話術腳本、品質協變量**（EVS 去留非本輪範圍）
- **CFAD / SpeechFake ZH 僅 zh-CN 對照臂**，不升主軸，外部效度限制須明標
- **月 0–1 情緒 zh-TW TTS 硬 go/no-go 維持不變**

### D5（誠實維持，不為換而換）
- **維持**：載體語音（AISHELL-3/LibriSpeech/real，年份不影響容量量測）、watermark 家族（AudioSeal/WavMark/SilentCipher＝開源全集）、neural codec 通道矩陣
- **唯一更新**：baseline 補《Will They Survive Neural Codecs?》（Interspeech 2025）為 watermark×neural-codec 最新直接前作（零 GPU、零新 RQ）
- **CodecFake+ 至多作 neural codec 世代參照，不進 pipeline、不擴通道矩陣**

### 五方向正式題目（定案，中／英）
- **D1**：《分布偏移下語音深偽偵測的選擇性預測基準》／ *A Shift-Aware Selective-Prediction Benchmark for Audio Deepfake Detection*
- **D2**：《真實通訊通道上音訊深偽反制訊號存活的樂觀偏差審計及畸變層歸因》／ *An Optimism-Bias Audit of Audio Deepfake Countermeasure-Signal Survival over Communication Channels, with Distortion-Layer Attribution*
- **D3**：《被動語音深偽偵測之適應性洗刷攻擊成本上界評估》／ *An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
- **D4**：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》／ *An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Corpus Study*
- **D5**：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》／ *A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels and Its EU AI Act Article 50 Readability Assessment*
