from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

fonts_map = {
    "be_vietnam_pro": {
        "name": "Be Vietnam Pro Bold",
        "path": REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf",
        "desc": "Chuẩn mực font tiếng Việt quốc tế: Dấu thanh thoát, nét dày đầm, dễ đọc nhất"
    },
    "lexend": {
        "name": "Lexend Bold",
        "path": REPO_ROOT / "assets/fonts/Lexend-Bold.ttf",
        "desc": "Font giáo dục của Google: Thiết kế tối ưu hóa tốc độ đọc và khả năng ghi nhớ"
    },
    "montserrat": {
        "name": "Montserrat Bold",
        "path": REPO_ROOT / "assets/fonts/Montserrat-Bold.ttf",
        "desc": "Hình học hiện đại, phong cách mạnh mẽ, chuẩn quốc tế"
    },
    "quicksand": {
        "name": "Quicksand Bold",
        "path": REPO_ROOT / "assets/fonts/Quicksand-Bold.ttf",
        "desc": "Bo góc tròn thân thiện, hài hòa tự nhiên với nét vẽ tay bảng trắng"
    },
    "nunito_sans": {
        "name": "Nunito Sans SemiBold",
        "path": REPO_ROOT / "assets/fonts/NunitoSans-SemiBold.ttf",
        "desc": "Font đang dùng hiện tại"
    }
}

sample_text = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

# Let's test fit-to-content capsule at sizes 50, 54, 58
print("Testing font metrics for Fit-to-Content Capsule:")
for fkey, finfo in fonts_map.items():
    print(f"\n--- {finfo['name']} ---")
    for sz in [50, 54, 58]:
        font = ImageFont.truetype(str(finfo['path']), sz)
        bbox = font.getbbox(sample_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pad_x = 48
        cap_w = tw + pad_x * 2
        print(f"  Size {sz}pt: text_w={tw}px, cap_w={cap_w}px, text_h={th}px | Margin left/right={(1920-cap_w)//2}px")
