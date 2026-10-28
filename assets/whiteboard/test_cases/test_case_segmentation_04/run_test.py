#!/usr/bin/env python3
"""
Test Case 04: Phân vùng tự động và Hoạt hoạ Sơ đồ Khoa học (Science Diagram: THE WATER CYCLE)
Quy trình:
1. Phân vùng 9 phần tử nguyên tử:
   - Tiêu đề THE WATER CYCLE
   - Mặt trời (Sun)
   - Hồ nước (Lake)
   - Mũi tên Bay hơi (EVAPORATION)
   - Mũi tên Ngưng tụ (CONDENSATION)
   - Đám mây (Clouds)
   - Mưa rơi & Mũi tên Giáng thủy (PRECIPITATION)
   - Dãy núi & Cây cối & Dòng sông (Mountain, Trees, River)
   - Mũi tên Tích tụ dòng chảy (COLLECTION)
2. Xuất ảnh phân vùng QA kiểm định: water_cycle-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: water_cycle_animation.mp4 (không cần voice over).
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

img_path = DIR / "water_cycle.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# Bounding boxes
bbox_title = {"x": 569, "y": 64, "width": 782, "height": 77}
bbox_sun = {"x": 104, "y": 72, "width": 399, "height": 396}
bbox_lake = {"x": 355, "y": 750, "width": 1045, "height": 270}
bbox_evap = {"x": 519, "y": 400, "width": 401, "height": 380}
bbox_cond = {"x": 622, "y": 240, "width": 478, "height": 190}
bbox_clouds = {"x": 780, "y": 177, "width": 753, "height": 183}
bbox_precip = {"x": 1200, "y": 300, "width": 350, "height": 230}
bbox_mountain = {"x": 1000, "y": 400, "width": 850, "height": 450}
bbox_collec = {"x": 1200, "y": 800, "width": 535, "height": 180}

total_duration_ms = 22000

elements = [
    # 1. Title (500ms - 3000ms)
    {
        "id": "el-01-title",
        "label": "Tiêu đề: THE WATER CYCLE",
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
    # 2. Sun (3000ms - 5500ms)
    {
        "id": "el-02-sun",
        "label": "Mặt trời chiếu sáng (Sun)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_sun,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 3000,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Lake (5500ms - 7500ms)
    {
        "id": "el-03-lake",
        "label": "Hồ nước mặt đất (Lake)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_lake,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Evaporation Arrow (7500ms - 9500ms)
    {
        "id": "el-04-evap",
        "label": "Giai đoạn 1: Bay hơi (EVAPORATION)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_evap,
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 7500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": [bbox_lake]
        }
    },
    # 5. Condensation Arrow (9500ms - 11500ms)
    {
        "id": "el-05-cond",
        "label": "Giai đoạn 2: Ngưng tụ (CONDENSATION)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_cond,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": [bbox_sun]
        }
    },
    # 6. Clouds (11500ms - 13500ms)
    {
        "id": "el-06-clouds",
        "label": "Đám mây tích tụ hơi nước (Clouds)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_clouds,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Precipitation Arrow & Raindrops (13500ms - 15500ms)
    {
        "id": "el-07-precip",
        "label": "Giai đoạn 3: Giáng thủy / Mưa rơi (PRECIPITATION)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_precip,
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 13500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": [bbox_clouds]
        }
    },
    # 8. Mountain & Trees & River (15500ms - 18000ms)
    {
        "id": "el-08-mountain",
        "label": "Núi đồi, Rừng cây & Dòng sông",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_mountain,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15500,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Collection Arrow (18000ms - 20000ms)
    {
        "id": "el-09-collec",
        "label": "Giai đoạn 4: Thu nhận dòng chảy về hồ (COLLECTION)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_collec,
        "reveal": {
            "direction": "right_to_left",
            "startMs": 18000,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": [bbox_lake, bbox_mountain]
        }
    }
]

annotation = {
    "sceneId": "test_case_segmentation_04_watercycle",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

ann_path = DIR / "water_cycle.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: water_cycle-regions.png
regions_png = DIR / "water_cycle-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "water_cycle_animation.mp4"
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
for t in [2, 5, 8, 11, 14, 18, 21]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
