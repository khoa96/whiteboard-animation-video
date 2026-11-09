#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "projects/project_articles_a_an"
IMAGES_DIR = PROJ_DIR / "images"
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
    ]
    
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 26)
    except:
        font = ImageFont.load_default()

    for idx, el in enumerate(elements):
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        color = colors[idx % len(colors)]
        border_color = (color[0], color[1], color[2], 230)
        fill_color = (color[0], color[1], color[2], 40)
        
        draw.rectangle([x, y, x + w, y + h], fill=fill_color, outline=border_color, width=3)
        tag = f"[{el['sequence']}] {el['label']} ({el['reveal']['startMs']}ms-{el['reveal']['startMs']+el['reveal']['durationMs']}ms)"
        # Draw tag background
        draw.rectangle([x, y, x + len(tag)*13, y + 32], fill=(20, 23, 31, 220))
        draw.text((x + 6, y + 4), tag, fill=(255, 255, 255, 255), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(out_preview_path)
    print(f"  ✓ Saved preview: {out_preview_path}")

def build_scene_01():
    img_path = IMAGES_DIR / "scene_01.png"
    scene_dir = SCENES_DIR / "scene_01"
    shutil.copy(img_path, scene_dir / "scene_01.png")
    
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    m_title = np.zeros_like(ink)
    m_badge = np.zeros_like(ink)
    m_eye = np.zeros_like(ink)
    m_ear = np.zeros_like(ink)
    m_l_letter = np.zeros_like(ink)
    m_l_cat = np.zeros_like(ink)
    m_r_letter = np.zeros_like(ink)
    m_r_apple = np.zeros_like(ink)

    for i in range(1, num_labels):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 210 and 600 < cx < 1320:
            m_title |= comp
        elif 210 <= cy < 340 and 600 < cx < 1320:
            m_badge |= comp
        elif 340 <= cy < 800 and 600 <= cx < 1055:
            m_eye |= comp
        elif 340 <= cy < 800 and 1055 <= cx <= 1350:
            m_ear |= comp
        elif cx <= 650:
            if cy < 530:
                m_l_letter |= comp
            else:
                m_l_cat |= comp
        else:
            if cy < 530:
                m_r_letter |= comp
            else:
                m_r_apple |= comp

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "TITLE: A or AN?",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_title),
            "reveal": {"direction": "left_to_right", "startMs": 1830, "durationMs": 3800}
        },
        {
            "id": "el-02-badge",
            "sequence": 2,
            "label": "BADGE: = 1 (Singular Noun)",
            "type": "box",
            "colorMode": "auto",
            "region": get_bounding_box(m_badge),
            "reveal": {"direction": "left_to_right", "startMs": 5800, "durationMs": 3300}
        },
        {
            "id": "el-03-eye-anchor",
            "sequence": 3,
            "label": "ANCHOR: Letter (Eye) - NO!",
            "type": "colored_image",
            "colorMode": "wash",
            "region": get_bounding_box(m_eye, pad=0),
            "reveal": {"direction": "left_to_right", "startMs": 14680, "durationMs": 10500}
        },
        {
            "id": "el-04-ear-anchor",
            "sequence": 4,
            "label": "ANCHOR: Sound (Ear) - YES!",
            "type": "colored_image",
            "colorMode": "wash",
            "region": get_bounding_box(m_ear, pad=0),
            "reveal": {"direction": "top_to_bottom", "startMs": 25860, "durationMs": 4800}
        },
        {
            "id": "el-05-left-letter",
            "sequence": 5,
            "label": "A + Consonant Sound",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_l_letter),
            "reveal": {"direction": "left_to_right", "startMs": 30990, "durationMs": 2000}
        },
        {
            "id": "el-06-left-cat",
            "sequence": 6,
            "label": "Icon Cat & a cat (/kæt/)",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_l_cat),
            "reveal": {"direction": "left_to_right", "startMs": 33000, "durationMs": 2200}
        },
        {
            "id": "el-07-right-letter",
            "sequence": 7,
            "label": "AN + Vowel Sound",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_r_letter),
            "reveal": {"direction": "left_to_right", "startMs": 35480, "durationMs": 2400}
        },
        {
            "id": "el-08-right-apple",
            "sequence": 8,
            "label": "Icon Apple & an apple (/ˈæpl/)",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_r_apple),
            "reveal": {"direction": "left_to_right", "startMs": 37900, "durationMs": 2800}
        }
    ]

    data = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 42720,
        "globalStartMs": 0,
        "globalEndMs": 42720,
        "fps": 60,
        "elements": elements
    }
    
    ann_path = scene_dir / "scene_01.annotation.json"
    ann_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Scene 01 Micro-Atomic Annotation saved: {ann_path}")
    draw_preview(img_path, elements, scene_dir / "scene_01_regions.png")

