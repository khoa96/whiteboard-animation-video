---
name: whiteboard-preproduction-orchestrator
description: Coordinates, monitors, and orchestrates specialized AI agents executing the end-to-end Whiteboard Animation Pre-Production pipeline (S00 through S08) with automated adversarial reviews, strict quality gate enforcement, and change propagation.
---
# Whiteboard Pre-Production Orchestrator

## Mission

Serve as the **Supreme Executive Director & Master Pipeline Coordinator** for the entire Whiteboard Animation production system. This Skill governs the end-to-end multi-agent workflow, coordinating specialized agents across all 11 skills (S00 through S08), managing the project lifecycle, enforcing mandatory approval gates, executing adversarial review loops, and guaranteeing that no video moves to animation without complete pedagogical and visual synchronization.

## Operational Workflow Architecture

The Orchestrator executes a deterministic 7-phase state machine:

```
[Phase 0: Intake] ──> S00 (Project Intake & Source Audit) ──> [Gate G00: Source Integrity]
                            │
[Phase 1: Briefing] ──> S01 (Creative Brief Builder) ──> [Gate G01: User Approval]
                            │
[Phase 2: Pedagogy] ──> S02 (Lesson Design Architect) ──> [Gate G02: User Approval]
                            │
[Phase 3: Blueprint] ──> S03 (Script Blueprint Designer) ──> [Gate G03: User Approval]
                            │
[Phase 4: Bridge]   ──> S04 (Narration–Visual Beat Planner) ──> [Gate G04: User Approval]
                            │
                            ├───────────────────────────────┐
                            ▼                               ▼
[Phase 5: Dual]     S05A (Narration Script)          S05B (Scene Matrix)
                            │                               │
                            └───────────────┬───────────────┘
                                            ▼
                               [Cross-Branch Reconciliation]
                                            │
                                  [Gate G05: User Approval]
                                            │
                                            ▼
[Phase 6: Visuals]  ──> S06 (Image Prompts) ──> [Image Generation] ──> S06B (CV QA)
                                            │
                                [Gate G07: Image/CV Accepted]
                                            │
                                            ▼
[Phase 7: Timeline] ──> S07 (Voice–Animation Timeline) ──> [Gate G08: Audio Sync]
                                            │
                                            ▼
[Phase 8: Audit]    ──> S08 (Production Readiness Auditor) ──> [Gate G09: Final Pass]
                                            │
                                            ▼
                               [Handoff to Video Renderer]
```

## Dual-Agent Adversarial Governance Protocol

For every stage from S00 to S08, the Orchestrator enforces a 3-step quality loop:

1. **Step 1 (Execution):** The primary specialized agent executes the skill, drafting the dual-format artifacts (`.json` canonical + `.md` review copy).
2. **Step 2 (Adversarial Review):** The Orchestrator summons the specialized Inspector Agent for that domain to grade the draft against the **Council Rubric (100-point scale)**:
   - *Pedagogical & Domain Rigor (25 pts)*
   - *Data Contracts & Traceability (25 pts)*
   - *Whiteboard Production & Animation Feasibility (20 pts)*
   - *Edge Cases & Failure Recovery (15 pts)*
   - *Agent Actionability & Clarity (15 pts)*
   *Passing Threshold:* Score $\ge 90/100$ and zero critical findings.
3. **Step 3 (Revision Loop):**
   - If Score $< 90$: The Inspector returns itemized defects with line-level evidence. The primary agent performs surgical revisions until the score reaches $\ge 90$.
   - Once Passed: The Orchestrator presents the review document to the user at the designated Gate.

## User Approval Gate Protocol

- Artifact states: `draft` $\rightarrow$ `in_review` $\rightarrow$ `approved` (or `revision_required`).
- **THE CARDINAL RULE:** **Only the human user can transition an artifact to `approved`.**
- Agents and the Orchestrator may only set `in_review`, `revision_required`, or `blocked`.
- The Orchestrator halts execution at each Gate (G01, G02, G03, G04, G05, G09) and presents a concise briefing to the user, asking for approval before initiating the next phase.

## Upstream Invalidation & Change-Control Protocol

When a user requests a change to an earlier artifact:
1. **Change Impact Analysis:**
   - Change in `CB01`: Marks `LDB01`, `SB01`, `BPL01`, `NS01`, `SM01`, `IP`, `Timeline` as `needs_revalidation`.
   - Change in `LDB01`: Marks `SB01` onwards as `needs_revalidation`.
   - Change in `BPL01`: Marks `NS01` and `SM01` as `needs_revalidation`.
   - Change in `NS01` (text change only): Marks audio/timeline as `needs_revalidation`; if cue words change, updates `SM01.elements[].bound_narration_cue`.
   - Change in `SM01`: Invalidates image prompts and CV manifest.
