import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf"
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

THEMES = [
    {
        "id": "current_flawed",
        "title": "THIẾT KẾ CŨ (LỖI): Viên nang #F3F6FA nhạt nhòa, hẹp ngang, bị ép 2 dòng",
        "bg_color": (243, 246, 250, 255),      # #F3F6FA
        "border_color": None,
        "border_width": 0,
        "text_color": (32, 33, 36),             # #202124
        "accent_color": (52, 120, 212),         # #3478D4
        "shadow": False,
        "force_two_lines": True,
        "is_narrow": True,
        "tag": "CURRENT (FLAWED)"
    },
    {
        "id": "option_1_dark_slate",
        "title": "OPTION 1: DARK SLATE OBSIDIAN (Chuẩn MasterClass / Apple TV)",
        "subtitle": "Đen than chì trầm cao cấp, chữ trắng tinh, tương phản tối đa 21:1, tách bạch 100% khỏi nền trắng",
        "bg_color": (20, 23, 31, 248),          # #14171F
        "border_color": (51, 65, 85, 220),       # Slate-700
        "border_width": 1.5,
        "text_color": (255, 255, 255),           # Pure White
        "accent_color": (245, 166, 35),          # Amber Gold #F5A623
        "shadow": True,
        "tag": "1. CINEMATIC DARK SLATE"
    },
    {
        "id": "option_2_midnight_navy",
        "title": "OPTION 2: DEEP MIDNIGHT NAVY (Chuẩn Giáo Dục Quốc Tế / Oxford & Duolingo)",
        "subtitle": "Xanh navy hoàng gia sâu thẳm, chữ trắng ngọc trai, cực kỳ học thuật và uy tín",
        "bg_color": (15, 23, 42, 250),           # #0F172A (Slate-900)
        "border_color": (56, 189, 248, 160),     # Cyan micro stroke
        "border_width": 1.5,
        "text_color": (248, 250, 252),           # #F8FAFC
        "accent_color": (56, 189, 248),          # Sky Cyan #38BDF8
        "shadow": True,
        "tag": "2. ACADEMIC MIDNIGHT NAVY"
    },
    {
        "id": "option_3_pure_white_card",
        "title": "OPTION 3: CRISP WHITE CARD + HAIRLINE STROKE (Modern Notion / Clean UI)",
        "subtitle": "Nền trắng sứ tinh khôi, viền Micro-Stroke xám bạc 2px sắc sảo + đổ bóng mềm nâng khối",
        "bg_color": (255, 255, 255, 255),        # Pure White #FFFFFF
        "border_color": (203, 213, 225, 255),    # Slate-300 #CBD5E1
        "border_width": 2.0,
        "text_color": (15, 23, 42),              # Obsidian #0F172A
        "accent_color": (37, 99, 235),           # Royal Blue #2563EB
        "shadow": True,
        "tag": "3. CRISP WHITE CARD"
    },
    {
        "id": "option_4_warm_ivory",
        "title": "OPTION 4: WARM IVORY & ESPRESSO (Editorial Handbook / Ấm áp & Dịu mắt)",
        "subtitle": "Nền vàng kem cát ấm êm dịu thị giác, viền hổ phách, chữ nâu than cà phê đậm",
        "bg_color": (254, 243, 199, 255),        # Amber-100 #FEF3C7
        "border_color": (252, 211, 77, 230),     # Amber-300 #FCD34D
        "border_width": 2.0,
        "text_color": (41, 37, 36),              # Stone-900 #292524
        "accent_color": (234, 88, 12),           # Terracotta #EA580C
        "shadow": True,
        "tag": "4. WARM IVORY NOTEBOOK"
    },
    {
        "id": "option_5_tech_dock",
        "title": "OPTION 5: TECH CHARCOAL DOCK + BRAND ACCENT (Pro Creator Dynamic Dock)",
        "subtitle": "Thanh dock than chì hiện đại bo tròn lớn, vạch nhận diện thương hiệu Blue #3478D4",
        "bg_color": (28, 32, 40, 248),           # #1C2028
        "border_color": (59, 130, 246, 180),     # Blue-500
        "border_width": 1.5,
        "text_color": (249, 250, 251),           # Gray-50
        "accent_color": (52, 120, 212),          # Brand Blue #3478D4
        "has_left_bar": True,
        "shadow": True,
        "tag": "5. PRO CREATOR TECH DOCK"
    }
]

