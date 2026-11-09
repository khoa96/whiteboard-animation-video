#!/usr/bin/env python3
"""
measure_and_build_semantic_annotations.py — Tái cấu trúc phân vùng vi mô chuẩn ngữ nghĩa
cho toàn bộ Scene 04 -> Scene 09 của WB-ENG-A1-003.

Nguyên tắc bắt buộc:
1. 0% ký tự hoặc icon bị đường biên cắt ngang.
2. Tách bạch Câu hỏi (Prompt) và Đáp án (Reveal Answer) cho các cảnh thực hành (Scene 8, 9).
3. Tách từng tầng nội dung (Header, Item 1, Item 2) thay vì gom cả cột lớn (Scene 4, 5, 7).
4. Phủ 99-100% mực, 0px overlap giữa các khối.
5. Timing khớp 100% theo từng Cue SRT.
"""

import json
from pathlib import Path
import cv2
import numpy as np

PALETTE = [
    (230, 40, 40), (40, 160, 230), (40, 200, 40), (200, 40, 180),
    (180, 120, 40), (140, 40, 220), (220, 140, 20), (20, 180, 220),
    (40, 180, 100), (180, 40, 40), (0, 140, 255), (100, 100, 255),
    (255, 100, 50), (50, 100, 255), (160, 60, 200)
]