2. **Surgical Regeneration:** Rather than restarting from scratch, the Orchestrator instructs affected agents to preserve unchanged sections and re-validate only modified components.
3. **Audit Trail:** Log all changes with timestamps in `projects/<project_id>/approvals/approval-log.md`.

## Step-by-Step Orchestration Execution Guide

### Initialization
1. Receive user command or trigger (e.g. *"Bắt đầu dự án Whiteboard mới về [Chủ đề]"*).
2. Create project directory under `projects/<project_id>/` and initialize `project.yaml` and `approval-log.md`.

### Phase 0: Project Intake & Source Audit
1. Invoke `project-intake-audit` (S00).
2. Validate sources, master prompts, and voice profiles. Verify G00 clearance.

### Phase 1: Creative Briefing
1. Invoke `creative-brief-builder` (S01).
2. Conduct adaptive interview (Part A) + AI pedagogical analysis (Part B).
3. Run Adversarial Review. Ensure Score $\ge 90$.
4. Halt at Gate G01. Request user approval.

### Phase 2: Lesson Design Architecture
1. Upon G01 approval, invoke `lesson-design-architect` (S02).
2. Build 10-pillar instructional architecture (`LDB01.json` + `LDB01.md`).
3. Run Adversarial Review. Ensure Score $\ge 90$.
4. Halt at Gate G02. Request user approval.

### Phase 3: Script Blueprinting
1. Upon G02 approval, invoke `script-blueprint-designer` (S03).
2. Partition lesson into modules and scenes with strict time budgets.
3. Run Adversarial Review. Ensure Score $\ge 90$.
4. Halt at Gate G03. Request user approval.

### Phase 4: Narration–Visual Beat Planning (The Core Bridge)
1. Upon G03 approval, invoke `narration-visual-beat-planner` (S04).
2. Co-design all atomic beats with the 8 mandatory fields (`BPL01.json` + `BPL01.md`).
3. Run Adversarial Review. Ensure Score $\ge 90$.
4. Halt at Gate G04. Request user approval.

### Phase 5: Dual Synchronized Production Branches
1. Dispatch parallel tasks:
   - Branch A: Invoke `narration-script-writer` (S05A) to write spoken dialogue locked to Beat IDs and conduct cadence audits.
   - Branch B: Invoke `scene-matrix-builder` (S05B) to design spatial layouts, element inventories, and board states.
2. Run cross-branch reconciliation check (verify 100% beat coverage and exact cue binding).
3. Halt at Gate G05. Request user approval.

### Phase 6: Visual Image Generation & CV Diagnostics
1. Invoke `image-prompt-generator` (S06) to produce Master Prompt v2.1-compliant scene prompts.
2. Trigger image generation for each scene.
3. Invoke `rendered-image-cv-qa-auditor` (S06B) to inspect actual PNGs and CV masks.
4. Verify Gate G07 clearance (`accepted_cv_manifest.json`).

### Phase 7: Voiceover & Timeline Assembly
1. Generate voiceover audio (`voiceover.wav`) via TTS engine using `tts_export.txt`.
2. Generate forced-alignment timestamps (`alignment.json`).
3. Invoke `voice-animation-timeline-builder` (S07) to assemble frame-accurate `timeline.json`.
4. Verify Gate G08 clearance.

### Phase 8: Final Production Readiness Audit & Handoff
1. Invoke `production-sync-readiness-auditor` (S08).
2. Run complete 8-point audit battery across all artifacts.
3. Issue Gate G09 Production Readiness Certificate.
4. Provide the exact rendering command to launch `render_stream_whiteboard.py`.

## Project State Tracking Manifest (`project.yaml`)

```yaml
project_id: WB-2026-COUNTABLE-NOUNS
title: "Countable vs Uncountable Nouns"
current_phase: PHASE_4_BEAT_PLAN
active_skill: S04-narration-visual-beat-planner
gates:
  G00_intake: APPROVED
  G01_creative_brief: APPROVED
  G02_lesson_design: APPROVED
  G03_script_blueprint: APPROVED
  G04_beat_plan: IN_REVIEW
  G05_narration_and_matrix: NOT_STARTED
  G06_image_prompts: NOT_STARTED
  G07_cv_manifest: NOT_STARTED
  G08_timeline: NOT_STARTED
  G09_readiness: NOT_STARTED
artifacts:
  intake_report: { version: "1.0", path: "00_intake/intake_report.json" }
  creative_brief: { version: "1.0", path: "01_creative_brief/CB01.json" }
  lesson_design: { version: "1.0", path: "02_lesson_design/LDB01.json" }
  script_blueprint: { version: "1.0", path: "03_script_blueprint/SB01.json" }
  beat_plan: { version: "1.0", path: "04_beat_plan/BPL01.json" }
```

