#!/usr/bin/env python3
"""
scripts/subtitle_styler.py
Bộ công cụ tạo kiểu & kết xuất phụ đề động cao cấp cho Whiteboard Animation.
Hỗ trợ chuyển đổi từ SRT sang ASS (Advanced SubStation Alpha) và sinh tham số
kết xuất FFmpeg chuyên nghiệp với các Preset chuẩn mỹ thuật bảng trắng.

Các Preset thẩm mỹ:
1. 'whiteboard_modern' (Mặc định):
   Chữ màu mực đen bút lông #202124, viền hào quang trắng bảo vệ tương phản (Outline=2.5),
   không hộp đen thô kệch, cỡ chữ lớn 28pt sắc nét, tọa độ nằm hoàn hảo trong Subtitle Safe Zone.
2. 'pastel_capsule':
   Viên nang mờ hiện đại màu xanh pastel/xám nhạt, chữ màu xanh navy đậm #1E293B.
3. 'high_contrast':
   Viên nang đen bán trong suốt (alpha 40%), chữ trắng tinh #FFFFFF.
4. 'grammar_focus':
   Nền trắng, chữ đen, làm nổi bật động từ/từ khóa bằng màu cam điểm nhấn #F5A623.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# Bảng quy đổi màu Hex (#RRGGBB) sang ASS Hex (&HAABBGGRR)
def hex_to_ass_color(hex_str: str, alpha: int = 0) -> str:
    """Chuyển đổi #RRGGBB hoặc #RGB sang định dạng màu ASS &HAABBGGRR."""
    clean = hex_str.strip().lstrip("#")
    if len(clean) == 3:
        clean = "".join(c * 2 for c in clean)
    if len(clean) == 6:
        r = int(clean[0:2], 16)
        g = int(clean[2:4], 16)
        b = int(clean[4:6], 16)
        a = max(0, min(255, alpha))
        return f"&H{a:02X}{b:02X}{g:02X}{r:02X}"
    if hex_str.startswith("&H"):
        return hex_str
    return "&H00FFFFFF"