NEW_SCENE_DEFS = {
    4: {
        "title": "REGIONS 2 & 3: FEELINGS & LOCATIONS",
        "sceneDurationMs": 38480,
        "globalStartMs": 115340,
        "globalEndMs": 153820,
        "srtStartCue": 21,
        "srtEndCue": 27,
        "elements": [
            # Cue 21: Tiếp theo là vùng số hai và vùng số ba...
            {"id": "el-01-title", "sequence": 1, "label": "REGIONS 2 & 3: FEELINGS & LOCATIONS", "type": "text", "colorMode": "none",
             "region": {"x": 100, "y": 30, "width": 1720, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 3800}},
            # Cue 21-22: Vùng 2: Cảm xúc
            {"id": "el-02-col1-header", "sequence": 2, "label": "FEELINGS (HOW?)", "type": "text", "colorMode": "none",
             "region": {"x": 60, "y": 190, "width": 800, "height": 100},
             "reveal": {"direction": "left_to_right", "startMs": 4400, "durationMs": 2000}},
            # Cue 22: Cô ấy rất vui: She is happy.
            {"id": "el-03-col1-item1", "sequence": 3, "label": "☺ She is happy.", "type": "card", "colorMode": "auto",
             "region": {"x": 60, "y": 310, "width": 800, "height": 200},
             "reveal": {"direction": "left_to_right", "startMs": 6600, "durationMs": 4200}},
            # Cue 23: Chúng tôi đang mệt: We are tired.
            {"id": "el-04-col1-item2", "sequence": 4, "label": "☹ We are tired.", "type": "card", "colorMode": "auto",
             "region": {"x": 60, "y": 540, "width": 800, "height": 210},
             "reveal": {"direction": "left_to_right", "startMs": 11000, "durationMs": 3800}},
            # Cue 25: Tương tự với nơi chốn...
            {"id": "el-05-col2-header", "sequence": 5, "label": "LOCATIONS (WHERE?)", "type": "text", "colorMode": "none",
             "region": {"x": 940, "y": 190, "width": 900, "height": 100},
             "reveal": {"direction": "left_to_right", "startMs": 23300, "durationMs": 2200}},
            # Cue 25: Tôi đang ở nhà: I am at home.
            {"id": "el-06-col2-item1", "sequence": 6, "label": "🏠 I am at home.", "type": "card", "colorMode": "auto",
             "region": {"x": 940, "y": 310, "width": 900, "height": 200},
             "reveal": {"direction": "left_to_right", "startMs": 25700, "durationMs": 2300}},
            # Cue 26: Họ đang ở trường: They are at school.
            {"id": "el-07-col2-item2", "sequence": 7, "label": "🏫 They are at school.", "type": "card", "colorMode": "auto",
             "region": {"x": 940, "y": 530, "width": 900, "height": 230},
             "reveal": {"direction": "left_to_right", "startMs": 28200, "durationMs": 3800}},
            # Cue 27: Không cần động từ hành động phức tạp...
            {"id": "el-08-bottom-takeaway", "sequence": 8, "label": "NO ACTION VERB NEEDED — TO BE DOES IT ALL!", "type": "box", "colorMode": "none",
             "region": {"x": 80, "y": 810, "width": 1760, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 32400, "durationMs": 5600}}
        ]
    },
    5: {
        "title": "THE 3 FORMS: AM — IS — ARE",
        "sceneDurationMs": 51600,
        "globalStartMs": 154320,
        "globalEndMs": 205920,
        "srtStartCue": 28,
        "srtEndCue": 34,
        "elements": [
            # Cue 28: Ở thì hiện tại, cỗ máy TO BE chia thành ba nhánh...
            {"id": "el-01-title", "sequence": 1, "label": "THE 3 FORMS: AM — IS — ARE", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 30, "width": 1620, "height": 150},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 5500}},
            # Cue 29: Khung viền 3 thẻ (Card outlines)
            {"id": "el-02-cards-outline", "sequence": 2, "label": "Outline of 3 Cards", "type": "box", "colorMode": "none",
             "region": {"x": 40, "y": 280, "width": 1840, "height": 550},
             "reveal": {"direction": "left_to_right", "startMs": 6600, "durationMs": 4800}},
            # Cue 30: Nhánh 1: AM đi riêng với I...
            {"id": "el-03-am-badge", "sequence": 3, "label": "Badge: AM (FOR 'I' ONLY)", "type": "card", "colorMode": "wash",
             "region": {"x": 70, "y": 240, "width": 560, "height": 125},
             "reveal": {"direction": "left_to_right", "startMs": 12100, "durationMs": 2200}},
            {"id": "el-04-am-body", "sequence": 4, "label": "I + AM | I am ready.", "type": "text", "colorMode": "none",
             "region": {"x": 70, "y": 420, "width": 560, "height": 380},
             "reveal": {"direction": "left_to_right", "startMs": 14500, "durationMs": 3500}},
            # Cue 31-32: Nhánh 2: IS dành cho số ít, mẹo chữ S...
            {"id": "el-05-is-badge", "sequence": 5, "label": "Badge: IS (SINGULAR = 1)", "type": "card", "colorMode": "wash",
             "region": {"x": 670, "y": 240, "width": 600, "height": 125},
             "reveal": {"direction": "left_to_right", "startMs": 18600, "durationMs": 2500}},
            {"id": "el-06-is-rule-s", "sequence": 6, "label": "S = SINGLE / ONE", "type": "text", "colorMode": "auto",
             "region": {"x": 670, "y": 380, "width": 600, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 21300, "durationMs": 4500}},
            {"id": "el-07-is-body", "sequence": 7, "label": "HE / SHE / IT | The cat | He is tall.", "type": "text", "colorMode": "none",
             "region": {"x": 670, "y": 525, "width": 600, "height": 280},
             "reveal": {"direction": "left_to_right", "startMs": 26000, "durationMs": 11000}},
            # Cue 33: Nhánh 3: ARE dành cho số nhiều...
            {"id": "el-08-are-badge", "sequence": 8, "label": "Badge: ARE (PLURAL = 2+ & YOU)", "type": "card", "colorMode": "wash",
             "region": {"x": 1300, "y": 240, "width": 560, "height": 160},
             "reveal": {"direction": "left_to_right", "startMs": 37600, "durationMs": 2800}},
            {"id": "el-09-are-body", "sequence": 9, "label": "YOU / WE / THEY | Cats | We are ready.", "type": "text", "colorMode": "none",
             "region": {"x": 1300, "y": 440, "width": 560, "height": 360},
             "reveal": {"direction": "left_to_right", "startMs": 40600, "durationMs": 6800}},
            # Cue 34: Nhớ mẹo chữ S cho số ít...
            {"id": "el-10-bottom-tip", "sequence": 10, "label": "REMEMBER: 'IS' HAS AN 'S' FOR SINGULAR!", "type": "box", "colorMode": "none",
             "region": {"x": 80, "y": 850, "width": 1760, "height": 170},
             "reveal": {"direction": "left_to_right", "startMs": 48000, "durationMs": 3400}}
        ]
    },
    6: {
        "title": "SHORT FORMS (CONTRACTIONS)",
        "sceneDurationMs": 44760,
        "globalStartMs": 206420,
        "globalEndMs": 251180,
        "srtStartCue": 35,
        "srtEndCue": 41,
        "elements": [
            # Cue 35: Trong giao tiếp hàng ngày... Contractions
            {"id": "el-01-title", "sequence": 1, "label": "SHORT FORMS (CONTRACTIONS)", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 30, "width": 1620, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 6800}},
            # Cue 36-37: Chiếc kéo thần kỳ cắt chữ i và nháy đơn...
            {"id": "el-02-magic-scissors", "sequence": 2, "label": "✂️ Scissors cut 'i' + Apostrophe '", "type": "icon", "colorMode": "auto",
             "region": {"x": 810, "y": 155, "width": 310, "height": 185},
             "reveal": {"direction": "left_to_right", "startMs": 8000, "durationMs": 7500}},
            # Cue 38: I am được rút gọn thành: I'm...
            {"id": "el-03-row1-full", "sequence": 3, "label": "Row 1: I am -> I'm [/aim/]", "type": "card", "colorMode": "auto",
             "region": {"x": 80, "y": 235, "width": 1760, "height": 125},
             "reveal": {"direction": "left_to_right", "startMs": 16200, "durationMs": 7000}},
            # Cue 39: He is -> He's. She is -> She's. Nhớ âm gió /z/...
            {"id": "el-04-row2-left", "sequence": 4, "label": "Row 2: He is -> He's | She is -> She's", "type": "card", "colorMode": "auto",
             "region": {"x": 80, "y": 380, "width": 1360, "height": 220},
             "reveal": {"direction": "left_to_right", "startMs": 23700, "durationMs": 6000}},
            # Bong bóng thoại /z/ sound cô lập tuyệt đối, không bị chia cắt!
            {"id": "el-05-row2-z-badge", "sequence": 5, "label": "Bong bóng thoại: [/z/ sound]", "type": "card", "colorMode": "auto",
             "region": {"x": 1450, "y": 420, "width": 390, "height": 140},
             "reveal": {"direction": "left_to_right", "startMs": 30000, "durationMs": 3300}},
            # Cue 40: They are -> They're. We are -> We're.
            {"id": "el-06-row3", "sequence": 6, "label": "Row 3: They are -> They're | We are -> We're", "type": "card", "colorMode": "auto",
             "region": {"x": 80, "y": 615, "width": 1760, "height": 220},
             "reveal": {"direction": "left_to_right", "startMs": 33800, "durationMs": 5600}},
            # Cue 41: Nói dạng rút gọn sẽ giúp câu nói tự nhiên...
            {"id": "el-07-footer", "sequence": 7, "label": "NATIVE SPEAKERS USE SHORT FORMS IN DAILY SPEECH!", "type": "box", "colorMode": "none",
             "region": {"x": 80, "y": 855, "width": 1760, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 39900, "durationMs": 4500}}
        ]
    },
    7: {
        "title": "COMMON MISTAKES TO AVOID",
        "sceneDurationMs": 37480,
        "globalStartMs": 251680,
        "globalEndMs": 289160,
        "srtStartCue": 42,
        "srtEndCue": 48,
        "elements": [
            # Cue 42: Trước khi luyện tập, hãy cùng ghé trạm bắt bệnh...
            {"id": "el-01-title", "sequence": 1, "label": "COMMON MISTAKES TO AVOID", "type": "text", "colorMode": "none",
             "region": {"x": 150, "y": 30, "width": 1620, "height": 120},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 3800}},
            # Cue 42-43: Hai tiêu đề cột DON'T SAY vs SAY THIS
            {"id": "el-02-col-headers", "sequence": 2, "label": "DON'T SAY ❌  vs  SAY THIS ✔️", "type": "box", "colorMode": "none",
             "region": {"x": 150, "y": 170, "width": 1620, "height": 110},
             "reveal": {"direction": "left_to_right", "startMs": 4400, "durationMs": 3000}},
            # Cue 43: Lỗi thứ nhất: Bệnh bỏ quên TO BE...
            {"id": "el-03-error1-header", "sequence": 3, "label": "MISSING TO BE (FEELING/STATE)", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 285, "width": 1520, "height": 85},
             "reveal": {"direction": "left_to_right", "startMs": 7600, "durationMs": 2800}},
            # Cue 44: Người Việt hay nói I tired... phải nói là I am tired...
            {"id": "el-04-error1-pair", "sequence": 4, "label": "I tired. ❌ (Missing am)  vs  I am tired. ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 375, "width": 1760, "height": 150},
             "reveal": {"direction": "left_to_right", "startMs": 10600, "durationMs": 8500}},
            # Cue 45: Lỗi thứ hai: Bệnh thừa TO BE...
            {"id": "el-05-error2-header", "sequence": 5, "label": "EXTRA TO BE (WITH ACTION VERBS)", "type": "text", "colorMode": "none",
             "region": {"x": 200, "y": 525, "width": 1520, "height": 85},
             "reveal": {"direction": "left_to_right", "startMs": 19400, "durationMs": 2800}},
            # Cue 46-47: I am go to school ❌ ... nói đơn giản I go to school ✔️
            {"id": "el-06-error2-pair", "sequence": 6, "label": "I am go to school. ❌ (Do not mix with go)  vs  I go to school. ✔️", "type": "box", "colorMode": "auto",
             "region": {"x": 80, "y": 615, "width": 1760, "height": 155},
             "reveal": {"direction": "left_to_right", "startMs": 22400, "durationMs": 8300}},
            # Cue 48: Quy tắc vàng: TO BE đi với tính từ và danh từ...
            {"id": "el-07-footer-card", "sequence": 7, "label": "TO BE = ADJECTIVES & NOUNS (NOT WITH SIMPLE ACTION VERBS!)", "type": "box", "colorMode": "none",
             "region": {"x": 240, "y": 780, "width": 1440, "height": 180},
             "reveal": {"direction": "left_to_right", "startMs": 31200, "durationMs": 5800}}
        ]
    },
    8: {
        "title": "PRACTICE: CHOOSE AM / IS / ARE (PART 1)",
        "sceneDurationMs": 32120,
        "globalStartMs": 289660,
        "globalEndMs": 321780,
        "srtStartCue": 49,
        "srtEndCue": 53,
        "elements": [
            # Cue 49: Bây giờ đến lượt bạn. Hãy chọn AM, IS hay ARE...
            {"id": "el-01-title", "sequence": 1, "label": "PRACTICE: CHOOSE AM / IS / ARE", "type": "text", "colorMode": "none",
             "region": {"x": 100, "y": 30, "width": 1720, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 4500}},
            # Cue 50: Câu số một: I ___ a student. Bạn có 3 giây suy nghĩ...
            {"id": "el-02-q1-prompt", "sequence": 2, "label": "Q1: 1. I ______ a student. [AM] [IS] [ARE]", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 170, "width": 1720, "height": 360},
             "reveal": {"direction": "left_to_right", "startMs": 5400, "durationMs": 4600},
             "reveal_protected_regions": [{"x": 480, "y": 275, "width": 180, "height": 120}]},
            # Cue 51: Đáp án chính xác là AM: I am a student!
            {"id": "el-03-q1-answer", "sequence": 3, "label": "Dấu tích xanh ✔️ [AM]", "type": "icon", "colorMode": "auto",
             "region": {"x": 490, "y": 280, "width": 160, "height": 110},
             "reveal": {"direction": "left_to_right", "startMs": 10400, "durationMs": 4000}},
            # Cue 52: Câu số hai: She ___ very happy. AM, IS hay ARE?
            {"id": "el-04-q2-prompt", "sequence": 4, "label": "Q2: 2. She ______ very happy. [AM] [IS] [ARE]", "type": "box", "colorMode": "auto",
             "region": {"x": 100, "y": 540, "width": 1720, "height": 360},
             "reveal": {"direction": "left_to_right", "startMs": 17600, "durationMs": 5500},
             "reveal_protected_regions": [{"x": 900, "y": 655, "width": 180, "height": 120}]},
            # Cue 53: Đáp án là IS: She is very happy!
            {"id": "el-05-q2-answer", "sequence": 5, "label": "Dấu tích xanh ✔️ [IS]", "type": "icon", "colorMode": "auto",
             "region": {"x": 910, "y": 660, "width": 160, "height": 110},
             "reveal": {"direction": "left_to_right", "startMs": 23600, "durationMs": 4500}},
            # Dòng nhắc nhở chân trang
            {"id": "el-06-footer-reminder", "sequence": 6, "label": "3 SECONDS TO THINK BEFORE THE ANSWER!", "type": "text", "colorMode": "none",
             "region": {"x": 380, "y": 915, "width": 1160, "height": 80},
             "reveal": {"direction": "left_to_right", "startMs": 29000, "durationMs": 2800}}
        ]
    },
    9: {
        "title": "FINAL CHALLENGE & SUMMARY",
        "sceneDurationMs": 51880,
        "globalStartMs": 322280,
        "globalEndMs": 374160,
        "srtStartCue": 54,
        "srtEndCue": 62,
        "elements": [
            # Cue 54: Ba câu thử thách cuối cùng...
            {"id": "el-01-title", "sequence": 1, "label": "FINAL CHALLENGE & SUMMARY", "type": "text", "colorMode": "none",
             "region": {"x": 100, "y": 30, "width": 1720, "height": 120},
             "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 1800}},
            # Cue 55: Câu số ba: The cat ___ sleeping.
            {"id": "el-02-q3-prompt", "sequence": 2, "label": "3. The cat ______ sleeping.", "type": "text", "colorMode": "none",
             "region": {"x": 80, "y": 160, "width": 1280, "height": 125},
             "reveal": {"direction": "left_to_right", "startMs": 2400, "durationMs": 5300}},
            # Cue 56: Đáp án là IS: The cat is sleeping...
            {"id": "el-03-q3-answer", "sequence": 3, "label": "[ IS ] ✔️", "type": "card", "colorMode": "auto",
             "region": {"x": 1400, "y": 160, "width": 440, "height": 125},
             "reveal": {"direction": "left_to_right", "startMs": 8200, "durationMs": 4000}},
            # Cue 57: Câu số bốn: Tom and Mary ___ friends...
            {"id": "el-04-q4-prompt", "sequence": 4, "label": "4. Tom and Mary ______ friends.", "type": "text", "colorMode": "none",
             "region": {"x": 80, "y": 295, "width": 1280, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 14100, "durationMs": 5400}},
            # Cue 58: Đáp án là ARE: Tom and Mary are friends...
            {"id": "el-05-q4-answer", "sequence": 5, "label": "[ ARE ] ✔️", "type": "card", "colorMode": "auto",
             "region": {"x": 1400, "y": 295, "width": 440, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 19900, "durationMs": 4800}},
            # Cue 59: Câu số năm: We ___ at home...
            {"id": "el-06-q5-prompt", "sequence": 6, "label": "5. We ______ at home.", "type": "text", "colorMode": "none",
             "region": {"x": 80, "y": 435, "width": 1280, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 28100, "durationMs": 3000}},
            # Cue 60: Đáp án là ARE: We are at home.
            {"id": "el-07-q5-answer", "sequence": 7, "label": "[ ARE ] ✔️", "type": "card", "colorMode": "auto",
             "region": {"x": 1400, "y": 435, "width": 440, "height": 130},
             "reveal": {"direction": "left_to_right", "startMs": 31600, "durationMs": 3500}},
            # Cue 61: Hãy ghi nhớ: Bảng tổng kết Master Summary (Thẻ nền vàng)
            {"id": "el-08-summary-box", "sequence": 8, "label": "Khung thẻ: MASTER SUMMARY:", "type": "box", "colorMode": "wash",
             "region": {"x": 40, "y": 625, "width": 1840, "height": 315},
             "reveal": {"direction": "left_to_right", "startMs": 35700, "durationMs": 3000}},
            # 3 dòng quy tắc bên trong
            {"id": "el-09-summary-bullets", "sequence": 9, "label": "• I -> AM | • HE/SHE/IT -> IS | • YOU/WE/THEY -> ARE", "type": "text", "colorMode": "none",
             "region": {"x": 90, "y": 720, "width": 1700, "height": 210},
             "reveal": {"direction": "left_to_right", "startMs": 39000, "durationMs": 7200}},
            # Cue 62: Bài học tiếp theo... NEXT: NEGATIVE & QUESTIONS
            {"id": "el-10-next-teaser", "sequence": 10, "label": "NEXT: NEGATIVE & QUESTIONS", "type": "text", "colorMode": "none",
             "region": {"x": 1250, "y": 945, "width": 620, "height": 80},
             "reveal": {"direction": "left_to_right", "startMs": 46800, "durationMs": 4800}}
        ]
    }
}


