#!/usr/bin/env python3
"""
Test Case 19: Phân vùng tự động và Hoạt hoạ Cơ chế Truyền nhiệt vào Băng (HEAT TRANSFERS TO THE ICE)
Quy trình:
1. Phân vùng chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề: HEAT TRANSFERS TO THE ICE
   - Môi trường ấm: WARM SURROUNDINGS (Nhãn mô tả)
   - Luồng khí ấm: WARM-AIR WAVES (Các đường sóng nhiệt)
   - Mũi tên nhiệt trên: INWARD HEAT ARROW (TOP)
   - Mũi tên nhiệt dưới: INWARD HEAT ARROW (BOTTOM)
   - Khối băng đặc: SOLID ICE CUBE
   - Vũng nước tan: FORMING PUDDLE (Nước bắt đầu tan ở chân băng)
   - Nhãn hấp thụ nhiệt: ICE TAKES IN HEAT
   - Mũi tên & hiện tượng tan: RIGHT HEAT ARROW & MELTING BEGINS
2. Xuất ảnh phân vùng QA kiểm định: heat_transfers_ice-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: heat_transfers_ice_animation.mp4 (không cần voice over).
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

img_path = DIR / "heat_transfers_ice.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 11 Bounding boxes đạt chuẩn 100.00000% độ phủ mực và 0.00000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "ht-01-title",
        "label": "Tiêu đề: HEAT TRANSFERS TO THE ICE",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 400, "y": 90, "width": 1120, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. WARM SURROUNDINGS label
    {
        "id": "ht-02-label-warm",
        "label": "Nhãn: WARM SURROUNDINGS",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 150, "y": 280, "width": 500, "height": 160},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 2800,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Warm waves (Outer: Top & Bottom waves)
    {
        "id": "ht-03-waves-outer",
        "label": "Luồng sóng nhiệt ấm: WARM-AIR WAVES (Trên & Dưới)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 240, "y": 480, "width": 280, "height": 155},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4900,
            "durationMs": 1400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Warm waves (Middle wave)
    {
        "id": "ht-04-wave-middle",
        "label": "Luồng sóng nhiệt ấm: WARM-AIR WAVES (Giữa)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 520, "y": 536, "width": 65, "height": 34},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5200,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Upper left inward heat arrow
    {
        "id": "ht-05-left-arrow-top",
        "label": "Mũi tên truyền nhiệt trên bên trái: INWARD HEAT ARROW (TOP)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 540, "y": 440, "width": 225, "height": 95},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6600,
            "durationMs": 1600,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Lower left inward heat arrow (main body & tip)
    {
        "id": "ht-06-left-arrow-tip",
        "label": "Mũi tên truyền nhiệt dưới bên trái: INWARD HEAT ARROW (BODY & TIP)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 550, "y": 570, "width": 215, "height": 64},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8400,
            "durationMs": 1400,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Lower left inward heat arrow (base)
    {
        "id": "ht-07-left-arrow-base",
        "label": "Mũi tên truyền nhiệt dưới bên trái: INWARD HEAT ARROW (BASE)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 550, "y": 634, "width": 175, "height": 36},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8400,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Solid Ice Cube body
    {
        "id": "ht-08-ice-cube-body",
        "label": "Khối băng đặc trung tâm: SOLID ICE CUBE",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 765, "y": 350, "width": 397, "height": 284},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 10200,
            "durationMs": 3000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Forming puddle at bottom
    {
        "id": "ht-09-forming-puddle",
        "label": "Vũng nước bắt đầu tan: FORMING PUDDLE",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 725, "y": 634, "width": 445, "height": 126},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13400,
            "durationMs": 2200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Bottom label: ICE TAKES IN HEAT
    {
        "id": "ht-10-label-takes-heat",
        "label": "Nhãn hấp thu nhiệt: ICE TAKES IN HEAT",
        "sequence": 10,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 650, "y": 800, "width": 620, "height": 80},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15800,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 11. Right side: heat arrow + MELTING BEGINS
    {
        "id": "ht-11-melting-begins",
        "label": "Mũi tên & hiện tượng bắt đầu tan: RIGHT HEAT ARROW & MELTING BEGINS",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1162, "y": 460, "width": 530, "height": 155},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17800,
            "durationMs": 2400,
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
    "sceneId": "test_case_segmentation_19_heat_transfers_ice",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "heat_transfers_ice.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: heat_transfers_ice-regions.png
regions_png = DIR / "heat_transfers_ice-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "heat_transfers_ice_animation.mp4"
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
for t in [2, 4, 6, 8, 10, 13, 15, 17, 19, 20]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
