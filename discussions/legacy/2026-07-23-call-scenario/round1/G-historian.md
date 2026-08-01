# G-historian 文獻史官席 — Round 1 發言

日期：2026-07-23。所有 Verified 均為本日 web 查證。

## 立場摘要

1. 「streaming 前綴早期判定 × selective 棄權（帶風險承諾）× 輕量化 × 未見生成器」四交集在我的搜尋範圍內**仍然空著**——不 kill。
2. 但周邊正被快速包圍：ICASSP 2026 已有論文佔下「來電開場超短音訊偵測」灘頭；若本題的貢獻退化成「短音訊上比 EER」，closest-work 直接撞死。
3. Gap 必須錨在 **sequential/anytime 判定與風險控制的 commit-time**，不是短音訊辨識力。
4. 電話通道軸有現成離線資源（ASVspoof 5 C08–C11 含 8kHz 窄帶與 PSTN 模擬），不需自建 rig。

## 主體分析

### 最接近的工作（依威脅程度排序）

**(1) Shi et al., "Audio Deepfake Detection at the First Greeting: 'Hi!'"（ICASSP 2026, arXiv:2601.19573, 2026-01-27 提交）** — **Verified**（https://arxiv.org/html/2601.19573，查證 2026-07-23）。針對 0.5–2.0 秒超短音訊、明確以「詐騙者開場問候」為場景，提出 S-MGAA，主打低 RTF、少參數、edge 部署。**重疊面**：來電動機、超短前綴、輕量化——三項全撞。**未覆蓋**：摘要層面無 sequential decision（它把 0.5s/1s/2s 當固定長度分別評測，不回答「聽到第幾秒才有資格 commit」）、無棄權/selective policy、無凍結門檻下的風險保證。這是頭號 closest work，論文寫作時必須正面引用並劃界。

**(2) RTCFake（ACL 2026, arXiv:2604.23742, 2026-04-26 提交）** — **Verified**（https://arxiv.org/abs/2604.23742，查證 2026-07-23）。約 600 小時、經 Zoom 等真實 RTC 平台傳輸的 deepfake 資料集 + phoneme-guided consistency learning，評測含未見平台與未知噪聲。**重疊面**：真實通訊通道。**未覆蓋**：偵測仍是 utterance 級離線判定，無早期判定、無棄權、無輕量化軸。注意：這證明「經通道傳輸的 ADD 資料集」已有人做且免自建 rig 的替代品存在。

**(3) Delgado et al., "On Deepfake Voice Detection — It's All in the Presentation"（arXiv:2509.26471, 2025）** — **Verified**（https://arxiv.org/abs/2509.26471，查證 2026-07-23）。論證 raw deepfake 與「經呈現通道（電話播放/注入）」的 deepfake 分佈差異是泛化失敗主因，提出資料建構框架，宣稱在更真實 setup 下提升 39% 準確率，附公開 test protocol（GitHub: CavoloFrattale/deepfake-detection-test-protocol）。**重疊面**：電話通道現實性論證，可直接引為 motivation。**未覆蓋**：無 streaming、無棄權、無輕量化。其方法依賴實體 calling pipeline——正是我們硬約束禁止的路線；**Inference**：這反而支持「用 ASVspoof 5 離線通道條件替代」的設計。後續動向：搜尋未見其團隊 2026 年的直接續作（**Unknown**，可能只是我沒搜到）。

**(4) PartialSpoof 系（TASLP 2023, arXiv:2204.05177）及 2025 後續** — **Verified**（https://arxiv.org/abs/2204.05177；後續如 PET ICASSP 2025、LENS-DF arXiv:2507.16220、frame-level temporal difference arXiv:2507.15101，查證 2026-07-23）。segment 級標注細至 20ms，2025 年已發展成「manipulated region localization」子領域（survey: arXiv:2506.14396）。**重疊面**：sub-utterance 時間解析度。**關鍵區別**：它們是**事後回看完整音訊做定位**，非因果前綴上的早期判定；判定語意是「哪段是假」而非「何時有資格說」。

**(5) 短音訊長度效應文獻（"how much audio" 的既有形態）** — **Verified**：AASIST2（arXiv:2309.08279）明確處理短 utterance 劣化；文獻共識為 0–2 秒 EER 常升破 10%（查證 2026-07-23）。**含義**：「長度 vs 效能」曲線已有人畫過（作為 ablation），所以單畫曲線不是貢獻；把長度變成 **anytime 決策變數並掛上風險保證**才是未被佔的位置。

### 交集各腿的單獨現況

