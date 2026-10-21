#!/usr/bin/env python3
"""
Tạo annotation.json chuẩn cho Test Case 3: HỆ HÔ HẤP & CƠ CHẾ TRAO ĐỔI KHÍ (Respiratory System).
Bố cục khoa học: Hình giải phẫu tổng thể bên trái kết nối với khung phóng đại phế nang bên phải.
"""
from pathlib import Path
import json

CASE_DIR = Path(__file__).resolve().parent
ANN_PATH = CASE_DIR / "respiratory_system.annotation.json"

annotation = {
    "version": "1.0",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": 24000,
    "storyBasis": "Hệ Hô Hấp: Không khí đi từ Mũi qua Khí quản vào Phổi, trao đổi khí O2 và CO2 tại Phế nang và Mao mạch",
    "elements": [
        {
            "id": "el-01-title",
            "sequence": 1,
            "label": "Tiêu đề: HỆ HÔ HẤP",
            "type": "text",
            "narrativeRole": "Giới thiệu chủ đề giải phẫu",
            "region": {
                "x": 590,
                "y": 65,
                "width": 620,
                "height": 120
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 400,
                "durationMs": 1600,
                "protectedRegions": []
            }
        },
        {
            "id": "el-02-nose-profile",
            "sequence": 2,
            "label": "Đường thở trên (Mũi, Miệng, Họng)",
            "type": "colored_image",
            "narrativeRole": "Cửa ngõ dẫn khí vào cơ thể",
            "region": {
                "x": 540,
                "y": 165,
                "width": 260,
                "height": 345
            },
            "reveal": {
                "direction": "top_to_bottom",
                "startMs": 2200,
                "durationMs": 1900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-03-label-mui",
            "sequence": 3,
            "label": "Nhãn: MŨI & Đường dẫn",
            "type": "text",
            "narrativeRole": "Chú thích cơ quan mũi",
            "region": {
                "x": 360,
                "y": 245,
                "width": 230,
                "height": 80
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 4200,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-04-airflow",
            "sequence": 4,
            "label": "Luồng khí xanh & Nhãn: HÍT VÀO",
            "type": "colored_image",
            "narrativeRole": "Minh họa luồng khí hít vào",
            "region": {
                "x": 260,
                "y": 345,
                "width": 280,
                "height": 120
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 5200,
                "durationMs": 1200,
                "protectedRegions": []
            }
        },
        {
            "id": "el-05-trachea-bronchi",
            "sequence": 5,
            "label": "Khí quản & Phế quản",
            "type": "colored_image",
            "narrativeRole": "Ống dẫn khí chính phân nhánh vào 2 phổi",
            "region": {
                "x": 685,
                "y": 470,
                "width": 155,
                "height": 180
            },
            "reveal": {
                "direction": "top_to_bottom",
                "startMs": 6600,
                "durationMs": 1600,
                "protectedRegions": []
            }
        },
        {
            "id": "el-06-label-khi-quan",
            "sequence": 6,
            "label": "Nhãn: KHÍ QUẢN & Đường dẫn",
            "type": "text",
            "narrativeRole": "Chú thích khí quản",
            "region": {
                "x": 300,
                "y": 470,
                "width": 445,
                "height": 115
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 8300,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-07-label-phe-quan",
            "sequence": 7,
            "label": "Nhãn: PHẾ QUẢN & Đường dẫn",
            "type": "text",
            "narrativeRole": "Chú thích phế quản",
            "region": {
                "x": 240,
                "y": 610,
                "width": 505,
                "height": 115
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 9300,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-08-lungs",
            "sequence": 8,
            "label": "Hai lá Phổi (Trái & Phải)",
            "type": "colored_image",
            "narrativeRole": "Cơ quan hô hấp chính chứa các chùm phế nang",
            "region": {
                "x": 500,
                "y": 520,
                "width": 525,
                "height": 445
            },
            "reveal": {
                "direction": "top_to_bottom",
                "startMs": 10300,
                "durationMs": 2600,
                "protectedRegions": []
            }
        },
        {
            "id": "el-09-label-phoi",
            "sequence": 9,
            "label": "Nhãn: PHỔI & Đường dẫn",
            "type": "text",
            "narrativeRole": "Chú thích lá phổi",
            "region": {
                "x": 315,
                "y": 735,
                "width": 270,
                "height": 115
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 13000,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-10-zoom-lines",
            "sequence": 10,
            "label": "Đường phóng đại liên kết kính lúp",
            "type": "gesture",
            "narrativeRole": "Dẫn hướng mắt người xem sang vùng phóng đại",
            "region": {
                "x": 885,
                "y": 435,
                "width": 285,
                "height": 345
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 14100,
                "durationMs": 1100,
                "protectedRegions": []
            }
        },
        {
            "id": "el-11-magnified-circle",
            "sequence": 11,
            "label": "Khung kính lúp: Phế nang & Mao mạch",
            "type": "colored_image",
            "narrativeRole": "Mô phỏng túi phế nang và mao mạch máu bao quanh",
            "region": {
                "x": 1145,
                "y": 270,
                "width": 595,
                "height": 600
            },
            "reveal": {
                "direction": "radial_outward",
                "startMs": 15400,
                "durationMs": 2800,
                "protectedRegions": []
            }
        },
        {
            "id": "el-12-label-phe-nang",
            "sequence": 12,
            "label": "Nhãn: PHẾ NANG",
            "type": "text",
            "narrativeRole": "Chú thích túi khí phế nang",
            "region": {
                "x": 1420,
                "y": 330,
                "width": 280,
                "height": 105
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 18400,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-13-label-mao-mach",
            "sequence": 13,
            "label": "Nhãn: MAO MẠCH",
            "type": "text",
            "narrativeRole": "Chú thích mạch máu",
            "region": {
                "x": 1480,
                "y": 790,
                "width": 335,
                "height": 140
            },
            "reveal": {
                "direction": "left_to_right",
                "startMs": 19400,
                "durationMs": 900,
                "protectedRegions": []
            }
        },
        {
            "id": "el-14-gas-exchange",
            "sequence": 14,
            "label": "Trao đổi khí: Mũi tên O2 (xanh) & CO2 (cam)",
            "type": "gesture",
            "narrativeRole": "O2 khuếch tán vào máu, CO2 khuếch tán vào phế nang",
            "region": {
                "x": 1350,
                "y": 530,
                "width": 250,
                "height": 200
            },
            "reveal": {
                "direction": "bottom_to_top",
                "startMs": 20500,
                "durationMs": 2400,
                "protectedRegions": []
            }
        }
    ]
}

with open(ANN_PATH, "w", encoding="utf-8") as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)

print(f"✓ Đã tạo annotation JSON: {ANN_PATH}")