# Danh sách Preset chuẩn quốc tế cho Whiteboard Video
PRESETS: Dict[str, Dict[str, Any]] = {
    "whiteboard_modern": {
        "name": "whiteboard_modern",
        "description": "Chữ đen mực bút dạ, viền hào quang trắng nhẹ, không hộp nền, chuẩn mỹ thuật bảng trắng",
        "font_name": "Montserrat, Arial, Helvetica, DejaVu Sans",
        "font_size": 28,
        "bold": True,
        "italic": False,
        "primary_color": "&H00242120",      # Deep marker black #202124
        "secondary_color": "&H0023A6F5",    # Accent Orange #F5A623
        "outline_color": "&H00FFFFFF",      # Pure White #FFFFFF
        "outline_width": 2.5,
        "back_color": "&H00000000",         # Trong suốt hoàn toàn
        "border_style": 1,                  # 1 = Outline + Drop Shadow
        "shadow": 1.0,
        "alignment": 2,                     # 2 = Bottom Center
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,                     # Nằm an toàn trong Subtitle Zone (Y: 960-1030)
        "max_chars_per_line": 42
    },
    "pastel_capsule": {
        "name": "pastel_capsule",
        "description": "Viên nang nền pastel mờ hiện đại, chữ xanh đen navy",
        "font_name": "Arial Rounded MT Bold, Montserrat, Arial",
        "font_size": 26,
        "bold": True,
        "italic": False,
        "primary_color": "&H003B291E",      # Dark navy #1E293B
        "secondary_color": "&H0023A6F5",    # Accent Orange
        "outline_color": "&H00FFFFFF",
        "outline_width": 0.0,
        "back_color": "&H4DF8F4F0",         # Pastel gray-blue mờ (alpha ~30%)
        "border_style": 3,                  # 3 = Opaque/Translucent Bounding Box
        "shadow": 0.0,
        "alignment": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 40,
        "max_chars_per_line": 42
    },
    "high_contrast": {
        "name": "high_contrast",
        "description": "Viên nang đen mờ bán trong suốt, chữ trắng độ tương phản cao",
        "font_name": "Montserrat, Arial, DejaVu Sans",
        "font_size": 26,
        "bold": True,
        "italic": False,
        "primary_color": "&H00FFFFFF",      # Pure White
        "secondary_color": "&H0023A6F5",    # Accent Orange
        "outline_color": "&H00000000",
        "outline_width": 1.0,
        "back_color": "&H66101010",         # Dark semi-transparent box
        "border_style": 3,
        "shadow": 0.0,
        "alignment": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 40,
        "max_chars_per_line": 42
    },
    "classic_closed_caption": {
        "name": "classic_closed_caption",
        "description": "Hộp đen chữ trắng kiểu truyền hình cổ điển",
        "font_name": "Arial",
        "font_size": 20,
        "bold": False,
        "italic": False,
        "primary_color": "&H00FFFFFF",
        "secondary_color": "&H0000FFFF",
        "outline_color": "&H00000000",
        "outline_width": 0.0,
        "back_color": "&H80000000",
        "border_style": 3,
        "shadow": 0.0,
        "alignment": 2,
        "margin_l": 60,
        "margin_r": 60,
        "margin_v": 15,
        "max_chars_per_line": 45
    },
    "whiteboard_flat_capsule": {
        "name": "whiteboard_flat_capsule",
        "description": "Chuẩn Phụ Đề Chính Thức Dự Án: Đen than chì trầm #14171F, kính mờ 75% Smoky Glass, viền Slate, chữ trắng tuyết Be Vietnam Pro Bold (Fit Content)",
        "font_name": "Be Vietnam Pro Bold, Be Vietnam Pro, Arial",
        "font_size": 44,
        "font_size_min": 42,
        "font_size_max": 50,
        "font_weight": 700,
        "bold": True,
        "italic": False,
        "primary_color": "&H00FFFFFF",      # Pure White #FFFFFF
        "accent_color": "#F5A623",          # Amber Gold #F5A623
        "secondary_color": "&H0023A6F5",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#14171F",
        "background_opacity": 0.75,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 16,
        "border_color": "#334155",
        "border_width": 2.0,
        "shadow": 2.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "dynamic_fit",
        "max_width": 1760,
        "max_lines": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,
        "max_chars_per_line": 75
    },
    "dark_slate_obsidian": {
        "name": "dark_slate_obsidian",
        "description": "Chuẩn Chính Thức: Đen than chì trầm #14171F, kính mờ 75% Smoky Glass, viền Slate, chữ Be Vietnam Pro Bold 60pt (1 Hàng Dynamic Fit)",
        "font_name": "Be Vietnam Pro Bold, Be Vietnam Pro, Arial",
        "font_size": 60,
        "font_size_min": 44,
        "font_size_max": 60,
        "font_weight": 700,
        "bold": True,
        "italic": False,
        "primary_color": "&H00FFFFFF",      # Pure White #FFFFFF
        "accent_color": "#F5A623",          # Amber Gold #F5A623
        "secondary_color": "&H0023A6F5",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#14171F",
        "background_opacity": 0.75,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 16,
        "border_color": "#334155",
        "border_width": 2.0,
        "shadow": 2.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "dynamic_fit",
        "max_width": 1840,
        "max_lines": 1,
        "margin_l": 40,
        "margin_r": 40,
        "margin_v": 45,
        "max_chars_per_line": 80
    },
    "midnight_navy_academic": {
        "name": "midnight_navy_academic",
        "description": "Option 2: Xanh navy hoàng gia #0F172A, viền Cyan #38BDF8, chữ trắng ngọc trai, cực kỳ học thuật",
        "font_name": "Nunito Sans, Montserrat, Arial",
        "font_size": 48,
        "font_size_min": 44,
        "font_size_max": 52,
        "font_weight": 600,
        "bold": True,
        "italic": False,
        "primary_color": "&H00FCFAF8",      # Pearl White #F8FAFC
        "accent_color": "#38BDF8",          # Sky Cyan #38BDF8
        "secondary_color": "&H00F8BD38",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#0F172A",
        "background_opacity": 0.98,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 18,
        "border_color": "#38BDF8",
        "border_width": 1.5,
        "shadow": 2.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "full_dock",
        "max_width": 1760,
        "max_lines": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,
        "max_chars_per_line": 75
    },
    "crisp_white_card": {
        "name": "crisp_white_card",
        "description": "Option 3: Trắng sứ #FFFFFF, viền Micro-Stroke #CBD5E1 2px + đổ bóng mềm, chữ đen #0F172A (Notion Clean UI)",
        "font_name": "Nunito Sans, Montserrat, Arial",
        "font_size": 48,
        "font_size_min": 44,
        "font_size_max": 52,
        "font_weight": 600,
        "bold": True,
        "italic": False,
        "primary_color": "&H002A170F",      # Obsidian #0F172A
        "accent_color": "#2563EB",          # Royal Blue #2563EB
        "secondary_color": "&H00EB6325",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#FFFFFF",
        "background_opacity": 1.0,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 18,
        "border_color": "#CBD5E1",
        "border_width": 2.0,
        "shadow": 3.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "full_dock",
        "max_width": 1760,
        "max_lines": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,
        "max_chars_per_line": 75
    },
    "warm_ivory_editorial": {
        "name": "warm_ivory_editorial",
        "description": "Option 4: Nền kem cát ấm #FEF3C7, viền hổ phách, chữ nâu cà phê #292524 (Sổ tay giáo dục dịu mắt)",
        "font_name": "Nunito Sans, Montserrat, Arial",
        "font_size": 48,
        "font_size_min": 44,
        "font_size_max": 52,
        "font_weight": 600,
        "bold": True,
        "italic": False,
        "primary_color": "&H00242529",      # Stone-900 #292524
        "accent_color": "#EA580C",          # Terracotta #EA580C
        "secondary_color": "&H000C58EA",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#FEF3C7",
        "background_opacity": 1.0,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 18,
        "border_color": "#FCD34D",
        "border_width": 2.0,
        "shadow": 2.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "full_dock",
        "max_width": 1760,
        "max_lines": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,
        "max_chars_per_line": 75
    },
    "tech_charcoal_dock": {
        "name": "tech_charcoal_dock",
        "description": "Option 5: Thanh dock than chì #1C2028, viền Blue, chữ xám bạc, nhận diện thương hiệu Blue #3478D4",
        "font_name": "Nunito Sans, Montserrat, Arial",
        "font_size": 48,
        "font_size_min": 44,
        "font_size_max": 52,
        "font_weight": 600,
        "bold": True,
        "italic": False,
        "primary_color": "&H00FBFAF9",      # Gray-50 #F9FAFB
        "accent_color": "#38BDF8",          # Brand Blue
        "secondary_color": "&H00F8BD38",
        "letter_spacing": 0.2,
        "line_height": 1.18,
        "background_mode": "rounded_rect",
        "background_color": "#1C2028",
        "background_opacity": 0.98,
        "background_radius": 22,
        "background_padding_x": 48,
        "background_padding_y": 18,
        "border_color": "#3B82F6",
        "border_width": 1.5,
        "shadow": 2.0,
        "alignment": 5,
        "anchor_x": 960,
        "anchor_y": 980,
        "dock_mode": "full_dock",
        "max_width": 1760,
        "max_lines": 2,
        "margin_l": 80,
        "margin_r": 80,
        "margin_v": 45,
        "max_chars_per_line": 75
    }
}


