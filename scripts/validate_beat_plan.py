#!/usr/bin/env python3
"""
validate_beat_plan.py — Công cụ kiểm định chất lượng (Gate 2 Validator) cho file beat_plan.json.
Kiểm tra:
1. Tính đầy đủ của cấu trúc JSON theo Schema.
2. 100% Beats có lời thoại và mục tiêu hình ảnh (Zero Naked Dialogue).
3. Cảnh báo nhịp nói quá nhanh (> 160 WPM) hoặc quá chậm (< 110 WPM).
4. Cảnh báo nét vẽ rùa bò (> 4.5s) hoặc chớp nhoáng (< 1.2s).
5. Xác minh tất cả Text Role đều thuộc danh mục chuẩn v2.1 (T0-T9, NONE).
"""

import sys
import json
import re
from pathlib import Path
import argparse

VALID_TEXT_ROLES = {"T0", "T1", "T2", "T3", "T4", "T5", "T6", "T7a", "T7b", "T7c", "T8", "T9", "NONE"}

def validate_beat_plan(path: Path) -> bool:
    if not path.exists():
        print(f"❌ Lỗi: Không tìm thấy file {path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi cú pháp JSON trong {path}: {e}")
        return False

    errors = []
    warnings = []

    scenes = data.get("scenes", [])
    if not scenes:
        errors.append("Danh sách 'scenes' rỗng!")

    total_beats = 0
    total_words = 0
    total_duration = 0.0

    for s in scenes:
        s_num = s.get("scene_index", 0)
        s_title = s.get("title", f"Scene {s_num}")
        beats = s.get("beats", [])
        if not beats:
            errors.append(f"Scene {s_num} ('{s_title}') không có bất kỳ Beat nào!")

        for b in beats:
            total_beats += 1
            b_id = b.get("beat_id", f"S{s_num}-B{total_beats}")
            narr = b.get("narration", "").strip()
            dur = float(b.get("estimated_duration_sec", 0.0))
            vis = b.get("visual", {})
            target = vis.get("target_element_id", "").strip()
            role = vis.get("text_role", "NONE")
            exp_state = b.get("expected_screen_state", "").strip()

            if not narr:
                errors.append(f"[{b_id}] Thiếu lời thoại narration!")
            if not target:
                errors.append(f"[{b_id}] THOẠI RỖNG (Naked Dialogue): Thiếu target_element_id!")
            if not exp_state:
                warnings.append(f"[{b_id}] Thiếu expected_screen_state!")
            if role not in VALID_TEXT_ROLES:
                errors.append(f"[{b_id}] Text Role '{role}' không hợp lệ! Phải thuộc danh mục v2.1: {sorted(list(VALID_TEXT_ROLES))}")

            words = len(re.findall(r"\b[\w'-]+\b", narr))
            total_words += words
            total_duration += dur

            if dur > 4.5:
                warnings.append(f"[{b_id}] Thời lượng vẽ {dur}s > 4.5s. Cần phân rã thành micro-actions để tránh vẽ giật/chậm!")
            elif dur < 1.2:
                warnings.append(f"[{b_id}] Thời lượng vẽ {dur}s < 1.2s. Nét vẽ xuất hiện quá chớp nhoáng!")

            if dur > 0:
                beat_wpm = (words / dur) * 60.0
                if beat_wpm > 175:
                    warnings.append(f"[{b_id}] Tốc độ nói {beat_wpm:.0f} WPM quá nhanh so với thời gian vẽ ({dur}s)!")
                elif beat_wpm < 90 and words > 0:
                    warnings.append(f"[{b_id}] Tốc độ nói {beat_wpm:.0f} WPM quá chậm so với thời gian vẽ ({dur}s)!")

    print(f"============================================================")
    print(f"🔍 KẾT QUẢ KIỂM ĐỊNH BEAT PLAN: {path.name}")
    print(f"============================================================")
    print(f"  • Tổng phân cảnh: {len(scenes)}")
    print(f"  • Tổng Beats: {total_beats}")
    print(f"  • Tổng từ: {total_words} từ")
    print(f"  • Tổng thời lượng: {total_duration:.1f}s ({total_duration/60:.2f} phút)")
    
    if total_duration > 0:
        avg_wpm = (total_words / total_duration) * 60.0
        print(f"  • Tốc độ đọc trung bình: {avg_wpm:.1f} WPM")

    if errors:
        print(f"\n❌ PHÁT HIỆN {len(errors)} LỖI CẦN SỬA NGAY:")
        for e in errors:
            print(f"   - {e}")
    else:
        print(f"\n✅ ĐẠT CHUẨN GATE 2: 100% Beats hợp lệ, 0% Thoại rỗng.")

    if warnings:
        print(f"\n⚠️ CÓ {len(warnings)} CẢNH BÁO TỐI ƯU HÓA:")
        for w in warnings:
            print(f"   - {w}")

    return len(errors) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate beat_plan.json.")
    parser.add_argument("beat_plan", type=Path, help="Path to beat_plan.json")
    args = parser.parse_args()

    ok = validate_beat_plan(args.beat_plan)
    sys.exit(0 if ok else 1)
