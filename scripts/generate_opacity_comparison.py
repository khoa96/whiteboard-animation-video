from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf"
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

# We will create a comparison board testing 5 Opacity levels for Option 1 (Dark Slate)
# On a realistic whiteboard background with drawing markers passing slightly behind/near it.

opacities = [
    {
        "tier": "MỨC 1 — 90% (Đen mờ sâu, viền Slate mềm)",
        "opacity": 0.90,
        "alpha_int": 230,
        "ass_alpha": "&H19",  # 25 in dec
        "desc": "Tối màu sang trọng, không đen kịt, vẫn giữ độ tương phản tối cao 17:1",
        "tag": "90% OPACITY (SOLID SOFT)"
    },
    {
        "tier": "MỨC 2 — 80% (Frosted Dark Glass — Khuyên Dùng)",
        "opacity": 0.80,
        "alpha_int": 204,
        "ass_alpha": "&H33",  # 51 in dec
        "desc": "Kính đen mờ hiện đại, nhìn thấy nền trắng mờ ảo phía sau, rất điện ảnh",
        "tag": "80% OPACITY (FROSTED GLASS)"
    },
    {
        "tier": "MỨC 3 — 70% (Smoky Translucent)",
        "opacity": 0.70,
        "alpha_int": 178,
        "ass_alpha": "&H4C",  # 76 in dec
        "desc": "Độ trong suốt vừa phải, nhẹ nhàng, thanh thoát",
        "tag": "70% OPACITY (SMOKY)"
    },
    {
        "tier": "MỨC 4 — 60% (Medium Glass)",
        "opacity": 0.60,
        "alpha_int": 153,
        "ass_alpha": "&H66",  # 102 in dec
        "desc": "Trong suốt cao, thấy rõ chi tiết bên dưới, chữ trắng vẫn đọc tốt",
        "tag": "60% OPACITY (TRANSLUCENT)"
    },
    {
        "tier": "MỨC 5 — 45% (Ultra Light Smoky Pill)",
        "opacity": 0.45,
        "alpha_int": 115,
        "ass_alpha": "&H8C",  # 140 in dec
        "desc": "Khói mờ siêu nhẹ, hòa quyện tối đa vào nền bảng trắng",
        "tag": "45% OPACITY (LIGHT SMOKE)"
    }
]

board_w = 1920
row_h = 240
board_h = 160 + len(opacities) * row_h
board = Image.new("RGBA", (board_w, board_h), (248, 250, 252, 255))
bdraw = ImageDraw.Draw(board)

title_font = ImageFont.truetype(str(FONT_PATH), 34)
subtitle_font = ImageFont.truetype(str(FONT_PATH), 20)
tag_font = ImageFont.truetype(str(FONT_PATH), 22)
desc_font = ImageFont.truetype(str(FONT_PATH), 18)
sub_font = ImageFont.truetype(str(FONT_PATH), 46)

# Header
bdraw.rectangle([0, 0, board_w, 140], fill=(20, 23, 31, 255))
bdraw.text((60, 28), "SO SÁNH 5 CẤP ĐỘ ĐỘ MỜ (OPACITY) CHO PHƯƠNG ÁN 1: DARK SLATE", font=title_font, fill=(255, 255, 255))
bdraw.text((60, 80), "Thanh Dock 1760px trải rộng, bo tròn R=22px — Tùy biến độ trong suốt để không bị 'đen xì'", font=subtitle_font, fill=(148, 163, 184))

sample_text = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

for idx, op in enumerate(opacities):
    y_start = 140 + idx * row_h
    # Alternate background with subtle grid/pattern to see transparency clearly!
    bg_row = (255, 255, 255, 255) if idx % 2 == 0 else (245, 247, 250, 255)
    bdraw.rectangle([0, y_start, board_w, y_start + row_h], fill=bg_row)
    bdraw.line([0, y_start + row_h - 1, board_w, y_start + row_h - 1], fill=(226, 232, 240, 255), width=1)
    
    # Draw a colored decorative stripe behind the capsule to prove transparency!
    bdraw.rectangle([200, y_start + 110, 1720, y_start + 195], fill=(241, 245, 249, 255))
    # Some simulated marker sketch lines behind
    bdraw.line([300, y_start + 120, 800, y_start + 185], fill=(52, 120, 212, 100), width=4)
    bdraw.line([1200, y_start + 175, 1650, y_start + 130], fill=(245, 166, 35, 100), width=4)
    
    # Text labels
    bdraw.text((60, y_start + 18), op["tier"], font=tag_font, fill=(30, 41, 59))
    bdraw.text((60, y_start + 48), op["desc"], font=desc_font, fill=(100, 116, 139))
    
    # Right badge
    bdraw.rounded_rectangle([board_w - 320, y_start + 20, board_w - 60, y_start + 55], radius=6, fill=(30, 41, 59, 240))
    bdraw.text((board_w - 305, y_start + 26), op["tag"], font=subtitle_font, fill=(245, 166, 35))
    
    # Capsule Dock
    cap_y_center = y_start + 155
    cw = 1760
    ch = 82
    cx1 = 80
    cx2 = cx1 + cw
    cy1 = cap_y_center - ch // 2
    cy2 = cy1 + ch
    cr = 20
    
    # Draw translucent dock
    dock_overlay = Image.new("RGBA", (board_w, board_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(dock_overlay)
    
    # Shadow
    odraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, int(op["alpha_int"] * 0.2)))
    
    # Background with custom opacity
    odraw.rounded_rectangle(
        [cx1, cy1, cx2, cy2], 
        radius=cr, 
        fill=(20, 23, 31, op["alpha_int"]),
        outline=(51, 65, 85, int(op["alpha_int"] * 0.9)),
        width=2
    )
    
    board = Image.alpha_composite(board, dock_overlay)
    bdraw = ImageDraw.Draw(board)
    
    # Text
    t_box = sub_font.getbbox(sample_text)
    tw = t_box[2] - t_box[0]
    th_val = t_box[3] - t_box[1]
    tx = (board_w - tw) // 2
    ty = cy1 + (ch - th_val) // 2 - 3
    
    words = sample_text.split(" ")
    curr_x = tx
    for wd in words:
        wb = sub_font.getbbox(wd + " ")
        ww = wb[2] - wb[0]
        clean_wd = wd.strip(".,;:?!")
        col = (245, 166, 35) if clean_wd in ["A/AN", "THE", "water"] else (255, 255, 255)
        bdraw.text((curr_x, ty), wd + " ", font=sub_font, fill=col)
        curr_x += ww

out_board = OUTPUT_DIR / "subtitle_opacity_comparison_board.png"
board.convert("RGB").save(out_board, quality=95)
print(f"Opacity comparison board saved: {out_board}")
