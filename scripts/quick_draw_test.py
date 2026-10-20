#!/usr/bin/env python3
"""
scripts/quick_draw_test.py — Công cụ test nhanh bước vẽ Whiteboard Animation (không cần kịch bản / audio / SRT)

Cách dùng:
  1. Test ngay với bài giảng tiếng Anh mẫu:
     python3 scripts/quick_draw_test.py

  2. Test với ảnh bài giảng của bạn (nếu đã có file .annotation.json cùng tên):
     python3 scripts/quick_draw_test.py --image path/to/my_image.png

  3. Tùy chọn tốc độ & chất lượng:
     python3 scripts/quick_draw_test.py --preset fast       # 720p, 20fps, render 3-5s
     python3 scripts/quick_draw_test.py --preset full       # 1080p, 30fps
     python3 scripts/quick_draw_test.py --color-mode never  # Không tô màu bất kỳ đối tượng nào
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
SCRIPTS_DIR = ROOT / "scripts"


def run_cmd(cmd: list[str]) -> bool:
    print(f"\n▶ Đang chạy: {' '.join(cmd)}")
    ret = subprocess.run(cmd)
    return ret.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Test nhanh bước vẽ Whiteboard Animation (không cần kịch bản / TTS)")
    parser.add_argument("--image", "-i", type=str, default=None,
                        help="Đường dẫn file ảnh .png cần test. Mặc định dùng bài giảng tiếng Anh mẫu.")
    parser.add_argument("--annotation", "-a", type=str, default=None,
                        help="Đường dẫn file .annotation.json tương ứng. Mặc định tự tìm file cùng tên với ảnh.")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Đường dẫn video mp4 đầu ra.")
    parser.add_argument("--preset", choices=["fast", "full"], default="fast",
                        help="fast: 720p 20fps (render siêu nhanh xem thử ~4-6s); full: 1080p 30fps.")
    parser.add_argument("--color-mode", choices=["auto", "always", "never"], default="auto",
                        help="auto: chỉ tô màu hình ảnh, text/gạch chân chỉ đi nét; never: bỏ hoàn toàn tô màu.")
    parser.add_argument("--open", action="store_true", default=True,
                        help="Tự động mở video sau khi render (trên macOS/Windows).")
    parser.add_argument("--no-open", dest="open", action="store_false")

    args = parser.parse_args()

    # Mặc định sử dụng bài giảng tiếng Anh mẫu
    if args.image is None:
        img_path = EXAMPLES_DIR / "test_english_lesson.png"
        ann_path = EXAMPLES_DIR / "test_english_lesson.annotation.json"
        if not img_path.exists() or not ann_path.exists():
            print("Chưa có bài giảng mẫu, đang tự động tạo...")
            gen_script = SCRIPTS_DIR / "generate_english_test_scene.py"
            subprocess.run([sys.executable, str(gen_script)], check=True)
    else:
        img_path = Path(args.image).resolve()
        if not img_path.exists():
            print(f"[Lỗi] Không tìm thấy ảnh: {img_path}")
            return 1
        if args.annotation:
            ann_path = Path(args.annotation).resolve()
        else:
            ann_path = img_path.with_name(img_path.stem + ".annotation.json")
        if not ann_path.exists():
            print(f"[Lỗi] Không tìm thấy file annotation: {ann_path}")
            print(f"Gợi ý: Mở assets/preview.html trên trình duyệt để kéo thả phân vùng và lưu file.")
            return 1

    out_video = Path(args.output).resolve() if args.output else img_path.with_name(img_path.stem + "-whiteboard.mp4")
    regions_preview = img_path.with_name(img_path.stem + "-regions.png")

    py_bin = sys.executable

    print("\n" + "=" * 60)
    print("🚀 BẮT ĐẦU TEST ENGINE VẼ BẢNG TRẮNG WHITEBOARD")
    print("=" * 60)
    print(f"• Ảnh đầu vào      : {img_path}")
    print(f"• File annotation  : {ann_path}")
    print(f"• Video kết quả    : {out_video}")
    print(f"• Cấu hình preset  : {args.preset} (Chế độ màu: {args.color_mode})")

    # Bước 1: Render ảnh preview các vùng
    print("\n[Bước 1/2] Xuất ảnh kiểm tra các vùng vẽ (Regions Preview)...")
    cmd_preview = [
        py_bin,
        str(SCRIPTS_DIR / "render_annotation_preview.py"),
        str(img_path),
        str(ann_path),
        str(regions_preview)
    ]
    if run_cmd(cmd_preview):
        print(f"  → Ảnh kiểm tra vùng: {regions_preview}")

    # Bước 2: Render video Whiteboard
    print("\n[Bước 2/2] Render video Whiteboard Animation...")
    cap_size = "720" if args.preset == "fast" else "1080"
    fps = "20" if args.preset == "fast" else "30"

    cmd_render = [
        py_bin,
        str(SCRIPTS_DIR / "render_stream_whiteboard.py"),
        str(img_path),
        str(ann_path),
        str(out_video),
        "--cap-long-edge", cap_size,
        "--fps", fps,
        "--color-mode", args.color_mode,
        "--ink-path", "skeleton"
    ]
    if not run_cmd(cmd_render):
        print("\n[Lỗi] Render video thất bại.")
        return 1

    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH TEST VẼ BẢNG TRẮNG!")
    print(f"📁 Video kết quả : {out_video}")
    print(f"🖼️ Ảnh kiểm tra vùng : {regions_preview}")
    print("=" * 60)

    if args.open:
        if sys.platform == "darwin":
            subprocess.run(["open", str(out_video)])
        elif sys.platform == "win32":
            os.startfile(str(out_video))

    return 0


if __name__ == "__main__":
    sys.exit(main())
