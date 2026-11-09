#!/usr/bin/env python3
"""
AI Scene Image Generator
Tạo ảnh minh họa Whiteboard Animation 16:9 bằng Gemini Image Models
tuân thủ quy chuẩn Whiteboard Master Prompt Scene Generator v2.1.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np


def get_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip("'\"")
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong môi trường hoặc file .env!")


def generate_image(prompt: str, output_path: str | Path, model: str = "gemini-2.5-flash-image") -> Path:
    api_key = get_gemini_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "imageConfig": {
                "aspectRatio": "16:9"
            }
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    print(f"🎨 Đang gửi prompt tới Gemini Image Model ({model})...")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    candidates = res.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"Gemini API không trả về candidate nào: {res}")

    parts = candidates[0].get("content", {}).get("parts", [])
    image_bytes = None
    for p in parts:
        if "inlineData" in p and "data" in p["inlineData"]:
            image_bytes = base64.b64decode(p["inlineData"]["data"])
            break

    if not image_bytes:
        raise RuntimeError(f"Không tìm thấy dữ liệu ảnh inlineData trong phản hồi: {res}")

    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    # Decode ảnh bằng OpenCV
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("Không thể decode byte ảnh OpenCV!")

    h, w = img.shape[:2]
    print(f"📐 Ảnh gốc nhận được: {w}x{h}")

    # Đảm bảo canvas chuẩn 1920x1080 16:9 với nền #FFFFFF
    target_w, target_h = 1920, 1080
    if w != target_w or h != target_h:
        # Scale giữ nguyên tỷ lệ và đặt lên nền trắng 1920x1080
        scale = min(target_w / w, target_h / h)
        nw, nh = int(round(w * scale)), int(round(h * scale))
        resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

        canvas = np.full((target_h, target_w, 3), 255, dtype=np.uint8)
        # Căn giữa theo chiều ngang, đặt sát trên để bảo vệ Subtitle Safe Zone ở dưới
        ox = (target_w - nw) // 2
        oy = 0 if nh < target_h else (target_h - nh) // 2
        canvas[oy:oy + nh, ox:ox + nw] = resized
        final_img = canvas
    else:
        final_img = img

    cv2.imwrite(str(out_p), final_img)
    print(f"✅ Đã lưu ảnh đạt chuẩn 16:9 1920x1080: {out_p}")
    return out_p


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo ảnh AI cho Whiteboard Animation")
    parser.add_argument("--prompt-file", "-f", help="File chứa prompt")
    parser.add_argument("--prompt", "-p", help="Nội dung prompt trực tiếp")
    parser.add_argument("--output", "-o", required=True, help="Đường dẫn file ảnh xuất (.png)")
    parser.add_argument("--model", "-m", default="gemini-2.5-flash-image", help="Model tạo ảnh")

    args = parser.parse_args()
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.prompt:
        prompt_text = args.prompt
    else:
        print("Lỗi: Cần cung cấp --prompt hoặc --prompt-file", file=sys.stderr)
        sys.exit(1)

    generate_image(prompt_text, args.output, model=args.model)
