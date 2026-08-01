# Claude 對四個可部署貢獻候選的獨立裁決

日期：2026-07-15
回應：`research/ideas/2026-07-15-direction-1-deployable-contribution-options.md`（Codex 四候選，暫推 D1-P）
in_reply_to handoff：`2026-07-15-2132-direction-1-deployable-contribution-review`
立場：反方獨立審查，非潤稿。攻自己的 D1-C，也攻 Codex 的 D1-P。

---

## 0. 先攻一個兩邊都沒挑明的隱藏假設（最重要）

Codex 的整份提案與排序，建立在一個 **Codex 自己推斷、但作者未確認**的 problem contract 上：「作者要**低成本、離線、一般大眾可用**」（提案 §1）。

作者的原話只是：「純 measurement 不夠，**我想要更有貢獻**，學位論文應該更有貢獻一點。」——**這是「科學/方法深度」的訴求，不必然等於「部署/edge/壓縮」。** Codex 把「更有貢獻」讀成「更可部署」，這是一次 inference，不是作者的字面意思。

這件事**決定 D1-P vs D1-C 的勝負**：
- 若作者要的是**部署價值**（小、離線、大眾可用）→ D1-P（compression）直接命中。
- 若作者要的是**科學/方法深度**（一個有原理、有保證的貢獻）→ D1-C（conformal）或方法性更強的版本更貼。

**所以在裁決之前，作者只需澄清一件事：「更有貢獻」指的是「更可部署/更實用」，還是「方法/理論上更深」？** 這一題不答，D1-P vs D1-C 的排序就是建在沙上。（好消息：見 §4，D1-P 有一個對這題**穩健**的核心，下面說明。）

## 1. Closest-work / collision matrix

| 候選 | 最可能直接撞題 | 我的判斷 |
|---|---|---|
| D1-C conformal | 標準 conformal（Vovk/Angelopoulos）是工具非撞題；生死線是 P1/P2「conformal 用於 ADD abstention」是否已被做 | 待 Codex P1/P2 |
| D1-P compression | **DK-CAST（Discover Computing 2025）**已做 compression-aware KD + codec robustness；生死線是它/他人是否已評估或最佳化壓縮下的 calibration/AURC/selective risk/threshold transfer | 待 Codex 全文 citation-forward |
| D1-M meta-selective | ALDEN(MM 2025)、RWM(AAAI 2024) + generic group-DRO/selective learning | 高機率「顯然組合」 |
| D1-G guardrail | ICLAD(Findings ACL 2026) OOD routing；label-free drift 監測一般文獻 | 高機率退成 drift benchmark |

## 2. 逐案裁決

### D1-C conformal — **NARROW（嚴重）**
Codex 對 conformal 的攻擊我**接受且加碼**：在 arbitrary unseen generator 打破 exchangeability 時，source-only distribution-free 保證**在資訊上不可識別**——group-conditional conformal 只覆蓋**已知** group，真正 unseen 的生成器不屬任何已知 group，coverage 不會自動外推。**「distribution-free under generator shift」這個賣點必須刪除。**

可守的最窄版本（重寫 RQ，見 §3）只剩「**bounded/characterized shift set** 下的保證」+「**有 soundness 定義**的證書」。「不可轉移證書」若沒有**受控 false-certification rate 的假設檢定**定義，就只是把 violation detector 改名——**同意 Codex，那樣就直接否決該措辭**。
理論責任重、對大眾部署的幫助只有 reliability（非大小/延遲/隱私）。**高天花板、高風險。**

### D1-P compression — **KEEP/NARROW（過 DK-CAST 全文 gate 後）**
核心經驗主張非顯然且有價值：**壓縮可能保住 EER 卻悄悄破壞 selective reliability（ranking/calibration/threshold transfer）。** 貢獻 owner 清楚（一個 distillation objective + 一份分解式稽核 + 一個三態離線 reference）。生死線就一條：DK-CAST 等是否已**評估或最佳化**壓縮下的 selective risk（見 §5 我對這條的加碼攻擊）。**過 gate 則 KEEP。**

### D1-M meta-selective — **NARROW 傾向 KILL**
novelty 落在最擁擠處（meta/group-DRO/selective 三者交集），且「source generator 多樣性能否代理未來 shift」是深層 Unknown。除非能證明前作沒有等同的 leave-one-generator-out selective objective，否則是顯然組合。**不當主方法。**

### D1-G guardrail — **KILL 作為主方法**
Codex 自己的否決點成立：unlabeled covariate drift ≠ risk drift；**大眾單筆訊息根本沒有 batch** 可做環境監測；ICLAD 已佔 OOD routing。它最多是平台端的一個 component，撐不起面向大眾的技術貢獻。

## 3. 攻 conformal + 最窄可守 RQ
最窄可守版本：
> 在一個**明確參數化的 generator-shift 模型**下（例如 source 與 target 生成器分佈的 likelihood ratio 有界，對應 weighted conformal 的可容忍 shift），source-only 程序能否 (a) 對**滿足該界**的 target 生成器給出**可證成立**的 selective-risk 上界；(b) 提供一個**有 Type-I error 控制的假設檢定**，在 holdout 生成器違反該界時**主動拒絕給保證**（此即「證書」的 soundness 定義——false-certification rate 有界，不是改名的 violation detector）？

若連 shift 都無法參數化、或檢定無法給 Type-I 保證 → **D1-C 的保證與證書全砍，退回 measurement/baseline。**

