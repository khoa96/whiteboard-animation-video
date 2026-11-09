import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf"
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

# Load base image
base = Image.open(BASE_IMG_PATH).convert("RGBA")

# Let's crop just the bottom portion (Y: 600 to 1080) for detailed close-up comparison
# and also generate full 1920x1080 snapshots.

themes = [
    {
        "id": "current_flawed",
        "tag": "THIẾT KẾ CŨ (LỖI)",
        "desc": "Nền #F3F6FA nhợt nhạt mất mép, hộp hẹp 800px ở giữa, bị chém 2 hàng",
        "bg_color": (243, 246, 250, 255),
        "border_color": None,
        "border_w": 0,
        "text_color": (32, 33, 36),
        "accent_color": (52, 120, 212),
        "shadow": False,
        "is_bug": True
    },
    {
        "id": "opt1_dark_slate",
        "tag": "OPTION 1: DARK SLATE OBSIDIAN",
        "desc": "Đen than chì #14171F, viền Slate, chữ trắng #FFFFFF, accent cam #F5A623 (Chuẩn MasterClass/Apple TV)",
        "bg_color": (20, 23, 31, 248),
        "border_color": (51, 65, 85, 220),
        "border_w": 1.5,
        "text_color": (255, 255, 255),
        "accent_color": (245, 166, 35),
        "shadow": True,
        "is_bug": False
    },
    {
        "id": "opt2_midnight_navy",
        "tag": "OPTION 2: DEEP MIDNIGHT NAVY",
        "desc": "Xanh navy hoàng gia #0F172A, viền Cyan #38BDF8, chữ trắng ngọc trai (Chuẩn Oxford/Duolingo)",
        "bg_color": (15, 23, 42, 250),
        "border_color": (56, 189, 248, 160),
        "border_w": 1.5,
        "text_color": (248, 250, 252),
        "accent_color": (56, 189, 248),
        "shadow": True,
        "is_bug": False
    },
    {
        "id": "opt3_pure_white_card",
        "tag": "OPTION 3: CRISP WHITE CARD",
        "desc": "Trắng sứ #FFFFFF, viền Micro-Stroke #CBD5E1 2px + bóng đổ mềm, chữ đen #0F172A (Notion Clean UI)",
        "bg_color": (255, 255, 255, 255),
        "border_color": (203, 213, 225, 255),
        "border_w": 2.0,
        "text_color": (15, 23, 42),
        "accent_color": (37, 99, 235),
        "shadow": True,
        "is_bug": False
    },
    {
        "id": "opt4_warm_ivory",
        "tag": "OPTION 4: WARM IVORY & ESPRESSO",
        "desc": "Nền kem cát ấm #FEF3C7, viền hổ phách, chữ nâu cà phê #292524 (Sổ tay giáo dục dịu mắt)",
        "bg_color": (254, 243, 199, 255),
        "border_color": (252, 211, 77, 230),
        "border_w": 2.0,
        "text_color": (41, 37, 36),
        "accent_color": (234, 88, 12),
        "shadow": True,
        "is_bug": False
    },
    {
        "id": "opt5_tech_dock",
        "tag": "OPTION 5: TECH DOCK + ACCENT BAR",
        "desc": "Thanh dock than chì #1C2028, vạch nhận diện thương hiệu Blue #3478D4 (Pro Creator YouTube)",
        "bg_color": (28, 32, 40, 248),
        "border_color": (59, 130, 246, 180),
        "border_w": 1.5,
        "text_color": (249, 250, 251),
        "accent_color": (52, 120, 212),
        "has_left_bar": True,
        "shadow": True,
        "is_bug": False
    }
]

# We will create a comprehensive Comparison Board Image (1920 x 2400)
# displaying each option cropped at the bottom subtitle area with full annotations!
board_w = 1920
row_h = 240
board_h = 160 + len(themes) * row_h
board = Image.new("RGBA", (board_w, board_h), (248, 250, 252, 255))
bdraw = ImageDraw.Draw(board)

title_font = ImageFont.truetype(str(FONT_PATH), 34)
subtitle_font = ImageFont.truetype(str(FONT_PATH), 20)
tag_font = ImageFont.truetype(str(FONT_PATH), 22)
desc_font = ImageFont.truetype(str(FONT_PATH), 18)
sub_font = ImageFont.truetype(str(FONT_PATH), 46)

