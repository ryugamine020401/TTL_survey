# P-platform 行動平台工程師 — Round 1 判決

## 立場摘要（≤5 行）

- 第三方 app 層：**全滅**。iOS 與 Android 皆無合法且技術可行的公開 API，讓非系統 app 拿到即時蜂巢通話的雙向語音流。
- OS/OEM 特權層：**唯一乾淨的即時來電音訊部署點**（Pixel 系統 Phone app 已是先例，on-device、8kHz 級、串流）。碩士生無法部署，但**可以把 estimand 誠實錨在此點**。
- Carrier 層：技術上存在，但網內轉碼條件不透明、學生無從界定取樣率/通道，不能當 estimand 錨點。
- 側錄層：人人可做，但音訊雙重劣化，estimand 髒。
- 結論：**場景不 kill**（真實部署點存在），但「第三方 app 即時攔截來電」這個敘事必須死；建議改錨到 OS-privileged Phone-app framing。

## 主體分析

**app 層（Verified，全滅）。** iOS 上 CallKit 只提供來電 UI 整合與 VoIP 推播，**不暴露 PSTN/蜂巢通話的音訊 buffer**；AVAudioSession 也拿不到對方語音，Apple 以隱私為由封鎖，連「偵測是否被錄音」的 API 都不存在。〔Verified｜https://developer.apple.com/forums/tags/callkit ；https://getstream.io/video/docs/ios/advanced/incoming-calls/callkit-integration/ ｜查證 2026-07-23｜搜尋詞「iOS CallKit third-party app access call audio stream 2025」〕Android 側：microphone 錄通話自 Android 10 起被封；2022-05-11 Google Play 政策明文禁止用 AccessibilityService 錄通話（官方語：「The Accessibility API is not designed and cannot be requested for remote call audio recording」），並把通話錄音歸類為 spyware。**唯一豁免是系統/預裝 dialer（Pixel、Xiaomi）**。〔Verified｜https://www.theregister.com/2022/04/22/google_banning_thirdparty_callrecording_apps/ ；https://m.gsmarena.com/google_to_kill_callrecording_apps_on_play_store_on_may_11-news-54039.php ｜查證 2026-07-23｜搜尋詞「Android call recording API restrictions AccessibilityService ban Android 10」〕

**OS/OEM 特權層（Verified，可錨）。** Google Pixel 的 Scam Detection 正是此層先例：接到非聯絡人來電時，**on-device AI（Gemini Nano 2）即時處理通話音訊**找詐騙話術，且「音訊不儲存、不上傳、never leaves the phone's RAM」，僅限 Pixel 9 系列。〔Verified｜https://support.google.com/phoneapp/answer/15654065 ；https://store.google.com/us/magazine/march-pixel-drop-scam-detection ｜查證 2026-07-23｜搜尋詞「Pixel Scam Detection on-device call audio Google 2025」〕**關鍵含義**：拿到即時來電音訊流是 OS 廠商 / 預裝 Phone app 的特權，不是第三方 app 能力。這對本論文是好消息而非壞消息——**這是一個真實、有文件、on-device、輕量化的部署點**，estimand（8kHz 級、單通道、post-network、逐秒串流前綴）可以科學地錨在「系統 Phone app 的 on-device 即時篩選」，論文只做離線模擬、不需要真的變成 Google。這與 proposal-final 的 edge/本機輕量化敘事完全相容。

**Carrier 層（Verified 部分 + Inference）。** T-Mobile Scam Shield 等在網內即時分析，但**主要是號碼信譽/行為啟發式（metadata），不是對語音內容做深偽偵測**；synthetic-voice 內容級偵測目前主要在企業 contact center，而非消費者網內。〔Verified｜https://www.t-mobile.com/news/press/scam-block ；https://tnsi.com/resource/com/top-five-takeaways-from-2025-robocalls-robotexts-and-the-battle-for-voice-security-blog/ ｜查證 2026-07-23｜搜尋詞「carrier network AI scam call detection T-Mobile real-time」〕碩士生無法界定網內轉碼後的確切取樣率/通道，**不宜當 estimand 錨點**（Inference）。

**側錄層（Verified，髒）。** 擴音+第二裝置錄音人人可做，但音質受房間噪音、回聲、二次麥克風劣化，且已不是純電話通道信號。〔Verified｜https://transom.org/2020/recording-cellular-phone-calls/ ｜查證 2026-07-23ｕ搜尋詞「speakerphone second device audio quality」〕可作 robustness stress，不宜作主 estimand。

## 對候選研究問題的具體修改

保留「串流前綴 → anytime 三態」形式化，但**把部署行為者從『第三方 app』改寫為『OS-privileged / 系統 Phone app 的 on-device 篩選』**（Pixel Scam Detection 為 named 先例）。estimand 明文錨定：on-device、單通道、電話帶寬（8kHz）、逐秒到達前綴、無雲端。**刪除任何「我做一個 app 攔截你的來電」暗示**，否則 L-legal 與現實會一起打臉。若作者堅持第三方 app 可部署，則此候選問題 kill。

## kill conditions（什麼證據出現就放棄本路線）

1. 若連 OS 廠商先例都要求上雲（音訊離開裝置）才能即時偵測 → on-device 串流 estimand 崩，退回「事後語音訊息分析」。
2. 若 S/A 席證明短前綴下 SSL 偵測器劣化到無 anytime 有效判定空間 → 串流敘事本身失效（那是方法問題，非平台問題）。
3. 若作者要求論文必須「真的部署可攔截來電的行為者」→ 直接 kill，改錨。

## 改錨選項排序（若嚴格要求第三方可部署）

1. **OS-privileged Phone-app framing**（首選，保留來電場景，錨 Pixel 先例，只做離線模擬）。
2. **語音訊息事後分析**（LINE/WhatsApp voice message：app 對自家音訊有合法存取，estimand 乾淨，但非即時來電）。
3. **視訊會議 app 串流**（app 擁有自己的媒體流，串流 estimand 成立）。
4. **擴音側錄**（真實但雙重劣化，作 robustness）。
5. carrier 端（估 estimand 不可行，排除）。

## 給下一波的一句話

第三方 app 即時攔截來電已死，但 on-device 系統 Phone app 是真實可錨的部署點——S/A/C 請把 estimand 直接錨在「8kHz、單通道、逐秒前綴、on-device、無雲端」，別再假設 app 能碰到通話流。
