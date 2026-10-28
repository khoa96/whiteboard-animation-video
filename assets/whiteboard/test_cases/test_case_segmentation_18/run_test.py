#!/usr/bin/env python3
"""
Test Case 18: Phân vùng tự động và Hoạt hoạ Nguyên nhân Băng tan (WHY DOES ICE MELT?)
Quy trình:
1. Phân vùng 6 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: WHY DOES ICE MELT?
   - Nguồn nhiệt: HEAT (Mặt trời & nhãn HEAT)
   - Truyền nhiệt: HEAT MOVES INTO THE ICE (Các mũi tên cam hướng vào khối băng & nhãn mô tả)
   - Khối băng: ICE (Khối băng đặc & nhãn ICE)
   - Biến đổi pha: THE ICE MELTS (Mũi tên xanh chuyển trạng thái & nhãn mô tả)
   - Vũng nước tan: MELTED WATER (Vũng nước lỏng & nhãn MELTED WATER)
2. Xuất ảnh phân vùng QA kiểm định: why_ice_melts-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: why_ice_melts_animation.mp4 (không cần voice over).
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

img_path = DIR / "why_ice_melts.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 6 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "im-01-title",
        "label": "Tiêu đề: WHY DOES ICE MELT?",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 400, "y": 60, "width": 1120, "height": 160},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Left: Sun & HEAT label
    {
        "id": "im-02-heat-sun",
        "label": "Nguồn phát nhiệt: HEAT (Mặt trời & nhãn HEAT)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 320, "width": 380, "height": 510},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2700,
            "durationMs": 2600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Transition 1: HEAT MOVES INTO THE ICE & orange arrows
    {
        "id": "im-03-heat-moves",
        "label": "Quá trình truyền nhiệt: HEAT MOVES INTO THE ICE",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 460, "y": 340, "width": 340, "height": 490},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5500,
            "durationMs": 2800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Center: Solid Ice Cube & ICE label
    {
        "id": "im-04-ice-cube",
        "label": "Trạng thái rắn ban đầu: ICE (Khối băng đặc & nhãn ICE)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 800, "y": 340, "width": 320, "height": 490},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 8500,
            "durationMs": 2600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Transition 2: THE ICE MELTS & blue arrow
    {
        "id": "im-05-ice-melts",
        "label": "Hiện tượng biến đổi pha: THE ICE MELTS",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1120, "y": 340, "width": 310, "height": 490},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11300,
            "durationMs": 2800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Right: Puddle & MELTED WATER label
    {
        "id": "im-06-melted-water",
        "label": "Trạng thái lỏng kết quả: MELTED WATER (Vũng nước tan & nhãn MELTED WATER)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1430, "y": 340, "width": 430, "height": 490},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 14300,
            "durationMs": 3200,
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
    "sceneId": "test_case_segmentation_18_why_ice_melts",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "why_ice_melts.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: why_ice_melts-regions.png
regions_png = DIR / "why_ice_melts-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "why_ice_melts_animation.mp4"
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
for t in [2, 4, 7, 10, 13, 16, 18, 19]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
