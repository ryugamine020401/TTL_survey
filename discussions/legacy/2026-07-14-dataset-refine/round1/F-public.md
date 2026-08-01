# Round 1 資料集提議：一般民眾代表（Agent F）
日期：2026-07-14

> 我的判準只有一條：**新資料集是否更接近「真實詐騙現場實際到達受害者耳朵的那段音訊」**——最新（含閉源）TTS 世代、繁體中文、走過真實通道。一個方向如果用的資料集離真實詐騙很遠，它量出來的數字再漂亮，也救不了那位接到電話的阿嬤、那位被冒名主管的上班族、那位被偽造錄音抹黑的選民。
>
> **紀律自綁**：本輪只做兩件事——(1) 舊資料集換新、(2) 題目正式化。不加實驗、不加 RQ、不加比較、不擴範圍。凡舊資料集仍是該任務最佳選擇者，我誠實寫「維持」，絕不為換而換。所有大型新集一律沿用定稿的 20k 分層抽樣。

---

## 我看五個方向「離真實詐騙有多遠」的排序（先講立場）

| 離真實詐騙 | 方向 | 一句話理由（民眾視角） |
|---|---|---|
| **最近** | **D4 繁中詐騙審計** | 唯一直接對著台灣受害者耳朵的方向；但 fake 生成器停在 2022–2023，等於用「三年前的詐騙工具」測 2026 的詐騙——這是我最想換的一格 |
| 近 | **D2 通道存活審計** | 唯一錨真實通道（RTCFake）；但 fake 還是 XTTS/VITS，反制訊號折扣係數量在舊 fake 上會失真 |
| 中 | **D3 攻擊成本地圖** | RQ2 的「neural codec 必殺動作」若只對舊生成器，攻擊者早換工具了；CodecFake+ 讓它對得上 2025 世代 |
| 中 | **D1 選擇性預測基準** | unseen-generator 軸決定「負領土地圖」反不反映 2026 攻擊；2021 DF + MLAAD v5 已過期 |
| 較遠（但合理） | **D5 watermark 容量** | 服務的是非即時語音訊息/選民自證，本就不對即時詐騙電話；載體語音年份不影響，資料幾乎不必換 |

以下逐方向給提議。

---

## D1｜分布偏移下語音深偽偵測的選擇性預測基準

### 現用舊資料集
- ASVspoof 2019 LA train + dev（訓練種子，2019 錄音棚）
- ASVspoof 2019 LA eval（in-domain 對照格）
- ASVspoof 2021 DF eval（unseen 對象，2021 世代）
- In-the-Wild（real 類 + unseen，2022）
- MLAAD v5（unseen-generator 廣度，2023）

### 建議替換
**核心要換的是 unseen-generator 軸**（決定「負領土地圖」反不反映 2026 攻擊者手上的工具），in-domain 訓練種子**可選換、非必要**。

1. **unseen-generator 軸：ASVspoof 2021 DF + MLAAD v5 → DFADD（2024, diffusion/FM）＋ CodecFake+（2025, neural codec）＋ SpeechFake 開源部（2025）**——三者合成一個「2024–2025 生成範式」的抽樣池，取代 2021 世代。
2. **eval-only 真實流通錨：加 Deepfake-Eval-2024（2025, eval-only）**——這是唯一「攻擊分布 = 2024 年社群實際流通、隱含含閉源商用世代」的公開集，最能證明舊 benchmark 結論已過期。**只當 eval 格，不進訓練。**
3. **（可選）in-domain 訓練種子：ASVspoof 2019 LA → ASVspoof 5 train（2024, crowdsourced 非棚錄）**——把 "seen" 分布從 2019 錄音棚升到 2024 多裝置多語者。**列為可選，因為它改的是「in-domain 的定義」而非核心 novelty，且會多一輪訓練復現風險。**

