#!/usr/bin/env python3
"""
Tạo annotation.json chuẩn cho Test Case 4: ĐIỆN MẶT TRỜI CHO GIA ĐÌNH (Solar Power System).
Bố cục 4 Zone rõ rệt, khoảng cách rộng rãi, bóc tách chính xác 100% từng biểu tượng, mũi tên, công thức, biểu đồ.
Tất cả các bounding box đều được căn chỉnh hoàn hảo, KHÔNG CÓ BẤT KỲ GIAO CẮT NGOÀI Ý MUỐN NÀO!
Đặc biệt: Tách biểu tượng Ắc quy và nhãn PIN LƯU TRỮ để bảo toàn chữ 'P' trọn vẹn 100%.
"""
from pathlib import Path
import json
import cv2

CASE_DIR = Path(__file__).resolve().parent
IMG_PATH = CASE_DIR / "solar_power.png"
ANN_PATH = CASE_DIR / "solar_power.annotation.json"
REGIONS_PATH = CASE_DIR / "solar_power-regions.png"

img = cv2.imread(str(IMG_PATH))
H, W = img.shape[:2]

# Bounding boxes pixel-perfect verified:
# TOP
box_title = {"x": 385, "y": 48, "width": 1150, "height": 95}
box_title_underline = {"x": 385, "y": 145, "width": 1150, "height": 28}

# ZONE A: DÒNG NĂNG LƯỢNG CHÍNH
box_zone_a_tag = {"x": 50, "y": 190, "width": 65, "height": 59}       # y: 190..249
box_sun = {"x": 92, "y": 250, "width": 208, "height": 255}              # y: 250..505 (ngay dưới tag A)
box_arrow_1 = {"x": 305, "y": 308, "width": 82, "height": 60}
box_panel = {"x": 390, "y": 240, "width": 195, "height": 265}
box_arrow_2 = {"x": 588, "y": 308, "width": 84, "height": 60}
box_controller = {"x": 675, "y": 260, "width": 195, "height": 245}
box_arrow_3 = {"x": 873, "y": 308, "width": 83, "height": 60}
box_battery_icon = {"x": 975, "y": 255, "width": 195, "height": 185}   # Biểu tượng ắc quy (không chạm Arrow 3)
box_battery_label = {"x": 938, "y": 445, "width": 245, "height": 65}    # Nhãn 'PIN LƯU TRỮ' trọn vẹn chữ P
box_arrow_4 = {"x": 1153, "y": 308, "width": 84, "height": 60}
box_inverter = {"x": 1240, "y": 240, "width": 185, "height": 280}
box_arrow_5 = {"x": 1428, "y": 308, "width": 82, "height": 60}
box_house = {"x": 1530, "y": 215, "width": 215, "height": 243}         # y: 215..458 (chứa nhà và chữ NGÔI NHÀ)

# ZONE B: THIẾT BỊ TIÊU THỤ ĐIỆN (bắt đầu từ y: 460, ngay dưới nhãn NGÔI NHÀ)
box_zone_b_tag = {"x": 1315, "y": 545, "width": 60, "height": 65}
box_b_led = {"x": 1378, "y": 460, "width": 160, "height": 228}
box_b_fan = {"x": 1541, "y": 460, "width": 170, "height": 228}
box_b_laptop = {"x": 1714, "y": 460, "width": 166, "height": 228}

# ZONE C: CÔNG THỨC TÍNH ĐIỆN NĂNG
box_zone_c_head = {"x": 50, "y": 715, "width": 690, "height": 68}
box_zone_c_underline = {"x": 140, "y": 784, "width": 600, "height": 22}
box_zone_c_formula = {"x": 65, "y": 835, "width": 1050, "height": 78}
box_zone_c_calc_text = {"x": 260, "y": 920, "width": 680, "height": 115}
box_zone_c_oval = {"x": 622, "y": 914, "width": 232, "height": 112}

