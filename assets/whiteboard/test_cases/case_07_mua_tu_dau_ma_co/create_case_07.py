#!/usr/bin/env python3
"""
Tạo ảnh minh họa bảng trắng (1920x1080) và file annotation.json chuẩn cho Test Case 7:
Chủ đề: "Mưa từ đâu mà có? (Vòng tuần hoàn của nước)"
Chuẩn mực:
- Nền trắng thuần #FFFFFF.
- Bố cục Process Flow / Cycle khép kín, phân vùng ZERO OVERLAP.
- Mọi nhãn chữ nằm trọn vẹn trong vùng, có lề thoáng 20-30px.
- Tỉ lệ ink:color = 90:10 (Chữ, mũi tên, khung = 100% ink; icon = wash nhanh).
"""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont

DIR = Path(__file__).resolve().parent
IMG_PATH = DIR / "scene-01-vong-tuan-hoan-nuoc.png"
ANN_PATH = DIR / "scene-01-vong-tuan-hoan-nuoc.annotation.json"

W, H = 1920, 1080
BG_COLOR = (255, 255, 255)  # Nền trắng chuẩn #FFFFFF


def get_font(size: int, bold: bool = True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_arrow(draw, start, end, color, width=4, arrow_len=18):
    """Vẽ đường thẳng có đầu mũi tên nhọn."""
    x0, y0 = start
    x1, y1 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - arrow_len * math.cos(angle - math.pi / 6),
          y1 - arrow_len * math.sin(angle - math.pi / 6))
    p2 = (x1 - arrow_len * math.cos(angle + math.pi / 6),
          y1 - arrow_len * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=color)


def draw_curved_arrow(draw, points, color, width=5, arrow_len=18):
    """Vẽ đường cong qua các điểm có đầu mũi tên ở điểm cuối."""
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    p_last = points[-1]
    p_prev = points[-2]
    angle = math.atan2(p_last[1] - p_prev[1], p_last[0] - p_prev[0])
    p1 = (p_last[0] - arrow_len * math.cos(angle - math.pi / 6),
          p_last[1] - arrow_len * math.sin(angle - math.pi / 6))
    p2 = (p_last[0] - arrow_len * math.cos(angle + math.pi / 6),
          p_last[1] - arrow_len * math.sin(angle + math.pi / 6))
    draw.polygon([p_last, p1, p2], fill=color)


