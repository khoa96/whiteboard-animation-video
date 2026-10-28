#!/usr/bin/env python3
"""
Test Case 06: Phân vùng tự động và Hoạt hoạ Bài giảng Ngữ Pháp (COUNTABLE AND UNCOUNTABLE NOUNS)
Quy trình:
1. Phân vùng 22 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề & Phụ đề
   - Vạch ngăn cột đứt nét 1 & 2
   - Cột 1: Header, 1 Apple, 1 Book, 1 Egg, Grammar Rule
   - Cột 2: Header, 3 Apples, 2 Books, 4 Eggs, Grammar Rule
   - Cột 3: Header, Water, Milk, Rice, Bread, Grammar Rule
   - 3 Câu ví dụ thực tế kèm mũi tên & gạch chân
2. Xuất ảnh phân vùng QA kiểm định: grammar_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: grammar_lesson_animation.mp4 (không cần voice over).
4. Trích xuất snapshots kiểm tra chất lượng vào snapshots/.
"""
import json
import subprocess
import sys
import time
from pathlib import Path
import cv2
import numpy as np

DIR = Path(__file__).resolve().parent
REPO_ROOT = [p for p in Path(__file__).resolve().parents if (p / "scripts").exists()][0]

img_path = DIR / "grammar_lesson.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 22 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title & Subtitle
    {
        "id": "el-01-title",
        "label": "Tiêu đề & Phụ đề: COUNTABLE AND UNCOUNTABLE NOUNS",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 0, "y": 0, "width": 1920, "height": 210},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Divider 1
    {
        "id": "el-02-divider1",
        "label": "Vạch phân cột 1 nét đứt",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 655, "y": 210, "width": 20, "height": 650},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 3100,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 3. Divider 2
    {
        "id": "el-03-divider2",
        "label": "Vạch phân cột 2 nét đứt",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1248, "y": 210, "width": 20, "height": 650},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 4400,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 4. Col 1 Header
    {
        "id": "el-04-col1-header",
        "label": "Cột 1 Tiêu đề: SINGULAR COUNTABLE NOUNS",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 210, "width": 575, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5800,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Col 1 Apple
    {
        "id": "el-05-col1-apple",
        "label": "Cột 1: One apple",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 340, "width": 575, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7100,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Col 1 Book
    {
        "id": "el-06-col1-book",
        "label": "Cột 1: One book",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 485, "width": 575, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8400,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Col 1 Egg
    {
        "id": "el-07-col1-egg",
        "label": "Cột 1: One egg",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 630, "width": 575, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9700,
            "durationMs": 1000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Col 1 Rule
    {
        "id": "el-08-col1-rule",
        "label": "Cột 1 Công thức: a / an + singular noun",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 775, "width": 575, "height": 95},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 10800,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Col 2 Header
    {
        "id": "el-09-col2-header",
        "label": "Cột 2 Tiêu đề: PLURAL COUNTABLE NOUNS",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 210, "width": 573, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12200,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Col 2 Apples
    {
        "id": "el-10-col2-apples",
        "label": "Cột 2: Three apples",
        "sequence": 10,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 340, "width": 573, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13500,
            "durationMs": 1400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 11. Col 2 Books
    {
        "id": "el-11-col2-books",
        "label": "Cột 2: Two books",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 485, "width": 573, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15000,
            "durationMs": 1400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 12. Col 2 Eggs
    {
        "id": "el-12-col2-eggs",
        "label": "Cột 2: Four eggs",
        "sequence": 12,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 630, "width": 573, "height": 145},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 16500,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 13. Col 2 Rule
    {
        "id": "el-13-col2-rule",
        "label": "Cột 2 Công thức: noun + s / es",
        "sequence": 13,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 775, "width": 573, "height": 95},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17800,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 14. Col 3 Header
    {
        "id": "el-14-col3-header",
        "label": "Cột 3 Tiêu đề: UNCOUNTABLE NOUNS",
        "sequence": 14,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1268, "y": 210, "width": 582, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 19200,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 15. Col 3 Water
    {
        "id": "el-15-col3-water",
        "label": "Cột 3: One glass of water",
        "sequence": 15,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1268, "y": 340, "width": 282, "height": 220},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 20500,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 16. Col 3 Milk
    {
        "id": "el-16-col3-milk",
        "label": "Cột 3: One bottle of milk",
        "sequence": 16,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1550, "y": 340, "width": 300, "height": 220},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 21800,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 17. Col 3 Rice
    {
        "id": "el-17-col3-rice",
        "label": "Cột 3: One bowl of rice",
        "sequence": 17,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1268, "y": 560, "width": 282, "height": 215},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 23100,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 18. Col 3 Bread
    {
        "id": "el-18-col3-bread",
        "label": "Cột 3: One loaf of bread",
        "sequence": 18,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1550, "y": 560, "width": 300, "height": 215},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 24400,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 19. Col 3 Rule
    {
        "id": "el-19-col3-rule",
        "label": "Cột 3 Công thức: some + uncountable noun",
        "sequence": 19,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1268, "y": 775, "width": 582, "height": 95},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 25700,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 20. Sent 1
    {
        "id": "el-20-sent1",
        "label": "Câu 1: I have an apple (mũi tên & gạch chân)",
        "sequence": 20,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 870, "width": 550, "height": 180},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 27100,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 21. Sent 2
    {
        "id": "el-21-sent2",
        "label": "Câu 2: She has three books (mũi tên & gạch chân)",
        "sequence": 21,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 630, "y": 870, "width": 575, "height": 180},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 28700,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 22. Sent 3
    {
        "id": "el-22-sent3",
        "label": "Câu 3: He drinks some water (mũi tên & gạch chân)",
        "sequence": 22,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1205, "y": 870, "width": 645, "height": 180},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 30300,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 33000

# Kiểm tra độ phủ mực và chồng lấn
covered_mask = np.zeros_like(ink)
for b in boxes:
    r = b["region"]
    covered_mask[r["y"]:r["y"]+r["height"], r["x"]:r["x"]+r["width"]] += 1

covered = int(np.count_nonzero((ink == 1) & (covered_mask >= 1)))
overlap = int(np.count_nonzero((ink == 1) & (covered_mask > 1)))

print(f"Tổng số pixel mực: {total_ink}")
print(f"Độ phủ mực: {covered}/{total_ink} ({covered/total_ink*100:.5f}%)")
print(f"Chồng lấn pixel mực: {overlap} ({overlap/total_ink*100:.5f}%)")

if covered < total_ink:
    raise ValueError(f"Chưa phủ hết mực! Thiếu {total_ink - covered} pixels.")
if overlap > 0:
    raise ValueError(f"Có {overlap} pixels bị chồng lấn giữa các vùng!")

annotation = {
    "sceneId": "test_case_segmentation_06_grammar",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "grammar_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: grammar_lesson-regions.png
regions_png = DIR / "grammar_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "grammar_lesson_animation.mp4"
hand_path = REPO_ROOT / "assets/drawing-hand.png"
print(f"\n🎬 BẮT ĐẦU HOẠT HOẠ VIDEO WHITEBOARD: {raw_mp4.name} (60fps 1080p)...")
start_time = time.time()

cmd_render = [
    sys.executable,
    str(REPO_ROOT / "scripts/render_stream_whiteboard.py"),
    str(img_path),
    str(ann_path),
    str(raw_mp4),
    str(hand_path),
    "--canvas-hex", "#FFFFFF",
    "--fps", "60",
    "--cap-long-edge", "1920"
]
subprocess.run(cmd_render, check=True)
render_elapsed = time.time() - start_time
print(f"✅ HOÀN TẤT HOẠT HOẠ trong {render_elapsed:.2f} giây ({render_elapsed/60:.2f} phút)!")

# Trích xuất snapshots kiểm tra chất lượng vào snapshots/
snap_dir = DIR / "snapshots"
snap_dir.mkdir(parents=True, exist_ok=True)
for t in [2, 5, 8, 11, 14, 18, 22, 26, 30, 32]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
