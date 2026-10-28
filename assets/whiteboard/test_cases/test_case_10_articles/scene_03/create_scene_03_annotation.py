#!/usr/bin/env python3
"""
Tạo annotation chuẩn cho Scene 03: WHAT ARE A AND AN?
Schema: region {x, y, width, height}, reveal {startMs, durationMs, direction}
Màu loang: type "colored_image", colorMode "wash" cho book icon, apple icon, box icon.
"""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent

timing_path = DIR / "timing_cues.json"
timing_data = json.loads(timing_path.read_text(encoding="utf-8"))
total_duration_ms = timing_data["totalDurationMs"]

elements = [
    # 1. Title: WHAT ARE A AND AN? (Line 1: 500 - 3692ms)
    {
        "id": "el-01-title",
        "label": "Title: WHAT ARE A AND AN?",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 360, "y": 65, "width": 1200, "height": 125},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 3000,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 2. Core Concept Text: ONE + COUNTABLE NOUN (Line 2: 4192 - 11680ms)
    {
        "id": "el-02-concept-text",
        "label": "Concept: ONE + COUNTABLE NOUN",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 280, "y": 840, "width": 1180, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4200,
            "durationMs": 4200,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 3. Box Icon beside concept (Line 2: 8600 - 11500ms)
    {
        "id": "el-03-box-icon",
        "label": "Single Item Box Icon",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1485, "y": 810, "width": 185, "height": 175},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8600,
            "durationMs": 2800,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 4. Book Icon (Line 3: 12180 - 15372ms)
    {
        "id": "el-04-book-icon",
        "label": "Book Illustration",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 280, "y": 270, "width": 460, "height": 330},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12200,
            "durationMs": 2000,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 5. Label: a book (Line 3: 14300 - 15350ms)
    {
        "id": "el-05-book-label",
        "label": "Label: a book",
        "sequence": 5,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 340, "y": 600, "width": 330, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 14300,
            "durationMs": 1050,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 6. Apple Icon (Line 4: 15872 - 18584ms)
    {
        "id": "el-06-apple-icon",
        "label": "Apple Illustration",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1230, "y": 260, "width": 310, "height": 330},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15900,
            "durationMs": 1600,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 7. Label: an apple (Line 4: 17600 - 18550ms)
    {
        "id": "el-07-apple-label",
        "label": "Label: an apple",
        "sequence": 7,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1180, "y": 630, "width": 410, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17600,
            "durationMs": 950,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_10_scene_03",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

out_path = DIR / "scene_03.annotation.json"
out_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[Scene 03] Saved {len(elements)} elements to {out_path}")

# Tự động xuất ảnh phân vùng chuẩn scene_03-regions.png
import subprocess, sys
repo_root = DIR.parent.parent.parent.parent
regions_png = DIR / "scene_03-regions.png"
subprocess.run([
    sys.executable,
    str(repo_root / "scripts/render_annotation_preview.py"),
    str(DIR / "scene_03.png"),
    str(out_path),
    str(regions_png)
], check=True)
print(f"[Scene 03] Generated {regions_png}")