- **Early-exit/anytime 推論在語音**：存在（HuBERT-EE、DAISY arXiv:2406.05464、Temporal early exiting for streaming speech commands ICASSP 2022、ED-SKWS Interspeech 2024；查證 2026-07-23）——但目標是**省算力**，不是風險控制的 commit-time；且未見用於 ADD（**Unknown**：窮舉不足）。
- **Sequential testing / anytime-valid inference**：e-value/e-process 統計文獻成熟且活躍（如 "Anytime validity is free", JRSS-B 2026, arXiv:2501.03982；查證 2026-07-23），但**未搜到任何音訊分類/ADD 應用先例**。這是方法論搬運的空位，也是 S-sequential 席的主戰場。
- **棄權在 ADD**：存在但非 streaming——ReTA（arXiv:2412.01425，open-set 屬性歸因的 reject 門檻自適應）、FADEL、Kwok ensemble confidence（proposal-final 已引）。
- **電話通道評測資源**：**Verified**（https://arxiv.org/html/2502.08857，查證 2026-07-23）：ASVspoof 5 官方條件 C00–C11，其中 C08–C10 為 8kHz 窄帶 Opus/AMR/Speex，**C11 為八組端到端 PSTN 撥打管線的預錄非線性響應卷積**——即「電話通道軸」已內建於 primary confirmatory 資料集，免申請、免 rig。這對候選問題是重大利多。

### 殘餘 gap 的 bounded wording（建議措辭）

「在已記錄的搜尋範圍內，未見同時具備以下四者的工作：(i) 因果前綴上的 anytime 三態判定（非固定長度截斷評測）；(ii) source-frozen 且帶風險承諾的棄權策略；(iii) 部署級輕量模型；(iv) documented lineage-disjoint 未見生成器評測。最接近的 Shi et al. 2026 覆蓋 (iii)+超短音訊但按固定長度評測且無棄權；PartialSpoof 系覆蓋 sub-utterance 解析度但為事後定位；anytime-valid 統計工具成熟但未見音訊分類應用。」

### 搜尋範圍限制（誠實條款）

搜尋為英文、US-region、arXiv/Google 為主；未系統掃 Interspeech 2026 錄取清單、ISCA archive 全文、IEEE Xplore 付費牆內容與中文期刊；「未搜到 sequential testing 用於音訊」屬**弱否定**——SPRT 在語音活動偵測（VAD）、關鍵詞確認等老文獻可能有先例，正式寫作前需補一輪系統性檢索。搜尋詞記錄：`streaming real-time audio deepfake detection low-latency 2025 2026`、`PartialSpoof segment-level spoof detection follow-up 2025`、`"early exit" audio anti-spoofing deepfake`、`"utterance length" short duration audio deepfake detection`、`arXiv 2509.26471 Delgado telephone`、`sequential probability ratio test anytime-valid audio classification e-value`、`ASVspoof 5 codec conditions telephone 8kHz C00`、`audio deepfake abstention selective prediction streaming`、`"early exit" anytime inference speech keyword spotting`、`anti-spoofing duration short utterances EER degradation`。

## 對候選研究問題的具體修改或否決

不否決，但修改定位：候選問題的可辯護核心是「**commit-time 作為 selective policy 的新維度**」，不是「短音訊偵測」。建議把問題句從「聽到第幾秒才有資格判定」精化為「凍結的 anytime 三態策略在未見生成器與電話通道條件（ASVspoof 5 C08–C11）下，其 commit-time／coverage／leakage 三方權衡是否守得住承諾」——這與 proposal-final 的 `Δ_light`、UCB policy 機器可直接銜接，屬推廣而非改行。

## Kill conditions

- 若正式檢索發現任一篇同時做「因果前綴 + 棄權 + 風險保證」的 ADD 工作（特別注意 Interspeech/ICASSP 2026 與 ASVspoof workshop），本席支持的 gap 即失效，退回 proposal-final。
- 若 Shi et al. 的完整版（非摘要）實際上已含 sequential commit 機制，同上。
- 若 S-sequential 席判定 anytime-valid 工具在相依音訊幀上無法給出非平凡保證（前綴分數高度自相關），則「風險承諾」這條腿斷，gap 退化為又一篇短音訊評測——應 kill。

## 給下一波的一句話

灘頭已有人搶（"Hi!" 佔超短音訊、RTCFake 佔通道），唯一還空著的是「什麼時候有資格開口」的統計判定學——S 席請確認相依前綴上的 anytime 風險保證做不做得出來，那是這個題目唯一的命脈。
