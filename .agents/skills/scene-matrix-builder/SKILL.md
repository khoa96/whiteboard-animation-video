---
name: scene-matrix-builder
description: Translates approved instructional beats into a comprehensive Scene Matrix (SM01), defining visual zones, element inventories, drawing/reveal orders, board states, and exact narration cue bindings while respecting whiteboard canvas and CV segmentation constraints.
---
# Scene Matrix Builder — S05B

## Mission

Transform the synchronized visual requirements of `BPL01` into a complete, mathematically coherent, production-grade **Scene Matrix (SM01)**. S05B acts as the **Senior Whiteboard Visual Director & Spatial Composition Specialist**.

S05B plans the entire physical canvas for every scene: what elements exist, where they are placed, the order in which the marker draws them, and how the canvas accumulates state. S05B directly binds visual events to the exact spoken cues established in `NS01`.

## Architectural Invariants for Scene Matrix

1. **Static Source Image Principle:** In this whiteboard architecture, each scene is generated as **one single, complete, static master image** containing all text, illustrations, and graphic elements. Sequential reveal is executed during post-processing by drawing elements in order, NOT by generating multiple disconnected images.
2. **Pre-Render Spatial Intent vs. Post-Render Pixel Data:**
   - At S05B, coordinate positions are declared as **Target Layout Regions** (e.g., `ZONE_LEFT_TOP`, `ZONE_CENTER_CONTRAST`, `ZONE_BOTTOM_SUMMARY`).
   - S05B NEVER invents or claims fake pixel coordinates (e.g. `[124, 350, 400, 600]`) before the AI image is actually generated and measured by CV.
3. **Typography & Subtitle Safe Zone Guard:**
   - All visual elements must strictly avoid the bottom 180px of a 1080p canvas (`y > 900px`), reserved for video subtitles.
   - Text elements must follow the Typography Lock and standard text roles (`T0` Title, `T1` Subtitle, `T2` Body, `T3` Label, `T4` Formula/Rule, `T5` Accent).
4. **CV Segmentation Feasibility (Zero-Contact & Ink Islands):**
   - Independent elements must be designed with sufficient visual gutter (minimum 40px spacing) so computer vision algorithms (SAM / YOLO / contour detectors) can segment them cleanly without stroke bleeding.

## Required Input Contract

1. `projects/<project_id>/04_beat_plan/BPL01.json` (approved, Gate G04) — Core beat structure and visual element IDs.
2. `projects/<project_id>/05_narration_script/NS01.json` (approved or draft with stable cue spans) — For exact cue binding.
3. `whiteboard_visual_style_bible_v1.0_accepted.md` and `whiteboard_master_prompt_scene_generator_v2.1.md`.

*Precondition Guard:* `BPL01` must be `approved`. S05B may construct layout drafts while `NS01` is in review, but CANNOT be marked `approved` until `NS01` is approved and exact audio cue spans are bound.

## Core Information Dimensions of SM01

### 1. Canvas Architecture per Scene
- Canvas dimensions: 1920x1080 (16:9).
- Layout grid partitioning (e.g., 2-Column Split, 3-Card Horizontal, Central Radial, Linear Pipeline).
- Subtitle Safe Zone: `[0, 900, 1920, 1080]` — strictly marked NO DRAWING.

### 2. Comprehensive Element Inventory
Every element across every scene must have an explicit profile:
- `element_id`: Stable identifier (e.g., `SC01_E01`, `SC01_E02`).
- `category`: `ILLUSTRATION` | `TEXT_LABEL` | `ICON` | `CONTAINER_BOX` | `CONNECTOR_ARROW` | `ACCENT_MARKER`.
- `target_layout_region`: Standardized zone descriptor (e.g., `COL_LEFT_CENTER`).
- `visual_content_description`: Detailed prompt-ready description of what the object looks like (e.g., *"Clean 2D black marker outline of a ripe apple with a small leaf, selective flat red fill"*).
- `exact_text`: If category is `TEXT_LABEL`, the EXACT string that must appear on the board (e.g., `"2 apples"`).
- `ink_color`: Marker color hex code (`#000000` Black, `#2563EB` Blue, `#0D9488` Teal, `#EA580C` Orange).
- `cv_segmentation_isolation_note`: Note ensuring element has dedicated empty white space surrounding it.

