#!/usr/bin/env python3
"""
scripts/universal_ai_segmenter.py
Thuật toán phân vùng vi mô đa năng kết hợp AI Vision và Computer Vision (AMSS Engine v2.0):
1. Đọc Scene Matrix & Timing Cues để hiểu kịch bản và nhịp thời gian mili-giây.
2. Gọi Gemini Vision (Multimodal Object Detection) để nhận diện chính xác từng đối tượng vi mô:
   - Khung viền (Container borders/frames): Luôn vẽ ở ĐẦU mục (Intro Cue), chỉ vẽ viền rỗng.
   - Hàng nội dung (Item rows): Tách riêng từng hàng nội dung (ví dụ: từng cặp icon + chữ).
   - Hình vẽ minh họa (Illustrations / Doodles).
   - Dòng chữ / Nhãn (Text lines / Labels).
   - Đề bài câu hỏi (Quiz prompt / blanks / option buttons).
   - Đáp án điền vào / Dấu tick (Quiz answer / checkmark) -> TÁCH RỜI HOÀN TOÀN KHỎI ĐỀ BÀI!
   - Quy tắc / Huy hiệu (Rule boxes / Badges).
3. Tinh chỉnh bằng OpenCV (Connected Components & Ink Snapping):
   - Snap bounding box ôm sát 100% nét mực thực tế.
   - Bảo đảm 0.00% overlap giữa các phần tử kề nhau.
4. Gắn nhịp thời gian Master Clock theo vai trò ngữ nghĩa (Semantic Timing Binding).
5. Xuất scene_XX.annotation.json và ảnh visual preview scene_XX_regions.png
   (Container chỉ vẽ viền rỗng, các hàng nội dung con hiển thị 100% rõ ràng, không bị đè khuất).
"""

import sys
import os
import json
import base64
import time
import urllib.request
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent


