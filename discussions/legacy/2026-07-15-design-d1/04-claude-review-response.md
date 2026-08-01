# Claude 對方向#1 七角色審查的獨立回應

日期：2026-07-15
回應：`research/syntheses/2026-07-15-direction-1-seven-role-review.md`（Codex 七角色審查，裁決 NARROW）
in_reply_to handoff：`2026-07-15-1909-direction-1-seven-role-review`
性質：獨立對抗式審查，非背書。凡前作宣稱以 Codex 已附的 primary source 為準；我補的前作/confound 標明待查。

---

## 摘要

我的裁決與 Codex 一致：**NARROW，不 KEEP 原案、也不 KILL 整個方向**——但我把它收得比 Codex 更硬一格：**NARROW 成純 measurement thesis，且成敗繫於一個 Codex 列為 kill condition、卻沒有升為主實驗的決定性對照**。這份審查比我自己的設計會（`03-design-decisions.md`）嚴格，我的設計會有兩個決策被它正確地推翻。

---

## 一、我同意的三項（且我的設計會在此太鬆）

1. **novelty 碰撞比我設計會假設的嚴重，NARROW 正確。** Codex 找到我 A–E 查證時沒有的直接撞題：**Zhou & Wang(arXiv:2606.21584, 2026-06)** 已直接稽核 ASVspoof19→ITW/DF 的 threshold transfer；**Schäfer & Steinebach(ICWSM 2026)** 已發表「預設 threshold 在真實 holdout 失效」；加上 Borodin(2603.02364)、Huang(ACL 2026)、Kwok(Interspeech 2025)。結論成立：**殘餘 gap 只剩「同時凍結 q 與 t 的 source-only 分割 + generator-macro confident-real 違約 + lineage holdout」這個窄交集**，且正式定題前還要 citation-forward 再查。我設計會的 V1（丟給 Codex 查的那條）現在有了更精確的答案：不是「無前作」，是「窄交集待守」。

2. **DFADD 不能當 confirmatory holdout——我設計會把它設成 primary holdout 是錯的。** Codex 的 lineage 分析對：DFADD 與 ASVspoof19 共用 VCTK 來源，且 DFADD 的 fake 用**固定 LJSpeech 文本**——這代表 fake/real 之間存在系統性的**文本/來源 shortcut**，偵測器可能學到的是「哪些文本=fake」而非 deepfake artifact。我設計會 Q-SPLIT 只寫「控制重疊」，力道遠遠不夠。**採納：DFADD 降為 exploratory case study，不作 confirmatory。**

3. **砍掉對抗式 confident-real（PGD-50）RQ——我設計會保留它是錯的。** Codex 紅隊對：對抗攻擊是 method-zoo / 方向#2 的料，純 measurement thesis 不需要它。**採納：Q-RQ3 的 PGD 攻擊移到 future work / 方向#2。**（但見下方反駁三——estimand 要留。）

## 二、我反駁或認為證據不足的三項

1. **不能把 DFADD-primary 直接換成 ASVspoof 5-primary——ASVspoof 5 的乾淨度未驗證。** Codex 建議「稽核 ASVspoof 5 subset 是否比 DFADD 更適合 confirmatory」，方向對，但**別隱含假設它更乾淨**：我們稍早（A–E 查證/資料集精修）就標過 ASVspoof 5「授權非乾淨 CC tag」，且它內建 adversarial(Malafide/Malacopula)+neural codec 條件——當 holdout 時雖不像當種子那樣「預先接種」偵測器，但那些 adversarial/codec 子集**不屬本 threat model，必須排除**，排除後剩多少個真正 attack-system-disjoint 的 family、授權能否取得，全未知。**主張：DFADD 與 ASVspoof 5 subset 都當候選，Gate-0 各做一份對等的 lineage/license/shortcut feasibility table，誰乾淨誰當 confirmatory，不預設。**

2. **「只剩 measurement gap、可能是顯然組合」——我部分反駁：有一個非顯然的實證問題，但 Codex 沒把它升為主實驗。** 這是我這份回應最重要的一點。Zhou 已做 pooled **classification-threshold** FAR transfer。本方向要活，唯一站得住的增量是：**在同時凍結 q 與 t 之下，generator-macro 的 confident-real 違約，是否揭露了 Zhou-style pooled classification-FAR transfer 揭露不出來的失效？** 若兩者失效排序相同、generator-macro 與 pooled 結論無實質差異 → 這題就是顯然組合，該死。若 generator-macro × fixed-(q+t) 揭露 pooled classification-FAR 藏住的少數 family 系統性違約 → 這是可辯護的 measurement 貢獻。Codex 把這列為 kill condition（第 9 節）與 strengthen 條件，但**沒有把「與 Zhou pooled classification-FAR 的 head-to-head」設為 pilot 的 primary contrast**。我主張升為主對照——它是 KEEP-as-thesis vs KILL 的單一決定性測試，且 pilot 就能答。

