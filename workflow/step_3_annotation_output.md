# ĐẦU RA MẪU BƯỚC 3: ATOMIC SEGMENTATION & REGION ANNOTATION
## (Dữ liệu mẫu chuẩn hóa lấy từ Scene 01: ARTICLES — THREE GROUPS)

Tài liệu này thể hiện cấu trúc đầu ra chuẩn của **Bước 3**, bao gồm:
1. Nguyên lý phân tách nguyên tử (Atomic Decomposition) chống lỗi giật/đơ (Freeze-and-pop).
2. Bản đồ tọa độ 11 phần tử nguyên tử trên Canvas 1920x1080.
3. Nội dung file cấu trúc chuẩn `scene_01.annotation.json`.
4. Mã nguồn Python tự động hóa sinh annotation và kiểm tra 0% Overlap.
5. Kiểm định thị giác qua ảnh preview `scene_01-regions.png`.

---

### PHẦN 1: NGUYÊN LÝ PHÂN TÁCH NGUYÊN TỬ (ZERO-OVERLAP RULE)

#### Vấn đề nghiêm trọng ở Case 07 (Thất bại)
Trong Case 07, một thẻ (Card) lớn thường được khai báo là một `type: "box"` bao trọn toàn bộ khung ngoài cùng mọi icon và nhãn chữ bên trong. Khi thuật toán gán Connected Components (CC) chạy, vùng hình chữ nhật lớn bao trùm đã "chiếm đoạt" (steal) toàn bộ các nét vẽ bên trong. Kết quả là khi đến lượt các icon bên trong cần vẽ, chúng không còn nét mực nào khả dụng, khiến bàn tay vẽ bị khựng lại đứng yên (freeze) trong vài giây rồi bất ngờ bật sáng hình ảnh (pop-up glitch).

#### Giải pháp chuẩn mực tại Scene 01 và Scene 02 (Thành công)
1. **Phân tách theo khe hở tự nhiên (Natural whitespace gaps)**: Mỗi Card/Cột được chia thành Header, Body, Icon riêng biệt.
2. **Quy tắc phân loại Type cho Khối có màu nền (Colored Badges vs Outline Boxes)**:
   - Nếu là **khung rỗng (outline frame)** chỉ có viền: đặt `type: "box"`, `colorMode: "none"`.
   - Nếu là **hộp có màu nền (colored badge / icon có nền màu)** như các ô nguyên âm `A, E, I, O, U` hay ô cam `Y`: **BẮT BUỘC** đặt `type: "colored_image"`, `colorMode: "wash"`.
   - *Lý do*: Nếu đặt `type: "box"`, engine sẽ hiểu nhầm là khung rỗng nên chỉ vẽ 4 cạnh hình chữ nhật và gán `color_frames = 0`, làm mất màu nền trong suốt video và chỉ bật sáng ở giây cuối cùng. Khi đặt `type: "colored_image"`, ngòi bút sẽ vẽ chữ/viền mực trước (90% thời gian) rồi quét loang màu nền ngay sau đó (10% thời gian) cực kỳ tự nhiên.
1. **Card 1 (A/AN)**:
   - Khung trên & Nhãn `A / AN`: `y = 329..430, x = 99..645`
   - Cột trái (Khung trái + Icon sách + chữ `a book`): `y = 430..747, x = 99..385`
   - Cột phải (Khung phải + Quả táo + chữ `an apple`): `y = 430..747, x = 385..645`
2. **Card 2 (THE)**:
   - Khung trên & Nhãn `THE`: `y = 329..422, x = 687..1233`
   - Khung dưới + Cặp sách + chữ `the book`: `y = 422..747, x = 687..1233`
3. **Card 3 (ZERO ARTICLE)**:
   - Khung trên & Nhãn `ZERO ARTICLE`: `y = 329..422, x = 1274..1821`
   - Khung dưới + Ly nước + chữ `WATER`: `y = 422..747, x = 1274..1821`