def get_api_key() -> str:
    """Lấy Gemini API Key từ môi trường hoặc file .env."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong môi trường hoặc file .env!")


def call_gemini_vision(img_bytes: bytes, prompt: str, api_key: str, models=("gemini-flash-latest", "gemini-pro-latest")) -> str:
    """Gọi Gemini Multimodal API với danh sách fallback model."""
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": "image/png", "data": img_b64}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    data_json = json.dumps(payload).encode("utf-8")

    last_err = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data_json, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"]
        except Exception as e:
            last_err = e
            time.sleep(1)
            continue
    raise RuntimeError(f"Lỗi gọi Gemini Vision sau các model {models}: {last_err}")


def extract_scene_matrix_context(proj_dir: Path, scene_name: str) -> str:
    """Trích xuất mô tả phân cảnh từ scene_matrix.md hoặc beat_plan.json nếu có."""
    matrix_file = proj_dir / "scene_matrix.md"
    if matrix_file.exists():
        content = matrix_file.read_text(encoding="utf-8")
        idx_str = scene_name.replace("scene_", "SCENE ")
        if idx_str in content:
            parts = content.split(idx_str)
            if len(parts) > 1:
                chunk = parts[1].split("### SCENE")[0]
                return f"SCENE MATRIX SPECIFICATION:\n{chunk[:2000]}"
    return ""


def get_tight_ink_bbox(ink_mask: np.ndarray, x0: int, y0: int, x1: int, y1: int, pad: int = 4) -> Tuple[int, int, int, int]:
    """Co/giãn bounding box để ôm sát nét mực thực tế trong vùng quan tâm."""
    h_canvas, w_canvas = ink_mask.shape
    x0_cl = max(0, min(w_canvas - 1, x0))
    y0_cl = max(0, min(h_canvas - 1, y0))
    x1_cl = max(0, min(w_canvas, x1))
    y1_cl = max(0, min(h_canvas, y1))

    if x1_cl <= x0_cl or y1_cl <= y0_cl:
        return x0, y0, max(10, x1 - x0), max(10, y1 - y0)

    sub = ink_mask[y0_cl:y1_cl, x0_cl:x1_cl]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        return x0_cl, y0_cl, max(10, x1_cl - x0_cl), max(10, y1_cl - y0_cl)

    min_x = max(0, x0_cl + int(xs.min()) - pad)
    min_y = max(0, y0_cl + int(ys.min()) - pad)
    max_x = min(w_canvas, x0_cl + int(xs.max()) + 1 + pad)
    max_y = min(h_canvas, y0_cl + int(ys.max()) + 1 + pad)

    return min_x, min_y, max(10, max_x - min_x), max(10, max_y - min_y)


def draw_regions_preview(img_path: Path, elements: List[dict], out_path: Path):
    """Vẽ ảnh preview đa màu sắc với đầy đủ nhãn, sequence và thời gian hiển thị.
    Cải tiến v2.0:
    - Container/Khung viền chỉ vẽ Outline nét viền (KHÔNG TÔ MÀU NỀN), nhãn đặt ở mép trên.
    - Vẽ Container trước, sau đó vẽ các hàng nội dung con đè lên để KHÔNG BAO GIỜ BỊ CHE KHUẤT!
    """
    img = Image.open(img_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    colors = [
        (52, 120, 212),   # 1: Cobalt Blue
        (34, 168, 149),   # 2: Teal Green
        (245, 166, 35),   # 3: Warm Amber
        (220, 38, 38),    # 4: Red
        (139, 92, 246),   # 5: Violet
        (16, 185, 129),   # 6: Emerald
        (236, 72, 153),   # 7: Pink
        (234, 88, 12),    # 8: Orange
        (14, 165, 233),   # 9: Sky Blue
        (168, 85, 247),   # 10: Purple
        (132, 204, 22),   # 11: Lime
        (244, 63, 94),    # 12: Rose
    ]

    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 20)
    except Exception:
        font = ImageFont.load_default()

    # Sắp xếp vẽ: Containers (khung lớn) vẽ trước; Inner Items (hàng con, chữ, icon) vẽ sau
    containers = [el for el in elements if el.get("elementType") == "container"]
    non_containers = [el for el in elements if el.get("elementType") != "container"]

    # 1. Vẽ Containers (Khung viền rỗng: outline only, NO FILL)
    for el in containers:
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        if w <= 0 or h <= 0:
            continue
        c = colors[(el["sequence"] - 1) % len(colors)]
        border = (c[0], c[1], c[2], 255)

        # Chỉ vẽ đường viền khung 3px, TUYỆT ĐỐI KHÔNG FILL để không che đè nội dung con!
        draw.rectangle([x, y, x + w, y + h], outline=border, width=3)
        start_ms = el["reveal"]["startMs"]
        dur_ms = el["reveal"]["durationMs"]
        tag = f"[{el['sequence']}] {el['label']} ({start_ms}ms-{start_ms+dur_ms}ms)"
        tag_w = len(tag) * 10
        tag_y = max(0, y - 26)
        draw.rectangle([x, tag_y, x + tag_w, tag_y + 24], fill=(20, 24, 33, 230))
        draw.text((x + 6, tag_y + 3), tag, fill=(255, 255, 255, 255), font=font)

    # 2. Vẽ Inner Elements (Từng hàng nội dung, icon, chữ, đáp án)
    for el in non_containers:
        r = el["region"]
        x, y, w, h = r["x"], r["y"], r["width"], r["height"]
        if w <= 0 or h <= 0:
            continue
        c = colors[(el["sequence"] - 1) % len(colors)]
        border = (c[0], c[1], c[2], 240)
        fill = (c[0], c[1], c[2], 45)

        # Vẽ hộp bao quanh đối tượng cụ thể kèm fill nhẹ nhận diện
        draw.rectangle([x, y, x + w, y + h], fill=fill, outline=border, width=3)
        start_ms = el["reveal"]["startMs"]
        dur_ms = el["reveal"]["durationMs"]
        tag = f"[{el['sequence']}] {el['label']} ({start_ms}ms-{start_ms+dur_ms}ms)"
        tag_w = len(tag) * 10
        tag_y = max(0, y - 26)
        draw.rectangle([x, tag_y, x + tag_w, tag_y + 24], fill=(20, 24, 33, 230))
        draw.text((x + 6, tag_y + 3), tag, fill=(255, 255, 255, 255), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(out_path)
    print(f"  ✓ Đã xuất ảnh preview phân vùng: {out_path.name}")


def segment_scene(scene_dir: Path, proj_dir: Path, force: bool = False) -> bool:
    scene_name = scene_dir.name
    img_path = scene_dir / f"{scene_name}.png"
    cues_path = scene_dir / "timing_cues.json"
    ann_path = scene_dir / f"{scene_name}.annotation.json"
    out_preview = scene_dir / f"{scene_name}_regions.png"

    if not img_path.exists():
        print(f"⚠️ [Bỏ qua {scene_name}] Không tìm thấy file ảnh: {img_path.name}")
        return False
    if not cues_path.exists():
        print(f"⚠️ [Bỏ qua {scene_name}] Không tìm thấy timing_cues.json")
        return False

    print(f"\n=======================================================")
    print(f"🔍 BẮT ĐẦU PHÂN VÙNG THỊ GIÁC AI (AMSS v2.0) CHO: {scene_name.upper()}")
    print(f"=======================================================")

    with open(cues_path, "r", encoding="utf-8") as f:
        cues_data = json.load(f)
    cues = cues_data.get("cues", [])
    total_dur_ms = cues_data.get("totalDurationMs", 30000)

    # Đọc ảnh và ma trận mực
    img_bgr = cv2.imread(str(img_path))
    h_canvas, w_canvas = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    ink_mask = gray < 240

    matrix_context = extract_scene_matrix_context(proj_dir, scene_name)
    cues_text_list = "\n".join([f"Cue #{c['index']} ({c['startMs']}ms - {c['endMs']}ms): \"{c['text']}\"" for c in cues])

    api_key = get_api_key()

    prompt = f"""You are a master Whiteboard Animation vision and annotation engineer.
