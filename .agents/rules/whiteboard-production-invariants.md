---
trigger: always_on
description: "Apply persistent Whiteboard Animation production invariants for source authority, approval gates, traceability, timing semantics, visual alignment, image prompts, and QA status labels."
---

# Whiteboard Production Invariants

These rules are project-wide invariants. Skills describe workflows; this file defines constraints that all workflows must obey.

## 1. Source-of-truth and precedence

1. The latest explicitly user-approved artifact is authoritative for its stage.
2. A later-stage Skill may transform an approved artifact but may not silently rewrite its meaning, learning scope, examples, or user decisions.
3. If two approved sources conflict, stop and report the conflict with file, section, and field references. Do not pick one silently.
4. A user correction supersedes the previous decision only after its scope is clear; record the decision and version impact.
5. Conversation context is not a durable project source. Persist important decisions in the project manifest and approval log.

## 2. Approval lifecycle

Allowed artifact states: `draft`, `in_review`, `revision_required`, `approved`, `superseded`, `blocked`.

- Only the user can move an artifact to `approved`.
- A Skill may set `draft`, `in_review`, `revision_required`, or `blocked` based on work performed.
- No downstream production stage may proceed when a required upstream artifact is not `approved`.
- A substantive change to an approved upstream artifact invalidates the affected downstream artifacts. Mark them `needs_revalidation`; do not pretend they remain approved.

## 3. Traceability

Use stable identifiers and never recycle an ID after deletion:

- Project: `WB-<slug>`
- Creative Brief: `CB01`
- Lesson Design Brief: `LDB01`
- Script Blueprint: `SB01`
- Beat: `B01.01`
- Scene: `SC01`
- Element: `SC01_E01`
- Visual Event: `SC01_B01.01_EV01`
- Audio cue: `AC_SC01_B01.01_01`

Every downstream object must point back to its parent source IDs. If an element or beat is renamed, preserve its ID and record the rename. If its meaning changes, create a new ID and a migration note.

## 4. Dual-format artifacts

For production-critical artifacts, maintain:
- Markdown: readable review copy for the user.
- JSON: structured canonical data for automated validation and downstream transformations.

Both must be generated from the same approved data, not independently authored. If Markdown and JSON disagree, mark the artifact `blocked` until reconciled.

## 5. Timing semantics

Keep these separate:
- pedagogical order;
- narration/beat budget (estimate);
- visual-event order and estimated draw duration;
- actual audio word/phrase timestamps;
- renderer-measured stroke/draw duration;
- final animation timeline.

Never call a planned duration an actual timestamp. Actual alignment requires the produced audio (or an explicitly supplied alignment file). HOLD is not a substitute for missing visual coverage or a meaningless wait.

## 6. Narration–visual alignment

- Each instructional meaning unit must have visual support: a new visual event, an existing visible element referenced, a deliberate emphasis, comparison, or a documented reason why no visual change is pedagogically better.
- Not every sentence needs a new drawing.
- Every visual event must serve explanation, example, contrast, orientation, assessment, feedback, or memory.
- A scene image is a complete static source composition. Sequential reveal is implemented through separable element/event scheduling, not by asking one static image to animate itself.
- A new scene is a new source image unless a project explicitly changes that production model.

## 7. Image prompt constraints

When a project references Whiteboard Master Prompt v2.1, it is a governing production standard for image prompts. Preserve its exact Typography Lock verbatim, T0–T9 text-role map, palette, canvas, subtitle safe zone, isolated-ink/gutter rules, zero-contact rules, negative prompt constraints, and Gates A–H. Do not replace or paraphrase the source standard. The exact master-prompt file supplied for the project must be read before prompt generation.

Do not introduce visible words, labels, symbols, objects, or decorations that are absent from the approved Scene Matrix. Every generated prompt must contain all required visible scene content in the same complete image; no mandatory text-free image plus overlay workflow.

## 8. Educational and factual integrity

- Respect the approved learner level, scope, prerequisites, and learning objectives.
- Separate core taught content from optional extension.
- Distinguish factual source material from model inference and creative proposal.
- Never silently simplify a rule in a way that makes it false or absolute.
- Preserve exact English examples and their approved context.

## 9. Critical review protocol

For every major artifact:
1. Draft against the input contract.
2. Run a hostile review from at least three relevant lenses (e.g. pedagogy, production, data/traceability).
3. Classify findings as Critical / Major / Minor; cite concrete IDs and source locations.
4. Revise only issues supported by evidence or clearly marked design decisions.
5. Re-run the same checks; show which findings are fixed, remain open, or are accepted risks.

Do not fabricate independent human reviewers. These are simulated review lenses, not external certification.

## 10. Honest validation labels

Use distinct labels:
- `STRUCTURAL PASS`: file and schema integrity.
- `TRACEABILITY PASS`: IDs and cross-references are complete.
- `CONTENT PASS`: factual/pedagogical checks passed against sources.
- `VISUAL PROMPT PASS`: prompt text complies; it does not mean generated image passed.
- `IMAGE QA PASS`: actual rendered image has been inspected.
- `CV QA PASS`: actual segmentation diagnostics have been run.
- `AUDIO QA PASS`: actual voice/audio and alignment have been checked.
- `RENDER QA PASS`: actual rendered video has been reviewed.

Never promote one type of PASS into another.
