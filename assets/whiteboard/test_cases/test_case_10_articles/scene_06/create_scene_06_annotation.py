#!/usr/bin/env python3
"""
Tạo annotation chuẩn cho Scene 06: SPECIAL CASES: FIRST SOUND
Atomic Segmentation & Zero Overlap
Khắc phục triệt để lỗi màu: Cả 4 thẻ đặc biệt chứa icon và badge màu loang dùng:
  type: "colored_image", colorMode: "wash"
Tự động xuất ảnh phân vùng chuẩn scene_06-regions.png.
"""
import json
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent

timing_path = DIR / "timing_cues.json"
timing_data = json.loads(timing_path.read_text(encoding="utf-8"))
total_duration_ms = timing_data["totalDurationMs"]

elements = [
    # 1. Title: SPECIAL CASES: FIRST SOUND (Cue 1: 500ms - 4460ms)
    {
        "id": "el-01-title",
        "label": "Title: SPECIAL CASES - FIRST SOUND",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 690, "y": 68, "width": 533, "height": 157},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 3800,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 2. Card 1 (Top-Left): an hour (Cue 2: 4960ms - 12472ms)
    {
        "id": "el-02-card-hour",
        "label": "Card 1: an hour (H IS SILENT)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 139, "y": 68, "width": 539, "height": 424},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5000,
            "durationMs": 7200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 3. Card 2 (Top-Right): an honest man (Cue 3: 12972ms - 18636ms)
    {
        "id": "el-03-card-honest",
        "label": "Card 2: an honest man (H IS SILENT)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1241, "y": 68, "width": 539, "height": 424},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13000,
            "durationMs": 5400,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 4. Card 3 (Bottom-Left): a university (Cue 4: 19136ms - 25976ms)
    {
        "id": "el-04-card-university",
        "label": "Card 3: a university (STARTS WITH Y SOUND)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 139, "y": 504, "width": 805, "height": 412},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 19200,
            "durationMs": 6500,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 5. Card 4 (Bottom-Right): a European country (Cue 5: 26476ms - 32356ms)
    {
        "id": "el-05-card-european",
        "label": "Card 4: a European country (STARTS WITH Y SOUND)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 956, "y": 504, "width": 823, "height": 412},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 26500,
            "durationMs": 5600,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 6. Bottom Reminder: LISTEN TO THE FIRST SOUND (Cue 6: 32856ms - 39720ms)
    {
        "id": "el-06-bottom-reminder",
        "label": "Reminder: LISTEN TO THE FIRST SOUND",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 623, "y": 922, "width": 672, "height": 36},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 33000,
            "durationMs": 6200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_10_scene_06",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

out_path = DIR / "scene_06.annotation.json"
out_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[Scene 06] Saved {len(elements)} elements to {out_path}")

# Tự động xuất ảnh phân vùng chuẩn scene_06-regions.png
repo_root = [p for p in Path(__file__).resolve().parents if (p / "scripts").exists()][0]
regions_png = DIR / "scene_06-regions.png"
subprocess.run([
    sys.executable,
    str(repo_root / "scripts/render_annotation_preview.py"),
    str(DIR / "scene_06.png"),
    str(out_path),
    str(regions_png)
], check=True)
print(f"[Scene 06] Generated {regions_png}")