def create_scene_image():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_title = get_font(44, bold=True)
    f_sub = get_font(28, bold=True)
    f_box_title = get_font(32, bold=True)
    f_body = get_font(26, bold=True)
    f_label = get_font(22, bold=False)

    # -------------------------------------------------------------
    # 1. ZONE 1: Tiêu đề đỉnh (x: 200, y: 30, w: 1520, h: 110)
    # -------------------------------------------------------------
    title_text = "VÒNG TUẦN HOÀN CỦA NƯỚC: MƯA TỪ ĐÂU MÀ CÓ?"
    draw.text((360, 48), title_text, fill=(30, 41, 59), font=f_title)
    draw.line([(320, 112), (1600, 112)], fill=(37, 99, 235), width=4)

    # -------------------------------------------------------------
    # 2. ZONE 2: Icon Mặt trời tỏa nắng (x: 80, y: 150, w: 440, h: 280)
    # -------------------------------------------------------------
    sun_cx, sun_cy, sun_r = 300, 265, 48
    # Vẽ các tia nắng tỏa ra
    for i in range(12):
        ang = i * (math.pi / 6)
        r1 = sun_r + 10
        r2 = sun_r + 26 if i % 2 == 0 else sun_r + 18
        draw.line([(sun_cx + r1 * math.cos(ang), sun_cy + r1 * math.sin(ang)),
                   (sun_cx + r2 * math.cos(ang), sun_cy + r2 * math.sin(ang))],
                  fill=(245, 158, 11), width=4)
    # Vòng tròn mặt trời
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=(254, 240, 138), outline=(234, 88, 12), width=4)
    # Mắt và nụ cười thân thiện
    draw.ellipse([sun_cx - 18, sun_cy - 10, sun_cx - 10, sun_cy + 2], fill=(234, 88, 12))
    draw.ellipse([sun_cx + 10, sun_cy - 10, sun_cx + 18, sun_cy + 2], fill=(234, 88, 12))
    draw.arc([sun_cx - 15, sun_cy - 5, sun_cx + 15, sun_cy + 22], start=10, end=170, fill=(234, 88, 12), width=3)
    # Tia nhiệt chiếu chéo xuống
    draw.line([(270, 335), (250, 375)], fill=(245, 158, 11), width=3)
    draw.line([(300, 338), (300, 380)], fill=(245, 158, 11), width=3)
    draw.line([(330, 335), (350, 375)], fill=(245, 158, 11), width=3)
    # Khung nhãn ÁNH NẮNG MẶT TRỜI
    draw.rounded_rectangle([180, 385, 420, 422], radius=8, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((205, 392), "ÁNH NẮNG MẶT TRỜI", fill=(180, 83, 9), font=f_label)

    # -------------------------------------------------------------
    # 3. ZONE 5: Cụm đám mây ngưng tụ (x: 1360, y: 150, w: 480, h: 270)
    # -------------------------------------------------------------
    cloud_ox, cloud_oy = 1420, 175
    # Đám mây bồng bềnh
    draw.ellipse([cloud_ox + 40, cloud_oy + 40, cloud_ox + 170, cloud_oy + 140], fill=(240, 249, 255), outline=(51, 65, 85), width=4)
    draw.ellipse([cloud_ox + 120, cloud_oy + 10, cloud_ox + 280, cloud_oy + 130], fill=(240, 249, 255), outline=(51, 65, 85), width=4)
    draw.ellipse([cloud_ox + 230, cloud_oy + 30, cloud_ox + 360, cloud_oy + 140], fill=(240, 249, 255), outline=(51, 65, 85), width=4)
    draw.rectangle([cloud_ox + 70, cloud_oy + 80, cloud_ox + 320, cloud_oy + 140], fill=(240, 249, 255))
    draw.line([(cloud_ox + 40, cloud_oy + 140), (cloud_ox + 360, cloud_oy + 140)], fill=(51, 65, 85), width=4)
    # Khung nhãn 2. NGƯNG TỤ
    draw.rounded_rectangle([1480, 350, 1760, 402], radius=8, fill=(238, 242, 255), outline=(79, 70, 229), width=3)
    draw.text((1525, 360), "2. NGƯNG TỤ", fill=(67, 56, 202), font=f_sub)

    # -------------------------------------------------------------
    # 4. ZONE 8: Khung chu trình khép kín ở giữa (x: 580, y: 160, w: 720, h: 580)
    # -------------------------------------------------------------
    box_x0, box_y0, box_x1, box_y1 = 600, 180, 1280, 720
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=16, fill=(255, 255, 255), outline=(30, 41, 59), width=3)
    draw.rounded_rectangle([box_x0 + 6, box_y0 + 6, box_x1 - 6, box_y1 - 6], radius=12, fill=None, outline=(203, 213, 225), width=2)

    # Tiêu đề trung tâm
    draw.text((740, 210), "CHU TRÌNH TUẦN HOÀN", fill=(220, 38, 38), font=f_box_title)
    draw.line([(730, 260), (1190, 260)], fill=(220, 38, 38), width=2)

    # Vòng tròn mũi tên chu trình
    c_cx, c_cy, c_r = 940, 385, 75
    draw.arc([c_cx - c_r, c_cy - c_r, c_cx + c_r, c_cy + c_r], start=185, end=265, fill=(13, 148, 136), width=4)
    draw.arc([c_cx - c_r, c_cy - c_r, c_cx + c_r, c_cy + c_r], start=275, end=355, fill=(79, 70, 229), width=4)
    draw.arc([c_cx - c_r, c_cy - c_r, c_cx + c_r, c_cy + c_r], start=5, end=85, fill=(220, 38, 38), width=4)
    draw.arc([c_cx - c_r, c_cy - c_r, c_cx + c_r, c_cy + c_r], start=95, end=175, fill=(37, 99, 235), width=4)

    draw.text((875, 370), "KHÉP KÍN", fill=(30, 41, 59), font=f_body)

    # Tóm tắt các giai đoạn (dùng dấu -> chuẩn font)
    draw.text((650, 500), "• Bốc hơi   ->   Ngưng tụ   ->   Mưa rơi", fill=(15, 23, 42), font=f_body)
    draw.text((650, 560), "• Dòng nước liên tục luân chuyển không ngừng", fill=(71, 85, 105), font=f_body)
    draw.text((650, 620), "• Tổng lượng nước Trái Đất luôn được bảo toàn", fill=(71, 85, 105), font=f_body)

    # -------------------------------------------------------------
    # 5. ZONE 4: Hơi nước bốc lên (x: 80, y: 440, w: 440, h: 300)
    # -------------------------------------------------------------
    # Khung nhãn 1. BỐC HƠI
    draw.rounded_rectangle([190, 460, 410, 512], radius=8, fill=(240, 253, 250), outline=(13, 148, 136), width=3)
    draw.text((235, 470), "1. BỐC HƠI", fill=(15, 118, 110), font=f_sub)
    # 3 mũi tên lượn sóng bốc thẳng lên trời
    for col_x in [220, 300, 380]:
        wave_pts = []
        for wy in range(710, 535, -12):
            wx = col_x + 10 * math.sin((wy - 535) * 0.1)
            wave_pts.append((wx, wy))
        draw_curved_arrow(draw, wave_pts, color=(13, 148, 136), width=4, arrow_len=14)

    # -------------------------------------------------------------
    # 6. ZONE 6: Mưa rơi xuống đất & núi (x: 1360, y: 440, w: 480, h: 350)
    # -------------------------------------------------------------
    # Khung nhãn 3. MƯA RƠI
    draw.rounded_rectangle([1490, 460, 1730, 512], radius=8, fill=(254, 242, 242), outline=(220, 38, 38), width=3)
    draw.text((1540, 470), "3. MƯA RƠI", fill=(185, 28, 28), font=f_sub)
    # Các vệt giọt mưa chéo màu xanh đậm
    rain_drops = [
        ((1470, 535), (1450, 570)), ((1530, 530), (1510, 565)), ((1590, 540), (1570, 575)),
        ((1660, 530), (1640, 565)), ((1720, 535), (1700, 570)),
        ((1450, 595), (1430, 630)), ((1510, 590), (1490, 625)), ((1570, 600), (1550, 635)),
        ((1640, 585), (1620, 620)), ((1700, 595), (1680, 630)),
        ((1480, 655), (1460, 690)), ((1550, 650), (1530, 685)), ((1620, 660), (1600, 695)),
    ]
    for p_start, p_end in rain_drops:
        draw.line([p_start, p_end], fill=(37, 99, 235), width=3)
    # Mũi tên rơi xuống sườn núi
    draw_arrow(draw, (1780, 535), (1780, 675), color=(220, 38, 38), width=4, arrow_len=16)
    # Dãy núi đón mưa ở dưới
    mt_pts = [(1390, 770), (1490, 690), (1580, 750), (1690, 680), (1810, 770)]
    draw.polygon(mt_pts, fill=(241, 245, 249), outline=(71, 85, 105))
    draw.line([(1390, 770), (1810, 770)], fill=(71, 85, 105), width=3)

    # -------------------------------------------------------------
    # 7. ZONE 3: Mặt nước sông & đại dương (x: 80, y: 760, w: 560, h: 280)
    # -------------------------------------------------------------
    # Khung nhãn SÔNG & ĐẠI DƯƠNG
    draw.rounded_rectangle([170, 780, 530, 832], radius=8, fill=(219, 234, 254), outline=(37, 99, 235), width=2)
    draw.text((215, 790), "SÔNG & ĐẠI DƯƠNG", fill=(29, 78, 216), font=f_sub)
    # Mảng nước xanh và các làn sóng biển
    draw.rounded_rectangle([110, 845, 600, 1010], radius=16, fill=(239, 246, 255), outline=(37, 99, 235), width=3)
    for row_y in [885, 925, 965]:
        pts = []
        for sx in range(130, 580, 15):
            sy = row_y + 4 * math.sin((sx - 130) * 0.08)
            pts.append((sx, sy))
        for j in range(len(pts) - 1):
            draw.line([pts[j], pts[j+1]], fill=(29, 78, 216), width=3)

    # -------------------------------------------------------------
    # 8. ZONE 7: Dòng chảy hồi lưu về biển (x: 660, y: 760, w: 1180, h: 280)
    # -------------------------------------------------------------
    # Khung nhãn 4. DÒNG CHẢY HỒI LƯU
    draw.rounded_rectangle([1020, 780, 1480, 832], radius=8, fill=(239, 246, 255), outline=(37, 99, 235), width=3)
    draw.text((1065, 790), "4. DÒNG CHẢY HỒI LƯU", fill=(29, 78, 216), font=f_sub)
    # Dòng sông từ núi (phải) đổ về biển (trái)
    river_top = []
    river_bot = []
    for rx in range(1800, 680, -20):
        t_offset = 12 * math.sin((rx - 680) * 0.015)
        river_top.append((rx, 910 + t_offset))
        river_bot.append((rx, 975 + t_offset))
    river_poly = river_top + list(reversed(river_bot))
    draw.polygon(river_poly, fill=(224, 242, 254), outline=(37, 99, 235))
    # Mũi tên uốn lượn chỉ hướng chảy về biển
    flow_arrow_pts = [(1650, 942), (1400, 938), (1150, 948), (900, 942), (720, 942)]
    draw_curved_arrow(draw, flow_arrow_pts, color=(37, 99, 235), width=5, arrow_len=20)

    img.save(IMG_PATH, quality=95)
    print(f"  ✓ Đã tạo ảnh hoàn hảo: {IMG_PATH}")


