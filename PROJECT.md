# Master Thesis Project

Last updated: 2026-07-25

## Current phase

Research ideation, verification, and domain knowledge synthesis.

No final thesis topic has been selected. The immediate objective is to build an evidence-linked problem map from stakeholder decisions, target claims, threat models, available evidence, and valid evaluation conditions. The existing five broad directions are retained as candidate branches to be repositioned and tested by that map.

## Problem area

Audio deepfakes are increasingly easy to generate, while passive detectors often degrade under unseen generators, languages, channels, compression, and laundering. Provenance and watermarking provide different guarantees and have different deployment dependencies. A useful thesis should state exactly what it can verify, under which threat model, and how that evidence affects a real decision.

## Candidate direction families

These are candidates, not commitments:

1. Shift-aware selective prediction and uncertainty for audio deepfake detection.
2. Independent evaluation over real telecom or messaging channels.
3. Adaptive-laundering and attacker-cost evaluation.
4. Active liveness or challenge-response under modern streaming voice conversion.
5. Audio provenance, watermark survival, and cross-layer consistency.

The first family was the previous leading candidate. It is now treated as a provisional branch rather than the default direction until the problem map establishes its stakeholder, decision value, threat model, and residual gap. Its novelty must still be repositioned against uncertainty-aware work such as FADEL and newer calibration studies. Combining the full ML benchmark, adversarial evaluation, warning UX, and a powered user study is likely too broad for one thesis.

## Research objective for the ideation phase

Identify one thesis direction that satisfies all of the following:

- A precise and falsifiable research question.
- A gap supported by a documented and current literature search.
- A contribution that remains useful if the main hypothesis is false.
- Data, compute, software, and evaluation access compatible with a one-year master's project.
- A threat model and metric that match the claimed deployment value.
- A scope that does not depend on an optional user study or unavailable proprietary data.

## Current boundaries

- Do not assume that an eight-paper survey establishes novelty.
- Do not treat role-based agent discussions as peer review.
- Do not make a user study the critical path before power analysis and IRB feasibility are known.
- Do not require training a new foundation model.
- Prefer public data and reproducible baselines; treat approval-gated datasets as risks.
- Keep HCI/usable-security work optional until the technical core is defensible.

## Open questions

- What is the closest prior work to selective prediction or classification with rejection in audio deepfake detection?
- Do uncertainty scores retain useful ranking under unseen-generator and unseen-channel shift?
- Is real-manifold distance meaningfully different from evidential or feature-distance OOD baselines?
- What operational definition should replace the informal `max P(confident-real | fake)` expression?
- Which datasets can legally and practically support cross-dataset evaluation?
- What compute, storage, advisor expertise, and IRB support are available?
- Should the final contribution be primarily ML, security evaluation, systems, or usable security?

## Existing local evidence

- `survey/README.md`: summaries of eight initial sources.
- `discussions/legacy/`: archived role-based discussions, plans, and pre-problem-map ideation.
- `discussions/problem-map/`: the active step-by-step reasoning record.

These sources provide hypotheses and search leads. Claims must be rechecked against original and current sources.
