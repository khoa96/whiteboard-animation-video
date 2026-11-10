---
name: rendered-image-cv-qa-auditor
description: Audits actual rendered scene images and computer vision (CV) segmentation results against the approved Scene Matrix, verifying text spelling, element completeness, ink-island isolation, subtitle safe zone compliance, and segmentation mask validity before timeline assembly (S06B).
---
# Rendered Image & CV QA Auditor — S06B

## Mission

Bridge the hazardous gap between AI image generation and video animation rendering. S06B acts as the **Senior CV & Image QA Lead (Segmentation/Ink-Island/Gutter Inspector)**. 

A syntactically valid image prompt does NOT guarantee a usable image. Image generation models frequently introduce typos, hallucinatory background doodles, touching strokes, or intrusion into subtitle safe zones. S06B performs strict visual and algorithmic quality inspection on the **actual generated image files** and their **CV segmentation masks**, generating the official `accepted_cv_manifest.json` required by S07.

## Governing Invariants

1. **Physical Asset Verification:** S06B NEVER operates on prompt text alone. It requires actual image files (`SCxx.png`) and actual segmentation diagnostics. If image files do not exist, S06B terminates with status `BLOCKED_AWAITING_IMAGE_ASSETS`.
2. **Measurement of Actual Coordinates:** S06B is the stage where `actual_bbox_px` (measured bounding boxes $[x, y, w, h]$ in pixels) are first recorded and mapped to `element_id`.
3. **Zero-Tolerance Defect Policy:**
   - ANY misspelling in on-screen educational text = IMMEDIATE REJECTION & REGENERATION.
   - ANY visual intrusion into the subtitle safe zone ($y > 900\text{px}$) = IMMEDIATE REJECTION & REGENERATION.
   - ANY stroke fusion between two distinct semantic elements that prevents CV separation = IMMEDIATE REJECTION or manual inpainting flag.

## Required Input Contract

1. Rendered image files: `projects/<project_id>/08_image_assets/SC01.png`, `SC02.png`, etc.
2. `projects/<project_id>/06_scene_matrix/SM01.json` (approved).
3. Segmentation diagnostic outputs produced by `scripts/universal_ai_segmenter.py` or OpenCV contour detectors.

## 5-Point Quality Inspection Protocol

### 1. Typography & Spelling Verification (Gate A)
- Inspect all visible text in `SCxx.png`.
- Compare against `SM01.elements[].exact_text`.
- Check: Letter clarity, correct capitalization, absence of AI pseudo-text/glyphs, and monoline marker consistency.

### 2. Element Inventory Completeness (Gate B)
- Identify all visual objects on canvas.
- Verify 1-to-1 mapping with `SM01.elements`:
  * Missing elements? (Element declared in SM01 but absent from image).
  * Phantom / Hallucinated elements? (Extra decorative flowers, frames, or random icons not requested).

### 3. Subtitle Safe Zone Clearance (Gate C)
- Algorithmic pixel check: Inspect canvas region $y \in [900, 1080]$ across all $x \in [0, 1920]$.
- Tolerance: Region must be $\ge 99.5\%$ pure white (`#FFFFFF`). Any marker ink detected inside this zone triggers an automatic defect flag.

### 4. Ink-Island & Zero-Contact Gutter Check (Gate D)
- Measure white space margin between adjacent elements.
- Required minimum gutter: 30 pixels.
- Flag any touching outlines or bleeding fills that would confuse semantic segmentation.

### 5. Computer Vision (CV) Segmentation Audit (Gate E)
- Run/evaluate segmentation masks:
  * Has each `element_id` been successfully isolated into a clean binary mask?
  * Is there mask fragmentation (one single icon broken into 10 disjointed specks)?
  * Is there mask merger (two separate words merged into one blob)?
- Record `actual_bbox_px`: $[x_{\min}, y_{\min}, \text{width}, \text{height}]$ for each accepted element.

## Output Artifact Schema (`accepted_cv_manifest.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "CV_MANIFEST_01",
  "audit_timestamp": "ISO-8601",
  "status": "APPROVED_FOR_ANIMATION | REVISION_REQUIRED",
  "scenes": [
    {
      "scene_id": "SC01",
      "image_path": "projects/WB-xxxx/08_image_assets/SC01.png",
      "resolution": [1920, 1080],
      "qa_verdict": "PASS",
      "safe_zone_compliant": true,
      "text_accuracy_compliant": true,
      "accepted_elements": [
        {
          "element_id": "SC01_E01",
          "actual_bbox_px": [150, 220, 380, 410],
          "mask_path": "projects/WB-xxxx/08_image_assets/masks/SC01_E01.png",
          "stroke_density_score": 0.42,
          "cv_segmentation_quality": "HIGH"
        },
        {
          "element_id": "SC01_E02",
          "actual_bbox_px": [180, 660, 320, 110],
          "mask_path": "projects/WB-xxxx/08_image_assets/masks/SC01_E02.png",
          "stroke_density_score": 0.28,
          "cv_segmentation_quality": "HIGH"
        }
      ]
    }
  ],
  "defect_log": []
}
```

## Mandatory Quality Gate G07

- Output `IMAGE_QA_REPORT.md` summarizing inspection results for all scenes.
- If defects exist: Assign status `REVISION_REQUIRED`, specify exact defect coordinates, and generate a surgical regeneration prompt or inpainting directive.
- If all scenes pass: Assign status `APPROVED_FOR_ANIMATION`, produce `accepted_cv_manifest.json`, and unlock Gate G07 for S07 (Voice–Animation Timeline Builder).

