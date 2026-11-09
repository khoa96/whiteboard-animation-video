from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_IMG_PATH = REPO_ROOT / "projects/WB-TEST-CASE-10/images/scene_01.png"
OUTPUT_DIR = Path("/Users/nguyendangkhoa/.gemini/antigravity/brain/e545d7f6-54bd-4bab-b5ea-adab52c82053")

# Load base image with hand drawing
base_img = Image.open(BASE_IMG_PATH).convert("RGBA")

# 1. TEST OPTION 4 (WARM IVORY) AT 75% OPACITY VS OPTION 1 (DARK SLATE) AT 75% OPACITY
# Both using Fit-to-Content Capsule (Padding 44px) and larger, bolder typography!

fonts_config = [
    {
        "id": "be_vietnam_pro",
        "name": "Be Vietnam Pro Bold",
        "path": REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf",
        "tag": "ĐỀ XUẤT SỐ 1: BE VIETNAM PRO BOLD",
        "desc": "Font tối ưu tiếng Việt & Anh hàng đầu: X-height cao, nét đầm chắc, dấu thanh thoát tuyệt đối"
    },
    {
        "id": "lexend",
        "name": "Lexend Bold",
        "path": REPO_ROOT / "assets/fonts/Lexend-Bold.ttf",
        "tag": "ĐỀ XUẤT SỐ 2: LEXEND BOLD (GOOGLE EDUCATION)",
        "desc": "Font chuẩn giáo dục quốc tế của Google: Nghiên cứu giúp tăng tốc độ đọc hiểu cho học viên"
    },
    {
        "id": "montserrat",
        "name": "Montserrat Bold",
        "path": REPO_ROOT / "assets/fonts/Montserrat-Bold.ttf",
        "tag": "ĐỀ XUẤT SỐ 3: MONTSERRAT BOLD",
        "desc": "Hình học hiện đại, chữ cứng cáp, phong cách tài liệu giáo dục phương Tây"
    },
    {
        "id": "quicksand",
        "name": "Quicksand Bold",
        "path": REPO_ROOT / "assets/fonts/Quicksand-Bold.ttf",
        "tag": "ĐỀ XUẤT SỐ 4: QUICKSAND BOLD",
        "desc": "Đầu nét bo tròn mềm mại, đồng điệu tự nhiên với nét vẽ tay hoạt họa bảng trắng"
    }
]

# We will create:
# 1) Image: "showcase_fit_and_opacity_75.png" (comparing Option 1 at 75% vs Option 4 at 75% on actual video scene)
# 2) Image: "showcase_font_options_large.png" (comparing the 4 fonts at larger size with fit-to-content)

sample_text = "A/AN chỉ vật chung chung, THE chỉ vật cụ thể, và water không cần mạo từ."

# Function to render a scene overlay with hand visible behind
def render_scene_overlay(theme, font_path, font_size, text, output_file):
    canvas = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    font = ImageFont.truetype(str(font_path), font_size)
    tag_font = ImageFont.truetype(str(REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf"), 22)
    
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # FIT TO CONTENT CAPSULE:
    # Padding left/right = 48px, Padding top/bottom = 18px
    pad_x = 48
    pad_y = 18
    cw = tw + pad_x * 2
    ch = th + pad_y * 2
    cx1 = (1920 - cw) // 2
    cy1 = 980 - ch // 2
    cx2 = cx1 + cw
    cy2 = cy1 + ch
    cr = 22
    
    # Shadow
    odraw.rounded_rectangle([cx1, cy1 + 4, cx2, cy2 + 4], radius=cr, fill=(0, 0, 0, 30))
    
    # Capsule Background with Opacity
    odraw.rounded_rectangle(
        [cx1, cy1, cx2, cy2],
        radius=cr,
        fill=theme["bg_color"],
        outline=theme["border_color"],
        width=int(theme.get("border_width", 2))
    )
    
    # Draw text centered inside capsule
    tx = (1920 - tw) // 2
    ty = cy1 + (ch - th) // 2 - 3
    
    # Render words with accent color
    words = text.split(" ")
    curr_x = tx
    for wd in words:
        wb = font.getbbox(wd + " ")
        ww = wb[2] - wb[0]
        clean_wd = wd.strip(".,;:?!")
        col = theme["accent_color"] if clean_wd in ["A/AN", "THE", "water"] else theme["text_color"]
        odraw.text((curr_x, ty), wd + " ", font=font, fill=col)
        curr_x += ww
        
    # Top info badge
    tag_text = f"{theme['tag']} | Font: {font_path.stem} ({font_size}pt) | Width: {cw}px (FIT CONTENT)"
    tb = tag_font.getbbox(tag_text)
    odraw.rounded_rectangle([40, 40, 60 + (tb[2]-tb[0]), 80], radius=8, fill=(15, 23, 42, 230))
    odraw.text((50, 48), tag_text, font=tag_font, fill=(255, 255, 255))
    
    final_img = Image.alpha_composite(canvas, overlay)
    final_img.convert("RGB").save(output_file, quality=95)
    print(f"Saved: {output_file.name}")

# Theme Option 1 (75% Opacity Dark Slate)
theme_opt1_75 = {
    "tag": "OPTION 1: DARK SLATE (75% OPACITY)",
    "bg_color": (20, 23, 31, 191),        # 75% of 255 = 191
    "border_color": (51, 65, 85, 210),
    "border_width": 2,
    "text_color": (255, 255, 255),
    "accent_color": (245, 166, 35)
}

# Theme Option 4 (75% Opacity Warm Ivory)
theme_opt4_75 = {
    "tag": "OPTION 4: WARM IVORY (75% OPACITY)",
    "bg_color": (254, 243, 199, 191),     # Amber-100 with 75% opacity
    "border_color": (252, 211, 77, 230),   # Amber-300
    "border_width": 2,
    "text_color": (41, 37, 36),            # Stone-900
    "accent_color": (234, 88, 12)          # Terracotta
}

# Render Option 1 (75%) with Be Vietnam Pro
render_scene_overlay(
    theme_opt1_75, 
    REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf", 
    44, 
    sample_text, 
    OUTPUT_DIR / "preview_opt1_dark_slate_75_fit.png"
)

# Render Option 4 (75%) with Be Vietnam Pro
render_scene_overlay(
    theme_opt4_75, 
    REPO_ROOT / "assets/fonts/BeVietnamPro-Bold.ttf", 
    44, 
    sample_text, 
    OUTPUT_DIR / "preview_opt4_warm_ivory_75_fit.png"
)

# Render with Lexend Bold
render_scene_overlay(
    theme_opt1_75, 
    REPO_ROOT / "assets/fonts/Lexend-Bold.ttf", 
    44, 
    sample_text, 
    OUTPUT_DIR / "preview_opt1_lexend_75_fit.png"
)

# Render with Quicksand Bold
render_scene_overlay(
    theme_opt1_75, 
    REPO_ROOT / "assets/fonts/Quicksand-Bold.ttf", 
    46, 
    sample_text, 
    OUTPUT_DIR / "preview_opt1_quicksand_75_fit.png"
)

# Render with Montserrat Bold
render_scene_overlay(
    theme_opt1_75, 
    REPO_ROOT / "assets/fonts/Montserrat-Bold.ttf", 
    42, 
    sample_text, 
    OUTPUT_DIR / "preview_opt1_montserrat_75_fit.png"
)

print("All single scene renders generated.")
