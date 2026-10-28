#!/usr/bin/env python3
"""
Test Case 14: Phân vùng tự động và Hoạt hoạ Hai Dạng Năng lượng (TWO TYPES OF ENERGY)
Quy trình:
1. Phân vùng 9 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: TWO TYPES OF ENERGY
   - Nhánh RENEWABLE: Tiêu đề nhánh + SUN, WIND, WATER
   - Nhánh NON-RENEWABLE: Tiêu đề nhánh + COAL, OIL, GAS
2. Xuất ảnh phân vùng QA kiểm định: energy_types-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: energy_types_animation.mp4 (không cần voice over).
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

img_path = DIR / "energy_types.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 9 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "et-01-title",
        "label": "Tiêu đề: TWO TYPES OF ENERGY",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 400, "y": 40, "width": 1120, "height": 140},
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
        "id": "et-02-renewable-header",
        "label": "Nhánh 1: RENEWABLE (Năng lượng tái tạo)",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 100, "y": 180, "width": 800, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 2700,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Left Item 1: SUN
    {
        "id": "et-03-sun",
        "label": "Mục 1: SUN (Năng lượng mặt trời)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 300, "width": 400, "height": 400},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 4400,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Left Item 2: WIND
    {
        "id": "et-04-wind",
        "label": "Mục 2: WIND (Năng lượng gió)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 500, "y": 300, "width": 400, "height": 400},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 6800,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Left Item 3: WATER
    {
        "id": "et-05-water",
        "label": "Mục 3: WATER (Năng lượng nước)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 700, "width": 800, "height": 340},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 9200,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Right Header: NON-RENEWABLE
    {
        "id": "et-06-nonrenewable-header",
        "label": "Nhánh 2: NON-RENEWABLE (Năng lượng không tái tạo)",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1020, "y": 180, "width": 800, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11600,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Right Item 1: COAL
    {
        "id": "et-07-coal",
        "label": "Mục 4: COAL (Than đá)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1020, "y": 300, "width": 430, "height": 400},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 13600,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Right Item 2: OIL
    {
        "id": "et-08-oil",
        "label": "Mục 5: OIL (Dầu mỏ)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1450, "y": 300, "width": 370, "height": 400},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 16000,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Right Item 3: GAS
    {
        "id": "et-09-gas",
        "label": "Mục 6: GAS (Khí đốt tự nhiên)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1020, "y": 700, "width": 800, "height": 340},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 18400,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 22000

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
    "sceneId": "test_case_segmentation_14_energy_types",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "energy_types.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: energy_types-regions.png
regions_png = DIR / "energy_types-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "energy_types_animation.mp4"
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
for t in [2, 4, 7, 10, 13, 16, 19, 21]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