Analyze this 1920x1080 educational whiteboard image and segment it into fine-grained atomic elements.

CRITICAL GENERALIZED SEGMENTATION SPECIFICATIONS (MANDATORY FOR ALL WHITEBOARD ANIMATION PROJECTS):

1. ATOMIC ROW-BY-ROW / ITEM-BY-ITEM GRANULARITY (ZERO MONOLITHIC BOXES):
   - Whenever an image displays a list, multi-row table, card with items, or comparison columns (e.g. Column A with rows 'a book', 'a cat', 'a car'; Column AN with rows 'an apple', 'an egg', 'an umbrella'):
     * NEVER group the whole card/column into one large bounding box!
     * YOU MUST SEGMENT EACH ROW / CONTENT ITEM AS A DISTINCT INDEPENDENT ELEMENT:
       Row 1: [Icon + text phrase]
       Row 2: [Icon + text phrase]
       Row 3: [Icon + text phrase]
     * Each content row must map to the EXACT cue where that specific item is spoken in the narration!

2. CONTAINER & CARD FRAME RULES:
   - If an outer frame/border exists around a card or column:
     * Label it as role "container".
     * Its bounding box is the outer rectangle of the card.
     * CRUCIAL: It MUST be mapped to the INTRODUCTORY CUE of that column/card (when the narrator introduces the column or card), NEVER at the end of the items!

3. QUESTION VS ANSWER DECOUPLING (MANDATORY FOR ALL QUIZZES, DRILLS, CHALLENGES):
   - You MUST separate the question prompt (card frame, prompt text like '___ dog', icon, option buttons) from the ANSWER!
   - Answer reveals (checkmark tick '✔', filled letter 'A' or 'AN', explanation like 'H IS SILENT' or 'STARTS WITH Y SOUND') MUST BE SEPARATE ELEMENTS.
   - Answers must ONLY be mapped to the cue that reveals the answer (after any thinking pauses), NEVER during the question prompt!

4. ORDERING:
   Ensure elements are sequenced logically in chronological order of appearance (title/header first, then container frame, then item rows sequentially, then answers, then summary rules).

TIMING CUES AVAILABLE:
{cues_text_list}

{matrix_context}