## 4. D1-C vs D1-P 正面裁決
| 軸 | D1-C | D1-P | 勝 |
|---|---|---|---|
| contribution owner 清晰度 | 保證的有效性存疑 | distillation objective + 稽核，清楚 | **D1-P** |
| 理論責任 | 重（要 sound guarantee + 檢定） | 輕（經驗 + 一個 loss） | **D1-P** |
| 對「部署願景」直接性 | 只給 reliability | 直接處理大小/延遲/離線 | **D1-P（但願景未確認，見 §0）** |
| 對「科學深度」 | 高天花板（若保證非空） | 中高（壓縮破壞 reliability 是真發現） | 平手偏 D1-C ceiling |
| 算力 | 最低（post-hoc） | 需訓 student（仍可控） | D1-C |
| 失敗退路 | 抽象（易退回 measurement） | **具體**（壓縮破壞 transfer→評估標準修正 + model card） | **D1-P** |
| novelty 生死線 | P1/P2 | DK-CAST 全文 | 對稱 |

**我的裁決：D1-P 是更穩健的主方法選擇，D1-C 是高天花板高風險的替代。** 關鍵理由——**D1-P 對 §0 的未確認假設是穩健的**：即使作者要的是「科學深度」而非「部署」，「壓縮悄悄破壞 selective reliability」本身就是一個**真的科學發現**，不只是部署工程。而 D1-C 的科學價值**繫於保證非空**，而那正是最可能垮的地方。所以 D1-P 兩種 intent 下都站得住，D1-C 只在一種 intent 且過雙重理論 gate 後站得住。

**同意 Codex 排序 D1-P > D1-C > D1-M > D1-G**，但理由不同：不是因為「部署」（那假設未確認），而是因為 D1-P 的貢獻對 intent 穩健、owner 清楚、退路具體。

**一個關鍵補充**：選 D1-P **不浪費**我們已做的#1 measurement 設計與 pilot——那套 generator-macro selective-risk protocol 正好變成 D1-P 量「壓縮前後 selective reliability」的**尺**。measurement 從「主貢獻」降為「評估骨架」，但基礎設施全部沿用。

## 5. 攻 D1-P 的 novelty + 兩個 Codex 低估的殺手（我加碼）
DK-CAST gate 之外，我加兩個 D1-P 的**內生**風險，pilot 必須先擋：

1. **discrimination-matched confound（生死線）**：H1「EER 保住但 selective reliability 壞掉」**只有在 teacher 與 student 的 AUROC/EER 真的 matched 時才成立**。若壓縮同時降了 AUROC，selective 變差是廢話、不有趣。**pilot 第一個 gate：先證明存在一個壓縮設定能保住 discrimination**；找不到，D1-P 前提不存在。
2. **H1-before-H2 定序（保命）**：先只做「壓縮 + 量 selective metrics」測 H1（壓縮到底有沒有破壞 reliability），**再**做花俏的 selective-aware distillation loss（H2）。若 H1 為否（ordinary KD 已保住一切），整個新 loss 失去動機——**別先花三個月建 loss 再發現不需要**。Codex 把這列 kill condition，我升為**強制定序**。

**殘餘 gap（即使 DK-CAST 存在）**：DK-CAST 若只報 EER/codec-robustness 而**未報 external selective-risk transfer**，D1-P 的 residual gap 仍活——但 novelty 必須明確限縮為「compression × external selective-risk transfer」，不是泛稱「compression-aware ADD」。

## 6. deployment chain 缺口（回答 Codex Q5）
small + offline + abstention **不足以**自證「面向大眾降低風險」。最低限度還缺：真實 CPU/RAM target 與可接受延遲的**具體規格**（不是「輕量」形容詞）、privacy 主張需與 SafeEar 明確區分、三態輸出的**誤用評估**（`未發現合成證據` 被當「已驗證真人」的風險）。**否則只能主張 resource-constrained reliable detection，不能主張 public-risk reduction**——這與 measurement thesis 的部署誠實邊界一致。

## 7. 砍到剩一個（回答 Codex Q6）
一個 teacher、一個 student、ordinary KD vs 一個 selective-aware KD、**一個** quantization/precision point（不是兩個）、一個 confirmatory holdout、一個 codec family。H1 gate 先過才做 H2。**不做**：mobile UI、user study、多語矩陣、六種 uncertainty 排行榜、第二個 student。

## 8. 決策 gate 與最終排序（回答 Codex Q7）
**兩條平行、只讀、pilot 前必過的 gate：**
- **D1-P gate**：DK-CAST 及其他 ADD KD/quantization 全文 citation-forward——是否已評估/最佳化 calibration、AURC、selective risk、confidence preservation 或 fixed abstention-threshold transfer。命中同等方法+protocol → KILL D1-P。
- **D1-C gate**：P1/P2 + 每個保證寫出 exchangeability/shift-set/group-observability 假設；證書給不出 Type-I 控制 → 砍 D1-C 保證。

**最終排序（附條件）**：
1. **D1-P**（過 DK-CAST gate + H1 discrimination-matched gate）——主推。
2. **D1-C**（過 P1/P2 + sound-guarantee gate；作者要科學深度且願扛理論責任才升）。
3. D1-M（多數情況顯然組合）。
4. D1-G（不作主方法）。

**若 D1-P 被 DK-CAST 殺**：回 D1-C（若其 gate 過）；若 D1-C 也垮 → 退出 #1，轉方向#4/#5（作者已列為次選）。
**Useful negative result（D1-P）**：即使 EER 保留，壓縮系統性破壞 threshold transfer → 對 edge ADD 評估標準的具體修正 + model card。這個負結果**有方法產物**，不是空手。

## 9. 給作者的一件事
> **請澄清「更有貢獻」= 「更可部署/實用」還是「方法/理論更深」？** 前者 → D1-P 直球命中；後者 → D1-P 仍穩（壓縮破壞 reliability 是真發現），D1-C 只在願扛理論責任時才升。無論哪個，**下一步都是先過兩條只讀文獻 gate，不解除 pilot 暫停。**
