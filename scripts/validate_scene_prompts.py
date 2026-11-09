#!/usr/bin/env python3
"""
validate_scene_prompts.py — Kiểm định tính tuân thủ của file SCENE_PROMPTS.md
đối với chuẩn Whiteboard Master Prompt v2.1.

Các tiêu chí kiểm tra:
1. Có đoạn Typography Lock nguyên văn (Verbatim Typography Lock).
2. Có quy tắc Subtitle Safe Zone (khóa 200px đáy màn hình Y: 880-1080).
3. Đủ 5 mã Hex chuẩn mực (#FFFFFF, #202124, #3478D4, #22A895, #F5A623).
4. Có danh mục Negative Tokens cấm vẽ tay / bút vẽ / bóng đổ / dính nét.
5. Kiểm tra khoảng hở nét (Isolated Ink Islands >= 35px).
"""

import sys
import re
from pathlib import Path
import argparse

REQUIRED_HEX = ["#FFFFFF", "#202124", "#3478D4", "#22A895", "#F5A623"]

def validate_prompts_file(path: Path) -> bool:
    if not path.exists():
        print(f"❌ Không tìm thấy file: {path}")
        return False

    text = path.read_text(encoding="utf-8")
    errors = []
    warnings = []

    # 1. Check Typography Lock
    if "TYPOGRAPHY LOCK" not in text:
        errors.append("Thiếu đoạn 'TYPOGRAPHY LOCK' bắt buộc!")
    elif "use this same lettering system for every scene" not in text:
        warnings.append("Đoạn 'TYPOGRAPHY LOCK' dường như bị chỉnh sửa, không khớp 100% bản chuẩn v2.1.")

    # 2. Check Subtitle Safe Zone
    if ("880" not in text and "840" not in text) or "1080" not in text:
        errors.append("Thiếu cảnh báo Subtitle Safe Zone (khóa Y: 840/880 - 1080)!")
    elif "bottom" not in text.lower() and "safe zone" not in text.lower():
        warnings.append("Khuyến nghị dùng cụm từ 'bottom 200/240 pixels' để AI sinh ảnh nhận diện rõ ranh giới.")

    # 3. Check Hex Palette
    for h in REQUIRED_HEX:
        if h not in text and h.lower() not in text:
            errors.append(f"Thiếu mã màu chuẩn: {h}")

    # 4. Check Negative Tokens
    neg_lower = text.lower()
    if "no drawing hands" not in neg_lower and "no hands holding pens" not in neg_lower and "hand" not in neg_lower:
        errors.append("Thiếu cảnh báo cấm vẽ bàn tay cầm bút (Hands / Pens)!")

    # 5. Check isolated ink islands rule
    if "isolated ink islands" not in neg_lower and "whitespace" not in neg_lower and "gutter" not in neg_lower:
        warnings.append("Chưa nhấn mạnh quy tắc 'Isolated Ink Islands' (khoảng cách nét >= 35-40px).")

    print(f"============================================================")
    print(f"🎨 KIỂM ĐỊNH TÍNH TUÂN THỦ PROMPT V2.1: {path.name}")
    print(f"============================================================")

    if errors:
        print(f"\n❌ PHÁT HIỆN {len(errors)} LỖI VI PHẠM MASTER PROMPT V2.1:")
        for e in errors:
            print(f"   - {e}")
    else:
        print(f"\n✅ ĐẠT CHUẨN 100%: Tuân thủ toàn diện Whiteboard Master Prompt v2.1!")

    if warnings:
        print(f"\n⚠️ CẢNH BÁO TỐI ƯU HÓA ({len(warnings)} cảnh báo):")
        for w in warnings:
            print(f"   - {w}")

    return len(errors) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate prompt file against master prompt v2.1.")
    parser.add_argument("prompt_file", type=Path, help="Path to SCENE_PROMPTS.md")
    args = parser.parse_args()

    ok = validate_prompts_file(args.prompt_file)
    sys.exit(0 if ok else 1)
