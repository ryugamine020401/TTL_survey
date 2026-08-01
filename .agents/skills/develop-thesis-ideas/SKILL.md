---
name: develop-thesis-ideas
description: Generate, verify, compare, red-team, and synthesize research directions for this master's thesis. Use for thesis brainstorming, novelty checks, related-work gap analysis, hypothesis formation, feasibility review, candidate comparison, or domain knowledge mapping in audio deepfake research. Do not use for routine experiment implementation, thesis prose polishing, or unrelated research topics.
---

# Develop Thesis Ideas

Use an evidence-first workflow that keeps exploration broad enough to discover alternatives and critical enough to eliminate weak ideas early.

## 1. Select the mode

Classify the request as one or more of:

- **Explore:** generate materially different candidate directions.
- **Validate:** verify claims, novelty, assumptions, feasibility, or access.
- **Synthesize:** build a knowledge map of a subfield.
- **Compare:** evaluate candidates using common evidence and criteria.
- **Decide:** recommend only when the user asks to choose.

If the request is open-ended, use Explore before Decide. If the user already supplies a claim or candidate, begin with Validate rather than defending it.

## 2. Load only relevant context

Read `PROJECT.md`, `DECISIONS.md`, and `TASKS.md`. Then read only the relevant portions of `survey/`, `discussions/`, original PDFs, and prior research artifacts.

For a Claude-to-Codex task, read `exchange/claude-outbox/INDEX.md`, the named immutable handoff, and only its required source artifacts. Do not broadly scan `discussions/` or `research/` to discover new agent work. Treat the Claude outbox as read-only.

When returning work to another agent, keep the full artifact in the appropriate purpose-based directory. Put only a short pointer handoff in `exchange/codex-outbox/`, update only its `INDEX.md`, and follow `exchange/README.md`. Never modify a sent handoff; issue corrections or additions as new delta files linked with `in_reply_to`, `supersedes`, or `delta_of`.

Treat local summaries and agent discussions as leads. Verify material claims from original sources.

## 3. Frame the inquiry

State:

- the problem and stakeholder;
- the unit of analysis and threat model;
- what would count as a contribution;
- the time, data, compute, legal, and ethics boundaries;
- the decision this work should enable.

Surface missing information, but continue with explicit assumptions when they do not materially change the research direction.

## 4. Build the evidence base

Search local sources first. For current novelty, SOTA, dataset access, product behavior, laws, or policy, verify externally.

For technical research, prefer original papers, official proceedings, official specifications, dataset pages, and author repositories. Record the search date, scope, closest prior work, and publication status. Include contradicting and negative evidence.

Use the evidence states and claim rules in [evidence-standard.md](references/evidence-standard.md).

## 5. Generate or refine candidates

For open exploration, produce three to seven candidates that differ in research question or mechanism, not just model architecture.

For each serious candidate define:

- research question;
- falsifiable hypothesis;
- proposed contribution;
- closest prior work and residual gap;
- minimal method and data;
- primary metric and comparison;
- expected failure mode;
- useful result if the hypothesis is false.

## 6. Red-team before ranking

Attack each candidate on:

- prior-art collision and scoop risk;
- dataset access, licensing, and reproducibility;
- compute and engineering load;
- construct validity, confounding, leakage, and metric mismatch;
- adaptive attacker or threat-model escape;
- ethics, privacy, IRB, and deployment assumptions;
- one-year minimum scope and dependency risk.

Seek the cheapest literature check or feasibility test that could invalidate the candidate.

## 7. Synthesize and compare

Separate established knowledge, disputed findings, missing evidence, and new hypotheses. Identify whether each gap is field-level or limited to a dataset, language, channel, population, metric, or deployment context.

When comparing candidates, use consistent criteria and explain every rating. Never let a numeric score replace evidence or uncertainty.

## 8. End with a validation contract

Specify:

- the next smallest validation step;
- evidence that would strengthen the idea;
- evidence that would kill or narrow it;
- a useful pivot if the main hypothesis fails;
- remaining uncertainty and search limitations.

Follow [output-contract.md](references/output-contract.md) for substantial written artifacts.

## 9. Maintain project state

When the user asks for files, store outputs under:

- `research/ideas/` for exploration;
- `research/validations/` for claim, novelty, and feasibility checks;
- `research/syntheses/` for knowledge maps.

Update `TASKS.md` when next actions materially change. Update `PROJECT.md` only after scope changes are approved. Treat `DECISIONS.md` as author-owned and read-only: state whether it should change and provide an exact proposed entry when useful, but never edit it.
