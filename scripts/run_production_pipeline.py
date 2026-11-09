#!/usr/bin/env python3
"""
scripts/run_production_pipeline.py
Kịch bản sản xuất tự động toàn diện:
1. Render video vẽ tay 60fps cho từng Scene (chuẩn Stream Whiteboard Renderer).
2. Ghép Audio Master Clock (narration.wav) cho từng Scene.
3. Burn phụ đề động chuẩn dark_slate_obsidian cho từng Scene.
4. Ghép nối các phân cảnh thành video bài giảng hoàn chỉnh: output/articles_a_an_final.mp4.
"""
import os
import sys
import subprocess
import time
from pathlib import Path
import argparse

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import subtitle_styler

PROJ_DIR = REPO_ROOT / "projects/project_articles_a_an"
SCENES_DIR = PROJ_DIR / "scenes"
OUTPUT_DIR = PROJ_DIR / "output"
HAND_PATH = REPO_ROOT / "assets/drawing-hand.png"
PYTHON_BIN = REPO_ROOT / ".venv/bin/python"

ALL_SCENES = [f"scene_{i:02d}" for i in range(1, 10)]

def render_scene_video(scene_name: str, force: bool = False):
    scene_dir = SCENES_DIR / scene_name
    img_path = scene_dir / f"{scene_name}.png"
    ann_path = scene_dir / f"{scene_name}.annotation.json"
    raw_mp4 = scene_dir / f"{scene_name}.mp4"

    if not force and raw_mp4.exists() and raw_mp4.stat().st_size > 500000:
        print(f"  ⚡ [{scene_name}] Đã có video thô sẵn: {raw_mp4.name} ({raw_mp4.stat().st_size / 1024 / 1024:.2f} MB), bỏ qua render.")
        return True

    print(f"  🎬 [{scene_name}] Đang render nét vẽ tay 60 fps...")
    cmd = [
        str(PYTHON_BIN),
        str(REPO_ROOT / "scripts/render_stream_whiteboard.py"),
        str(img_path),
        str(ann_path),
        str(raw_mp4),
        str(HAND_PATH),
        "--canvas-hex", "#FFFFFF",
        "--fps", "60",
        "--cap-long-edge", "1920"
    ]
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  ❌ [{scene_name}] Render lỗi: {res.stderr[-400:]}")
        return False
    print(f"  ✓ [{scene_name}] Render hoàn tất trong {time.time()-t0:.1f}s -> {raw_mp4.name}")
    return True

def mux_scene_audio(scene_name: str):
    scene_dir = SCENES_DIR / scene_name
    raw_mp4 = scene_dir / f"{scene_name}.mp4"
    audio_path = scene_dir / "narration.wav"
    if not audio_path.exists():
        audio_path = scene_dir / "narration.m4a"
    voice_mp4 = scene_dir / f"{scene_name}_voice.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_mp4),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        str(voice_mp4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  ❌ [{scene_name}] Ghép audio lỗi: {res.stderr[-300:]}")
        return False
    print(f"  ✓ [{scene_name}] Đã ghép audio -> {voice_mp4.name}")
    return True

def burn_scene_subtitle(scene_name: str):
    scene_dir = SCENES_DIR / scene_name
    voice_mp4 = scene_dir / f"{scene_name}_voice.mp4"
    srt_path = scene_dir / "input.srt"
    sub_mp4 = scene_dir / f"{scene_name}_sub.mp4"

    ok = subtitle_styler.burn_subtitles_to_video(
        input_video=voice_mp4,
        srt_or_ass=srt_path,
        output_video=sub_mp4,
        project_dir=PROJ_DIR
    )
    if not ok:
        print(f"  ❌ [{scene_name}] Dập phụ đề lỗi!")
        return False
    print(f"  ✓ [{scene_name}] Đã dập phụ đề chuẩn dark_slate_obsidian -> {sub_mp4.name}")
    return True

def stitch_full_course(scenes_to_stitch):
    print("\n" + "=" * 65)
    print(f"🎞️ TIẾN HÀNH GHÉP NỐI {len(scenes_to_stitch)} PHÂN CẢNH THÀNH VIDEO HOÀN CHỈNH")
    print("=" * 65)

    sub_scenes = [SCENES_DIR / s / f"{s}_sub.mp4" for s in scenes_to_stitch]
    for s_path in sub_scenes:
        if not s_path.exists():
            print(f"❌ Không tìm thấy file phân cảnh: {s_path}")
            return False

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    concat_txt = OUTPUT_DIR / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s_path in sub_scenes:
            f.write(f"file '{s_path.resolve()}'\n")

    final_video = OUTPUT_DIR / "articles_a_an_final.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(final_video)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Ghép nối lỗi: {res.stderr[-300:]}")
        return False

    file_size_mb = final_video.stat().st_size / (1024 * 1024)
    print(f"🎉 XUẤT SẮC! VIDEO HOÀN CHỈNH ĐÃ ĐƯỢC KẾT XUẤT:")
    print(f"   📁 Đường dẫn: {final_video}")
    print(f"   💾 Dung lượng: {file_size_mb:.2f} MB")
    
    # Đo tổng thời lượng thực tế
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_video)]
    dur_sec = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip() or 0)
    print(f"   ⏱️ Tổng thời lượng: {dur_sec:.2f} giây (~{dur_sec/60:.1f} phút)")

    # Trích xuất ảnh snapshot
    snap_dir = OUTPUT_DIR / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    sample_timestamps = [10, 40, 70, 100, 130, 160, 190, 220, 250]
    for idx, t in enumerate(sample_timestamps[:len(scenes_to_stitch)], start=1):
        if t < dur_sec:
            snap_file = snap_dir / f"scene_{idx:02d}_preview.png"
            subprocess.run(["ffmpeg", "-y", "-ss", f"{t:02d}", "-i", str(final_video), "-vframes", "1", str(snap_file)], capture_output=True)
    print(f"   📸 Đã trích xuất ảnh snapshots tại: {snap_dir}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Pipeline sản xuất video whiteboard animation hoàn chỉnh.")
    parser.add_argument("--scenes", nargs="*", default=ALL_SCENES, help="Danh sách scene cần render (mặc định: tất cả 9 scenes)")
    parser.add_argument("--force", action="store_true", help="Bắt buộc render lại kể cả khi đã có video thô")
    args = parser.parse_args()

    active_scenes = args.scenes

    print("=" * 65)
    print("🚀 BẮT ĐẦU CHUỖI SẢN XUẤT TỰ ĐỘNG WHITEBOARD ANIMATION")
    print(f"📁 Dự án: {PROJ_DIR.name}")
    print(f"🎬 Phân cảnh: {', '.join(active_scenes)}")
    print("=" * 65)

    for s in active_scenes:
        print(f"\n▶ ĐANG XỬ LÝ {s.upper()}...")
        if not render_scene_video(s, force=args.force):
            sys.exit(1)
        if not mux_scene_audio(s):
            sys.exit(1)
        if not burn_scene_subtitle(s):
            sys.exit(1)

    if len(active_scenes) == len(ALL_SCENES):
        if not stitch_full_course(active_scenes):
            sys.exit(1)

if __name__ == "__main__":
    main()
