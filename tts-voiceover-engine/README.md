# TTS Voice-Over Engine (Google AI Studio)

Hệ thống chuyển đổi kịch bản học tiếng Anh song ngữ thành file âm thanh chất lượng cao với giọng đọc đặc trưng cố định của kênh (Custom Voice ID).

---

## 🚀 CÁCH SỬ DỤNG NHANH (QUICK START)

### 1. Cài đặt thư viện
```bash
cd tts-voiceover-engine
npm install
```

### 2. Cấu hình API Key
Mở file `.env` và điền `GEMINI_API_KEY`:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
TTS_MODEL_MODE=gemini-3.8-flash-tts
CUSTOM_VOICE_ID=voice_qm5tk2dpfj15
```

### 3. Khởi tạo giọng đọc đặc trưng của kênh (Chỉ chạy 1 lần đầu)
```bash
npm run init-voice
```
Lệnh này sẽ gửi bản thiết kế chân dung giọng nói (Voice Design Prompt) lên Google AI Studio để "đúc" ra một mã giọng cố định (`CUSTOM_VOICE_ID`).

### 4. Tạo Voice-Over từ kịch bản
Soạn kịch bản trong `inputs/sample-script.txt` (hoặc truyền qua `--file`), sau đó chạy:
```bash
npm run generate
```
File âm thanh chuẩn phòng thu (`.wav`) sẽ tự động xuất ra thư mục `outputs/voiceover_<timestamp>.wav`.

---

## 🎙️ CÚ PHÁP ĐẶC TRƯNG CHUẨN A1
Trong kịch bản, sử dụng tag `[A1: ...]` cho các câu tiếng Anh để hệ thống tự động giãn nhịp và bật cực kỳ rõ âm cuối (`break`, `rest`, `want`), chống tuyệt đối hiện tượng nuốt âm hoặc nối âm:

```text
Các bạn hãy chú ý nghe kỹ âm cuối của từng từ và không nối âm nhé: [A1: I want to take a break].
```
