# CẤU TRÚC ĐẦU VÀO CHUẨN KHI KHỞI TẠO MỘT DỰ ÁN MỚI
## (Standard Project Onboarding Structure & Input Specification)

Tài liệu này quy định cấu trúc thư mục và các tệp dữ liệu cần cung cấp khi bắt đầu bất kỳ một dự án video Whiteboard Animation mới. Việc chuẩn bị đúng cấu trúc này giúp AI hoặc đội ngũ kỹ thuật có thể kích hoạt quy trình sản xuất tự động ngay lập tức mà không cần hỏi lại yêu cầu.

---

## I. CÂU LỆNH TỰ ĐỘNG KHỞI TẠO CẤU TRÚC DỰ ÁN (AUTOMATED SCAFFOLD COMMAND)

Để khởi tạo một dự án mới hoàn chỉnh chỉ với **1 câu lệnh duy nhất**, bạn (hoặc yêu cầu AI) chạy lệnh sau trong terminal:

```bash
# Cú pháp tổng quát:
python3 scripts/init_project.py <tên_hoặc_đường_dẫn_dự_án> [--title "Tiêu đề bài học"] [--voice "tên_voice"]

# Ví dụ 1: Tạo dự án mới lưu trong thư mục projects/
python3 scripts/init_project.py project_present_simple --title "Thì Hiện Tại Đơn"

# Ví dụ 2: Tạo dự án test case mới trong assets/whiteboard/test_cases/
python3 scripts/init_project.py assets/whiteboard/test_cases/case_11_passive_voice --title "Câu Bị Động"
```

> **Mẹo tự động hóa bằng AI**:
> Bạn chỉ cần nhắn tin cho AI: *"Hãy tạo dự án mới tên là `project_past_simple` về chủ đề Thì Quá Khứ Đơn"*, AI sẽ tự động kích hoạt câu lệnh `scripts/init_project.py` để dựng toàn bộ cây thư mục và các tệp mẫu sẵn sàng cho bạn.

---

## II. CẤU TRÚC THƯ MỤC ĐƯỢC TỰ ĐỘNG SINH RA

Sau khi chạy câu lệnh trên, dự án sẽ có đầy đủ cấu trúc chuẩn hóa:

```text
ten_du_an/
├── brief.md              # 1. Tóm tắt sáng tạo & yêu cầu dự án (đã điền sẵn form mẫu)
├── subtitle_draft.srt    # 2. Toàn bộ lời thoại phân theo cảnh (kèm mốc thời gian mẫu)
├── project.json          # 3. Cấu hình kỹ thuật (1920x1080, #FFFFFF, 60fps, giọng đọc Edge-TTS)
├── images/               # 4. Thư mục chứa các ảnh tĩnh 16:9 sinh từ AI
│   └── README.md         #    (Hướng dẫn độ phân giải, nền trắng và đặt tên file)
└── scenes/               # 5. Thư mục làm việc cho từng scene kết xuất
```

---

## III. ĐẶC TẢ CHI TIẾT 3 TỆP ĐẦU VÀO BẮT BUỘC

---

### 1. Tệp `brief.md` (Tóm tắt yêu cầu sư phạm & phong cách)
* **Mục đích**: Cung cấp thông tin nền tảng để thiết lập các tham số AI và kiểm soát chất lượng.
* **Mẫu nội dung cần điền (Copy & Paste)**:

```markdown
# CREATIVE BRIEF DỰ ÁN: [TÊN CHỦ ĐỀ]

## 1. Thông số tổng quan
- **Chủ đề bài giảng**: [Ví dụ: Thì Hiện Tại Đơn - Present Simple Tense]
- **Khán giả mục tiêu**: [Ví dụ: Học sinh lớp 6 / Người đi làm mất gốc tiếng Anh]
- **Thời lượng toàn video**: [Ví dụ: 6 – 8 phút]
- **Tổng số scene**: [Ví dụ: 8 scenes]

## 2. Yêu cầu âm thanh (Voice Direction)
- **Giọng thuyết minh**: [Ví dụ: Nam miền Bắc, điềm tĩnh, truyền cảm (Edge-TTS: en-US-AndrewMultilingualNeural)]
- **Phát âm tiếng Anh**: [American English (Mỹ) chuẩn bản ngữ]

## 3. Quy chuẩn thị giác (Visual Direction)
- **Phong cách**: 2D Hand-drawn Whiteboard, nét vẽ bút dạ tự nhiên, không 3D, không người thật.
- **Nền**: Trắng tuyệt đối `#FFFFFF`.
- **Màu chức năng**:
  - Đen: Nét chính, chữ viết, khung viền.
  - Xanh dương: Khái niệm chính, điểm nhấn.
  - Cam / Đỏ: Cảnh báo, trường hợp đặc biệt, lưu ý.
  - Xanh lá: Đáp án đúng, ví dụ tích cực.
```

---

### 2. Tệp `script_draft.srt` (Kịch bản lời thoại chia theo cảnh)
* **Mục đích**: Cung cấp lời thuyết minh hoàn chỉnh. Hệ thống sẽ dựa vào các mốc thời gian này để cắt lời cho từng scene và đưa vào bộ tổng hợp giọng nói đa ngữ.
* **Quy tắc định dạng**:
  - Dùng định dạng SRT chuẩn (hoặc file Markdown đánh số từng Scene).
  - Viết câu ngắn, tự nhiên, ngắt nghỉ hợp lý.
  - Các ví dụ tiếng Anh viết đúng chính tả, không phiên âm bồi sang tiếng Việt.
* **Mẫu định dạng**:

```srt
1
00:00:00,000 --> 00:00:06,500
[SCENE 01] Chào các bạn, hôm nay chúng ta sẽ cùng tìm hiểu về...

2
00:00:07,000 --> 00:00:15,000
Có ba điểm cốt lõi bạn cần ghi nhớ...

...

6
00:00:45,000 --> 00:00:52,000
[SCENE 02] Trước tiên, hãy quan sát ví dụ sau đây...
```

---

### 3. Thư mục `images/` (Ảnh nguồn tĩnh 16:9)
* **Mục đích**: Là nguồn dữ liệu hình ảnh gốc để trích xuất nét vẽ và màu sắc.
* **Quy chuẩn ảnh**:
  - **Tỷ lệ**: Bắt buộc là `16:9` (ngang).
  - **Độ phân giải**: Khuyến nghị từ `1376x768`, `1920x1080` đến `2K` (hệ thống sẽ tự động resize về đúng chuẩn Full HD).
  - **Nền ảnh**: Nền trắng sáng, không có hoa văn texture giấy hay đổ bóng râm.
  - **Khoảng cách nét vẽ**: Các đối tượng (icon, chữ cái, nhãn) cần có khoảng hở thoáng đãng (whitespace) tối thiểu 20-30px, không để chữ dính vào hình vẽ hay mũi tên đè lên chữ.
  - **Quy tắc đặt tên file**: Đặt tên có tiền tố chỉ số scene để pipeline tự động nhận diện:
    - `scene_01.jpg` (hoặc `scene_01_raw.png`)
    - `scene_02.jpg` (hoặc `scene_02_raw.png`)
    - `scene_03.jpg` (hoặc `scene_03_raw.png`)

---

## IV. SAU KHI CUNG CẤP ĐỦ 3 NGUYÊN LIỆU TRÊN

Ngay khi bạn cung cấp thư mục dự án với 3 thành phần trên, hệ thống sẽ tự động triển khai quy trình:
1. Tự động đọc `brief.md` để xác lập phong cách.
2. Tự động đọc `images/scene_XX` $\rightarrow$ chuẩn hóa canvas 1920x1080 `#FFFFFF`.
3. Tự động cắt lời thoại trong `script_draft.srt` cho Scene XX $\rightarrow$ tạo `narration.m4a` và mốc thời gian chuẩn mili-giây.
4. Tự động phân rã nguyên tử các vùng vẽ (Zero-Overlap) $\rightarrow$ tạo `annotation.json`.
5. Tự động render video 60 fps và đóng gói video có lồng tiếng + phụ đề hoàn chỉnh.
