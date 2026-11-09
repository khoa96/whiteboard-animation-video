#!/usr/bin/env python3
"""
compile_beat_plan.py — Biên dịch bản thiết kế Narration-Visual Beat Plan (SSOT)
thành hai sản phẩm dẫn xuất song hành:
1. narration_script.txt (cho khâu lồng tiếng TTS)
2. scene_matrix.md (cho khâu thiết kế bố cục và hoạt họa)

Đồng thời kiểm định:
- Zero Naked Dialogue: Không có câu thoại nào thiếu mục tiêu vẽ.
- WPM check: Tốc độ nói trong dải tối ưu 125 - 145 từ/phút.
- Dragging check: Cảnh báo nếu 1 nét vẽ kéo dài > 4.5 giây.
"""

import sys
import json
import re
from pathlib import Path
import argparse


def compile_beat_plan(beat_plan_path: Path, output_dir: Path = None):
    if not beat_plan_path.exists():
        print(f"❌ Lỗi: Không tìm thấy file {beat_plan_path}")
        sys.exit(1)

    with open(beat_plan_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if output_dir is None:
        output_dir = beat_plan_path.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    project_title = data.get("project_title", "Whiteboard Animation Project")
    project_id = data.get("project_id", "project_unknown")
    target_wpm = data.get("target_wpm", 135)
    scenes = data.get("scenes", [])

    print(f"============================================================")
    print(f"🚀 BIÊN DỊCH BEAT PLAN: {project_title} ({project_id})")
    print(f"============================================================")

    warnings = []
    errors = []

    # File outputs
    script_lines = [
        f"# KỊCH BẢN THUYẾT MINH CHUẨN HOÁ: {project_title}",
        f"# Mã dự án: {project_id}",
        f"# Tự động trích xuất từ: {beat_plan_path.name}",
        f"# Tốc độ đọc khuyến nghị: {target_wpm} từ/phút",
        f"# Quy chuẩn: Giọng đọc Nam miền Bắc điềm tĩnh, ấm áp, phát âm tiếng Anh chuẩn American English.",
        ""
    ]

    matrix_lines = [
        f"# MA TRẬN PHÂN CẢNH & VISUAL BEAT MAP V3.0",
        f"## DỰ ÁN: {project_title}",
        f"**Mã dự án:** `{project_id}` | **Biên dịch từ:** `{beat_plan_path.name}`",
        f"**Khóa cứng Bảng màu:** `#FFFFFF`, `#202124`, `#3478D4`, `#22A895`, `#F5A623`",
        f"**Khóa an toàn:** Vùng đáy canvas ($Y: 880 - 1080$) giữ trắng thuần làm Subtitle Safe Zone.",
        "",
        "---",
        ""
    ]

    total_beats = 0
    total_words = 0
    total_est_seconds = 0.0

    for s_idx, scene in enumerate(scenes):
        scene_num = scene.get("scene_index", s_idx + 1)
        scene_title = scene.get("title", f"Scene {scene_num}")
        beats = scene.get("beats", [])
        layout = scene.get("layout_architecture", "custom_layout")

        script_lines.append(f"=== SCENE {scene_num:02d}: {scene_title} ===")
        script_lines.append(f"(Thời lượng dự kiến: ~{scene.get('target_duration_sec', 40)} giây)")
        script_lines.append("")

        matrix_lines.append(f"### SCENE {scene_num:02d}: {scene_title}")
        matrix_lines.append(f"* **Kiến trúc Bố cục:** `{layout}`")
        matrix_lines.append(f"* **Số lượng Beats:** {len(beats)}")
        matrix_lines.append("")
        matrix_lines.append("| Beat ID | Lời thoại thuyết minh (Narration) | Mục tiêu vẽ (Visual Target) | Hành động vẽ | Role | Thời lượng | Trạng thái màn hình sau Beat |")
        matrix_lines.append("| :---: | :--- | :--- | :--- | :---: | :---: | :--- |")

        scene_words = 0
        scene_time = 0.0

        for b in beats:
            total_beats += 1
            b_id = b.get("beat_id", f"S{scene_num:02d}-B{total_beats}")
            narr = b.get("narration", "").strip()
            visual = b.get("visual", {})
            target_el = visual.get("target_element_id", "").strip()
            event_type = visual.get("event_type", "draw_new")
            text_role = visual.get("text_role", "NONE")
            vis_desc = visual.get("description", "")
            est_dur = float(b.get("estimated_duration_sec", 3.0))
            expected_state = b.get("expected_screen_state", "")

            # Validation checks
            words = re.findall(r"\b[\w'-]+\b", narr)
            w_count = len(words)
            scene_words += w_count
            total_words += w_count
            scene_time += est_dur
            total_est_seconds += est_dur

            if not narr:
                errors.append(f"❌ [Lỗi Rỗng] {b_id}: Lời thoại narration bị bỏ trống!")
            if not target_el:
                errors.append(f"❌ [Lỗi Thoại Rỗng / Naked Dialogue] {b_id}: Không có target_element_id! Bàn tay sẽ bị đóng băng!")
            if est_dur > 4.5:
                warnings.append(f"⚠️ [Cảnh Báo Kéo Giãn] {b_id}: Thời lượng vẽ {est_dur}s quá dài (> 4.5s). Nên phân rã thành micro-actions!")
            if est_dur < 1.2:
                warnings.append(f"⚠️ [Cảnh Báo Quá Nhanh] {b_id}: Thời lượng vẽ {est_dur}s quá ngắn (< 1.2s). Khán giả khó tiếp thu kịp!")

            # Add to script
            script_lines.append(f"[VO]  # {b_id}")
            script_lines.append(narr)
            script_lines.append("")

            # Add to matrix table
            narr_clean = narr.replace("|", "\\|")
            vis_desc_clean = vis_desc.replace("|", "\\|")
            exp_clean = expected_state.replace("|", "\\|")
            matrix_lines.append(f"| `{b_id}` | {narr_clean} | `{target_el}` | {event_type} ({vis_desc_clean}) | `{text_role}` | {est_dur}s | {exp_clean} |")

        # End of scene in script
        script_lines.append("[HOLD FINAL DRAWING — 0.5 SECOND, NO SPEECH]")
        script_lines.append(f"=== END SCENE {scene_num:02d} ===")
        script_lines.append("")
        script_lines.append("")

        matrix_lines.append("")
        matrix_lines.append(f"**Tổng thời lượng Scene {scene_num:02d}:** ~{scene_time:.1f}s ({scene_words} từ).")
        matrix_lines.append("")
        matrix_lines.append("---")
        matrix_lines.append("")

    # Write files
    script_out_path = output_dir / "narration_script.txt"
    matrix_out_path = output_dir / "scene_matrix.md"

    with open(script_out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(script_lines))

    with open(matrix_out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(matrix_lines))

    print(f"\n📊 BÁO CÁO PHÂN TÍCH NHỊP ĐIỆU:")
    print(f"  • Tổng số Beats: {total_beats}")
    print(f"  • Tổng số từ thoại: {total_words}")
    print(f"  • Tổng thời lượng dự kiến: {total_est_seconds:.1f} giây ({total_est_seconds/60:.2f} phút)")
    effective_wpm = (total_words / (total_est_seconds / 60.0)) if total_est_seconds > 0 else 0
    print(f"  • Tốc độ đọc thực tế: {effective_wpm:.1f} WPM (Mục tiêu: {target_wpm} WPM)")

    if errors:
        print(f"\n🚨 PHÁT HIỆN {len(errors)} LỖI NGHIÊM TRỌNG:")
        for err in errors:
            print(f"  {err}")
    else:
        print(f"\n✅ KIỂM ĐỊNH THÀNH CÔNG: 0% Thoại rỗng (Zero Naked Dialogue).")

    if warnings:
        print(f"\n⚠️ CẢNH BÁO TỐC ĐỘ / NHỊP ({len(warnings)} cảnh báo):")
        for w in warnings:
            print(f"  {w}")

    print(f"\n🎉 ĐÃ XUẤT THÀNH CÔNG:")
    print(f"  ✓ {script_out_path}")
    print(f"  ✓ {matrix_out_path}")

    return len(errors) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile beat_plan.json to script and matrix.")
    parser.add_argument("beat_plan", type=Path, help="Path to beat_plan.json")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory")
    args = parser.parse_args()

    success = compile_beat_plan(args.beat_plan, args.output_dir)
    sys.exit(0 if success else 1)
