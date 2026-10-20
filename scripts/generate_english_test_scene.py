#!/usr/bin/env python3
"""
Tạo bài giảng tiếng Anh mẫu để test trực tiếp engine vẽ Whiteboard.
Bao gồm:
  1. Title (Text - ink only)
  2. Formula Box (Box & Text - ink only)
  3. Question Sentence (Text - ink only)
  4. Underline (Gạch chân dấu hiệu nhận biết - gesture ink only)
  5. Options (Text - ink only)
  6. Circle answer (Khoanh tròn đáp án đúng - gesture ink only)
  7. Explanation (Text - ink only)
  8. Badge / Icon (Hình ảnh có màu - colored_image ink + color wash)
"""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_PATH = OUTPUT_DIR / "test_english_lesson.png"
JSON_PATH = OUTPUT_DIR / "test_english_lesson.annotation.json"

W, H = 1920, 1080
BG_COLOR = (245, 235, 215)  # Màu kem bảng trắng #F5EBD7


def _get_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def create_scene():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = _get_font(52)
    font_heading = _get_font(36)
    font_body = _get_font(32)
    font_bold = _get_font(34)
    font_small = _get_font(24)

    # 1. Title: ENGLISH GRAMMAR: PRESENT PERFECT
    draw.text((100, 50), "ENGLISH GRAMMAR: PRESENT PERFECT", fill=(20, 25, 40), font=font_title)
    draw.line([(100, 115), (1150, 115)], fill=(38, 103, 255), width=4)

    # 2. Formula Box
    box_x0, box_y0, box_x1, box_y1 = 100, 150, 1250, 290
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=12, outline=(50, 70, 100), width=3)
    draw.text((130, 170), "FORMULA / CÔNG THỨC:", fill=(180, 50, 40), font=font_heading)
    draw.text((130, 225), "Subject  +  have / has  +  V3 / Ved", fill=(20, 30, 50), font=font_bold)

    # 3. Question Sentence
    q_text = "Question: She ________ in London since 2018."
    draw.text((100, 340), q_text, fill=(20, 25, 40), font=font_bold)

    # 4. Underline dưới từ "since 2018"
    draw.line([(550, 385), (760, 385)], fill=(38, 103, 255), width=5)

    # 5. Options A, B, C, D
    draw.text((120, 430), "A. lives", fill=(40, 45, 60), font=font_body)
    draw.text((360, 430), "B. has lived", fill=(40, 45, 60), font=font_body)
    draw.text((640, 430), "C. lived", fill=(40, 45, 60), font=font_body)
    draw.text((860, 430), "D. was living", fill=(40, 45, 60), font=font_body)

    # 6. Khoanh tròn đáp án đúng "B. has lived" (màu đỏ rực rỡ)
    draw.ellipse([340, 415, 570, 480], outline=(220, 38, 38), width=5)

    # 7. Explanation Box
    exp_x0, exp_y0, exp_x1, exp_y1 = 100, 530, 1250, 700
    draw.rounded_rectangle([exp_x0, exp_y0, exp_x1, exp_y1], radius=10, outline=(70, 90, 120), width=2)
    draw.text((130, 550), "EXPLANATION / GIẢI THÍCH:", fill=(38, 103, 255), font=font_heading)
    draw.text((130, 605), "• 'since 2018' là mốc thời gian trong quá khứ -> Dùng Present Perfect", fill=(30, 40, 55), font=font_body)
    draw.text((130, 650), "• Chủ ngữ 'She' là ngôi thứ 3 số ít -> Đi với 'has' + V3 ('has lived')", fill=(30, 40, 55), font=font_body)

    # 8. Badge minh họa bên phải (Hình vẽ ngôi sao có màu sắc đa dạng)
    badge_cx, badge_cy = 1550, 420
    # Vòng tròn nền huy hiệu
    draw.ellipse([badge_cx - 160, badge_cy - 160, badge_cx + 160, badge_cy + 160], fill=(255, 230, 140), outline=(230, 160, 30), width=6)
    # Ngôi sao 5 cánh màu cam đỏ
    star_pts = []
    for i in range(10):
        r = 110 if i % 2 == 0 else 50
        angle = i * math.pi / 5 - math.pi / 2
        star_pts.append((badge_cx + r * math.cos(angle), badge_cy + r * math.sin(angle)))
    draw.polygon(star_pts, fill=(245, 120, 30), outline=(190, 80, 20))
    draw.text((badge_cx - 95, badge_cy + 190), "PERFECT SCORE!", fill=(180, 60, 20), font=font_heading)
    draw.text((badge_cx - 70, badge_cy + 240), "+100 POINTS", fill=(40, 80, 160), font=font_small)

    img.save(IMG_PATH, quality=95)
    print(f"  ✓ Đã tạo ảnh: {IMG_PATH}")


