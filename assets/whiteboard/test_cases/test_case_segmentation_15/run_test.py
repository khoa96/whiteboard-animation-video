#!/usr/bin/env python3
"""
Test Case 15: Phân vùng tự động và Hoạt hoạ So sánh Bản chất Năng lượng (WHAT IS THE DIFFERENCE?)
Quy trình:
1. Phân vùng 7 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề chính: WHAT IS THE DIFFERENCE?
   - Cột RENEWABLE: Tiêu đề nhánh + Câu khẳng định REPLENISHED NATURALLY + Minh hoạ vòng lặp tái sinh (Sun, Wind, Circular Arrows)
   - Cột NON-RENEWABLE: Tiêu đề nhánh + Câu khẳng định NOT REPLACED QUICKLY + Minh hoạ giới hạn hữu hạn (Coal, Oil Barrel, Gauge Meter)
2. Xuất ảnh phân vùng QA kiểm định: replenished_comparison-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: replenished_comparison_animation.mp4 (không cần voice over).
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

img_path = DIR / "replenished_comparison.png"
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
        "id": "rc-01-title",
        "label": "Tiêu đề: WHAT IS THE DIFFERENCE?",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 300, "y": 40, "width": 1320, "height": 160},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Left Header: RENEWABLE
    {
        "id": "rc-02-left-header",
        "label": "Nhánh 1: RENEWABLE (Năng lượng tái tạo)",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 100, "y": 200, "width": 850, "height": 140},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 2700,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Left Statement: REPLENISHED NATURALLY
    {
        "id": "rc-03-left-statement",
        "label": "Khẳng định: REPLENISHED NATURALLY (Được tái tạo tự nhiên)",
        "sequence": 3,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 100, "y": 340, "width": 850, "height": 110},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4400,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Left Visual: Sun, Wind, Renewal Arrow
    {
        "id": "rc-04-left-visual",
        "label": "Minh họa tái sinh: Mặt trời, Tuabin gió và Mũi tên tuần hoàn",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 450, "width": 850, "height": 590},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 6600,
            "durationMs": 4000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Right Header: NON-RENEWABLE
    {
        "id": "rc-05-right-header",
        "label": "Nhánh 2: NON-RENEWABLE (Năng lượng không tái tạo)",
        "sequence": 5,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 970, "y": 200, "width": 850, "height": 140},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 10800,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Right Statement: NOT REPLACED QUICKLY
    {
        "id": "rc-06-right-statement",
        "label": "Khẳng định: NOT REPLACED QUICKLY (Không thể phục hồi nhanh)",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 970, "y": 340, "width": 850, "height": 110},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12800,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Right Visual: Coal, Oil Barrel, Gauge Meter
    {
        "id": "rc-07-right-visual",
        "label": "Minh họa hữu hạn: Đống than, Thùng dầu mỏ và Đồng hồ đo cạn kiệt",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 970, "y": 450, "width": 850, "height": 590},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 15000,
            "durationMs": 4000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 21000

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
    "sceneId": "test_case_segmentation_15_replenished_comparison",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "replenished_comparison.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: replenished_comparison-regions.png
regions_png = DIR / "replenished_comparison-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "replenished_comparison_animation.mp4"
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
for t in [2, 4, 6, 9, 12, 14, 18, 20]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
