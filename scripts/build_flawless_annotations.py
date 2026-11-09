#!/usr/bin/env python3
import json
import cv2
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def get_bbox(mask):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)

def build_tc04():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-04"
    img_path = proj_dir / "images/scene_01.png"
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    total_ink = np.sum(ink)

    # 1. Header: DO VS MAKE (Y: 60..180, X: 600..1300)
    bx_hdr = get_bbox(ink[60:180, 600:1300])
    bx_hdr = [bx_hdr[0] + 600, bx_hdr[1] + 60, bx_hdr[2], bx_hdr[3]]

    # 2. Left Container: X: 130..810, Y: 150..850
    bx_c_left = get_bbox(ink[150:850, 130:810])
    bx_c_left = [bx_c_left[0] + 130, bx_c_left[1] + 150, bx_c_left[2], bx_c_left[3]]

    # 3. Right Container: X: 1110..1810, Y: 150..850
    bx_c_right = get_bbox(ink[150:850, 1110:1810])
    bx_c_right = [bx_c_right[0] + 1110, bx_c_right[1] + 150, bx_c_right[2], bx_c_right[3]]

    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "DO VS MAKE",
            "region": {"x": bx_hdr[0] - 2, "y": bx_hdr[1] - 2, "width": bx_hdr[2] + 4, "height": bx_hdr[3] + 4},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_card_do",
            "type": "card",
            "label": "DO: Activities & Tasks (I do my homework.)",
            "region": {"x": bx_c_left[0] - 2, "y": bx_c_left[1] - 2, "width": bx_c_left[2] + 4, "height": bx_c_left[3] + 4},
            "reveal": {"startMs": 4500, "durationMs": 6500, "direction": "stream"},
            "colorMode": "auto"
        },
        {
            "id": "e3_card_make",
            "type": "card",
            "label": "MAKE: Create & Produce (I make a cake.)",
            "region": {"x": bx_c_right[0] - 2, "y": bx_c_right[1] - 2, "width": bx_c_right[2] + 4, "height": bx_c_right[3] + 4},
            "reveal": {"startMs": 11500, "durationMs": 7500, "direction": "stream"},
            "colorMode": "auto"
        }
    ]

    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 20000,
        "elements": elements
    }
    out_ann = proj_dir / "images/scene_01.annotation.json"
    out_ann.write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC04 annotation written: {len(elements)} elements")
    return ann, ink, total_ink

def build_tc05():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-05"
    img_path = proj_dir / "images/scene_01.png"
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    total_ink = np.sum(ink)

    # 1. Header: PAST VS PRESENT (Y: 60..180, X: 500..1400)
    bx_hdr = get_bbox(ink[60:180, 500:1400])
    bx_hdr = [bx_hdr[0] + 500, bx_hdr[1] + 60, bx_hdr[2], bx_hdr[3]]

    # 2. Left Card (Yesterday): X: 140..810, Y: 200..870
    bx_left = get_bbox(ink[200:870, 140:810])
    bx_left = [bx_left[0] + 140, bx_left[1] + 200, bx_left[2], bx_left[3]]

    # 3. Arrow: X: 820..1120, Y: 400..600
    bx_arrow = get_bbox(ink[400:600, 820:1120])
    if bx_arrow:
        bx_arrow = [bx_arrow[0] + 820, bx_arrow[1] + 400, bx_arrow[2], bx_arrow[3]]

    # 4. Right Card (Today): X: 1120..1800, Y: 200..870
    bx_right = get_bbox(ink[200:870, 1120:1800])
    bx_right = [bx_right[0] + 1120, bx_right[1] + 200, bx_right[2], bx_right[3]]

    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "PAST VS PRESENT",
            "region": {"x": bx_hdr[0] - 2, "y": bx_hdr[1] - 2, "width": bx_hdr[2] + 4, "height": bx_hdr[3] + 4},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_card_yesterday",
            "type": "card",
            "label": "YESTERDAY: I walked to work.",
            "region": {"x": bx_left[0] - 2, "y": bx_left[1] - 2, "width": bx_left[2] + 4, "height": bx_left[3] + 4},
            "reveal": {"startMs": 4500, "durationMs": 6500, "direction": "stream"},
            "colorMode": "auto"
        }
    ]
    if bx_arrow:
        elements.append({
            "id": "e3_arrow",
            "type": "underline",
            "label": "Transition Arrow",
            "region": {"x": bx_arrow[0] - 2, "y": bx_arrow[1] - 2, "width": bx_arrow[2] + 4, "height": bx_arrow[3] + 4},
            "reveal": {"startMs": 11500, "durationMs": 1000, "direction": "left-to-right"},
            "colorMode": "none"
        })
    elements.append({
        "id": "e4_card_today",
        "type": "card",
        "label": "TODAY: I walk to work.",
        "region": {"x": bx_right[0] - 2, "y": bx_right[1] - 2, "width": bx_right[2] + 4, "height": bx_right[3] + 4},
        "reveal": {"startMs": 12800, "durationMs": 6500, "direction": "stream"},
        "colorMode": "auto"
    })

    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 20000,
        "elements": elements
    }
    out_ann = proj_dir / "images/scene_01.annotation.json"
    out_ann.write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC05 annotation written: {len(elements)} elements")
    return ann, ink, total_ink