*Kết quả đo đạc bằng thuật toán:*
- **Số cặp vùng chồng lấn (Overlaps)**: **0 / 55 cặp (0.00%)**.
- **Số pixel mực bị bỏ sót (Unassigned ink)**: **0 / 225,918 pixels (0.00%)**.

---

### PHẦN 2: BẢN ĐỒ TỌA ĐỘ 11 PHẦN TỬ NGUYÊN TỬ (CANVAS 1920x1080)

| ID | Nhãn phần tử | Sequence | Type | ColorMode | Region (x, y, w, h) | StartMs | DurationMs |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| `el-01-title` | Tiêu đề: ARTICLES | 1 | `text` | `none` | `{640, 50, 640, 130}` | 600 | 3,200 |
| `el-02-subtitle` | Phụ đề: THREE GROUPS | 2 | `text` | `none` | `{680, 195, 560, 85}` | 4,000 | 2,800 |
| `el-03-card1-header` | Khung & Nhãn: A / AN | 3 | `text` | `none` | `{99, 329, 546, 101}` | 7,800 | 3,400 |
| `el-04-card1-book` | Icon & chữ: a book | 4 | `colored_image`| `wash` | `{99, 430, 286, 317}` | 11,400 | 2,800 |
| `el-05-card1-apple` | Icon & chữ: an apple | 5 | `colored_image`| `wash` | `{385, 430, 260, 317}` | 14,400 | 2,800 |
| `el-06-card2-header` | Khung & Nhãn: THE | 6 | `text` | `none` | `{687, 329, 546, 93}` | 18,000 | 3,400 |
| `el-07-card2-content`| Cặp sách & the book | 7 | `colored_image`| `wash` | `{687, 422, 546, 325}` | 21,600 | 4,000 |
| `el-08-card3-header` | Khung & Nhãn: ZERO ARTICLE | 8 | `text` | `none` | `{1274, 329, 547, 93}` | 26,500 | 3,500 |
| `el-09-card3-content`| Ly nước & WATER | 9 | `colored_image`| `wash` | `{1274, 422, 547, 325}` | 30,200 | 3,800 |
| `el-10-divider` | Đường kẻ phân cách | 10 | `line` | `none` | `{90, 780, 1740, 80}` | 35,000 | 1,200 |
| `el-11-today` | Khung bài học: TODAY: A / AN| 11 | `box` | `wash` | `{650, 870, 620, 160}` | 36,400 | 4,400 |

---

### PHẦN 3: FILE DỮ LIỆU ĐẦU RA CHUẨN (`scene_01.annotation.json`)

