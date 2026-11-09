#!/usr/bin/env python3
"""
Máy chủ xem trước & chỉnh sửa Whiteboard Animation cục bộ (Local Preview Server)
Cung cấp API lưu file trực tiếp vào đĩa cho assets/preview.html,
loại bỏ hoàn toàn việc phải tải file về máy và chép đè thủ công.

Cách dùng:
  python3 scripts/preview_server.py [--port 8000] [--dir assets/whiteboard/thi-hien-tai-don]
"""
import argparse
import http.server
import json
import os
import socketserver
import subprocess
import sys
import urllib.parse
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
try:
    import subtitle_styler
except ImportError:
    subtitle_styler = None


class WhiteboardPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def end_headers(self):
        # Thêm CORS và Cache-Control để không bị cache dữ liệu cũ
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/projects":
            self.handle_get_projects()
        elif parsed.path == "/api/scenes":
            self.handle_get_scenes(parsed.query)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/save":
            self.handle_save()
        else:
            self.send_error(404, "Endpoint không tồn tại")

    def handle_get_projects(self):
        """Liệt kê các thư mục dự án trong projects/ và assets/whiteboard/"""
        projects = []
        img_exts = {".png", ".jpg", ".jpeg"}

        def is_valid_scene_img(path: Path) -> bool:
            name = path.name.lower()
            if path.suffix.lower() not in img_exts:
                return False
            if name.endswith("-regions.png") or name.endswith("_regions.png"):
                return False
            if name.endswith("-regions.jpg") or name.endswith("_regions.jpg"):
                return False
            if name.startswith("crop_") or name.startswith("snap_"):
                return False
            return True

        # 1. Quét projects/
        proj_dir = REPO_ROOT / "projects"
        if proj_dir.exists():
            for p in sorted(proj_dir.iterdir()):
                if p.is_dir() and not p.name.startswith("."):
                    img_folder = p / "images" if (p / "images").exists() else p
                    scene_imgs = [f for f in img_folder.iterdir() if is_valid_scene_img(f)]
                    projects.append({
                        "name": f"📁 {p.name}",
                        "relPath": str(img_folder.relative_to(REPO_ROOT)),
                        "sceneCount": len(scene_imgs)
                    })

        # 2. Quét assets/whiteboard/ (legacy)
        wb_dir = REPO_ROOT / "assets" / "whiteboard"
        if wb_dir.exists():
            for p in sorted(wb_dir.iterdir()):
                if p.is_dir() and not p.name.startswith("."):
                    scene_imgs = [f for f in p.iterdir() if is_valid_scene_img(f)]
                    projects.append({
                        "name": f"🎨 {p.name}",
                        "relPath": str(p.relative_to(REPO_ROOT)),
                        "sceneCount": len(scene_imgs)
                    })

        self.send_json({"ok": True, "projects": projects})

    def handle_get_scenes(self, query_str):
        """Liệt kê tất cả cặp ảnh & annotation trong một thư mục dự án"""
        params = urllib.parse.parse_qs(query_str)
        default_dir = "projects/WB-TEST-CASE-01/images" if (REPO_ROOT / "projects/WB-TEST-CASE-01/images").exists() else "assets/whiteboard/thi-hien-tai-don"
        rel_dir = params.get("dir", [default_dir])[0]
        target_dir = (REPO_ROOT / rel_dir).resolve()

        if not str(target_dir).startswith(str(REPO_ROOT)) or not target_dir.exists():
            self.send_json({"ok": False, "error": "Thư mục không hợp lệ"}, status=400)
            return

        img_exts = {".png", ".jpg", ".jpeg"}
        scenes = []
        for f in sorted(target_dir.iterdir()):
            name_lower = f.name.lower()
            if f.suffix.lower() in img_exts:
                if name_lower.endswith("-regions.png") or name_lower.endswith("_regions.png"):
                    continue
                if name_lower.endswith("-regions.jpg") or name_lower.endswith("_regions.jpg"):
                    continue
                if name_lower.startswith("crop_") or name_lower.startswith("snap_"):
                    continue

                base = f.stem
                cfg_path = target_dir / f"{base}.annotation.json"
                cfg_data = None
                if cfg_path.exists():
                    try:
                        cfg_data = json.loads(cfg_path.read_text(encoding="utf-8"))
                    except Exception:
                        pass
                scenes.append({
                    "name": base,
                    "imgName": f.name,
                    "imgUrl": "/" + str(f.relative_to(REPO_ROOT)).replace("\\", "/"),
                    "cfgName": f"{base}.annotation.json",
                    "cfgRelPath": str(cfg_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                    "hasConfig": cfg_data is not None,
                    "cfg": cfg_data
                })

        self.send_json({"ok": True, "dir": str(target_dir.relative_to(REPO_ROOT)), "scenes": scenes})

    def handle_save(self):
        """Lưu trực tiếp nội dung annotation.json vào ổ đĩa"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body)

            rel_path = payload.get("filepath", "")
            data = payload.get("data")

            if not rel_path or data is None:
                self.send_json({"ok": False, "error": "Thiếu filepath hoặc data"}, status=400)
                return

            target_file = (REPO_ROOT / rel_path).resolve()
            if not str(target_file).startswith(str(REPO_ROOT)):
                self.send_json({"ok": False, "error": "Đường dẫn ngoài thư mục dự án bị từ chối"}, status=403)
                return

            target_file.parent.mkdir(parents=True, exist_ok=True)
            text = json.dumps(data, ensure_ascii=False, indent=2)
            target_file.write_text(text, encoding="utf-8")

            print(f"  ✓ [Lưu thành công]: {target_file.relative_to(REPO_ROOT)} ({len(data.get('elements', []))} elements)")

            # Tự động đồng bộ các file liên quan (Auto-Sync Pipeline)
            synced_files = self.auto_sync_artifacts(target_file, data)

            msg = f"Đã lưu thành công: {target_file.name}"
            if synced_files:
                msg += f" (Đã tự động đồng bộ: {', '.join(synced_files)})"

            self.send_json({
                "ok": True,
                "message": msg,
                "synced": synced_files
            })
        except Exception as e:
            print(f"  ✗ [Lỗi lưu file]: {e}")
            self.send_json({"ok": False, "error": str(e)}, status=500)

    def auto_sync_artifacts(self, target_file: Path, data: dict) -> list[str]:
        """Tự động đồng bộ các tệp liên quan khi annotation được cập nhật."""
        synced = []
        stem = target_file.name
        for sfx in [".annotation.json", ".json"]:
            if stem.endswith(sfx):
                stem = stem[:-len(sfx)]
                break

        parent_dir = target_file.parent

        # 1. Tự động vẽ lại ảnh preview regions overlay (<scene>_regions.png)
        possible_imgs = [parent_dir / f"{stem}.png", parent_dir / f"{stem}.jpg", parent_dir / f"{stem}.jpeg"]
        img_path = next((p for p in possible_imgs if p.exists()), None)
        if img_path:
            out_regions = parent_dir / f"{stem}_regions.png"
            venv_py = REPO_ROOT / ".venv/bin/python"
            py_bin = str(venv_py) if venv_py.exists() else sys.executable
            res = subprocess.run([
                py_bin,
                str(REPO_ROOT / "scripts/render_annotation_preview.py"),
                str(img_path),
                str(target_file),
                str(out_regions)
            ], capture_output=True, text=True)
            if res.returncode == 0:
                synced.append(out_regions.name)
                print(f"    ↳ [Auto-Sync Overlay]: Đã làm mới {out_regions.name}")
            else:
                print(f"    ✗ [Auto-Sync Overlay Thất bại]: {res.stderr[:200]}")

        # 2. Tự động đồng bộ phụ đề ASS chuẩn thẩm mỹ
        project_dir = parent_dir.parent if parent_dir.name == "images" else parent_dir
        srt_candidates = [
            parent_dir / f"{stem}.srt",
            project_dir / "input.srt",
            project_dir / "subtitle_draft.srt"
        ]
        for srt_f in srt_candidates:
            if srt_f.exists() and subtitle_styler is not None:
                ass_f = srt_f.with_suffix(".ass")
                try:
                    cfg = subtitle_styler.load_subtitle_config(project_dir)
                    subtitle_styler.compile_srt_to_ass(srt_f, ass_f, config=cfg)
                    synced.append(ass_f.name)
                    print(f"    ↳ [Auto-Sync Subtitle]: Đã biên dịch lại {ass_f.name}")
                except Exception as ex:
                    print(f"    ✗ [Auto-Sync Subtitle Thất bại]: {ex}")
                break

        return synced

    def send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description="Server xem trước & lưu trực tiếp Whiteboard Animation")
    parser.add_argument("--port", type=int, default=8000, help="Cổng server (mặc định 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự động mở trình duyệt")
    args = parser.parse_args()

    port = args.port
    # Thử bind port, nếu bận thì tăng dần
    for p in range(port, port + 20):
        try:
            server = socketserver.TCPServer(("", p), WhiteboardPreviewHandler)
            port = p
            break
        except OSError:
            continue
    else:
        print("[Lỗi] Không tìm được cổng khả dụng từ 8000-8020")
        sys.exit(1)

    url = f"http://localhost:{port}/assets/preview.html"
    print("=" * 65)
    print("MÁY CHỦ XEM TRƯỚC WHITEBOARD ANIMATION (HỖ TRỢ LƯU TRỰC TIẾP)")
    print("=" * 65)
    print(f"  🌐 URL Preview: {url}")
    print("  💾 Chế độ lưu: Ghi đĩa trực tiếp 100% (không cần tải file về)")
    print("  Nhấn Ctrl + C để dừng máy chủ.")
    print("=" * 65)

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã tắt máy chủ.")
        server.server_close()


if __name__ == "__main__":
    main()