### 3. Reveal Choreography & State Progression
- `reveal_order`: 1, 2, 3...
- `trigger_beat_id`: Maps to `B01.01`, etc.
- `narration_cue_phrase`: The exact words in the script that trigger the start of drawing.
- `estimated_draw_duration_seconds`: Estimated drawing time based on stroke complexity (simple icon: 2s; complex diagram: 4.5s).
- `board_state_after_reveal`: Summary of active visible elements on canvas.

## Step-by-Step Execution Protocol

1. **Inventory Aggregation:** Extract all `visual_element_ids` from `BPL01.json`.
2. **Spatial Zone Mapping:** Assign non-overlapping target layout zones adhering to 16:9 proportions and subtitle safe zones.
3. **Detail Element Specifications:** Define visual description, exact text strings, and color assignments.
4. **Cue Binding:** Cross-reference `NS01.json` to link each element's reveal trigger to exact spoken words.
5. **Cross-Branch Reconciliation Check:** Verify that:
   - Every element in `BPL01` exists in `SM01`.
   - No surprise elements exist in `SM01` that were not in `BPL01`.
   - Every cue phrase matches `NS01` verbatim.
6. **Generate Dual-Format Artifacts:**
   - Canonical `SM01.json`
   - Human review document `SM01.md` containing canvas layout ASCII/tables and element matrices.

## Output Artifact Schema (`SM01.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "SM01",
  "version": "1.0",
  "source_bpl_version": "1.0",
  "source_ns_version": "1.0",
  "status": "in_review",
  "scenes": [
    {
      "scene_id": "SC01",
      "canvas_layout": {
        "aspect_ratio": "16:9",
        "resolution": "1920x1080",
        "layout_type": "SPLIT_TWO_COLUMN",
        "subtitle_safe_zone_margin_bottom_px": 180
      },
      "elements": [
        {
          "element_id": "SC01_E01",
          "category": "ILLUSTRATION",
          "target_layout_region": "ZONE_LEFT_MID",
          "visual_content_description": "Clean black marker illustration of two crisp red apples with green leaves, flat 2D style",
          "exact_text": null,
          "ink_color": "#000000",
          "accent_color": "#EA580C",
          "associated_beat_id": "B01.01",
          "reveal_order": 1,
          "bound_narration_cue": "two apples",
          "estimated_draw_duration_seconds": 3.0,
          "cv_isolation_guarantee": "Minimum 50px white margin separating from E02"
        },
        {
          "element_id": "SC01_E02",
          "category": "TEXT_LABEL",
          "target_layout_region": "ZONE_LEFT_MID_BELOW_E01",
          "visual_content_description": "Handwritten marker text below apples",
          "exact_text": "2 apples",
          "text_role": "T3_LABEL",
          "ink_color": "#000000",
          "associated_beat_id": "B01.01",
          "reveal_order": 2,
          "bound_narration_cue": "two apples",
          "estimated_draw_duration_seconds": 1.5,
          "cv_isolation_guarantee": "Underneath E01 with 40px clear vertical gap"
        }
      ],
      "board_states": [
        {
          "state_id": "STATE_01",
          "after_beat_id": "B01.01",
          "visible_element_ids": ["SC01_E01", "SC01_E02"]
        }
      ]
    }
  ],
  "cross_branch_verification": {
    "bpl_coverage_percent": 100.0,
    "ns_cue_binding_status": "FULL_MATCH",
    "orphan_elements_count": 0
  },
  "approval_gate": {
    "gate_id": "G05B",
    "state": "PENDING_USER_APPROVAL"
  }
}
```

## Mandatory Approval Gate G05B & Cross-Branch Check

- Verify `cross_branch_verification.orphan_elements_count == 0` and `bpl_coverage_percent == 100`.
- Present `SM01.md` with visual layout maps and element inventories.
- **HARD STOP:** S06 (Image Prompt Generator) CANNOT proceed until both G05A and G05B are approved.

