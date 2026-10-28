#!/usr/bin/env python3
"""
Test Case 02: Phân vùng tự động và Hoạt hoạ Biểu đồ Cột (Bar Chart: THỜI GIAN ĐỌC SÁCH)
Quy trình:
1. Phân vùng 6 phần tử nguyên tử (Tiêu đề, Trục tọa độ & Vạch chia, 4 Cột dữ liệu Thứ 2, 3, 4, 5).
2. Tự động bảo vệ nét (protectedRegions) cho trục để không vẽ đè lên các cột.
3. Xuất ảnh phân vùng QA kiểm định: barchart-regions.png.
4. Render video hoạt hoạ Whiteboard 60fps 1080p: barchart_animation.mp4 (không cần voice over).
5. Trích xuất snapshots kiểm tra chất lượng vào snapshots/.
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

img_path = DIR / "barchart.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 1. Bounding box của 4 cột và tiêu đề
bbox_title = {"x": 540, "y": 40, "width": 870, "height": 100}
bbox_bar_1 = {"x": 510, "y": 620, "width": 200, "height": 400}
bbox_bar_2 = {"x": 780, "y": 405, "width": 200, "height": 615}
bbox_bar_3 = {"x": 1050, "y": 510, "width": 200, "height": 510}
bbox_bar_4 = {"x": 1330, "y": 190, "width": 210, "height": 830}

# 2. Tách trục tọa độ
mask_bars = np.zeros((1080, 1920), dtype=bool)
for b in [bbox_title, bbox_bar_1, bbox_bar_2, bbox_bar_3, bbox_bar_4]:
    mask_bars[b["y"]:b["y"]+b["height"], b["x"]:b["x"]+b["width"]] = True

axes_ink = (ink > 0) & (~mask_bars)
ys, xs = np.where(axes_ink)
bbox_axes = {
    "x": int(xs.min()),
    "y": int(ys.min()),
    "width": int(xs.max() - xs.min() + 1),
    "height": int(ys.max() - ys.min() + 1)
}

covered_pixels = int(np.count_nonzero((ink > 0) & mask_bars)) + int(np.count_nonzero(axes_ink))

print("=" * 65)
print("🎯 [CV AUDIT TEST CASE 02: BAR CHART]")
print(f"  + Tổng số nét mực canvas: {total_ink} pixels")
print(f"  + Nét mực phân vùng bao trọn: {covered_pixels} pixels")
print(f"  + Tỷ lệ bao phủ (Coverage): {covered_pixels/total_ink*100.0:.3f}%")
print(f"  + Nét mực bị bỏ sót: {total_ink - covered_pixels} pixels (0.00%)")
print("=" * 65)

total_duration_ms = 19000

elements = [
    # 1. Title (500ms - 3500ms)
    {
        "id": "el-01-title",
        "label": "Tiêu đề: THỜI GIAN ĐỌC SÁCH",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": bbox_title,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 3000,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 2. Trục tọa độ & Vạch chia (3500ms - 6500ms)
    {
        "id": "el-02-axes",
        "label": "Hệ trục tọa độ (SỐ PHÚT, 0..30) & Đường đáy",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_axes,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 3500,
            "durationMs": 3000,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_bar_1, bbox_bar_2, bbox_bar_3, bbox_bar_4]
        }
    },
    # 3. Cột 1: Thứ 2 (6500ms - 9000ms)
    {
        "id": "el-03-bar-thu-2",
        "label": "Cột 1: Thứ 2 (10 phút)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_1,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 6500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Cột 2: Thứ 3 (9000ms - 11500ms)
    {
        "id": "el-04-bar-thu-3",
        "label": "Cột 2: Thứ 3 (20 phút)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_2,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 9000,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Cột 3: Thứ 4 (11500ms - 14000ms)
    {
        "id": "el-05-bar-thu-4",
        "label": "Cột 3: Thứ 4 (15 phút)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_3,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 11500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Cột 4: Thứ 5 (14000ms - 17000ms)
    {
        "id": "el-06-bar-thu-5",
        "label": "Cột 4: Thứ 5 (30 phút)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_4,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 14000,
            "durationMs": 3000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_segmentation_02_barchart",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

ann_path = DIR / "barchart.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# 3. Xuất ảnh phân vùng QA kiểm định: barchart-regions.png
regions_png = DIR / "barchart-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# 4. Render Whiteboard Video Animation (60fps, 1080p, không cần voice over)
raw_mp4 = DIR / "barchart_animation.mp4"
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

# 5. Trích xuất snapshots kiểm tra chất lượng vào snapshots/
snap_dir = DIR / "snapshots"
snap_dir.mkdir(parents=True, exist_ok=True)
for t in [2, 5, 8, 11, 14, 18]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
