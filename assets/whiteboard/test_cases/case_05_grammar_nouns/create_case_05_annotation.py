#!/usr/bin/env python3
"""
Tạo annotation.json chuẩn cho Test Case 5: SINGULAR -> PLURAL (English Grammar).
Bố cục 4 Zone rõ rệt:
Zone 1: Tiêu đề SINGULAR -> PLURAL & 3 từ khóa ONE, MANY, NOUN
Zone 2: So sánh trực quan (ONE cat vs MANY cats), quy trình chuyển đổi và quy tắc NOUN + S -> PLURAL
Zone 3: Câu ví dụ "I have three cats." với đúng 1 gạch chân xanh dưới từ "cats"
Zone 4: Ví dụ bổ sung (book -> books, apple -> apples)
"""
from pathlib import Path
import json
import cv2

CASE_DIR = Path(__file__).resolve().parent
IMG_PATH = CASE_DIR / "grammar_nouns.png"
ANN_PATH = CASE_DIR / "grammar_nouns.annotation.json"
REGIONS_PATH = CASE_DIR / "grammar_nouns-regions.png"

img = cv2.imread(str(IMG_PATH))
H, W = img.shape[:2]

# --- 1. TỌA ĐỘ CHÍNH XÁC TỪNG PHẦN TỬ (ZERO OVERLAP & ĐẦY ĐỦ CHI TIẾT) ---

# ZONE 1:
box_title = {"x": 375, "y": 65, "width": 1175, "height": 118}
box_kw_one = {"x": 558, "y": 210, "width": 172, "height": 82}
box_kw_many = {"x": 820, "y": 210, "width": 240, "height": 82}
box_kw_noun = {"x": 1140, "y": 210, "width": 230, "height": 82}

# ZONE 2 - LEFT (SINGULAR):
box_left_one = {"x": 260, "y": 290, "width": 175, "height": 78}      # y: 290..368
box_left_cat = {"x": 215, "y": 382, "width": 215, "height": 222}      # y: 382..604
box_left_cat_label = {"x": 250, "y": 610, "width": 175, "height": 75} # y: 610..685

# ZONE 2 - CENTER:
box_trans_eq = {"x": 575, "y": 430, "width": 770, "height": 82}
box_rule = {"x": 580, "y": 612, "width": 760, "height": 82}          # y: 612..694 (bao trọn vẹn toàn bộ chữ PLURAL)

# ZONE 2 - RIGHT (PLURAL):
box_right_many = {"x": 1485, "y": 290, "width": 240, "height": 78}    # y: 290..368
box_right_3cats = {"x": 1425, "y": 380, "width": 395, "height": 225}   # y: 380..605
box_right_cats_label = {"x": 1515, "y": 610, "width": 215, "height": 75} # y: 610..685

# ZONE 3:
box_sentence = {"x": 500, "y": 745, "width": 925, "height": 120}     # y: 745..865, x: 500..1425 (bao gồm cả dấu chấm '.')
box_underline = {"x": 1170, "y": 870, "width": 228, "height": 22}      # y: 870..892 (chỉ dưới 'cats')

# ZONE 4:
box_ex_book_icon = {"x": 220, "y": 915, "width": 118, "height": 120}   # x: 220..338
box_ex_book_text = {"x": 348, "y": 925, "width": 510, "height": 95}    # x: 348..858

box_ex_apple_icon = {"x": 1045, "y": 915, "width": 100, "height": 115} # x: 1045..1145
box_ex_apple_text = {"x": 1155, "y": 925, "width": 545, "height": 115} # x: 1155..1700

