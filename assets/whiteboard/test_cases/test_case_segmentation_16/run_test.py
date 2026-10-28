#!/usr/bin/env python3
"""
Test Case 16: Phân vùng tự động và Hoạt hoạ Vòng tuần hoàn của Nước (THE WATER CYCLE)
Quy trình:
1. Phân vùng 8 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: THE WATER CYCLE
   - Mặt trời (Sun)
   - Giai đoạn 1: Bốc hơi (Evaporation rising arrows + 1. EVAPORATION)
   - Mũi tên dẫn khí bốc lên mây (Evaporation arc arrow)
   - Giai đoạn 2: Ngưng tụ (Condensation cloud + 2. CONDENSATION + arrow)
   - Giai đoạn 3: Giáng thủy / Mưa rơi (Raincloud + falling raindrops)
   - Nhãn giai đoạn 3: 3. PRECIPITATION
   - Vùng tích nước và dòng hồi lưu khép kín (Water waves + return cycle flow arrow)
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

# 8 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "wc-01-title",
        "label": "Tiêu đề: THE WATER CYCLE",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 400, "y": 40, "width": 1120, "height": 150},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Sun (top-left)
    {
        "id": "wc-02-sun",
        "label": "Mặt trời: Sun (Năng lượng nhiệt khởi nguồn)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 190, "width": 450, "height": 380},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2700,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Evaporation Stage: Rising vapor arrows + label 1. EVAPORATION
    {
        "id": "wc-03-evaporation",
        "label": "Giai đoạn 1: Bốc hơi (1. EVAPORATION & Hơi nước bốc lên)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 500, "y": 540, "width": 640, "height": 220},
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 4900,
            "durationMs": 2600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Cycle Arrow 1: Rising vapor arc to cloud
    {
        "id": "wc-04-evap-arrow",
        "label": "Mũi tên chu trình: Hơi nước dẫn lên tầng mây",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 500, "y": 340, "width": 280, "height": 200},
        "reveal": {
            "direction": "bottom_to_top",
            "startMs": 7700,
            "durationMs": 1400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Condensation Stage: Cloud + 2. CONDENSATION + transition arrow
    {
        "id": "wc-05-condensation",
        "label": "Giai đoạn 2: Ngưng tụ (2. CONDENSATION & Đám mây tích tụ)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 780, "y": 190, "width": 940, "height": 280},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9300,
            "durationMs": 2800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Precipitation Stage - Cloud & Rain: Raincloud + falling raindrops
    {
        "id": "wc-06-rain-cloud",
        "label": "Giai đoạn 3: Mưa rơi (Đám mây giáng thuỷ & các giọt mưa)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1200, "y": 470, "width": 640, "height": 298},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 12300,
            "durationMs": 2600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Precipitation Stage - Label: 3. PRECIPITATION
    {
        "id": "wc-07-precip-label",
        "label": "Nhãn giai đoạn 3: 3. PRECIPITATION",
        "sequence": 7,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1330, "y": 768, "width": 500, "height": 112},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15100,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Water Body & Return Cycle Flow: Water waves + return flow arrow
    {
        "id": "wc-08-water-return",
        "label": "Dòng hồi lưu & Tụ thủy: Các tầng sóng nước & Mũi tên hoàn tất chu trình",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 150, "y": 768, "width": 1175, "height": 260},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 16800,
            "durationMs": 3800,
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
    "sceneId": "test_case_segmentation_16_water_cycle",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
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
for t in [2, 4, 7, 10, 13, 16, 19, 21]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