### 通過五項驗收
| 驗收項 | 說明 |
|---|---|
| **更新（年份）** | DFADD 2024、CodecFake+ 2025、SpeechFake 2025、Deepfake-Eval-2024 2025（vs 舊的 2021/2023） |
| **可取得（來源+授權+大小）** | DFADD（HuggingFace，開源，數 GB）🟢／CodecFake+（HuggingFace `CodecFake/CodecFake_Plus_Dataset`，開源，大 → 抽樣）🟢／SpeechFake 開源部（HuggingFace `DeepFense/SpeechFake`，Apache 2.0，>TB → 抽樣）🟢／Deepfake-Eval-2024（GitHub，eval-only、scrape 內容再散布受限，音訊 56.5h）🟡 |
| **算力相容（抽樣後規模）** | 全部沿用分層抽 20k；Deepfake-Eval-2024 音訊僅 56.5h 可整段當一個 eval 格，不增訓練成本；in-domain 種子換 ASVspoof 5 亦抽 20k。GPU 430–520 不變 |
| **契合原方法（不需改方法）** | 全是「換餵進同一條快取管線的 fake」；`s × g × R–C` 介面一行不改，只是網格的 source 軸換了 cell 內容 |
| **時效性論證（一句話）** | 讓「偵測器沒見過的生成器」是 2024–2025 的 diffusion/FM、neural-codec 與真實流通世代，而非 2021 的舊 TTS——負領土地圖才是 2026 阿嬤真的會遇到的攻擊，不是三年前的博物館展品 |

> **民眾視角誠實話**：Deepfake-Eval-2024 是 52 語、非繁中，離「台灣詐騙現場」仍有距離；但 D1 本就是通用 benchmark、不是繁中方向，把它當「唯一摸得到閉源商用世代」的 eval 錨是合理的——真實流通的 2024 fake，比錄音棚裡的 2021 樣本更接近攻擊者今天手上的東西。

---

## D2｜真實通道上音訊深偽反制訊號的樂觀偏差審計

### 現用舊資料集
- bona fide real：ASVspoof 2019 LA real / In-the-Wild real / MLAAD real
- fake：XTTS-v2、VITS、YourTTS（2022–2023 開源 TTS）
- **真實通道錨：RTCFake（定稿當它是「月 0 才知能否取得」的單點故障）**
- watermark：AudioSeal（單一）

### 建議替換
1. **RTCFake：維持，但從「單點故障」改標為「已確認 HuggingFace 公開可下載」**——事實層已解除風險（`JunXueTech/RTCFake`，~600h，公開）。這不是換新，是**降風險**；仍保留月 0 確認學術重散布條款（授權未明標）。
2. **fake 生成器：XTTS-v2/VITS/YourTTS → 補 2025 世代（CodecFake+ 的 codec-based 世代 ＋ SpeechFake 開源部）**——把反制訊號拿去對「攻擊者今天真的在用的 fake」測存活。

### 通過五項驗收
| 驗收項 | 說明 |
|---|---|
| **更新（年份）** | RTCFake 2026（真實 RTC 通道）；fake 世代 2025（vs 2022–2023） |
| **可取得（來源+授權+大小）** | RTCFake（HuggingFace 公開可下載，~600h，散布條款月 0 確認）🟢／CodecFake+、SpeechFake 開源部（HuggingFace，開源/Apache 2.0）🟢 |
| **算力相容（抽樣後規模）** | RTCFake ~600h → 抽樣池 20k；fake 補充亦併入 20k 分層池；watermark 仍 AudioSeal 單一。GPU ~510 不變 |
| **契合原方法（不需改方法）** | 「通道存活審計台」的探針與協定完全不動；只是灌進去的 fake 換成 2025 世代、真實通道錨的取得性確認為可下載 |
| **時效性論證（一句話）** | γ（樂觀偏差係數）是給整個社群當「通道折扣」直接消費的數字——它必須量在 2026 攻擊者用的 fake 上，量在真的走過 Zoom/RTC 的音訊上，才是 2026 的折扣係數，而不是 2022 的 |

> **民眾視角誠實話**：RTCFake 是 Zoom 這類 RTC 平台，**不是**阿嬤接到的那通「+886 開頭的假冒檢警電話」的蜂巢/PSTN 通道——這一點外部效度差距要在論文裡誠實寫明。但在「一位碩士生今天下得到的公開真實通道」裡，它是最接近的，比純模擬 codec 近太多。我支持它，並要求論文別把「RTC ≈ 詐騙電話通道」講死。

---

## D3｜被動語音深偽偵測的 adaptive-laundering 攻擊成本上界地圖

### 現用舊資料集
- ASVspoof 2019 LA / 2021 DF（DF 抽 20k 確認 / 10k 搜尋）
- In-the-Wild、MLAAD（unseen-generator 軸）
- laundering 工具鏈（EnCodec/DAC + ffmpeg codec）

