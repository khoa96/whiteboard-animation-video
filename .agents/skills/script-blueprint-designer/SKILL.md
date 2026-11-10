---
name: script-blueprint-designer
description: Architects the structural macro-design of the whiteboard animation video, partitioning the lesson into pedagogical modules and scenes, allocating time budgets, and defining scene-level visual strategies in an approval-ready Script Blueprint (SB01).
---
# Script Blueprint Designer — S03

## Mission

Transform the approved pedagogical strategy (`LDB01`) and production parameters (`CB01`) into the high-level structural architecture of the video. S03 acts as the **Lead Instructional Architect & Whiteboard Pacing Director**. It segments the educational journey into coherent Modules and discrete Scenes, assigns strict time budgets, and defines the visual staging strategy for every scene.

S03 defines **the architectural skeleton of the video**. It does NOT write word-for-word narration lines (which is S05A) and does NOT enumerate individual drawing strokes or element inventories (which is S05B).

## Operational Context & Pipeline Position

- **Preceding Step:** S02 (Lesson Design Architect) — requires `LDB01` status `approved` (Gate G02).
- **Subsequent Step:** S04 (Narration–Visual Beat Planner) — Gate G03.
- **Key Bridge Function:** Ensures that the pedagogical sequence designed in LDB01 translates into a well-paced, visually viable scene-by-scene roadmap before granular beats are plotted.

## Required Input Contract

1. `projects/<project_id>/01_creative_brief/CB01.json` (approved) — Provides target duration, audience level, format, and tone.
2. `projects/<project_id>/02_lesson_design/LDB01.json` (approved) — Provides learning objectives, teaching sequence, concept structure, misconceptions, examples/non-examples, and boundaries.

*Precondition Guard:* If either `CB01` or `LDB01` is not `approved`, HALT and report `ERROR: S03 requires approved CB01 and LDB01.`

## Core Architectural Responsibilities

### 1. Macro-Modular Decomposition
Partition the video into 4 to 6 logical pedagogical modules:
- **Module 1: The Cognitive Hook & Problem Activation** (~10–15% of duration) — Introduce context, expose learner misconception or provoke curiosity.
- **Module 2: Core Concept Deconstruction & Visual Metaphor** (~25–30% of duration) — Break down the primary grammar/vocabulary mechanism using a central whiteboard visual model.
- **Module 3: Contrastive Analysis & Minimal Pairs** (~25–30% of duration) — Side-by-side comparison of valid vs invalid usage, resolving the cognitive obstacle identified in LDB01.
- **Module 4: Guided Micro-Practice / Formative Challenge** (~15–20% of duration) — Interactive question-pause-reveal sequence for active recall.
- **Module 5: Synthesis, Anchor Rule & Memory Takeaway** (~10% of duration) — Visual summary anchor reinforcing the primary learning objective.

### 2. Scene Partitioning & Canvas Strategy
- Break modules down into discrete Scenes (`SC01`, `SC02`, ...).
- **Whiteboard Scene Principle:** In whiteboard animation, each Scene represents a distinct static canvas composition (or fresh board). Avoid scene switching every 5 seconds (which causes visual whiplash); typical whiteboard scenes last 30 to 75 seconds, allowing visual elements to accumulate systematically.
- For each scene, specify:
  * **Scene ID:** `SC01`, `SC02`, etc.
  * **Module Reference:** Which pedagogical module this scene belongs to.
  * **Pedagogical Purpose:** The exact learning milestone achieved on this canvas.
  * **Visual Strategy & Layout Architecture:** Spatial division (e.g., Two-column split, Left-to-right timeline, Central hub with radiating branches) in accordance with `whiteboard_visual_style_bible_v1.0_accepted.md`.
  * **Accumulation & Transition Plan:** How elements build upon the board and how the board transitions to the next scene (clean wipe, natural pause).

### 3. Time Budgeting & Cadence Calibration
- Allocate time budgets per scene and module in seconds.
- Verify total duration against `CB01.target_duration_seconds` (tolerance: ±5%).
- **Time Reconciliation Protocol:** If total allocated seconds deviate by more than 5% from target:
  * Over-budget (> +5%): Reduce expository hook or trim secondary illustrative examples; preserve core contrast and formative check.
  * Under-budget (< -5%): Deepen formative practice by adding 1 extra contrastive minimal pair.
- Ensure speaking rate assumes a natural, pedagogical English delivery (130–150 WPM for ESL/EFL learners).

## Step-by-Step Execution Protocol

1. **Intake Mapping:** Read `LDB01.teaching_sequence` and map each stage to a planned Module.
2. **Scene Allocation:** Determine the optimal number of scenes (typically 4–7 scenes for a 3–5 minute explainer).
3. **Visual Strategy Formulation:** Assign layout paradigms that best suit the concept (e.g., contrasting pairs require a split canvas; timelines require a linear flow).
4. **Duration Balance Audit:** Calculate cumulative seconds. If over-budget, trim redundant steps; if under-budget, expand guided practice.
5. **Generate Dual-Format Artifacts:**
   - Canonical `SB01.json`
   - Human review document `SB01.md`
6. **Internal Adversarial Check:**
   - *Pacing Lens:* Is any scene longer than 90 seconds without visual renewal?
   - *Pedagogical Lens:* Does every scene directly advance a Learning Objective from LDB01?
   - *Feasibility Lens:* Are layout zones balanced according to 16:9 widescreen layout?

## Output Artifact Schema (`SB01.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "SB01",
  "version": "1.0",
  "source_ldb_version": "1.0",
  "status": "in_review",
  "total_budget_seconds": 300,
  "allocated_budget_seconds": 300,
  "modules": [
    {
      "module_id": "MOD_01",
      "module_name": "HOOK_AND_DISCOVERY",
      "pedagogical_goal": "Activate learner attention and expose common L1 misconception",
      "budget_seconds": 45,
      "supported_lo_ids": ["LO_01"],
      "scene_ids": ["SC01"]
    }
  ],
  "scenes": [
    {
      "scene_id": "SC01",
      "module_id": "MOD_01",
      "title": "The Grocery Mystery",
      "target_duration_seconds": 45,
      "pedagogical_function": "Contrast 'many water' vs 'much water' in everyday context",
      "visual_strategy": {
        "layout_type": "SPLIT_TWO_COLUMN | CENTRAL_HUB | LINEAR_TIMELINE | 3_ZONE_GRID",
        "primary_focal_point": "Center shopping cart icon with thought bubbles",
        "ink_palette_focus": "Black outlines + Orange alert for incorrect grammar",
        "transition_out": "CLEAN_BOARD_WIPE"
      },
      "estimated_beat_count": 4
    }
  ],
  "pacing_metrics": {
    "target_wpm": 140,
    "total_estimated_words": 700
  },
  "approval_gate": {
    "gate_id": "G03",
    "state": "PENDING_USER_APPROVAL"
  }
}
```

## Mandatory Approval Gate G03

- Present `SB01.md` displaying the module structure, scene breakdown, visual layouts, and time budgets.
- Halt execution and await explicit user approval before triggering S04.
