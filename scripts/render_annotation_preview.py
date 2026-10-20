import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _find_font(prefer_cjk: bool = False) -> str | None:
    candidates = []
    if sys.platform == "darwin":  # macOS
        if prefer_cjk:
            candidates.extend([
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
            ])
        candidates.extend([
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ])
    elif sys.platform == "win32":  # Windows
        if prefer_cjk:
            candidates.append("C:/Windows/Fonts/msyh.ttc")
        candidates.extend([
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ])
    else:  # Linux
        candidates.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ])

    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def main(image_path: str, annotation_path: str, output_path: str) -> None:
    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    data = json.loads(Path(annotation_path).read_text(encoding="utf-8"))
    labels = " ".join(element.get("label", "") for element in data.get("elements", []))
    has_cjk = any("\u4e00" <= c <= "\u9fff" for c in labels)
    font_path = _find_font(prefer_cjk=has_cjk)

    if font_path:
        font = ImageFont.truetype(font_path, 26)
        small_font = ImageFont.truetype(font_path, 16)
    else:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    colors = [
        (38, 103, 255, 225),   # Xanh dương
        (255, 105, 92, 225),   # Đỏ cam
        (41, 167, 102, 225),   # Xanh lá
        (181, 100, 255, 225),  # Tím
        (245, 158, 11, 225),   # Vàng hổ phách
    ]

    for index, element in enumerate(data.get("elements", []), start=1):
        region = element.get("region", {})
        x, y = region.get("x", 0), region.get("y", 0)
        right, bottom = x + region.get("width", 0), y + region.get("height", 0)
        color = colors[(index - 1) % len(colors)]
        fill = (*color[:3], 24)

        # Vẽ khung bao
        draw.rounded_rectangle((x, y, right, bottom), radius=10, outline=color, width=3, fill=fill)

        # Vẽ số thứ tự
        draw.ellipse((x + 6, y + 6, x + 38, y + 38), fill=color)
        draw.text((x + 22, y + 10), str(index), anchor="mt", font=small_font, fill="white")

        # Chuẩn bị nhãn
        el_type = element.get("type", "")
        el_label = element.get("label", "")
        dir_label = element.get("reveal", {}).get("direction", "")
        type_badge = f"[{el_type}] " if el_type else ""
        label_text = f"{index}. {type_badge}{el_label} ({dir_label})" if dir_label else f"{index}. {type_badge}{el_label}"

        # Vẽ nhãn nền trắng mờ
        text_w = len(label_text) * 11 + 20
        label_right = min(right - 6, x + 44 + text_w)
        draw.rounded_rectangle((x + 44, y + 6, label_right, y + 38), radius=6, fill=(255, 255, 255, 230))
        draw.text((x + 50, y + 11), label_text, font=small_font, fill=(20, 24, 33, 255))

        # Vẽ handPath hoặc vectorPath nếu có
        hand_path = element.get("handPath")
        if hand_path and "start" in hand_path and "end" in hand_path:
            start = tuple(hand_path["start"])
            end = tuple(hand_path["end"])
            draw.line((start, end), fill=color, width=3)
            draw.polygon((end, (end[0] - 10, end[1] - 5), (end[0] - 10, end[1] + 5)), fill=color)

    result = Image.alpha_composite(image, overlay).convert("RGB")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path, quality=95)


if __name__ == "__main__":
    main(*sys.argv[1:4])

