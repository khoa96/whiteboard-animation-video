#!/usr/bin/env python3
import json
import cv2
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def process_tc04():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-04"
    img_path = proj_dir / "images/scene_01.png"
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    total_ink = np.sum(ink)

    # 1. Header: DO VS MAKE
    # 2. Left Card (DO)
    # 3. Right Baker Icon (top)
    # 4. Right Card Frame & Text (lower)
    
    # Let's inspect coordinates precisely:
    # Header: Y: 68..160, X: 645..1275
    # Left Card: Y: 162..838, X: 142..798
    # Right Card: Y: 140..838, X: 1130..1798
    
    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "DO VS MAKE",
            "region": {"x": 647, "y": 69, "width": 628, "height": 90},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_card_do",
            "type": "card",
            "label": "DO: Activities & Tasks (I do my homework.)",
            "region": {"x": 142, "y": 162, "width": 655, "height": 676},
            "reveal": {"startMs": 4500, "durationMs": 7500, "direction": "stream"},
            "colorMode": "auto"
        },
        {
            "id": "e3_card_make",
            "type": "card",
            "label": "MAKE: Create & Produce (I make a cake.)",
            "region": {"x": 1130, "y": 140, "width": 668, "height": 698},
            "reveal": {"startMs": 12500, "durationMs": 7000, "direction": "stream"},
            "colorMode": "auto"
        }
    ]

    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 20000,
        "elements": elements
    }
    (proj_dir / "images/scene_01.annotation.json").write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC04 Annotation saved.")

def process_tc05():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-05"
    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "PAST VS PRESENT",
            "region": {"x": 573, "y": 77, "width": 777, "height": 82},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_card_yesterday",
            "type": "card",
            "label": "YESTERDAY: I walked to work.",
            "region": {"x": 158, "y": 219, "width": 637, "height": 641},
            "reveal": {"startMs": 4500, "durationMs": 6500, "direction": "stream"},
            "colorMode": "auto"
        },
        {
            "id": "e3_arrow",
            "type": "underline",
            "label": "Transition Arrow",
            "region": {"x": 834, "y": 487, "width": 260, "height": 106},
            "reveal": {"startMs": 11200, "durationMs": 1000, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e4_card_today",
            "type": "card",
            "label": "TODAY: I walk to work.",
            "region": {"x": 1134, "y": 219, "width": 637, "height": 641},
            "reveal": {"startMs": 12500, "durationMs": 6500, "direction": "stream"},
            "colorMode": "auto"
        }
    ]
    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 20000,
        "elements": elements
    }
    (proj_dir / "images/scene_01.annotation.json").write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC05 Annotation saved.")

def process_tc06():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-06"
    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "3 STEPS TO SPEAK FLUENTLY",
            "region": {"x": 371, "y": 99, "width": 1179, "height": 75},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_box1_listen",
            "type": "card",
            "label": "Step 1: LISTEN (Play short audio daily.)",
            "region": {"x": 247, "y": 220, "width": 414, "height": 655},
            "reveal": {"startMs": 4500, "durationMs": 5500, "direction": "stream"},
            "colorMode": "auto"
        },
        {
            "id": "e3_arrow_1",
            "type": "underline",
            "label": "Flow Arrow 1",
            "region": {"x": 666, "y": 539, "width": 80, "height": 47},
            "reveal": {"startMs": 10200, "durationMs": 800, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e4_box2_shadow",
            "type": "card",
            "label": "Step 2: SHADOW (Copy the speaking rhythm.)",
            "region": {"x": 754, "y": 220, "width": 413, "height": 655},
            "reveal": {"startMs": 11200, "durationMs": 5500, "direction": "stream"},
            "colorMode": "auto"
        },
        {
            "id": "e5_arrow_2",
            "type": "underline",
            "label": "Flow Arrow 2",
            "region": {"x": 1174, "y": 539, "width": 80, "height": 47},
            "reveal": {"startMs": 16900, "durationMs": 800, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e6_box3_record",
            "type": "card",
            "label": "Step 3: RECORD (Check your own voice.)",
            "region": {"x": 1260, "y": 220, "width": 413, "height": 655},
            "reveal": {"startMs": 17900, "durationMs": 5500, "direction": "stream"},
            "colorMode": "auto"
        }
    ]
    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 24000,
        "elements": elements
    }
    (proj_dir / "images/scene_01.annotation.json").write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC06 Annotation saved.")

if __name__ == "__main__":
    process_tc04()
    process_tc05()
    process_tc06()
