#!/usr/bin/env python3
"""
build_all_annotations.py — Tự động sinh kịch bản phân vùng vẽ (.annotation.json)
và ảnh bản đồ phân vùng (_regions.png) cho toàn bộ Scene 03 -> Scene 09 của WB-ENG-A1-003.
"""

import json
from pathlib import Path
import cv2
import numpy as np

PALETTE = [
    (230, 40, 40), (40, 160, 230), (40, 200, 40), (200, 40, 180),
    (180, 120, 40), (140, 40, 220), (220, 140, 20), (20, 180, 220),
    (40, 180, 100), (180, 40, 40), (0, 140, 255), (100, 100, 255)
]

SCENE_DEFS = {
    3: {
        "title": "REGION 1: WHO OR WHAT? (NOUNS)",
        "sceneDurationMs": 41480,
        "globalStartMs": 73360,
        "globalEndMs": 114840,
        "srtStartCue": 15,
        "srtEndCue": 20,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "REGION 1: WHO OR WHAT? (NOUNS)", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 40, "width": 1520, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 3500}},
            {"id": "el-02-card-teacher", "sequence": 2, "label": "I am a teacher. 👩‍🏫", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 240, "width": 570, "height": 600},
             "reveal": {"direction": "left_to_right", "startMs": 5000, "durationMs": 6500}},
            {"id": "el-03-card-doctor", "sequence": 3, "label": "He is a doctor. 👨‍⚕️", "type": "box", "colorMode": "auto",
             "region": {"x": 660, "y": 240, "width": 600, "height": 600},
             "reveal": {"direction": "left_to_right", "startMs": 12500, "durationMs": 6500}},
            {"id": "el-04-card-students", "sequence": 4, "label": "They are students. 👥", "type": "box", "colorMode": "auto",
             "region": {"x": 1270, "y": 240, "width": 590, "height": 600},
             "reveal": {"direction": "left_to_right", "startMs": 19500, "durationMs": 6500}},
            {"id": "el-05-bottom-rule", "sequence": 5, "label": "A/AN for 1 person vs S for 2+ people", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 860, "width": 1720, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 27000, "durationMs": 13000}}
        ]
    },
    4: {
        "title": "REGIONS 2 & 3: FEELINGS & LOCATIONS",
        "sceneDurationMs": 38980,
        "globalStartMs": 114840,
        "globalEndMs": 153820,
        "srtStartCue": 21,
        "srtEndCue": 27,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "REGIONS 2 & 3: FEELINGS & LOCATIONS", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 40, "width": 1620, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 3500}},
            {"id": "el-02-left-panel", "sequence": 2, "label": "FEELINGS & STATES (HOW?) - She is happy / We are tired", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 190, "width": 860, "height": 700},
             "reveal": {"direction": "left_to_right", "startMs": 4500, "durationMs": 14500}},
            {"id": "el-03-right-panel", "sequence": 3, "label": "LOCATIONS (WHERE?) - I am at home / They are at school", "type": "box", "colorMode": "auto",
             "region": {"x": 960, "y": 190, "width": 880, "height": 700},
             "reveal": {"direction": "left_to_right", "startMs": 20000, "durationMs": 13000}},
            {"id": "el-04-bottom-takeaway", "sequence": 4, "label": "NO ACTION VERB NEEDED — TO BE DOES IT ALL!", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 900, "width": 1720, "height": 150},
             "reveal": {"direction": "left_to_right", "startMs": 33500, "durationMs": 4800}}
        ]
    },
    5: {
        "title": "THE 3 FORMS: AM — IS — ARE",
        "sceneDurationMs": 52100,
        "globalStartMs": 153820,
        "globalEndMs": 205920,
        "srtStartCue": 28,
        "srtEndCue": 34,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "THE 3 FORMS: AM — IS — ARE", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 40, "width": 1520, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4500}},
            {"id": "el-02-box-am", "sequence": 2, "label": "AM (ONLY FOR 'I') - I am ready.", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 230, "width": 550, "height": 620},
             "reveal": {"direction": "left_to_right", "startMs": 6000, "durationMs": 9500}},
            {"id": "el-03-box-is", "sequence": 3, "label": "IS (SINGULAR = 1) - S = SINGLE - He is tall.", "type": "box", "colorMode": "auto",
             "region": {"x": 640, "y": 230, "width": 640, "height": 620},
             "reveal": {"direction": "left_to_right", "startMs": 16500, "durationMs": 17000}},
            {"id": "el-04-box-are", "sequence": 4, "label": "ARE (PLURAL = 2+ & YOU) - We are ready.", "type": "box", "colorMode": "auto",
             "region": {"x": 1290, "y": 230, "width": 570, "height": 620},
             "reveal": {"direction": "left_to_right", "startMs": 34500, "durationMs": 12000}},
            {"id": "el-05-bottom-tip", "sequence": 5, "label": "REMEMBER THE 'S' RULE FOR SINGULAR!", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 860, "width": 1720, "height": 190},
             "reveal": {"direction": "left_to_right", "startMs": 47500, "durationMs": 4000}}
        ]
    },
    6: {
        "title": "SHORT FORMS (CONTRACTIONS)",
        "sceneDurationMs": 45260,
        "globalStartMs": 205920,
        "globalEndMs": 251180,
        "srtStartCue": 35,
        "srtEndCue": 41,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "SHORT FORMS (CONTRACTIONS)", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 40, "width": 1520, "height": 150},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4000}},
            {"id": "el-02-magic-shears", "sequence": 2, "label": "Apostrophe Shears ✂️ Cuts The Letter", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 200, "width": 1720, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 5500, "durationMs": 6500}},
            {"id": "el-03-pair-im", "sequence": 3, "label": "I am -> I'm (/aɪm/)", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 390, "width": 1720, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 13000, "durationMs": 7500}},
            {"id": "el-04-pair-hes-shes", "sequence": 4, "label": "He is -> He's | She is -> She's (/z/)", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 540, "width": 1720, "height": 230},
             "reveal": {"direction": "left_to_right", "startMs": 21500, "durationMs": 9500}},
            {"id": "el-05-pair-theyre-were", "sequence": 5, "label": "They are -> They're | We are -> We're", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 780, "width": 1720, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 32000, "durationMs": 6500}},
            {"id": "el-06-pronunciation-badge", "sequence": 6, "label": "SOUND NATURAL: DROP VOWEL, KEEP END SOUND!", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 930, "width": 1720, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 39500, "durationMs": 5000}}
        ]
    },
    7: {
        "title": "COMMON MISTAKES TO AVOID",
        "sceneDurationMs": 37980,
        "globalStartMs": 251180,
        "globalEndMs": 289160,
        "srtStartCue": 42,
        "srtEndCue": 48,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "COMMON MISTAKES TO AVOID", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 40, "width": 1520, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4000}},
            {"id": "el-02-col-wrong", "sequence": 2, "label": "DON'T SAY ❌ (I tired / I am go)", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 180, "width": 860, "height": 670},
             "reveal": {"direction": "left_to_right", "startMs": 5500, "durationMs": 13500}},
            {"id": "el-03-col-correct", "sequence": 3, "label": "SAY THIS ✔️ (I am tired / I go to school)", "type": "box", "colorMode": "auto",
             "region": {"x": 960, "y": 180, "width": 880, "height": 670},
             "reveal": {"direction": "left_to_right", "startMs": 20000, "durationMs": 11500}},
            {"id": "el-04-bottom-shield", "sequence": 4, "label": "TO BE + ADJECTIVE/NOUN (NO: TO BE + VERB)", "type": "box", "colorMode": "none",
             "region": {"x": 100, "y": 860, "width": 1720, "height": 190},
             "reveal": {"direction": "left_to_right", "startMs": 32500, "durationMs": 5000}}
        ]
    },
    8: {
        "title": "PRACTICE: CHOOSE AM / IS / ARE (PART 1)",
        "sceneDurationMs": 32620,
        "globalStartMs": 289160,
        "globalEndMs": 321780,
        "srtStartCue": 49,
        "srtEndCue": 53,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "PRACTICE: CHOOSE AM / IS / ARE", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 40, "width": 1620, "height": 170},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4500}},
            {"id": "el-02-q1-student", "sequence": 2, "label": "1. I ___ a student. -> [ AM ] ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 220, "width": 1720, "height": 380},
             "reveal": {"direction": "left_to_right", "startMs": 5500, "durationMs": 12500}},
            {"id": "el-03-q2-happy", "sequence": 3, "label": "2. She ___ very happy. -> [ IS ] ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 610, "width": 1720, "height": 430},
             "reveal": {"direction": "left_to_right", "startMs": 18500, "durationMs": 13500}}
        ]
    },
    9: {
        "title": "PRACTICE (PART 2) & RECAP",
        "sceneDurationMs": 52380,
        "globalStartMs": 321780,
        "globalEndMs": 374160,
        "srtStartCue": 54,
        "srtEndCue": 62,
        "elements": [
            {"id": "el-01-title", "sequence": 1, "label": "PRACTICE: CHOOSE AM / IS / ARE", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 40, "width": 1620, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 3500}},
            {"id": "el-02-q3-cat", "sequence": 2, "label": "3. The cat ___ sleeping. -> [ IS ] ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 180, "width": 1720, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 4500, "durationMs": 9500}},
            {"id": "el-03-q4-friends", "sequence": 3, "label": "4. Tom and Mary ___ friends. -> [ ARE ] ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 330, "width": 1720, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 14500, "durationMs": 11500}},
            {"id": "el-04-q5-home", "sequence": 4, "label": "5. We ___ at home. -> [ ARE ] ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 480, "width": 1720, "height": 150},
             "reveal": {"direction": "left_to_right", "startMs": 26500, "durationMs": 7500}},
            {"id": "el-05-master-recap", "sequence": 5, "label": "MASTER RECAP: AM (I) | IS (He/She/It/1) | ARE (You/We/They/2+)", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 640, "width": 1720, "height": 420},
             "reveal": {"direction": "left_to_right", "startMs": 35000, "durationMs": 16500}}
        ]
    }
}