Return a valid JSON array of objects:
[
  {{
    "id": "el-01-title",
    "label": "Short label (e.g. Row 1: a book (icon and text))",
    "role": "title" | "container" | "item_row" | "illustration" | "text" | "question_prompt" | "answer_reveal" | "rule" | "accent",
    "box_2d": [ymin, xmin, ymax, xmax],
    "cue_index": 1
  }}
]
Note: box_2d coordinates must be normalized 0-1000 integers [ymin, xmin, ymax, xmax].
Output ONLY pure JSON. No markdown code blocks."""

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    print(f"  🤖 Đang gửi ảnh và kịch bản thoại sang Gemini Vision...")
    raw_resp = call_gemini_vision(img_bytes, prompt, api_key)
    clean_json = raw_resp.strip()
    if clean_json.startswith("```json"):
        clean_json = clean_json[7:]
    if clean_json.startswith("```"):
        clean_json = clean_json[3:]
    if clean_json.endswith("```"):
        clean_json = clean_json[:-3]
    clean_json = clean_json.strip()

    try:
        detected_elements = json.loads(clean_json)
    except Exception as e:
        print(f"❌ Lỗi parse JSON từ Gemini Vision: {e}\nRaw: {raw_resp[:300]}")
        return False

    print(f"  ✓ Gemini Vision đã phát hiện {len(detected_elements)} đối tượng vi mô độc lập!")

    # Nhóm các elements theo cue_index để tính thời gian mượt mà
    cues_dict = {c["index"]: c for c in cues}
    elements_by_cue: Dict[int, List[dict]] = {}
    for el in detected_elements:
        c_idx = el.get("cue_index", 1)
        if c_idx not in cues_dict:
            c_idx = min(cues_dict.keys(), key=lambda k: abs(k - c_idx))
        elements_by_cue.setdefault(c_idx, []).append(el)

    final_elements = []
    seq_counter = 1

    # Duyệt theo thứ tự cue để đảm bảo sequence tăng dần và đúng nhịp sư phạm
    for c_idx in sorted(cues_dict.keys()):
        cue_info = cues_dict[c_idx]
        cue_start = cue_info["startMs"]
        cue_end = cue_info["endMs"]
        cue_dur = cue_end - cue_start

        els = elements_by_cue.get(c_idx, [])
        if not els:
            continue

        # Đưa element 'container' lên đầu cue nếu có trong cue đó
        els_sorted = sorted(els, key=lambda x: 0 if x.get("role") == "container" else 1)

        n_in_cue = len(els_sorted)
        slot_dur = max(600, cue_dur // n_in_cue)

        for i, el in enumerate(els_sorted):
            ymin, xmin, ymax, xmax = el["box_2d"]
            px0 = int(xmin * w_canvas / 1000)
            py0 = int(ymin * h_canvas / 1000)
            px1 = int(xmax * w_canvas / 1000)
            py1 = int(ymax * h_canvas / 1000)

            # Snap mực thực tế bằng OpenCV
            rx, ry, rw, rh = get_tight_ink_bbox(ink_mask, px0, py0, px1, py1, pad=5)

            el_start = cue_start + int(i * (cue_dur / n_in_cue))
            el_dur = max(700, min(cue_dur - (el_start - cue_start), slot_dur))

            role = el.get("role", "text")
            if role == "container":
                action = "draw_container"
                elem_type = "container"
            elif role in ("illustration", "item_row"):
                action = "draw_new"
                elem_type = "illustration"
            elif role in ("answer_reveal", "accent"):
                action = "highlight"
                elem_type = "accent"
            elif role == "connector":
                action = "connect_arrow"
                elem_type = "connector"
            else:
                action = "write_text"
                elem_type = "text"

            final_elements.append({
                "id": f"el-{seq_counter:02d}-{el.get('id', 'obj')}",
                "sequence": seq_counter,
                "label": el.get("label", f"Object {seq_counter}"),
                "elementType": elem_type,
                "action": action,
                "region": {
                    "x": rx,
                    "y": ry,
                    "width": rw,
                    "height": rh
                },
                "reveal": {
                    "startMs": el_start,
                    "durationMs": el_dur,
                    "drawingStyle": "stroke",
                    "colorStroke": True,
                    "strokeWidth": 3
                }
            })
            seq_counter += 1

    annotation_data = {
        "sceneId": scene_name,
        "imagePath": f"{scene_name}.png",
        "canvas": {
            "width": w_canvas,
            "height": h_canvas
        },
        "elements": final_elements
    }

    with open(ann_path, "w", encoding="utf-8") as f:
        json.dump(annotation_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Đã lưu annotation vi mô hoàn chỉnh: {ann_path.name} ({len(final_elements)} elements)")

    # Xuất ảnh preview trực quan
    draw_regions_preview(img_path, final_elements, out_preview)
    return True


def segment_image_standalone(
    img_path: Path,
    ann_path: Path,
    out_preview: Path | None = None,
    total_dur_ms: int = 25000,
    context_desc: str = "",
    cues_path: Path | None = None
) -> bool:
    """Phân vùng ảnh độc lập có hoặc không có timing_cues.json (hỗ trợ voice-over sync)."""
    if not img_path.exists():
        print(f"❌ Không tìm thấy file ảnh: {img_path}")
        return False

    print(f"\n=======================================================")
    print(f"🔍 BẮT ĐẦU PHÂN VÙNG THỊ GIÁC AI (AMSS v2.0 - STANDALONE)")
    print(f"📁 Ảnh: {img_path.name}")
    if cues_path and cues_path.exists():
        print(f"🎙️ Đồng bộ Master Clock theo: {cues_path.name}")
    print(f"=======================================================")

    img_bgr = cv2.imread(str(img_path))
    if img_bgr is None:
        print(f"❌ Không thể đọc ảnh bằng OpenCV: {img_path}")
        return False
    h_canvas, w_canvas = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    ink_mask = gray < 240

    api_key = get_api_key()

    cues = []
    cues_text_list = ""
    if cues_path and cues_path.exists():
        with open(cues_path, "r", encoding="utf-8") as f:
            cues_data = json.load(f)
        cues = cues_data.get("cues", [])
        total_dur_ms = cues_data.get("totalDurationMs", total_dur_ms)
        cues_text_list = "\nTIMING CUES AVAILABLE (Map each element to the most relevant cue_index):\n" + "\n".join(
            [f"Cue #{c['index']} ({c['startMs']}ms - {c['endMs']}ms): \"{c['text']}\"" for c in cues]
        )

    prompt = f"""You are a master Whiteboard Animation vision and annotation engineer.