def build_scene_02():
    img_path = IMAGES_DIR / "scene_02.png"
    scene_dir = SCENES_DIR / "scene_02"
    shutil.copy(img_path, scene_dir / "scene_02.png")
    
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    
    m_title = np.zeros_like(ink)
    m_sub = np.zeros_like(ink)
    m_stamp = np.zeros_like(ink)
    m_left = np.zeros_like(ink)
    m_right = np.zeros_like(ink)
    m_bottom = np.zeros_like(ink)

    for y in range(1080):
        for x in range(1920):
            if not ink[y, x]:
                continue
            if y < 165:
                m_title[y, x] = True
            elif y < 250 and x < 1500:
                m_sub[y, x] = True
            elif x >= 1530 and y < 301:
                m_stamp[y, x] = True
            elif y >= 810:
                m_bottom[y, x] = True
            elif x < 950:
                m_left[y, x] = True
            else:
                m_right[y, x] = True

    masks = [m_title, m_sub, m_stamp, m_left, m_right, m_bottom]
    boxes = []
    for idx, m in enumerate(masks):
        ys, xs = np.where(m)
        pad = 0 if idx in [2, 4] else 1
        b = {
            "x": int(xs.min()) - pad,
            "y": int(ys.min()) - pad,
            "width": int(xs.max() - xs.min() + 1) + 2*pad,
            "height": int(ys.max() - ys.min() + 1) + 2*pad
        }
        boxes.append(b)

    elements = [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "TITLE: TRAP 1: The Letter 'H'",
            "type": "text",
            "colorMode": "auto",
            "region": boxes[0],
            "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4440}
        },
        {
            "id": "el-02-subtitle",
            "sequence": 2,
            "label": "SUBTITLE: Both words start with H, opposite rules!",
            "type": "text",
            "colorMode": "auto",
            "region": boxes[1],
            "reveal": {"direction": "left_to_right", "startMs": 5190, "durationMs": 5360}
        },
        {
            "id": "el-03-left-card",
            "sequence": 3,
            "label": "CARD: a house (/haʊs/ -> Consonant Sound)",
            "type": "card",
            "colorMode": "wash",
            "region": boxes[3],
            "reveal": {"direction": "left_to_right", "startMs": 11150, "durationMs": 8530}
        },
        {
            "id": "el-04-stamp-badge",
            "sequence": 4,
            "label": "BADGE: Silent H Warning",
            "type": "box",
            "colorMode": "auto",
            "region": boxes[2],
            "reveal": {"direction": "top_to_bottom", "startMs": 20280, "durationMs": 2500}
        },
        {
            "id": "el-05-right-card",
            "sequence": 5,
            "label": "CARD: an hour (/ˈaʊər/ -> Silent H & /aʊ/)",
            "type": "card",
            "colorMode": "wash",
            "region": boxes[4],
            "reveal": {"direction": "left_to_right", "startMs": 22780, "durationMs": 9840}
        },
        {
            "id": "el-06-bottom-summary",
            "sequence": 6,
            "label": "SUMMARY: Trust your ears, not your eyes!",
            "type": "card",
            "colorMode": "wash",
            "region": boxes[5],
            "reveal": {"direction": "left_to_right", "startMs": 32870, "durationMs": 4000}
        }
    ]

    data = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 38870,
        "globalStartMs": 0,
        "globalEndMs": 38870,
        "fps": 60,
        "elements": elements
    }
    
    ann_path = scene_dir / "scene_02.annotation.json"
    ann_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Scene 02 Micro-Atomic Annotation saved: {ann_path}")
    draw_preview(img_path, elements, scene_dir / "scene_02_regions.png")

