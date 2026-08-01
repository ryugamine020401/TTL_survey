# C-signal 電信通道訊號專家席 — Round 1 發言

日期：2026-07-23。回應 Gate 三席判決後之改錨場景：OS-privileged 系統 Phone app 的 on-device 篩選，estimand 錨在 8kHz、單通道、post-network、逐秒串流前綴。

## 立場摘要

1. 零 rig 下，來電通道可模擬到「窄頻重採樣 + 傳統/行動 codec + 真實 PSTN 管線響應卷積 + Gilbert-Elliott 丟包」層級，全部 CPU 可做；EVS 維持砍除，VoLTE 以 AMR-WB 近似並誠列缺口。
2. 端點 DSP（AGC/噪抑/回音消除）與真實 VoLTE 鏈路不可模擬——樂觀偏差 γ 不靠建 rig 解，靠 ASVspoof 2021 LA C3（組織者已做過的真實 PSTN 傳輸、免申請）作 sim-to-real 校準。
3. 前綴截取必須「整段先過通道、解碼後截波形」，每通話固定一次通道實現；per-prefix 重編碼是錯誤 estimand。
4. RTCFake 已查證為 gated，違反免申請 hard gate，critical path 排除。

## 主體分析

### A. 可離線模擬且 CPU 可做（更新原方向二/三紀錄）

- **窄頻管線**：16k→8k→16k 重採樣、G.711 a/µ-law、GSM-FR——ffmpeg 內建，零爭議。〔Verified〕
- **AMR-NB/AMR-WB**：ffmpeg 經 `libopencore-amrnb`（NB 編解）與 `libvo-amrwbenc`（WB 編碼），gyan.dev Windows 預編譯 build 已啟用這些旗標，免自行編譯專利參考碼。原紀錄「AMR-WB 需編譯專利碼」已不成立——opencore/vo 是 Apache 授權的既有函式庫。〔Verified：https://www.gyan.dev/ffmpeg/builds/ 、https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/libopencore-amr.c ，2026-07-23〕
- **Opus/Speex**：libopus/libspeex 標準可得。〔Verified〕
- **EVS**：ffmpeg 主線至今無 EVS 編碼器；唯一途徑仍是 3GPP TS 26.442/26.443 ANSI-C 參考碼（專利授權灰色、需自行編譯）。**維持原判：砍。** VoLTE 語音以 AMR-WB 近似（實務上 VoLTE 大量使用 AMR-WB），VoNR/EVS 誠實列為 coverage 缺口而非偷渡。〔Verified：https://en.wikipedia.org/wiki/Enhanced_Voice_Services 、https://github.com/wanglihe/3gpp-evs ，2026-07-23〕
- **關鍵免費資產（呼應 G 席）**：ASVspoof 5 內建 C08（Opus 8k, 4–20kbps）、C09（AMR 8k, 4.75–12.2kbps）、C10（Speex 8k）、C11（八組「裝置→PSTN→客服平台」端到端撥打管線之響應、以 synchronised swept-sine 估計後卷積，六種撥打裝置×四種注入法）。通道軸免申請、免 rig、與 proposal-final 的 primary confirmatory 同源。〔Verified：arXiv:2502.08857，2026-07-23〕**Caveat**：C11 是把非線性系統的量測響應做**線性卷積**近似，不含 codec 非線性與時變行為，不可宣稱等同真實撥打。〔Verified，同上〕
- **丟包/jitter**：Opus 封包級、AMR 幀級的 Gilbert-Elliott 丟棄 + 解碼器內建 PLC（packet loss concealment），CPU 可做、實作簡單。〔Inference：解碼器 PLC 介面存在為 Verified，GE 參數選擇屬設計決策〕

### B. 做不到的，與 γ 教訓的關係

不可模擬：手機端點 DSP（AGC、噪抑、AEC——廠商閉源且機型各異）、真實 VoLTE 空中介面、營運商級聯轉碼（ASVspoof 2021 論文明言 C3 含「multiple, unknown intermediate PSTN transcodings」）、自適應 jitter buffer 的時間伸縮（WebRTC NetEQ 類）。原方向二教訓＝模擬通道對真實通道**系統性樂觀（γ）**。零 rig 下的解法不是放棄，而是：**ASVspoof 2021 LA 的 C1（clean）/C2、C5（Asterisk PBX a-law/µ-law）/C3（真手機經 PSTN 到 SIP 端點）是同源 utterance 的配對條件**，Zenodo 4837263 免申請、keys 公開（ODC-By）。用它可以在零 rig 下**實測**「模擬 codec 條件 vs 真實 PSTN 傳輸」的效能差，給 γ 一個經驗上界。〔Verified：arXiv:2109.00535、https://zenodo.org/record/4837263 、https://www.asvspoof.org/index2021.html ，2026-07-23〕限制：2021 LA 的攻擊是 2019 的 A07–A19 舊生成器 → 只能當**通道軸校準與 robustness**，不能當未見生成器的 confirmatory。〔Verified〕