def build_scene(s_num: int, project_dir: Path):
    img_path = project_dir / "images" / f"scene_{s_num:02d}.png"
    annot_path = project_dir / "images" / f"scene_{s_num:02d}.annotation.json"
    region_path = project_dir / "images" / f"scene_{s_num:02d}_regions.png"

    if not img_path.exists():
        print(f"Bỏ qua Scene {s_num}: Không tìm thấy ảnh {img_path}")
        return

    data = SCENE_DEFS[s_num]
    annotation = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": data["sceneDurationMs"],
        "globalStartMs": data["globalStartMs"],
        "globalEndMs": data["globalEndMs"],
        "srtStartCue": data["srtStartCue"],
        "srtEndCue": data["srtEndCue"],
        "fps": 60,
        "elements": data["elements"]
    }

    with open(annot_path, "w", encoding="utf-8") as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)

    # Draw regions visualization
    img = cv2.imread(str(img_path))
    vis = img.copy()
    h, w = img.shape[:2]

    # Verify coverage
    thresh = cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10) < 190
    total_ink = int(np.count_nonzero(thresh))

    coverage = np.zeros((h, w), dtype=int)
    for el in data["elements"]:
        idx = el["sequence"]
        r = el["region"]
        x, y, rw, rh = r["x"], r["y"], r["width"], r["height"]
        color = PALETTE[(idx - 1) % len(PALETTE)]
        cv2.rectangle(vis, (x, y), (x + rw, y + rh), color, 3)

        eid = el.get("id", f"el-{idx}")
        badge_txt = f"[{idx}] {eid}"
        badge_w = len(badge_txt) * 11 + 16
        badge_y = y - 8 if y > 35 else y + rh + 24
        cv2.rectangle(vis, (x, badge_y - 22), (x + badge_w, badge_y + 4), color, -1)
        cv2.putText(vis, badge_txt, (x + 6, badge_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

        coverage[y:y+rh, x:x+rw] += 1

    cv2.imwrite(str(region_path), vis)

    covered_ink = int(np.count_nonzero((coverage >= 1) & thresh))
    pct = (covered_ink / total_ink * 100.0) if total_ink > 0 else 100.0
    overlap = int(np.count_nonzero((coverage > 1) & thresh))
    print(f"  • Scene {s_num:02d}: {len(data['elements'])} elements | Mực: {pct:.1f}% ({covered_ink:,}/{total_ink:,}) | Trùng: {overlap}px | Xuất: {region_path.name}")


def main():
    root = Path("projects/WB-ENG-A1-003")
    print("=" * 65)
    print(" TỰ ĐỘNG PHÂN VÙNG VÀ XUẤT TOÀN BỘ REGION MAPS (SCENE 03 -> 09)")
    print("=" * 65)
    for s in range(3, 10):
        build_scene(s, root)
    print("=" * 65)
    print("🎉 Hoàn tất tự động hóa phân vùng cho toàn bộ các Scene còn lại!")


if __name__ == "__main__":
    main()
