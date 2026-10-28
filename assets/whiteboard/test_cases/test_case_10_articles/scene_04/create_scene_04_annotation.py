#!/usr/bin/env python3
"""
Tạo annotation chuẩn cho Scene 04: CHOOSE BY THE FIRST SOUND
Tối ưu hóa bố cục: Bảng được căn chỉnh cân đối (bottom=989px), để lại 90px biên dưới cho phụ đề MarginV=4.
Màu loang: type "colored_image", colorMode "wash" cho center box, consonant box, vowel box, book icon, apple icon, summary.
"""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent

timing_path = DIR / "timing_cues.json"
timing_data = json.loads(timing_path.read_text(encoding="utf-8"))
total_duration_ms = timing_data["totalDurationMs"]

elements = [
    # 1. Title: A OR AN? FIRST SOUND (Line 1: 500 - 3452ms)
    {
        "id": "el-01-title",
        "label": "Title: A OR AN? FIRST SOUND",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 700, "y": 62, "width": 520, "height": 193},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2800,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 2. Center Node: FIRST SOUND Box (Line 2: 3952 - 7024ms)
    {
        "id": "el-02-center-box",
        "label": "Center Node: FIRST SOUND",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 763, "y": 268, "width": 394, "height": 103},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 3950,
            "durationMs": 1000,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 3. Left Branch Arrows
    {
        "id": "el-03-left-arrows",
        "label": "Left Branch Arrows",
        "sequence": 3,
        "type": "connector",
        "colorMode": "none",
        "region": {"x": 503, "y": 295, "width": 251, "height": 107},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5000,
            "durationMs": 500,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 4. Box: CONSONANT SOUND (Blue)
    {
        "id": "el-04-box-consonant",
        "label": "Box: CONSONANT SOUND (Blue)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 369, "y": 407, "width": 354, "height": 161},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5550,
            "durationMs": 900,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 5. Big letter A
    {
        "id": "el-05-big-a",
        "label": "Letter: A",
        "sequence": 5,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 490, "y": 577, "width": 112, "height": 76},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6500,
            "durationMs": 500,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 6. Right Branch Arrows (Line 3: 7524 - 10740ms)
    {
        "id": "el-06-right-arrows",
        "label": "Right Branch Arrows",
        "sequence": 6,
        "type": "connector",
        "colorMode": "none",
        "region": {"x": 1157, "y": 295, "width": 260, "height": 107},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7550,
            "durationMs": 550,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 7. Box: VOWEL SOUND (Orange)
    {
        "id": "el-07-box-vowel",
        "label": "Box: VOWEL SOUND (Orange)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1211, "y": 407, "width": 331, "height": 161},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8150,
            "durationMs": 1300,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 8. Big letter AN
    {
        "id": "el-08-big-an",
        "label": "Letter: AN",
        "sequence": 8,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1291, "y": 577, "width": 166, "height": 76},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9500,
            "durationMs": 1100,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 9. Book Icon (Line 4: 11240 - 17120ms)
    {
        "id": "el-09-book-icon",
        "label": "Book Icon",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 449, "y": 658, "width": 215, "height": 148},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11300,
            "durationMs": 3200,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 10. Text: a book
    {
        "id": "el-10-book-text",
        "label": "Text: a book",
        "sequence": 10,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 449, "y": 810, "width": 215, "height": 67},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 14600,
            "durationMs": 2200,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 11. Apple Icon (Line 5: 17620 - 23500ms)
    {
        "id": "el-11-apple-icon",
        "label": "Apple Icon",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1291, "y": 658, "width": 166, "height": 148},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17700,
            "durationMs": 3100,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 12. Text: an apple
    {
        "id": "el-12-apple-text",
        "label": "Text: an apple",
        "sequence": 12,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1247, "y": 810, "width": 260, "height": 76},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 20900,
            "durationMs": 2300,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 13. Summary: SOUND, NOT LETTER (Line 6: 24000 - 29040ms)
    {
        "id": "el-13-summary",
        "label": "Reminder: SOUND, NOT LETTER",
        "sequence": 13,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 638, "y": 886, "width": 672, "height": 103},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 24100,
            "durationMs": 4400,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_10_scene_04",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

out_path = DIR / "scene_04.annotation.json"
out_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[Scene 04] Saved {len(elements)} elements to {out_path}")

# Tự động xuất ảnh phân vùng chuẩn scene_04-regions.png
import subprocess, sys
repo_root = DIR.parent.parent.parent.parent
regions_png = DIR / "scene_04-regions.png"
subprocess.run([
    sys.executable,
    str(repo_root / "scripts/render_annotation_preview.py"),
    str(DIR / "scene_04.png"),
    str(out_path),
    str(regions_png)
], check=True)
print(f"[Scene 04] Generated {regions_png}")
