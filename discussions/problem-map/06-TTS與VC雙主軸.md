# 步驟 06：TTS 與 VC 作為兩條生成主軸

日期：2026-07-26  
狀態：已確認  
上一步：`05-Audio-Deepfake技術時間軸查證.md`

## 本步問題

語音 deepfake 的生成技術，是否可以主要拆成 Text-to-Speech（TTS）與 Voice Conversion（VC）兩條平行發展線？

## 結論

**可以，但結論的適用範圍要限定為「模型產生或轉換的假語音」。**

在此範圍內：

- **TTS：文字 → 語音**
  - 主要改變或產生語句內容。
  - 多說話者、speaker adaptation 與 voice cloning 使輸出可以模仿指定身分。
- **VC：來源語音 → 轉換後語音**
  - 通常保留來源語音的語言內容。
  - 主要改變說話者身分、音色、風格、情緒或其他聲學屬性。

ASVspoof 2019 的 Logical Access（LA）條件使用 17 種 TTS 與 VC 系統產生攻擊，並把 synthetic、converted 與 replayed speech 稱為三種主要 spoofing 形式。由於 replay 是播放／擷取既有語音，而不是生成新的語音內容，因此對「生成技術史」而言，TTS 與 VC 是合理的兩條主軸。

依據：

- [ASVspoof 2019: Future Horizons in Spoofed and Fake Audio Detection](https://www.isca-archive.org/interspeech_2019/todisco19_interspeech.html)
- [ASVspoof 2019 Evaluation Plan](https://www.asvspoof.org/asvspoof2019/asvspoof2019_evaluation_plan.pdf)
- [ASVspoof 2019 fake-speech examples：攻擊類型明列 TTS 與 VC](https://www.asvspoof.org/audio_examples)

## 不能忽略，但不與 TTS／VC 並列為生成主軸的項目

### 1. Replay

- 播放或重新錄製真人／生成語音。
- 它改變的是呈現與擷取路徑，不是語音的生成機制。
- 後續應放入 threat model、channel 或 laundering 分支。

### 2. Speech editing、inpainting、splicing、partial fake

- 只修改一句話中的局部內容，可能混合真人與生成片段。
- 它描述的是「修改範圍或操作方式」，底層生成器仍可能來自 TTS、VC 或新型 generalist speech model。
- 後續可作為跨越 TTS 與 VC 的橫向分支。

### 3. Generalist／hybrid speech generation

- 新型模型可能同時支援 TTS、VC、內容編輯、去噪與 style conversion。
- 因此 TTS／VC 是理解歷史的任務主軸，不一定是現代模型架構的互斥分類。

## 邏輯結構

```text
Audio Deepfake 的產生
├─ 主要生成路線
│  ├─ TTS：由文字產生語音
│  └─ VC：由來源語音轉換聲音
├─ 跨路線操作
│  └─ editing／inpainting／splicing／partial fake
└─ 傳遞與偽裝
   └─ replay／codec／channel／post-processing／laundering
```

這不是完全按照模型架構的 MECE，而是按照「輸入與主要任務」做的第一層分類。現代 generalist 模型可以同時實作多個任務，因此需要另外標示「兩路線開始融合」。

## 對時間軸的決定

- TTS 與 VC 使用兩條平行泳道。
- 每條泳道各自排列技術年代與代表論文。
- 同時支援兩種任務的現代模型，以跨線連結或「融合」節點表示。
- Replay 與 post-processing 不塞入生成技術時間軸，留到 Detection／共同演化的 threat-model 層。

## 下一個單一問題

先從 TTS 泳道開始：TTS 的歷史應依哪些真正改變生成機制與能力的技術轉折分期？

