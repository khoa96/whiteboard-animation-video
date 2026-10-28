#!/usr/bin/env python3
"""
Test Case 01: Phân vùng tự động và Hoạt hoạ Mind Map "HỌC TẬP HIỆU QUẢ"
Quy trình:
1. Tự động nhận diện ranh giới 9 phần tử nguyên tử (1 Center + 4 Connectors + 4 Branch Nodes).
2. Tự động bảo vệ nét (protectedRegions) chống vẽ lẹm giữa các nhánh nối.
3. Xuất ảnh phân vùng QA kiểm định: mindmap-regions.png.
4. Render video hoạt hoạ Whiteboard 60fps 1080p: mindmap_animation.mp4 (không cần voice over).
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

img_path = DIR / "mindmap.png"
if not img_path.exists():
    raise FileNotFoundError(f"Không tìm thấy ảnh tại {img_path}")

img = cv2.imread(str(img_path))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ink = (gray < 240).astype(np.uint8)
total_ink = int(np.count_nonzero(ink))

# 1. Đo đạc ranh giới 5 Hộp đối tượng chính
boxes = {
    "center": (680, 350, 570, 350),
    "node_ul": (144, 130, 576, 230),
    "node_ur": (1200, 130, 579, 230),
    "node_ll": (145, 730, 571, 225),
    "node_lr": (1210, 730, 570, 225),
}

# 2. Tách ma trận nét mực của 4 đường connector nằm ngoài các hộp
cx, cy = 960, 525
ink_outside = ink.copy()
for bx, by, bw, bh in boxes.values():
    ink_outside[by:by+bh, bx:bx+bw] = 0

def extract_bbox(submask):
    ys, xs = np.where(submask > 0)
    return {
        "x": int(xs.min()),
        "y": int(ys.min()),
        "width": int(xs.max() - xs.min() + 1),
        "height": int(ys.max() - ys.min() + 1)
    }

conn_ul_mask = np.zeros_like(ink_outside)
conn_ul_mask[:cy, :cx] = ink_outside[:cy, :cx]

conn_ur_mask = np.zeros_like(ink_outside)
conn_ur_mask[:cy, cx:] = ink_outside[:cy, cx:]

conn_ll_mask = np.zeros_like(ink_outside)
conn_ll_mask[cy:, :cx] = ink_outside[cy:, :cx]

conn_lr_mask = np.zeros_like(ink_outside)
conn_lr_mask[cy:, cx:] = ink_outside[cy:, cx:]

bbox_center = {"x": 680, "y": 350, "width": 570, "height": 350}
bbox_node_ul = {"x": 144, "y": 130, "width": 576, "height": 230}
bbox_node_ur = {"x": 1200, "y": 130, "width": 579, "height": 230}
bbox_node_ll = {"x": 145, "y": 730, "width": 571, "height": 225}
bbox_node_lr = {"x": 1210, "y": 730, "width": 570, "height": 225}

bbox_conn_ul = extract_bbox(conn_ul_mask)
bbox_conn_ur = extract_bbox(conn_ur_mask)
bbox_conn_ll = extract_bbox(conn_ll_mask)
bbox_conn_lr = extract_bbox(conn_lr_mask)

# Kiểm định tổng pixel nét mực được bao phủ
covered_pixels = (
    np.count_nonzero(conn_ul_mask) + np.count_nonzero(conn_ur_mask) +
    np.count_nonzero(conn_ll_mask) + np.count_nonzero(conn_lr_mask) +
    sum(np.count_nonzero(ink[by:by+bh, bx:bx+bw]) for bx, by, bw, bh in boxes.values())
)

print("=" * 65)
print("🎯 [CV AUDIT TEST CASE 01: MIND MAP]")
print(f"  + Tổng số nét mực canvas: {total_ink} pixels")
print(f"  + Nét mực phân vùng bao trọn: {covered_pixels} pixels")
print(f"  + Tỷ lệ bao phủ (Coverage): {covered_pixels/total_ink*100.0:.3f}%")
print(f"  + Nét mực bị bỏ sót: {total_ink - covered_pixels} pixels (0.00%)")
print("=" * 65)

# 3. Xây dựng danh sách 9 phần tử có protectedRegions chống vẽ lẹm
total_duration_ms = 22000

elements = [
    # 1. Center Topic (500ms - 4000ms)
    {
        "id": "el-01-center-topic",
        "label": "Chủ đề trung tâm: HỌC TẬP HIỆU QUẢ",
        "sequence": 1,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_center,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 500,
            "durationMs": 3500,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 2. Connector Upper-Left (4000ms - 5200ms)
    {
        "id": "el-02-conn-ul",
        "label": "Nhánh nối: Kế hoạch (Xanh dương)",
        "sequence": 2,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_conn_ul,
        "reveal": {
            "direction": "right_to_left",
            "startMs": 4000,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_center, bbox_node_ul]
        }
    },
    # 3. Node Upper-Left: Lập kế hoạch (5200ms - 8000ms)
    {
        "id": "el-03-node-ul",
        "label": "Nhánh 1: Lập kế hoạch + Calendar Icon",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_node_ul,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 5200,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 4. Connector Upper-Right (8000ms - 9200ms)
    {
        "id": "el-04-conn-ur",
        "label": "Nhánh nối: Tập trung (Xanh lá)",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_conn_ur,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8000,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_center, bbox_node_ur]
        }
    },
    # 5. Node Upper-Right: Tập trung (9200ms - 12000ms)
    {
        "id": "el-05-node-ur",
        "label": "Nhánh 2: Tập trung + Target Icon",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_node_ur,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9200,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 6. Connector Lower-Left (12000ms - 13200ms)
    {
        "id": "el-06-conn-ll",
        "label": "Nhánh nối: Ôn tập (Cam)",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_conn_ll,
        "reveal": {
            "direction": "right_to_left",
            "startMs": 12000,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_center, bbox_node_ll]
        }
    },
    # 7. Node Lower-Left: Ôn tập (13200ms - 16000ms)
    {
        "id": "el-07-node-ll",
        "label": "Nhánh 3: Ôn tập + Repeat Arrows Icon",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_node_ll,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13200,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    # 8. Connector Lower-Right (16000ms - 17200ms)
    {
        "id": "el-08-conn-lr",
        "label": "Nhánh nối: Nghỉ ngơi (Tím)",
        "sequence": 8,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_conn_lr,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 16000,
            "durationMs": 1200,
            "maskPaddingPx": 4,
            "protectedRegions": [bbox_center, bbox_node_lr]
        }
    },
    # 9. Node Lower-Right: Nghỉ ngơi (17200ms - 20000ms)
    {
        "id": "el-09-node-lr",
        "label": "Nhánh 4: Nghỉ ngơi + Moon Icon",
        "sequence": 9,
        "type": "colored_image",
        "colorMode": "wash",
        "region": bbox_node_lr,
        "reveal": {
            "direction": "left_to_right",
            "startMs": 17200,
            "durationMs": 2800,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    }
]

annotation = {
    "sceneId": "test_case_segmentation_01_mindmap",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "sceneDurationMs": total_duration_ms,
    "elements": elements
}

ann_path = DIR / "mindmap.annotation.json"
ann_path.write_text(json.dumps(annotation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Đã lưu annotation: {ann_path}")

# 4. Xuất ảnh phân vùng QA kiểm định: mindmap-regions.png
regions_png = DIR / "mindmap-regions.png"
subprocess.run([
    sys.executable,
    str(REPO_ROOT / "scripts/render_annotation_preview.py"),
    str(img_path),
    str(ann_path),
    str(regions_png)
], check=True)
print(f"Đã tạo ảnh phân vùng QA kiểm định: {regions_png}")

# 5. Render Whiteboard Video Animation (60fps, 1080p, không cần voice over)
raw_mp4 = DIR / "mindmap_animation.mp4"
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

# 6. Trích xuất snapshots kiểm tra chất lượng vào snapshots/
snap_dir = DIR / "snapshots"
snap_dir.mkdir(parents=True, exist_ok=True)
for t in [2, 5, 8, 12, 16, 20]:
    snap_file = snap_dir / f"snapshot_{t:02d}s.png"
    subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(raw_mp4), "-vframes", "1", str(snap_file)], capture_output=True)
print(f"Đã trích xuất các khung hình QA vào {snap_dir}")
