# HƯỚNG DẪN TỐI ƯU HÓA RENDER & TÁI SỬ DỤNG CHO CÁC DỰ ÁN
## (Whiteboard Animation Render Optimization & Project Portability Guide)

Tài liệu này tổng hợp các giải pháp kỹ thuật, thông số tối ưu hóa thời gian kết xuất (render time) và quy trình chuẩn để áp dụng cho bất kỳ dự án video bảng trắng nào trong tương lai.

---

## I. CƠ CHẾ 2 CHẾ ĐỘ RENDER (2-TIER RENDERING STRATEGY)

Thay vì luôn chạy chế độ phân giải cao và 60 fps ngay từ đầu, áp dụng chiến lược 2 tầng:

| Chế độ | Mục đích sử dụng | Thông số kỹ thuật | Thời gian render |
| :--- | :--- | :--- | :--- |
| **Tier 1: Fast Preview (Bản nháp nhanh)** | Căn chỉnh nhịp vẽ với giọng đọc, kiểm tra thứ tự nét bút, kiểm tra phụ đề | `--fps 30 --cap-long-edge 960` | **~8 – 12 giây / scene** (nhanh gấp 4 lần) |
| **Tier 2: Production Master (Bản phát hành cuối)** | Đóng gói video chất lượng cao nhất để xuất bản lên YouTube/LMS | `--fps 60 --cap-long-edge 1080` (hoặc 1920) | **~30 – 50 giây / scene** |

### Câu lệnh mẫu:

#### 1. Lệnh Render Bản Xem Nhanh (Draft Preview):
```bash
.venv/bin/python scripts/render_stream_whiteboard.py \
  scene_02.png scene_02.annotation.json preview.mp4 assets/drawing-hand.png \
  --fps 30 --cap-long-edge 960 --canvas-hex "#FFFFFF"
```

#### 2. Lệnh Render Bản Hoàn Thiện (Final Master):
```bash
.venv/bin/python scripts/render_stream_whiteboard.py \
  scene_02.png scene_02.annotation.json scene_02.mp4 assets/drawing-hand.png \
  --fps 60 --cap-long-edge 1080 --canvas-hex "#FFFFFF"
```

---

## II. DANH MỤC CÁC SỬA ĐỔI CỐT LÕI ĐÃ ĐƯỢC ĐÓNG GÓI VÀO ENGINE

Các thay đổi sau đã được áp dụng trực tiếp vào engine [scripts/render_stream_whiteboard.py](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/scripts/render_stream_whiteboard.py), đảm bảo **mọi scene và mọi dự án sau này đều tự động được bảo vệ**:

1. **Ưu tiên tuyệt đối cho `colorMode: "wash"` (Dòng 510–517)**:
   - Trước đây: `el_type in ["box", "text"]` ép `needs_color_wash = False`, khiến các ô/badge có màu nền bị rỗng ruột trong suốt video.
   - Hiện tại: `el_color_mode` được kiểm tra đầu tiên. Bất kỳ phần tử nào khai báo `"colorMode": "wash"` đều được cấp frame tô màu loang (`contour-wipe`), không bao giờ bị rỗng ruột hay giật màu ở cuối video.
2. **Quy tắc trích xuất nét vẽ hữu cơ (`skeleton`)**:
   - Đối với hộp/badge chứa chữ cái bên trong (như các ô nguyên âm `A, E, I, O, U` hay `Y`): Luôn đặt `"type": "colored_image"`, `"colorMode": "wash"`.
   - Engine sẽ trích xuất nét vẽ theo dáng chữ thật của bút dạ thay vì chỉ vẽ 4 cạnh hình học rỗng.
3. **Smart Subtitle Position (`MarginV=4`)**:
   - Cố định lề dưới ở mức `MarginV=4`, cỡ chữ `FontSize=13` với viền mờ bán trong suốt `BackColour=&H80000000` để phụ đề không bao giờ che khuất nội dung ở Zone 4 phía đáy màn hình.

---

## III. QUY TRÌNH 1-DÒNG LỆNH TỰ ĐỘNG HÓA PIPELINE

Khi sản xuất nhiều cảnh, chạy toàn bộ chuỗi Bước 1 $\rightarrow$ Bước 5 bằng 1 dòng lệnh gộp:

```bash
# Giả sử đang ở thư mục scene_XX:
python3 create_audio.py && \
python3 create_annotation.py && \
python3 ../../../scripts/render_stream_whiteboard.py scene.png scene.annotation.json scene.mp4 ../../../assets/drawing-hand.png --canvas-hex "#FFFFFF" && \
ffmpeg -y -i scene.mp4 -i narration.m4a -c:v copy -c:a aac scene_voice.mp4 && \
ffmpeg -y -i scene_voice.mp4 -vf "subtitles=input.srt:force_style='FontSize=13,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=3,MarginV=4'" -c:a copy scene_sub.mp4
```
Chỉ cần chạy 1 lần duy nhất, toàn bộ sản phẩm hoàn thiện sẽ xuất hiện đầy đủ trong thư mục của cảnh đó.
