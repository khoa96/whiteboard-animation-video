#!/usr/bin/env python3
"""
Bộ thực thi Render song song đa tiến trình (Concurrent Parallel Batch Renderer)
Chạy đồng thời n test case bằng ProcessPoolExecutor để kiểm tra tối đa hiệu năng render bảng trắng.
"""
import concurrent.futures
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_BIN = str(REPO_ROOT / ".venv/bin/python")

TEST_CASES = [
    {
        "id": "TC04",
        "name": "DO VS MAKE",
        "dir": "projects/WB-TEST-CASE-04",
        "snapshots": ["00:00:04.000", "00:00:09.000", "00:00:16.000"]
    },
    {
        "id": "TC05",
        "name": "PAST VS PRESENT",
        "dir": "projects/WB-TEST-CASE-05",
        "snapshots": ["00:00:04.000", "00:00:09.000", "00:00:16.000"]
    },
    {
        "id": "TC06",
        "name": "3 STEPS TO SPEAK FLUENTLY",
        "dir": "projects/WB-TEST-CASE-06",
        "snapshots": ["00:00:04.000", "00:00:08.000", "00:00:14.000", "00:00:20.000"]
    }
]

def render_single_test_case(tc: dict) -> dict:
    start_t = time.time()
    proj_dir = REPO_ROOT / tc["dir"]
    img_f = proj_dir / "images/scene_01.png"
    ann_f = proj_dir / "images/scene_01.annotation.json"
    raw_mp4 = proj_dir / "scenes/scene_01.mp4"
    sub_mp4 = proj_dir / "scenes/scene_01_with_subtitles.mp4"
    ass_f = proj_dir / "input.ass"
    hand_f = REPO_ROOT / "assets/drawing-hand.png"
    snap_dir = proj_dir / "scenes/snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 [{tc['id']}] Bắt đầu render hoạt họa: {tc['name']}...")

    # 1. Render Whiteboard Video
    cmd_render = [
        PYTHON_BIN,
        str(REPO_ROOT / "scripts/render_stream_whiteboard.py"),
        str(img_f),
        str(ann_f),
        str(raw_mp4),
        str(hand_f),
        "--cap-long-edge", "1920",
        "--fps", "30",
        "--canvas-hex", "#FFFFFF"
    ]
    res_render = subprocess.run(cmd_render, capture_output=True, text=True)
    if res_render.returncode != 0:
        return {"id": tc["id"], "ok": False, "error": f"Render lỗi: {res_render.stderr[:300]}"}

    # 2. Burn Subtitles
    print(f"  ↳ [{tc['id']}] Ghi đè phụ đề chuẩn thẩm mỹ...")
    cmd_sub = [
        "python3",
        str(REPO_ROOT / "scripts/subtitle_styler.py"),
        "burn",
        str(raw_mp4),
        str(ass_f),
        str(sub_mp4),
        "--project", str(proj_dir)
    ]
    res_sub = subprocess.run(cmd_sub, capture_output=True, text=True)
    if res_sub.returncode != 0:
        return {"id": tc["id"], "ok": False, "error": f"Phụ đề lỗi: {res_sub.stderr[:300]}"}

    # 3. Extract Snapshots
    print(f"  ↳ [{tc['id']}] Trích xuất snapshots kiểm tra...")
    for idx, ts in enumerate(tc["snapshots"], start=1):
        out_snap = snap_dir / f"snap_{idx:02d}.png"
        cmd_snap = [
            "ffmpeg", "-y", "-ss", ts,
            "-i", str(sub_mp4),
            "-vframes", "1",
            str(out_snap)
        ]
        subprocess.run(cmd_snap, capture_output=True)

    dur = time.time() - start_t
    size_mb = sub_mp4.stat().st_size / (1024 * 1024)
    print(f"✅ [{tc['id']}] Hoàn thành xuất sắc trong {dur:.1f}s ({size_mb:.2f} MB)")
    return {
        "id": tc["id"],
        "name": tc["name"],
        "ok": True,
        "duration": dur,
        "video": str(sub_mp4),
        "size_mb": size_mb
    }

def main():
    print("=" * 65)
    print("BẮT ĐẦU CHẠY ĐỒNG THỜI (PARALLEL EXECUTION) 3 TEST CASE:")
    print("  • TC04: DO VS MAKE")
    print("  • TC05: PAST VS PRESENT")
    print("  • TC06: 3 STEPS TO SPEAK FLUENTLY")
    print("=" * 65)

    wall_start = time.time()
    results = []
    # Thực thi song song tối đa 3 workers
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(render_single_test_case, tc): tc["id"] for tc in TEST_CASES}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)

    total_wall_time = time.time() - wall_start
    sum_individual_time = sum(r["duration"] for r in results if r["ok"])
    speedup = sum_individual_time / total_wall_time if total_wall_time > 0 else 1.0

    print("=" * 65)
    print("🎉 HOÀN THÀNH TẤT CẢ TIẾN TRÌNH ĐỒNG THỜI!")
    print(f"  • Tổng thời gian thực tế (Wall Time): {total_wall_time:.1f} giây")
    print(f"  • Tổng thời gian nếu chạy tuần tự   : {sum_individual_time:.1f} giây")
    print(f"  • Hệ số tăng tốc đồng thời (Speedup): {speedup:.2f}x nhanh hơn!")
    print("=" * 65)

    for r in sorted(results, key=lambda x: x["id"]):
        status = "Thành công ✓" if r["ok"] else f"Thất bại ✗ ({r.get('error')})"
        print(f"  • {r['id']} ({r.get('name')}): {status} - {r.get('duration', 0):.1f}s")

if __name__ == "__main__":
    main()
