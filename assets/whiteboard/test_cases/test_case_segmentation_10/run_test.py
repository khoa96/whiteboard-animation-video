#!/usr/bin/env python3
"""
Test Case 10: Phân vùng tự động và Hoạt hoạ Từ vựng Tiếng Anh Sân Bay (AT THE AIRPORT)
Quy trình:
1. Phân vùng 11 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề chính: AT THE AIRPORT
   - Hàng 1 (5 mục): PASSPORT, BOARDING PASS, LUGGAGE TAG, SUITCASE, CARRY-ON
   - Hàng 2 (5 mục): CHECK-IN COUNTER, SECURITY CHECKPOINT, DEPARTURE BOARD, BOARDING GATE, BAGGAGE CAROUSEL
2. Xuất ảnh phân vùng QA kiểm định: airport_lesson-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: airport_lesson_animation.mp4 (không cần voice over).
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

img_path = DIR / "airport_lesson.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 11 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "el-01-title",
        "label": "Tiêu đề: AT THE AIRPORT",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 500, "y": 40, "width": 920, "height": 115},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Row 1 Col 1: PASSPORT
    {
        "id": "el-02-passport",
        "label": "Mục 1: PASSPORT (Hộ chiếu)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 160, "width": 330, "height": 395},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 2600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Row 1 Col 2: BOARDING PASS
    {
        "id": "el-03-boarding-pass",
        "label": "Mục 2: BOARDING PASS (Thẻ lên máy bay)",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 410, "y": 160, "width": 370, "height": 395},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 4700,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Row 1 Col 3: LUGGAGE TAG
    {
        "id": "el-04-luggage-tag",
        "label": "Mục 3: LUGGAGE TAG (Thẻ hành lý)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 780, "y": 160, "width": 365, "height": 395},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 6800,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 5. Row 1 Col 4: SUITCASE
    {
        "id": "el-05-suitcase",
        "label": "Mục 4: SUITCASE (Va li kéo)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1145, "y": 160, "width": 355, "height": 395},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 8900,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Row 1 Col 5: CARRY-ON
    {
        "id": "el-06-carry-on",
        "label": "Mục 5: CARRY-ON (Túi xách tay)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1500, "y": 160, "width": 370, "height": 395},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 11000,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Row 2 Col 1: CHECK-IN COUNTER
    {
        "id": "el-07-check-in-counter",
        "label": "Mục 6: CHECK-IN COUNTER (Quầy làm thủ tục)",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 80, "y": 555, "width": 330, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 13200,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 8. Row 2 Col 2: SECURITY CHECKPOINT
    {
        "id": "el-08-security-checkpoint",
        "label": "Mục 7: SECURITY CHECKPOINT (Cổng an ninh soi chiếu)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 410, "y": 555, "width": 370, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 15300,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Row 2 Col 3: DEPARTURE BOARD
    {
        "id": "el-09-departure-board",
        "label": "Mục 8: DEPARTURE BOARD (Bảng thông tin chuyến bay)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 780, "y": 555, "width": 365, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 17400,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Row 2 Col 4: BOARDING GATE
    {
        "id": "el-10-boarding-gate",
        "label": "Mục 9: BOARDING GATE (Cổng lên máy bay)",
        "sequence": 10,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1145, "y": 555, "width": 355, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 19500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 11. Row 2 Col 5: BAGGAGE CAROUSEL
    {
        "id": "el-11-baggage-carousel",
        "label": "Mục 10: BAGGAGE CAROUSEL (Băng chuyền hành lý)",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1500, "y": 555, "width": 370, "height": 470},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 21600,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 25000

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
    "sceneId": "test_case_segmentation_10_airport",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "airport_lesson.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: airport_lesson-regions.png
regions_png = DIR / "airport_lesson-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "airport_lesson_animation.mp4"
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
for t in [2, 5, 8, 12, 16, 20, 24]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
