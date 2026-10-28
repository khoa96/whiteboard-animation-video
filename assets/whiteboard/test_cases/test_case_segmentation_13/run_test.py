#!/usr/bin/env python3
"""
Test Case 13: Phân vùng tự động và Hoạt hoạ Môi trường & Phát triển bền vững (ENVIRONMENT AND SUSTAINABILITY)
Quy trình:
1. Phân vùng 9 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: ENVIRONMENT AND SUSTAINABILITY
   - Hàng 1 (4 khái niệm): RENEWABLE ENERGY, EMISSIONS, RECYCLING, LANDFILL
   - Hàng 2 (4 khái niệm): DROUGHT, DEFORESTATION, CONSERVATION, BIODIVERSITY
2. Xuất ảnh phân vùng QA kiểm định: environment_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: environment_lesson_animation.mp4 (không cần voice over).
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

img_path = DIR / "environment_lesson.png"
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
        "id": "el-01-title",
        "label": "Tiêu đề: ENVIRONMENT AND SUSTAINABILITY",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 100, "y": 40, "width": 1720, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Row 1 Col 1: RENEWABLE ENERGY
    {
        "id": "el-02-renewable-energy",
        "label": "Mục 1: RENEWABLE ENERGY (Năng lượng tái tạo)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 160, "width": 380, "height": 490},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2600,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Row 1 Col 2: EMISSIONS
    {
        "id": "el-03-emissions",
        "label": "Mục 2: EMISSIONS (Khí thải công nghiệp)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 480, "y": 160, "width": 480, "height": 430},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 4900,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Row 1 Col 3: RECYCLING
    {
        "id": "el-04-recycling",
        "label": "Mục 3: RECYCLING (Tái chế rác thải)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 960, "y": 160, "width": 480, "height": 430},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 7200,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Row 1 Col 4: LANDFILL
    {
        "id": "el-05-landfill",
        "label": "Mục 4: LANDFILL (Bãi chôn lấp rác)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1440, "y": 160, "width": 420, "height": 430},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 9500,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Row 2 Col 1: DROUGHT
    {
        "id": "el-06-drought",
        "label": "Mục 5: DROUGHT (Hạn hán khô cằn)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 650, "width": 380, "height": 400},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 11800,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Row 2 Col 2: DEFORESTATION
    {
        "id": "el-07-deforestation",
        "label": "Mục 6: DEFORESTATION (Nạn phá rừng)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 480, "y": 590, "width": 480, "height": 460},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 14100,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Row 2 Col 3: CONSERVATION
    {
        "id": "el-08-conservation",
        "label": "Mục 7: CONSERVATION (Bảo tồn thiên nhiên)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 960, "y": 590, "width": 480, "height": 460},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 16400,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Row 2 Col 4: BIODIVERSITY
    {
        "id": "el-09-biodiversity",
        "label": "Mục 8: BIODIVERSITY (Đa dạng sinh học)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1440, "y": 590, "width": 420, "height": 460},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 18700,
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
    "sceneId": "test_case_segmentation_13_environment",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "environment_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: environment_lesson-regions.png
regions_png = DIR / "environment_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "environment_lesson_animation.mp4"
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
for t in [2, 5, 8, 12, 16, 20]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
