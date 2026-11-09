#!/usr/bin/env python3
"""
rebuild_all_micro_scenes.py
Automated end-to-end rendering, muxing, burning and stitching for all 4 micro-segmented scenes.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "projects/project_articles_a_an"
SCENES_DIR = PROJ_DIR / "scenes"
OUTPUT_DIR = PROJ_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import subtitle_styler

def run_cmd(cmd_list, description):
    print(f"  ▶ {description}...")
    res = subprocess.run(cmd_list, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  ❌ Lỗi khi chạy: {' '.join(cmd_list)}")
        print(f"  STDOUT: {res.stdout}")
        print(f"  STDERR: {res.stderr}")
        raise RuntimeError(f"Command failed: {description}")
    return res

def process_scene(s_num: int):
    s_name = f"scene_{s_num:02d}"
    s_dir = SCENES_DIR / s_name
    img_path = s_dir / f"{s_name}.png"
    ann_path = s_dir / f"{s_name}.annotation.json"
    raw_video = s_dir / f"{s_name}.mp4"
    audio_path = s_dir / "narration.m4a"
    voice_video = s_dir / f"{s_name}_voice.mp4"
    srt_path = s_dir / "input.srt"
    sub_video = s_dir / f"{s_name}_sub.mp4"
    snaps_dir = s_dir / "snapshots"
    snaps_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*65}")
    print(f"🎬 ĐANG XỬ LÝ {s_name.upper()}...")
    print(f"{'='*65}")

    # 1. Render whiteboard stream video (1920x1080 @ 60fps)
    render_cmd = [
        str(REPO_ROOT / ".venv/bin/python3"),
        str(REPO_ROOT / "scripts/render_stream_whiteboard.py"),
        str(img_path),
        str(ann_path),
        str(raw_video),
        "--cap-long-edge", "1920",
        "--fps", "60"
    ]
    run_cmd(render_cmd, f"Render video hoạt họa 60fps ({s_name}.mp4)")

    # 2. Mux audio master clock
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        str(voice_video),
        "-loglevel", "error"
    ]
    run_cmd(mux_cmd, f"Ghép audio Master Clock ({s_name}_voice.mp4)")

    # 3. Burn dark_slate_obsidian subtitles
    print(f"  ▶ Dập phụ đề dark_slate_obsidian ({s_name}_sub.mp4)...")
    subtitle_styler.burn_subtitles_to_video(
        input_video=str(voice_video),
        srt_or_ass=str(srt_path),
        output_video=str(sub_video),
        project_dir=str(PROJ_DIR)
    )
    print(f"  ✓ Đã dập phụ đề thành công: {sub_video.name}")

    # 4. Extract QA snapshots
    # Sample 4 points across the scene
    dur_res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(sub_video)
    ], capture_output=True, text=True)
    dur = float(dur_res.stdout.strip())
    sample_times = [round(dur * frac, 1) for frac in [0.15, 0.40, 0.65, 0.90]]

    for t in sample_times:
        snap_path = snaps_dir / f"snap_{t}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(t), "-i", str(sub_video),
            "-vframes", "1", str(snap_path), "-loglevel", "error"
        ])
    print(f"  ✓ Đã trích xuất {len(sample_times)} ảnh QA snapshots: {sample_times}")

def stitch_master_video():
    print(f"\n{'='*65}")
    print("🎞️ ĐANG NỐI TOÀN BỘ CÁC CẢNH THÀNH VIDEO MASTER...")
    print(f"{'='*65}")
    concat_list = OUTPUT_DIR / "concat_list.txt"
    lines = []
    for s_num in [1, 2, 3, 4]:
        sub_video = SCENES_DIR / f"scene_{s_num:02d}" / f"scene_{s_num:02d}_sub.mp4"
        lines.append(f"file '{sub_video.resolve()}'")
    concat_list.write_text("\n".join(lines) + "\n", encoding="utf-8")

    final_video = OUTPUT_DIR / "articles_a_an_final.mp4"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_video),
        "-loglevel", "error"
    ]
    run_cmd(concat_cmd, f"Ghép nối chuỗi 4 cảnh vào {final_video.name}")

    # Final video snapshots
    out_snaps = OUTPUT_DIR / "snapshots"
    out_snaps.mkdir(parents=True, exist_ok=True)
    for t in [10, 45, 80, 120, 155]:
        snap_path = out_snaps / f"master_snap_{t}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(t), "-i", str(final_video),
            "-vframes", "1", str(snap_path), "-loglevel", "error"
        ])
    print(f"  ✓ Đã trích xuất snapshots hoàn thiện cho Master Video!")
    print(f"🎉 TOÀN TẤT! Video Master xuất sắc sẵn sàng tại: {final_video}")

if __name__ == "__main__":
    for s in [1, 2, 3, 4]:
        process_scene(s)
    stitch_master_video()

