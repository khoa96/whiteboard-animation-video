from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

board_w = 1920
row_h = 240
title_h = 160
num_rows = 5
board_h = title_h + num_rows * row_h

board = Image.new("RGBA", (board_w, board_h), (248, 250, 252, 255))
bdraw = ImageDraw.Draw(board)

title_font = ImageFont.truetype(str(REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf"), 34)
subtitle_font = ImageFont.truetype(str(REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf"), 20)
tag_font = ImageFont.truetype(str(REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf"), 22)
desc_font = ImageFont.truetype(str(REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf"), 17)

# Header
bdraw.rectangle([0, 0, board_w, title_h], fill=(15, 23, 42, 255))
bdraw.text((60, 32), "SO SÁNH CÁC PHÔNG CHỮ & KÍCH THƯỚC MỚI (FIT CONTENT + PADDING VỪA PHẢI)", font=title_font, fill=(255, 255, 255))
bdraw.text((60, 85), "Giải quyết triệt để lỗi thừa khoảng trống 2 bên & Nâng cấp nét chữ to, đầm chắc, chuẩn nhận diện", font=subtitle_font, fill=(148, 163, 184))

sample_text = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

candidates = [
    {
        "tag": "1. BE VIETNAM PRO BOLD (44pt) — ⭐ KHUYÊN DÙNG SỐ 1",
        "desc": "Thiết kế chuyên biệt cho tiếng Việt & Anh: X-height cao, nét đầm chắc cực rõ, dấu thanh thoát không bao giờ dính nét",
        "font_path": REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf",
        "font_size": 44,
        "theme": "opt1_dark_75"
    },
    {
        "tag": "2. LEXEND BOLD (44pt) — CHUẨN GIÁO DỤC GOOGLE",
        "desc": "Font nghiên cứu giáo dục của Google: Khoảng cách con chữ mở rộng, hỗ trợ học viên đọc lướt và ghi nhớ nhanh hơn 19%",
        "font_path": REPO_ROOT / "assets/fonts/Lexend-Bold.ttf",
        "font_size": 44,
        "theme": "opt1_dark_75"
    },
    {
        "tag": "3. MONTSERRAT BOLD (42pt) — HÌNH HỌC HIỆN ĐẠI",
        "desc": "Font hình học hiện đại (Geometric Sans): Chữ vuông vức, nét dày mạnh mẽ, phong cách tài liệu giáo dục quốc tế",
        "font_path": REPO_ROOT / "assets/fonts/Montserrat-Bold.ttf",
        "font_size": 42,
        "theme": "opt1_dark_75"
    },
    {
        "tag": "4. QUICKSAND BOLD (46pt) — BO TRÒN WHITEBOARD",
        "desc": "Đầu nét bo tròn mềm mại (Rounded Terminals): Cực kỳ thân thiện, đồng điệu hoàn hảo với nét vẽ tay bút lông bảng trắng",
        "font_path": REPO_ROOT / "assets/fonts/Quicksand-Bold.ttf",
        "font_size": 46,
        "theme": "opt1_dark_75"
    },
    {
        "tag": "5. OPTION 4: WARM IVORY (75% OPACITY) + BE VIETNAM PRO BOLD (44pt)",
        "desc": "Nền kem cát ấm 75% độ mờ, chữ nâu than cà phê đậm #292524, êm dịu thị giác, nhìn rõ cánh tay vẽ phía sau",
        "font_path": REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf",
        "font_size": 44,
        "theme": "opt4_ivory_75"
    }
]

for idx, item in enumerate(candidates):
    y_start = title_h + idx * row_h
    bg_row = (255, 255, 255, 255) if idx % 2 == 0 else (241, 245, 249, 255)
    bdraw.rectangle([0, y_start, board_w, y_start + row_h], fill=bg_row)
    bdraw.line([0, y_start + row_h - 1, board_w, y_start + row_h - 1], fill=(226, 232, 240, 255), width=1)
    
    # Meta text
    bdraw.text((60, y_start + 18), item["tag"], font=tag_font, fill=(30, 41, 59))
    bdraw.text((60, y_start + 48), item["desc"], font=desc_font, fill=(100, 116, 139))
    
    # Render capsule
    cap_font = ImageFont.truetype(str(item["font_path"]), item["font_size"])
    bbox = cap_font.getbbox(sample_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # Fit to content: padding_x = 48
    pad_x = 48
    pad_y = 16
    cw = tw + pad_x * 2
    ch = th + pad_y * 2
    cx1 = (board_w - cw) // 2
    cy1 = y_start + 155 - ch // 2
    cx2 = cx1 + cw
    cy2 = cy1 + ch
    cr = 20
    
    # Color scheme
    if item["theme"] == "opt1_dark_75":
        bg_col = (20, 23, 31, 191)       # 75% dark slate
        border_col = (51, 65, 85, 210)
        t_col = (255, 255, 255)
        acc_col = (245, 166, 35)
    else:
        bg_col = (254, 243, 199, 191)    # 75% warm ivory
        border_col = (252, 211, 77, 230)
        t_col = (41, 37, 36)
        acc_col = (234, 88, 12)
        
    # Draw simulated decorative line behind to show 75% opacity
    bdraw.line([cx1 - 60, cy1 + ch//2, cx2 + 60, cy1 + ch//2], fill=(52, 120, 212, 120), width=6)
    
    # Draw capsule
    dock_overlay = Image.new("RGBA", (board_w, board_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(dock_overlay)
    odraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
    odraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, fill=bg_col, outline=border_col, width=2)
    board = Image.alpha_composite(board, dock_overlay)
    bdraw = ImageDraw.Draw(board)
    
    # Draw text
    tx = (board_w - tw) // 2
    ty = cy1 + (ch - th) // 2 - 3
    words = sample_text.split(" ")
    curr_x = tx
    for wd in words:
        wb = cap_font.getbbox(wd + " ")
        ww = wb[2] - wb[0]
        clean_wd = wd.strip(".,;:?!")
        col = acc_col if clean_wd in ["A/AN", "THE", "water"] else t_col
        bdraw.text((curr_x, ty), wd + " ", font=cap_font, fill=col)
        curr_x += ww
        
    # Badge right
    bdraw.rounded_rectangle([board_w - 320, y_start + 18, board_w - 60, y_start + 50], radius=6, fill=(30, 41, 59, 240))
    bdraw.text((board_w - 305, y_start + 24), f"RỘNG: {cw}px (FIT)", font=subtitle_font, fill=(245, 166, 35))

board_path = OUTPUT_DIR / "subtitle_v2_font_and_fit_showcase.png"
board.convert("RGB").save(board_path, quality=95)
print(f"Master font and fit showcase saved: {board_path}")