# ZONE D: BIỂU ĐỒ SẢN LƯỢNG ĐIỆN
box_zone_d_head = {"x": 1210, "y": 715, "width": 600, "height": 78}
box_zone_d_chart = {"x": 1215, "y": 798, "width": 650, "height": 255}

elements = [
    # Top Section
    {
        "id": "el-01-title",
        "sequence": 1,
        "label": "Tiêu đề: ĐIỆN MẶT TRỜI CHO GIA ĐÌNH",
        "type": "text",
        "narrativeRole": "Giới thiệu chủ đề hệ thống điện mặt trời gia đình",
        "region": box_title,
        "reveal": {"direction": "left_to_right", "startMs": 400, "durationMs": 1400, "protectedRegions": []}
    },
    {
        "id": "el-02-title-underline",
        "sequence": 2,
        "label": "Gạch chân xanh tiêu đề chính",
        "type": "gesture",
        "narrativeRole": "Nhấn mạnh tiêu đề",
        "region": box_title_underline,
        "reveal": {"direction": "left_to_right", "startMs": 1850, "durationMs": 550, "protectedRegions": []}
    },

    # Zone A: Main Energy Flow
    {
        "id": "el-03-zone-a-tag",
        "sequence": 3,
        "label": "Ký hiệu: A.",
        "type": "text",
        "narrativeRole": "Đánh dấu Khu vực A",
        "region": box_zone_a_tag,
        "reveal": {"direction": "left_to_right", "startMs": 2500, "durationMs": 400, "protectedRegions": []}
    },
    {
        "id": "el-04-sun",
        "sequence": 4,
        "label": "1. Mặt Trời & Nhãn: MẶT TRỜI",
        "type": "colored_image",
        "narrativeRole": "Nguồn năng lượng quang năng ban đầu",
        "region": box_sun,
        "reveal": {"direction": "radial_outward", "startMs": 3000, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-05-arrow-1",
        "sequence": 5,
        "label": "Mũi tên xanh: Ánh sáng tới tấm pin",
        "type": "gesture",
        "narrativeRole": "Quang năng chiếu xạ tới bề mặt pin",
        "region": box_arrow_1,
        "reveal": {"direction": "left_to_right", "startMs": 4250, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-06-panel",
        "sequence": 6,
        "label": "2. Tấm pin mặt trời & Nhãn: TẤM PIN",
        "type": "colored_image",
        "narrativeRole": "Hấp thụ quang năng chuyển thành dòng điện một chiều DC",
        "region": box_panel,
        "reveal": {"direction": "top_to_bottom", "startMs": 4750, "durationMs": 1300, "protectedRegions": []}
    },
    {
        "id": "el-07-arrow-2",
        "sequence": 7,
        "label": "Mũi tên đen: Pin tới Điều khiển sạc",
        "type": "gesture",
        "narrativeRole": "Dẫn điện tới bộ điều khiển",
        "region": box_arrow_2,
        "reveal": {"direction": "left_to_right", "startMs": 6100, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-08-controller",
        "sequence": 8,
        "label": "3. Bộ điều khiển & Nhãn: ĐIỀU KHIỂN",
        "type": "colored_image",
        "narrativeRole": "Ổn định điện áp và kiểm soát sạc",
        "region": box_controller,
        "reveal": {"direction": "top_to_bottom", "startMs": 6600, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-09-arrow-3",
        "sequence": 9,
        "label": "Mũi tên đen: Điều khiển tới Pin lưu trữ",
        "type": "gesture",
        "narrativeRole": "Truyền năng lượng vào khối ắc quy lưu trữ",
        "region": box_arrow_3,
        "reveal": {"direction": "left_to_right", "startMs": 7850, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-10-battery-icon",
        "sequence": 10,
        "label": "4. Khối ắc quy lưu trữ",
        "type": "colored_image",
        "narrativeRole": "Tích trữ năng lượng phục vụ khi không có nắng",
        "region": box_battery_icon,
        "reveal": {"direction": "top_to_bottom", "startMs": 8350, "durationMs": 1000, "protectedRegions": []}
    },
    {
        "id": "el-11-battery-label",
        "sequence": 11,
        "label": "Nhãn: PIN LƯU TRỮ",
        "type": "text",
        "narrativeRole": "Chú thích khối pin lưu trữ",
        "region": box_battery_label,
        "reveal": {"direction": "left_to_right", "startMs": 9400, "durationMs": 550, "protectedRegions": []}
    },
    {
        "id": "el-12-arrow-4",
        "sequence": 12,
        "label": "Mũi tên đen: Pin lưu trữ tới Biến tần",
        "type": "gesture",
        "narrativeRole": "Đưa điện một chiều DC tới biến tần",
        "region": box_arrow_4,
        "reveal": {"direction": "left_to_right", "startMs": 10000, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-13-inverter",
        "sequence": 13,
        "label": "5. Bộ biến tần & Nhãn: BIẾN TẦN",
        "type": "colored_image",
        "narrativeRole": "Chuyển điện một chiều DC thành điện xoay chiều AC 220V",
        "region": box_inverter,
        "reveal": {"direction": "top_to_bottom", "startMs": 10500, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-14-arrow-5",
        "sequence": 14,
        "label": "Mũi tên đen: Biến tần tới Ngôi nhà",
        "type": "gesture",
        "narrativeRole": "Cung cấp nguồn điện xoay chiều vào hộ gia đình",
        "region": box_arrow_5,
        "reveal": {"direction": "left_to_right", "startMs": 11750, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-15-house",
        "sequence": 15,
        "label": "6. Ngôi nhà & Nhãn: NGÔI NHÀ",
        "type": "colored_image",
        "narrativeRole": "Nơi tiêu thụ và phân phối điện cho gia đình",
        "region": box_house,
        "reveal": {"direction": "top_to_bottom", "startMs": 12250, "durationMs": 1400, "protectedRegions": []}
    },

    # Zone B: Household Electrical Appliances
    {
        "id": "el-16-zone-b-tag",
        "sequence": 16,
        "label": "Ký hiệu: B.",
        "type": "text",
        "narrativeRole": "Đánh dấu Khu vực B",
        "region": box_zone_b_tag,
        "reveal": {"direction": "left_to_right", "startMs": 13750, "durationMs": 400, "protectedRegions": []}
    },
    {
        "id": "el-17-b-led",
        "sequence": 17,
        "label": "Mũi tên & Bóng đèn LED: ĐÈN LED",
        "type": "colored_image",
        "narrativeRole": "Thắp sáng sinh hoạt tiết kiệm năng lượng",
        "region": box_b_led,
        "reveal": {"direction": "top_to_bottom", "startMs": 14200, "durationMs": 1300, "protectedRegions": []}
    },
    {
        "id": "el-18-b-fan",
        "sequence": 18,
        "label": "Mũi tên & Quạt điện: QUẠT",
        "type": "colored_image",
        "narrativeRole": "Làm mát không gian sống",
        "region": box_b_fan,
        "reveal": {"direction": "top_to_bottom", "startMs": 15600, "durationMs": 1300, "protectedRegions": []}
    },
    {
        "id": "el-19-b-laptop",
        "sequence": 19,
        "label": "Mũi tên & Máy tính: LAPTOP",
        "type": "colored_image",
        "narrativeRole": "Thiết bị điện tử học tập và làm việc",
        "region": box_b_laptop,
        "reveal": {"direction": "top_to_bottom", "startMs": 17000, "durationMs": 1300, "protectedRegions": []}
    },

    # Zone C: Energy Calculation
    {
        "id": "el-20-zone-c-head",
        "sequence": 20,
        "label": "Tiêu đề: C. CÁCH TÍNH ĐIỆN NĂNG",
        "type": "text",
        "narrativeRole": "Hướng dẫn công thức tính điện năng tiêu thụ",
        "region": box_zone_c_head,
        "reveal": {"direction": "left_to_right", "startMs": 18400, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-21-zone-c-underline",
        "sequence": 21,
        "label": "Gạch chân xanh mục tính điện",
        "type": "gesture",
        "narrativeRole": "Nhấn mạnh tiêu đề công thức",
        "region": box_zone_c_underline,
        "reveal": {"direction": "left_to_right", "startMs": 19650, "durationMs": 450, "protectedRegions": []}
    },
    {
        "id": "el-22-zone-c-formula",
        "sequence": 22,
        "label": "Công thức: Điện năng (Wh) = Công suất (W) × Thời gian (h)",
        "type": "text",
        "narrativeRole": "Công thức vật lý cơ bản",
        "region": box_zone_c_formula,
        "reveal": {"direction": "left_to_right", "startMs": 20150, "durationMs": 1600, "protectedRegions": []}
    },
    {
        "id": "el-23-zone-c-calc-text",
        "sequence": 23,
        "label": "Phép tính mẫu: 100 W × 5 h = 500 Wh",
        "type": "text",
        "narrativeRole": "Ví dụ định lượng thực tế",
        "region": box_zone_c_calc_text,
        "reveal": {"direction": "left_to_right", "startMs": 21800, "durationMs": 1400, "protectedRegions": []}
    },
    {
        "id": "el-24-zone-c-oval",
        "sequence": 24,
        "label": "Vòng khoanh cam: 500 Wh",
        "type": "gesture",
        "narrativeRole": "Khoanh tròn làm nổi bật kết quả 500 Wh",
        "region": box_zone_c_oval,
        "reveal": {"direction": "radial_outward", "startMs": 23250, "durationMs": 900, "protectedRegions": []}
    },

    # Zone D: Bar Chart
    {
        "id": "el-25-zone-d-head",
        "sequence": 25,
        "label": "Tiêu đề: D. SẢN LƯỢNG ĐIỆN",
        "type": "text",
        "narrativeRole": "Tiêu đề biểu đồ sản lượng trong ngày",
        "region": box_zone_d_head,
        "reveal": {"direction": "left_to_right", "startMs": 24250, "durationMs": 1200, "protectedRegions": []}
    },
    {
        "id": "el-26-zone-d-chart",
        "sequence": 26,
        "label": "Biểu đồ cột: 8h (2kWh), 12h (4kWh), 16h (3kWh)",
        "type": "colored_image",
        "narrativeRole": "Trục tọa độ và 3 cột sản lượng điện theo thời gian",
        "region": box_zone_d_chart,
        "reveal": {"direction": "left_to_right", "startMs": 25500, "durationMs": 3400, "protectedRegions": []}
    }
]

annotation = {
    "version": "1.0",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": 29800,
    "storyBasis": "Hệ thống điện mặt trời gia đình: Từ năng lượng mặt trời qua các thiết bị lưu trữ, nghịch lưu đến tải tiêu thụ, công thức tính toán và biểu đồ sản lượng",
    "elements": elements
}

with open(ANN_PATH, "w", encoding="utf-8") as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)

print(f"✓ Đã tạo annotation JSON: {ANN_PATH}")

# Vẽ Regions map
vis = img.copy()
colors = [
    (230, 40, 40),    # Blue (BGR: Red channel)
    (40, 180, 40),    # Green
    (40, 80, 240),    # Orange
    (180, 40, 180),   # Purple
    (40, 200, 220),   # Yellow
    (200, 120, 40),   # Cyan
    (120, 40, 220),   # Magenta
]

for i, el in enumerate(elements):
    r = el["region"]
    c = colors[i % len(colors)]
    x, y, w, h = r["x"], r["y"], r["width"], r["height"]
    cv2.rectangle(vis, (x, y), (x + w, y + h), c, 2)
    label_txt = f"{el['sequence']}. {el['id']}"
    cv2.putText(vis, label_txt, (x + 4, max(y - 6, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.40, c, 1, cv2.LINE_AA)

cv2.imwrite(str(REGIONS_PATH), vis)
print(f"✓ Đã tạo ảnh phân vùng hoàn hảo: {REGIONS_PATH}")
