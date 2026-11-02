# 🎙️ HƯỚNG DẪN TOÀN DIỆN VỀ ĐỘNG CƠ VOICE-OVER (TTS-VOICEOVER-ENGINE)
> **Động cơ tạo giọng nói thống nhất duy nhất cho toàn bộ dự án Whiteboard Animation**

---

## 📌 MỤC LỤC
1. [Giới thiệu tổng quan kiến trúc](#1-giới-thiệu-tổng-quan-kiến-trúc)
2. [Luồng hoạt động End-to-End (Workflow)](#2-luồng-hoạt-động-end-to-end-workflow)
3. [Cấu hình giọng nói & Bản sắc kênh](#3-cấu-hình-giọng-nói--bản-sắc-kênh)
   - [Chế độ A: Giọng đặc trưng độc quyền kênh (Custom Voice ID)](#chế-độ-a-giọng-đặc-trưng-độc-quyền-kênh-custom-voice-id)
   - [Chế độ B: Giọng Prebuilt chuẩn Google AI Studio (Dự phòng)](#chế-độ-b-giọng-prebuilt-chuẩn-google-ai-studio-dự-phòng)
4. [Tích hợp Audio Master Clock cho Whiteboard Video](#4-tích-hợp-audio-master-clock-cho-whiteboard-video)
5. [Cơ chế xoay tua API Key & Quản lý hạn mức (Rate Limits)](#5-cơ-chế-xoay-tua-api-key--quản-lý-hạn-mức-rate-limits)
6. [Hướng dẫn thao tác nhanh (Quickstart)](#6-hướng-dẫn-thao-tác-nhanh-quickstart)
7. [Quy tắc viết kịch bản tối ưu ngữ điệu A1-A2 (Best Practices)](#7-quy-tắc-viết-kịch-bản-tối-ưu-ngữ-điệu-a1-a2-best-practices)

---

## 1. Giới thiệu tổng quan kiến trúc

Toàn bộ dự án sử dụng **một động cơ Text-to-Speech duy nhất** đặt tại:

```text
whiteboard-video-main/
│
├── .env                        # File cấu hình biến môi trường DUY NHẤT toàn repo
│
└── tts-voiceover-engine/       # 🚀 ĐỘNG CƠ VOICE-OVER DUY NHẤT CỦA DỰ ÁN
    ├── src/
    │   ├── voice-manager.ts    # Google AI Studio Voice Design API (Quản lý Custom Voice ID)
    │   ├── tts-client.ts       # Gemini TTS Client (Exponential Backoff & Jitter)
    │   ├── script-preprocessor.ts # Tiền xử lý kịch bản: Thought groups, [NATURAL], [DRILL]
    │   ├── audio-utils.ts      # PCM L16 24kHz -> WAV 44-byte Header, tính mili-giây
    │   └── index.ts            # CLI Entrypoint hỗ trợ xuất Audio, SRT và Timing Cues
    ├── config/
    │   └── voice-persona.json  # Bản thiết kế chân dung giọng đọc độc quyền của kênh
    └── outputs/                # Thư mục xuất file âm thanh mặc định
```

---

## 2. Luồng hoạt động End-to-End (Workflow)

```text
┌────────────────────────┐
│  Kịch bản văn bản thô  │ (Hỗ trợ định dạng .txt, .md, .srt, tag [NATURAL] và [DRILL])
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   ScriptPreprocessor   │ • Phân tách từng câu độc lập
│   (Tiền xử lý nhịp điệu)│ • Tự động loại bỏ tiêu đề markdown, xử lý tag phát âm
└───────────┬────────────┘ • Chèn micro-pauses (~300ms) tạo khoảng lấy hơi tự nhiên
            │
            ▼
┌────────────────────────┐
│    Google TTS Client   │ • Gửi yêu cầu đến Google AI Studio (gemini-3.8-flash-tts)
│  (Xoay tua chống lỗi)  │ • Tự động xử lý 429/503 bằng Exponential Backoff & Jitter
└───────────┬────────────┘ • Giữ vững tông giọng qua Custom Voice ID cố định
            │
            ▼
┌────────────────────────┐
│       AudioUtils       │ • Tiếp nhận dữ liệu PCM L16 (24.000 Hz Mono)
│   (Đóng gói âm thanh)  │ • Ghép nối chèn lead-in (0.5s), gap (0.5s), tail (2.0s)
└───────────┬────────────┘ • Dập Header WAV chuẩn 44-byte hoặc encode AAC (.m4a)
            │
            ▼
┌──────────────────────────────────────────────────────────────┐
│                  BỘ BA DỮ LIỆU ĐẦU RA                        │
│ 1. narration.wav / .m4a   : Âm thanh lời giảng hoàn chỉnh     │
│ 2. timing_cues.json       : Mốc startMs, durationMs từng câu │
│ 3. input.srt              : Phụ đề chuẩn thời gian mili-giây │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Cấu hình giọng nói & Bản sắc kênh

### Chế độ A: Giọng đặc trưng độc quyền kênh (Custom Voice ID - Mặc định)
Kênh sở hữu một giọng đọc nhất quán, không đụng hàng nhờ tính năng **Google AI Studio Voice Design API**.

* File cấu hình chân dung: `tts-voiceover-engine/config/voice-persona.json`
* Mã giọng hiện tại: `voice_xnxd3uit2744` (Nam 25 tuổi, chuẩn giọng Bắc hiện đại, phát âm tiếng Anh chuẩn Mỹ A1).
* **Khởi tạo lại hoặc tạo mới giọng đọc**:
  ```bash
  cd tts-voiceover-engine
  npm run init-voice
  ```
  Lệnh sẽ tự động gọi API, nhận mã `voice_xxxx` mới và ghi thẳng vào `.env` gốc và `voice-persona.json`.

---

### Chế độ B: Giọng Prebuilt chuẩn Google AI Studio (Dự phòng)
Nếu muốn dùng các giọng đọc có sẵn của Google, bạn cấu hình biến `PREBUILT_FALLBACK_VOICE` trong file `.env` ở thư mục gốc:

```env
PREBUILT_FALLBACK_VOICE=Achird
```

| Tên giọng | Giới tính | Phong cách đặc trưng |
| :--- | :---: | :--- |
| **Achird** | Nam | Tươi sáng, nhiệt huyết, trẻ trung 25 tuổi (Khuyên dùng) |
| **Charon** | Nam | Trầm ấm, đĩnh đạc, dày dặn, uy tín |
| **Puck** | Nam | Hoạt bát, sôi nổi, dí dỏm |
| **Erinome** | Nữ | Rõ ràng, mô phạm, chuẩn mực |
| **Aoede** | Nữ | Dịu dàng, truyền cảm, sâu lắng |
| **Kore** | Nữ | Tự tin, đĩnh đạc, hiện đại |

---

## 4. Tích hợp Audio Master Clock cho Whiteboard Video

Để phục vụ nguyên tắc **Audio Master Clock (Âm thanh là đồng hồ chủ)** điều khiển các nét vẽ ở Bước 3 và Bước 4, `tts-voiceover-engine` hỗ trợ xuất trực tiếp mốc thời gian và phụ đề:

```bash
# Cú pháp tạo âm thanh cho 1 scene cụ thể:
npm --prefix tts-voiceover-engine run generate -- \
  --file path/to/script.txt \
  --output path/to/scene_01/narration.wav \
  --srt path/to/scene_01/input.srt \
  --cues path/to/scene_01/timing_cues.json
```

Kết quả:
1. `narration.wav` (hoặc `.m4a`): Âm thanh liền mạch.
2. `timing_cues.json`: Chứa `startMs`, `durationMs` của từng câu để file `scene_01.annotation.json` gán thời gian vẽ.
3. `input.srt`: File phụ đề chuẩn dùng để burn hardsub ở Bước 5.

---

## 5. Cơ chế xoay tua API Key & Quản lý hạn mức (Rate Limits)

Google AI Studio Free Tier áp dụng hạn mức:
* **Flash Models (`gemini-3.8-flash-tts`):** 15 RPM, 250 lượt gọi / ngày / key.

Trong file `.env` gốc, bạn có thể điền 1 hoặc nhiều API Key cách nhau bởi dấu phẩy:
```env
GEMINI_API_KEYS=key_gmail_1,key_gmail_2,key_gmail_3
```

---

## 6. Hướng dẫn thao tác nhanh (Quickstart)

### Bước 1: Cài đặt thư viện (Chỉ làm 1 lần)
```bash
cd tts-voiceover-engine
npm install
cd ..
```

### Bước 2: Thiết lập file môi trường
Điền API key vào file `.env` tại thư mục gốc dự án:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

### Bước 3: Tạo Voice-Over từ kịch bản mẫu
```bash
cd tts-voiceover-engine
npm run generate
```

### Bước 4: Tạo Voice-Over từ file kịch bản bất kỳ
```bash
cd tts-voiceover-engine
npm run generate -- --file inputs/sample-script.txt
```

---

## 7. Quy tắc viết kịch bản tối ưu ngữ điệu A1-A2 (Best Practices)

1. **Ngắt nhịp Thought Groups**: Dùng dấu phẩy `,` để tạo nhịp nghỉ tự nhiên giữa các vế câu.
2. **Thẻ `[NATURAL: ...]`**: Dành cho câu giao tiếp trôi chảy, ngữ điệu nối âm bản xứ.
3. **Thẻ `[DRILL: ...]`**: Dành cho từ vựng cần bật cực rõ âm cuối:
   ```text
   Hãy cùng phát âm: [DRILL: book... cat... desk].
   ```
