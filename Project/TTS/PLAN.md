# 七階段 TTS 實作規劃與完成狀態

日期：2026-08-01

## 目標

建立七個 TTS 歷史階段的可播放語音；七段使用完全相同的英文句子，保留 raw 輸出，再製作規格與音量一致的 comparison playback 檔。

## 實作流程

1. 鎖定共同句子、語言、mono 與播放格式。
2. 查核 Stage 1–3 的官方／原作者程式、授權與可編譯性。
3. 在 Windows 本機建立 Cygwin/MinGW 專案工具鏈。
4. 編譯 KLSYN、Flite、hts_engine 與 Flite+hts_engine。
5. 用 Stage 1–3 各自的歷史引擎生成同一句話。
6. Stage 4–6 採用作者頁面已公開的同句展示音檔。
7. 以 F5-TTS 官方權重在 RTX 3060 本機生成 Stage 7 同句語音。
8. 將七個 raw 檔轉成 24 kHz、mono、PCM16、whole-file RMS 0.065。
9. 驗證七段音檔存在、有效、長度大於 0.5 秒且非靜音；輸出 manifest 與聆聽頁。

## 完成狀態

- [x] Stage 1 KLSYN 本機編譯與生成
- [x] Stage 2 Flite diphone 本機編譯與生成
- [x] Stage 3 HTS 本機編譯與生成
- [x] Stage 4 Merlin 同句官方音檔
- [x] Stage 5 Tacotron 2 同句官方音檔
- [x] Stage 6 FastSpeech 同句官方音檔
- [x] Stage 7 F5-TTS 官方權重本機 GPU 推論
- [x] 七段相同文本驗證
- [x] 七段統一播放格式與音量
- [x] manifest、文件與聆聽頁

## 無法消除的控制限制

「相同文本」與「相同播放規格」已完成；「完全相同的 speaker identity」無法跨七個時代成立。原因是 Stage 1 不具 learned speaker identity，而各歷史系統也沒有共用同一 speaker 的 voice/checkpoint。這組音檔適合展示方法演進與主觀聆聽，不應宣稱為只改變模型架構的嚴格 MOS benchmark。
