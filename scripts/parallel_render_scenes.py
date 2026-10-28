#!/usr/bin/env python3
"""
scripts/parallel_render_scenes.py
Chạy render song song đồng thời nhiều Scene cùng lúc và đo đạc thời gian chính xác từng giây.
"""
import time
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_scene_pipeline(scene_num: int):
    scene_dir = REPO_ROOT / f"assets/whiteboard/test_cases/test_case_10_articles/scene_{scene_num:02d}"
    png_path = scene_dir / f"scene_{scene_num:02d}.png"
    anno_path = scene_dir / f"scene_{scene_num:02d}.annotation.json"
    raw_mp4 = scene_dir / f"scene_{scene_num:02d}.mp4"
    audio_path = scene_dir / "narration.m4a"
    srt_path = scene_dir / "input.srt"
    voice_mp4 = scene_dir / f"scene_{scene_num:02d}_voice.mp4"
    final_sub_mp4 = scene_dir / f"scene_{scene_num:02d}_sub.mp4"
    hand_path = REPO_ROOT / "assets/drawing-hand.png"

    # Step 1: Render whiteboard video 60fps
    cmd_render = [
        str(REPO_ROOT / ".venv/bin/python"),
        str(REPO_ROOT / "scripts/render_stream_whiteboard.py"),
        str(png_path),
        str(anno_path),
        str(raw_mp4),
        str(hand_path),
        "--canvas-hex", "#FFFFFF",
        "--fps", "60",
        "--cap-long-edge", "1920"
    ]
    p_render = subprocess.run(cmd_render, capture_output=True, text=True)
    if p_render.returncode != 0:
        return False, f"Render failed: {p_render.stderr[-300:]}"

    # Step 2: Mux audio
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_mp4),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        str(voice_mp4)
    ]
    p_mux = subprocess.run(cmd_mux, capture_output=True, text=True)
    if p_mux.returncode != 0:
        return False, f"Audio muxing failed: {p_mux.stderr[-300:]}"

    # Step 3: Burn subtitle MarginV=4
    cmd_sub = [
        "ffmpeg", "-y",
        "-i", str(voice_mp4),
        "-vf", f"subtitles={srt_path}:force_style='FontSize=13,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=3,MarginV=4'",
        "-c:a", "copy",
        str(final_sub_mp4)
    ]
    p_sub = subprocess.run(cmd_sub, capture_output=True, text=True)
    if p_sub.returncode != 0:
        return False, f"Subtitle burning failed: {p_sub.stderr[-300:]}"

    # Step 4: Auto-extract QA snapshots into scene_dir/snapshots/
    snap_dir = scene_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    # Extract snapshots every 5 seconds
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_sub_mp4)]
    total_sec = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip() or 30)
    for t in [2, 6, 10, 15, 20, 25, int(total_sec - 3)]:
        if t < total_sec:
            snap_file = snap_dir / f"snapshot_{t:02d}s.png"
            subprocess.run(["ffmpeg", "-y", "-ss", f"00:00:{t:02d}.000", "-i", str(final_sub_mp4), "-vframes", "1", str(snap_file)], capture_output=True)

    return True, f"Success -> {final_sub_mp4.name}"

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor

    if len(sys.argv) > 1:
        scenes = [int(arg) for arg in sys.argv[1:]]
    else:
        scenes = [5, 6]
    print("=" * 65)
    print(f"⚡ BẮT ĐẦU CHẠY ĐỒNG THỜI SONG SONG SCENE {scenes}...")
    print("=" * 65)

    start_total = time.time()
    
    with ProcessPoolExecutor(max_workers=len(scenes)) as executor:
        futures = {executor.submit(run_scene_pipeline, s): s for s in scenes}
        for future in futures:
            s_id = futures[future]
            success, msg = future.result()
            print(f"🎬 Scene {s_id:02d}: {'✅ THÀNH CÔNG' if success else '❌ THẤT BẠI'} ({msg})")

    total_elapsed = time.time() - start_total
    print("=" * 65)
    print(f"⏱️  TỔNG THỜI GIAN HOÀN THÀNH CẢ 2 SCENE: {total_elapsed:.2f} giây ({total_elapsed/60:.2f} phút)!")
    print("=" * 65)
