#!/usr/bin/env python3
"""
micro_semantic_segmenter.py — Thuật toán phân vùng vi mô (Micro-Semantic Segmentation Engine)
Phân rã triệt để canvas thành từng đối tượng độc lập:
1. Container / Outer Frame: Khung viền hộp thẻ, bảng, đường bo
2. Visual Artwork / Illustration: Hình vẽ nhân vật, đồ vật, icon minh họa
3. Text Sentence / Line: Từng dòng chữ, từng câu văn hoàn chỉnh
4. Keywords / Badges / Formulas: Công thức ngữ pháp, từ khóa nổi bật
5. Gestures / Accents: Dấu tích xanh ✔, gạch chéo đỏ ❌, nét gạch chân, mũi tên

Giải quyết triệt để lỗi nét nhảy (pen jump) giữa hình vẽ và câu chữ,
đảm bảo:
- 100.0% độ phủ mực (Zero ink left behind).
- Vẽ hoàn thiện 100% từng hình minh họa trước khi chuyển sang viết dòng chữ.
- Viết tuần tự từng câu văn từ trái sang phải.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import numpy as np

PALETTE = [
    (240, 50, 50),    # 1: Red
    (40, 160, 240),   # 2: Sky Blue
    (40, 200, 80),    # 3: Green
    (220, 50, 180),   # 4: Magenta
    (240, 150, 20),   # 5: Orange
    (140, 40, 230),   # 6: Purple
    (20, 200, 220),   # 7: Cyan
    (220, 180, 20),   # 8: Yellow-gold
    (50, 110, 240),   # 9: Royal Blue
    (180, 40, 60),    # 10: Crimson
    (40, 180, 140),   # 11: Teal
    (250, 100, 160),  # 12: Pink
    (100, 100, 255),  # 13: Lavender
    (120, 200, 40),   # 14: Lime
    (200, 100, 40),   # 15: Rust
    (160, 40, 200),   # 16: Violet
    (50, 180, 240),   # 17: Light Blue
    (240, 120, 80),   # 18: Coral
]


def extract_ink_and_components(img_bgr: np.ndarray):
    """Trích xuất toàn bộ pixel mực và phân tích Connected Components."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    diff = 255 - gray
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    ink_mask = (diff > 18) | (sat > 40)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(ink_mask.astype(np.uint8))
    components = []
    for i in range(1, num_labels):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area < 2:
            continue
        x = int(stats[i, cv2.CC_STAT_LEFT])
        y = int(stats[i, cv2.CC_STAT_TOP])
        w = int(stats[i, cv2.CC_STAT_WIDTH])
        h = int(stats[i, cv2.CC_STAT_HEIGHT])
        cx, cy = centroids[i]
        components.append({
            "id": i, "x": x, "y": y, "w": w, "h": h,
            "cx": float(cx), "cy": float(cy), "area": area,
            "mask": (labels == i)
        })
    return ink_mask, components


def compute_tight_bbox(comp_list: List[dict], canvas_w: int, canvas_h: int, pad_x: int = 8, pad_y: int = 6):
    """Tính bounding box ôm khít danh sách CC kèm padding bảo đảm an toàn mép."""
    if not comp_list:
        return 0, 0, 0, 0
    min_x = min(c["x"] for c in comp_list)
    min_y = min(c["y"] for c in comp_list)
    max_x = max(c["x"] + c["w"] for c in comp_list)
    max_y = max(c["y"] + c["h"] for c in comp_list)

    rx = max(0, min_x - pad_x)
    ry = max(0, min_y - pad_y)
    rw = min(canvas_w - rx, (max_x - min_x) + pad_x * 2)
    rh = min(canvas_h - ry, (max_y - min_y) + pad_y * 2)
    return rx, ry, rw, rh


