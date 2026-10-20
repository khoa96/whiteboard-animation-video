#!/usr/bin/env python3
"""
Tạo bộ 4 ảnh nét vẽ bảng trắng 16:9 (1920x1080) cho video giải thích 1 phút:
Chủ đề: Sức Mạnh Của Lãi Kép (Compound Interest) - Kỳ Quan Thứ 8
Phiên bản hoàn thiện: Đồ họa chuẩn, không lỗi font ký tự, căn chỉnh lề hoàn hảo.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = Path(__file__).resolve().parent
W, H = 1920, 1080
BG_COLOR = (245, 235, 215)  # Kem bảng trắng chuẩn #F5EBD7


def get_font(size: int, bold: bool = True):
    bold_candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    regular_candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    candidates = bold_candidates if bold else regular_candidates
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ========================================================
# CẢNH 1: Hiệu ứng Hòn tuyết lăn (Snowball Effect) (~14s)
# ========================================================
def draw_scene_01():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_title = get_font(64)
    f_head = get_font(46)
    f_quote = get_font(52)
    f_body = get_font(38)
    f_label = get_font(32)

    # 1. Tiêu đề chính
    draw.text((100, 45), "LÃI KÉP: KỲ QUAN THỨ 8 CỦA THẾ GIỚI", fill=(20, 30, 55), font=f_title)
    draw.line([(100, 125), (1420, 125)], fill=(38, 103, 255), width=5)

    # 2. Khung trái: Khái niệm & Quy tắc cốt lõi
    b1_x0, b1_y0, b1_x1, b1_y1 = 100, 165, 960, 980
    draw.rounded_rectangle([b1_x0, b1_y0, b1_x1, b1_y1], radius=16, outline=(38, 103, 255), width=4)

    draw.text((140, 205), "QUY TẮC CỐT LÕI:", fill=(180, 50, 40), font=f_head)
    draw.text((140, 290), '"LÃI MẸ ĐẺ LÃI CON"', fill=(20, 30, 60), font=f_quote)
    draw.line([(140, 360), (740, 360)], fill=(220, 38, 38), width=4)

    draw.text((140, 395), "• Tiền vốn sinh ra tiền lãi", fill=(40, 50, 75), font=f_body)
    draw.text((140, 460), "• Tiền lãi gộp vào vốn -> sinh lãi mới", fill=(40, 50, 75), font=f_body)
    draw.text((140, 525), "• Tích lũy liên tục theo thời gian", fill=(40, 50, 75), font=f_body)

    # Icon đồng tiền đòn bẩy
    # Đồng xu nhỏ ban đầu
    cx1, cy1 = 260, 760
    draw.ellipse([cx1 - 50, cy1 - 50, cx1 + 50, cy1 + 50], outline=(245, 158, 11), width=5)
    draw.text((cx1 - 14, cy1 - 25), "$", fill=(245, 158, 11), font=get_font(44))
    draw.text((cx1 - 65, cy1 + 70), "VỐN NHỎ", fill=(100, 110, 130), font=f_label)

    # Mũi tên tăng trưởng cong
    draw.text((390, 645), "TÍCH LŨY", fill=(38, 103, 255), font=f_label)
    draw.arc([350, 700, 550, 820], 180, 360, fill=(38, 103, 255), width=5)
    draw.polygon([(540, 750), (565, 760), (540, 775)], fill=(38, 103, 255))

    # Đống tiền lớn tích lũy
    cx2, cy2 = 720, 750
    for dy in [20, 0, -20]:
        draw.ellipse([cx2 - 75, cy2 + dy - 35, cx2 + 75, cy2 + dy + 35], outline=(41, 167, 102), width=5)
    draw.text((cx2 - 35, cy2 - 45), "$$$", fill=(41, 167, 102), font=get_font(42))
    draw.text((cx2 - 90, cy2 + 70), "TÀI SẢN KHỦNG", fill=(41, 167, 102), font=f_label)

    # 3. Khung phải: Minh họa Hòn tuyết lăn (Snowball Effect)
    b2_x0, b2_y0, b2_x1, b2_y1 = 1010, 165, 1820, 980
    draw.rounded_rectangle([b2_x0, b2_y0, b2_x1, b2_y1], radius=16, outline=(70, 90, 120), width=4)

    draw.text((1060, 205), "HIỆU ỨNG HÒN TUYẾT LĂN:", fill=(38, 103, 255), font=f_head)

    # Sườn dốc thoai thoải từ trên xuống
    draw.line([(1080, 420), (1760, 840)], fill=(160, 175, 195), width=6)
    draw.line([(1080, 430), (1760, 850)], fill=(200, 210, 225), width=2)

    # Hòn tuyết 1 (Đỉnh núi - rất nhỏ)
    bx1, by1 = 1170, 430
    draw.ellipse([bx1 - 30, by1 - 30, bx1 + 30, by1 + 30], outline=(38, 103, 255), width=4)
    draw.text((bx1 - 70, by1 - 75), "Bắt đầu nhỏ", fill=(70, 85, 105), font=f_label)

    # Hòn tuyết 2 (Lưng chừng - lớn dần)
    bx2, by2 = 1390, 560
    draw.ellipse([bx2 - 55, by2 - 55, bx2 + 55, by2 + 55], outline=(38, 103, 255), width=5)
    draw.arc([bx2 - 40, by2 - 40, bx2 + 40, by2 + 40], 0, 180, fill=(38, 103, 255), width=3)
    draw.text((bx2 - 70, by2 - 95), "Lăn liên tục...", fill=(70, 85, 105), font=f_label)

    # Hòn tuyết 3 (Chân núi - khổng lồ)
    bx3, by3 = 1640, 730
    draw.ellipse([bx3 - 95, by3 - 95, bx3 + 95, by3 + 95], outline=(220, 38, 38), width=6)
    draw.arc([bx3 - 75, by3 - 75, bx3 + 75, by3 + 75], 30, 240, fill=(220, 38, 38), width=4)
    draw.text((bx3 - 90, by3 + 120), "KHỔNG LỒ!", fill=(220, 38, 38), font=f_head)

    # Kết luận dưới đáy khung tuyết
    draw.text((1060, 915), "-> Dốc càng dài, quả cầu tuyết càng to!", fill=(20, 30, 50), font=f_body)

    out_path = PROJECT_DIR / "scene-01-snowball.png"
    img.save(out_path, quality=95)
    print(f"  ✓ Đã xuất: {out_path.name}")


# ========================================================
# CẢNH 2: Biểu đồ Tăng trưởng: Tuyến tính vs Lãi kép (~15s)
# ========================================================
def draw_scene_02():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_title = get_font(64)
    f_head = get_font(44)
    f_sub = get_font(38)
    f_label = get_font(30)
    f_bold_tag = get_font(44)

    # 1. Tiêu đề
    draw.text((100, 45), "BIỂU ĐỒ: TUYẾN TÍNH VS CẤP SỐ NHÂN", fill=(20, 30, 55), font=f_title)
    draw.line([(100, 125), (1400, 125)], fill=(38, 103, 255), width=5)

    # 2. Khung biểu đồ tổng thể
    box_x0, box_y0, box_x1, box_y1 = 100, 160, 1820, 980
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=16, outline=(70, 90, 120), width=4)

    # Hệ trục tọa độ X - Y
    ox, oy = 260, 850
    xmax, ymax = 1680, 240

    # Trục hoành X (Thời gian / Năm)
    draw.line([(ox, oy), (xmax, oy)], fill=(30, 40, 60), width=5)
    draw.polygon([(xmax, oy), (xmax - 18, oy - 9), (xmax - 18, oy + 9)], fill=(30, 40, 60))
    draw.text((xmax - 260, oy + 25), "THỜI GIAN (NĂM)", fill=(30, 40, 60), font=f_label)

    # Trục tung Y (Tài sản $)
    draw.line([(ox, oy), (ox, ymax)], fill=(30, 40, 60), width=5)
    draw.polygon([(ox, ymax), (ox - 9, ymax + 18), (ox + 9, ymax + 18)], fill=(30, 40, 60))
    draw.text((ox - 30, ymax - 55), "TÀI SẢN TÍCH LŨY ($)", fill=(30, 40, 60), font=f_head)

    # Các mốc thời gian trên trục X
    milestones = [
        (ox, "0"),
        (ox + 300, "10 Năm"),
        (ox + 600, "20 Năm"),
        (ox + 900, "30 Năm"),
    ]
    for mx, mtxt in milestones:
        draw.line([(mx, oy), (mx, oy + 12)], fill=(70, 80, 100), width=3)
        draw.text((mx - 40, oy + 20), mtxt, fill=(70, 80, 100), font=f_label)

    # ĐƯỜNG 1: Tiết kiệm thông thường (Tuyến tính - Linear)
    draw.line([(ox, oy), (ox + 1350, oy - 230)], fill=(120, 140, 165), width=5)
    draw.text((1250, 660), "TIẾT KIỆM ĐƠN (TUYẾN TÍNH)", fill=(90, 105, 125), font=f_sub)

    # ĐƯỜNG 2: Lãi Kép (Exponential Curve)
    pts = []
    num_steps = 100
    for i in range(num_steps + 1):
        t = i / num_steps
        px = ox + t * 1320
        norm_y = (math.exp(t * 3.4) - 1.0) / (math.exp(3.4) - 1.0)
        py = oy - norm_y * 560
        pts.append((px, py))

    # Vẽ đường cong nét dày
    for k in range(len(pts) - 1):
        draw.line([pts[k], pts[k + 1]], fill=(220, 38, 38), width=7)

    # Nhãn đường Lãi Kép
    draw.text((1180, 240), "LÃI KÉP (CẤP SỐ NHÂN)", fill=(220, 38, 38), font=f_bold_tag)

    # ĐIỂM BÙNG PHÁT (Tipping Point)
    tip_x, tip_y = ox + 680, oy - 125
    draw.ellipse([tip_x - 30, tip_y - 30, tip_x + 30, tip_y + 30], outline=(245, 158, 11), width=5)

    # Hộp chú thích Điểm bùng phát (nằm góc trên bên trái điểm uốn, thoáng đãng)
    box_tip_x0, box_tip_y0 = tip_x - 440, tip_y - 250
    box_tip_x1, box_tip_y1 = tip_x - 10, tip_y - 140
    draw.rounded_rectangle([box_tip_x0, box_tip_y0, box_tip_x1, box_tip_y1], radius=12, outline=(245, 158, 11), width=3)
    draw.text((box_tip_x0 + 20, box_tip_y0 + 15), "ĐIỂM BÙNG PHÁT (TIPPING POINT)", fill=(180, 50, 40), font=get_font(26))
    draw.text((box_tip_x0 + 20, box_tip_y0 + 60), "Sau mốc này, tiền tăng theo phương thẳng đứng!", fill=(40, 50, 70), font=get_font(18))

    # Mũi tên chỉ từ hộp chú thích vào điểm bùng phát
    draw.line([(box_tip_x1 - 40, box_tip_y1), (tip_x - 15, tip_y - 15)], fill=(245, 158, 11), width=4)
    draw.polygon([(tip_x - 10, tip_y - 10), (tip_x - 28, tip_y - 14), (tip_x - 18, tip_y - 28)], fill=(245, 158, 11))

    out_path = PROJECT_DIR / "scene-02-chart.png"
    img.save(out_path, quality=95)
    print(f"  ✓ Đã xuất: {out_path.name}")


# ========================================================
# CẢNH 3: Sơ đồ tư duy (Mindmap) 3 Chân kiềng cốt lõi (~16s)
# ========================================================
def draw_scene_03():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_title = get_font(64)
    f_formula = get_font(42)
    f_head = get_font(42)
    f_sub = get_font(36)
    f_label = get_font(30)

    # 1. Tiêu đề
    draw.text((100, 45), "3 CHÂN KIỀNG TẠO NÊN LÃI KÉP", fill=(20, 30, 55), font=f_title)
    draw.line([(100, 125), (1200, 125)], fill=(38, 103, 255), width=5)

    # 2. Node trung tâm Mindmap (rộng rãi)
    c_x, c_y = 960, 220
    draw.rounded_rectangle([c_x - 420, c_y - 65, c_x + 420, c_y + 65], radius=18, outline=(38, 103, 255), width=5)
    draw.text((c_x - 275, c_y - 48), "CÔNG THỨC:  A = P × (1 + r)^t", fill=(20, 30, 60), font=f_formula)
    draw.text((c_x - 190, c_y + 8), "3 YẾU TỐ QUYẾT ĐỊNH THẮNG LỢI", fill=(180, 50, 40), font=f_label)

    # Các đường nối Mindmap từ tâm tỏa xuống 3 nhánh
    draw.line([(c_x - 250, c_y + 65), (380, 350)], fill=(38, 103, 255), width=4)
    draw.line([(c_x, c_y + 65), (960, 350)], fill=(41, 167, 102), width=4)
    draw.line([(c_x + 250, c_y + 65), (1540, 350)], fill=(220, 38, 38), width=5)

    # ----------------------------------------------------
    # NHÁNH 1 (Trái): Vốn ban đầu (P)
    # ----------------------------------------------------
    k1_x0, k1_y0, k1_x1, k1_y1 = 100, 350, 660, 970
    draw.rounded_rectangle([k1_x0, k1_y0, k1_x1, k1_y1], radius=16, outline=(38, 103, 255), width=4)
    draw.text((140, 385), "1. VỐN BAN ĐẦU (P)", fill=(38, 103, 255), font=f_head)
    draw.text((140, 450), "Principal Amount", fill=(80, 95, 115), font=f_label)
    draw.line([(140, 500), (620, 500)], fill=(200, 210, 225), width=2)

    # Icon Túi tiền 💰
    px, py = 380, 620
    draw.ellipse([px - 60, py - 30, px + 60, py + 70], outline=(38, 103, 255), width=5)
    draw.polygon([(px - 35, py - 30), (px + 35, py - 30), (px + 20, py - 60), (px - 20, py - 60)], outline=(38, 103, 255), fill=(245, 235, 215))
    draw.text((px - 14, py - 5), "$", fill=(38, 103, 255), font=get_font(52))

    draw.text((140, 760), "• Không cần số vốn quá lớn", fill=(40, 50, 75), font=f_sub)
    draw.text((140, 830), "• Quan trọng là sự đều đặn", fill=(40, 50, 75), font=f_sub)
    draw.text((140, 900), "• Tích tiểu thành đại", fill=(70, 85, 105), font=f_label)

    # ----------------------------------------------------
    # NHÁNH 2 (Giữa): Lãi suất (r)
    # ----------------------------------------------------
    k2_x0, k2_y0, k2_x1, k2_y1 = 690, 350, 1230, 970
    draw.rounded_rectangle([k2_x0, k2_y0, k2_x1, k2_y1], radius=16, outline=(41, 167, 102), width=4)
    draw.text((730, 385), "2. LÃI SUẤT (r)", fill=(41, 167, 102), font=f_head)
    draw.text((730, 450), "Interest Rate (%)", fill=(80, 95, 115), font=f_label)
    draw.line([(730, 500), (1190, 500)], fill=(200, 210, 225), width=2)

    # Icon Biểu đồ cột tăng trưởng 📈
    gx, gy = 960, 630
    draw.rounded_rectangle([gx - 75, gy + 10, gx - 35, gy + 70], radius=4, outline=(41, 167, 102), width=4)
    draw.rounded_rectangle([gx - 20, gy - 20, gx + 20, gy + 70], radius=4, outline=(41, 167, 102), width=4)
    draw.rounded_rectangle([gx + 35, gy - 55, gx + 75, gy + 70], radius=4, outline=(41, 167, 102), width=4)
    draw.line([(gx - 70, gy - 20), (gx + 75, gy - 75)], fill=(220, 38, 38), width=5)

    draw.text((730, 760), "• Tỷ suất sinh lời bình quân", fill=(40, 50, 75), font=f_sub)
    draw.text((730, 830), "• Khoảng 8% - 12% / năm", fill=(40, 50, 75), font=f_sub)
    draw.text((730, 900), "• Tránh rủi ro mất vốn", fill=(70, 85, 105), font=f_label)

    # ----------------------------------------------------
    # NHÁNH 3 (Phải): Thời gian (t) - Đòn bẩy quyền năng nhất
    # ----------------------------------------------------
    k3_x0, k3_y0, k3_x1, k3_y1 = 1260, 330, 1820, 980
    draw.rounded_rectangle([k3_x0, k3_y0, k3_x1, k3_y1], radius=18, outline=(220, 38, 38), width=5)
    draw.text((1300, 370), "3. THỜI GIAN (t)", fill=(220, 38, 38), font=f_head)
    draw.text((1300, 435), "ĐÒN BẨY SỐ 1!", fill=(180, 50, 40), font=get_font(38))
    draw.line([(1300, 490), (1780, 490)], fill=(220, 38, 38), width=3)

    # Icon Đồng hồ cát ⏳
    hx, hy = 1540, 600
    draw.line([(hx - 55, hy - 65), (hx + 55, hy - 65)], fill=(220, 38, 38), width=6)
    draw.line([(hx - 55, hy + 65), (hx + 55, hy + 65)], fill=(220, 38, 38), width=6)
    draw.polygon([(hx - 50, hy - 60), (hx + 50, hy - 60), (hx, hy), (hx, hy)], outline=(20, 30, 55), width=4)
    draw.polygon([(hx - 50, hy + 60), (hx + 50, hy + 60), (hx, hy), (hx, hy)], outline=(20, 30, 55), width=4)
    draw.ellipse([hx - 8, hy + 30, hx + 8, hy + 46], fill=(245, 158, 11))

    draw.text((1300, 740), "• Là số mũ (t) trong công thức", fill=(220, 38, 38), font=f_sub)
    draw.text((1300, 810), "• Thời gian dài -> Bùng nổ", fill=(20, 30, 60), font=get_font(32))
    draw.text((1300, 885), "-> BẮT ĐẦU CÀNG SỚM CÀNG TỐT!", fill=(180, 50, 40), font=get_font(26))

    out_path = PROJECT_DIR / "scene-03-mindmap.png"
    img.save(out_path, quality=95)
    print(f"  ✓ Đã xuất: {out_path.name}")


# ========================================================
# CẢNH 4: Infographic So sánh 2 mốc tuổi & Hành động (~13s)
# ========================================================
def draw_scene_04():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_title = get_font(62)
    f_head = get_font(44)
    f_big_stat = get_font(52)
    f_sub = get_font(36)
    f_label = get_font(30)
    f_cta = get_font(44)

    # 1. Tiêu đề
    draw.text((100, 45), "SO SÁNH: BẮT ĐẦU TUỔI 20 VS TUỔI 30", fill=(20, 30, 55), font=f_title)
    draw.line([(100, 125), (1450, 125)], fill=(38, 103, 255), width=5)

    # 2. Hai cột so sánh Infographic đối xứng
    # CỘT A: Bắt đầu năm 20 tuổi
    a_x0, a_y0, a_x1, a_y1 = 100, 160, 920, 780
    draw.rounded_rectangle([a_x0, a_y0, a_x1, a_y1], radius=16, outline=(41, 167, 102), width=5)

    draw.text((140, 195), "NGƯỜI A: BẮT ĐẦU Ở TUỔI 20", fill=(41, 167, 102), font=f_head)
    draw.text((140, 260), "Đầu tư sớm 10 năm so với người B", fill=(70, 85, 105), font=f_label)
    draw.line([(140, 305), (880, 305)], fill=(200, 210, 225), width=2)

    # Biểu đồ cột tài sản Người A (Rất cao)
    draw.rounded_rectangle([200, 340, 360, 720], radius=10, fill=(41, 167, 102), outline=(20, 30, 50), width=4)
    draw.text((230, 480), "3X", fill=(255, 255, 255), font=get_font(64))

    draw.text((400, 380), "TÀI SẢN:", fill=(70, 85, 105), font=f_sub)
    draw.text((400, 440), "GẤP 3 LẦN!", fill=(41, 167, 102), font=f_big_stat)
    draw.text((400, 530), "• Vốn bỏ ra ít hơn", fill=(30, 40, 60), font=f_sub)
    draw.text((400, 600), "• Thời gian tích lũy 40 năm", fill=(30, 40, 60), font=f_sub)
    draw.text((400, 670), "-> An nhàn tự do tài chính", fill=(41, 167, 102), font=f_sub)

    # CỘT B: Bắt đầu năm 30 tuổi
    b_x0, b_y0, b_x1, b_y1 = 1000, 160, 1820, 780
    draw.rounded_rectangle([b_x0, b_y0, b_x1, b_y1], radius=16, outline=(160, 175, 195), width=4)

    draw.text((1040, 195), "NGƯỜI B: BẮT ĐẦU Ở TUỔI 30", fill=(180, 50, 40), font=f_head)
    draw.text((1040, 260), "Chần chừ 10 năm mới bắt đầu đầu tư", fill=(70, 85, 105), font=f_label)
    draw.line([(1040, 305), (1780, 305)], fill=(200, 210, 225), width=2)

    # Biểu đồ cột tài sản Người B (Chỉ cao 1/3)
    draw.rounded_rectangle([1100, 580, 1260, 720], radius=10, fill=(180, 190, 205), outline=(20, 30, 50), width=4)
    draw.text((1140, 620), "1X", fill=(20, 30, 50), font=get_font(54))

    draw.text((1300, 380), "TÀI SẢN:", fill=(70, 85, 105), font=f_sub)
    draw.text((1300, 440), "CHỈ ĐẠT 1/3", fill=(180, 50, 40), font=f_big_stat)
    draw.text((1300, 530), "• Dù mỗi tháng cố bỏ vốn nhiều hơn", fill=(80, 95, 115), font=f_sub)
    draw.text((1300, 600), "• Thời gian chỉ còn 30 năm", fill=(80, 95, 115), font=f_sub)
    draw.text((1300, 670), "-> Khó đuổi kịp người bắt đầu sớm", fill=(180, 50, 40), font=f_sub)

    # 3. Khung Thông điệp Kêu gọi Hành động dưới đáy
    cta_x0, cta_y0, cta_x1, cta_y1 = 100, 815, 1820, 980
    draw.rounded_rectangle([cta_x0, cta_y0, cta_x1, cta_y1], radius=16, outline=(245, 158, 11), width=4)

    # Icon Tên lửa 🚀
    rx, ry = 220, 895
    draw.polygon([(rx, ry - 40), (rx + 25, ry + 20), (rx - 25, ry + 20)], outline=(220, 38, 38), fill=(245, 235, 215), width=4)
    draw.line([(rx - 25, ry + 20), (rx - 35, ry + 40)], fill=(245, 158, 11), width=4)
    draw.line([(rx + 25, ry + 20), (rx + 35, ry + 40)], fill=(245, 158, 11), width=4)
    draw.ellipse([rx - 8, ry - 10, rx + 8, ry + 6], fill=(38, 103, 255))

    draw.text((290, 840), "THÔNG ĐIỆP: BẮT ĐẦU SỚM > ĐẦU TƯ NHIỀU", fill=(180, 50, 40), font=f_cta)
    draw.text((290, 910), "Hãy gieo hạt giống tài chính của bạn ngay hôm nay!", fill=(20, 30, 60), font=f_sub)

    out_path = PROJECT_DIR / "scene-04-comparison.png"
    img.save(out_path, quality=95)
    print(f"  ✓ Đã xuất: {out_path.name}")


if __name__ == "__main__":
    print("=" * 60)
    print("Bắt đầu tạo bộ 4 ảnh bảng trắng cho 'Sức Mạnh Lãi Kép'...")
    print("=" * 60)
    draw_scene_01()
    draw_scene_02()
    draw_scene_03()
    draw_scene_04()
    print("=" * 60)
    print("Hoàn tất tạo 4 ảnh cảnh vẽ!")
