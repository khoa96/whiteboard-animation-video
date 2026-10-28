#!/usr/bin/env python3
"""
Tạo annotation chuẩn cho Scene 05: COMMON EXAMPLES
Sử dụng thuật toán Thị giác Máy tính (scripts/auto_segment_regions.py)
tự động xác định và phân vùng chính xác 100% nét vẽ (Icon + Text), Zero Overlap.

Tất cả 12 thẻ ví dụ đều dùng:
  type: "colored_image", colorMode: "wash"
Tự động xuất ảnh phân vùng chuẩn scene_05-regions.png.
"""
import json
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
REPO_ROOT = [p for p in Path(__file__).resolve().parents if (p / "scripts").exists()][0]
sys.path.insert(0, str(REPO_ROOT))

from scripts.auto_segment_regions import compute_exact_regions

timing_path = DIR / "timing_cues.json"
timing_data = json.loads(timing_path.read_text(encoding="utf-8"))
total_duration_ms = timing_data["totalDurationMs"]

# 1. Định nghĩa các cửa sổ không gian tìm kiếm sơ bộ
scene_05_windows = [
    ("Title", 500, 80, 900, 120),
    ("Header A", 420, 220, 220, 100),
    ("Header AN", 1180, 220, 260, 100),
    # Nhóm A
    ("a book", 270, 330, 290, 212),
    ("a dog", 580, 330, 320, 212),
    ("a cat", 270, 543, 290, 207),
    ("a tree", 580, 543, 320, 207),
    ("a car", 270, 751, 290, 209),
    ("a ball", 580, 751, 320, 209),
    # Nhóm AN
    ("an apple", 980, 330, 370, 212),
    ("an ice cream", 1370, 330, 400, 212),
    ("an egg", 980, 543, 370, 207),
    ("an orange", 1370, 543, 400, 207),
    ("an umbrella", 980, 751, 370, 209),
    ("an elephant", 1370, 751, 400, 209),
]

# 2. Chạy thuật toán CV tự động phát hiện ranh giới chính xác tuyệt đối
img_path = DIR / "scene_05.png"
bboxes = compute_exact_regions(img_path, scene_05_windows, pad_x=4, pad_y=3)

# 3. Khớp nối thứ tự xuất hiện (Sequence) theo Audio Master Clock
# Thứ tự đọc của Cue 2: "A book, a cat, a car, a dog, a tree, a ball."
# Thứ tự đọc của Cue 3: "An apple, an egg, an umbrella, an ice cream, an orange, an elephant."
elements = [
    # 1. Title: COMMON EXAMPLES (Cue 1: 500ms - 3932ms)
    {
        "id": "el-01-title",
        "label": "Title: COMMON EXAMPLES",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": bboxes["Title"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 3000,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },
    # 2. Header A Group (Cue 2: 4432ms - 11296ms)
    {
        "id": "el-02-header-a",
        "label": "Header: A Group",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["Header A"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4450,
            "durationMs": 800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 3. Card: a book
    {
        "id": "el-03-card-book",
        "label": "Card: a book",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a book"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 4. Card: a cat
    {
        "id": "el-04-card-cat",
        "label": "Card: a cat",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a cat"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 5. Card: a car
    {
        "id": "el-05-card-car",
        "label": "Card: a car",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a car"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 6. Card: a dog
    {
        "id": "el-06-card-dog",
        "label": "Card: a dog",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a dog"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 7. Card: a tree
    {
        "id": "el-07-card-tree",
        "label": "Card: a tree",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a tree"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 8. Card: a ball
    {
        "id": "el-08-card-ball",
        "label": "Card: a ball",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["a ball"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 10300,
            "durationMs": 950,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 9. Header AN Group (Cue 3: 11796ms - 20388ms)
    {
        "id": "el-09-header-an",
        "label": "Header: AN Group",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["Header AN"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11800,
            "durationMs": 800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 10. Card: an apple
    {
        "id": "el-10-card-apple",
        "label": "Card: an apple",
        "sequence": 10,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an apple"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12650,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 11. Card: an egg
    {
        "id": "el-11-card-egg",
        "label": "Card: an egg",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an egg"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13900,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 12. Card: an umbrella
    {
        "id": "el-12-card-umbrella",
        "label": "Card: an umbrella",
        "sequence": 12,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an umbrella"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15150,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 13. Card: an ice cream
    {
        "id": "el-13-card-ice-cream",
        "label": "Card: an ice cream",
        "sequence": 13,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an ice cream"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 16400,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 14. Card: an orange
    {
        "id": "el-14-card-orange",
        "label": "Card: an orange",
        "sequence": 14,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an orange"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17650,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 15. Card: an elephant
    {
        "id": "el-15-card-elephant",
        "label": "Card: an elephant",
        "sequence": 15,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bboxes["an elephant"],
        "reveal": {
            "direction": "left_to_right",
            "startMs": 18900,
            "durationMs": 1400,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_10_scene_05",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

out_path = DIR / "scene_05.annotation.json"
out_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[Scene 05] Đã lưu {len(elements)} elements chuẩn xác vào {out_path}")

# Tự động xuất ảnh phân vùng kiểm định chất lượng scene_05-regions.png
regions_png = DIR / "scene_05-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(DIR / "scene_05.png"),
    str(out_path),
    str(regions_png)
], check=True)
print(f"[Scene 05] Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")