### C. 串流前綴 × 有狀態 codec：截取位置決定 estimand 正確性

真實來電中，編碼是隨說話**持續進行**的因果過程；偵測器在時刻 τ 拿到的是**接收端解碼串流的前 τ 秒**。因此正確做法：**每 utterance 過一次完整通道（encode-once/decode-once，固定丟包軌跡 seed），前綴在解碼後波形上沿 20ms 幀界截取**。理由：(1) 語音編碼器僅有毫秒級 lookahead，encode(前綴) ≈ encode(全段)之前綴，但 per-prefix 重編碼會在截點產生真實通話中不存在的 flush/padding 邊界偽影；(2) 同一通話不同前綴若各自重抽丟包實現，會破壞 sequential decision 所需的同一 sample path（filtration 一致性）——這是 S 席 anytime 保證的前提；(3) 計算上每 utterance 一次 codec pass，成本降一個數量級。〔Inference，基於 codec 因果性之 Verified 事實〕

### D. 現成真實通道 ADD 資料的 confirmatory/exploratory 判定

- **ASVspoof 5 C08–C11**：confirmatory 主軸（免申請、未見生成器 lineage 已 audit、通道軸內建）。〔Verified〕
- **ASVspoof 2021 LA**：真實 PSTN 傳輸但舊攻擊 → 專職 sim-to-real γ 校準 + robustness，不入主 estimand。〔Verified〕
- **RTCFake**：HuggingFace 頁面明示「not publicly available at this stage」、需挑戰賽註冊後審核，CC-BY-NC-4.0 → **違反免申請 hard gate，排除於 critical path**，開放後至多 exploratory。〔Verified：https://huggingface.co/datasets/JunXueTech/RTCFake ，2026-07-23〕

搜尋詞記錄：「ASVspoof 2021 LA telephony codec conditions C1-C7 PSTN VoIP transmission」「ffmpeg EVS codec 3GPP TS 26.442 encoder open source 2025」「ASVspoof 5 codec conditions C08 C09 C10 C11 narrowband PSTN impulse response」「RTCFake dataset download」「ffmpeg libopencore-amrnb vo-amrwbenc gyan build」「ASVspoof 2021 LA Zenodo keys open access」。

## 對候選研究問題的具體修改

1. estimand 明文定義為「**post-channel 解碼串流的前 τ 秒**」，並寫死評測協定：encode-once/decode-once、每通話單一通道實現、幀界截取。
2. 通道套件預先登記：{8kHz 重採樣, G.711, GSM-FR, AMR-NB, AMR-WB, Opus-NB, ASVspoof5 C11 IR, GE 丟包+PLC}；EVS 除名並列為 limitation。
3. 新增一條輕量 sanity 實驗：ASVspoof 2021 LA C1/C2/C5/C3 上量測「模擬條件→真實 PSTN」效能差，作為 γ 經驗上界寫進 external validity 段。
4. RTCFake 從任何 confirmatory 敘述中刪除。

## Kill conditions

- 若 2021 LA C3 實測顯示真實 PSTN 退化巨大且與所有模擬條件無序關（γ 不可界定），「離線通道模擬支撐來電場景」的敘事崩潰，應退回 proposal-final 原題。
- 若 S 席判定 anytime 風險保證在統計上要求 per-prefix 獨立通道重抽樣（與 encode-once 協定矛盾且無法用多 seed 重複實現調和），我的截取協定需重議。
- 若查實 ASVspoof 5 Zenodo 免費包實際不含 C08–C11 條件音檔（目前僅 protocol 已驗，條件音檔在 eval shards 為 Inference），通道軸須改為自行以已登記套件對 C00 加工生成——這仍可行，但失去「組織者官方條件」的公信力。

## 給下一波的一句話

給 S/A：通道已可零 rig 支撐到「窄頻 codec + 真實 PSTN 響應 + 丟包」且每通話只有一條固定的 post-channel 解碼串流——你們的 sequential estimand 與 policy 請建立在這條單一 sample path 的前綴上，別假設可以重抽通道。
