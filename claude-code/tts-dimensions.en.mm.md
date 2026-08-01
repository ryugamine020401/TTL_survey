---
title: TTS Evaluation Dimensions
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 3
  maxWidth: 320
---

# TTS Evaluation Dimensions

## Layering principle

- Single sample vs output distribution → A vs B
- Reference / conditioning required? → sub-axes inside A
- Audio vs system vs social consequence → A/B vs C vs D
- **The original 8 items sit at different levels; listing them in parallel misleads**
- Report as an **A×B matrix**; C in the header as budget; D in its own section

## A. Output quality (per-sample)

### A1 Intelligibility & text fidelity

- Q: did it say the right words?
- Sub-items
  - Phonetic correctness · heteronyms
  - Number & abbreviation normalization (TN)
  - Code-switching · loanwords
  - Hallucinated insertions · skipping
- Metrics
  - WER／CER via ASR transcription
  - Phoneme error rate
  - Intelligibility MOS
  - TN／G2P accuracy
- Pitfalls
  - ASR is itself biased — not human intelligibility
  - Low WER may mean over-normalization

### A2 Naturalness & signal quality

- Q: does it sound like a real recording?
- Sub-items
  - Prosodic naturalness · segmental quality
  - Artifacts: metallic timbre · buzz · discontinuities
  - Bandwidth／sample rate
- Metrics
  - Subjective: MOS · CMOS
  - No-reference automatic: UTMOS · NISQA · DNSMOS
  - Reference-based: PESQ · ViSQOL (reconstruction tasks only)
- Pitfalls
  - MOS not comparable across papers — within-test only
  - Automatic MOS predictors fail out of distribution
  - Listeners conflate "natural" with "similar to reference" → ask MOS and SMOS separately

### A3 Conditional conformance

- **Key merge: similarity and controllability are two forms of one axis**
  - Both ask "does it conform to the specified condition?"
  - Differ only in how the condition is expressed: reference audio vs value／label
  - Share one conditioning mechanism; routinely trade off

#### A3a Reference-driven (similarity / implicit condition)

- Sub-items
  - Speaker timbre · accent
  - Emotion · prosodic style
  - **Recording／channel environment**
- Metrics
  - SMOS
  - SECS speaker-embedding cosine (WavLM／ECAPA)
  - Accent／emotion classification accuracy
  - F0 RMSE／correlation · duration correlation · DTW
  - Channel match: RT60 error · SNR match
- Pitfalls
  - Highly encoder-dependent — rankings invert across encoders
  - High SECS ≠ perceived similarity
  - Environment similarity ignored yet decides "same recording?"

#### A3b Label-driven (controllability / explicit condition)

- Sub-items
  - Total duration · speaking rate
  - F0 shift／range
  - Pause placement & length · emphasis
  - Style／emotion intensity
- Metrics
  - Control error: target vs measured
  - **Control range** (attainable interval)
  - **Disentanglement** (drift in others when one is changed)
- Pitfalls
  - "It is controllable" without range and disentanglement = overstatement
  - Naturalness collapses at extremes → report quality-vs-control curves

## B. Reliability (distribution-level)

- **Not new properties — different readings of A**

### B1 Robustness = the tail of A

- Q: how bad is the worst case, how often?
- Failure modes
  - Skipping · repetition · early truncation
  - Long-form drift · runaway generation
  - Seed sensitivity
  - Adversarial inputs: very long sentences · bare digits · odd punctuation · code-switching · empty
- Metrics
  - Failure rate per N utterances
  - **P95／P99 of WER, not the mean**
  - Quality-drift curve over long-form synthesis
  - Cross-seed variance
- Pitfalls
  - Never represent robustness by a mean
  - Clean short-sentence test set = meaningless number
  - AR and NAR fail differently → design separate probes

### B2 Generalization & data efficiency = A out of domain

- Sub-items
  - Unseen speakers · unseen languages／accents
  - Cross-domain: read vs spontaneous
  - Cross-recording-condition · low-resource languages
  - Seconds of enrollment for few-shot
- Metrics
  - Same A metrics, in-domain／out-of-domain columns
  - Data-volume-vs-performance curve
  - Enrollment-seconds-vs-similarity curve
- Pitfalls
  - Unseen speaker from the same corpus is still in-domain — **cross-corpus counts**
  - "Only 3 seconds" as a single point is not comparable — report the curve

## C. System cost (content-independent)

### C1 Efficiency & deployment

- Sub-items
  - Time-to-first-byte · real-time factor
  - Streaming throughput
  - Parameter count · peak memory
  - Post-quantization behavior
  - On-device power & thermals
- Metrics
  - Numbers **plus explicit hardware and batch settings**
  - A-axis before／after quantization
- Pitfalls
  - Efficiency unbound to quality is meaningless → report "A under an X latency budget"
  - Streaming and offline quality differ — do not cite for each other

## D. Sociotechnical (opposite direction to A–C)

### D1 Safety, misuse & detectability

- Sub-items
  - Non-consensual voice impersonation
  - Voice fraud · social engineering
  - Bypassing speaker verification (ASV spoofing)
  - Synthetic-speech detection
  - Provenance & watermarking
  - Consent & authorization
- Metrics
  - Detector EER／min-tDCF **under unseen generators**
  - ASV attack success rate
  - Watermark survival (compression／re-recording／time-stretch) ＋ imperceptibility
  - Residual detection rate after adversarial laundering
- Pitfalls
  - **Runs opposite to A–C — cannot be summed into one score**
  - Detection on seen generators severely overstates capability
  - Watermarking guarantees provenance ≠ passive detection guarantees real/fake — not substitutes

## Trade-offs (no axis optimizes alone)

- A1 ↔ A2: low WER → flat prosody; expressiveness → more mispronunciation
- A3a ↔ A2: cloning a noisy reference means reproducing the noise
- A3b ↔ A2: the more extreme the control, the worse the naturalness
- A3a ↔ A3b: strong reference conditioning compresses explicit control range
- B1 ↔ A2: high-entropy sampling raises both the naturalness ceiling and tail failures
- C1 ↔ all: distillation／quantization sacrifice A3b and B1 first, A2 second
- D1 ↔ A2/A3a/B2: **capability is the risk**

## Minimum reporting set

- A1／A2／A3: one subjective + one objective each; MOS and SMOS as distinct questions
- B1: failure rate + P95 WER on a deliberately hard test set
- B2: at least one **cross-corpus** unseen-speaker result beside the in-domain one
- C1: hardware／batch／streaming settings + A values at that budget
- D1: training-data consent status · watermarked? · detectability under a public detector
- **State what was not measured, rather than leaving it silent**

## Link to audio-deepfake work (this project)

- **Taxonomy inverts: A–C = adversary capability, D = defender's evaluation surface**
- A2／A3a → credibility ceiling of an attack (is a human fooled?)
- B1 → attack yield
  - Failed samples are never sent
  - **In-the-wild samples are a distribution pre-filtered by the adversary** ← underused detection cue
- B2 + C1 → attack scale and cost (real-time? on-device? how much target audio?)
- D1 → must be reported under unseen generators／channels, after compression and laundering
- Conclusion: the threat model must place the adversary on A–C before D's evaluation conditions mean anything