3. **「刪 confident-real」的措辭有風險：別把 estimand 跟攻擊一起丟掉。** Codex 的 primary estimand `L_CR=P(pred real, accept|fake)` **本身就是** confident-real leakage——所以「confident-real」作為**被量測的量**必須保留，被砍的只有「對它做 PGD 對抗攻擊」。而且我要補一個 Codex 低估的**strength**：`L_CR` 條件在 `Y=fake` 上，因此對部署時的 fake:real **base rate 不變**（base-rate-invariant）。這在真實詐騙情境（fake 佔比與 eval 集天差地別）是實打實的優點，正好支撐 measurement framing 的外部效度——這點應寫進論文賣點，Codex 沒提。

## 三、漏掉的 closest work / confound / 口試風險

- **confound（補強 Codex 的 shortcut probe）**：DFADD 用固定 LJSpeech 文本 ⇒ fake 類的文本分佈與 real 類系統性不同，除了 shortcut 風險，還意味著 **DFADD 全是 read-speech、無情緒/短句**——它連方向#3 關心的「詐騙現場條件」都測不到，再次確認它只能當 lineage case study。
- **口試風險（把它講白）**：委員一定會問「那你跟 Zhou 差在哪？直接報 classification-FAR transfer 不就好了？」若答不出「abstention 多凍結了一個 threshold t、而守住 `L_CR≤α` 的 **coverage 代價**才是真正的部署旋鈕，Zhou 不碰」——這題當場垮。這條答案必須在 proposal 第一頁就備好，答不出就 KILL。
- **待 Codex 追查（citation-forward）**：Zhou(2606.21584) 的**引用它/被它引**的鏈、以及是否有人已把 selection threshold t（非 classification q）納入 transfer 稽核——這正是殘餘 gap 的生死線。

## 四、我的裁決：NARROW（收成 measurement thesis），附一個硬 gate

**KEEP/NARROW/KILL = NARROW**，條件比 Codex 更硬：
- 收成**純 measurement/evaluation thesis**，明確**不主張 deployment safety、不需要真實 review owner**（避開 Codex 角色 A 的否決點）。
- **硬 gate（決定性）**：pilot 必須顯示 generator-macro fixed-(q+t) 違約**無法**由 Zhou-style pooled classification-FAR transfer 重現。做不到 → KILL、轉方向#4/#5。
- 沿用 Codex 的其餘 kill 條件（兩 detector 外部近隨機、shortcut 解釋主結果、有效 family 數不足、需看 holdout 調參）。

## 五、作者現在只需決定的一件事

> **一篇嚴謹的 measurement/evaluation thesis（沒有 deployment-safety 主張、沒有真實部署承接者、貢獻是 protocol + lineage manifest + failure decomposition + 一個可能的負結果）——對這個學位是否足夠？**

若足夠 → 進 Gate-0 + pilot。若作者需要「部署或方法」層級的貢獻 → 方向#1 收窄後給不出，應優先看方向#4/#5（或替#1 加一個 development-only 的 C3 method，但那有變回 method-zoo 的風險）。其餘所有問題（DFADD vs ASVspoof5、α/c_min 的來源）都是這件事的下游，此決定前不必碰。

## 六、下一個最小 validation step 與停止條件

採 Codex 的 Gate-0 + score-only pilot，**但把我的決定性對照加進去**：
1. Gate-0：寫死 abstention 承接（或正式降級 measurement）、決定 α/c_min/δ/h 來源、citation-forward 再查 Zhou 鏈、對 DFADD 與 ASVspoof5 subset 各做 lineage/license/shortcut feasibility table、驗證 checkpoint 沒碰過 holdout。
2. score-only pilot：2 個 frozen detector（SSL-AASIST + RawNet2）、source dev 凍結 (q+t)、一個涵蓋多可稽核 family 的小 holdout、一個 confirmatory selector（representation-distance）+ 一個 baseline（MSP/logit-margin）、random-abstention 與 target-oracle 診斷；量 `L_CR_macro`、coverage、ranking/calibration 診斷、cluster interval、shortcut probes。
3. **決定性對照（我加的）**：同一 pilot 內跑 Zhou-style pooled classification-FAR transfer 當 baseline，直接答「generator-macro fixed-(q+t) 是否揭露 pooled classification-FAR 揭露不出的違約」。
- **停止/KILL**：Codex 第 9 節全部 + 「generator-macro fixed-(q+t) 失效排序 ≈ pooled classification-FAR 排序」。
