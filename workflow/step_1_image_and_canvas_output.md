# ĐẦU RA MẪU BƯỚC 1: IMAGE PROMPT & CANVAS STANDARDIZATION
## (Dữ liệu mẫu chuẩn hóa lấy từ Scene 01: ARTICLES — THREE GROUPS)

Tài liệu này thể hiện cấu trúc đầu ra chuẩn của **Bước 1**, bao gồm:
1. Cấu trúc Prompt tạo ảnh AI chi tiết cho Scene 01.
2. Quy trình tiền xử lý kỹ thuật (Image Preprocessing & Normalization).
3. Mã nguồn Python chuẩn hóa Canvas về chuẩn 1920x1080 `#FFFFFF`.
4. Đặc tả kỹ thuật của file ảnh đầu ra sẵn sàng cho Engine phân rã.

---

### PHẦN 1: PROMPT TẠO ẢNH AI CHO SCENE 01

Prompt được thiết kế bằng tiếng Anh theo cấu trúc 4 Zone với các ràng buộc nghiêm ngặt nhằm tạo ra tệp đồ họa thông tin hoàn hảo cho hoạt họa bảng trắng:

```text
Create ONE finished 16:9 landscape educational whiteboard infographic about English articles. This is a static source image for a hand-drawn animation pipeline, not a storyboard and not a video frame sequence.

Style and canvas: pure white background (#FFFFFF), flat 2D hand-drawn marker illustration, clean black outlines, friendly simple icons, bright but controlled blue, orange, and green accents. Natural, traceable linework. Large, highly legible English lettering. No 3D, no photorealism, no teacher character, no hands, no pen, no shadows, no gradients, no paper texture, no border, no watermark.

Layout: four clearly separated horizontal zones with generous white space. Keep every icon, word, arrow, and frame independent. Do not let any arrow cross text or illustrations.

ZONE 1 — TITLE: At the top center, write exactly: “ARTICLES”. Directly beneath it, write exactly: “THREE GROUPS”.

ZONE 2 — THREE ARTICLE GROUPS: Arrange three equal, separate cards in one horizontal row.
- Card 1: write “A / AN”. Under the label, draw one simple book and one simple apple. Under the icons, write exactly “a book” and “an apple”. Use a blue accent.
- Card 2: write “THE”. Draw two similar books, with one book clearly highlighted as the specific book being referred to. Under the illustration, write exactly “the book”. Use a green accent.
- Card 3: write “ZERO ARTICLE”. Draw a simple glass of water with a water droplet. Under the illustration, write exactly “WATER”. Use an orange accent. This is only a brief preview of the category, not a detailed grammar explanation.

ZONE 3 — READING ORDER: Below the three cards, draw one simple, centered horizontal connector or guide line that visually groups the three categories. It must not touch the cards or text.

ZONE 4 — TODAY’S LESSON: At the bottom center, draw a clean blue outline around the words “TODAY: A / AN”. This is the only emphasized text in the bottom zone. Do not add any other words.

Strict text control: Render only these exact text strings: “ARTICLES”, “THREE GROUPS”, “A / AN”, “a book”, “an apple”, “THE”, “the book”, “ZERO ARTICLE”, “WATER”, “TODAY: A / AN”. Spell them exactly. No Vietnamese text, no additional captions, no invented words or letters.

Segmentation requirements: Each of the three category cards, every icon, each text label, the connector, and the bottom emphasis frame must have clear boundaries and enough spacing for separate object detection and stroke extraction. Keep the three cards balanced and the reading order obvious from left to right.

Negative constraints: no extra articles, no sentences, no decorative doodles, no crowded arrangement, no overlapping lines, no object touching the canvas edges. Generate one polished static whiteboard infographic only.
```

---

### PHẦN 2: QUY TRÌNH TIỀN XỬ LÝ ẢNH (CANVAS STANDARDIZATION)

Ảnh sau khi sinh ra từ AI (ngay cả khi đạt 2K hoặc 4K) thường có các vấn đề kỹ thuật sau:
1. **Sai lệch màu nền**: Nền AI sinh ra thường có giá trị màu ngà, xám nhạt (`#F8F9FA` hoặc `#FCFCFC`) thay vì trắng tuyệt đối. Nếu không xử lý, khi đưa vào engine hoạt hoạ sẽ xuất hiện vết ố loang lổ.
2. **Kích thước không chuẩn Full HD**: Tỷ lệ có thể bị lệch 1-2 pixel khiến quá trình render video 60 fps bị co giãn méo nét.
3. **Viền đen hoặc viền mờ sát cạnh**: Do AI tự sinh viền bo viền cạnh màn hình.

#### Mã nguồn Python chuẩn hóa Canvas (`standardize_canvas.py`):
```python
import cv2
import numpy as np
from PIL import Image

def standardize_whiteboard_image(input_path: str, output_path: str):
    # 1. Đọc ảnh gốc độ phân giải cao
    img = Image.open(input_path).convert("RGB")
    
    # 2. Resize chuẩn xác về Full HD 1920x1080 bằng bộ lọc Lanczos chất lượng cao
    img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    arr = np.array(img_resized)
    
    # 3. Chuyển sang ảnh xám để phân tích ngưỡng nền
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    
    # 4. Ngưỡng trắng chuẩn: Mọi pixel có độ sáng > 248 được đưa về #FFFFFF tuyệt đối (255, 255, 255)
    bg_mask = gray >= 248
    arr[bg_mask] = [255, 255, 255]
    
    # 5. Loại bỏ viền sát cạnh (4 cạnh biên 5px đưa về trắng tuyệt đối)
    arr[:5, :, :] = [255, 255, 255]
    arr[-5:, :, :] = [255, 255, 255]
    arr[:, :5, :] = [255, 255, 255]
    arr[:, -5:, :] = [255, 255, 255]
    
    # 6. Lưu file hoàn thiện
    out_img = Image.fromarray(arr)
    out_img.save(output_path, "PNG", optimize=True)
    print(f"✓ Đã chuẩn hóa thành công: {output_path} (1920x1080, #FFFFFF)")

if __name__ == "__main__":
    standardize_whiteboard_image(
        "images/Infographic_about_English_articles_2K_20261023171450.jpg",
        "scene_01.png"
    )
```

---

### PHẦN 3: ĐẶC TẢ KỸ THUẬT TỆP ĐẦU RA MẪU

* **Tên tệp**: `scene_01.png`
* **Vị trí lưu trữ**: `assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.png`
* **Định dạng**: PNG không nén suy hao (Lossless PNG)
* **Kích thước**: `1920 x 1080 pixels` (Tỷ lệ 16:9)
* **Không gian màu**: sRGB
* **Màu nền**: `#FFFFFF` (RGB: `255, 255, 255`) tuyệt đối
* **Tổng số Connected Components mực**: 110 thành phần nét
* **Sự phân bố nội dung thị giác**:
  - `Zone 1 (Title)`: `y = 64..270`, `x = 660..1260` (Chữ ARTICLES và THREE GROUPS).
  - `Zone 2 (Cards)`: `y = 329..747`, `x = 99..1821` (3 thẻ cân đối: A/AN, THE, ZERO ARTICLE).
  - `Zone 3 (Divider)`: `y = 786..846`, `x = 97..1813` (Đường kẻ ngang phân cách).
  - `Zone 4 (Focus Badge)`: `y = 874..1023`, `x = 660..1260` (Hộp đóng khung TODAY: A / AN).