### 建議替換
1. **unseen-generator / laundering 對象：2021 DF + MLAAD → CodecFake+（2025）＋ DFADD（2024）＋ SpeechFake 開源部（2025）**——尤其 CodecFake+ 與 RQ2「neural codec transcode 是不可逆必殺動作」直接同構：它就是 31 開源 neural codec + 17 codec-based 生成系統的集合，讓「必殺動作」從假想威脅變成對 2025 世代 fake 的實測。
2. **（可選）in-domain 種子：ASVspoof 2019/2021 → ASVspoof 5（2024）**——crowdsourced + 內建 neural codec 條件 + 首含 adversarial，與 D3 的攻擊成本主題契合；抽 20k。

### 通過五項驗收
| 驗收項 | 說明 |
|---|---|
| **更新（年份）** | CodecFake+ 2025、DFADD 2024、SpeechFake 2025、ASVspoof 5 2024（vs 2019/2021） |
| **可取得（來源+授權+大小）** | CodecFake+（HuggingFace，開源，多 .part → 抽樣）🟢／DFADD（HuggingFace，數 GB）🟢／SpeechFake 開源部（Apache 2.0 → 抽樣）🟢／ASVspoof 5（Zenodo 14498691，直接下載 → 抽樣 20k）🟢 |
| **算力相容（抽樣後規模）** | 沿用 20k 確認池 / 10k 搜尋池；neural codec transcode 動作空間不變。GPU 610 不變 |
| **契合原方法（不需改方法）** | greedy 搜尋、可控植入可逆性標註、成本地圖全不動；只是 laundering 打的對象與 seed 換成 2025 世代 |
| **時效性論證（一句話）** | 攻擊成本上界要對「攻擊者今天真的能生成的 fake」才算數——CodecFake+ 讓「neural codec 是零成本、物理不可逆的必殺動作」這個結論，是對 2025 世代生成器實測出來的，不是對 2019 老古董 |

> **民眾視角誠實話**：D3 的承重錨（neural codec many-to-one 投影的物理不可逆）本來就不隨生成器版本過期，這是它最讓我安心的地方——但把 laundering 打擊對象換到 CodecFake+，能讓「防守方在裸奔」這個對部署機構的警告，講得更貼近 2026 的真實攻防，機構才不能拿「那是舊資料」搪塞。

---

## D4｜詐騙現場條件下語音深偽偵測的評估效度審計（繁中）★ 我最有把握的方向

### 現用舊資料集
- 話術腳本：~165 條反詐宣導/刑事局公開話術（公開，維持）
- bona fide real：Common Voice zh-TW、AISHELL、公開廣播 + ASVspoof/In-the-Wild real（載體，維持）
- **fake：純 2 家開源情緒可控 TTS/VC（情緒可控 VITS 系 / OpenVoice 類 + VC 參考語者）← 2022–2023 世代，這是我最想換的一格**
- 通道：offline codec 模擬（維持）
- 品質協變量：UTMOS + ECAPA speaker similarity（維持）

### 建議替換
**這是全案唯一直接對著台灣受害者耳朵的方向，也是我最堅持要換的一格。** 詐騙現場的「那三秒」是哭腔、是急迫命令——2022 的 VITS/YourTTS/OpenVoice 產不出可信的台灣國語哭腔，等於用三年前的詐騙工具去測 2026 的詐騙。

1. **fake 生成器：VITS 系 / YourTTS / OpenVoice → 2025 世代 zh-capable 開源可控 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）**——這些才是 2025–2026 詐騙集團真的搆得到、且能做出情緒（哭腔/急迫）的當代工具。**維持「純 2 家」的定稿設計，只把這 2 家升級到 2025 世代，不加第三家。**
2. **對照臂：補 SpeechFake ZH 子集（2025）／ CFAD（2024）作為 zh-CN 對照**——僅用來佐證「落差不是單一腔調 artifact」，**明文標註腔調為 zh-CN（大陸普通話）、非 zh-TW，屬外部效度限制**。
3. **自建定位維持不變**——因為**沒有任何公開的 zh-TW deepfake 語音集**（這是我查證後的硬事實），D4 的自建正確且必要，本輪不動這個定位，只換 fake 生成器世代。

