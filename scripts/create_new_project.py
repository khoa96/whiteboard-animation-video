#!/usr/bin/env python3
"""
create_new_project.py — Khởi tạo thư mục và tài nguyên chuẩn cho một dự án video mới.

Cách dùng:
    python scripts/create_new_project.py WB-ENG-A1-004 "Mạo từ A và AN trong Tiếng Anh"
"""

import sys
import json
import argparse
from pathlib import Path


def create_project(project_id: str, title: str) -> Path:
    root = Path(__file__).resolve().parent.parent
    proj_dir = root / "projects" / project_id
    if proj_dir.exists():
        print(f"Lỗi: Thư mục dự án {proj_dir} đã tồn tại!")
        sys.exit(1)

    proj_dir.mkdir(parents=True, exist_ok=True)
    images_dir = proj_dir / "images"
    scenes_dir = proj_dir / "scenes"
    images_dir.mkdir(exist_ok=True)
    scenes_dir.mkdir(exist_ok=True)

    templates_dir = root / ".agents" / "skills" / "content-engine" / "templates"

    # 1. project.json
    project_meta = {
        "projectId": project_id,
        "title": title,
        "version": "1.0",
        "createdAt": "2026-11-04T00:00:00Z",
        "status": "STAGE_1_INTAKE",
        "voiceId": "voice_xnxd3uit2744",
        "fps": 60,
        "canvas": {"width": 1920, "height": 1080}
    }
    with open(proj_dir / "project.json", "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2, ensure_ascii=False)

    # 2. brief.md
    brief_tmpl = templates_dir / "BRIEF.template.md"
    if brief_tmpl.exists():
        content = brief_tmpl.read_text(encoding="utf-8")
        content = content.replace("{{PROJECT_ID}}", project_id).replace("{{PROJECT_TITLE}}", title)
        (proj_dir / "brief.md").write_text(content, encoding="utf-8")

    # 3. SCENE_MATRIX_AND_PROMPTS.md
    matrix_tmpl = templates_dir / "SCENE_MATRIX.template.md"
    if matrix_tmpl.exists():
        content = matrix_tmpl.read_text(encoding="utf-8")
        content = content.replace("{{PROJECT_ID}}", project_id).replace("{{PROJECT_TITLE}}", title)
        (proj_dir / "SCENE_MATRIX_AND_PROMPTS.md").write_text(content, encoding="utf-8")

    # 4. narration_script_draft.txt
    script_tmpl = templates_dir / "SCRIPT.template.txt"
    if script_tmpl.exists():
        content = script_tmpl.read_text(encoding="utf-8")
        content = content.replace("{{PROJECT_ID}}", project_id).replace("{{PROJECT_TITLE}}", title)
        (proj_dir / "narration_script_draft.txt").write_text(content, encoding="utf-8")

    print(f"🎉 Khởi tạo thành công dự án mới: {proj_dir}")
    print(f"  • Thư mục hình ảnh : {images_dir}")
    print(f"  • Thư mục video    : {scenes_dir}")
    print(f"  • Metadata dự án   : {proj_dir / 'project.json'}")
    print(f"  • Giáo trình nháp  : {proj_dir / 'brief.md'}")
    return proj_dir


def main():
    parser = argparse.ArgumentParser(description="Khởi tạo dự án video Whiteboard Animation mới")
    parser.add_argument("project_id", type=str, help="Mã dự án (e.g. WB-ENG-A1-004)")
    parser.add_argument("title", type=str, help="Tiêu đề bài học")
    args = parser.parse_args()

    create_project(args.project_id, args.title)


if __name__ == "__main__":
    main()
