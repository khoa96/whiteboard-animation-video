---
name: image-prompt-generator
description: Generates production-grade, self-contained AI image generation prompts for each scene from the approved Scene Matrix, strictly adhering to Whiteboard Master Prompt v2.1, the Typography Lock, zero-contact ink-island segregation, and subtitle safe zone rules.
---
# Image Prompt Generator — S06

## Mission

Transform the spatial layouts, element inventories, and visual directives from the approved Scene Matrix (`SM01`) into self-contained, broadcast-quality AI image generation prompts. S06 acts as the **Master Prompt Engineering & Computer Vision Constraints Inspector**.

S06 ensures that every generated prompt produces a flawless 16:9 whiteboard master image that can be effortlessly segmented by computer vision (CV) algorithms for subsequent hand-drawing animation.

## Governing Invariants & Production Standards

1. **Master Prompt v2.1 Supremacy:** Every prompt must inherit and incorporate the rules of `whiteboard_master_prompt_scene_generator_v2.1.md` and `whiteboard_visual_style_bible_v1.0_accepted.md`.
2. **Single Comprehensive Canvas:** Exactly ONE image prompt per scene. The prompt must instruct the image generator to render the entire scene in full—including all illustrations, diagrams, icons, connectors, and **ALL exact text strings**. (No prompt may ask for a textless image relying on manual text post-overlays).
3. **Typography Lock Verbatim:** The Typography Lock clause must be included in every prompt to enforce clean, legible, monoline marker lettering without AI hallucinated pseudo-lettering.
4. **CV Segmentation Zero-Contact Rule:** Every distinct element must be an isolated "ink island" surrounded by clean white margin (`#FFFFFF`). No elements may touch, overlap, or bleed into one another unless explicitly grouped as a unified container.
5. **Subtitle Safe Zone Guard:** The bottom 18% of the canvas (bottom 180px in 1080p, `y > 900px`) must remain completely pristine white space.

## Required Input Contract

1. `projects/<project_id>/06_scene_matrix/SM01.json` (status `approved`, Gate G05B).
2. `whiteboard_master_prompt_scene_generator_v2.1.md` (authoritative standard pinned in workspace).
3. `whiteboard_visual_style_bible_v1.0_accepted.md`.

*Precondition Guard:* If `SM01` is not `approved`, HALT. Never generate image prompts without an approved Scene Matrix.

## Anatomical Structure of a Scene Image Prompt

Each scene prompt must be structured into the following 6 mandatory blocks:

### Block 1: Style Anchor & Canvas Definition
- Specify: *“Clean 2D educational whiteboard animation master canvas, pure white background #FFFFFF, crisp black marker line art, consistent medium line weight, flat minimal vector-like aesthetic, zero gradients, zero shadows, zero paper texture, 16:9 widescreen composition (1920x1080).”*

### Block 2: Palette Specification
- Base outlines: `#000000` (Pure Black).
- Background: `#FFFFFF` (Pure White).
- Selective Accent Colors:
  * Primary Accent: `#2563EB` (Cobalt Blue — for titles, key concepts, positive rules).
  * Secondary Accent: `#0D9488` (Teal — for structure boxes, examples, supporting highlights).
  * Alert / Contrast Accent: `#EA580C` (Warm Orange — for errors, question marks, contrastive minimal pairs).
- Strictly limit to at most 2 accent colors per scene to prevent sensory overload.

### Block 3: Spatial Layout & Bounding Zones
- Explicitly partition the 16:9 canvas using layout coordinates:
  * Title Zone (Top 0–15%).
  * Content Zones (Left / Center / Right / Grid modules between 15% and 82%).
  * Subtitle Safe Zone (Bottom 82%–100% / `y: 900–1080px`) — explicitly commanded as: *“ABSOLUTE EMPTY WHITE SPACE. DO NOT DRAW ANY ART, TEXT, OR MARGIN MARKS IN THE BOTTOM 18% OF CANVAS.”*

### Block 4: Detailed Element & Visual Description
- Enumerate every `element_id` from `SM01`:
  * Exact physical description of illustrations, characters, or diagrams.
  * Spatial positioning and relative scale.
  * Explicit white-space separation between objects (*“Surround each object with at least 40px of blank white space for CV segmentation”*).

### Block 5: Exact Text Specifications (Typography Lock)
- For every text element, specify:
  * Text Role (`T0_TITLE`, `T1_SUBTITLE`, `T2_BODY`, `T3_LABEL`, `T4_FORMULA`).
  * **EXACT TEXT IN DOUBLE QUOTES** (e.g., *Write exact text: "2 apples"*).
  * Font style: Clean, legible sans-serif marker lettering, neat uppercase or title case, zero spelling errors, zero random squiggles.

### Block 6: Negative Prompt Constraints
- Embed negative constraints: *“No 3D render, no drop shadows, no photorealism, no gradients, no grunge texture, no colored backgrounds, no messy sketch lines, no touching objects, no overlapping strokes, no illegible text, no gibberish characters, no drawings in the bottom 18% subtitle safe zone.”*

## Step-by-Step Execution Protocol

1. **Extract Scene Specifications:** Iterate through each scene in `SM01.json`.
2. **Compile Scene Image Prompts:** Assemble Blocks 1–6 into a self-contained prompt string for each scene.
3. **Verify Text Consistency:** Confirm that every string in the prompt matches `SM01.elements[].exact_text` verbatim.
4. **Output Generation:**
   - Save individual prompt files: `projects/<project_id>/07_image_prompts/SC01.prompt.md`, `SC02.prompt.md`, etc.
   - Generate summary manifest: `image_prompts_pack.json`.
5. **Pre-Execution Linting:** Validate against Master Prompt v2.1 Gates A through H (checking safe zone command, palette restriction, zero-contact command, and typography lock).

## Output Artifact Schema (`image_prompts_pack.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "IP_PACK_01",
  "master_prompt_version": "v2.1",
  "total_scenes": 5,
  "scenes": [
    {
      "scene_id": "SC01",
      "prompt_file_path": "projects/WB-xxxx/07_image_prompts/SC01.prompt.md",
      "text_inventory": [
        {"element_id": "SC01_E02", "exact_text": "2 apples", "role": "T3_LABEL"}
      ],
      "element_count": 4,
      "safe_zone_enforced": true,
      "zero_contact_enforced": true,
      "full_prompt_text": "..."
    }
  ],
  "approval_gate": {
    "gate_id": "G06",
    "state": "READY_FOR_IMAGE_GENERATION"
  }
}
```

## Gate G06 Verification

- Structural check ensures every scene has an independent prompt.
- Text inventory matches `SM01` with zero spelling discrepancies.
- **Next Stage:** Prompts are submitted to image generation pipeline (e.g., Imagen 3, Midjourney, or DALL-E 3), followed immediately by S06B for actual image inspection.

