#!/usr/bin/env python3
"""
Test Case 17: Phân vùng tự động và Hoạt hoạ Cơ chế Bốc hơi Nước (1. EVAPORATION)
Quy trình:
1. Phân vùng 7 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: 1. EVAPORATION
   - Mặt trời: Sun (Nguồn nhiệt lượng)
   - Khối nước lỏng: Liquid water waves
   - Nhãn nước lỏng: LIQUID WATER
   - Các mũi tên hơi nước bốc lên: Upward vapor arrows
   - Nhãn hơi nước: WATER VAPOR
   - Câu giải thích giáo dục: HEAT TURNS LIQUID WATER INTO WATER VAPOR.
2. Xuất ảnh phân vùng QA kiểm định: evaporation_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: evaporation_lesson_animation.mp4 (không cần voice over).
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

img_path = DIR / "evaporation_lesson.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 7 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "ev-01-title",
        "label": "Tiêu đề: 1. EVAPORATION",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 400, "y": 40, "width": 1120, "height": 130},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Sun (upper center)
    {
        "id": "ev-02-sun",
        "label": "Mặt trời: Sun (Nguồn phát nhiệt bức xạ)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 700, "y": 180, "width": 520, "height": 310},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2700,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Liquid water waves
    {
        "id": "ev-03-liquid-water",
        "label": "Khối nước lỏng: Các tầng sóng nước",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 450, "y": 670, "width": 1020, "height": 125},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5100,
            "durationMs": 2400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Label: LIQUID WATER
    {
        "id": "ev-04-water-label",
        "label": "Nhãn danh xưng: LIQUID WATER",
        "sequence": 4,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 650, "y": 795, "width": 620, "height": 85},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7700,
            "durationMs": 1600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Upward vapor arrows
    {
        "id": "ev-05-vapor-arrows",
        "label": "Động năng bốc hơi: 3 mũi tên chỉ hướng hơi nước bốc lên",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 750, "y": 495, "width": 350, "height": 175},
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 9500,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Label: WATER VAPOR
    {
        "id": "ev-06-vapor-label",
        "label": "Nhãn danh xưng: WATER VAPOR",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1100, "y": 495, "width": 500, "height": 175},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11900,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Bottom sentence: HEAT TURNS LIQUID WATER INTO WATER VAPOR.
    {
        "id": "ev-07-sentence",
        "label": "Khái quát bản chất: HEAT TURNS LIQUID WATER INTO WATER VAPOR.",
        "sequence": 7,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 200, "y": 890, "width": 1520, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 14000,
            "durationMs": 3500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 20000

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
    "sceneId": "test_case_segmentation_17_evaporation",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "evaporation_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: evaporation_lesson-regions.png
regions_png = DIR / "evaporation_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "evaporation_lesson_animation.mp4"
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
for t in [2, 4, 7, 9, 12, 14, 17, 19]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
