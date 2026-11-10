---
name: voice-animation-timeline-builder
description: Synthesizes actual recorded voiceover audio, word-level forced alignment data, accepted CV element manifests, and renderer drawing speed profiles into a mathematically synchronized production timeline (timeline.json) for video rendering (S07).
---
# Voice–Animation Timeline Builder — S07

## Mission

Serve as the **Master Audio-Visual Synchronization & Renderer Calibration Engineer**. S07 assembles the final, frame-accurate animation timeline that commands the downstream video renderer (`render_stream_whiteboard.py`).

S07 operates exclusively on **empirical production data**: actual recorded voiceover audio, exact forced-alignment timestamps, accepted CV element masks from S06B, and calibrated hand-drawing speed profiles. It guarantees that the viewer sees the marker draw each concept in perfect harmony with the spoken words, completely eliminating voice-visual lag or rushed animation.

## Governing Invariants for Timeline Building

1. **Empirical Audio Timestamp Requirement:** Never substitute estimated sentence durations for actual audio timestamps. S07 requires real audio (`voiceover.wav`) and a valid forced-alignment transcript (`alignment.json`).
2. **Drawing Speed Calibration:** Hand-drawing duration is not arbitrary. It is a function of element stroke density, contour perimeter, and renderer drawing profile:
   $$T_{\text{draw}} = \frac{\text{Stroke Length (pixels)}}{\text{Renderer Speed (px/s)}} + T_{\text{hand\_approach\_retract}}$$
3. **Synchronous Anchoring Rule:** The drawing of an element MUST commence precisely at the onset of its bound narration cue word ($\pm 0.1\text{s}$) or complete right as the key word is emphasized, depending on the didactic intent (Draw-Ahead vs. Draw-With).
4. **No Clashing Overlaps:** If element $B$ is scheduled to draw while element $A$ is still being drawn on the same board, the hand animation will collide. S07 detects draw collisions and automatically re-times or accelerates strokes to preserve visual clarity.

## Required Input Contract

1. `projects/<project_id>/09_audio/voiceover.wav` (actual voiceover file).
2. `projects/<project_id>/09_audio/alignment.json` (word/phoneme forced-alignment data).
3. `projects/<project_id>/06_scene_matrix/SM01.json` (approved, with cue bindings).
4. `projects/<project_id>/08_image_assets/accepted_cv_manifest.json` (from S06B).
5. Renderer configuration: Drawing profile settings (e.g. from `config/` or `render_stream_whiteboard.py`).

*Precondition Guard:* If actual audio or accepted CV manifest is missing, S07 stops with `BLOCKED_AWAITING_PRODUCTION_ASSETS`. S07 NEVER fabricates timestamps.

## Timeline Synchronization Mechanics

### 1. Cue-to-Audio Mapping
- For each element in `SM01`:
  * Look up its `bound_narration_cue` (e.g., `"two apples"`).
  * Locate the exact start timestamp ($t_{\text{start}}$) and end timestamp ($t_{\text{end}}$) in `alignment.json`.
  * Set $t_{\text{trigger}} = t_{\text{start}}$.

### 2. Draw Duration & Speed Profile Calculation
- Query `accepted_cv_manifest.json` for `stroke_density_score` and bounding box dimensions.
- Calculate available audio window: $\Delta t_{\text{window}} = t_{\text{next\_trigger}} - t_{\text{trigger}}$.
- Determine draw speed multiplier:
  * If base draw duration exceeds $\Delta t_{\text{window}}$, scale drawing velocity so the stroke completes before the next cue begins.
  * If $\Delta t_{\text{window}}$ is generous, allow a natural, smooth marker stroke followed by a static hold.

### 3. Subtitle Event Integration
- Generate word-level or phrase-level subtitle events aligned with audio timestamps, strictly formatted for the subtitle safe zone ($y \in [920, 1040]$).

## Output Artifact Schema (`timeline.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "TIMELINE_01",
  "audio_file": "projects/WB-xxxx/09_audio/voiceover.wav",
  "total_duration_seconds": 298.42,
  "renderer_profile": "STANDARD_MARKER_V2",
  "scenes": [
    {
      "scene_id": "SC01",
      "start_time_seconds": 0.0,
      "end_time_seconds": 44.5,
      "background_image": "projects/WB-xxxx/08_image_assets/SC01.png",
      "animation_events": [
        {
          "event_id": "EV_01",
          "element_id": "SC01_E01",
          "action_type": "DRAW_STROKE_WITH_HAND",
          "start_time_seconds": 2.14,
          "duration_seconds": 2.80,
          "end_time_seconds": 4.94,
          "mask_file": "projects/WB-xxxx/08_image_assets/masks/SC01_E01.png",
          "hand_style": "default_right_hand",
          "cue_phrase": "two apples",
          "easing": "ease_in_out"
        },
        {
          "event_id": "EV_02",
          "element_id": "SC01_E02",
          "action_type": "DRAW_TEXT_LABEL",
          "start_time_seconds": 5.10,
          "duration_seconds": 1.40,
          "end_time_seconds": 6.50,
          "mask_file": "projects/WB-xxxx/08_image_assets/masks/SC01_E02.png",
          "cue_phrase": "two apples",
          "easing": "linear"
        }
      ],
      "subtitles": [
        {
          "start_time_seconds": 0.5,
          "end_time_seconds": 4.8,
          "text": "Have you ever wondered why we say 'two apples'..."
        }
      ]
    }
  ],
  "collision_audit": {
    "hand_collision_detected": false,
    "max_draw_velocity_factor": 1.15
  },
  "approval_gate": {
    "gate_id": "G08",
    "state": "READY_FOR_STREAM_RENDER"
  }
}
```

## Mandatory Quality Gate G08

- Verify `collision_audit.hand_collision_detected == false`.
- Check that all elements from `accepted_cv_manifest.json` have corresponding `animation_events`.
- Output `TIMELINE_QA_REPORT.md` confirming audio-visual synchronization metrics.
- Unlock downstream rendering engine (`render_stream_whiteboard.py`).