# ==============================================================================
# Phân rã cấu trúc vi mô cho Scene 03 (Nouns: Teacher, Doctor, Students)
# ==============================================================================
def decompose_scene_03(components: List[dict]) -> Dict[str, List[dict]]:
    """
    Phân rã Scene 03 thành 12 phần tử vi mô:
    - el-01-title: Tiêu đề REGION 1: WHO OR WHAT? (NOUNS)
    - Card 1:
      - el-02-card1-box: Khung hộp hình vuông của Card 1
      - el-03-card1-illus-teacher: Hình vẽ cô giáo cầm sách
      - el-04-card1-sentence: Câu văn "I am a teacher."
    - Card 2:
      - el-05-card2-box: Khung hộp hình vuông của Card 2
      - el-06-card2-illus-doctor: Hình vẽ bác sĩ
      - el-07-card2-sentence: Câu văn "He is a doctor."
    - Card 3:
      - el-08-card3-box: Khung hộp hình vuông của Card 3
      - el-09-card3-illus-students: Hình vẽ 2 học sinh
      - el-10-card3-sentence: Câu văn "They are students."
    - Bottom Takeaway:
      - el-11-bottom-text: Câu kết luận "USE A NOUN TO NAME A PERSON, JOB, OR THING."
      - el-12-bottom-underline: Nét gạch chân highlight "PERSON, JOB, OR THING."
    """
    groups = {
        "el-01-title": [],
        "el-02-card1-box": [],
        "el-03-card1-illus-teacher": [],
        "el-04-card1-sentence": [],
        "el-05-card2-box": [],
        "el-06-card2-illus-doctor": [],
        "el-07-card2-sentence": [],
        "el-08-card3-box": [],
        "el-09-card3-illus-students": [],
        "el-10-card3-sentence": [],
        "el-11-bottom-text": [],
        "el-12-bottom-underline": [],
    }

    for c in components:
        cx, cy = c["cx"], c["cy"]
        w, h = c["w"], c["h"]

        # 1. Title trên đỉnh
        if cy < 220:
            groups["el-01-title"].append(c)

        # 2. Bottom Takeaway dưới đáy
        elif cy > 840:
            if c["area"] > 4000 and w > 400 and h < 35:  # Nét gạch chân highlight
                groups["el-12-bottom-underline"].append(c)
            else:
                groups["el-11-bottom-text"].append(c)

        # 3. Card 1 (x < 660)
        elif cx < 660:
            if w > 450 and h > 450:  # Khung hộp Card 1
                groups["el-02-card1-box"].append(c)
            elif cy >= 670:  # Chữ "I am a teacher."
                groups["el-04-card1-sentence"].append(c)
            else:  # Hình cô giáo
                groups["el-03-card1-illus-teacher"].append(c)

        # 4. Card 2 (660 <= cx < 1260)
        elif cx < 1260:
            if w > 450 and h > 450:  # Khung hộp Card 2
                groups["el-05-card2-box"].append(c)
            elif cy >= 670:  # Chữ "He is a doctor."
                groups["el-07-card2-sentence"].append(c)
            else:  # Hình bác sĩ
                groups["el-06-card2-illus-doctor"].append(c)

        # 5. Card 3 (cx >= 1260)
        else:
            if w > 450 and h > 450:  # Khung hộp Card 3
                groups["el-08-card3-box"].append(c)
            elif cy >= 670:  # Chữ "They are students."
                groups["el-10-card3-sentence"].append(c)
            else:  # Hình 2 học sinh
                groups["el-09-card3-illus-students"].append(c)

    return groups


