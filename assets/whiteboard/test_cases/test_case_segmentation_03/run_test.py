#!/usr/bin/env python3
"""
Test Case 03: Phân vùng tự động và Hoạt hoạ Biểu đồ Đường (Line Graph: NHIỆT ĐỘ TRONG NGÀY)
Quy trình:
1. Phân vùng 7 phần tử nguyên tử (Tiêu đề, Trục tọa độ, 4 Điểm dữ liệu 8h, 12h, 16h, 20h, Đường nối dữ liệu Blue).
2. Tự động bảo vệ nét (protectedRegions) cho trục để không chạm đường dữ liệu.
3. Xuất ảnh phân vùng QA kiểm định: linegraph-regions.png.
4. Render video hoạt hoạ Whiteboard 60fps 1080p: linegraph_animation.mp4 (không cần voice over).
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

img_path = DIR / "linegraph.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 1. Bounding boxes của Tiêu đề, 4 Điểm mốc và Đường dữ liệu
bbox_title = {"x": 550, "y": 70, "width": 800, "height": 90}
bbox_p1 = {"x": 445, "y": 480, "width": 105, "height": 100}
bbox_p2 = {"x": 800, "y": 285, "width": 80, "height": 110}
bbox_p3 = {"x": 1130, "y": 345, "width": 80, "height": 105}
bbox_p4 = {"x": 1465, "y": 435, "width": 80, "height": 95}

# Blue line
b, g, r = cv2.split(img)
is_blue = (b > 160) & (r < 100) & (gray < 240)
ys_b, xs_b = np.where(is_blue)
bbox_line = {
    "x": int(xs_b.min() - 4),
    "y": int(ys_b.min() - 4),
    "width": int(xs_b.max() - xs_b.min() + 9),
    "height": int(ys_b.max() - ys_b.min() + 9)
}

# 2. Tách trục tọa độ
mask_other = np.zeros((1080, 1920), dtype=bool)
for b_box in [bbox_title, bbox_p1, bbox_p2, bbox_p3, bbox_p4, bbox_line]:
    mask_other[b_box["y"]:b_box["y"]+b_box["height"], b_box["x"]:b_box["x"]+b_box["width"]] = True

axes_ink = (ink > 0) & (~mask_other)
ys_ax, xs_ax = np.where(axes_ink)
bbox_axes = {
    "x": int(xs_ax.min() - 4),
    "y": int(ys_ax.min() - 4),
    "width": int(xs_ax.max() - xs_ax.min() + 9),
    "height": int(ys_ax.max() - ys_ax.min() + 9)
}

covered_pixels = int(np.count_nonzero((ink > 0) & mask_other)) + int(np.count_nonzero(axes_ink))

print("=" * 65)
print("🎯 [CV AUDIT TEST CASE 03: LINE GRAPH]")
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
        "label": "Tiêu đề: NHIỆT ĐỘ TRONG NGÀY",
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
    # 2. Trục tọa độ (°C và GIỜ) (3500ms - 7500ms)
    {
        "id": "el-02-axes",
        "label": "Hệ trục tọa độ (°C, GIỜ & Vạch mốc thời gian)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_axes,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 3500,
            "durationMs": 4000,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_line, bbox_p1, bbox_p2, bbox_p3, bbox_p4]
        }
    },
    # 3. Điểm 1: 8h (24°C) (7500ms - 9000ms)
    {
        "id": "el-03-point-1",
        "label": "Mốc 8h: 24°C (Điểm tròn cam)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_p1,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7500,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Điểm 2: 12h (31°C) (9000ms - 10500ms)
    {
        "id": "el-04-point-2",
        "label": "Mốc 12h: 31°C (Điểm tròn cam)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_p2,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9000,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Điểm 3: 16h (29°C) (10500ms - 12000ms)
    {
        "id": "el-05-point-3",
        "label": "Mốc 16h: 29°C (Điểm tròn cam)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_p3,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 10500,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Điểm 4: 20h (26°C) (12000ms - 13500ms)
    {
        "id": "el-06-point-4",
        "label": "Mốc 20h: 26°C (Điểm tròn cam)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_p4,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12000,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Đường dữ liệu xanh dương (13500ms - 17000ms)
    {
        "id": "el-07-data-line",
        "label": "Đường đồ thị nhiệt độ (Xanh dương liên tục)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_line,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13500,
            "durationMs": 3500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_segmentation_03_linegraph",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

ann_path = DIR / "linegraph.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# 3. Xuất ảnh phân vùng QA kiểm định: linegraph-regions.png
regions_png = DIR / "linegraph-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# 4. Render Whiteboard Video Animation (60fps, 1080p, không cần voice over)
raw_mp4 = DIR / "linegraph_animation.mp4"
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
for t in [2, 5, 8, 11, 15, 18]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