def create_annotation_file():
    annotation = {
        "sceneId": "scene-01-vong-tuan-hoan-nuoc",
        "canvas": {"width": W, "height": H},
        "storyBasis": "Vòng tuần hoàn của nước: Ánh nắng làm ấm biển -> Bốc hơi -> Ngưng tụ thành mây -> Mưa rơi -> Dòng chảy hồi lưu về sông biển khép kín chu trình.",
        "sceneDurationMs": 33500,
        "elements": [
            {
                "id": "el-01-title",
                "label": "Tiêu đề: VÒNG TUẦN HOÀN CỦA NƯỚC",
                "sequence": 1,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Giới thiệu chủ đề bài giảng khoa học",
                "subtitle": "Bạn có bao giờ tự hỏi: những giọt mưa từ đâu rơi xuống?",
                "region": {"x": 200, "y": 30, "width": 1520, "height": 110},
                "reveal": {
                    "direction": "left_to_right",
                    "startMs": 300,
                    "durationMs": 1800,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-02-sun",
                "label": "Icon Mặt trời tỏa nắng ấm áp",
                "sequence": 2,
                "type": "colored_image",
                "colorMode": "wash",
                "narrativeRole": "Nguồn nhiệt năng khởi đầu chu trình",
                "subtitle": "Bạn có bao giờ tự hỏi: những giọt mưa từ đâu rơi xuống?",
                "region": {"x": 80, "y": 150, "width": 440, "height": 280},
                "reveal": {
                    "direction": "top_to_bottom",
                    "startMs": 2200,
                    "durationMs": 2200,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-03-ocean",
                "label": "Mặt nước Sông & Đại dương",
                "sequence": 3,
                "type": "colored_image",
                "colorMode": "wash",
                "narrativeRole": "Nguồn nước hấp thu nhiệt lượng mặt trời",
                "subtitle": "Mọi thứ bắt đầu khi ánh nắng mặt trời làm ấm các dòng sông và đại dương.",
                "region": {"x": 80, "y": 760, "width": 560, "height": 280},
                "reveal": {
                    "direction": "left_to_right",
                    "startMs": 4900,
                    "durationMs": 4800,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-04-evaporation",
                "label": "3 Mũi tên lượn sóng: 1. BỐC HƠI",
                "sequence": 4,
                "type": "arrow",
                "colorMode": "none",
                "narrativeRole": "Hơi nước bốc lên từ mặt biển",
                "subtitle": "Nước ấm dần lên, biến thành hơi nước nhẹ bay vút lên bầu trời.",
                "region": {"x": 80, "y": 440, "width": 440, "height": 300},
                "reveal": {
                    "direction": "bottom_to_top",
                    "startMs": 10400,
                    "durationMs": 4500,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-05-cloud",
                "label": "Cụm đám mây: 2. NGƯNG TỤ",
                "sequence": 5,
                "type": "colored_image",
                "colorMode": "wash",
                "narrativeRole": "Hơi nước ngưng tụ thành mây trắng",
                "subtitle": "Lên cao gặp lạnh, các hạt hơi nước gom lại thành những đám mây trắng.",
                "region": {"x": 1360, "y": 150, "width": 480, "height": 270},
                "reveal": {
                    "direction": "left_to_right",
                    "startMs": 15800,
                    "durationMs": 4800,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-06-rain",
                "label": "Mưa rơi xuống sườn núi: 3. MƯA RƠI",
                "sequence": 6,
                "type": "arrow",
                "colorMode": "none",
                "narrativeRole": "Mây nặng hạt tạo thành cơn mưa rơi xuống",
                "subtitle": "Khi mây quá nặng, nước rơi xuống mặt đất tạo thành những cơn mưa.",
                "region": {"x": 1360, "y": 440, "width": 480, "height": 350},
                "reveal": {
                    "direction": "top_to_bottom",
                    "startMs": 21400,
                    "durationMs": 4700,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-07-river-flow",
                "label": "Dòng sông hồi lưu: 4. DÒNG CHẢY HỒI LƯU",
                "sequence": 7,
                "type": "arrow",
                "colorMode": "none",
                "narrativeRole": "Dòng nước từ sườn núi chảy về biển",
                "subtitle": "Nước mưa chảy về sông suối, tiếp tục một vòng tuần hoàn bất tận.",
                "region": {"x": 660, "y": 760, "width": 1180, "height": 280},
                "reveal": {
                    "direction": "right_to_left",
                    "startMs": 26900,
                    "durationMs": 3800,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            },
            {
                "id": "el-08-cycle-box",
                "label": "Khung trung tâm: CHU TRÌNH KHÉP KÍN",
                "sequence": 8,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Đúc kết quy luật tuần hoàn bất tận của nước",
                "subtitle": "Nước mưa chảy về sông suối, tiếp tục một vòng tuần hoàn bất tận.",
                "region": {"x": 580, "y": 160, "width": 720, "height": 580},
                "reveal": {
                    "direction": "top_to_bottom",
                    "startMs": 30800,
                    "durationMs": 1700,
                    "maskPaddingPx": 10,
                    "protectedRegions": []
                }
            }
        ]
    }
    ANN_PATH.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Đã tạo annotation thành công: {ANN_PATH}")


if __name__ == "__main__":
    print("=" * 60)
    print("Khởi tạo Scene & Annotation cho Case 07 (Vòng tuần hoàn nước)...")
    print("=" * 60)
    create_scene_image()
    create_annotation_file()
    print("Hoàn tất!")
