# Research Tasks

Last updated: 2026-08-01

## Now

<!-- The problem-map reset is the active work. The previous D1 execution gates
remain below as paused historical tasks until the map revalidates that branch. -->

- Build the audio deepfake detection problem map step by step under `discussions/problem-map/`, using one numbered Markdown record per completed reasoning step.
- Build the confirmed historical structure as two parallel timelines - Audio Deepfake and Detection - plus a co-evolution layer linking new forgery capabilities to invalidated detection assumptions and responses.
- TTS and Voice Conversion are confirmed as parallel generation swimlanes. Validate the period boundaries separately for each lane before adding detailed periods and papers to the Markmap; show modern generalist/editing systems as cross-lane nodes.
- The TTS timeline now contains seven nodes after validating the 2000-2017 gap: HMM statistical parametric (2000), DNN/RNN statistical parametric bridge (2013), then neural end-to-end (2017). Freeze further TTS corpus expansion; complete the seven-anchor Audio Deepfake capability extraction as a short closeout while the VC lane proceeds.
- Start a Voice Conversion technology-history survey with an unrestricted metadata candidate pool, a 15-paper anchor pilot, a 35-paper full-text core, and expansion to roughly 70-100 papers only while new mechanisms, counterexamples, or period-boundary evidence continue to appear. Select historical anchors using citation impact within comparable publication-age cohorts, authoritative peer-reviewed venues, and demonstrated role in a technical transition; do not rank papers by raw citation count alone. Record the citation source and retrieval date, publication status, DOI or official proceedings page, inclusion reason, and exclusion reason. Download legally available full texts only after bibliographic verification into `papers/vc-history/`, with a provenance manifest in `papers/vc-history/README.md`.
- Treat the seven TTS nodes as overlapping technical trend groups rather than strictly disjoint year bins. A verified 35-paper download and reading set (five papers per group) is recorded in `research/syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md`.
- A ten-scope logical gap analysis over the 35-paper closed corpus is complete under `research/validations/2026-07-31-tts-35-scope-gap-analysis/`. Each scope separates verified findings, closed-corpus residual gaps, search-only leads, explicit no-gap verdicts, and stop conditions. Next, externally validate only the retained candidates; do not treat closed-corpus absence as field-level novelty.
- The set is now expanded to 100 papers in `research/syntheses/2026-07-27-tts-100-paper-collection-list.md`, scoped to TTS synthesis technique evolution only. 87 of 100 have venue, year, and DOI or official proceedings confirmed, and 87 PDFs are in `papers/tts-history/` under a `001`-`100` naming scheme. Four prior records were corrected: VALL-E is now a 2025 IEEE TASLP journal paper rather than a preprint; #012 is ATR mu-talk; #093 UniAudio's ICML title differs from its arXiv title; #009 exists as both SSW2 1994 and an IJST 1997 journal version. Thirteen papers remain unobtained, almost all behind institutional paywalls, and twelve ICLR/ICML/NeurIPS entries still need their formal proceedings record confirmed.
- All 35 TTS-history PDFs have been obtained and format-checked under `papers/tts-history/`; provenance and the corrected T4-01 file are recorded in its `README.md`. Next, extract from each of the seven anchor papers its prior-generation problem, input/output representation, generation mechanism, speaker conditioning, author-stated limitations, and newly enabled Audio Deepfake capability. Use the other 28 papers for within-group validation only after the anchors support the proposed transitions.
- Obtain the title, DOI, link, or first page of the paper the author must present, then place it in the historical map and prepare a separate paper analysis.
- Require every retained question node to state its parent, logical basis, required evidence, and evidence status.

## Next

- After the author confirms the generation periods, add them to the formal problem map and build the Detection timeline using the same publication-status and evidence-label rules.
- Verify the pre-2013 origins of speaker-verification spoofing research and compare the task definitions of ASVspoof 2015, 2019, and 2021.
- Propose historical periods only after at least two dimensions change together; ask the author to confirm the periods before adding them to the visual map.
- After the historical branch is stable, proceed to stakeholder, decision, target-claim, threat-model, and available-evidence branches.
- Use current primary literature to validate retained branches; do not infer novelty from sparse local coverage.

## Previous direction — paused pending problem-map review

- Send proposal v2 (`research/ideas/2026-07-17-provisional-thesis-proposal-v2-calibration-transfer.md`) to the senior/advisor and ask whether beating ordinary KD + source-dev recalibration is a thesis-level contribution bar, whether journalists/fact-checkers are the right primary stakeholder, and whether H1-only measurement is an explicit pivot rather than the intended thesis.
- Specify the two-week score-only H1a/H1b gate: frozen SSL reference, truncated-layer probe and at most one ordinary-KD student; model-specific source-dev calibration and `(q_m,t_m)` at the same operating constraint; matched AUROC/eAURC; generator-macro confident-real leakage; mandatory ordinary-KD+temperature-scaling baseline plus affine/Platt sensitivity; explicit kill conditions. Do not design H2 beyond a mechanism sketch before both gates survive.
- Treat lineage as a Phase-0 blocker. Audit ASVspoof 5 selected C00 first (8 non-adversarial/non-legacy IDs, conservatively 7 architecture families), and the corrected 2025-04 DFADD release as exploratory, for L0-L5 generator lineage, checkpoint/data leakage, speaker/content/source overlap, licenses, hashes, deduplication, and dataset shortcuts.
- Complete the remaining fixed-threshold P3 citation-forward check (Schäfer and Steinebach; Zhou and Wang; Borodin et al.; Huang et al.) and the P4 ASVspoof 5 lineage/license gate; the D1-P DK-CAST gate and D1-C conformal P1/P2 gate are complete in `research/validations/2026-07-17-d1p-d1c-literature-gates.md`.
- Freeze a preregistration-ready score-only protocol only after advisor-interest, ASVspoof 5 lineage, and small-cluster precision/power gates pass; pilot execution remains paused.

### Conditional continuation of the paused direction

- If the advisor agrees the provisional contribution is thesis-level and Phase 0 passes, run the minimal H1a/H1b score audit without tuning layers, thresholds, calibration, or preprocessing on the holdout.
- If H1a fails, kill D1-P; if source-dev TS/Platt repairs the failure, kill H2; only if both gates survive, run a method-specific closest-work check and specify one correctness-aware operating-point or clean-codec selection-consistency objective against ordinary KD, KD+TS, and KD+Platt.
- Keep D1-C conformal as a baseline/backup only; do not claim source-only distribution-free guarantees under arbitrary unseen-generator shift.
- Decide whether direction #1 becomes the thesis, narrows to a measurement/evaluation thesis, pivots to dataset-shortcut/evaluation validity, or is killed by the documented stop conditions.
- Only after a direction is selected, create an implementation and experiment plan.

## Later or optional

- Design a warning-interface pilot and conduct power analysis.
- Prepare an IRB protocol if a human-subject study remains part of the selected scope.
- Extend the technical evaluation to real communication channels.

## Stop conditions for ideation

Move from ideation to implementation only when one candidate has:

- documented closest prior work and a defensible residual gap;
- available data and at least one runnable baseline;
- explicit primary metrics and threat model;
- a one-year minimum scope and a useful negative-result fallback;
- advisor approval.
