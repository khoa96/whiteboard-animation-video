#!/usr/bin/env python3
import json
from pathlib import Path
import cv2
import numpy as np

def inspect_scene_ink(s_num: int):
    root = Path("projects/WB-ENG-A1-003")
    img_path = root / "images" / f"scene_{s_num:02d}.png"
    annot_path = root / "images" / f"scene_{s_num:02d}.annotation.json"
    
    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    diff = 255 - gray
    ink_mask = (diff > 18) | (sat > 40)
    
    with open(annot_path, "r", encoding="utf-8") as f:
        annot = json.load(f)
        
    coverage = np.zeros((h, w), dtype=bool)
    for el in annot["elements"]:
        r = el["region"]
        x, y, rw, rh = r["x"], r["y"], r["width"], r["height"]
        coverage[y:y+rh, x:x+rw] = True
        
    missing = ink_mask & (~coverage)
    n_missing = np.count_nonzero(missing)
    total = np.count_nonzero(ink_mask)
    pct = (total - n_missing) / total * 100
    
    print(f"Scene {s_num:02d}: Đã phủ {pct:.2f}% | Thiếu: {n_missing} px")
    
    # Tìm các CC bị thiếu
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(missing.astype(np.uint8))
    for i in range(1, min(10, num_labels)):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > 10:
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w_c = stats[i, cv2.CC_STAT_WIDTH]
            h_c = stats[i, cv2.CC_STAT_HEIGHT]
            print(f"   Missing CC #{i}: area={area} at (x={x}, y={y}, w={w_c}, h={h_c})")

for s in range(4, 10):
    inspect_scene_ink(s)
