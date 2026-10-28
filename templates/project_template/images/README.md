# HƯỚNG DẪN CHUẨN BỊ ẢNH NGUỒN CHO DỰ ÁN
## (Source Images Guidelines for Whiteboard Animation)

Thư mục này dùng để chứa các hình ảnh minh hoạ gốc tĩnh cho từng scene của dự án.

### 1. Quy chuẩn kỹ thuật ảnh:
- **Tỉ lệ khung hình (Aspect Ratio)**: Bắt buộc là `16:9` (ngang).
- **Độ phân giải khuyến nghị**: `1920x1080` (Full HD), `1376x768`, hoặc `2560x1440` (2K).
- **Màu nền**: Màu trắng đồng nhất (`#FFFFFF`). Tránh các nền có hoa văn giấy vẽ, đổ bóng loang lổ.
- **Quy tắc nét vẽ & khoảng cách**:
  - Các chữ cái, icon, nhãn và hộp thoại cần có khoảng cách hở tối thiểu `25 - 30px`.
  - Không vẽ nét chữ đè chồng lên hình vẽ hoặc mũi tên đâm xuyên qua chữ.
  - Phù hợp với phong cách nét vẽ 2D doodle / line-art / marker pen.

### 2. Quy tắc đặt tên file ảnh:
Hãy đặt tên file ảnh theo tiền tố số thứ tự scene để pipeline tự động nhận diện:
- `scene_01.png` (hoặc `scene_01.jpg`)
- `scene_02.png` (hoặc `scene_02.jpg`)
- `scene_03.png` (hoặc `scene_03.jpg`)
- ...
- `scene_XX.png`
