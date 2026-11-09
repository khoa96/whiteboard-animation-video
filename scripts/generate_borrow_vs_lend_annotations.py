#!/usr/bin/env python3
"""
generate_borrow_vs_lend_annotations.py — Đồng bộ Master Clock và phân vùng hoạt họa tự động
cho dự án project_borrow_vs_lend theo chuẩn Gate 2 của Content Engine.
"""

import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "projects/project_borrow_vs_lend"
SCENES_DIR = PROJ_DIR / "scenes"

def get_bounding_box(mask, pad=4):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return {"x": 0, "y": 0, "width": 0, "height": 0}
    x_min = max(0, int(xs.min()) - pad)
    y_min = max(0, int(ys.min()) - pad)
    x_max = min(1920, int(xs.max()) + 1 + pad)
    y_max = min(1080, int(ys.max()) + 1 + pad)
    return {
        "x": x_min,
        "y": y_min,
        "width": x_max - x_min,
        "height": y_max - y_min
    }

def draw_preview(img_path, elements, out_preview_path):
    img = Image.open(img_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    colors = [
        (52, 120, 212, 160),   # Blue
        (34, 168, 149, 160),   # Teal
        (245, 166, 35, 160),   # Orange
        (220, 38, 38, 160),    # Red
        (139, 92, 246, 160),   # Purple
        (16, 185, 129, 160),   # Green
    ]
    
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    for idx, el in enumerate(elements):
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        color = colors[idx % len(colors)]
        border_color = (color[0], color[1], color[2], 230)
        fill_color = (color[0], color[1], color[2], 40)
        
        draw.rectangle([x, y, x + w, y + h], fill=fill_color, outline=border_color, width=3)
        tag = f"[{el['sequence']}] {el['label']} ({el['reveal']['startMs']}ms - {el['reveal']['startMs']+el['reveal']['durationMs']}ms)"
        tag_w = len(tag) * 11
        draw.rectangle([x, max(0, y - 30), x + tag_w, max(0, y - 30) + 28], fill=(20, 23, 31, 230))
        draw.text((x + 6, max(0, y - 30) + 3), tag, fill=(255, 255, 255, 255), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(out_preview_path)
    print(f"  ✓ Đã lưu ảnh phân vùng: {out_preview_path.name}")


def build_scene_01():
    print("\n--- XỬ LÝ SCENE 01: Bản Chất Dòng Chảy ---")
    scene_dir = SCENES_DIR / "scene_01"
    img_path = scene_dir / "scene_01.png"
    cues_path = scene_dir / "timing_cues.json"

    with open(cues_path, "r", encoding="utf-8") as f:
        cues_data = json.load(f)
    cues = {c["index"]: c for c in cues_data["cues"]}
    total_dur = cues_data["totalDurationMs"]

    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    m_title = np.zeros_like(ink)
    m_alex = np.zeros_like(ink)
    m_ben = np.zeros_like(ink)
    m_borrow = np.zeros_like(ink)
    m_lend = np.zeros_like(ink)
    m_prep = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 210:
            m_title |= comp
        elif cx < 650 and cy >= 210:
            m_alex |= comp
        elif cx > 1300 and cy >= 210:
            m_ben |= comp
        elif 650 <= cx <= 1300:
            if 210 <= cy < 450:
                m_borrow |= comp
            elif 450 <= cy < 650:
                m_lend |= comp
            else:
                m_prep |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "TITLE: BORROW vs. LEND",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_title),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[1]["startMs"],
                "durationMs": cues[2]["endMs"] - cues[1]["startMs"]
            }
        },
        {
            "id": "el-02-char-alex",
            "sequence": 2,
            "label": "2D Character: Alex (YOU)",
            "type": "colored_image",
            "colorMode": "wash",
            "region": get_bounding_box(m_alex),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[3]["startMs"],
                "durationMs": cues[3]["durationMs"]
            }
        },
        {
            "id": "el-03-char-ben",
            "sequence": 3,
            "label": "2D Character: Ben (FRIEND)",
            "type": "colored_image",
            "colorMode": "wash",
            "region": get_bounding_box(m_ben),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[4]["startMs"],
                "durationMs": cues[4]["durationMs"]
            }
        },
        {
            "id": "el-04-arrow-borrow",
            "sequence": 4,
            "label": "Arrow: BORROW = Take in",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_borrow),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[5]["startMs"],
                "durationMs": cues[5]["durationMs"]
            }
        },
        {
            "id": "el-05-arrow-lend",
            "sequence": 5,
            "label": "Arrow: LEND = Give out",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_lend),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[6]["startMs"],
                "durationMs": cues[6]["durationMs"]
            }
        },
        {
            "id": "el-06-preposition-card",
            "sequence": 6,
            "label": "Rule: borrow FROM -> lend TO",
            "type": "box",
            "colorMode": "auto",
            "region": get_bounding_box(m_prep),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[7]["startMs"],
                "durationMs": cues[7]["durationMs"]
            }
        }
    ]

    annotation = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": total_dur,
        "globalStartMs": 0,
        "globalEndMs": total_dur,
        "fps": 60,
        "elements": elements
    }

    out_annot = scene_dir / "scene_01.annotation.json"
    with open(out_annot, "w", encoding="utf-8") as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Đã xuất cấu hình hoạt họa: {out_annot.name}")

    out_preview = scene_dir / "scene_01_regions.png"
    draw_preview(img_path, elements, out_preview)