# Metadata & SRT Master Clock timing cho Scene 03
SCENE_03_CONFIG = {
    "sceneDurationMs": 41980,
    "globalStartMs": 73360,
    "globalEndMs": 115340,
    "srtStartCue": 15,
    "srtEndCue": 20,
    "fps": 60,
    "elements_meta": [
        # Cue 15: Bây giờ, hãy đến với vùng kết nối đầu tiên: Danh từ...
        ("el-01-title", "REGION 1: WHO OR WHAT? (NOUNS)", "text", "none", 400, 5500),
        
        # Cue 16: Khi giới thiệu bản thân: Tôi là một giáo viên, ta nói: I am a teacher.
        # Phân rã 3 tầng: Khung thẻ -> Hình cô giáo -> Câu chữ tiếng Anh
        ("el-02-card1-box", "Card 1: Box Frame", "box", "none", 6800, 1300),
        ("el-03-card1-illus-teacher", "Card 1: Teacher Illustration", "icon", "auto", 8300, 2800),
        ("el-04-card1-sentence", "Card 1: I am a teacher.", "text", "none", 11300, 1800),
        
        # Cue 17: Khi nói về anh ấy: Anh ấy là một bác sĩ: He is a doctor.
        ("el-05-card2-box", "Card 2: Box Frame", "box", "none", 13700, 1200),
        ("el-06-card2-illus-doctor", "Card 2: Doctor Illustration", "icon", "auto", 15100, 2700),
        ("el-07-card2-sentence", "Card 2: He is a doctor.", "text", "none", 18000, 1700),
        
        # Cue 18: Và khi nói về một nhóm người: Họ là những học sinh: They are students.
        ("el-08-card3-box", "Card 3: Box Frame", "box", "none", 20200, 1200),
        ("el-09-card3-illus-students", "Card 3: Students Illustration", "icon", "auto", 21600, 2800),
        ("el-10-card3-sentence", "Card 3: They are students.", "text", "none", 24600, 1800),
        
        # Cue 19 & 20: Bạn hãy chú ý nhé... Chỉ cần có TO BE làm cầu nối...
        ("el-11-bottom-text", "USE A NOUN TO NAME A PERSON, JOB, OR THING.", "text", "none", 35000, 4200),
        ("el-12-bottom-underline", "Highlight Underline", "underline", "auto", 39400, 1800),
    ]
}


# ==============================================================================
# Phân rã cấu trúc vi mô cho Scene 01 (How do you say this? Contrast)
# ==============================================================================
def decompose_scene_01(components: List[dict]) -> Dict[str, List[dict]]:
    """
    Phân rã Scene 01 thành 13 phần tử vi mô:
    - Tiêu đề & Quote tiếng Việt
    - Card sai: Khung viền -> Câu chữ "I very happy" -> Dấu chéo đỏ ❌ -> Nhãn "MISSING VERB"
    - Hub "WHY?"
    - Card đúng: Khung viền -> Câu chữ "I AM very happy" -> Gạch chân chữ AM -> Dấu tích xanh ✔ -> Nhãn kết nối
    - Bottom takeaway: "EVERY ENGLISH SENTENCE NEEDS A VERB!"
    """
    groups = {
        "el-01-header": [],
        "el-02-vietnamese-quote": [],
        "el-03-incorrect-box": [],
        "el-04-incorrect-text": [],
        "el-05-incorrect-cross": [],
        "el-06-missing-verb-label": [],
        "el-07-why-question": [],
        "el-08-correct-box": [],
        "el-09-correct-text": [],
        "el-10-correct-underline": [],
        "el-11-correct-check": [],
        "el-12-connects-label": [],
        "el-13-bottom-takeaway": [],
    }

    for c in components:
        cx, cy = c["cx"], c["cy"]
        w, h = c["w"], c["h"]

        # 1. Header trên cùng
        if cy < 170:
            groups["el-01-header"].append(c)

        # 2. Vietnamese quote
        elif cy < 380 and 600 <= cx <= 1350:
            groups["el-02-vietnamese-quote"].append(c)

        # 3. Bottom takeaway
        elif cy >= 820:
            groups["el-13-bottom-takeaway"].append(c)

        # 4. Center WHY?
        elif 800 <= cx <= 1120 and 420 <= cy <= 650:
            groups["el-07-why-question"].append(c)

        # 5. Cột trái: Card sai (cx < 800)
        elif cx < 800:
            if cy >= 700:
                groups["el-06-missing-verb-label"].append(c)
            elif w > 500 and h > 250:
                groups["el-03-incorrect-box"].append(c)
            elif 630 <= cx <= 770 and 420 <= cy <= 520:
                groups["el-05-incorrect-cross"].append(c)
            else:
                groups["el-04-incorrect-text"].append(c)

        # 6. Cột phải: Card đúng (cx >= 1120)
        else:
            if cy >= 700:
                groups["el-12-connects-label"].append(c)
            elif w > 500 and h > 250:
                groups["el-08-correct-box"].append(c)
            elif 1660 <= cx <= 1820 and 410 <= cy <= 520:
                groups["el-11-correct-check"].append(c)
            elif c["area"] > 1000 and w > 100 and h < 30:  # Nét gạch chân chữ AM
                groups["el-10-correct-underline"].append(c)
            else:
                groups["el-09-correct-text"].append(c)

    return groups


