import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf"
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

board_w = 1920
row_h = 270
board_h = 160 + 3 * row_h
board = Image.new("RGBA", (board_w, board_h), (248, 250, 252, 255))
bdraw = ImageDraw.Draw(board)

title_font = ImageFont.truetype(str(FONT_PATH), 34)
subtitle_font = ImageFont.truetype(str(FONT_PATH), 20)
tag_font = ImageFont.truetype(str(FONT_PATH), 22)
desc_font = ImageFont.truetype(str(FONT_PATH), 18)
sub_font = ImageFont.truetype(str(FONT_PATH), 46)

# Header
bdraw.rectangle([0, 0, board_w, 140], fill=(15, 23, 42, 255))
bdraw.text((60, 28), "SO SÁNH CÁC GIẢI PHÁP BỐ CỤC: FULL-WIDTH DOCK VS DYNAMIC CAPSULE", font=title_font, fill=(255, 255, 255))
bdraw.text((60, 80), "Giải quyết triệt để lỗi ép 2 hàng & lỗi căn giữa làm hẹp không gian hiển thị", font=subtitle_font, fill=(148, 163, 184))

layouts = [
    {
        "id": "layout_a_full_dock_centered",
        "tag": "GIẢI PHÁP 1: FULL-WIDTH DOCK BAR — CĂN GIỮA (Khuyên Dùng Nhất)",
        "desc": "Thanh dock cố định rộng 1760px (lề 80px), cao 84px mỏng gọn, chữ căn giữa. Đảm bảo 100% câu dài nằm trọn 1 dòng.",
        "mode": "full_center"
    },
    {
        "id": "layout_b_full_dock_left",
        "tag": "GIẢI PHÁP 2: FULL-WIDTH DOCK BAR — CĂN TRÁI + ACCENT PILL (Chuẩn Truyền Hình)",
        "desc": "Thanh dock 1760px, chữ căn trái từ X=140px với vạch màu nhận diện. Đọc từ trái sang phải tự nhiên, tốc độ tiếp thu cao nhất.",
        "mode": "full_left"
    },
    {
        "id": "layout_c_dynamic_wide_capsule",
        "tag": "GIẢI PHÁP 3: DYNAMIC WIDE CAPSULE (Viên Nang Tự Co Giãn Tối Đa 1760px)",
        "desc": "Viên nang tự động mở rộng theo đúng độ dài của câu (tối đa 1760px). Không bẻ dòng nếu câu dưới 75 ký tự.",
        "mode": "dynamic_wide"
    }
]

text_sample = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

for idx, lay in enumerate(layouts):
    y_start = 140 + idx * row_h
    bg_row = (255, 255, 255, 255) if idx % 2 == 0 else (241, 245, 249, 255)
    bdraw.rectangle([0, y_start, board_w, y_start + row_h], fill=bg_row)
    bdraw.line([0, y_start + row_h - 1, board_w, y_start + row_h - 1], fill=(226, 232, 240, 255), width=1)
    
    bdraw.text((60, y_start + 20), lay["tag"], font=tag_font, fill=(30, 41, 59))
    bdraw.text((60, y_start + 50), lay["desc"], font=desc_font, fill=(100, 116, 139))
    
    cap_y_center = y_start + 170
    bg_col = (15, 23, 42, 250)      # Slate-900 (Navy / Slate style)
    border_col = (56, 189, 248, 160)
    ch = 82
    cr = 20
    
    t_box = sub_font.getbbox(text_sample)
    tw = t_box[2] - t_box[0]
    th_val = t_box[3] - t_box[1]
    
    if lay["mode"] == "full_center":
        cw = 1760
        cx1 = 80
        cx2 = cx1 + cw
        cy1 = cap_y_center - ch // 2
        cy2 = cy1 + ch
        bdraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
        bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, fill=bg_col, outline=border_col, width=2)
        tx = (board_w - tw) // 2
        ty = cy1 + (ch - th_val) // 2 - 3
        
    elif lay["mode"] == "full_left":
        cw = 1760
        cx1 = 80
        cx2 = cx1 + cw
        cy1 = cap_y_center - ch // 2
        cy2 = cy1 + ch
        bdraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
        bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, fill=bg_col, outline=border_col, width=2)
        # Left accent pill
        bdraw.rounded_rectangle([cx1 + 20, cy1 + 18, cx1 + 26, cy2 - 18], radius=3, fill=(56, 189, 248, 255))
        tx = cx1 + 48
        ty = cy1 + (ch - th_val) // 2 - 3
        
    else: # dynamic_wide
        cw = min(1760, tw + 120)
        cx1 = (board_w - cw) // 2
        cx2 = cx1 + cw
        cy1 = cap_y_center - ch // 2
        cy2 = cy1 + ch
        bdraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
        bdraw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=cr, fill=bg_col, outline=border_col, width=2)
        tx = (board_w - tw) // 2
        ty = cy1 + (ch - th_val) // 2 - 3

    # Draw words with accent color
    words = text_sample.split(" ")
    curr_x = tx
    for wd in words:
        wb = sub_font.getbbox(wd + " ")
        ww = wb[2] - wb[0]
        clean_wd = wd.strip(".,;:?!")
        col = (56, 189, 248) if clean_wd in ["A/AN", "THE", "water"] else (248, 250, 252)
        bdraw.text((curr_x, ty), wd + " ", font=sub_font, fill=col)
        curr_x += ww

board_path = OUTPUT_DIR / "subtitle_layout_showcase.png"
board.convert("RGB").save(board_path, quality=95)
print(f"Layout showcase saved at: {board_path}")