def build_scene_03():
    img_path = IMAGES_DIR / "scene_03.png"
    scene_dir = SCENES_DIR / "scene_03"
    shutil.copy(img_path, scene_dir / "scene_03.png")
    
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    m_hdr = np.zeros_like(ink)
    m_umb_card = np.zeros_like(ink)
    m_tip = np.zeros_like(ink)
    m_uni_card = np.zeros_like(ink)
    m_umb_snd = np.zeros_like(ink)
    m_uni_snd = np.zeros_like(ink)

    for i in range(1, num_labels):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 250:
            m_hdr |= comp
        elif cy > 750:
            if cx < 900:
                m_umb_snd |= comp
            else:
                m_uni_snd |= comp
        elif 350 <= cy <= 650 and 680 <= cx <= 1250:
            m_tip |= comp
        elif cx < 680:
            m_umb_card |= comp
        else:
            m_uni_card |= comp

    elements = [
        {
            "id": "el-01-header",
            "sequence": 1,
            "label": "TITLE: TRAP 2: The Letter 'U'",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_hdr, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 3760}
        },
        {
            "id": "el-02-umbrella-card",
            "sequence": 2,
            "label": "CARD: an umbrella (/ʌmˈbrelə/)",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_umb_card, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 4860, "durationMs": 5600}
        },
        {
            "id": "el-03-umbrella-sound",
            "sequence": 3,
            "label": "SOUND: /ʌ/ (Vowel Sound) -> Use AN ✓",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_umb_snd, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 10710, "durationMs": 2560}
        },
        {
            "id": "el-04-center-tip",
            "sequence": 4,
            "label": "PRO TIP: 'U' sounds like 'YOU'?",
            "type": "box",
            "colorMode": "auto",
            "region": get_bounding_box(m_tip, pad=2),
            "reveal": {"direction": "top_to_bottom", "startMs": 13870, "durationMs": 5560}
        },
        {
            "id": "el-05-university-card",
            "sequence": 5,
            "label": "CARD: a university (/juː/)",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_uni_card, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 19680, "durationMs": 3920}
        },
        {
            "id": "el-06-university-sound",
            "sequence": 6,
            "label": "SOUND: /j/ (Semi-consonant) -> Use A!",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_uni_snd, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 23850, "durationMs": 7850}
        }
    ]

    data = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 33700,
        "globalStartMs": 0,
        "globalEndMs": 33700,
        "fps": 60,
        "elements": elements
    }
    
    ann_path = scene_dir / "scene_03.annotation.json"
    ann_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Scene 03 Micro-Atomic Annotation saved: {ann_path}")
    draw_preview(img_path, elements, scene_dir / "scene_03_regions.png")

def build_scene_04():
    img_path = IMAGES_DIR / "scene_04.png"
    scene_dir = SCENES_DIR / "scene_04"
    shutil.copy(img_path, scene_dir / "scene_04.png")
    
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink = gray < 240
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(ink.astype(np.uint8)*255, connectivity=8)

    m_hdr = np.zeros_like(ink)
    m_q1 = np.zeros_like(ink)
    m_q2 = np.zeros_like(ink)
    m_q3 = np.zeros_like(ink)
    m_gold = np.zeros_like(ink)

    for i in range(1, num_labels):
        cx, cy = centroids[i]
        comp = (labels == i)
        if cy < 175:
            m_hdr |= comp
        elif 175 <= cy < 298:
            m_q1 |= comp
        elif 298 <= cy < 405:
            m_q2 |= comp
        elif 405 <= cy < 525:
            m_q3 |= comp
        else:
            m_gold |= comp

    elements = [
        {
            "id": "el-01-header",
            "sequence": 1,
            "label": "QUIZ: 3-SECOND CHALLENGE!",
            "type": "text",
            "colorMode": "auto",
            "region": get_bounding_box(m_hdr, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 500, "durationMs": 4080}
        },
        {
            "id": "el-02-quiz-q1",
            "sequence": 2,
            "label": "Q1: 1. [AN] honest person (/ɒnɪst/)",
            "type": "text",
            "colorMode": "wash",
            "region": get_bounding_box(m_q1, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 5180, "durationMs": 21630}
        },
        {
            "id": "el-03-quiz-q2",
            "sequence": 3,
            "label": "Q2: 2. [A] dog (/d/ Consonant)",
            "type": "text",
            "colorMode": "wash",
            "region": get_bounding_box(m_q2, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 27410, "durationMs": 5080}
        },
        {
            "id": "el-04-quiz-q3",
            "sequence": 4,
            "label": "Q3: 3. [AN] orange (/ɔː/ Vowel)",
            "type": "text",
            "colorMode": "wash",
            "region": get_bounding_box(m_q3, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 32740, "durationMs": 4440}
        },
        {
            "id": "el-05-golden-rule",
            "sequence": 5,
            "label": "SUMMARY: ★ GOLDEN RULE BOX ★",
            "type": "card",
            "colorMode": "wash",
            "region": get_bounding_box(m_gold, pad=2),
            "reveal": {"direction": "left_to_right", "startMs": 37780, "durationMs": 10490}
        }
    ]

    data = {
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 50270,
        "globalStartMs": 0,
        "globalEndMs": 50270,
        "fps": 60,
        "elements": elements
    }
    
    ann_path = scene_dir / "scene_04.annotation.json"
    ann_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Scene 04 Micro-Atomic Annotation saved: {ann_path}")
    draw_preview(img_path, elements, scene_dir / "scene_04_regions.png")

if __name__ == "__main__":
    print("🚀 Bắt đầu phân rã nguyên tử và sinh file annotation cho 4 scenes...")
    build_scene_01()
    build_scene_02()
    build_scene_03()
    build_scene_04()
    print("✨ Hoàn tất toàn bộ phân vùng!")
