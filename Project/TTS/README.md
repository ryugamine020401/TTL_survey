# 七個時代的本機 TTS

輸入一段英文，網頁會用七種不同時期的方法各產生一段語音。所有程式、模型與輸出都留在這個專案內，不需要上傳文字或音檔到雲端。

## 使用方式

第一次使用，先安裝環境並下載模型：

```powershell
.\scripts\setup_interactive.ps1
```

完成後啟動本機網站：

```powershell
.\serve.ps1
```

瀏覽器會開啟 `http://127.0.0.1:8000`。輸入英文後，可以單獨生成某一階段，也可以一次生成全部七個階段並直接播放或下載。

目前限制：只接受英文 ASCII 文字，最多 300 個字元。Stage 5 使用逐點生成的 WaveRNN，通常需要等待約 1–2 分鐘。

## 七個階段

| 階段 | 本機實作 | 簡單理解 |
|---:|---|---|
| 1 | KLSYN + rsynth rules | 用人工規則控制聲音的共振參數 |
| 2 | Flite kal16 | 拼接預先錄製的雙音素單元 |
| 3 | Flite + HTS | 由 HMM 預測聲學參數再合成 |
| 4 | Tacotron 2 + Griffin-Lim | 神經網路預測頻譜，再由傳統演算法還原波形 |
| 5 | Tacotron 2 + WaveRNN | 自回歸模型逐步產生語音 |
| 6 | FastPitch + HiFi-GAN | 平行產生頻譜與波形，速度較快 |
| 7 | F5-TTS v1 Base | 參考短語音提示後產生新的語音 |

Stage 4 是用來呈現「神經聲學模型 + 傳統波形重建」的過渡方法，不宣稱是 Merlin 原始 voice。Stage 1–3 使用歷史原始碼或官方實作；Stage 4–7 使用公開模型在本機推論。

## 檔案位置

- 模型與第三方原始碼：`.cache/`、`vendor/`
- 生成的聲音：`output/interactive/`
- 本機網頁：`listen.html`
- API 與合成流程：`src/local_app.py`、`src/interactive_engines.py`

這些大型模型、執行環境與生成音檔已由 `.gitignore` 排除，不會跟著程式碼推上 GitHub。