def create_annotation():
    annotation = {
        "sceneId": "test_english_lesson",
        "canvas": { "width": W, "height": H },
        "storyBasis": "Bài giảng tiếng Anh mẫu: Thì hiện tại hoàn thành",
        "sceneDurationMs": 10000,
        "elements": [
            {
                "id": "title",
                "label": "Tiêu đề bài học",
                "type": "text",
                "colorMode": "none",
                "sequence": 1,
                "region": { "x": 80, "y": 40, "width": 1100, "height": 95 },
                "reveal": { "direction": "left_to_right", "startMs": 200, "durationMs": 1300, "maskPaddingPx": 10 }
            },
            {
                "id": "formula",
                "label": "Khung công thức",
                "type": "box",
                "colorMode": "none",
                "sequence": 2,
                "region": { "x": 80, "y": 140, "width": 1200, "height": 165 },
                "reveal": { "direction": "left_to_right", "startMs": 1600, "durationMs": 1500, "maskPaddingPx": 10 }
            },
            {
                "id": "question",
                "label": "Câu hỏi trắc nghiệm",
                "type": "text",
                "colorMode": "none",
                "sequence": 3,
                "region": { "x": 80, "y": 320, "width": 1000, "height": 70 },
                "reveal": { "direction": "left_to_right", "startMs": 3200, "durationMs": 1300, "maskPaddingPx": 10 }
            },
            {
                "id": "underline",
                "label": "Gạch chân dấu hiệu since 2018",
                "type": "underline",
                "colorMode": "none",
                "sequence": 4,
                "region": { "x": 540, "y": 375, "width": 230, "height": 30 },
                "reveal": { "direction": "left_to_right", "startMs": 4600, "durationMs": 600, "maskPaddingPx": 5 }
            },
            {
                "id": "options",
                "label": "4 lựa chọn A B C D",
                "type": "text",
                "colorMode": "none",
                "sequence": 5,
                "region": { "x": 100, "y": 410, "width": 950, "height": 70 },
                "reveal": { "direction": "left_to_right", "startMs": 5300, "durationMs": 1200, "maskPaddingPx": 10 }
            },
            {
                "id": "circle_answer",
                "label": "Khoanh tròn đáp án đúng B",
                "type": "circle",
                "colorMode": "none",
                "sequence": 6,
                "region": { "x": 330, "y": 405, "width": 250, "height": 85 },
                "reveal": { "direction": "left_to_right", "startMs": 6600, "durationMs": 700, "maskPaddingPx": 5 }
            },
            {
                "id": "explanation",
                "label": "Khung giải thích chi tiết",
                "type": "text",
                "colorMode": "none",
                "sequence": 7,
                "region": { "x": 80, "y": 520, "width": 1200, "height": 195 },
                "reveal": { "direction": "left_to_right", "startMs": 7400, "durationMs": 1400, "maskPaddingPx": 10 }
            },
            {
                "id": "badge",
                "label": "Huy hiệu thưởng có màu",
                "type": "colored_image",
                "colorMode": "wash",
                "sequence": 8,
                "region": { "x": 1360, "y": 240, "width": 380, "height": 550 },
                "reveal": { "direction": "top_to_bottom", "startMs": 8900, "durationMs": 1000, "maskPaddingPx": 10 }
            }
        ]
    }
    JSON_PATH.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Đã tạo annotation: {JSON_PATH}")


if __name__ == "__main__":
    print("=" * 60)
    print("Khởi tạo bộ dữ liệu bài giảng tiếng Anh mẫu...")
    print("=" * 60)
    create_scene()
    create_annotation()
    print("Hoàn tất!")
