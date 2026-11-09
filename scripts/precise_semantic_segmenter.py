#!/usr/bin/env python3
import json
import cv2
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def segment_project(proj_name, duration_ms, structure_type):
    proj_dir = REPO_ROOT / f"projects/{proj_name}"
    img_path = proj_dir / "images/scene_01.png"
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    total_ink = np.sum(ink)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    # We want to partition all components into semantic groups based on their centroid or bounding box
    # Let's see what components exist
    elements = []
    
    if structure_type == "two_cards": # TC04, TC05
        # 1. Header: components with y < 200
        # 2. Left Card: components with x < 900 and y >= 160
        # 3. Middle Arrow: components with 800 < x < 1120 and 400 < y < 650
        # 4. Right Card: components with x >= 1050 and y >= 160
        
        hdr_mask = np.zeros_like(ink, dtype=bool)
        left_mask = np.zeros_like(ink, dtype=bool)
        arrow_mask = np.zeros_like(ink, dtype=bool)
        right_mask = np.zeros_like(ink, dtype=bool)

        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            comp_mask = (labels == i)
            cy, cx = centroids[i]
            if y < 190 and cy < 190:
                hdr_mask |= comp_mask
            elif 820 <= cx <= 1100 and 420 <= cy <= 620:
                arrow_mask |= comp_mask
            elif cx < 950:
                left_mask |= comp_mask
            else:
                right_mask |= comp_mask

        masks = [("Header", hdr_mask, "text", "left-to-right", 500, 3500, "none")]
        if proj_name == "WB-TEST-CASE-04":
            masks.append(("DO: Activities & Tasks", left_mask, "card", "stream", 4500, 7500, "auto"))
            masks.append(("MAKE: Create & Produce", right_mask, "card", "stream", 12500, 7000, "auto"))
        else: # TC05
            masks.append(("YESTERDAY: I walked to work.", left_mask, "card", "stream", 4500, 6500, "auto"))
            if np.any(arrow_mask):
                masks.append(("Transition Arrow", arrow_mask, "underline", "left-to-right", 11200, 1000, "none"))
            masks.append(("TODAY: I walk to work.", right_mask, "card", "stream", 12500, 6500, "auto"))

    elif structure_type == "three_cards": # TC06
        # 1. Header: y < 190
        # 2. Box 1: cx < 600
        # 3. Arrow 1: 580 <= cx <= 730
        # 4. Box 2: 700 <= cx <= 1220
        # 5. Arrow 2: 1200 <= cx <= 1350
        # 6. Box 3: cx > 1330
        
        hdr_mask = np.zeros_like(ink, dtype=bool)
        b1_mask = np.zeros_like(ink, dtype=bool)
        arr1_mask = np.zeros_like(ink, dtype=bool)
        b2_mask = np.zeros_like(ink, dtype=bool)
        arr2_mask = np.zeros_like(ink, dtype=bool)
        b3_mask = np.zeros_like(ink, dtype=bool)

        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            comp_mask = (labels == i)
            cy, cx = centroids[i]
            if y < 190 and cy < 190:
                hdr_mask |= comp_mask
            elif 580 <= cx <= 720 and 420 <= cy <= 620 and w < 160:
                arr1_mask |= comp_mask
            elif 1210 <= cx <= 1350 and 420 <= cy <= 620 and w < 160:
                arr2_mask |= comp_mask
            elif cx < 650:
                b1_mask |= comp_mask
            elif cx < 1280:
                b2_mask |= comp_mask
            else:
                b3_mask |= comp_mask

        masks = [
            ("3 STEPS TO SPEAK FLUENTLY", hdr_mask, "text", "left-to-right", 500, 3500, "none"),
            ("Step 1: LISTEN (Play short audio daily.)", b1_mask, "card", "stream", 4500, 5500, "auto"),
            ("Flow Arrow 1", arr1_mask, "underline", "left-to-right", 10200, 800, "none"),
            ("Step 2: SHADOW (Copy the speaking rhythm.)", b2_mask, "card", "stream", 11200, 5500, "auto"),
            ("Flow Arrow 2", arr2_mask, "underline", "left-to-right", 16900, 800, "none"),
            ("Step 3: RECORD (Check your own voice.)", b3_mask, "card", "stream", 17900, 5500, "auto")
        ]

    # Convert each non-empty mask to bounding box
    elem_list = []
    idx = 1
    for name, m, el_type, direction, start_ms, dur_ms, color_mode in masks:
        if not np.any(m):
            continue
        ys, xs = np.where(m)
        x0, y0 = int(xs.min()), int(ys.min())
        w, h = int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)
        elem_list.append({
            "id": f"e{idx}_{name[:10].strip().replace(' ', '_').lower()}",
            "type": el_type,
            "label": name,
            "region": {"x": x0, "y": y0, "width": w, "height": h},
            "reveal": {"startMs": start_ms, "durationMs": dur_ms, "direction": direction},
            "colorMode": color_mode
        })
        idx += 1

    ann = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": duration_ms,
        "elements": elem_list
    }
    
    out_ann = proj_dir / "images/scene_01.annotation.json"
    out_ann.write_text(json.dumps(ann, indent=2, ensure_ascii=False), encoding="utf-8")

    # Verify coverage
    covered = np.zeros_like(ink, dtype=bool)
    boxes = []
    for el in elem_list:
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        boxes.append((x, y, w, h))
        covered[y:y+h, x:x+w] |= ink[y:y+h, x:x+w]

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
                print(f"  Overlap: {elem_list[i]['label']} & {elem_list[j]['label']}")

    print(f"[{proj_name}] Coverage: {cov_pct:.3f}% ({covered_count}/{total_ink}) | Overlaps: {overlaps} | Elements: {len(elem_list)}")

if __name__ == "__main__":
    segment_project("WB-TEST-CASE-04", 20000, "two_cards")
    segment_project("WB-TEST-CASE-05", 20000, "two_cards")
    segment_project("WB-TEST-CASE-06", 24000, "three_cards")