def render_preview(theme, text, mode="full_dock", font_size=48, output_path=None):
    # Load base image
    if BASE_IMG_PATH.exists():
        base = Image.open(BASE_IMG_PATH).convert("RGBA")
    else:
        base = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
        
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    tag_font = ImageFont.truetype(str(FONT_PATH), 20)
    
    # Check if forced two lines (simulating current bug)
    if theme.get("force_two_lines", False):
        # Split text into 2 lines like current flawed output
        lines = [
            "A/AN chỉ vật chung chung, THE chỉ vật",
            "cụ thể, và water không cần mạo từ."
        ]
        line_boxes = [font.getbbox(l) for l in lines]
        max_lw = max(b[2] - b[0] for b in line_boxes)
        th = sum(b[3] - b[1] for b in line_boxes) + 14
        
        # Flawed narrow capsule
        w = max_lw + 96
        h = th + 48
        x1 = (1920 - w) // 2
        y1 = 980 - h // 2
        x2 = x1 + w
        y2 = y1 + h
        r = 27
        
        # Draw rounded rectangle
        draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=theme["bg_color"])
        
        # Draw lines centered
        curr_y = y1 + 24
        for l in lines:
            bb = font.getbbox(l)
            lw = bb[2] - bb[0]
            lx = (1920 - lw) // 2
            draw.text((lx, curr_y), l, font=font, fill=theme["text_color"])
            curr_y += (bb[3] - bb[1]) + 14
            
    else:
        # NEW REDESIGNED LAYOUT: SINGLE-LINE FIRST
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        if mode == "full_dock":
            # Extended dock bar: W = 1760px (margin 80px left/right)
            w = 1760
            h = 88
            x1 = 80
            y1 = 980 - h // 2
            x2 = x1 + w
            y2 = y1 + h
            r = 22
        elif mode == "dynamic_capsule":
            # Dynamic capsule expanding up to 1760px
            w = min(1760, tw + 110)
            h = 88
            x1 = (1920 - w) // 2
            y1 = 980 - h // 2
            x2 = x1 + w
            y2 = y1 + h
            r = 24
        else: # left_dock
            w = 1760
            h = 88
            x1 = 80
            y1 = 980 - h // 2
            x2 = x1 + w
            y2 = y1 + h
            r = 22
            
        # Draw shadow if enabled
        if theme.get("shadow", False):
            shadow_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(shadow_layer)
            s_offset_y = 6
            s_blur = 16
            sdraw.rounded_rectangle([x1, y1 + s_offset_y, x2, y2 + s_offset_y], radius=r, fill=(0, 0, 0, 45))
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(s_blur))
            base = Image.alpha_composite(base, shadow_layer)
            
        # Draw background container
        draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=theme["bg_color"])
        
        # Draw border stroke if specified
        if theme.get("border_color") and theme.get("border_width", 0) > 0:
            draw.rounded_rectangle(
                [x1, y1, x2, y2], 
                radius=r, 
                outline=theme["border_color"], 
                width=int(theme["border_width"])
            )
            
        # Draw left indicator bar if applicable (Option 5)
        if theme.get("has_left_bar", False):
            bar_w = 6
            bar_pad = 18
            draw.rounded_rectangle(
                [x1 + bar_pad, y1 + bar_pad, x1 + bar_pad + bar_w, y2 - bar_pad],
                radius=3,
                fill=theme["accent_color"]
            )
            
        # Draw Text
        # Let's support Keyword Highlighting if desired!
        # Render centered
        text_x = (1920 - tw) // 2
        text_y = y1 + (h - th) // 2 - 4
        
        # Simple word by word render for accent coloring
        words = text.split(" ")
        curr_x = text_x
        for wd in words:
            w_box = font.getbbox(wd + " ")
            w_w = w_box[2] - w_box[0]
            clean_w = wd.strip(".,;:?!")
            color = theme["accent_color"] if clean_w in ["A/AN", "THE", "water"] else theme["text_color"]
            draw.text((curr_x, text_y), wd + " ", font=font, fill=color)
            curr_x += w_w

    # Top Tag Label on screen for easy identification
    tag_bg_w = 420
    tag_bg_h = 36
    draw.rounded_rectangle([40, 40, 40 + tag_bg_w, 40 + tag_bg_h], radius=8, fill=(15, 23, 42, 220))
    draw.text((54, 46), theme["tag"], font=tag_font, fill=(255, 255, 255))
    
    # Merge overlay onto base
    final_img = Image.alpha_composite(base, overlay)
    if output_path:
        final_img.convert("RGB").save(output_path, quality=95)
    return final_img

# Test render for each theme
sample_text = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."
for th in THEMES:
    out_file = OUTPUT_DIR / f"subtitle_preview_{th['id']}.png"
    render_preview(th, sample_text, mode="full_dock", font_size=48, output_path=out_file)
    print(f"Rendered: {out_file.name}")

print("All individual previews generated successfully.")
