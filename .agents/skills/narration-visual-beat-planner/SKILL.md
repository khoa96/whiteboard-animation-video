---
name: narration-visual-beat-planner
description: Constructs the synchronized Narration–Visual Beat Plan (BPL01), the central architectural bridge where narration intent, visual element IDs, visual events, reveal order, and expected screen states are co-designed at the atomic beat level before script writing and scene layout begin.
---
# Narration–Visual Beat Planner — S04

## Mission

Serve as the **central architectural bridge (Cầu nối kiến trúc trung tâm)** of the entire Whiteboard Animation production pipeline. S04 solves the critical failure mode of sequential production where scripts are written in isolation and visuals are retrofitted as disconnected illustrations.

S04 co-designs the educational narrative and visual choreography simultaneously at the atomic **Beat** level. A Beat is the fundamental pedagogical unit of communication—typically one sentence or a cohesive clause—where an instructional idea is spoken while corresponding visual elements are drawn, highlighted, labeled, or compared on the whiteboard.

## Why This Skill Solves the Jerkiness & Desynchronization Problem

When scriptwriting precedes visual design:
1. Spoken sentences have no planned visual counterparts, leading to awkward static pauses ("orphan narration").
2. Complex illustrations take 10 seconds to draw while the voiceover finishes in 2 seconds, causing animation lag.
3. Visuals fail to reinforce cognitive processing because drawing happens after the learner has already heard the concept.

S04 mandates that **every single Beat must define both what is heard and what is seen**, locking them to stable IDs before S05A (Script Writing) and S05B (Scene Matrix) branch out.

## Required Input Contract

1. `projects/<project_id>/03_script_blueprint/SB01.json` (status `approved`, Gate G03).
2. `projects/<project_id>/02_lesson_design/LDB01.json` (approved) — Provides exact examples/non-examples, misconceptions, and learning objectives.
3. `projects/<project_id>/01_creative_brief/CB01.json` (approved) — Provides tone and cadence targets.

*Precondition Guard:* If `SB01` is not `approved`, HALT immediately. Never plot beats without an approved blueprint.

## Core Schema: The 8 Mandatory Beat Fields

Every entry in the Beat Plan MUST specify all 8 fields:

| Field Name | Field Key | Description & Standards |
|---|---|---|
| **Beat ID** | `beat_id` | Stable identifier hierarchically formatted: `B<Scene>.<Beat>` (e.g., `B01.01`, `B01.02`, `B02.01`). |
| **Learning Point** | `learning_point` | Exact pedagogical micro-point conveyed in this beat, tied to upstream `LO_xx`. |
| **Narration** | `narration` | Spoken narration draft or explicit narration intent (e.g., *"Notice how we can count one apple, two apples, but we never say one water, two waters."*). |
| **Visual Element IDs** | `visual_element_ids` | Array of stable element identifiers active in this beat: `[SC01_E01, SC01_E02]`. |
| **Visual Event** | `visual_event` | Precise action performed on canvas: `DRAW_NEW`, `HIGHLIGHT`, `ADD_LABEL`, `CONTRAST_COMPARE`, `CONNECT_ARROW`, `CROSS_OUT_ERROR`, `HOLD_FOCUS`. |
| **Reveal Order** | `reveal_order` | Integer indicating the exact chronological sequence of visual appearance within the scene (`1, 2, 3...`). |
| **Estimated Duration** | `estimated_duration_seconds` | Projected duration (seconds) calibrated to spoken syllable count and drawing complexity (typically 3–8 seconds per beat). |
| **Expected Screen State** | `expected_screen_state` | Explicit description of the whiteboard canvas appearance after this beat concludes (cumulative state of elements). |

## Visual Event Taxonomy (Whiteboard Mechanics)

Visual events must obey valid whiteboard drawing operations:
1. `DRAW_NEW`: The hand draws a new illustration, icon, or baseline diagram from scratch.
2. `ADD_LABEL`: The hand writes text, keywords, or phonetic transcription next to an existing graphic.
3. `HIGHLIGHT`: The marker applies an accent color stroke (e.g., Orange `#EA580C` or Teal `#0D9488` box/underline) to direct focus.
4. `CONTRAST_COMPARE`: Simultaneous or sequential juxtaposition of two side-by-side elements.
5. `CONNECT_ARROW`: The hand draws a connecting arrow or relationship bracket between two elements.
6. `CROSS_OUT_ERROR`: The hand draws a red/orange marker `X` through an incorrect example or misconception.
7. `HOLD_FOCUS`: No drawing action; the viewer consolidates learning while listening to an explanation of the already visible board state (maximum 4 seconds).

## Synchrony Principles: Dual Coding & Cognitive Load

1. **No Orphan Narration:** Every spoken sentence must have an explicit visual referent (`visual_element_ids` cannot be empty).
2. **No Orphan Drawing:** Every drawn visual must have an instructional purpose directly linked to a spoken learning point.
3. **Synchronized Pacing (Drawing Speed Calibration):**
   - Estimated speaking pace: ~2.3 to 2.6 words per second.
   - Whiteboard drawing heuristic: An icon takes 2–4 seconds; a word label takes 1.5–3 seconds; an accent underline takes 0.8–1.5 seconds.
   - If narration takes 3 seconds, do NOT schedule 3 complex illustrations in that beat!

## Step-by-Step Execution Protocol

1. **Scene Traversal:** Iterate through each Scene in `SB01.scenes`.
2. **Pedagogical Deconstruction:** Break each scene's function into atomic instructional steps (typically 4–8 beats per scene).
3. **Co-Designing Narration & Visuals:**
   - Write the narration intention for Beat $i$.
   - Simultaneously assign the visual elements and the active `visual_event`.
   - Update the cumulative `expected_screen_state` so downstream artists know what remains on the board.
4. **Cadence & Duration Check:** Sum beat durations per scene and verify against `SB01.scenes[i].target_duration_seconds`.
5. **Cross-Reference Integrity:** Ensure all examples from `LDB01` are captured accurately in the beats.
6. **Dual-Format Artifact Generation:**
   - Canonical `BPL01.json`
   - Human review document `BPL01.md` containing formatted markdown tables.

## Output Artifact Schema (`BPL01.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "BPL01",
  "version": "1.0",
  "source_sb_version": "1.0",
  "status": "in_review",
  "total_beats_count": 32,
  "total_estimated_duration": 300,
  "scenes": [
    {
      "scene_id": "SC01",
      "scene_title": "The Grocery Mystery",
      "scene_budget_seconds": 45,
      "beats": [
        {
          "beat_id": "B01.01",
          "learning_point": "Activate learner awareness of countable vs uncountable dilemma in shopping context",
          "narration": "Have you ever wondered why we say 'two apples', but never 'two waters'?",
          "visual_element_ids": ["SC01_E01", "SC01_E02"],
          "visual_event": "DRAW_NEW",
          "reveal_order": 1,
          "estimated_duration_seconds": 6,
          "expected_screen_state": "Left side shows 2 crisp red apples with label '2 apples'; right side shows water bottle with a large orange question mark."
        }
      ]
    }
  ],
  "approval_gate": {
    "gate_id": "G04",
    "state": "PENDING_USER_APPROVAL"
  }
}
```

## Mandatory Approval Gate G04

- Present `BPL01.md` with complete beat tables for all scenes.
- **HARD STOP:** Neither S05A (Narration Script Writer) nor S05B (Scene Matrix Builder) may commence until Gate G04 is explicitly approved by the user.

