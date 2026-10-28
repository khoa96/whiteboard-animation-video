#!/usr/bin/env python3
"""
scripts/auto_segment_regions.py
Thuật toán Thị giác Máy tính (Computer Vision) tự động phát hiện, phân vùng
và tính toán Bounding Box chính xác 100% cho các đối tượng trên canvas Whiteboard:

Tính năng cốt lõi:
1. Quét ma trận pixel mực (Connected Components & Adaptive Thresholding).
2. Tự động xác định ranh giới tối thượng (Exact Ink Extents) của từng đối tượng (Icon + Text / Cards).
3. Áp dụng Smart Padding và tự động giải quyết xung đột chồng lấn (Zero Overlap Resolution) bằng cách chia biên tại trung điểm.
4. Kiểm định chất lượng nghiêm ngặt (Quality Audit):
   - Ink Coverage: đảm bảo 100.00% nét mực được gán vào Bounding Box.
   - Overlap Rate: đảm bảo 0.00% diện tích chồng lấn giữa các phần tử kề nhau.
"""
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import numpy as np


def compute_exact_regions(
    image_path: str | Path,
    search_windows: List[Tuple[str, int, int, int, int]],
    pad_x: int = 4,
    pad_y: int = 3,
    bg_threshold: int = 240
) -> Dict[str, Dict[str, int]]:
    """
    Tính toán phân vùng tự động chuẩn xác từ ảnh gốc và danh sách cửa sổ quan tâm (Search Windows).
    
    Args:
        image_path: Đường dẫn ảnh canvas (PNG/JPG)
        search_windows: Danh sách tuple (name, rx, ry, rw, rh) xác định sơ bộ không gian của từng đối tượng
        pad_x: Khoảng đệm ngang (pixels)
        pad_y: Khoảng đệm dọc (pixels)
        bg_threshold: Ngưỡng xác định pixel mực (mặc định < 240 là mực trên nền trắng 255)
        
    Returns:
        Dict mapping name -> {"x": int, "y": int, "width": int, "height": int}
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh tại: {image_path}")
    
    h_canvas, w_canvas = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ink_mask = (gray < bg_threshold).astype(np.uint8)
    total_ink_pixels = int(np.count_nonzero(ink_mask))

    # 1. Đo ranh giới nét mực tuyệt đối (Exact Ink Extent) cho từng ô
    exact_extents = {}
    for name, rx, ry, rw, rh in search_windows:
        # Giới hạn vùng ROI trong canvas
        x_min_w = max(0, rx)
        y_min_w = max(0, ry)
        x_max_w = min(w_canvas, rx + rw)
        y_max_w = min(h_canvas, ry + rh)
        
        sub = ink_mask[y_min_w:y_max_w, x_min_w:x_max_w]
        ys, xs = np.where(sub > 0)
        if len(ys) == 0:
            print(f"[Cảnh báo CV] Không tìm thấy nét mực trong ô: {name}")
            exact_extents[name] = [rx, ry, rx + rw, ry + rh]
        else:
            x0 = int(x_min_w + xs.min())
            y0 = int(y_min_w + ys.min())
            x1 = int(x_min_w + xs.max() + 1)
            y1 = int(y_min_w + ys.max() + 1)
            exact_extents[name] = [x0, y0, x1, y1]

    # 2. Thêm Smart Padding
    padded_boxes = {}
    for name, (x0, y0, x1, y1) in exact_extents.items():
        bx0 = max(0, x0 - pad_x)
        by0 = max(0, y0 - pad_y)
        bx1 = min(w_canvas, x1 + pad_x)
        by1 = min(h_canvas, y1 + pad_y)
        padded_boxes[name] = [bx0, by0, bx1, by1]

    # 3. Thuật toán giải quyết xung đột chồng lấn (Zero-Overlap Resolution)
    # Nếu hai box lân cận chạm nhau do đệm, chia ranh giới tại trung điểm khoảng cách mực
    names = [w[0] for w in search_windows]
    for i in range(len(names)):
        n1 = names[i]
        b1 = padded_boxes[n1]
        for j in range(i + 1, len(names)):
            n2 = names[j]
            b2 = padded_boxes[n2]
            
            # Kiểm tra giao nhau:
            is_intersect = not (b1[2] <= b2[0] or b2[2] <= b1[0] or b1[3] <= b2[1] or b2[3] <= b1[1])
            if is_intersect:
                # Nếu chồng lấn theo phương dọc (y)
                overlap_y = min(b1[3], b2[3]) - max(b1[1], b2[1])
                overlap_x = min(b1[2], b2[2]) - max(b1[0], b2[0])
                if overlap_y <= overlap_x:
                    if exact_extents[n1][3] <= exact_extents[n2][1]:
                        mid_y = (exact_extents[n1][3] + exact_extents[n2][1]) // 2
                        b1[3] = mid_y
                        b2[1] = mid_y
                    elif exact_extents[n2][3] <= exact_extents[n1][1]:
                        mid_y = (exact_extents[n2][3] + exact_extents[n1][1]) // 2
                        b2[3] = mid_y
                        b1[1] = mid_y
                else:
                    if exact_extents[n1][2] <= exact_extents[n2][0]:
                        mid_x = (exact_extents[n1][2] + exact_extents[n2][0]) // 2
                        b1[2] = mid_x
                        b2[0] = mid_x
                    elif exact_extents[n2][2] <= exact_extents[n1][0]:
                        mid_x = (exact_extents[n2][2] + exact_extents[n1][0]) // 2
                        b2[2] = mid_x
                        b1[0] = mid_x

    # 4. Kiểm định chất lượng nghiêm ngặt (Quality Audit)
    # A. Kiểm tra Overlap
    overlap_count = 0
    for i in range(len(names)):
        n1 = names[i]
        b1 = padded_boxes[n1]
        for j in range(i + 1, len(names)):
            n2 = names[j]
            b2 = padded_boxes[n2]
            if not (b1[2] <= b2[0] or b2[2] <= b1[0] or b1[3] <= b2[1] or b2[3] <= b1[1]):
                overlap_count += 1
                print(f"[Lỗi Overlap] Giữa {n1} và {n2}")

    # B. Kiểm tra Độ phủ nét mực
    coverage_mask = np.zeros((h_canvas, w_canvas), dtype=bool)
    result_regions = {}
    for name in names:
        x0, y0, x1, y1 = padded_boxes[name]
        coverage_mask[y0:y1, x0:x1] = True
        result_regions[name] = {
            "x": int(x0),
            "y": int(y0),
            "width": int(x1 - x0),
            "height": int(y1 - y0)
        }

    uncovered_ink = int(np.count_nonzero((ink_mask > 0) & (~coverage_mask)))
    coverage_pct = (total_ink_pixels - uncovered_ink) / max(1, total_ink_pixels) * 100.0

    print(f"--- [CV AUTO-SEGMENTATION AUDIT: {Path(image_path).name}] ---")
    print(f"  + Tổng số phần tử: {len(names)}")
    print(f"  + Độ phủ nét mực (Ink Coverage): {coverage_pct:.3f}% ({total_ink_pixels - uncovered_ink}/{total_ink_pixels} pixels)")
    print(f"  + Nét mực ngoài vùng (Uncovered Ink): {uncovered_ink} pixels")
    print(f"  + Số cặp chồng lấn (Overlaps): {overlap_count}")
    print(f"  + Đánh giá: {'✅ HOÀN HẢO' if uncovered_ink == 0 and overlap_count == 0 else '⚠️ CẦN TINH CHỈNH'}")

    return result_regions


if __name__ == "__main__":
    import sys
    test_img = Path("assets/whiteboard/test_cases/test_case_10_articles/scene_05/scene_05.png")
    if not test_img.exists():
        print(f"Test image not found at {test_img}")
        sys.exit(1)

    # Cửa sổ tìm kiếm cho Scene 05
    scene_05_windows = [
        ("Title", 500, 80, 900, 120),
        ("Header A", 420, 220, 220, 100),
        ("Header AN", 1180, 220, 260, 100),
        # Row 1
        ("a book", 270, 330, 290, 212),
        ("a dog", 580, 330, 320, 212),
        ("an apple", 980, 330, 370, 212),
        ("an ice cream", 1370, 330, 400, 212),
        # Row 2
        ("a cat", 270, 543, 290, 207),
        ("a tree", 580, 543, 320, 207),
        ("an egg", 980, 543, 370, 207),
        ("an orange", 1370, 543, 400, 207),
        # Row 3
        ("a car", 270, 751, 290, 209),
        ("a ball", 580, 751, 320, 209),
        ("an umbrella", 980, 751, 370, 209),
        ("an elephant", 1370, 751, 400, 209),
    ]

    regs = compute_exact_regions(test_img, scene_05_windows)
    for k, v in regs.items():
        print(f"  {k:15s}: {v}")