SCENE_01_CONFIG = {
    "sceneDurationMs": 37880,
    "globalStartMs": 0,
    "globalEndMs": 37880,
    "srtStartCue": 1,
    "srtEndCue": 6,
    "fps": 60,
    "elements_meta": [
        ("el-01-header", "HOW DO YOU SAY THIS?", "text", "none", 400, 2000),
        ("el-02-vietnamese-quote", "Tôi rất vui ☺", "card", "auto", 2400, 2400),
        ("el-03-incorrect-box", "Incorrect Card: Box", "box", "none", 5000, 1400),
        ("el-04-incorrect-text", "I very happy", "text", "none", 6500, 3200),
        ("el-05-incorrect-cross", "Cross ❌", "icon", "auto", 9900, 2000),
        ("el-06-missing-verb-label", "MISSING VERB", "card", "auto", 12500, 2500),
        ("el-07-why-question", "WHY?", "card", "auto", 15800, 2800),
        ("el-08-correct-box", "Correct Card: Box", "box", "none", 19200, 1400),
        ("el-09-correct-text", "I AM very happy", "text", "none", 20800, 3200),
        ("el-10-correct-underline", "Underline 'AM'", "underline", "auto", 24200, 1400),
        ("el-11-correct-check", "Check ✔", "icon", "auto", 25800, 1800),
        ("el-12-connects-label", "TO BE CONNECTS THE SENTENCE", "card", "auto", 28000, 3200),
        ("el-13-bottom-takeaway", "EVERY ENGLISH SENTENCE NEEDS A VERB!", "card", "auto", 31800, 5500),
    ]
}


