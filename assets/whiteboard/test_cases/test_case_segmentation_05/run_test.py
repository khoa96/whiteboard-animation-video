#!/usr/bin/env python3
"""
Test Case 05: Phân vùng tự động và Hoạt hoạ Biểu đồ Cột So Sánh Doanh Số (PRODUCT SALES COMPARISON)
Quy trình:
1. Phân vùng 8 phần tử nguyên tử:
   - Tiêu đề: PRODUCT SALES COMPARISON
   - Trục tung & SALES + vạch chia 0..40
   - Trục hoành & PRODUCT + nhãn Product A, B, C
   - Đường mục tiêu đứt nét & Nhãn TARGET (y=30)
   - Cột A (Doanh số = 20, màu xanh pastel)
   - Cột B (Doanh số = 35, màu cam pastel)
   - Cột C (Doanh số = 25, màu xanh lá pastel)
   - Bảng chú giải (Legend: Solid Bars & Dashed Line)
2. Xuất ảnh phân vùng QA kiểm định: sales_chart-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: sales_chart_animation.mp4 (không cần voice over).
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

img_path = DIR / "sales_chart.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# Bounding boxes
bbox_title = {"x": 408, "y": 85, "width": 1103, "height": 66}
bbox_axis_v = {"x": 340, "y": 240, "width": 180, "height": 610}
bbox_axis_h = {"x": 458, "y": 820, "width": 1018, "height": 122}
bbox_target = {"x": 459, "y": 340, "width": 1192, "height": 80}
bbox_bar_a = {"x": 550, "y": 516, "width": 200, "height": 364}
bbox_bar_b = {"x": 830, "y": 283, "width": 200, "height": 597}
bbox_bar_c = {"x": 1130, "y": 411, "width": 200, "height": 469}
bbox_legend = {"x": 1487, "y": 549, "width": 313, "height": 81}

total_duration_ms = 21000

elements = [
    # 1. Title (500ms - 3000ms)
    {
        "id": "el-01-title",
        "label": "Tiêu đề: PRODUCT SALES COMPARISON",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": bbox_title,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2500,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 2. Vertical Axis & SALES (3000ms - 5500ms)
    {
        "id": "el-02-axis-v",
        "label": "Trục tung SALES & Thang đo (0, 10, 20, 30, 40)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_axis_v,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 3000,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Horizontal Axis & PRODUCT (5500ms - 8000ms)
    {
        "id": "el-03-axis-h",
        "label": "Trục hoành PRODUCT & Nhãn sản phẩm (A, B, C)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_axis_h,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": [bbox_bar_a, bbox_bar_b, bbox_bar_c]
        }
    },
    # 4. Target Reference Line (8000ms - 10000ms)
    {
        "id": "el-04-target",
        "label": "Đường mục tiêu đứt nét & Nhãn TARGET (y=30)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_target,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8000,
            "durationMs": 2000,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_bar_a, bbox_bar_b, bbox_bar_c]
        }
    },
    # 5. Bar A (10000ms - 12500ms)
    {
        "id": "el-05-bar-a",
        "label": "Cột Product A: Doanh số = 20",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_a,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 10000,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Bar B (12500ms - 15000ms)
    {
        "id": "el-06-bar-b",
        "label": "Cột Product B: Doanh số = 35 (Vượt Target)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_b,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 12500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Bar C (15000ms - 17500ms)
    {
        "id": "el-07-bar-c",
        "label": "Cột Product C: Doanh số = 25",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_bar_c,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 15000,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Legend (17500ms - 19500ms)
    {
        "id": "el-08-legend",
        "label": "Bảng chú giải (Legend: Solid Bars & Dashed Target Line)",
        "sequence": 8,
        "type": "text",
        "colorMode": "none",
        "region": bbox_legend,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_segmentation_05_saleschart",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

ann_path = DIR / "sales_chart.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: sales_chart-regions.png
regions_png = DIR / "sales_chart-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "sales_chart_animation.mp4"
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
for t in [2, 5, 8, 11, 14, 17, 20]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
