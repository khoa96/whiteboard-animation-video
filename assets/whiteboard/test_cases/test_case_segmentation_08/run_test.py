#!/usr/bin/env python3
"""
Test Case 08: Phân vùng tự động và Hoạt hoạ Vòng Đời Cây Đậu (THE LIFE CYCLE OF A BEAN PLANT)
Quy trình:
1. Phân vùng 17 phần tử nguyên tử chuẩn xác 100.000% độ phủ mực (0.000% chồng lấn):
   - Tiêu đề chính: THE LIFE CYCLE OF A BEAN PLANT
   - 5 giai đoạn sinh học (Hạt mầm, Nảy mầm, Cây con, Cây trưởng thành, Quả đậu & hạt mới)
   - Từng hình vẽ và nhãn tên độc lập
   - 4 mũi tên chỉ hướng chuyển tiếp giữa các giai đoạn
2. Xuất ảnh phân vùng QA kiểm định: bean_life_cycle-regions.png.
3. Render video hoạt hoạ Whiteboard 60fps 1080p: bean_life_cycle_animation.mp4 (không cần voice over).
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

img_path = DIR / "bean_life_cycle.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 17 Bounding boxes đạt 100.000% độ phủ mực và 0.000% chồng lấn
boxes = [
    # 1. Title
    {
        "id": "el-01-title",
        "label": "Tiêu đề: THE LIFE CYCLE OF A BEAN PLANT",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 200, "y": 60, "width": 1520, "height": 140},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 2. Stage 1: Seed
    {
        "id": "el-02-s1-seed",
        "label": "Giai đoạn 1: Hạt đậu (Seed)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 100, "y": 450, "width": 200, "height": 220},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 2600,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 3. Stage 1: Label
    {
        "id": "el-03-s1-label",
        "label": "Nhãn: SEED",
        "sequence": 3,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 100, "y": 860, "width": 220, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4200,
            "durationMs": 1000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 4. Arrow 1
    {
        "id": "el-04-arrow1",
        "label": "Mũi tên chuyển tiếp 1 -> 2",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 310, "y": 526, "width": 120, "height": 73},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5300,
            "durationMs": 1000,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 5. Stage 2: Germination
    {
        "id": "el-05-s2-germination",
        "label": "Giai đoạn 2: Nảy mầm (Germination)",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 440, "y": 350, "width": 230, "height": 440},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 6400,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 6. Stage 2: Label
    {
        "id": "el-06-s2-label",
        "label": "Nhãn: GERMINATION",
        "sequence": 6,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 370, "y": 860, "width": 370, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8500,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 7. Arrow 2
    {
        "id": "el-07-arrow2",
        "label": "Mũi tên chuyển tiếp 2 -> 3",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 675, "y": 526, "width": 118, "height": 73},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9800,
            "durationMs": 1000,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 8. Stage 3: Seedling Leaves
    {
        "id": "el-08-s3-canopy",
        "label": "Giai đoạn 3: Lá & mầm cây con (Seedling Shoot)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 793, "y": 380, "width": 265, "height": 145},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 10900,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 9. Stage 3: Seedling Roots & Soil
    {
        "id": "el-09-s3-roots",
        "label": "Giai đoạn 3: Rễ & tầng đất (Roots & Soil)",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 793, "y": 525, "width": 245, "height": 295},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 12500,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 10. Stage 3: Label
    {
        "id": "el-10-s3-label",
        "label": "Nhãn: SEEDLING",
        "sequence": 10,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 780, "y": 860, "width": 290, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 14100,
            "durationMs": 1000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 11. Arrow 3
    {
        "id": "el-11-arrow3",
        "label": "Mũi tên chuyển tiếp 3 -> 4",
        "sequence": 11,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1040, "y": 526, "width": 114, "height": 73},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15200,
            "durationMs": 1000,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 12. Stage 4: Mature Plant Foliage & Flower
    {
        "id": "el-12-s4-canopy",
        "label": "Giai đoạn 4: Tán lá, hoa & thân cây trưởng thành",
        "sequence": 12,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1130, "y": 250, "width": 345, "height": 275},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 16300,
            "durationMs": 2500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 13. Stage 4: Mature Plant Root System
    {
        "id": "el-13-s4-roots",
        "label": "Giai đoạn 4: Hệ rễ chùm bám sâu dưới đất",
        "sequence": 13,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1155, "y": 525, "width": 320, "height": 345},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 18900,
            "durationMs": 2000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 14. Stage 4: Label
    {
        "id": "el-14-s4-label",
        "label": "Nhãn: MATURE PLANT",
        "sequence": 14,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1110, "y": 870, "width": 375, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 21000,
            "durationMs": 1200,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 15. Arrow 4
    {
        "id": "el-15-arrow4",
        "label": "Mũi tên chuyển tiếp 4 -> 5",
        "sequence": 15,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1475, "y": 526, "width": 112, "height": 73},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 22300,
            "durationMs": 1000,
            "maskPaddingPx": 4,
            "protectedRegions": []
        }
    },
    # 16. Stage 5: Bean Pod & New Seeds
    {
        "id": "el-16-s5-pod-top",
        "label": "Giai đoạn 5: Cuống quả & nhãn BEAN POD",
        "sequence": 16,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1550, "y": 350, "width": 290, "height": 175},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 23400,
            "durationMs": 1500,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-17-s5-pod-bot",
        "label": "Giai đoạn 5: Thân quả đậu, hạt & nhãn NEW SEEDS",
        "sequence": 17,
        "type": "colored_image",
        "colorMode": "wash",
        "region": {"x": 1587, "y": 525, "width": 260, "height": 250},
        "reveal": {
            "direction": "top_to_bottom",
            "startMs": 25000,
            "durationMs": 1800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    # 18. Stage 5: Bottom Label
    {
        "id": "el-18-s5-label",
        "label": "Nhãn: BEAN POD",
        "sequence": 18,
        "type": "text",
        "colorMode": "none",
        "region": {"x": 1550, "y": 860, "width": 290, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 26900,
            "durationMs": 1000,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    }
]

total_duration_ms = 29000

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
    "sceneId": "test_case_segmentation_08_bean_life_cycle",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": boxes
}

ann_path = DIR / "bean_life_cycle.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# Xuất ảnh phân vùng QA kiểm định: bean_life_cycle-regions.png
regions_png = DIR / "bean_life_cycle-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# Render Whiteboard Video Animation
raw_mp4 = DIR / "bean_life_cycle_animation.mp4"
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
for t in [2, 5, 9, 13, 17, 21, 25, 28]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