def build_tc06():
    proj_dir = REPO_ROOT / "projects/WB-TEST-CASE-06"
    img_path = proj_dir / "images/scene_01.png"
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    total_ink = np.sum(ink)

    # 1. Header: 3 STEPS TO SPEAK FLUENTLY (Y: 60..190, X: 300..1600)
    bx_hdr = get_bbox(ink[60:190, 300:1600])
    bx_hdr = [bx_hdr[0] + 300, bx_hdr[1] + 60, bx_hdr[2], bx_hdr[3]]

    # 2. Box 1 (Listen): X: 80..580, Y: 190..850
    bx_box1 = get_bbox(ink[190:850, 80:580])
    bx_box1 = [bx_box1[0] + 80, bx_box1[1] + 190, bx_box1[2], bx_box1[3]]

    # 3. Arrow A: X: 580..720, Y: 400..600
    bx_arr_a = get_bbox(ink[400:600, 580:720])
    if bx_arr_a:
        bx_arr_a = [bx_arr_a[0] + 580, bx_arr_a[1] + 400, bx_arr_a[2], bx_arr_a[3]]

    # 4. Box 2 (Shadow): X: 710..1210, Y: 190..850
    bx_box2 = get_bbox(ink[190:850, 710:1210])
    bx_box2 = [bx_box2[0] + 710, bx_box2[1] + 190, bx_box2[2], bx_box2[3]]

    # 5. Arrow B: X: 1210..1350, Y: 400..600
    bx_arr_b = get_bbox(ink[400:600, 1210:1350])
    if bx_arr_b:
        bx_arr_b = [bx_arr_b[0] + 1210, bx_arr_b[1] + 400, bx_arr_b[2], bx_arr_b[3]]

    # 6. Box 3 (Record): X: 1340..1840, Y: 190..850
    bx_box3 = get_bbox(ink[190:850, 1340:1840])
    bx_box3 = [bx_box3[0] + 1340, bx_box3[1] + 190, bx_box3[2], bx_box3[3]]

    elements = [
        {
            "id": "e1_header",
            "type": "text",
            "label": "3 STEPS TO SPEAK FLUENTLY",
            "region": {"x": bx_hdr[0] - 2, "y": bx_hdr[1] - 2, "width": bx_hdr[2] + 4, "height": bx_hdr[3] + 4},
            "reveal": {"startMs": 500, "durationMs": 3500, "direction": "left-to-right"},
            "colorMode": "none"
        },
        {
            "id": "e2_box1_listen",
            "type": "card",
            "label": "Step 1: LISTEN (Play short audio daily.)",
            "region": {"x": bx_box1[0] - 2, "y": bx_box1[1] - 2, "width": bx_box1[2] + 4, "height": bx_box1[3] + 4},
            "reveal": {"startMs": 4500, "durationMs": 5500, "direction": "stream"},
            "colorMode": "auto"
        }
    ]
    if bx_arr_a:
        elements.append({
            "id": "e3_arrow_a",
            "type": "underline",
            "label": "Flow Arrow 1",
            "region": {"x": bx_arr_a[0] - 2, "y": bx_arr_a[1] - 2, "width": bx_arr_a[2] + 4, "height": bx_arr_a[3] + 4},
            "reveal": {"startMs": 10300, "durationMs": 800, "direction": "left-to-right"},
            "colorMode": "none"
        })
    elements.append({
        "id": "e4_box2_shadow",
        "type": "card",
        "label": "Step 2: SHADOW (Copy the speaking rhythm.)",
        "region": {"x": bx_box2[0] - 2, "y": bx_box2[1] - 2, "width": bx_box2[2] + 4, "height": bx_box2[3] + 4},
        "reveal": {"startMs": 11300, "durationMs": 5500, "direction": "stream"},
        "colorMode": "auto"
    })
    if bx_arr_b:
        elements.append({
            "id": "e5_arrow_b",
            "type": "underline",
            "label": "Flow Arrow 2",
            "region": {"x": bx_arr_b[0] - 2, "y": bx_arr_b[1] - 2, "width": bx_arr_b[2] + 4, "height": bx_arr_b[3] + 4},
            "reveal": {"startMs": 17100, "durationMs": 800, "direction": "left-to-right"},
            "colorMode": "none"
        })
    elements.append({
        "id": "e6_box3_record",
        "type": "card",
        "label": "Step 3: RECORD (Check your own voice.)",
        "region": {"x": bx_box3[0] - 2, "y": bx_box3[1] - 2, "width": bx_box3[2] + 4, "height": bx_box3[3] + 4},
        "reveal": {"startMs": 18100, "durationMs": 5500, "direction": "stream"},
        "colorMode": "auto"
    })

    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 24000,
        "elements": elements
    }
    out_ann = proj_dir / "images/scene_01.annotation.json"
    out_ann.write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ TC06 annotation written: {len(elements)} elements")
    return ann, ink, total_ink

def verify_coverage(tc_id, ann, ink, total_ink):
    covered = np.zeros_like(ink, dtype=bool)
    boxes = []
    for el in ann["elements"]:
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        boxes.append((x, y, w, h))
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(1920, x + w), min(1080, y + h)
        covered[y1:y2, x1:x2] |= ink[y1:y2, x1:x2]

    covered_count = np.sum(covered)
    cov_pct = covered_count / total_ink * 100
    overlaps = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            b1, b2 = boxes[i], boxes[j]
            ix1, iy1 = max(b1[0], b2[0]), max(b1[1], b2[1])
            ix2, iy2 = min(b1[0] + b1[2], b2[0] + b2[2]), min(b1[1] + b1[3], b2[1] + b2[3])
            if ix1 < ix2 and iy1 < iy2:
                overlaps += 1
    print(f"[{tc_id}] Ink Coverage: {cov_pct:.3f}% ({covered_count}/{total_ink}) | Overlaps: {overlaps}")

if __name__ == "__main__":
    for tc_fn, tc_name in [(build_tc04, "TC04"), (build_tc05, "TC05"), (build_tc06, "TC06")]:
        ann, ink, tot = tc_fn()
        verify_coverage(tc_name, ann, ink, tot)