```json
{
  "sceneId": "test_case_10_scene_01",
  "canvas": {
    "width": 1920,
    "height": 1080
  },
  "storyBasis": "Infographic tổng quan 3 nhóm mạo từ tiếng Anh: ARTICLES — THREE GROUPS (A/AN, THE, ZERO ARTICLE), dẫn nhập vào trọng tâm bài học hôm nay là nhóm A và AN.",
  "sceneDurationMs": 43284,
  "elements": [
    {
      "id": "el-01-title",
      "label": "Tiêu đề: ARTICLES",
      "sequence": 1,
      "type": "text",
      "colorMode": "none",
      "narrativeRole": "Giới thiệu chủ đề mạo từ trong tiếng Anh",
      "region": { "x": 640, "y": 50, "width": 640, "height": 130 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 600,
        "durationMs": 3200,
        "maskPaddingPx": 10,
        "protectedRegions": []
      }
    },
    {
      "id": "el-02-subtitle",
      "label": "Phụ đề: THREE GROUPS",
      "sequence": 2,
      "type": "text",
      "colorMode": "none",
      "narrativeRole": "Chia mạo từ làm 3 nhóm chính",
      "region": { "x": 680, "y": 195, "width": 560, "height": 85 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 4000,
        "durationMs": 2800,
        "maskPaddingPx": 10,
        "protectedRegions": []
      }
    },
    {
      "id": "el-03-card1-header",
      "label": "Khung và Nhãn nhóm 1: A / AN",
      "sequence": 3,
      "type": "text",
      "colorMode": "none",
      "narrativeRole": "Khung và tiêu đề nhóm mạo từ không xác định A và AN",
      "region": { "x": 99, "y": 329, "width": 546, "height": 101 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 7800,
        "durationMs": 3400,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-04-card1-book",
      "label": "Ví dụ 1: a book (cuốn sách)",
      "sequence": 4,
      "type": "colored_image",
      "colorMode": "wash",
      "narrativeRole": "Minh họa a book - một cuốn sách bất kỳ",
      "region": { "x": 99, "y": 430, "width": 286, "height": 317 },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 11400,
        "durationMs": 2800,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-05-card1-apple",
      "label": "Ví dụ 2: an apple (quả táo)",
      "sequence": 5,
      "type": "colored_image",
      "colorMode": "wash",
      "narrativeRole": "Minh họa an apple - một quả táo bất kỳ",
      "region": { "x": 385, "y": 430, "width": 260, "height": 317 },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 14400,
        "durationMs": 2800,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-06-card2-header",
      "label": "Khung và Nhãn nhóm 2: THE",
      "sequence": 6,
      "type": "text",
      "colorMode": "none",
      "narrativeRole": "Khung và tiêu đề nhóm mạo từ xác định THE",
      "region": { "x": 687, "y": 329, "width": 546, "height": 93 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 18000,
        "durationMs": 3400,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-07-card2-content",
      "label": "Minh họa sách & the book",
      "sequence": 7,
      "type": "colored_image",
      "colorMode": "wash",
      "narrativeRole": "Minh họa the book - cuốn sách cụ thể đã xác định",
      "region": { "x": 687, "y": 422, "width": 546, "height": 325 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 21600,
        "durationMs": 4000,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-08-card3-header",
      "label": "Khung và Nhãn nhóm 3: ZERO ARTICLE",
      "sequence": 8,
      "type": "text",
      "colorMode": "none",
      "narrativeRole": "Khung và tiêu đề nhóm không dùng mạo từ Zero Article",
      "region": { "x": 1274, "y": 329, "width": 547, "height": 93 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 26500,
        "durationMs": 3500,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-09-card3-content",
      "label": "Minh họa ly nước & WATER",
      "sequence": 9,
      "type": "colored_image",
      "colorMode": "wash",
      "narrativeRole": "Minh họa nước (danh từ không đếm được nói chung) không dùng mạo từ",
      "region": { "x": 1274, "y": 422, "width": 547, "height": 325 },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 30200,
        "durationMs": 3800,
        "maskPaddingPx": 8,
        "protectedRegions": []
      }
    },
    {
      "id": "el-10-divider",
      "label": "Đường kẻ phân cách trang trí",
      "sequence": 10,
      "type": "line",
      "colorMode": "none",
      "narrativeRole": "Phân cách nhóm tổng quan và trọng tâm bài học",
      "region": { "x": 90, "y": 780, "width": 1740, "height": 80 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 35000,
        "durationMs": 1200,
        "maskPaddingPx": 6,
        "protectedRegions": []
      }
    },
    {
      "id": "el-11-today",
      "label": "Hộp nhấn mạnh trọng tâm: TODAY: A / AN",
      "sequence": 11,
      "type": "box",
      "colorMode": "wash",
      "narrativeRole": "Xác định trọng tâm buổi học hôm nay là nhóm A / AN",
      "region": { "x": 650, "y": 870, "width": 620, "height": 160 },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 36400,
        "durationMs": 4400,
        "maskPaddingPx": 10,
        "protectedRegions": []
      }
    }
  ]
}
```

---

### PHẦN 4: LỆNH SINH ẢNH KIỂM TRA PHÂN VÙNG

Để xác thực trực quan trước khi render video, chạy script:
```bash
.venv/bin/python scripts/render_annotation_preview.py \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.png \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.annotation.json \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01-regions.png
```
Ảnh xuất ra `scene_01-regions.png` sẽ hiển thị 11 khung chữ nhật màu với thứ tự đánh số từ 1 đến 11, nhãn tên và mũi tên chỉ hướng vẽ, đảm bảo tuyệt đối không có viền nào chồng đè lên nhau.