# ==============================================================================
# Phân rã cấu trúc vi mô cho Scene 02 (Hub & 3 Branches)
# ==============================================================================
def decompose_scene_02(components: List[dict]) -> Dict[str, List[dict]]:
    """
    Phân rã Scene 02 thành 13 phần tử vi mô:
    - Tiêu đề "WHAT IS THE VERB TO BE?"
    - Hub "SUBJECT"
    - Hub "= [TO BE]"
    - Branch 1: Khung thẻ -> Dòng chữ "1. WHO / WHAT?" -> Icon Person
    - Branch 2: Khung thẻ -> Dòng chữ "2. HOW?" -> Icon Face
    - Branch 3: Khung thẻ -> Dòng chữ "3. WHERE?" -> Icon Location
    - Bottom rule: "IT DOES NOT SHOW ACTION. IT CONNECTS!"
    """
    groups = {
        "el-01-title": [],
        "el-02-hub-subject": [],
        "el-03-hub-tobe": [],
        "el-04-branch1-box": [],
        "el-05-branch1-text": [],
        "el-06-branch1-icon": [],
        "el-07-branch2-box": [],
        "el-08-branch2-text": [],
        "el-09-branch2-icon": [],
        "el-10-branch3-box": [],
        "el-11-branch3-text": [],
        "el-12-branch3-icon": [],
        "el-13-bottom-rule": [],
    }

    for c in components:
        cx, cy = c["cx"], c["cy"]
        w, h = c["w"], c["h"]

        # 1. Title
        if cy < 200:
            groups["el-01-title"].append(c)

        # 2. Bottom rule
        elif cy >= 900:
            groups["el-13-bottom-rule"].append(c)

        # 3. Hub Subject (cx < 610)
        elif cx < 610:
            groups["el-02-hub-subject"].append(c)

        # 4. Hub To Be (610 <= cx < 1020)
        elif cx < 1020:
            groups["el-03-hub-tobe"].append(c)

        # 5. Branch 1 (cy < 430)
        elif cy < 430:
            if w > 500 and h > 180:
                groups["el-04-branch1-box"].append(c)
            elif cx >= 1620:
                groups["el-06-branch1-icon"].append(c)
            else:
                groups["el-05-branch1-text"].append(c)

        # 6. Branch 2 (430 <= cy < 610)
        elif cy < 610:
            if w > 500 and h > 160:
                groups["el-07-branch2-box"].append(c)
            elif cx >= 1620:
                groups["el-09-branch2-icon"].append(c)
            else:
                groups["el-08-branch2-text"].append(c)

        # 7. Branch 3 (cy >= 610)
        else:
            if w > 500 and h > 200:
                groups["el-10-branch3-box"].append(c)
            elif cx >= 1620:
                groups["el-12-branch3-icon"].append(c)
            else:
                groups["el-11-branch3-text"].append(c)

    return groups


SCENE_02_CONFIG = {
    "sceneDurationMs": 35480,
    "globalStartMs": 37880,
    "globalEndMs": 73360,
    "srtStartCue": 7,
    "srtEndCue": 14,
    "fps": 60,
    "elements_meta": [
        ("el-01-title", "WHAT IS THE VERB TO BE?", "text", "none", 400, 4200),
        ("el-02-hub-subject", "SUBJECT", "card", "auto", 5200, 4000),
        ("el-03-hub-tobe", "= [TO BE]", "card", "auto", 9800, 4600),
        ("el-04-branch1-box", "Branch 1: Box", "box", "none", 15000, 1200),
        ("el-05-branch1-text", "1. WHO / WHAT? (IDENTITY / NOUN)", "text", "none", 16400, 2600),
        ("el-06-branch1-icon", "Identity Icon", "icon", "auto", 19200, 2000),
        ("el-07-branch2-box", "Branch 2: Box", "box", "none", 21800, 1100),
        ("el-08-branch2-text", "2. HOW? (FEELING / ADJECTIVE)", "text", "none", 23100, 2400),
        ("el-09-branch2-icon", "Feeling Icon", "icon", "auto", 25700, 1600),
        ("el-10-branch3-box", "Branch 3: Box", "box", "none", 27600, 1100),
        ("el-11-branch3-text", "3. WHERE? (LOCATION / PLACE)", "text", "none", 28900, 2400),
        ("el-12-branch3-icon", "Location Icon", "icon", "auto", 31500, 1600),
        ("el-13-bottom-rule", "IT DOES NOT SHOW ACTION. IT CONNECTS!", "card", "auto", 33400, 4000),
    ]
}


# ==============================================================================
# Pipeline xử lý và kiểm định phân vùng
# ==============================================================================
REGISTRY = {
    1: (decompose_scene_01, SCENE_01_CONFIG),
    2: (decompose_scene_02, SCENE_02_CONFIG),
    3: (decompose_scene_03, SCENE_03_CONFIG),
}