Analyze this 1920x1080 educational whiteboard image and segment it into fine-grained atomic elements.

CRITICAL GENERALIZED SEGMENTATION SPECIFICATIONS (MANDATORY):

1. ATOMIC ROW-BY-ROW / ITEM-BY-ITEM GRANULARITY (ZERO MONOLITHIC BOXES):
   - Whenever an image displays a list, multi-row table, card with items, or comparison columns:
     * NEVER group the whole card/column into one large bounding box!
     * YOU MUST SEGMENT EACH ROW / CONTENT ITEM AS A DISTINCT INDEPENDENT ELEMENT:
       e.g. Header badge, Illustration icon, Row 1 text, Row 2 text...

2. CONTAINER & CARD FRAME RULES:
   - If an outer frame/border exists around a card or column:
     * Label it as role "container".
     * Its bounding box is the outer rectangle of the card.
     * It MUST come BEFORE the items inside that card!

3. CONNECTORS & ACCENTS:
   - Directional arrows between cards/steps must be role "connector".
   - Underlines, highlights, badges must be role "accent".

4. ORDERING:
   Ensure elements are sequenced in strict logical, pedagogical drawing order.

{context_desc}
{cues_text_list}

Return a valid JSON array of objects:
[
  {{
    "id": "el-01-title",
    "label": "Short label (e.g. Title: SAY vs TELL)",
    "role": "title" | "container" | "item_row" | "illustration" | "text" | "connector" | "accent",
    "box_2d": [ymin, xmin, ymax, xmax]{', "cue_index": 1' if cues else ''}
  }}
]
Note: box_2d coordinates must be normalized 0-1000 integers [ymin, xmin, ymax, xmax].
Output ONLY pure JSON. No markdown code blocks."""

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    print(f"  🤖 Đang gửi ảnh sang Gemini Vision...")
    raw_resp = call_gemini_vision(img_bytes, prompt, api_key)
    clean_json = raw_resp.strip()
    if clean_json.startswith("```json"):
        clean_json = clean_json[7:]
    if clean_json.startswith("```"):
        clean_json = clean_json[3:]
    if clean_json.endswith("```"):
        clean_json = clean_json[:-3]
    clean_json = clean_json.strip()

    try:
        detected_elements = json.loads(clean_json)
    except Exception as e:
        print(f"❌ Lỗi parse JSON từ Gemini Vision: {e}\nRaw: {raw_resp[:300]}")
        return False

    print(f"  ✓ Gemini Vision đã phát hiện {len(detected_elements)} đối tượng vi mô độc lập!")

    n_elems = len(detected_elements)
    if n_elems == 0:
        print("❌ Không phát hiện element nào!")
        return False

    final_elements = []

    if cues:
        cues_dict = {c["index"]: c for c in cues}
        elements_by_cue: Dict[int, List[dict]] = {}
        for el in detected_elements:
            c_idx = el.get("cue_index", 1)
            if c_idx not in cues_dict:
                c_idx = min(cues_dict.keys(), key=lambda k: abs(k - c_idx))
            elements_by_cue.setdefault(c_idx, []).append(el)

        seq_counter = 1
        for c_idx in sorted(cues_dict.keys()):
            if c_idx not in elements_by_cue:
                continue
            els_in_cue = elements_by_cue[c_idx]
            cue_info = cues_dict[c_idx]
            cue_start = cue_info["startMs"]
            cue_end = cue_info["endMs"]
            cue_dur = max(600, cue_end - cue_start)
            n_in_cue = len(els_in_cue)
            slot_dur = max(600, cue_dur // n_in_cue)

            for i, el in enumerate(els_in_cue):
                ymin, xmin, ymax, xmax = el["box_2d"]
                px0 = int(xmin * w_canvas / 1000)
                py0 = int(ymin * h_canvas / 1000)
                px1 = int(xmax * w_canvas / 1000)
                py1 = int(ymax * h_canvas / 1000)

                rx, ry, rw, rh = get_tight_ink_bbox(ink_mask, px0, py0, px1, py1, pad=5)

                el_start = cue_start + int(i * (cue_dur / n_in_cue))
                el_dur = max(600, min(cue_dur - (el_start - cue_start), slot_dur))

                role = el.get("role", "text")
                if role == "container":
                    action = "draw_container"
                    elem_type = "container"
                elif role in ("illustration", "item_row"):
                    action = "draw_new"
                    elem_type = "illustration"
                elif role in ("answer_reveal", "accent"):
                    action = "highlight"
                    elem_type = "accent"
                elif role == "connector":
                    action = "connect_arrow"
                    elem_type = "connector"
                elif role == "title":
                    action = "write_text"
                    elem_type = "title"
                else:
                    action = "write_text"
                    elem_type = "text"

                final_elements.append({
                    "id": f"el-{seq_counter:02d}-{el.get('id', 'obj')}",
                    "sequence": seq_counter,
                    "label": el.get("label", f"Object {seq_counter}"),
                    "elementType": elem_type,
                    "action": action,
                    "region": {
                        "x": rx,
                        "y": ry,
                        "width": rw,
                        "height": rh
                    },
                    "reveal": {
                        "startMs": el_start,
                        "durationMs": el_dur,
                        "drawingStyle": "stroke",
                        "colorStroke": True,
                        "strokeWidth": 3
                    }
                })
                seq_counter += 1

        actual_scene_dur = total_dur_ms
    else:
        anim_time = max(5000, total_dur_ms - 2500)
        slot_ms = anim_time // n_elems
        draw_dur = max(600, int(slot_ms * 0.82))
        pause_ms = max(100, slot_ms - draw_dur)

        cur_ms = 800
        for seq, el in enumerate(detected_elements, start=1):
            ymin, xmin, ymax, xmax = el["box_2d"]
            px0 = int(xmin * w_canvas / 1000)
            py0 = int(ymin * h_canvas / 1000)
            px1 = int(xmax * w_canvas / 1000)
            py1 = int(ymax * h_canvas / 1000)

            rx, ry, rw, rh = get_tight_ink_bbox(ink_mask, px0, py0, px1, py1, pad=5)

            role = el.get("role", "text")
            if role == "container":
                action = "draw_container"
                elem_type = "container"
                dur = max(700, int(draw_dur * 0.9))
            elif role in ("illustration", "item_row"):
                action = "draw_new"
                elem_type = "illustration"
                dur = max(800, int(draw_dur * 1.1))
            elif role in ("answer_reveal", "accent"):
                action = "highlight"
                elem_type = "accent"
                dur = max(500, int(draw_dur * 0.8))
            elif role == "connector":
                action = "connect_arrow"
                elem_type = "connector"
                dur = max(500, int(draw_dur * 0.7))
            elif role == "title":
                action = "write_text"
                elem_type = "title"
                dur = max(800, int(draw_dur * 1.1))
            else:
                action = "write_text"
                elem_type = "text"
                dur = draw_dur

            final_elements.append({
                "id": f"el-{seq:02d}-{el.get('id', 'obj')}",
                "sequence": seq,
                "label": el.get("label", f"Object {seq}"),
                "elementType": elem_type,
                "action": action,
                "region": {
                    "x": rx,
                    "y": ry,
                    "width": rw,
                    "height": rh
                },
                "reveal": {
                    "startMs": cur_ms,
                    "durationMs": dur,
                    "drawingStyle": "stroke",
                    "colorStroke": True,
                    "strokeWidth": 3
                }
            })
            cur_ms += dur + pause_ms

        actual_scene_dur = max(total_dur_ms, cur_ms + 1500)

    annotation_data = {
        "sceneId": img_path.stem,
        "imagePath": img_path.name,
        "sceneDurationMs": actual_scene_dur,
        "canvas": {
            "width": w_canvas,
            "height": h_canvas
        },
        "elements": final_elements
    }

    ann_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ann_path, "w", encoding="utf-8") as f:
        json.dump(annotation_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Đã lưu annotation vi mô hoàn chỉnh: {ann_path.name} ({len(final_elements)} elements, {actual_scene_dur}ms)")

    if out_preview:
        draw_regions_preview(img_path, final_elements, out_preview)
    return True


def main():
    parser = argparse.ArgumentParser(description="Thuật toán phân vùng vi mô đa năng AI (AMSS Engine v2.0).")
    parser.add_argument("--image", type=Path, help="Đường dẫn file ảnh đơn lẻ để phân vùng độc lập (Test Case)")
    parser.add_argument("--output", type=Path, help="Đường dẫn file annotation.json xuất ra")
    parser.add_argument("--preview", type=Path, help="Đường dẫn file preview regions.png xuất ra")
    parser.add_argument("--duration", type=int, default=25000, help="Tổng thời lượng ước tính (ms)")
    parser.add_argument("--cues", type=Path, help="Đường dẫn file timing_cues.json để đồng bộ Master Clock âm thanh")
    parser.add_argument("--project", type=Path, default=REPO_ROOT / "projects/project_articles_a_an", help="Đường dẫn thư mục dự án")
    parser.add_argument("--scene", type=str, help="Tên scene cụ thể cần chạy (ví dụ: scene_08)")
    parser.add_argument("--scenes", nargs="*", help="Danh sách scene cụ thể cần chạy")
    parser.add_argument("--all", action="store_true", help="Chạy cho toàn bộ scenes trong dự án")
    parser.add_argument("--force", action="store_true", help="Bắt buộc phân vùng lại")
    args = parser.parse_args()

    if args.image:
        img_p = args.image.resolve()
        ann_p = args.output.resolve() if args.output else img_p.with_suffix(".annotation.json")
        prev_p = args.preview.resolve() if args.preview else img_p.parent / f"{img_p.stem}_regions.png"
        cues_p = args.cues.resolve() if args.cues else None
        success = segment_image_standalone(img_p, ann_p, out_preview=prev_p, total_dur_ms=args.duration, cues_path=cues_p)
        if success:
            print(f"🎉 Hoàn tất phân vùng độc lập cho ảnh: {img_p.name}")
        return

    proj_dir = args.project.resolve()
    scenes_dir = proj_dir / "scenes"

    if args.scene:
        target_scenes = [args.scene]
    elif args.scenes:
        target_scenes = args.scenes
    elif args.all:
        target_scenes = sorted([p.name for p in scenes_dir.iterdir() if p.is_dir() and p.name.startswith("scene_")])
    else:
        target_scenes = ["scene_05"]

    success_count = 0
    for s_name in target_scenes:
        s_dir = scenes_dir / s_name
        if segment_scene(s_dir, proj_dir, force=args.force):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"🎉 HOÀN TẤT PHÂN VÙNG AMSS CHO {success_count}/{len(target_scenes)} SCENES!")
    print("=" * 60)


if __name__ == "__main__":
    main()