def build_bezier_capsule_path(cx: int, cy: int, w: int, h: int, r: int = 18) -> str:
    """Tạo mã vẽ đường cong Bézier ASS cho viên nang bo góc."""
    x1 = int(cx - w // 2)
    y1 = int(cy - h // 2)
    x2 = int(cx + w // 2)
    y2 = int(cy + h // 2)
    k = int(round(r * 0.5522847))
    return (
        f"m {x1+r} {y1} "
        f"l {x2-r} {y1} "
        f"b {x2-r+k} {y1} {x2} {y1+r-k} {x2} {y1+r} "
        f"l {x2} {y2-r} "
        f"b {x2} {y2-r+k} {x2-r+k} {y2} {x2-r} {y2} "
        f"l {x1+r} {y2} "
        f"b {x1+r-k} {y2} {x1} {y2-r+k} {x1} {y2-r} "
        f"l {x1} {y1+r} "
        f"b {x1} {y1+r-k} {x1+r-k} {y1} {x1+r} {y1}"
    )


def measure_text_box(text: str, font_size: int = 48) -> Tuple[int, int]:
    """Đo kích thước chiều rộng và chiều cao của đoạn text để bọc viên nang."""
    font = None
    for fp in [
        REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf",
        Path.home() / "Library/Fonts/BeVietnamPro-Bold.ttf",
        REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf",
        Path.home() / "Library/Fonts/NunitoSans-SemiBold.ttf",
        Path("/Library/Fonts/Arial.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    ]:
        if fp.exists():
            try:
                from PIL import ImageFont
                font = ImageFont.truetype(str(fp), font_size)
                break
            except Exception:
                continue

    lines = text.split(r"\N")
    if not font:
        max_len = max(len(ln) for ln in lines)
        return int(max_len * font_size * 0.55), int(len(lines) * font_size * 1.25)

    widths = []
    heights = []
    for ln in lines:
        clean_ln = re.sub(r"\{.*?\}", "", ln)
        bbox = font.getbbox(clean_ln)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    max_w = max(widths) if widths else 400
    total_h = sum(heights) + (len(lines) - 1) * 12 if heights else 50
    return max_w, total_h


def load_subtitle_config(project_path: Optional[Path | str] = None) -> Dict[str, Any]:
    """Tải cấu hình phụ đề từ project.json hoặc trả về cấu hình mặc định chính thức (dark_slate_obsidian)."""
    cfg = dict(PRESETS["dark_slate_obsidian"])

    if project_path:
        p = Path(project_path)
        if p.is_file() and p.name == "project.json":
            json_file = p
        elif p.is_dir() and (p / "project.json").exists():
            json_file = p / "project.json"
        else:
            json_file = None

        if json_file and json_file.exists():
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                sub_data = data.get("settings", {}).get("subtitles", {})
                preset_key = sub_data.get("preset") or sub_data.get("style_preset")
                if preset_key and preset_key in PRESETS:
                    cfg.update(PRESETS[preset_key])
                for k, v in sub_data.items():
                    if k not in ("preset", "style_preset") and v is not None:
                        cfg[k] = v
            except Exception as e:
                print(f"[Cảnh báo Subtitle] Lỗi đọc project.json: {e}, dùng cấu hình mặc định.")

    return cfg


def srt_time_to_ass_time(srt_time: str) -> str:
    """Chuyển đổi định dạng thời gian SRT (00:01:23,456) sang ASS (0:01:23.45)."""
    clean = srt_time.strip().replace(",", ".")
    parts = clean.split(":")
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s_parts = parts[2].split(".")
        s = int(s_parts[0])
        cs = int(s_parts[1][:2]) if len(s_parts) > 1 else 0
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
    return "0:00:00.00"


def parse_srt(srt_text: str) -> List[Dict[str, Any]]:
    """Phân tích nội dung file SRT thành danh sách các sự kiện phụ đề."""
    blocks = re.split(r"\n\s*\n", srt_text.strip())
    events = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        idx_line = lines[0]
        time_line_idx = 1 if re.match(r"^\d+$", idx_line) else 0
        if time_line_idx >= len(lines):
            continue
        time_line = lines[time_line_idx]
        m = re.search(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", time_line)
        if not m:
            continue
        start_srt, end_srt = m.group(1), m.group(2)
        text_lines = lines[time_line_idx + 1:]
        text = " \\N".join(text_lines)
        events.append({
            "start": srt_time_to_ass_time(start_srt),
            "end": srt_time_to_ass_time(end_srt),
            "text": text
        })
    return events


def compile_srt_to_ass(
    srt_path: Path | str,
    ass_path: Path | str,
    config: Optional[Dict[str, Any]] = None,
    canvas_w: int = 1920,
    canvas_h: int = 1080
) -> Path:
    """Biên dịch file SRT sang file ASS với đầy đủ định dạng thẩm mỹ chuyên nghiệp."""
    srt_p = Path(srt_path)
    ass_p = Path(ass_path)
    if not srt_p.exists():
        raise FileNotFoundError(f"Không tìm thấy file SRT tại: {srt_p}")

    cfg = config or load_subtitle_config()
    events = parse_srt(srt_p.read_text(encoding="utf-8"))

    font_name = cfg.get("font_name", "Arial").split(",")[0].strip()
    font_size = int(cfg.get("font_size", 28))
    bold = -1 if cfg.get("bold", True) else 0
    italic = -1 if cfg.get("italic", False) else 0
    p_color = cfg.get("primary_color", "&H00242120")
    s_color = cfg.get("secondary_color", "&H0023A6F5")
    o_color = cfg.get("outline_color", "&H00FFFFFF")
    b_color = cfg.get("back_color", "&H00000000")
    border_style = int(cfg.get("border_style", 1))
    outline = float(cfg.get("outline_width", 2.5))
    shadow = float(cfg.get("shadow", 1.0))
    align = int(cfg.get("alignment", 2))
    margin_l = int(cfg.get("margin_l", 80))
    margin_r = int(cfg.get("margin_r", 80))
    margin_v = int(cfg.get("margin_v", 45))

    is_capsule = cfg.get("background_mode") == "rounded_rect"

    if is_capsule:
        bg_color_hex = cfg.get("background_color", "#14171F")
        bg_opacity = float(cfg.get("background_opacity", 0.75))
        bg_alpha = int(round((1.0 - bg_opacity) * 255))
        bg_ass_color = hex_to_ass_color(bg_color_hex, alpha=bg_alpha)
        accent_hex = cfg.get("accent_color", "#F5A623")
        accent_ass = hex_to_ass_color(accent_hex)
        radius = int(cfg.get("background_radius", 22))
        pad_x = int(cfg.get("background_padding_x", 48))
        pad_y = int(cfg.get("background_padding_y", 16))
        anchor_x = int(cfg.get("anchor_x", 960))
        anchor_y = int(cfg.get("anchor_y", 980))
        max_w_limit = int(cfg.get("max_width", 1760))
        spacing = float(cfg.get("letter_spacing", 0.2))
        dock_mode = cfg.get("dock_mode", "dynamic_fit")
        
        border_width = float(cfg.get("border_width", 2.0))
        border_color_hex = cfg.get("border_color", "#334155")
        if border_color_hex and border_width > 0:
            border_ass = hex_to_ass_color(border_color_hex)
        else:
            border_ass = bg_ass_color
            border_width = 0.0
            
        shadow_dist = float(cfg.get("shadow", 2.0))
        shadow_ass = hex_to_ass_color("#000000", alpha=160)

        ass_content = f"""[Script Info]
; Script generated by Antigravity Subtitle Engine v2.2 (Full-Width Dock Edition)
Title: Whiteboard Dynamic Subtitles - Full-Width Dock
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {canvas_w}
PlayResY: {canvas_h}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CapsuleBg,Arial,10,{bg_ass_color},&H00000000,{border_ass},{shadow_ass},0,0,0,0,100,100,0,0,1,{border_width},{shadow_dist},7,0,0,0,1
Style: SubText,{font_name},{font_size},{p_color},{accent_ass},&H00000000,&H00000000,{bold},{italic},0,0,100,100,{spacing},0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        max_lines = int(cfg.get("max_lines", 1))

        for ev in events:
            raw_text = ev['text']
            allowed_w = max_w_limit - pad_x * 2

            if max_lines == 1:
                # 1-line mode: strip any explicit \N
                clean_text = raw_text.replace(r"\N", " ")
                curr_fs = font_size
                tw, th = measure_text_box(clean_text, curr_fs)

                # Adaptively scale down font size if sentence is longer than allowed_w
                min_fs = int(cfg.get("font_size_min", 42))
                while tw > allowed_w and curr_fs > min_fs:
                    curr_fs -= 1
                    tw, th = measure_text_box(clean_text, curr_fs)

                fs_tag = f"\\fs{curr_fs}" if curr_fs != font_size else ""
                text_to_render = clean_text
                dialogue_tags = f"{{\\pos({anchor_x},{anchor_y}){fs_tag}}}"
            else:
                dialogue_tags = f"{{\\pos({anchor_x},{anchor_y})}}"
                single_tw, _ = measure_text_box(raw_text, font_size)
                if r"\N" not in raw_text and single_tw > allowed_w:
                    words = raw_text.split(" ")
                    mid = len(words) // 2
                    best_split = mid
                    best_diff = 999999
                    for i in range(max(1, mid - 3), min(len(words), mid + 4)):
                        l1 = " ".join(words[:i])
                        l2 = " ".join(words[i:])
                        w1, _ = measure_text_box(l1, font_size)
                        w2, _ = measure_text_box(l2, font_size)
                        diff = abs(w1 - w2)
                        if diff < best_diff and max(w1, w2) <= allowed_w:
                            best_diff = diff
                            best_split = i
                    l1 = " ".join(words[:best_split])
                    l2 = " ".join(words[best_split:])
                    text_to_render = f"{l1}\\N{l2}"
                else:
                    text_to_render = raw_text
                tw, th = measure_text_box(text_to_render, font_size)

            if dock_mode == "full_dock":
                w = max_w_limit
            else:
                w = min(max_w_limit, tw + pad_x * 2)
            h = max(76, th + pad_y * 2)
            path = build_bezier_capsule_path(anchor_x, anchor_y, w, h, radius)
            ass_content += f"Dialogue: 0,{ev['start']},{ev['end']},CapsuleBg,,0,0,0,,{{\\p1}}{path}{{\\p0}}\n"
            ass_content += f"Dialogue: 1,{ev['start']},{ev['end']},SubText,,0,0,0,,{dialogue_tags}{text_to_render}\n"
    else:
        ass_content = f"""[Script Info]
; Script generated by Antigravity Subtitle Engine v2.0
Title: Whiteboard Dynamic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {canvas_w}
PlayResY: {canvas_h}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},{p_color},{s_color},{o_color},{b_color},{bold},{italic},0,0,100,100,0.5,0,{border_style},{outline},{shadow},{align},{margin_l},{margin_r},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        for ev in events:
            ass_content += f"Dialogue: 0,{ev['start']},{ev['end']},Default,,0,0,0,,{ev['text']}\n"

    ass_p.parent.mkdir(parents=True, exist_ok=True)
    ass_p.write_text(ass_content, encoding="utf-8")
    return ass_p


def get_ffmpeg_subtitle_filter(
    srt_path: Path | str,
    project_dir: Optional[Path | str] = None,
    config: Optional[Dict[str, Any]] = None,
    prefer_ass: bool = True
) -> str:
    """
    Sinh tham số bộ lọc FFmpeg (-vf) chuẩn hóa.
    Nếu prefer_ass=True, tự động biên dịch SRT sang file ASS tạm để đạt độ ổn định và thẩm mỹ tối thượng.
    """
    srt_p = Path(srt_path).resolve()
    cfg = config or load_subtitle_config(project_dir)

    if prefer_ass:
        ass_p = srt_p.with_suffix(".ass")
        compile_srt_to_ass(srt_p, ass_p, cfg)
        escaped_ass = str(ass_p).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        return f"ass='{escaped_ass}'"
    else:
        font_name = cfg.get("font_name", "Arial").split(",")[0].strip()
        font_size = cfg.get("font_size", 28)
        p_color = cfg.get("primary_color", "&H00242120")
        b_color = cfg.get("back_color", "&H00000000")
        border = cfg.get("border_style", 1)
        margin_v = cfg.get("margin_v", 45)
        outline = cfg.get("outline_width", 2.5)

        style_str = (
            f"FontName={font_name},"
            f"FontSize={font_size},"
            f"PrimaryColour={p_color},"
            f"BackColour={b_color},"
            f"BorderStyle={border},"
            f"Outline={outline},"
            f"MarginV={margin_v}"
        )
        escaped_srt = str(srt_p).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        return f"subtitles='{escaped_srt}':force_style='{style_str}'"


def burn_subtitles_to_video(
    input_video: Path | str,
    srt_or_ass: Path | str,
    output_video: Path | str,
    project_dir: Optional[Path | str] = None,
    config: Optional[Dict[str, Any]] = None
) -> bool:
    """Ghi đè phụ đề chuẩn vào video bằng FFmpeg."""
    in_v = Path(input_video).resolve()
    sub_f = Path(srt_or_ass).resolve()
    out_v = Path(output_video).resolve()

    if not in_v.exists():
        raise FileNotFoundError(f"Không tìm thấy video gốc: {in_v}")
    if not sub_f.exists():
        raise FileNotFoundError(f"Không tìm thấy file phụ đề: {sub_f}")

    if sub_f.suffix.lower() == ".srt":
        vf_param = get_ffmpeg_subtitle_filter(sub_f, project_dir=project_dir, config=config, prefer_ass=True)
    else:
        escaped_sub = str(sub_f).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        vf_param = f"ass='{escaped_sub}'"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(in_v),
        "-vf", vf_param,
        "-c:a", "copy",
        str(out_v)
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        print(f"[Lỗi Burn Subtitles] {p.stderr[-500:]}")
        return False
    return True


# ==============================================================================
# CLI Interface
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Bộ công cụ định dạng & kết xuất phụ đề động Whiteboard Video")
    subparsers = parser.add_subparsers(dest="command")

    # Command: compile
    p_compile = subparsers.add_parser("compile", help="Biên dịch SRT sang ASS")
    p_compile.add_argument("srt", type=Path, help="Đường dẫn file SRT nguồn")
    p_compile.add_argument("ass", type=Path, help="Đường dẫn file ASS đích")
    p_compile.add_argument("--project", type=Path, default=None, help="Đường dẫn thư mục dự án (chứa project.json)")
    p_compile.add_argument("--preset", choices=list(PRESETS.keys()), default=None, help="Chọn Preset thẩm mỹ")

    # Command: burn
    p_burn = subparsers.add_parser("burn", help="Ghi phụ đề vào video")
    p_burn.add_argument("video", type=Path, help="Video nguồn MP4")
    p_burn.add_argument("sub", type=Path, help="File phụ đề SRT hoặc ASS")
    p_burn.add_argument("output", type=Path, help="Video đích MP4")
    p_burn.add_argument("--project", type=Path, default=None, help="Đường dẫn thư mục dự án")
    p_burn.add_argument("--preset", choices=list(PRESETS.keys()), default=None, help="Chọn Preset thẩm mỹ")

    # Command: list-presets
    subparsers.add_parser("presets", help="Hiển thị danh sách các Preset thẩm mỹ có sẵn")

    args = parser.parse_args()

    if args.command == "compile":
        cfg = load_subtitle_config(args.project)
        if args.preset:
            cfg.update(PRESETS[args.preset])
        out = compile_srt_to_ass(args.srt, args.ass, cfg)
        print(f"✓ Đã biên dịch thành công ASS: {out}")

    elif args.command == "burn":
        cfg = load_subtitle_config(args.project)
        if args.preset:
            cfg.update(PRESETS[args.preset])
        ok = burn_subtitles_to_video(args.video, args.sub, args.output, project_dir=args.project, config=cfg)
        if ok:
            print(f"🎉 Đã kết xuất video kèm phụ đề mới: {args.output}")
        else:
            sys.exit(1)

    elif args.command == "presets":
        print("=" * 65)
        print("DANH SÁCH PRESET PHỤ ĐỀ WHITEBOARD ANIMATION:")
        print("=" * 65)
        for k, v in PRESETS.items():
            print(f"  • {k:22s}: {v['description']}")
            print(f"    - Font: {v['font_name']} | Cỡ chữ: {v['font_size']}pt | Màu: {v['primary_color']}")
            bs = v.get('border_style', 'custom')
            ow = v.get('outline_width', v.get('border_width', 0))
            mv = v.get('margin_v', 45)
            print(f"    - BorderStyle: {bs} | Outline: {ow}px | MarginV: {mv}px")
        print("=" * 65)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

