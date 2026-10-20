#!/usr/bin/env python3
"""
Render tuần tự 4 cảnh video bảng trắng "Sức Mạnh Lãi Kép" (Compound Interest)
Sử dụng engine render_stream_whiteboard.py với đầy đủ:
- Full HD 1920x1080
- Skeleton tracking cho chữ viết tay tự nhiên
- Vector gesture cho box viền không màu (tránh lộ chữ sớm)
- 60 fps mượt mà
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
REPO_DIR = PROJECT_DIR.parents[2]
RENDERER = REPO_DIR / "scripts" / "render_stream_whiteboard.py"
HAND_PNG = REPO_DIR / "assets" / "drawing-hand.png"
PYTHON = sys.executable

SCENES = [
    ("scene-01-snowball.png", "scene-01-snowball.annotation.json", "scene-01-snowball.mp4"),
    ("scene-02-chart.png", "scene-02-chart.annotation.json", "scene-02-chart.mp4"),
    ("scene-03-mindmap.png", "scene-03-mindmap.annotation.json", "scene-03-mindmap.mp4"),
    ("scene-04-comparison.png", "scene-04-comparison.annotation.json", "scene-04-comparison.mp4"),
]


def main():
    print("=" * 65)
    print("Bắt đầu render 4 cảnh video Whiteboard FullHD (1920x1080, 60fps)...")
    print("=" * 65)
    total_start = time.time()

    force = "--force" in sys.argv
    for idx, (img_name, ann_name, mp4_name) in enumerate(SCENES, 1):
        img_path = PROJECT_DIR / img_name
        ann_path = PROJECT_DIR / ann_name
        mp4_path = PROJECT_DIR / mp4_name

        if not force and mp4_path.exists() and mp4_path.stat().st_size > 100_000:
            print(f"[{idx}/4] Bỏ qua vì đã render xong: {mp4_name} ({mp4_path.stat().st_size / 1024 / 1024:.2f} MB)")
            continue

        print(f"\n>>> [{idx}/4] Đang render: {mp4_name} ...")
        t0 = time.time()
        cmd = [
            PYTHON,
            str(RENDERER),
            str(img_path),
            str(ann_path),
            str(mp4_path),
            str(HAND_PNG),
            "--ink-path", "skeleton",
            "--color-mode", "auto",
            "--cap-long-edge", "1920"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - t0
        if res.returncode == 0:
            size_mb = mp4_path.stat().st_size / (1024 * 1024)
            print(f"    ✓ Hoàn thành {mp4_name} ({size_mb:.2f} MB) trong {elapsed:.1f}s")
        else:
            print(f"    ✗ Lỗi khi render {mp4_name}:\n{res.stderr}")
            sys.exit(1)

    total_time = time.time() - total_start
    print("\n" + "=" * 65)
    print(f"🎉 Hoàn thành render toàn bộ 4 cảnh trong {total_time:.1f} giây ({total_time / 60:.1f} phút)!")
    print("=" * 65)


if __name__ == "__main__":
    main()
