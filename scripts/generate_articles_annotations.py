#!/usr/bin/env python3
"""
scripts/generate_articles_annotations.py
Phân vùng vi mô chuẩn mực (Atomic Semantic Segmentation) & Đồng bộ Master Clock
cho toàn bộ 9 phân cảnh của project_articles_a_an.
"""

import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "projects/project_articles_a_an"
SCENES_DIR = PROJ_DIR / "scenes"


def get_bounding_box(mask, pad=4, max_w=1920, max_h=1080):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return {"x": 0, "y": 0, "width": 0, "height": 0}
    x_min = max(0, int(xs.min()) - pad)
    y_min = max(0, int(ys.min()) - pad)
    x_max = min(max_w, int(xs.max()) + 1 + pad)
    y_max = min(max_h, int(ys.max()) + 1 + pad)
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
        (236, 72, 153, 160),   # Pink
        (234, 88, 12, 160),    # Amber
    ]

    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()

    for idx, el in enumerate(elements):
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        if w == 0 or h == 0:
            continue
        color = colors[idx % len(colors)]
        border_color = (color[0], color[1], color[2], 230)
        fill_color = (color[0], color[1], color[2], 40)

        draw.rectangle([x, y, x + w, y + h], fill=fill_color, outline=border_color, width=3)
        tag = f"[{el['sequence']}] {el['label']} ({el['reveal']['startMs']}ms-{el['reveal']['startMs']+el['reveal']['durationMs']}ms)"
        tag_w = len(tag) * 11
        draw.rectangle([x, max(0, y - 28), x + tag_w, max(0, y - 28) + 26], fill=(20, 23, 31, 230))
        draw.text((x + 6, max(0, y - 28) + 3), tag, fill=(255, 255, 255, 255), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(out_preview_path)
    print(f"  ✓ Đã lưu ảnh phân vùng: {out_preview_path.name}")


def load_cues(scene_idx):
    cues_path = SCENES_DIR / f"scene_{scene_idx:02d}" / "timing_cues.json"
    with open(cues_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cues = {c["index"]: c for c in data["cues"]}
    return cues, data.get("totalDurationMs", 30000)


def save_annotation(scene_idx, elements, img_path):
    scene_dir = SCENES_DIR / f"scene_{scene_idx:02d}"
    ann_path = scene_dir / f"scene_{scene_idx:02d}.annotation.json"
    out_preview = scene_dir / f"scene_{scene_idx:02d}_regions.png"

    annotation_data = {
        "sceneId": f"scene_{scene_idx:02d}",
        "imagePath": f"scene_{scene_idx:02d}.png",
        "canvas": {
            "width": 1920,
            "height": 1080
        },
        "elements": elements
    }

    with open(ann_path, "w", encoding="utf-8") as f:
        json.dump(annotation_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Đã lưu annotation: {ann_path.name} ({len(elements)} elements)")

    draw_preview(img_path, elements, out_preview)


def build_scene(scene_idx, partition_fn):
    print(f"\n▶ ĐANG XỬ LÝ SCENE {scene_idx:02d}...")
    scene_dir = SCENES_DIR / f"scene_{scene_idx:02d}"
    img_path = scene_dir / f"scene_{scene_idx:02d}.png"
    cues, total_dur = load_cues(scene_idx)

    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    elements = partition_fn(num, labels, stats, centroids, ink, cues, total_dur)
    save_annotation(scene_idx, elements, img_path)


# ==============================================================================
# ĐỊNH NGHĨA PHÂN VÙNG CHO TỪNG SCENE CỤ THỂ
# ==============================================================================

def partition_s01(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_a_an = np.zeros_like(ink)
    m_the = np.zeros_like(ink)
    m_zero = np.zeros_like(ink)
    m_guide = np.zeros_like(ink)
    m_today = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 230:
            m_title |= comp
        elif 230 <= cy < 580:
            if cx < 750:
                m_a_an |= comp
            elif cx < 1180:
                m_the |= comp
            else:
                m_zero |= comp
        elif 580 <= cy < 640:
            m_guide |= comp
        else:
            m_today |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: ARTICLES THREE GROUPS",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {
                "startMs": cues[1]["startMs"],
                "durationMs": max(1200, cues[3]["endMs"] - cues[1]["startMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        },
        {
            "id": "el-02-card-a-an",
            "sequence": 2,
            "label": "Card 1: A / AN (a book, an apple)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_a_an),
            "reveal": {
                "startMs": cues[4]["startMs"],
                "durationMs": max(1200, cues[5]["endMs"] - cues[4]["startMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        },
        {
            "id": "el-03-card-the",
            "sequence": 3,
            "label": "Card 2: THE (the book)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_the),
            "reveal": {
                "startMs": cues[6]["startMs"],
                "durationMs": max(1200, cues[7]["endMs"] - cues[6]["startMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        },
        {
            "id": "el-04-card-zero",
            "sequence": 4,
            "label": "Card 3: ZERO ARTICLE (WATER)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_zero),
            "reveal": {
                "startMs": cues[8]["startMs"],
                "durationMs": max(1200, cues[9]["endMs"] - cues[8]["startMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        },
        {
            "id": "el-05-guide-line",
            "sequence": 5,
            "label": "Guide Line Connector",
            "elementType": "connector",
            "action": "connect_arrow",
            "region": get_bounding_box(m_guide),
            "reveal": {
                "startMs": cues[10]["startMs"],
                "durationMs": max(800, cues[10]["durationMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        },
        {
            "id": "el-06-focus-today",
            "sequence": 6,
            "label": "Focus Badge: TODAY: A / AN",
            "elementType": "accent",
            "action": "highlight",
            "region": get_bounding_box(m_today),
            "reveal": {
                "startMs": cues[11]["startMs"],
                "durationMs": max(1200, cues[11]["durationMs"]),
                "drawingStyle": "stroke",
                "colorStroke": True,
                "strokeWidth": 3
            }
        }
    ]
    return elements


def partition_s02(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_v_head = np.zeros_like(ink)
    m_v_letters = np.zeros_like(ink)
    m_c_head = np.zeros_like(ink)
    m_c_letters = np.zeros_like(ink)
    m_note_y = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 560:
            if cx < 850:
                if cy < 270:
                    m_v_head |= comp
                else:
                    m_v_letters |= comp
            else:
                if cy < 270:
                    m_c_head |= comp
                else:
                    m_c_letters |= comp
        else:
            m_note_y |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: VOWELS & CONSONANTS",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-vowel-heading",
            "sequence": 2,
            "label": "Heading: VOWEL LETTERS",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_v_head),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": cues[2]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-vowel-letters",
            "sequence": 3,
            "label": "Letters: A E I O U",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_v_letters),
            "reveal": {"startMs": cues[3]["startMs"], "durationMs": max(1500, cues[4]["endMs"] - cues[3]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-consonant-heading",
            "sequence": 4,
            "label": "Heading: CONSONANT LETTERS",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_c_head),
            "reveal": {"startMs": cues[5]["startMs"], "durationMs": cues[5]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-consonant-letters",
            "sequence": 5,
            "label": "Consonants: B C D F G ...",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_c_letters),
            "reveal": {"startMs": cues[6]["startMs"], "durationMs": max(1500, cues[7]["endMs"] - cues[6]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-06-note-y",
            "sequence": 6,
            "label": "Special Note: Y CAN ALSO BE A VOWEL",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_note_y),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1500, cues[11]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s03(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_book = np.zeros_like(ink)
    m_apple = np.zeros_like(ink)
    m_rule = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 580:
            if cx < 960:
                m_book |= comp
            else:
                m_apple |= comp
        else:
            m_rule |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: WHAT ARE A AND AN?",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-rule-one",
            "sequence": 2,
            "label": "Formula: ONE + COUNTABLE NOUN",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_rule),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1500, cues[4]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-ex-book",
            "sequence": 3,
            "label": "Example: a book",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_book),
            "reveal": {"startMs": cues[5]["startMs"], "durationMs": max(1500, cues[7]["endMs"] - cues[5]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-ex-apple",
            "sequence": 4,
            "label": "Example: an apple",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_apple),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1500, cues[11]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s04(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_sound_node = np.zeros_like(ink)
    m_consonant = np.zeros_like(ink)
    m_vowel = np.zeros_like(ink)
    m_reminder = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 160:
            m_title |= comp
        elif 160 <= cy < 270:
            m_sound_node |= comp
        elif 270 <= cy < 650:
            if cx < 960:
                m_consonant |= comp
            else:
                m_vowel |= comp
        else:
            m_reminder |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: A OR AN?",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-root-sound",
            "sequence": 2,
            "label": "Root Node: FIRST SOUND",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_sound_node),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1200, cues[3]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-branch-consonant",
            "sequence": 3,
            "label": "Branch: CONSONANT SOUND ➔ A (a book)",
            "elementType": "connector",
            "action": "connect_arrow",
            "region": get_bounding_box(m_consonant),
            "reveal": {"startMs": cues[4]["startMs"], "durationMs": max(1500, cues[7]["endMs"] - cues[4]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-branch-vowel",
            "sequence": 4,
            "label": "Branch: VOWEL SOUND ➔ AN (an apple)",
            "elementType": "connector",
            "action": "connect_arrow",
            "region": get_bounding_box(m_vowel),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1500, cues[11]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-reminder",
            "sequence": 5,
            "label": "Banner: SOUND, NOT LETTER",
            "elementType": "accent",
            "action": "highlight",
            "region": get_bounding_box(m_reminder),
            "reveal": {"startMs": cues[12]["startMs"], "durationMs": cues[12]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s05(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_col_a = np.zeros_like(ink)
    m_col_an = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        else:
            if cx < 960:
                m_col_a |= comp
            else:
                m_col_an |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: COMMON EXAMPLES",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-group-a",
            "sequence": 2,
            "label": "Group A: a book, a cat, a car",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_col_a),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(2000, cues[6]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-group-an",
            "sequence": 3,
            "label": "Group AN: an apple, an egg, an umbrella",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_col_an),
            "reveal": {"startMs": cues[7]["startMs"], "durationMs": max(2000, cues[12]["endMs"] - cues[7]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s06(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_hour = np.zeros_like(ink)
    m_honest = np.zeros_like(ink)
    m_univ = np.zeros_like(ink)
    m_europe = np.zeros_like(ink)
    m_listen = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 450:
            if cx < 960:
                m_hour |= comp
            else:
                m_honest |= comp
        elif 450 <= cy < 720:
            if cx < 960:
                m_univ |= comp
            else:
                m_europe |= comp
        else:
            m_listen |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: SPECIAL CASES / FIRST SOUND",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-card-hour",
            "sequence": 2,
            "label": "Card 1: an hour (H IS SILENT)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_hour),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1500, cues[4]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-card-honest",
            "sequence": 3,
            "label": "Card 2: an honest man (H IS SILENT)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_honest),
            "reveal": {"startMs": cues[5]["startMs"], "durationMs": max(1500, cues[6]["endMs"] - cues[5]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-card-univ",
            "sequence": 4,
            "label": "Card 3: a university (STARTS WITH Y SOUND)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_univ),
            "reveal": {"startMs": cues[7]["startMs"], "durationMs": max(1500, cues[10]["endMs"] - cues[7]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-card-europe",
            "sequence": 5,
            "label": "Card 4: a European country (STARTS WITH Y SOUND)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_europe),
            "reveal": {"startMs": cues[11]["startMs"], "durationMs": max(1500, cues[12]["endMs"] - cues[11]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-06-reminder",
            "sequence": 6,
            "label": "Reminder: LISTEN TO THE FIRST SOUND",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_listen),
            "reveal": {"startMs": cues[13]["startMs"], "durationMs": cues[13]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s07(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_look = np.zeros_like(ink)
    m_say = np.zeros_like(ink)
    m_listen = np.zeros_like(ink)
    m_choose = np.zeros_like(ink)
    m_examples = np.zeros_like(ink)
    m_reminder = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 420:
            if cx < 550:
                m_look |= comp
            elif cx < 920:
                m_say |= comp
            elif cx < 1320:
                m_listen |= comp
            else:
                m_choose |= comp
        elif 420 <= cy < 640:
            m_examples |= comp
        else:
            m_reminder |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: HOW TO CHOOSE",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-step-look",
            "sequence": 2,
            "label": "Step 1: LOOK",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_look),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1200, cues[3]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-step-say",
            "sequence": 3,
            "label": "Step 2: SAY",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_say),
            "reveal": {"startMs": cues[4]["startMs"], "durationMs": max(1200, cues[5]["endMs"] - cues[4]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-step-listen",
            "sequence": 4,
            "label": "Step 3: LISTEN (FIRST SOUND)",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_listen),
            "reveal": {"startMs": cues[6]["startMs"], "durationMs": max(1200, cues[7]["endMs"] - cues[6]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-step-choose",
            "sequence": 5,
            "label": "Step 4: CHOOSE (A / AN)",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_choose),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1200, cues[9]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-06-examples",
            "sequence": 6,
            "label": "Anchor: a book & an apple",
            "elementType": "illustration",
            "action": "draw_new",
            "region": get_bounding_box(m_examples),
            "reveal": {"startMs": cues[10]["startMs"], "durationMs": cues[10]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-07-reminder",
            "sequence": 7,
            "label": "Banner: SOUND, NOT LETTER",
            "elementType": "accent",
            "action": "highlight",
            "region": get_bounding_box(m_reminder),
            "reveal": {"startMs": cues[11]["startMs"], "durationMs": cues[11]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s08(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_q1 = np.zeros_like(ink)
    m_q2 = np.zeros_like(ink)
    m_q3 = np.zeros_like(ink)
    m_think = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 650:
            if cx < 720:
                m_q1 |= comp
            elif cx < 1250:
                m_q2 |= comp
            else:
                m_q3 |= comp
        else:
            m_think |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: CHOOSE A OR AN",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-q1-dog",
            "sequence": 2,
            "label": "Question 1: ___ dog ➔ A",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_q1),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1500, cues[4]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-q2-orange",
            "sequence": 3,
            "label": "Question 2: ___ orange ➔ AN",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_q2),
            "reveal": {"startMs": cues[5]["startMs"], "durationMs": max(1500, cues[7]["endMs"] - cues[5]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-q3-egg",
            "sequence": 4,
            "label": "Question 3: ___ egg ➔ AN",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_q3),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1500, cues[10]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-think-cue",
            "sequence": 5,
            "label": "Prompt: THINK FIRST",
            "elementType": "accent",
            "action": "highlight",
            "region": get_bounding_box(m_think),
            "reveal": {"startMs": cues[3]["startMs"], "durationMs": max(1000, cues[11]["endMs"] - cues[3]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def partition_s09(num, labels, stats, centroids, ink, cues, total_dur):
    m_title = np.zeros_like(ink)
    m_q4 = np.zeros_like(ink)
    m_q5 = np.zeros_like(ink)
    m_rule_a = np.zeros_like(ink)
    m_rule_an = np.zeros_like(ink)

    for i in range(1, num):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 180:
            m_title |= comp
        elif 180 <= cy < 500:
            if cx < 960:
                m_q4 |= comp
            else:
                m_q5 |= comp
        else:
            if cx < 960:
                m_rule_a |= comp
            else:
                m_rule_an |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Title: FINAL CHALLENGE",
            "elementType": "text",
            "action": "write_text",
            "region": get_bounding_box(m_title),
            "reveal": {"startMs": cues[1]["startMs"], "durationMs": cues[1]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-02-q4-hour",
            "sequence": 2,
            "label": "Question 4: ___ hour ➔ AN",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_q4),
            "reveal": {"startMs": cues[2]["startMs"], "durationMs": max(1500, cues[4]["endMs"] - cues[2]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-03-q5-univ",
            "sequence": 3,
            "label": "Question 5: ___ university ➔ A",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_q5),
            "reveal": {"startMs": cues[5]["startMs"], "durationMs": max(1500, cues[7]["endMs"] - cues[5]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-04-rule-a",
            "sequence": 4,
            "label": "Golden Rule: A + CONSONANT SOUND",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_rule_a),
            "reveal": {"startMs": cues[8]["startMs"], "durationMs": max(1200, cues[9]["endMs"] - cues[8]["startMs"]), "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        },
        {
            "id": "el-05-rule-an",
            "sequence": 5,
            "label": "Golden Rule: AN + VOWEL SOUND",
            "elementType": "container",
            "action": "draw_container",
            "region": get_bounding_box(m_rule_an),
            "reveal": {"startMs": cues[10]["startMs"], "durationMs": cues[10]["durationMs"], "drawingStyle": "stroke", "colorStroke": True, "strokeWidth": 3}
        }
    ]
    return elements


def main():
    print("=" * 65)
    print("🎨 BẮT ĐẦU PHÂN VÙNG HOẠT HỌA & ĐỒNG BỘ MASTER CLOCK CHO 9 SCENES")
    print("=" * 65)

    partitions = [
        (1, partition_s01),
        (2, partition_s02),
        (3, partition_s03),
        (4, partition_s04),
        (5, partition_s05),
        (6, partition_s06),
        (7, partition_s07),
        (8, partition_s08),
        (9, partition_s09),
    ]

    for idx, fn in partitions:
        build_scene(idx, fn)

    print("\n" + "=" * 65)
    print("🎉 HOÀN TẤT PHÂN VÙNG VÀ ĐỒNG BỘ CHO TOÀN BỘ 9 PHÂN CẢNH!")
    print("=" * 65)


if __name__ == "__main__":
    main()