# Header
bdraw.rectangle([0, 0, board_w, 140], fill=(15, 23, 42, 255))
bdraw.text((60, 28), "SO SÁNH 5 PHƯƠNG ÁN THIẾT KẾ PHỤ ĐỀ MỚI VS THIẾT KẾ CŨ", font=title_font, fill=(255, 255, 255))
bdraw.text((60, 80), "Whiteboard Animation Studio — Tối ưu hóa UI/UX: Độ tương phản WCAG, Bố cục Full-Width 1760px & Ưu tiên 1 dòng", font=subtitle_font, fill=(148, 163, 184))

text_sample = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

for idx, th in enumerate(themes):
    y_start = 140 + idx * row_h
    # Alternate subtle row background
    bg_row = (255, 255, 255, 255) if idx % 2 == 0 else (241, 245, 249, 255)
    bdraw.rectangle([0, y_start, board_w, y_start + row_h], fill=bg_row)
    bdraw.line([0, y_start + row_h - 1, board_w, y_start + row_h - 1], fill=(226, 232, 240, 255), width=1)
    
    # Meta label
    bdraw.text((60, y_start + 18), th["tag"], font=tag_font, fill=(30, 41, 59))
    bdraw.text((60, y_start + 48), th["desc"], font=desc_font, fill=(100, 116, 139))
    
    # Render subtitle capsule preview
    cap_y_center = y_start + 155
    if th["is_bug"]:
        # Flawed 2-line rendering centered
        line1 = "A/AN chỉ vật chung chung, THE chỉ vật"
        line2 = "cụ thể, và water không cần mạo từ."
        bb1 = sub_font.getbbox(line1)
        bb2 = sub_font.getbbox(line2)
        lw = max(bb1[2]-bb1[0], bb2[2]-bb2[0])
        cw = lw + 80
        ch = (bb1[3]-bb1[1]) + (bb2[3]-bb2[1]) + 40
        cx1 = (board_w - cw) // 2
        cy1 = cap_y_center - ch // 2
        cx2 = cx1 + cw
        cy2 = cy1 + ch
        bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=24, fill=th["bg_color"])
        # draw text lines
        t1_x = (board_w - (bb1[2]-bb1[0])) // 2
        t2_x = (board_w - (bb2[2]-bb2[0])) // 2
        bdraw.text((t1_x, cy1 + 14), line1, font=sub_font, fill=th["text_color"])
        bdraw.text((t2_x, cy1 + 14 + (bb1[3]-bb1[1]) + 8), line2, font=sub_font, fill=th["text_color"])
        
        # Draw red warning tag
        bdraw.rounded_rectangle([board_w - 280, y_start + 20, board_w - 60, y_start + 55], radius=6, fill=(239, 68, 68, 255))
        bdraw.text((board_w - 265, y_start + 26), "MẤT MÉP & 2 DÒNG", font=subtitle_font, fill=(255, 255, 255))
    else:
        # Full-width 1760px single-line dock
        cw = 1760
        ch = 82
        cx1 = 80
        cy1 = cap_y_center - ch // 2
        cx2 = cx1 + cw
        cy2 = cy1 + ch
        cr = 20
        
        # Shadow
        if th["shadow"]:
            # Simple shadow simulation on board
            bdraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
            
        bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, fill=th["bg_color"])
        if th.get("border_color") and th.get("border_w", 0) > 0:
            bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, outline=th["border_color"], width=int(th["border_w"]))
            
        if th.get("has_left_bar", False):
            bdraw.rounded_rectangle([cx1 + 16, cy1 + 16, cx1 + 22, cy2 - 16], radius=3, fill=th["accent_color"])
            
        # Draw text centered
        t_box = sub_font.getbbox(text_sample)
        tw = t_box[2] - t_box[0]
        th_val = t_box[3] - t_box[1]
        tx = (board_w - tw) // 2
        ty = cy1 + (ch - th_val) // 2 - 3
        
        # Highlight words
        words = text_sample.split(" ")
        curr_x = tx
        for wd in words:
            wb = sub_font.getbbox(wd + " ")
            ww = wb[2] - wb[0]
            clean_wd = wd.strip(".,;:?!")
            col = th["accent_color"] if clean_wd in ["A/AN", "THE", "water"] else th["text_color"]
            bdraw.text((curr_x, ty), wd + " ", font=sub_font, fill=col)
            curr_x += ww
            
        # Draw green approval tag
        bdraw.rounded_rectangle([board_w - 280, y_start + 20, board_w - 60, y_start + 55], radius=6, fill=(16, 185, 129, 255))
        bdraw.text((board_w - 265, y_start + 26), "FULL 1 DÒNG 1760PX", font=subtitle_font, fill=(255, 255, 255))

board_path = OUTPUT_DIR / "subtitle_comparison_master_board.png"
board.convert("RGB").save(board_path, quality=95)
print(f"Master comparison board saved at: {board_path}")
