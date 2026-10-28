#!/usr/bin/env python3
"""
scripts/init_project.py
Khởi tạo cấu trúc dự án mẫu (Template Scaffold) cho dự án Whiteboard Animation mới.

Sử dụng:
    python scripts/init_project.py <tên_hoặc_đường_dẫn_dự_án> [--title "Tiêu đề"] [--voice "tên_voice"]

Ví dụ:
    python scripts/init_project.py test_case_11_passive_voice
    python scripts/init_project.py assets/whiteboard/test_cases/case_11_tenses --title "Thì Quá Khứ Đơn"
"""

import os
import sys
import argparse
import shutil
import json
from pathlib import Path

# Thư mục gốc repo
REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "templates" / "project_template"

def init_project(target_path_str: str, title: str = None, voice: str = None, force: bool = False):
    target_path = Path(target_path_str)
    
    # Nếu chỉ truyền tên folder đơn giản, mặc định lưu vào thư mục projects/
    if not target_path.is_absolute() and len(target_path.parts) == 1:
        target_dir = REPO_ROOT / "projects" / target_path
    else:
        target_dir = target_path if target_path.is_absolute() else (REPO_ROOT / target_path)

    project_name = target_dir.name
    project_title = title if title else project_name.replace("_", " ").title()
    selected_voice = voice if voice else "en-US-AndrewMultilingualNeural"

    print("=" * 65)
    print(f"🎬 KHỞI TẠO DỰ ÁN WHITEBOARD ANIMATION: {project_name}")
    print(f"📁 Thư mục đích: {target_dir}")
    print("=" * 65)

    if target_dir.exists():
        if not force and any(target_dir.iterdir()):
            print(f"⚠️  Thư mục '{target_dir}' đã tồn tại và không rỗng!")
            print("   Dùng cờ --force (-f) nếu bạn muốn ghi đè.")
            sys.exit(1)
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Đảm bảo thư mục images/ và scenes/ tồn tại
    images_dir = target_dir / "images"
    scenes_dir = target_dir / "scenes"
    images_dir.mkdir(parents=True, exist_ok=True)
    scenes_dir.mkdir(parents=True, exist_ok=True)

    # 2. Tạo brief.md
    brief_template = (TEMPLATE_DIR / "brief.md").read_text(encoding="utf-8") if (TEMPLATE_DIR / "brief.md").exists() else ""
    brief_content = brief_template.replace("[TÊN CHỦ ĐỀ BÀI HỌC]", project_title)
    brief_content = brief_content.replace("[TÊN CHỦ ĐỀ]", project_title)
    brief_content = brief_content.replace("en-US-AndrewMultilingualNeural", selected_voice)
    (target_dir / "brief.md").write_text(brief_content, encoding="utf-8")
    print(f"  ✓ Đã tạo: brief.md (Tóm tắt sáng tạo & bảng màu)")

    # 3. Tạo subtitle_draft.srt
    srt_template = (TEMPLATE_DIR / "subtitle_draft.srt").read_text(encoding="utf-8") if (TEMPLATE_DIR / "subtitle_draft.srt").exists() else ""
    srt_content = srt_template.replace("[Chủ đề bài học]", project_title)
    (target_dir / "subtitle_draft.srt").write_text(srt_content, encoding="utf-8")
    print(f"  ✓ Đã tạo: subtitle_draft.srt (Kịch bản lời thoại mẫu)")

    # 4. Tạo images/README.md
    img_readme = (TEMPLATE_DIR / "images" / "README.md").read_text(encoding="utf-8") if (TEMPLATE_DIR / "images" / "README.md").exists() else ""
    (images_dir / "README.md").write_text(img_readme, encoding="utf-8")
    print(f"  ✓ Đã tạo: images/README.md (Hướng dẫn ảnh nguồn 16:9)")

    # 5. Tạo project.json
    project_cfg = {
        "project_name": project_name,
        "title": project_title,
        "version": "1.0.0",
        "settings": {
            "resolution": {"width": 1920, "height": 1080},
            "canvas_color": "#FFFFFF",
            "production_fps": 60,
            "draft_fps": 30,
            "voice": {
                "engine": "edge-tts",
                "model": selected_voice,
                "rate": "+0%",
                "volume": "+0%"
            },
            "subtitles": {
                "font_size": 13,
                "margin_v": 4,
                "border_style": 3,
                "primary_color": "&H00FFFFFF",
                "back_color": "&H80000000"
            }
        }
    }
    (target_dir / "project.json").write_text(json.dumps(project_cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Đã tạo: project.json (Cấu hình tham số kỹ thuật)")
    print(f"  ✓ Đã tạo: scenes/ (Thư mục làm việc cho các cảnh kết xuất)")

    print("\n" + "-" * 65)
    print("✨ DỰ ÁN ĐÃ SẴN SÀNG! 3 BƯỚC TIẾP THEO:")
    print(f"1. Cập nhật nội dung bài giảng tại: {target_dir / 'brief.md'}")
    print(f"2. Điền lời thoại các cảnh vào:     {target_dir / 'subtitle_draft.srt'}")
    print(f"3. Đặt ảnh 16:9 của từng cảnh vào: {target_dir / 'images'}/scene_01.png, scene_02.png...")
    print("-" * 65 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Khởi tạo dự án Whiteboard Animation mới từ template chuẩn.")
    parser.add_argument("project_path", help="Tên dự án hoặc đường dẫn thư mục muốn tạo (VD: project_tenses hoặc assets/whiteboard/test_cases/case_11)")
    parser.add_argument("--title", help="Tiêu đề bài học hiển thị trong brief (VD: 'Thì Quá Khứ Đơn')")
    parser.add_argument("--voice", default="en-US-AndrewMultilingualNeural", help="Tên model giọng đọc Edge-TTS (mặc định: en-US-AndrewMultilingualNeural)")
    parser.add_argument("-f", "--force", action="store_true", help="Ghi đè nếu thư mục đã tồn tại")

    args = parser.parse_args()
    init_project(args.project_path, title=args.title, voice=args.voice, force=args.force)

if __name__ == "__main__":
    main()