### 通過五項驗收
| 驗收項 | 說明 |
|---|---|
| **更新（年份）** | CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2 皆 2024–2025 開源；SpeechFake ZH 2025、CFAD 2024（vs 舊的 2022–2023 VITS/OpenVoice） |
| **可取得（來源+授權+大小）** | 2025 世代 zh 開源 TTS 皆 HuggingFace/GitHub 公開權重、可自建生成 🟢／SpeechFake ZH（HuggingFace，Apache 2.0 開源部）🟡（zh-CN 腔調，標外部效度限制）／CFAD（公開下載）🟡（zh-CN） |
| **算力相容（抽樣後規模）** | 自建 ~2–3 萬筆規模不變（GPU ≈180，全場最寬鬆）；對照臂只抽小樣本佐證，不放大規模 |
| **契合原方法（不需改方法）** | 「受控析因的評估落差量測」三讀法（彙總/分層/配對）完全不動；只是生成 fake 的 TTS 換代、多一個 zh-CN 對照切片。**月 0–1 情緒 zh-TW TTS 硬 go/no-go 關卡照舊**（換成 2025 世代反而更可能通過，因 CosyVoice 2/F5-TTS 情緒與跨語言能力遠強於 2022 VITS） |
| **時效性論證（一句話）** | 「到達耳朵的那三秒」若用 2022 的 TTS 合成，量的是「三年前的詐騙」；換成 2025 世代能產哭腔/急迫的 zh 開源 TTS，量的才是 2026 阿嬤真的會在電話裡聽到的那個聲音 |

> **民眾視角誠實話**：這一換對「救不救得了人」最關鍵。廠商今天宣稱「能防詐」的成績單，幾乎都來自十秒朗讀句、中性韻律、錄音棚——但攻擊者早就在用 2025 的情緒 TTS 做哭腔了。若 D4 也停在 2022 的 fake，它就變成「用舊工具驗舊工具」，反而給了廠商一個「你測的不是我們現在面對的攻擊」的免死金牌。升到 2025 世代，這份繁中考卷才真的擋得住廠商的搪塞。**這也是我唯一擔心「go/no-go 關卡」的地方——但 2025 世代的跨語言情緒能力比 2022 強得多，這一換讓關卡更可能綠燈，不是更可能紅燈。**

### 正式題目提議（中英）
- **中**：《詐騙情境音訊條件下語音深偽偵測器評估效度之審計——以繁體中文語料為例》
- **英**：*An Evaluation-Validity Audit of Audio Deepfake Detectors under Scam-Scenario Acoustic Conditions: A Traditional Chinese Corpus Study*

（拿掉「到達耳朵的那三秒」金句與冒號後的口語；保留「評估效度審計」的學術定位，並把「繁體中文語料」這個生態效度核心明列於副標，讓題目本身就宣告它服務的是台灣受害者。）

---

## D5｜詐騙音訊通道對 watermark provenance 標記的可靠位元容量審計

### 現用舊資料集
- 載體語音：AISHELL-3 + LibriSpeech + ASVspoof19 / In-the-Wild real（分層抽 ~10k 池）
- watermark：AudioSeal + WavMark + SilentCipher（開源 learned watermark）
- 通道：傳統 codec（AMR-WB/Opus/SILK/MP3/AAC-LC）＋ neural codec（EnCodec/DAC/SpeechTokenizer）
- baseline：AudioMarkBench（2024）

### 建議替換
**主體維持——這是我誠實判定「不該為換而換」的方向。** 理由：
1. **載體語音維持**——它只是 watermark 的載體，年份不影響「還剩幾個 bit」這個物理量測；AISHELL-3/LibriSpeech 是成熟穩定的載體，換成新集只會增加工具鏈風險、不增加科學效度。
2. **watermark 家族維持**——AudioSeal / WavMark / SilentCipher 已是當前開源可得的全部，沒有更新的可換。
3. **唯一更新：baseline 前作補「Will They Survive Neural Codecs?」（2025, Interspeech, arXiv 2505.19663）**——這是 D5 主題（watermark × neural codec）的最新前作，把 D5 的「第一張可靠 bit 容量地圖」定位錨到 2025 已發表基準（相對前作補上可控植入 ground-truth 錨 + 索引構造）。
4. **（可選）neural codec 世代參照 CodecFake+**——僅作 neural codec 通道的世代參照點，不改通道矩陣設計。

