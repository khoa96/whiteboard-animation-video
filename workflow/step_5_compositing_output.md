# ĐẦU RA MẪU BƯỚC 5: AUDIO-VISUAL COMPOSITING & SUBTITLE DELIVERY
## (Dữ liệu mẫu chuẩn hóa lấy từ Scene 01: ARTICLES — THREE GROUPS)

Tài liệu này thể hiện cấu trúc đầu ra chuẩn của **Bước 5**, bao gồm:
1. Quy trình ghép âm thanh và video (Audio-Video Muxing).
2. Kỹ thuật nhúng phụ đề thông minh chống đè nội dung (Smart Subtitle Burning).
3. Bảng tiêu chí kiểm định chất lượng (QA Verification Checklist).
4. Danh mục các sản phẩm đóng gói hoàn thiện bàn giao.

---

### PHẦN 1: QUY TRÌNH GHÉP ÂM THANH (AUDIO-VIDEO MUXING)

Sau khi video hoạt hoạ `scene_01.mp4` được render từ Bước 4, ta sử dụng FFmpeg để ghép tệp âm thanh đồng hồ chủ `narration.m4a` từ Bước 2:

```bash
ffmpeg -y \
  -i assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01.mp4 \
  -i assets/whiteboard/test_cases/test_case_10_articles/scene_01/narration.m4a \
  -c:v copy \
  -c:a aac \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01_voice.mp4
```

*Đặc điểm*:
- `-c:v copy`: Không mã hóa lại video (Stream Copy), giữ nguyên chất lượng hình ảnh 100% và thời gian xử lý cực nhanh (< 1 giây).
- `-c:a aac`: Đóng gói luồng âm thanh theo chuẩn AAC tương thích với mọi thiết bị di động và trình duyệt.

---

### PHẦN 2: KỸ THUẬT NHÚNG PHỤ ĐỀ CHỐNG ĐÈ NỘI DUNG (SMART HARDSUB)

#### Vấn đề phát hiện khi thử nghiệm ban đầu
Khi dùng cấu hình phụ đề mặc định (`MarginV=18`, `FontSize=16`), thanh nền đen của phụ đề ở câu số 5 đã bị đẩy cao lên và che khuất nửa trên của hộp bài học **TODAY: A / AN** ở Zone 4 phía dưới đáy màn hình.

#### Giải pháp cấu hình phụ đề thanh mảnh tối ưu
Hạ lề dọc xuống sát mép dưới (`MarginV=4`), giảm nhẹ kích cỡ chữ (`FontSize=13`), đặt màu nền mờ bán trong suốt 50% (`BackColour=&H80000000`):

```bash
ffmpeg -y \
  -i assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01_voice.mp4 \
  -vf "subtitles=assets/whiteboard/test_cases/test_case_10_articles/scene_01/input.srt:force_style='FontSize=13,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=3,MarginV=4'" \
  -c:a copy \
  assets/whiteboard/test_cases/test_case_10_articles/scene_01/scene_01_sub.mp4
```

*Kết quả*:
- Phụ đề hiển thị thanh thoát thành 1 dòng đơn sát mép dưới.
- Khung hộp **TODAY: A / AN** hoàn toàn nổi bật, không bị che khuất bất kỳ chi tiết nét vẽ nào.

---

### PHẦN 3: BẢNG KIỂM TRA CHẤT LƯỢNG (QA VERIFICATION CHECKLIST)

Mỗi scene trước khi bàn giao bắt buộc phải vượt qua bảng kiểm định 5 tiêu chí sau:

| Mốc kiểm tra | Thời điểm | Nội dung thuyết minh | Hành động thị giác thực tế | Trạng thái QA |
| :---: | :---: | :--- | :--- | :---: |
| **Tiêu đề** | `03.0s` | *"Chào các bạn, trong tiếng Anh, mạo từ..."* | Tay đang viết tiêu đề chính **ARTICLES**. | **ĐẠT (PASS)** |
| **Thẻ 1: A/AN** | `13.0s` | *"...ví dụ: a book - một cuốn sách..."* | Tay vẽ icon cuốn sách và chữ `a book` trong Card 1. | **ĐẠT (PASS)** |
| **Thẻ 2: THE** | `24.0s` | *"...ví dụ: the book - chính cuốn sách này."* | Tay vẽ cặp sách có vệt phát sáng trong Card 2. | **ĐẠT (PASS)** |
| **Thẻ 3: ZERO**| `33.0s` | *"...ví dụ như water - nước nói chung."* | Tay vẽ ly nước trong Card 3. | **ĐẠT (PASS)** |
| **Tiêu điểm** | `40.0s` | *"...bắt đầu với nhóm nền tảng đầu tiên: A và AN."*| Tay đóng khung xanh **TODAY: A / AN**, phụ đề không che chữ. | **ĐẠT (PASS)** |
| **Nghỉ tĩnh cuối** | `42.5s` | *(Hết tiếng nói, giữ tĩnh)* | Bàn tay thu về ngoài góc màn hình, bảng vẽ tĩnh trọn vẹn 2.5s. | **ĐẠT (PASS)** |

---

### PHẦN 4: DANH MỤC SẢN PHẨM BÀN GIAO HOÀN CHỈNH

Sau khi chạy xong Bước 5, thư mục của từng scene sẽ có đầy đủ các tệp tin xuất bản:

1. **`scene_01_sub.mp4`**: Video hoàn chỉnh nhất (hình vẽ whiteboard 60 fps + lồng tiếng song ngữ chuẩn + phụ đề tiếng Việt chạy thời gian thực).
2. **`scene_01_voice.mp4`**: Video hoàn chỉnh lồng tiếng (không phụ đề, thích hợp dùng làm video gốc hoặc tùy biến đa ngôn ngữ).
3. **`scene_01.mp4`**: Video hoạt hoạ hình vẽ bảng trắng không tiếng (silent video track).
4. **`narration.m4a`**: Tệp âm thanh thuyết minh Master Clock.
5. **`input.srt`**: Tệp phụ đề đồng bộ chuẩn xác từng mili-giây.
6. **`timing_cues.json`**: Bản ghi mốc thời gian chi tiết của từng câu thoại.
7. **`snapshots/`**: Thư mục ảnh chụp kiểm định chất lượng tại các giây `03s, 06s, 10s, 13s, 16s, 20s, 24s, 29s, 33s, 36s, 40s, 42s`.
