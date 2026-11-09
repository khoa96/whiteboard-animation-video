#!/usr/bin/env python3
"""
stitch_full_course.py — Tự động ghép nối toàn bộ các Scene video thành bài giảng hoàn chỉnh
kèm audio thuyết minh Master (narration.wav) và phụ đề SRT.

Cách dùng:
    python scripts/stitch_full_course.py projects/WB-ENG-A1-003
    python scripts/stitch_full_course.py projects/WB-ENG-A1-003 --output final_video.mp4
"""

import sys
import re
import subprocess
import argparse
from pathlib import Path


def stitch_course(project_dir: Path, output_name: str = "final_master_course.mp4") -> Path:
    scenes_dir = project_dir / "scenes"
    audio_master = project_dir / "narration.wav"
    srt_master = project_dir / "input.srt"

    if not scenes_dir.exists():
        print(f"Lỗi: Không tìm thấy thư mục scenes trong {project_dir}")
        sys.exit(1)

    # Tìm các scene video MP4 (hỗ trợ cả cấu trúc phẳng lẫn thư mục con scenes/scene_XX/scene_XX.mp4)
    raw_scenes = sorted(list(scenes_dir.glob("scene_*.mp4")) + list(scenes_dir.glob("scene_*/scene_*.mp4")))
    pure_scenes = []
    for s in raw_scenes:
        if "_with_audio" not in s.name and "final_" not in s.name:
            m = re.search(r"scene_(\d+)\.mp4", s.name)
            if m:
                pure_scenes.append((int(m.group(1)), s))

    pure_scenes.sort(key=lambda x: x[0])
    if not pure_scenes:
        print(f"Lỗi: Không tìm thấy video scene_XX.mp4 nào trong {scenes_dir}")
        sys.exit(1)

    print("=" * 65)
    print(" BẮT ĐẦU GHÉP NỐI TOÀN BỘ BÀI GIẢNG (COURSE STITCHER)")
    print("=" * 65)
    print(f"  • Thư mục dự án    : {project_dir}")
    print(f"  • Số lượng Scene   : {len(pure_scenes)} scenes")
    for idx, path in pure_scenes:
        print(f"    - Scene {idx:02d}: {path.name}")
    print("-" * 65)

    # 1. Tạo file concat list cho ffmpeg
    concat_list_file = scenes_dir / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for idx, path in pure_scenes:
            f.write(f"file '{path.resolve()}'\n")

    temp_video = scenes_dir / "temp_stitched_video.mp4"
    final_output = project_dir / output_name

    # 2. Concat video lossless
    print("  • Đang ghép nối chuỗi video không nén lại...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(temp_video)
    ]
    p_concat = subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p_concat.returncode != 0:
        print(f"Lỗi khi ghép video: {p_concat.stderr.decode('utf-8', errors='ignore')}")
        sys.exit(1)

    # 3. Mux Full Audio Master
    if audio_master.exists():
        print(f"  • Đang đồng bộ Audio Master thuyết minh ({audio_master.name})...")
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(temp_video),
            "-i", str(audio_master),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(final_output)
        ]
        p_final = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p_final.returncode != 0:
            print(f"Lỗi khi mux audio: {p_final.stderr.decode('utf-8', errors='ignore')}")
            sys.exit(1)
        if temp_video.exists():
            temp_video.unlink()
    else:
        temp_video.rename(final_output)

    if concat_list_file.exists():
        concat_list_file.unlink()

    file_size_mb = final_output.stat().st_size / (1024 * 1024)
    print("=" * 65)
    print(f"🎉 XUẤT BẢN THÀNH CÔNG BÀI GIẢNG HOÀN CHỈNH: {final_output.name} ({file_size_mb:.2f} MB)")
    print(f"  • Đường dẫn: {final_output}")
    print("=" * 65)
    return final_output


def main():
    parser = argparse.ArgumentParser(description="Tự động ghép các Scene thành video bài giảng hoàn chỉnh")
    parser.add_argument("project_dir", type=Path, help="Thư mục dự án (e.g. projects/WB-ENG-A1-003)")
    parser.add_argument("--output", type=str, default="final_master_course.mp4", help="Tên file video thành phẩm")
    args = parser.parse_args()

    stitch_course(args.project_dir, args.output)


if __name__ == "__main__":
    main()
