#!/usr/bin/env python3
"""
Tự động tạo 4 file Annotation JSON cho 4 cảnh video "Sức Mạnh Của Lãi Kép" (Compound Interest).
Độ phân giải: 1920x1080 (16:9).
Thời lượng: 58,800 ms khớp chính xác narration.m4a và input.srt.
Hạn chế chữ, ưu tiên biểu đồ, sơ đồ tư duy, icon đòn bẩy.
Tất cả các khung chứa (box) đều dùng colorMode="none" để tránh lộ chữ sớm.
Mỗi khung đều có phân rã giữa nét viền khung và nét vẽ nội dung/chữ bên trong.
"""
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

SCENES_DATA = [
    # ----------------------------------------------------
    # CẢNH 1: Hiệu ứng Hòn tuyết lăn (14,200 ms)
    # ----------------------------------------------------
    {
        "filename": "scene-01-snowball.annotation.json",
        "sceneId": "scene-01-snowball",
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 14200,
        "storyBasis": "Albert Einstein gọi Lãi Kép là kỳ quan thứ 8: Lãi mẹ đẻ lãi con, như hòn tuyết càng lăn càng to.",
        "elements": [
            {
                "id": "scene_title",
                "label": "Tiêu đề Lãi Kép: Kỳ quan thứ 8",
                "sequence": 1,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Giới thiệu chủ đề lãi kép",
                "subtitle": "Albert Einstein từng gọi Lãi Kép là kỳ quan thứ tám của thế giới.",
                "region": {"x": 90, "y": 40, "width": 1350, "height": 95},
                "reveal": {"direction": "left_to_right", "startMs": 200, "durationMs": 2200, "maskPaddingPx": 0},
                "handPath": {"start": [100, 70], "end": [1400, 125]}
            },
            {
                "id": "left_box",
                "label": "Khung Quy tắc Cốt lõi",
                "sequence": 2,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Định hình khối nguyên lý",
                "subtitle": "Nguyên lý rất đơn giản: Tiền lãi sinh ra lại tiếp tục sinh lãi mới.",
                "region": {"x": 100, "y": 165, "width": 860, "height": 815},
                "reveal": {"direction": "clockwise", "startMs": 2500, "durationMs": 1100, "maskPaddingPx": 0},
                "handPath": {"start": [100, 165], "end": [960, 980]}
            },
            {
                "id": "left_text",
                "label": "Quy tắc: Lãi Mẹ Đẻ Lãi Con",
                "sequence": 3,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Khắc sâu khái niệm cốt lõi",
                "subtitle": "Tiền lãi gộp vào vốn để sinh ra lãi mới.",
                "region": {"x": 130, "y": 195, "width": 800, "height": 380},
                "reveal": {"direction": "top_to_bottom", "startMs": 3700, "durationMs": 3200, "maskPaddingPx": 0},
                "handPath": {"start": [140, 210], "end": [500, 560]}
            },
            {
                "id": "coin_growth",
                "label": "Icon Vốn nhỏ tích lũy thành Tài sản khủng",
                "sequence": 4,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Hình ảnh hóa tiền sinh sôi",
                "subtitle": "Tiền vốn sinh lãi và tích lũy liên tục.",
                "region": {"x": 170, "y": 625, "width": 720, "height": 285},
                "reveal": {"direction": "left_to_right", "startMs": 7000, "durationMs": 2200, "maskPaddingPx": 0},
                "handPath": {"start": [200, 750], "end": [800, 750]}
            },
            {
                "id": "right_box",
                "label": "Khung Hiệu ứng Hòn tuyết lăn",
                "sequence": 5,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khối minh họa sườn dốc",
                "subtitle": "Tựa như một hòn tuyết càng lăn trên dốc dài thì càng khổng lồ.",
                "region": {"x": 1010, "y": 165, "width": 810, "height": 815},
                "reveal": {"direction": "clockwise", "startMs": 9300, "durationMs": 1000, "maskPaddingPx": 0},
                "handPath": {"start": [1010, 165], "end": [1820, 980]}
            },
            {
                "id": "snowball_slope",
                "label": "Minh họa 3 giai đoạn Quả cầu tuyết",
                "sequence": 6,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Hình tượng hóa sức mạnh thời gian",
                "subtitle": "Càng lăn trên dốc dài thì càng khổng lồ.",
                "region": {"x": 1050, "y": 200, "width": 750, "height": 760},
                "reveal": {"direction": "top_to_bottom", "startMs": 10400, "durationMs": 3400, "maskPaddingPx": 0},
                "handPath": {"start": [1080, 420], "end": [1700, 840]}
            }
        ]
    },

    # ----------------------------------------------------
    # CẢNH 2: Biểu đồ Tuyến tính vs Cấp số nhân (15,600 ms)
    # ----------------------------------------------------
    {
        "filename": "scene-02-chart.annotation.json",
        "sceneId": "scene-02-chart",
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 15600,
        "storyBasis": "So sánh đường thẳng Tuyến tính vs Đường cong Lãi kép vút thẳng tại Điểm bùng phát.",
        "elements": [
            {
                "id": "scene_title",
                "label": "Tiêu đề Biểu đồ Tuyến tính vs Cấp số nhân",
                "sequence": 1,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Giới thiệu đồ thị toán học",
                "subtitle": "Sự khác biệt nằm ở đây: Tiết kiệm thông thường chỉ tăng theo đường thẳng tuyến tính.",
                "region": {"x": 90, "y": 40, "width": 1350, "height": 95},
                "reveal": {"direction": "left_to_right", "startMs": 200, "durationMs": 2000, "maskPaddingPx": 0},
                "handPath": {"start": [100, 70], "end": [1400, 125]}
            },
            {
                "id": "chart_box",
                "label": "Khung biểu đồ tọa độ",
                "sequence": 2,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Bảng đồ thị",
                "subtitle": "Tiết kiệm thông thường chỉ tăng theo đường thẳng tuyến tính.",
                "region": {"x": 100, "y": 160, "width": 1720, "height": 820},
                "reveal": {"direction": "clockwise", "startMs": 2300, "durationMs": 1000, "maskPaddingPx": 0},
                "handPath": {"start": [100, 160], "end": [1820, 980]}
            },
            {
                "id": "axis_y",
                "label": "Trục tung Y & Nhãn Tài sản tích lũy ($)",
                "sequence": 3,
                "type": "object",
                "colorMode": "none",
                "narrativeRole": "Định vị trục giá trị tài sản",
                "subtitle": "Trục tung biểu thị giá trị tài sản tích lũy.",
                "region": {"x": 190, "y": 185, "width": 140, "height": 625},
                "reveal": {"direction": "top_to_bottom", "startMs": 3400, "durationMs": 1200, "maskPaddingPx": 0},
                "handPath": {"start": [250, 200], "end": [280, 800]}
            },
            {
                "id": "axis_x",
                "label": "Trục hoành X & Mốc thời gian 0-30 năm",
                "sequence": 4,
                "type": "object",
                "colorMode": "none",
                "narrativeRole": "Định vị trục thời gian",
                "subtitle": "Trục hoành biểu thị số năm tích lũy.",
                "region": {"x": 270, "y": 795, "width": 1450, "height": 75},
                "reveal": {"direction": "left_to_right", "startMs": 4700, "durationMs": 1400, "maskPaddingPx": 0},
                "handPath": {"start": [280, 800], "end": [1650, 800]}
            },
            {
                "id": "linear_curve",
                "label": "Đường thẳng Tiết kiệm đơn (Tuyến tính)",
                "sequence": 5,
                "type": "object",
                "colorMode": "none",
                "narrativeRole": "Mô hình tăng trưởng chậm tuyến tính",
                "subtitle": "Tiết kiệm thông thường chỉ tăng theo đường thẳng tuyến tính.",
                "region": {"x": 280, "y": 555, "width": 1450, "height": 235},
                "reveal": {"direction": "left_to_right", "startMs": 6200, "durationMs": 2500, "maskPaddingPx": 0},
                "handPath": {"start": [280, 800], "end": [1630, 570]}
            },
            {
                "id": "exponential_curve",
                "label": "Đường cong Lãi Kép vút thẳng đứng",
                "sequence": 6,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Tăng trưởng cấp số nhân bùng nổ",
                "subtitle": "Nhưng với Lãi kép, sau giai đoạn tích lũy âm thầm,",
                "region": {"x": 280, "y": 220, "width": 1450, "height": 580},
                "reveal": {"direction": "left_to_right", "startMs": 8800, "durationMs": 3400, "maskPaddingPx": 0},
                "handPath": {"start": [280, 800], "end": [1600, 240]}
            },
            {
                "id": "tipping_point",
                "label": "Khung Điểm Bùng Phát (Tipping Point)",
                "sequence": 7,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Nhấn mạnh mốc chuyển mình quan trọng",
                "subtitle": "đồ thị sẽ chạm tới Điểm Bùng Phát và vút thẳng theo cấp số nhân.",
                "region": {"x": 500, "y": 415, "width": 500, "height": 300},
                "reveal": {"direction": "clockwise", "startMs": 12300, "durationMs": 3000, "maskPaddingPx": 0},
                "handPath": {"start": [520, 425], "end": [960, 680]}
            }
        ]
    },

    # ----------------------------------------------------
    # CẢNH 3: Sơ đồ tư duy 3 Chân kiềng cốt lõi (16,200 ms)
    # ----------------------------------------------------
    {
        "filename": "scene-03-mindmap.annotation.json",
        "sceneId": "scene-03-mindmap",
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 16200,
        "storyBasis": "3 yếu tố cốt lõi: Vốn (P), Lãi suất (r), và Thời gian (t - Đòn bẩy quyền năng nhất).",
        "elements": [
            {
                "id": "scene_title",
                "label": "Tiêu đề 3 Chân Kiềng Tạo Nên Lãi Kép",
                "sequence": 1,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Đặt vấn đề các yếu tố cốt lõi",
                "subtitle": "Có ba yếu tố tạo nên Lãi kép: Số vốn, Lãi suất, và Thời gian.",
                "region": {"x": 90, "y": 40, "width": 1150, "height": 95},
                "reveal": {"direction": "left_to_right", "startMs": 200, "durationMs": 1800, "maskPaddingPx": 0},
                "handPath": {"start": [100, 70], "end": [1200, 125]}
            },
            {
                "id": "center_box",
                "label": "Khung Node công thức trung tâm",
                "sequence": 2,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Viền bao công thức",
                "subtitle": "Có ba yếu tố tạo nên Lãi kép: Số vốn, Lãi suất, và Thời gian.",
                "region": {"x": 520, "y": 150, "width": 880, "height": 140},
                "reveal": {"direction": "clockwise", "startMs": 2100, "durationMs": 800, "maskPaddingPx": 0},
                "handPath": {"start": [520, 150], "end": [1400, 290]}
            },
            {
                "id": "center_text",
                "label": "Công thức A = P * (1 + r)^t",
                "sequence": 3,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Công thức toán học bao quát",
                "subtitle": "Có ba yếu tố tạo nên Lãi kép: Số vốn, Lãi suất, và Thời gian.",
                "region": {"x": 540, "y": 160, "width": 840, "height": 120},
                "reveal": {"direction": "top_to_bottom", "startMs": 3000, "durationMs": 1000, "maskPaddingPx": 0},
                "handPath": {"start": [560, 175], "end": [1280, 260]}
            },
            {
                "id": "branch_1_box",
                "label": "Khung Nhánh 1: Vốn ban đầu (P)",
                "sequence": 4,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung yếu tố số vốn",
                "subtitle": "Thứ nhất là số vốn, không cần quá lớn nhưng cần đều đặn.",
                "region": {"x": 100, "y": 330, "width": 560, "height": 650},
                "reveal": {"direction": "clockwise", "startMs": 4100, "durationMs": 700, "maskPaddingPx": 0},
                "handPath": {"start": [100, 330], "end": [660, 980]}
            },
            {
                "id": "branch_1_content",
                "label": "Nội dung Vốn (P) & Túi tiền",
                "sequence": 5,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Minh họa vốn ban đầu",
                "subtitle": "Thứ nhất là số vốn, không cần quá lớn nhưng cần đều đặn.",
                "region": {"x": 115, "y": 345, "width": 530, "height": 620},
                "reveal": {"direction": "top_to_bottom", "startMs": 4900, "durationMs": 2600, "maskPaddingPx": 0},
                "handPath": {"start": [140, 370], "end": [450, 850]}
            },
            {
                "id": "branch_2_box",
                "label": "Khung Nhánh 2: Lãi suất (r)",
                "sequence": 6,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung yếu tố lãi suất",
                "subtitle": "Thứ hai là tỷ suất sinh lời bình quân hàng năm.",
                "region": {"x": 690, "y": 330, "width": 540, "height": 650},
                "reveal": {"direction": "clockwise", "startMs": 7600, "durationMs": 700, "maskPaddingPx": 0},
                "handPath": {"start": [690, 330], "end": [1230, 980]}
            },
            {
                "id": "branch_2_content",
                "label": "Nội dung Lãi suất (r) & Cột tăng trưởng",
                "sequence": 7,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Minh họa tỷ suất sinh lời",
                "subtitle": "Thứ hai là tỷ suất sinh lời bình quân hàng năm.",
                "region": {"x": 705, "y": 345, "width": 510, "height": 620},
                "reveal": {"direction": "top_to_bottom", "startMs": 8400, "durationMs": 2600, "maskPaddingPx": 0},
                "handPath": {"start": [730, 370], "end": [1050, 850]}
            },
            {
                "id": "branch_3_box",
                "label": "Khung Nhánh 3: Thời gian (t) Đòn bẩy số 1",
                "sequence": 8,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung yếu tố thời gian",
                "subtitle": "Nhưng hãy nhớ: Thời gian chính là đòn bẩy quyền năng nhất. Bạn không cần vốn khổng lồ, chỉ cần cho thời gian đủ dài để phép màu xảy ra.",
                "region": {"x": 1260, "y": 320, "width": 560, "height": 660},
                "reveal": {"direction": "clockwise", "startMs": 11100, "durationMs": 800, "maskPaddingPx": 0},
                "handPath": {"start": [1260, 320], "end": [1820, 980]}
            },
            {
                "id": "branch_3_content",
                "label": "Nội dung Thời gian (t) & Đồng hồ cát",
                "sequence": 9,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Minh họa đòn bẩy quyền năng nhất",
                "subtitle": "Nhưng hãy nhớ: Thời gian chính là đòn bẩy quyền năng nhất. Bạn không cần vốn khổng lồ, chỉ cần cho thời gian đủ dài để phép màu xảy ra.",
                "region": {"x": 1275, "y": 335, "width": 530, "height": 630},
                "reveal": {"direction": "top_to_bottom", "startMs": 12000, "durationMs": 3900, "maskPaddingPx": 0},
                "handPath": {"start": [1300, 370], "end": [1650, 880]}
            }
        ]
    },

    # ----------------------------------------------------
    # CẢNH 4: Infographic So sánh tuổi 20 vs 30 (12,800 ms)
    # ----------------------------------------------------
    {
        "filename": "scene-04-comparison.annotation.json",
        "sceneId": "scene-04-comparison",
        "canvas": {"width": 1920, "height": 1080},
        "sceneDurationMs": 12800,
        "storyBasis": "So sánh Người A bắt đầu tuổi 20 đạt gấp 3 lần tài sản so với Người B tuổi 30. Kêu gọi hành động ngay hôm nay.",
        "elements": [
            {
                "id": "scene_title",
                "label": "Tiêu đề So sánh: Bắt đầu tuổi 20 vs 30",
                "sequence": 1,
                "type": "text",
                "colorMode": "none",
                "narrativeRole": "Đưa ra dẫn chứng thực tế",
                "subtitle": "Bắt đầu ở tuổi hai mươi sẽ mang lại tài sản gấp ba lần so với tuổi ba mươi.",
                "region": {"x": 90, "y": 40, "width": 1400, "height": 95},
                "reveal": {"direction": "left_to_right", "startMs": 200, "durationMs": 1800, "maskPaddingPx": 0},
                "handPath": {"start": [100, 70], "end": [1450, 125]}
            },
            {
                "id": "col_a_box",
                "label": "Khung Cột Người A: Tuổi 20",
                "sequence": 2,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung minh chứng bắt đầu sớm",
                "subtitle": "Bắt đầu ở tuổi hai mươi sẽ mang lại tài sản gấp ba lần so với tuổi ba mươi.",
                "region": {"x": 100, "y": 160, "width": 820, "height": 620},
                "reveal": {"direction": "clockwise", "startMs": 2100, "durationMs": 700, "maskPaddingPx": 0},
                "handPath": {"start": [100, 160], "end": [920, 780]}
            },
            {
                "id": "col_a_content",
                "label": "Nội dung Người A: Cột 3X & Tài sản gấp 3",
                "sequence": 3,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Minh họa tài sản 3X tuổi 20",
                "subtitle": "Bắt đầu ở tuổi hai mươi sẽ mang lại tài sản gấp ba lần so với tuổi ba mươi.",
                "region": {"x": 115, "y": 175, "width": 790, "height": 590},
                "reveal": {"direction": "top_to_bottom", "startMs": 2900, "durationMs": 2700, "maskPaddingPx": 0},
                "handPath": {"start": [140, 200], "end": [650, 640]}
            },
            {
                "id": "col_b_box",
                "label": "Khung Cột Người B: Tuổi 30",
                "sequence": 4,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung hệ quả trì hoãn",
                "subtitle": "Dù nỗ lực bỏ vốn nhiều hơn nhưng khó đuổi kịp.",
                "region": {"x": 1000, "y": 160, "width": 820, "height": 620},
                "reveal": {"direction": "clockwise", "startMs": 5700, "durationMs": 700, "maskPaddingPx": 0},
                "handPath": {"start": [1000, 160], "end": [1820, 780]}
            },
            {
                "id": "col_b_content",
                "label": "Nội dung Người B: Cột 1X & Chỉ đạt 1/3",
                "sequence": 5,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Minh họa tài sản 1X tuổi 30",
                "subtitle": "Dù nỗ lực bỏ vốn nhiều hơn nhưng khó đuổi kịp.",
                "region": {"x": 1015, "y": 175, "width": 790, "height": 590},
                "reveal": {"direction": "top_to_bottom", "startMs": 6500, "durationMs": 2800, "maskPaddingPx": 0},
                "handPath": {"start": [1040, 200], "end": [1550, 640]}
            },
            {
                "id": "cta_border",
                "label": "Khung Viền Thông điệp Kêu gọi hành động",
                "sequence": 6,
                "type": "box",
                "colorMode": "none",
                "narrativeRole": "Khung viền CTA",
                "subtitle": "Đừng chờ đợi sự hoàn hảo. Hãy hành động và gieo hạt giống ngay hôm nay!",
                "region": {"x": 100, "y": 810, "width": 1720, "height": 175},
                "reveal": {"direction": "clockwise", "startMs": 9500, "durationMs": 700, "maskPaddingPx": 0},
                "handPath": {"start": [100, 810], "end": [1820, 985]}
            },
            {
                "id": "cta_content",
                "label": "Nội dung CTA & Icon Tên lửa 🚀",
                "sequence": 7,
                "type": "colored_image",
                "colorMode": "auto",
                "narrativeRole": "Kêu gọi hành động gieo hạt giống tài chính",
                "subtitle": "Đừng chờ đợi sự hoàn hảo. Hãy hành động và gieo hạt giống ngay hôm nay!",
                "region": {"x": 115, "y": 820, "width": 1690, "height": 155},
                "reveal": {"direction": "left_to_right", "startMs": 10300, "durationMs": 2300, "maskPaddingPx": 0},
                "handPath": {"start": [140, 880], "end": [1200, 880]}
            }
        ]
    }
]


def main():
    print("=" * 60)
    print("Tạo 4 file Annotation JSON chuẩn xác cho 'Lãi Kép'...")
    print("=" * 60)
    for sc in SCENES_DATA:
        filename = sc["filename"]
        out_file = PROJECT_DIR / filename
        data = {
            "sceneId": sc["sceneId"],
            "canvas": sc["canvas"],
            "sceneDurationMs": sc["sceneDurationMs"],
            "storyBasis": sc["storyBasis"],
            "elements": sc["elements"]
        }
        out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Đã ghi: {filename} ({len(sc['elements'])} elements, duration: {sc['sceneDurationMs']}ms)")
    print("=" * 60)
    print("Hoàn tất tạo 4 file Annotation JSON!")


if __name__ == "__main__":
    main()
