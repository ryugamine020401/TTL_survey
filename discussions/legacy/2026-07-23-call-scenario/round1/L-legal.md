# L-legal 法律與隱私席 — Round 1 發言

> **聲明**：本文為論文問題琢磨之背景論證，非專業法律意見，不得作為任何實際行為之法律依據。查證日期均為 2026-07-23。

## 立場摘要

1. 「接聽方對來電做**本機即時分析、不留存**」在代表性法域是三種模式中唯一全面可守的，且有 Google Pixel Scam Detection 的既有出貨先例背書。
2. 法律面**不觸發 kill**：純來電場景在法律上守得住，但可部署行為者被平台政策壓縮到 **OS/原廠 dialer 層級**，第三方 app 的部署敘事在法律+政策疊加下不可守。
3. 本機錄音留存＝法域分裂（台灣可、美國全體同意州不可）；上雲分析＝風險最高，不建議作論文部署敘事。

## 主體分析

### 台灣

- **Verified**：通訊之一方自行錄音，通保法第 29 條第 3 款「監察者為通訊之一方…而非出於不法目的」不罰；刑法 315-1 竊錄罪客體限「**他人**」非公開談話，通說與實務多認參與對話者錄自己參與的對話不構成（來源：臺灣高等檢察署生活與法律專欄 https://www.tph.moj.gov.tw/4421/4475/632364/960875/post ；律師實務彙整 https://www.honganlaw.com.tw/recording/ ）。搜尋詞：「通訊保障及監察法 一方當事人 自行錄音 刑法315-1」。
- **Inference**：既然「錄下」都合法，僅即時分析、不留存音訊，侵害更輕，依舉重明輕應同樣可守。
- **Verified**：個資法將「聲音」列於個人描述類個資，現行法無 GDPR 式「生物特徵特種資料」專章（法務部全國法規資料庫 https://law.moj.gov.tw/LawClass/LawAll.aspx?PCode=I0050021 ）。**Inference**：自然人為防詐之個人活動處理，落入個資法第 51 條個人活動除外之可能性高。

### 歐盟

- **Verified**：ICO 等指引下，聲音成為 GDPR 第 9 條特種生物特徵資料的前提是「**以唯一識別自然人為目的**」處理（https://summitnotes.app/blog/gdpr-voice-recordings-biometric-data/ ）。**Inference**：深偽偵測判斷「合成 vs 真人」，不建立語者身分模板、不識別是誰，主張不落入 Art. 9 是可辯護的；純個人防詐用途另有 Art. 2(2)(c) 家務除外可用。本機處理免除跨境傳輸與委外處理者義務，是雲端方案沒有的優勢。
- **Verified**：AI Act Art. 50 的深偽義務落在**生成/操縱內容的提供者與部署者**，偵測工具本身非高風險清單項目，且偵測犯罪之用途另有豁免（https://artificialintelligenceact.eu/article/50/ ；歐盟執委會 FAQ https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act ）。偵測器站在義務的受益側，不是義務側。搜尋詞：「EU AI Act deepfake detection Article 50」「GDPR voice biometric Article 9 on-device」。

### 美國

- **Verified**：聯邦法與多數州為 one-party consent；加州等約十餘州為全體同意，California Penal Code §632 禁止未經全體同意錄製機密通訊，參與者自錄也違法（https://codes.findlaw.com/ca/penal-code/pen-sect-632/ ；https://www.kazlg.com/california-call-recording-laws/ ）。搜尋詞：「one-party two-party consent California Penal Code 632」。
- **Verified**：Google Pixel Scam Detection 以 Gemini Nano **on-device 即時聽取通話**，不留存音訊/逐字稿、不上傳、預設關閉、僅限陌生號碼，已在美國全境（含全體同意州）出貨（Google 官方說明 https://support.google.com/phoneapp/answer/15654065 ；https://blog.google/security/staying-one-step-ahead-strengthening-androids-lead-in-scam-protection/ ）。**Inference**：即時瞬態分析不產生「紀錄」，是否構成 §632 的 record/eavesdrop 未經判例檢驗，但產業已以「不留存+預設關閉」的設計裁掉主要風險。**Unknown**：無直接判例。

### 平台政策（法律風險的實際執行層）

- **Verified**：Google Play 自 2022-05-11 起禁止第三方 app 以 Accessibility API 錄通話，僅 OEM 預設 dialer 可錄（https://www.theregister.com/software/2022/04/22/google-bans-third-party-call-recording-apps-from-play-store/ ）。iOS 從未提供第三方通話音訊 API；iOS 18.1（2024-10）起原生錄音會**向雙方語音播報**（https://www.macrumors.com/how-to/ios-record-your-phone-calls/ ）。搜尋詞：「Google Play call recording accessibility 2022」「iOS 18.1 call recording announcement」。
- **Inference**：法律上可守的模式（本機不留存），其可部署行為者實際上只剩 **OS 廠商/原廠 dialer**（Pixel 模式）。第三方 app 敘事死於政策而非法律。

### 三種模式判決

| 模式 | 台灣 | 歐盟 | 美國 | 平台 | 風險層級 |
|---|---|---|---|---|---|
| 本機即時分析不留存 | 可守 | 可守 | 可辯護（有出貨先例） | 僅 OS 層 | **低** |
| 本機錄音留存 | 可守 | 較重（storage limitation） | 全體同意州不可 | 僅 OS 層 | 中 |
| 上雲分析 | 個資法委外義務 | GDPR 全套+傳輸 | 第三方介入疑慮 | 政策+審查最嚴 | **高** |

**可支撐論文部署敘事的唯一模式：OS/dialer 層級之本機即時瞬態分析（Pixel Scam Detection 同構）。** 論文本身用公開資料集離線實驗，不涉及任何實際攔聽，法律問題僅存在於 motivation 的部署敘事層。

## 對候選研究問題的具體修改或否決

不否決。建議兩點修改：(1) 部署敘事明寫「以 OS 級 on-device、不留存、預設關閉之防詐功能為想定部署點」，引 Pixel Scam Detection 為先例，勿寫「第三方 app」；(2) 候選問題中「聽到第幾秒才 commit」的 anytime 形式與「瞬態處理、不留存」的法律最優設計**天然同構**——越早棄權/判定、緩衝的音訊越短，這可以寫成隱私 minimization 的加分論證，而非只是統計性質。

## Kill conditions

若出現以下任一證據，我放棄「本機不留存可守」路線：(1) 美國全體同意州出現判例或執法，認定**不留存的即時 AI 分析**仍構成非法竊聽/錄音；(2) Google 因法律原因在代表性法域下架或閹割 Scam Detection；(3) 歐盟將「通話端深偽偵測」列入 AI Act 高風險或禁止清單。另：若 P 席判定 OS 層以外無任何技術取得通話音訊之途徑，且認定「以 OS 級功能為想定部署點」不足以支撐碩士論文的部署敘事，則法律上最乾淨的改錨依序為：**語音訊息**（已送達的儲存媒體，接收方分析完全無攔聽問題，全法域乾淨）> 視訊會議（平台 API 存在但涉多方同意告知）> 擴音側錄（技術可行但在全體同意州與錄音同評價，並不更乾淨）。

## 給下一波的一句話

法律不殺這個場景，但把部署敘事鎖死在「OS 級、本機、瞬態、不留存」一條窄門上——S/A/C/D 請在這條窄門的約束下（無錄音留存＝不能事後重跑、緩衝越短越好）做形式化與機器設計，這反而讓 anytime 三態輸出從選項變成必然。