def build_scene_02():
    print("\n--- XỬ LÝ SCENE 02: Bẫy Câu Hỏi & Thử Thách 3 Giây ---")
    scene_dir = SCENES_DIR / "scene_02"
    img_path = scene_dir / "scene_02.png"
    cues_path = scene_dir / "timing_cues.json"

    with open(cues_path, "r", encoding="utf-8") as f:
        cues_data = json.load(f)
    cues = {c["index"]: c for c in cues_data["cues"]}
    total_dur = cues_data["totalDurationMs"]

    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    m_title = np.zeros_like(ink)
    m_left_card = np.zeros_like(ink)
    m_right_card = np.zeros_like(ink)
    m_quiz_card = np.zeros_like(ink)
    m_circle = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        area = stats[i][4]

        if cy < 190:
            m_title |= comp
        elif 190 <= cy < 450:
            if cx < 960:
                m_left_card |= comp
            else:
                m_right_card |= comp
        else:
            # Quiz area (cy >= 450)
            # Orange circle around B. lend + checkmark
            if (cy > 780 and 740 <= cx <= 1200) and (area in [9567, 1205] or (746 <= stats[i][0] <= 1150 and stats[i][1] >= 798)):
                m_circle |= comp
            else:
                m_quiz_card |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "TITLE: HOW TO ASK",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_title),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[1]["startMs"],
                "durationMs": cues[1]["durationMs"]
            }
        },
        {
            "id": "el-02-card-borrow",
            "sequence": 2,
            "label": "Card: Can I borrow your pen?",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_left_card),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[2]["startMs"],
                "durationMs": cues[2]["durationMs"]
            }
        },
        {
            "id": "el-03-card-lend",
            "sequence": 3,
            "label": "Card: Can you lend me your pen?",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_right_card),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[3]["startMs"],
                "durationMs": cues[3]["durationMs"]
            }
        },
        {
            "id": "el-04-quiz-box",
            "sequence": 4,
            "label": "Interactive Quiz Container",
            "type": "box",
            "colorMode": "auto",
            "region": get_bounding_box(m_quiz_card),
            "reveal": {
                "direction": "left_to_right",
                "startMs": cues[4]["startMs"],
                "durationMs": cues[4]["durationMs"]
            }
        },
        {
            "id": "el-05-answer-circle",
            "sequence": 5,
            "label": "Orange Circle: B. lend + Checkmark",
            "type": "colored_image",
            "colorMode": "wash",
            "region": get_bounding_box(m_circle),
            "reveal": {
                "direction": "center_out",
                "startMs": cues[5]["startMs"],
                "durationMs": cues[5]["durationMs"]
            }
        }
    ]

    annotation = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": total_dur,
        "globalStartMs": 27890,
        "globalEndMs": 27890 + total_dur,
        "fps": 60,
        "elements": elements
    }

    out_annot = scene_dir / "scene_02.annotation.json"
    with open(out_annot, "w", encoding="utf-8") as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Đã xuất cấu hình hoạt họa: {out_annot.name}")

    out_preview = scene_dir / "scene_02_regions.png"
    draw_preview(img_path, elements, out_preview)


def main():
    print("============================================================")
    print("🎬 TỰ ĐỘNG PHÂN VÙNG VÀ ĐỒNG BỘ MASTER CLOCK — BORROW vs LEND")
    print("============================================================")
    build_scene_01()
    build_scene_02()
    print("\n✅ HOÀN TẤT TOÀN BỘ 2 PHÂN CẢNH!")

if __name__ == "__main__":
    main()

