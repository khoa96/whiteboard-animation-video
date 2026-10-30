# 🎙️ HƯỚNG DẪN TOÀN DIỆN VỀ HỆ THỐNG VOICE-OVER (TEXT-TO-SPEECH)
> **Dành cho thành viên mới bắt đầu dự án Whiteboard Animation Video**

---

## 📌 MỤC LỤC
1. [Giới thiệu tổng quan kiến trúc](#1-giới-thiệu-tổng-quan-kiến-trúc)
2. [Luồng hoạt động End-to-End (Workflow)](#2-luồng-hoạt-động-end-to-end-workflow)
3. [Hướng dẫn cấu hình 1 hoặc nhiều giọng nói](#3-hướng-dẫn-cấu-hình-1-hoặc-nhiều-giọng-nói)
   - [Chế độ A: Giọng đặc trưng độc quyền kênh (Custom Voice ID)](#chế-độ-a-giọng-đặc-trưng-độc-quyền-kênh-custom-voice-id)
   - [Chế độ B: Sử dụng 30 giọng Prebuilt chuẩn của Google](#chế-độ-b-sử-dụng-30-giọng-prebuilt-chuẩn-của-google)
   - [Chế độ C: Kịch bản đa giọng (Multi-voice / Đối thoại phân vai)](#chế-độ-c-kịch-bản-đa-giọng-multi-voice--đối-thoại-phân-vai)
4. [Cơ chế xoay tua API Key & Quản lý hạn mức (Rate Limits)](#4-cơ-chế-xoay-tua-api-key--quản-lý-hạn-mức-rate-limits)
5. [Hướng dẫn thao tác nhanh từng bước (Quickstart)](#5-hướng-dẫn-thao-tác-nhanh-từng-bước-quickstart)
6. [Quy tắc viết kịch bản tối ưu ngữ điệu A1-A2 (Best Practices)](#6-quy-tắc-viết-kịch-bản-tối-ưu-ngữ-điệu-a1-a2-best-practices)

---

## 1. Giới thiệu tổng quan kiến trúc

Dự án cung cấp 2 phân hệ Voice-Over chuyên sâu:

```
whiteboard-video-main/
│
├── tts-voiceover-engine/       # 🚀 PHÂN HỆ 1: Engine độc lập tạo Voice-Over đặc trưng kênh
│   ├── src/                    # Mã nguồn TypeScript: Tiền xử lý, gọi API, ghép audio
│   ├── config/voice-persona.json # Bản sắc giọng độc quyền (Custom Voice Persona)
│   ├── inputs/sample-script.txt  # Kịch bản đầu vào
│   └── outputs/                # Thư mục xuất file âm thanh WAV hoàn chỉnh
│
└── scripts/tts_gemini.py       # 🎬 PHÂN HỆ 2: Engine Python tích hợp render video Whiteboard
    └── Tự động gọi TTS từng phân cảnh và căn khớp Audio Clock cho animation
```

---

## 2. Luồng hoạt động End-to-End (Workflow)

Quy trình biến một đoạn văn bản thô thành một file âm thanh chất lượng phòng thu:

```
┌────────────────────────┐
│  Kịch bản văn bản thô  │ (Hỗ trợ thẻ [NATURAL: ...] và [DRILL: ...])
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   ScriptPreprocessor   │ • Tự động phân tách từng câu / mệnh đề độc lập
│   (Tiền xử lý nhịp điệu)│ • Chèn micro-pauses (~300ms) tạo khoảng lấy hơi tự nhiên
└───────────┬────────────┘ • Chia mẻ (Chunking) an toàn < 1800 ký tự
            │
            ▼
┌────────────────────────┐
│    Google TTS Client   │ • Gửi yêu cầu đến Google AI Studio (Gemini TTS API)
│  (Xoay tua chống lỗi)  │ • Tự động chuyển model dự phòng nếu gặp lỗi 429
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│       AudioUtils       │ • Tiếp nhận dữ liệu PCM L16 (24.000 Hz Mono)
│   (Đóng gói âm thanh)  │ • Ghép nối các mẻ liền mạch, dập Header WAV chuẩn 44-byte
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ File xuất thành phẩm   │ • outputs/voiceover_YYYY-MM-DD.wav
└────────────────────────┘
```

---

## 3. Hướng dẫn cấu hình 1 hoặc nhiều giọng nói

### Chế độ A: Giọng đặc trưng độc quyền kênh (Custom Voice ID)
Đây là tính năng độc quyền sử dụng **Google AI Studio Voice Design API**. Kênh của bạn sẽ sở hữu một giọng đọc nhất quán, không đụng hàng với bất kỳ kênh nào khác.

File cấu hình tại: `tts-voiceover-engine/config/voice-persona.json`

```json
{
  "voiceDesignPrompt": "A 22-year-old charismatic bilingual male language teacher. Warm, engaging, and resonant voice timbre. Speaks Vietnamese with an authentic Northern Hanoi accent. Speaks English with a clear, measured General American accent: expressive intonation, articulate pronunciation, and a calm, deliberate teaching cadence.",
  "styleDirective": "Warm, inspiring, and patient educational tone. Speak Vietnamese in a natural Northern Hanoi accent. For English speech, tailor specifically to A1-A2 beginner learners: maintain a calm, measured pace (around 110-120 words per minute), speak in clear, well-connected thought groups rather than isolated words, distinctly enunciate key stressed syllables and final consonants, and insert gentle, natural micro-pauses between sentence clauses to allow effortless listening comprehension without sounding robotic.",
  "customVoiceId": "voice_qm5tk2dpfj15"
}
```

* **Khởi tạo giọng độc quyền mới:**
  Chỉ cần chỉnh sửa mô tả trong `voiceDesignPrompt` rồi chạy lệnh:
  ```bash
  cd tts-voiceover-engine
  npm run init-voice
  ```
  Hệ thống sẽ tự động gọi Google Voice Design API, nhận `voice_id` mới và lưu đè vào cấu hình.

---

### Chế độ B: Sử dụng 30 giọng Prebuilt chuẩn của Google
Nếu không dùng Custom Voice, bạn có thể chọn bất kỳ giọng nào trong 30 giọng đọc sẵn có của Google AI Studio bằng cách đổi biến `TTS_VOICE` trong file `.env`:

```env
TTS_PROVIDER=google
TTS_VOICE=Alnilam
```

#### Bảng tra cứu các giọng tiêu biểu:
| Tên giọng | Giới tính | Phong cách đặc trưng | Phù hợp nhất cho |
| :--- | :---: | :--- | :--- |
| **Alnilam** | Nam | Điềm đạm, ấm áp, nhịp điệu tự nhiên | Bài giảng tiếng Anh, kể chuyện, podcast |
| **Achird** | Nam | Sáng, năng động, thân thiện | Giới thiệu bài học, hội thoại đời thường |
| **Puck** | Nam | Hoạt bát, hào hứng, biểu cảm đa dạng | Nhân vật hoạt hình, đối thoại vui nhộn |
| **Charon** | Nam | Uy tín, trầm ấm, dõng dạc | Phim tài liệu, kiến thức khoa học, triết lý |
| **Aoede** | Nữ | Dịu dàng, sâu lắng, truyền cảm | Đọc truyện, thiền, ngữ văn |
| **Erinome** | Nữ | Chuẩn mực, rõ ràng, sư phạm | Hướng dẫn ngữ pháp, phát âm từ vựng |
| **Kore** | Nữ | Trẻ trung, tự tin, phát âm tách bạch | Thuyết trình, bản tin giáo dục |

---

### Chế độ C: Kịch bản đa giọng (Multi-voice / Đối thoại phân vai)
Khi làm video có đối thoại giữa 2 nhân vật (Ví dụ: Thầy giáo David và Học sinh Nam), bạn thiết lập trong kịch bản phân cảnh của whiteboard video (`project.json`):

```json
{
  "scenes": [
    {
      "id": "scene_01",
      "voice": "Alnilam",
      "narration": "Hello Nam! How are you doing today?"
    },
    {
      "id": "scene_02",
      "voice": "Puck",
      "narration": "I am doing great, teacher David! Today I want to learn English."
    }
  ]
}
```
Engine `scripts/tts_gemini.py` sẽ tự động chuyển đổi voice tương ứng cho từng phân cảnh khi render!

---

## 4. Cơ chế xoay tua API Key & Quản lý hạn mức (Rate Limits)

Google AI Studio Free Tier áp dụng hạn mức:
* **Flash Models (`gemini-3.8-flash-tts`):** 15 RPM (yêu cầu/phút), **250 lượt tạo / ngày / key**.
* **Pro Models (`gemini-2.5-pro-preview-tts`):** 2 RPM, **50 lượt tạo / ngày / key**.

### Cách khai báo nhiều Key để xoay tua liên tục:
Trong file `.env`, bạn điền các key từ nhiều tài khoản Google khác nhau, ngăn cách bằng dấu phẩy:
```env
GOOGLE_API_KEYS=key_gmail_1,key_gmail_2,key_gmail_3,key_gmail_4
```
* **Engine tự động:** Khi một key hoặc model chạm lỗi `429 (Too Many Requests)`, engine sẽ lập tức chuyển sang key hoặc model Flash tiếp theo mà không làm gián đoạn quá trình sinh giọng.
* **Bảo vệ an toàn:** File `.env` đã được chặn hoàn toàn trong `.gitignore` và có Git Pre-commit Hook tự động hủy lệnh commit nếu vô tình chứa API Key.

---

## 5. Hướng dẫn thao tác nhanh từng bước (Quickstart)

### Bước 1: Cài đặt thư viện (Chỉ làm 1 lần)
```bash
# Cài đặt cho Engine Voice-over TypeScript
cd tts-voiceover-engine
npm install

# Quay lại thư mục gốc dự án
cd ..
```

### Bước 2: Chuẩn bị file cấu hình môi trường
Sao chép `.env.example` thành `.env` và điền ít nhất 1 Google API Key:
```bash
cp .env.example .env
```

### Bước 3: Tạo Voice-Over từ kịch bản mẫu
```bash
cd tts-voiceover-engine
npm run generate
```
File âm thanh hoàn chỉnh sẽ xuất hiện tại thư mục `tts-voiceover-engine/outputs/voiceover_YYYY-MM-DD.wav`.

### Bước 4: Tạo Voice-Over từ một file kịch bản bất kỳ của bạn
```bash
npm run generate -- --file inputs/duong_dan_file_kich_ban.txt
```

---

## 6. Quy tắc viết kịch bản tối ưu ngữ điệu A1-A2 (Best Practices)

Để người học trình độ mới bắt đầu (Beginner A1-A2) nghe rõ ràng, dễ hiểu mà không bị giật cục hay máy móc, hãy áp dụng 3 quy tắc sau:

### Quy tắc 1: Sử dụng kỹ thuật ngắt nhịp nhóm nghĩa (Thought Groups)
Thay vì viết một câu quá dài, hãy dùng dấu phẩy `,` để tạo nhịp nghỉ tự nhiên:
* ❌ *Khó nghe:* `Every single day my morning begins at six o'clock and I wake up and drink a full glass of warm water.`
* ✅ *Dễ nghe A1-A2:* `Every single day, my morning begins at six o'clock. When the alarm rings, I wake up, and drink a full glass of warm water.`

### Quy tắc 2: Dùng thẻ `[NATURAL: ...]` cho câu giao tiếp trôi chảy
Khi muốn đọc một câu thành ngữ hoặc câu hội thoại với ngữ điệu nối âm bản xứ mượt mà:
```text
Các bạn hãy lắng nghe câu sau: [NATURAL: I would love to grab a cup of coffee].
```

### Quy tắc 3: Dùng thẻ `[DRILL: ...]` cho đoạn luyện phát âm bật âm cuối
Khi muốn học viên tập trung nghe rõ từng từ khóa và bật rõ âm đuôi (Ending Sounds):
```text
Bây giờ hãy cùng phát âm các từ sau: [DRILL: cat... book... street... desk].
```
*(Hệ thống sẽ tự động chèn khoảng dừng đủ lớn để học viên nhại theo sau từng từ).*