def build_and_audit_scene(s_num: int, project_dir: Path):
    img_path = project_dir / "images" / f"scene_{s_num:02d}.png"
    annot_path = project_dir / "images" / f"scene_{s_num:02d}.annotation.json"
    region_path = project_dir / "images" / f"scene_{s_num:02d}_regions.png"

    if not img_path.exists():
        print(f"Bỏ qua Scene {s_num}: Không tìm thấy ảnh {img_path}")
        return

    data = NEW_SCENE_DEFS[s_num]
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

    img = cv2.imread(str(img_path))
    vis = img.copy()
    h, w = img.shape[:2]

    # Kiểm tra mực & độ phủ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10) < 190
    total_ink = int(np.count_nonzero(thresh))

    coverage = np.zeros((h, w), dtype=int)
    for el in data["elements"]:
        idx = el["sequence"]
        r = el["region"]
        x, y, rw, rh = r["x"], r["y"], r["width"], r["height"]
        color = PALETTE[(idx - 1) % len(PALETTE)]
        cv2.rectangle(vis, (x, y), (x + rw, y + rh), color, 2)

        eid = el.get("id", f"el-{idx}")
        lbl = el.get("label", eid)
        badge_txt = f"[{idx}] {eid} ({lbl[:18]}...)" if len(lbl) > 18 else f"[{idx}] {eid} ({lbl})"
        badge_w = len(badge_txt) * 9 + 14
        badge_y = y - 6 if y > 30 else y + rh + 20
        cv2.rectangle(vis, (x, badge_y - 18), (x + badge_w, badge_y + 4), color, -1)
        cv2.putText(vis, badge_txt, (x + 4, badge_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        coverage[y:y+rh, x:x+rw] += 1

    cv2.imwrite(str(region_path), vis)

    covered_ink = int(np.count_nonzero((coverage >= 1) & thresh))
    pct = (covered_ink / total_ink * 100.0) if total_ink > 0 else 100.0
    overlap = int(np.count_nonzero((coverage > 1) & thresh))
    print(f"  • Scene {s_num:02d}: {len(data['elements'])} elements | Mực: {pct:.1f}% ({covered_ink:,}/{total_ink:,}) | Trùng: {overlap}px | Xuất: {region_path.name}")


def main():
    root = Path("projects/WB-ENG-A1-003")
    print("=" * 70)
    print(" TÁI CẤU TRÚC PHÂN VÙNG VI MÔ CHUẨN NGỮ NGHĨA (SCENE 04 -> 09)")
    print("=" * 70)
    for s in range(4, 10):
        build_and_audit_scene(s, root)
    print("=" * 70)
    print("🎉 Hoàn tất tái cấu trúc phân vùng vi mô chuẩn ngữ nghĩa!")


if __name__ == "__main__":
    main()