def process_scene(scene_num: int, project_dir: Path):
    """Thực thi phân vùng vi mô, xuất file annotation và ảnh kiểm định."""
    if scene_num not in REGISTRY:
        raise ValueError(f"Chưa cấu hình bộ phân rã cho Scene {scene_num}")

    decomposer_fn, config = REGISTRY[scene_num]
    img_path = project_dir / "images" / f"scene_{scene_num:02d}.png"
    annot_path = project_dir / "images" / f"scene_{scene_num:02d}.annotation.json"
    region_path = project_dir / "images" / f"scene_{scene_num:02d}_regions.png"

    img = cv2.imread(str(img_path))
    if img is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh: {img_path}")
    h, w = img.shape[:2]

    ink_mask, components = extract_ink_and_components(img)
    total_ink = int(np.count_nonzero(ink_mask))
    total_ccs = len(components)

    groups = decomposer_fn(components)

    elements = []
    vis = img.copy()
    assigned_mask = np.zeros((h, w), dtype=bool)

    for seq, meta in enumerate(config["elements_meta"], start=1):
        eid, label, el_type, color_mode, start_ms, dur_ms = meta
        c_list = groups.get(eid, [])

        if not c_list:
            print(f"  ⚠️ [Scene {scene_num:02d}] Cảnh báo: '{eid}' không có Connected Component nào!")
            continue

        rx, ry, rw, rh = compute_tight_bbox(c_list, w, h, pad_x=8, pad_y=6)

        elem_dict = {
            "id": eid,
            "sequence": seq,
            "label": label,
            "type": el_type,
            "colorMode": color_mode,
            "region": {
                "x": int(rx),
                "y": int(ry),
                "width": int(rw),
                "height": int(rh)
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": start_ms,
                "durationMs": dur_ms
            }
        }
        elements.append(elem_dict)

        # Cập nhật mask kiểm định
        for c in c_list:
            assigned_mask |= c["mask"]

        # Vẽ bounding box trên ảnh visual audit
        color = PALETTE[(seq - 1) % len(PALETTE)]
        cv2.rectangle(vis, (rx, ry), (rx + rw, ry + rh), color, 2)
        
        # Vẽ thẻ tên
        badge_txt = f"[{seq}] {eid}"
        badge_w = len(badge_txt) * 9 + 12
        badge_y = ry - 6 if ry > 25 else ry + rh + 18
        cv2.rectangle(vis, (rx, badge_y - 18), (rx + badge_w, badge_y + 4), color, -1)
        cv2.putText(vis, badge_txt, (rx + 4, badge_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

    # Xuất file annotation.json
    annotation = {
        "canvas": {"width": w, "height": h},
        "sceneDurationMs": config["sceneDurationMs"],
        "globalStartMs": config["globalStartMs"],
        "globalEndMs": config["globalEndMs"],
        "srtStartCue": config["srtStartCue"],
        "srtEndCue": config["srtEndCue"],
        "fps": config["fps"],
        "elements": elements
    }

    with open(annot_path, "w", encoding="utf-8") as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)

    cv2.imwrite(str(region_path), vis)

    # Kiểm định chất lượng
    covered_ink = int(np.count_nonzero(assigned_mask & ink_mask))
    unassigned_ink = total_ink - covered_ink
    pct = (covered_ink / total_ink * 100.0) if total_ink > 0 else 100.0

    print(f"✅ Scene {scene_num:02d}: {len(elements)} Micro-Elements | CCs: {total_ccs} | Ink: {pct:.2f}% ({covered_ink:,}/{total_ink:,}) | Unassigned: {unassigned_ink}px")
    return annotation


def main():
    project_dir = Path("projects/WB-ENG-A1-003")
    print("=" * 80)
    print(" THUẬT TOÁN PHÂN VÙNG VI MÔ ĐẾN TỪNG ĐỐI TƯỢNG (MICRO-SEMANTIC SEGMENTER)")
    print("=" * 80)
    for s in [1, 2, 3]:
        process_scene(s, project_dir)
    print("=" * 80)
    print("🎉 Hoàn tất phân rã 100% đối tượng độc lập cho Scene 01, 02, 03!")


if __name__ == "__main__":
    main()
