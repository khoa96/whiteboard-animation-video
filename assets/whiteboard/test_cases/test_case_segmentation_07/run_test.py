#!/usr/bin/env python3
"""
Test Case 07: Phân vùng tự động và Hoạt hoạ Bài giảng Phân số (UNDERSTANDING FRACTIONS)
Quy trình:
1. Phân vùng 10 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề chính: UNDERSTANDING FRACTIONS
   - Khối hình tròn phân số: 1/2 (xanh lam), 1/3 (xanh lá), 3/4 (cam)
   - Khối thanh phân số (Fraction Bars): 1/2, 1/3, 3/4
   - Trục số (Number line) từ 0 đến 1 có mốc 1/2, 3/4
   - Bất đẳng thức so sánh: 1/2 < 3/4
   - Định nghĩa quy tắc: A fraction represents part of a whole.
2. Xuất ảnh phân vùng QA kiểm định: fractions_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: fractions_lesson_animation.mp4 (không cần voice over).
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

img_path = DIR / "fractions_lesson.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 10 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "el-01-title",
        "label": "Tiêu đề: UNDERSTANDING FRACTIONS",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 350, "y": 40, "width": 1220, "height": 110},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Circle 1/2
    {
        "id": "el-02-circle-half",
        "label": "Hình tròn phân số 1/2 (Tô xanh lam)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 300, "y": 160, "width": 380, "height": 290},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 2600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Circle 1/3
    {
        "id": "el-03-circle-third",
        "label": "Hình tròn phân số 1/3 (Tô xanh lá)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 760, "y": 160, "width": 390, "height": 290},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4700,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Circle 3/4
    {
        "id": "el-04-circle-three-quarters",
        "label": "Hình tròn phân số 3/4 (Tô cam)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1230, "y": 160, "width": 390, "height": 290},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6800,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Bar 1/2
    {
        "id": "el-05-bar-half",
        "label": "Thanh phân số 1/2 (2 ô, tô 1 ô xanh lam)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 160, "y": 470, "width": 530, "height": 150},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9000,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Bar 1/3
    {
        "id": "el-06-bar-third",
        "label": "Thanh phân số 1/3 (3 ô, tô 1 ô xanh lá)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 700, "y": 470, "width": 520, "height": 150},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11100,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Bar 3/4
    {
        "id": "el-07-bar-three-quarters",
        "label": "Thanh phân số 3/4 (4 ô, tô 3 ô cam)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1230, "y": 470, "width": 530, "height": 150},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13200,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Number line
    {
        "id": "el-08-number-line",
        "label": "Trục số (Number line) 0 -> 1 kèm mốc 1/2 & 3/4",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 400, "y": 640, "width": 1120, "height": 160},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15400,
            "durationMs": 3000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Equation
    {
        "id": "el-09-equation",
        "label": "So sánh phân số: 1/2 < 3/4",
        "sequence": 9,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 800, "y": 810, "width": 320, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 18600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Definition
    {
        "id": "el-10-definition",
        "label": "Quy tắc: A fraction represents part of a whole.",
        "sequence": 10,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 380, "y": 940, "width": 1160, "height": 110},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 20800,
            "durationMs": 2800,
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
    "sceneId": "test_case_segmentation_07_fractions",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "fractions_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: fractions_lesson-regions.png
regions_png = DIR / "fractions_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "fractions_lesson_animation.mp4"
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
