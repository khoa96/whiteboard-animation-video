#!/usr/bin/env python3
"""
Sinh file annotation.json chuẩn cho Scene 01 (Test Case 10: Articles - Three Groups)
- Nền trắng thuần #FFFFFF
- Zero Overlap giữa tất cả 11 vùng nguyên tử
- Timing đồng bộ 100% với file audio narration.m4a (tổng thời lượng: 43.284s)
- Tỉ lệ ink:wash:
  + Chữ, đường kẻ, khung viền: colorMode="none" (100% ink)
  + Hình minh họa icon (sách, táo, ly nước, badge): colorMode="wash" (vẽ nét mực trước, tô màu sau)
"""
from pathlib import Path
import json

DIR = Path(__file__).resolve().parent
ANN_PATH = DIR / "scene_01.annotation.json"

elements = [
    # ---------------- Zone 1: Title & Subtitle ----------------
    {
        "id": "el-01-title",
        "label": "Tiêu đề: ARTICLES",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Giới thiệu chủ đề mạo từ trong tiếng Anh",
        "region": {"x": 640, "y": 50, "width": 640, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 600,
            "durationMs": 3200,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    {
        "id": "el-02-subtitle",
        "label": "Phụ đề: THREE GROUPS",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Chia mạo từ làm 3 nhóm chính",
        "region": {"x": 680, "y": 195, "width": 560, "height": 85},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4000,
            "durationMs": 2800,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },

    # ---------------- Zone 2 - Card 1: A / AN (Indefinite) ----------------
    {
        "id": "el-03-card1-header",
        "label": "Khung và Nhãn nhóm 1: A / AN",
        "sequence": 3,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Khung và tiêu đề nhóm mạo từ không xác định A và AN",
        "region": {"x": 99, "y": 329, "width": 546, "height": 101},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7800,
            "durationMs": 3400,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-04-card1-book",
        "label": "Ví dụ 1: a book (cuốn sách)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Minh họa a book - một cuốn sách bất kỳ",
        "region": {"x": 99, "y": 430, "width": 286, "height": 317},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 11400,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-05-card1-apple",
        "label": "Ví dụ 2: an apple (quả táo)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Minh họa an apple - một quả táo bất kỳ",
        "region": {"x": 385, "y": 430, "width": 260, "height": 317},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 14400,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },

    # ---------------- Zone 2 - Card 2: THE (Definite) ----------------
    {
        "id": "el-06-card2-header",
        "label": "Khung và Nhãn nhóm 2: THE",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Khung và tiêu đề nhóm mạo từ xác định THE",
        "region": {"x": 687, "y": 329, "width": 546, "height": 93},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 18000,
            "durationMs": 3400,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-07-card2-content",
        "label": "Minh họa sách & the book",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Minh họa the book - cuốn sách cụ thể đã xác định",
        "region": {"x": 687, "y": 422, "width": 546, "height": 325},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 21600,
            "durationMs": 4000,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },

    # ---------------- Zone 2 - Card 3: ZERO ARTICLE ----------------
    {
        "id": "el-08-card3-header",
        "label": "Khung và Nhãn nhóm 3: ZERO ARTICLE",
        "sequence": 8,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Khung và tiêu đề nhóm không dùng mạo từ Zero Article",
        "region": {"x": 1274, "y": 329, "width": 547, "height": 93},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 26500,
            "durationMs": 3500,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-09-card3-content",
        "label": "Minh họa ly nước & WATER",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Minh họa nước (danh từ không đếm được nói chung) không dùng mạo từ",
        "region": {"x": 1274, "y": 422, "width": 547, "height": 325},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 30200,
            "durationMs": 3800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },

    # ---------------- Zone 3: Divider Line ----------------
    {
        "id": "el-10-divider",
        "label": "Đường kẻ phân cách trang trí",
        "sequence": 10,
        "type": "line",
        "colorMode": "none",
        "narrativeRole": "Phân cách nhóm tổng quan và trọng tâm bài học",
        "region": {"x": 90, "y": 780, "width": 1740, "height": 80},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 35000,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },

    # ---------------- Zone 4: Focus Today Badge ----------------
    {
        "id": "el-11-today",
        "label": "Hộp nhấn mạnh trọng tâm: TODAY: A / AN",
        "sequence": 11,
        "type": "box",
        "colorMode": "wash",
        "narrativeRole": "Xác định trọng tâm buổi học hôm nay là nhóm A / AN",
        "region": {"x": 650, "y": 870, "width": 620, "height": 160},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 36400,
            "durationMs": 4400,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    }
]

annotation_data = {
    "sceneId": "test_case_10_scene_01",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "storyBasis": "Infographic tổng quan 3 nhóm mạo từ tiếng Anh: ARTICLES — THREE GROUPS (A/AN, THE, ZERO ARTICLE), dẫn nhập vào trọng tâm bài học hôm nay là nhóm A và AN.",
    "sceneDurationMs": 43284,
    "elements": elements
}

with open(ANN_PATH, "w", encoding="utf-8") as f:
    json.dump(annotation_data, f, ensure_ascii=False, indent=2)

print(f"Saved {ANN_PATH} with {len(elements)} elements. Total Duration: {annotation_data['sceneDurationMs']} ms")