### 通過五項驗收
| 驗收項 | 說明 |
|---|---|
| **更新（年份）** | 「Will They Survive Neural Codecs?」2025（Interspeech）補為前作；載體與 watermark 家族本就無更新可換，維持是正確而非落後 |
| **可取得（來源+授權+大小）** | 前作為論文/repo（arXiv 2505.19663）🟢；載體語料與 watermark checkpoint 皆已在用、公開 🟢 |
| **算力相容（抽樣後規模）** | ~10k 載體池、通道矩陣、GPU ≈220 全不變（補的是文獻定位，不是運算） |
| **契合原方法（不需改方法）** | 「可靠 bit 復原」pipeline 一行不改；補前作只影響 related work 與 baseline 對照的敘事，不動實驗 |
| **時效性論證（一句話）** | D5 服務的是非即時語音訊息/選民自證，不對即時詐騙電話——它的資料需求本就不吃「最新 fake 世代」，該更新的是把結論錨到 2025 最新的 watermark×neural codec 前作，讓「容量塌陷點」的論證對得上當前文獻，而不是硬換一批不影響物理量測的載體 |

> **民眾視角誠實話**：D5 離「即時詐騙電話現場」最遠——它明說了自己救不了正在響的那通電話，只服務事後的語音訊息、選民的來源自證。正因如此，硬把它的載體換成「更新的 fake」是搞錯對象：它量的是 watermark 過通道還剩幾個 bit，載體是真人聲音、不是 fake。**我支持維持，這是誠實，不是偷懶。** 唯一要補的是把最新前作放進來，讓它的政策判決（Article 50 可讀性）站在 2025 的地基上。

---

## 回傳摘要（純文字資料）

### 五個方向「舊 → 新」一行版（民眾視角）
- **D1**：unseen-generator 軸 `ASVspoof 2021 DF + MLAAD v5` → `DFADD(2024) + CodecFake+(2025) + SpeechFake 開源部(2025)`，另加 `Deepfake-Eval-2024(2025, eval-only)` 當真實流通錨；in-domain 種子可選 `ASVspoof 2019 LA → ASVspoof 5(2024)`。
- **D2**：真實通道錨 `RTCFake` 由「月 0 單點故障」→「已確認公開可下載、降風險」（維持不換、只解除風險）；fake 生成器 `XTTS/VITS/YourTTS(2022–23)` → 補 `CodecFake+ / SpeechFake 開源部(2025)`。
- **D3**：laundering 對象 `2021 DF + MLAAD` → `CodecFake+(2025) + DFADD(2024) + SpeechFake 開源部(2025)`（CodecFake+ 直接對上 RQ2 neural codec 必殺動作）；in-domain 種子可選 `ASVspoof 2019/2021 → ASVspoof 5(2024)`。
- **D4**（我最有把握）：fake 生成器 `情緒 VITS 系 / YourTTS / OpenVoice(2022–23)` → `2025 世代 zh 開源可控 TTS（CosyVoice 2 / F5-TTS / GPT-SoVITS / OpenVoice v2）`，補 `SpeechFake ZH / CFAD` 作 zh-CN 對照臂；**自建 zh-TW 定位維持不變（無現成 zh-TW 集）**。
- **D5**：**資料集維持**（載體語音與 watermark 家族無更新可換、換了只增風險不增效度）；唯一更新 baseline 前作補 `Will They Survive Neural Codecs?(2025, Interspeech)`，neural codec 世代可選參照 `CodecFake+`。

### 我提議的正式題目（僅對最有把握的 D4、D2）
- **D4（中）**：《詐騙情境音訊條件下語音深偽偵測器評估效度之審計——以繁體中文語料為例》
- **D4（英）**：*An Evaluation-Validity Audit of Audio Deepfake Detectors under Scam-Scenario Acoustic Conditions: A Traditional Chinese Corpus Study*
- **D2（中）**：《真實通訊通道上音訊深偽反制訊號存活率之樂觀偏差審計與畸變層歸因》
- **D2（英）**：*An Optimism-Bias Audit and Distortion-Layer Attribution of Audio Deepfake Countermeasure-Signal Survival over Real Communication Channels*

### 一句話立場
最該換、也最救得了人的是 **D4 的 fake 生成器世代**（用 2022 工具測 2026 詐騙等於給廠商免死金牌）；**D5 誠實維持不換**（載體年份不影響物理量測，硬換是搞錯對象）；**D2 的 RTCFake 是好消息不是風險**（公開可下載），但須誠實標明「RTC ≠ 詐騙電話蜂巢通道」的外部效度差距。
