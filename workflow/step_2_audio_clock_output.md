# ĐẦU RA MẪU BƯỚC 2: STORYBOARD & AUDIO MASTER CLOCK
## (Dữ liệu mẫu chuẩn hóa lấy từ Scene 01: ARTICLES — THREE GROUPS)

Tài liệu này thể hiện cấu trúc đầu ra chuẩn của **Bước 2**, bao gồm:
1. Bảng phân cảnh đồng bộ Âm thanh - Thị giác (**Audio-Visual Storyboard**).
2. Mã nguồn Python tổng hợp giọng đọc TTS song ngữ và đo thời lượng (`create_audio.py`).
3. Dữ liệu mốc thời gian chuẩn xác đến mili-giây (`timing_cues.json`).
4. Tệp phụ đề thời gian thực (`input.srt`).
5. Thông số kỹ thuật của tệp âm thanh hoàn chỉnh (`narration.m4a`).

---

### PHẦN 1: AUDIO-VISUAL STORYBOARD CHO SCENE 01

| Câu | Lời thoại thuyết minh (Voice Over) | Hành động vẽ trên bảng trắng (Visual Action) | Element ID liên kết |
| :---: | :--- | :--- | :--- |
| **1** | *"Chào các bạn, trong tiếng Anh, mạo từ - Articles - được chia làm ba nhóm chính."* | Bàn tay vẽ tiêu đề **ARTICLES** ở trên đỉnh, sau đó viết phụ đề **THREE GROUPS**. | `el-01-title`<br/>`el-02-subtitle` |
| **2** | *"Nhóm thứ nhất là A và AN - dùng cho một vật chung chung, ví dụ: a book - một cuốn sách, hay an apple - một quả táo."* | Bàn tay vẽ khung trên + nhãn **A / AN**, tiếp đó vẽ icon cuốn sách + chữ `a book`, sau đó vẽ quả táo + chữ `an apple`. | `el-03-card1-header`<br/>`el-04-card1-book`<br/>`el-05-card1-apple` |
| **3** | *"Nhóm thứ hai là THE - dùng khi vật đã được xác định cụ thể, ví dụ: the book - chính cuốn sách này."* | Bàn tay vẽ khung trên + nhãn **THE**, tiếp đó vẽ cặp sách phát sáng + chữ `the book`. | `el-06-card2-header`<br/>`el-07-card2-content` |
| **4** | *"Và nhóm thứ ba là Zero Article - những trường hợp không dùng mạo từ, ví dụ như water - nước nói chung."* | Bàn tay vẽ khung trên + nhãn **ZERO ARTICLE**, tiếp đó vẽ ly nước mát + chữ `WATER`. | `el-08-card3-header`<br/>`el-09-card3-content` |
| **5** | *"Để học thật vững, hôm nay chúng ta sẽ bắt đầu với nhóm nền tảng đầu tiên: A và AN."* | Bàn tay kẻ đường phân cách ngang toàn trang, sau đó đóng khung nổi bật cụm từ **TODAY: A / AN**. | `el-10-divider`<br/>`el-11-today` |

---

### PHẦN 2: LỆNH TỔNG HỢP ÂM THANH & DẬP AUDIO MASTER CLOCK

Toàn bộ hệ thống sử dụng `tts-voiceover-engine` (Google AI Studio Voice Design API) với Custom Voice ID độc quyền:
- **Custom Voice ID**: `voice_xnxd3uit2744` (Khóa cố định âm sắc đặc trưng của kênh).
- **Phát âm**: Giọng nam miền Bắc 25 tuổi, điềm tĩnh, ấm áp, nhả rõ âm cuối chuẩn A1, phát âm tiếng Anh chuẩn Mỹ bản ngữ.
- **Tự động hóa**: Sinh âm thanh chuẩn, tự động chèn lead-in `0.5s`, khoảng nghỉ giữa các câu `0.5s`, tail freeze `2.0s`, đồng thời xuất chuẩn xác `timing_cues.json` và `input.srt`.

#### Câu lệnh thực thi:

```bash
# Đứng từ thư mục gốc repo:
npm --prefix tts-voiceover-engine run generate -- \
  --file scene_01/script.txt \
  --output scene_01/narration.wav \
  --srt scene_01/input.srt \
  --cues scene_01/timing_cues.json
```

Lệnh trên sẽ tự động:
1. Đọc kịch bản câu thoại từ `scene_01/script.txt`.
2. Gọi Gemini TTS API với Custom Voice ID độc quyền `voice_xnxd3uit2744`.
3. Đo chính xác thời lượng từng câu và nối kèm khoảng nghỉ chuẩn sư phạm.
4. Xuất file âm thanh hoàn chỉnh: `scene_01/narration.wav` (hoặc `.m4a`).
5. Xuất phụ đề chuẩn mili-giây: `scene_01/input.srt`.
6. Xuất cấu trúc mốc thời gian làm đồng hồ chủ cho Bước 3: `scene_01/timing_cues.json`.


---

### PHẦN 3: FILE DỮ LIỆU MẪU MỐC THỜI GIAN (`timing_cues.json`)

```json
{
  "totalDurationMs": 43284,
  "cues": [
    {
      "index": 1,
      "startMs": 500,
      "endMs": 7148,
      "durationMs": 6648,
      "text": "Chào các bạn, trong tiếng Anh, mạo từ - Articles - được chia làm ba nhóm chính."
    },
    {
      "index": 2,
      "startMs": 7648,
      "endMs": 17416,
      "durationMs": 9768,
      "text": "Nhóm thứ nhất là A và AN - dùng cho một vật chung chung, ví dụ: a book - một cuốn sách, hay an apple - một quả táo."
    },
    {
      "index": 3,
      "startMs": 17916,
      "endMs": 25860,
      "durationMs": 7944,
      "text": "Nhóm thứ hai là THE - dùng khi vật đã được xác định cụ thể, ví dụ: the book - chính cuốn sách này."
    },
    {
      "index": 4,
      "startMs": 26360,
      "endMs": 34400,
      "durationMs": 8040,
      "text": "Và nhóm thứ ba là Zero Article - những trường hợp không dùng mạo từ, ví dụ như water - nước nói chung."
    },
    {
      "index": 5,
      "startMs": 34900,
      "endMs": 41284,
      "durationMs": 6384,
      "text": "Để học thật vững, hôm nay chúng ta sẽ bắt đầu với nhóm nền tảng đầu tiên: A và AN."
    }
  ]
}
```

---

### PHẦN 4: FILE PHỤ ĐỀ MẪU (`input.srt`)

```srt
1
00:00:00,500 --> 00:00:07,148
Chào các bạn, trong tiếng Anh, mạo từ - Articles - được chia làm ba nhóm chính.

2
00:00:07,648 --> 00:00:17,416
Nhóm thứ nhất là A và AN - dùng cho một vật chung chung, ví dụ: a book - một cuốn sách, hay an apple - một quả táo.

3
00:00:17,916 --> 00:00:25,860
Nhóm thứ hai là THE - dùng khi vật đã được xác định cụ thể, ví dụ: the book - chính cuốn sách này.

4
00:00:26,360 --> 00:00:34,400
Và nhóm thứ ba là Zero Article - những trường hợp không dùng mạo từ, ví dụ như water - nước nói chung.

5
00:00:34,900 --> 00:00:41,284
Để học thật vững, hôm nay chúng ta sẽ bắt đầu với nhóm nền tảng đầu tiên: A và AN.
```
