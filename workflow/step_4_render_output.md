# ĐẦU RA MẪU BƯỚC 4: WHITEBOARD STREAM ANIMATION RENDERING
## (Dữ liệu mẫu chuẩn hóa lấy từ Scene 01: ARTICLES — THREE GROUPS)

Tài liệu này thể hiện cấu trúc đầu ra chuẩn của **Bước 4**, bao gồm:
1. Lệnh thực thi Engine Render hoạt họa bảng trắng 60 fps.
2. Giải thích cơ chế thuật toán: Skeleton Ink Tracing, Contour-Wipe Coloring và Safe Mask.
3. Nhật ký Terminal thực tế khi render thành công Scene 01.
4. Đặc tả kỹ thuật file video hoạt hoạ gốc (`scene_01.mp4`).

---

### PHẦN 1: CÂU LỆNH RENDER ENGINE

Quá trình render hoạt họa được thực thi bằng Python trong môi trường ảo `.venv`:

```bash
.venv/bin/python scripts/render_stream_whiteboard.py \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.png \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.annotation.json \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4 \
  assets/drawing-hand.png \
  --canvas-hex "#FFFFFF"
```

#### Giải thích các tham số cốt lõi:
* `image`: Đường dẫn đến ảnh line-art tĩnh chuẩn hóa (`scene_01.png`).
* `annotation`: Đường dẫn đến file phân rã nguyên tử (`scene_01.annotation.json`).
* `output`: Tệp video MP4 xuất bản (`scene_01.mp4`).
* `hand`: Asset ảnh bàn tay cầm bút có kênh alpha trong suốt (`assets/drawing-hand.png`).
* `--canvas-hex "#FFFFFF"`: Ép nền canvas màu trắng tuyệt đối, chống ố màu nền.
* `--fps 60` (Mặc định 60 fps): Đảm bảo chuyển động của ngòi bút và cổ tay mượt mà như người thật đang vẽ.
* `--ink-path skeleton` (Mặc định): Thuật toán trích xuất xương đồ thị nét bút (Morphological Skeletonization) giúp nét vẽ đi tự nhiên dọc theo thân chữ và đường cong.
* `--color-fill contour-wipe` (Mặc định): Sau khi vẽ xong viền mực, màu sắc được quét lan tỏa theo đường đồng mức từ trong ra ngoài.

---

### PHẦN 2: CƠ CHẾ THUẬT TOÁN AN TOÀN (SAFE MASK ORCHESTRATION)

Để đảm bảo các nét vẽ sau không phá hủy hoặc làm thủng nét vẽ của phần tử trước:
1. **Trích xuất Connected Components (CC)**: Engine quét toàn bộ ảnh để nhóm các cụm pixel mực liền mạch.
2. **Gán CC vào Element tương ứng**: Mỗi CC được gán cho phần tử có diện tích bao phủ lớn nhất. Nhờ phân rã Zero-Overlap ở Bước 3, mỗi CC được gán chính xác 100%, không bị tranh chấp.
3. **Allowed Mask thông minh**:
   - Thay vì khoét cả hình chữ nhật của các phần tử sau (dễ làm đứt nét hoặc rách chữ), Engine chỉ trừ các pixel thực sự thuộc về nét mực của phần tử sau (được giãn nhẹ 2px).
   - Nhờ vậy, khoảng trắng hoặc đường biên không bao giờ khoét thủng nét vẽ của phần tử trước.

---

### PHẦN 3: NHẬT KÝ RENDER THỰC TẾ (TERMINAL LOGS)

```text
============================================================
Engine Render Bảng Trắng Whiteboard (Mask Orchestration + Stream Drawing)
============================================================
  • Ảnh đầu vào : assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.png
  • Độ phân giải : 1080x600, Tốc độ: 60 fps
  • Số vùng vẽ   : 11, Thời lượng: 43284ms
  • Thuật toán   : Nét bút=skeleton, Kiểu màu=contour-wipe, Chế độ màu=auto
  [Tiêu đề: ARTICLES] type=text ink=192f color=0f
  [Phụ đề: THREE GROUPS] type=text ink=168f color=0f
  [Khung và Nhãn nhóm 1: A / AN] type=text ink=204f color=0f
  [Ví dụ 1: a book (cuốn sách)] type=colored_image ink=151f color=17f
  [Ví dụ 2: an apple (quả táo)] type=colored_image ink=151f color=17f
  [Khung và Nhãn nhóm 2: THE] type=text ink=204f color=0f
  [Minh họa sách & the book] type=colored_image ink=216f color=24f
  [Khung và Nhãn nhóm 3: ZERO ARTICLE] type=text ink=210f color=0f
  [Minh họa ly nước & WATER] type=colored_image ink=205f color=23f
  [Đường kẻ phân cách trang trí] type=line ink=72f color=0f
  [Hộp nhấn mạnh trọng tâm: TODAY: A / AN] type=box ink=264f color=0f
  H.264 转码完成(ffmpeg): assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4

🎉 Video hoàn thành: assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4 (1.88 MB)
============================================================
OUTPUT=assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4
```

---

### PHẦN 4: ĐẶC TẢ KỸ THUẬT TỆP VIDEO ĐẦU RA

* **Tên tệp**: `scene_01.mp4`
* **Vị trí**: `assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4`
* **Thời lượng**: `43.284 giây` (tương đương 2,597 frames ở 60 fps).
* **Định dạng Video**: H.264 (High Profile), YUV420p.
* **Tốc độ khung hình (Frame Rate)**: `60.0 fps` hằng định (CFR).
* **Trạng thái âm thanh**: Silent (chưa ghép tiếng; âm thanh sẽ được ghép ở Bước 5).
* **Chuyển động bàn tay**:
  - Tự động hạ bút khi bắt đầu một vùng nét mực.
  - Tự động nhấc bút và bay lượn (hover trajectory) mượt mà giữa các nét rời rạc.
  - Tự động thu tay về góc dưới bên phải màn hình khi hoàn thành nét cuối cùng ở giây thứ `40.8`.
  - Giữ nguyên trạng thái bảng vẽ hoàn chỉnh trong 2.5 giây tĩnh cuối video.
