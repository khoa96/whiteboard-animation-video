#!/usr/bin/env python3
"""
scripts/batch_generate_voiceover.py
Tự động sinh audio Voice-Over + Subtitles SRT + Timing Cues JSON
cho toàn bộ các phân cảnh trong một project sử dụng tts-voiceover-engine.
"""

import sys
import os
import subprocess
from pathlib import Path
import argparse

REPO_ROOT = Path(__file__).resolve().parent.parent

def generate_voiceover_for_scene(scene_dir: Path):
    script_file = scene_dir / "script.txt"
    if not script_file.exists():
        print(f"⚠️ Bỏ qua {scene_dir.name}: không tìm thấy script.txt")
        return False

    wav_file = scene_dir / "narration.wav"
    srt_file = scene_dir / "input.srt"
    cues_file = scene_dir / "timing_cues.json"

    print(f"\n▶ ĐANG TẠO VOICEOVER CHO: {scene_dir.name}...")
    cmd = [
        "npm", "--prefix", str(REPO_ROOT / "tts-voiceover-engine"), "run", "generate", "--",
        "--input", str(script_file.resolve()),
        "--output", str(wav_file.resolve()),
        "--srt", str(srt_file.resolve()),
        "--cues", str(cues_file.resolve()),
        "--single-request"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Lỗi sinh voiceover cho {scene_dir.name}: {res.stderr[-400:]}")
        return False
    
    print(f"✓ Hoàn tất {scene_dir.name} -> {wav_file.name}, {srt_file.name}, {cues_file.name}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Tự động sinh Voice-Over cho tất cả scenes trong project.")
    parser.add_argument("project_dir", type=Path, help="Đường dẫn đến thư mục dự án (ví dụ: projects/project_articles_a_an)")
    parser.add_argument("--scenes", nargs="*", help="Danh sách scene cụ thể cần chạy (ví dụ: scene_01 scene_02)")
    args = parser.parse_args()

    proj_dir = args.project_dir.resolve()
    scenes_dir = proj_dir / "scenes"
    if not scenes_dir.exists():
        print(f"❌ Không tìm thấy thư mục scenes tại: {scenes_dir}")
        sys.exit(1)

    scene_dirs = sorted([d for d in scenes_dir.iterdir() if d.is_dir() and d.name.startswith("scene_")])
    if args.scenes:
        target_names = set(args.scenes)
        scene_dirs = [d for d in scene_dirs if d.name in target_names]

    print("=" * 65)
    print(f"🎙️ BẮT ĐẦU CHẠY BATCH VOICEOVER CHO {len(scene_dirs)} PHÂN CẢNH")
    print(f"📁 Dự án: {proj_dir.name}")
    print("=" * 65)

    success_count = 0
    for s_dir in scene_dirs:
        ok = generate_voiceover_for_scene(s_dir)
        if ok:
            success_count += 1

    print("\n" + "=" * 65)
    print(f"🎉 TỔNG KẾT: Đã hoàn tất {success_count}/{len(scene_dirs)} phân cảnh!")
    print("=" * 65)

if __name__ == "__main__":
    main()