elements = [
    # Zone 1: Title & Keywords
    {
        "id": "el-01-title",
        "sequence": 1,
        "label": "Tiêu đề: SINGULAR -> PLURAL",
        "type": "text",
        "narrativeRole": "Giới thiệu chủ đề Danh từ Số ít & Số nhiều",
        "region": box_title,
        "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 1400, "protectedRegions": []}
    },
    {
        "id": "el-02-kw-one",
        "sequence": 2,
        "label": "Từ khóa: ONE (Số ít)",
        "type": "text",
        "narrativeRole": "Khái niệm số ít - một đối tượng",
        "region": box_kw_one,
        "reveal": {"direction": "left_to_right", "startMs": 1900, "durationMs": 500, "protectedRegions": []}
    },
    {
        "id": "el-03-kw-many",
        "sequence": 3,
        "label": "Từ khóa: MANY (Số nhiều)",
        "type": "text",
        "narrativeRole": "Khái niệm số nhiều - nhiều đối tượng",
        "region": box_kw_many,
        "reveal": {"direction": "left_to_right", "startMs": 2500, "durationMs": 500, "protectedRegions": []}
    },
    {
        "id": "el-04-kw-noun",
        "sequence": 4,
        "label": "Từ khóa: NOUN (Danh từ)",
        "type": "text",
        "narrativeRole": "Đối tượng áp dụng quy tắc",
        "region": box_kw_noun,
        "reveal": {"direction": "left_to_right", "startMs": 3100, "durationMs": 500, "protectedRegions": []}
    },

    # Zone 2: Singular Side (Left)
    {
        "id": "el-05-left-one",
        "sequence": 5,
        "label": "Nhãn cột trái: ONE",
        "type": "text",
        "narrativeRole": "Chỉ định nhóm số ít",
        "region": box_left_one,
        "reveal": {"direction": "left_to_right", "startMs": 3750, "durationMs": 500, "protectedRegions": []}
    },
    {
        "id": "el-06-left-cat",
        "sequence": 6,
        "label": "Hình vẽ: 1 chú mèo hoạt hình",
        "type": "colored_image",
        "narrativeRole": "Minh họa 1 cá thể danh từ số ít",
        "region": box_left_cat,
        "reveal": {"direction": "radial_outward", "startMs": 4350, "durationMs": 1400, "protectedRegions": []}
    },
    {
        "id": "el-07-left-cat-label",
        "sequence": 7,
        "label": "Nhãn từ: cat",
        "type": "text",
        "narrativeRole": "Từ số ít ở dạng nguyên bản",
        "region": box_left_cat_label,
        "reveal": {"direction": "left_to_right", "startMs": 5850, "durationMs": 650, "protectedRegions": []}
    },

    # Zone 2: Transformation Flow (Center)
    {
        "id": "el-08-trans-eq",
        "sequence": 8,
        "label": "Quy trình chuyển đổi: cat -> cat + s -> cats",
        "type": "colored_image",
        "narrativeRole": "Mô phỏng thêm đuôi 's' vào danh từ",
        "region": box_trans_eq,
        "reveal": {"direction": "left_to_right", "startMs": 6650, "durationMs": 1800, "protectedRegions": []}
    },

    # Zone 2: Plural Side (Right)
    {
        "id": "el-09-right-many",
        "sequence": 9,
        "label": "Nhãn cột phải: MANY",
        "type": "text",
        "narrativeRole": "Chỉ định nhóm số nhiều",
        "region": box_right_many,
        "reveal": {"direction": "left_to_right", "startMs": 8600, "durationMs": 500, "protectedRegions": []}
    },
    {
        "id": "el-10-right-3cats",
        "sequence": 10,
        "label": "Hình vẽ: 3 chú mèo hoạt hình",
        "type": "colored_image",
        "narrativeRole": "Minh họa nhiều cá thể danh từ số nhiều",
        "region": box_right_3cats,
        "reveal": {"direction": "radial_outward", "startMs": 9200, "durationMs": 2000, "protectedRegions": []}
    },
    {
        "id": "el-11-right-cats-label",
        "sequence": 11,
        "label": "Nhãn từ: cats (chữ s xanh lá)",
        "type": "text",
        "narrativeRole": "Từ số nhiều hoàn chỉnh",
        "region": box_right_cats_label,
        "reveal": {"direction": "left_to_right", "startMs": 11300, "durationMs": 700, "protectedRegions": []}
    },

    # Zone 2: Grammar Rule (Center Bottom)
    {
        "id": "el-12-rule",
        "sequence": 12,
        "label": "Quy tắc ngữ pháp: NOUN + S -> PLURAL",
        "type": "colored_image",
        "narrativeRole": "Công thức đúc kết nguyên tắc chung",
        "region": box_rule,
        "reveal": {"direction": "left_to_right", "startMs": 12150, "durationMs": 1600, "protectedRegions": []}
    },

    # Zone 3: Example Sentence & Underline
    {
        "id": "el-13-sentence",
        "sequence": 13,
        "label": "Câu ví dụ: I have three cats.",
        "type": "text",
        "narrativeRole": "Ứng dụng trong câu giao tiếp thực tế",
        "region": box_sentence,
        "reveal": {"direction": "left_to_right", "startMs": 13950, "durationMs": 1800, "protectedRegions": []}
    },
    {
        "id": "el-14-underline",
        "sequence": 14,
        "label": "Gạch chân xanh duy nhất: dưới từ 'cats'",
        "type": "gesture",
        "narrativeRole": "Nhấn mạnh danh từ số nhiều trong câu",
        "region": box_underline,
        "reveal": {"direction": "left_to_right", "startMs": 15850, "durationMs": 650, "protectedRegions": []}
    },

    # Zone 4: Additional Examples
    {
        "id": "el-15-ex-book-icon",
        "sequence": 15,
        "label": "Biểu tượng: Cuốn sách",
        "type": "colored_image",
        "narrativeRole": "Ví dụ bổ sung 1: đồ vật",
        "region": box_ex_book_icon,
        "reveal": {"direction": "radial_outward", "startMs": 16650, "durationMs": 900, "protectedRegions": []}
    },
    {
        "id": "el-16-ex-book-text",
        "sequence": 16,
        "label": "Ví dụ: book -> books",
        "type": "colored_image",
        "narrativeRole": "Chuyển đổi số nhiều của book",
        "region": box_ex_book_text,
        "reveal": {"direction": "left_to_right", "startMs": 17650, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-17-ex-apple-icon",
        "sequence": 17,
        "label": "Biểu tượng: Quả táo",
        "type": "colored_image",
        "narrativeRole": "Ví dụ bổ sung 2: hoa quả",
        "region": box_ex_apple_icon,
        "reveal": {"direction": "radial_outward", "startMs": 19000, "durationMs": 900, "protectedRegions": []}
    },
    {
        "id": "el-18-ex-apple-text",
        "sequence": 18,
        "label": "Ví dụ: apple -> apples",
        "type": "colored_image",
        "narrativeRole": "Chuyển đổi số nhiều của apple",
        "region": box_ex_apple_text,
        "reveal": {"direction": "left_to_right", "startMs": 20000, "durationMs": 1300, "protectedRegions": []}
    }
]

annotation = {
    "version": "1.0",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": 22000,
    "storyBasis": "Ngữ pháp tiếng Anh: Quy tắc chuyển đổi Danh từ số ít sang số nhiều (Singular -> Plural)",
    "elements": elements
}

with open(ANN_PATH, "w", encoding="utf-8") as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)

print(f"✓ Đã tạo annotation JSON: {ANN_PATH}")

# Vẽ Regions map
vis = img.copy()
colors = [
    (230, 40, 40),    # Blue (BGR: Red channel)
    (40, 180, 40),    # Green
    (40, 80, 240),    # Orange
    (180, 40, 180),   # Purple
    (40, 200, 220),   # Yellow
    (200, 120, 40),   # Cyan
    (120, 40, 220),   # Magenta
]

for i, el in enumerate(elements):
    r = el["region"]
    c = colors[i % len(colors)]
    x, y, w, h = r["x"], r["y"], r["width"], r["height"]
    cv2.rectangle(vis, (x, y), (x + w, y + h), c, 2)
    label_txt = f"{el['sequence']}. {el['id']}"
    cv2.putText(vis, label_txt, (x + 4, max(y - 6, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.40, c, 1, cv2.LINE_AA)

cv2.imwrite(str(REGIONS_PATH), vis)
print(f"✓ Đã tạo ảnh phân vùng hoàn hảo: {REGIONS_PATH}")
