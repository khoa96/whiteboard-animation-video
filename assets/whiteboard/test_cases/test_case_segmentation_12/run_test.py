#!/usr/bin/env python3
"""
Test Case 12: Phân vùng tự động và Hoạt hoạ Động từ Nấu ăn (COOKING VERBS)
Quy trình:
1. Phân vùng 11 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: COOKING VERBS
   - Hàng 1 (5 hành động): CHOP, SLICE, WHISK, STIR, POUR
   - Hàng 2 (5 hành động): PEEL, GRATE, KNEAD, DRAIN, SPRINKLE
2. Xuất ảnh phân vùng QA kiểm định: cooking_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: cooking_lesson_animation.mp4 (không cần voice over).
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

img_path = DIR / "cooking_lesson.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 11 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "el-01-title",
        "label": "Tiêu đề: COOKING VERBS",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 500, "y": 40, "width": 920, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Row 1 Col 1: CHOP
    {
        "id": "el-02-chop",
        "label": "Hành động 1: CHOP (Chặt, băm nhỏ)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 160, "width": 310, "height": 420},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Row 1 Col 2: SLICE
    {
        "id": "el-03-slice",
        "label": "Hành động 2: SLICE (Thái lát mỏng)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 390, "y": 160, "width": 380, "height": 420},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 4700,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Row 1 Col 3: WHISK
    {
        "id": "el-04-whisk",
        "label": "Hành động 3: WHISK (Đánh trứng, khuấy lồng)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 770, "y": 160, "width": 370, "height": 420},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 6800,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Row 1 Col 4: STIR
    {
        "id": "el-05-stir",
        "label": "Hành động 4: STIR (Khuấy đều bằng thìa)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1140, "y": 160, "width": 360, "height": 420},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 8900,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Row 1 Col 5: POUR
    {
        "id": "el-06-pour",
        "label": "Hành động 5: POUR (Rót nước)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1500, "y": 160, "width": 360, "height": 420},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 11000,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Row 2 Col 1: PEEL
    {
        "id": "el-07-peel",
        "label": "Hành động 6: PEEL (Gọt vỏ)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 580, "width": 310, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 13200,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Row 2 Col 2: GRATE
    {
        "id": "el-08-grate",
        "label": "Hành động 7: GRATE (Bào sợi)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 390, "y": 580, "width": 380, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 15300,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Row 2 Col 3: KNEAD
    {
        "id": "el-09-knead",
        "label": "Hành động 8: KNEAD (Nhào bột bằng tay)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 770, "y": 580, "width": 370, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 17400,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Row 2 Col 4: DRAIN
    {
        "id": "el-10-drain",
        "label": "Hành động 9: DRAIN (Lọc ráo nước qua rổ)",
        "sequence": 10,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1140, "y": 580, "width": 360, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 19500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 11. Row 2 Col 5: SPRINKLE
    {
        "id": "el-11-sprinkle",
        "label": "Hành động 10: SPRINKLE (Rắc gia vị)",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1500, "y": 580, "width": 360, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 21600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 25000

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
    "sceneId": "test_case_segmentation_12_cooking",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "cooking_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: cooking_lesson-regions.png
regions_png = DIR / "cooking_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "cooking_lesson_animation.mp4"
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
for t in [2, 5, 8, 12, 16, 20, 24]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
