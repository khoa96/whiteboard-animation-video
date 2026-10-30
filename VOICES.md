 

# Thư Viện 30 Giọng Đọc Google AI Studio (Gemini Audio Modality)

Tài liệu này tổng hợp đầy đủ 30 giọng nói chuẩn phòng thu của Google AI Studio (mô hình **`gemini-2.5-flash-preview-tts`**) kèm đặc tính âm sắc và thể loại video Whiteboard phù hợp.

---

## 🛠️ Cách thay đổi giọng đọc

Bạn có thể thay đổi giọng đọc bằng 1 trong 3 cách sau:

### Cách 1: Thay đổi trong file `.env` (Khuyên dùng)

Mở file `.env` và sửa dòng `TTS_VOICE`:

```env
TTS_VOICE=Charon       # Đổi tên thành bất kỳ giọng nào trong bảng dưới (ví dụ: Kore, Erinome, Puck...)
```

### Cách 2: Thay đổi trong file cấu hình JSON

Mở file [config/tts_voices.json](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/config/tts_voices.json) và sửa:

```json
{
  "active_voice": "Charon"
}
```

### Cách 3: Truyền trực tiếp qua dòng lệnh

Khi chạy lệnh tạo giọng đọc:

```bash
.venv/bin/python scripts/tts_narration.py input.srt --output narration.m4a --voice Erinome
```

---

## 🏆 Top Giọng Đọc Đề Xuất Theo Thể Loại Video Whiteboard

| Thể loại Video                                      | Giọng Nam tốt nhất       | Giọng Nữ tốt nhất    | Điểm nổi bật                                                 |
| ----------------------------------------------------- | --------------------------- | ------------------------ | ---------------------------------------------------------------- |
| **Giáo dục & Tiếng Anh Song ngữ A1**        | `Achird`, `Iapetus`     | `Erinome`, `Leda`    | Nhả rõ âm cuối, phát âm chuẩn US English, không nối âm |
| **Kinh tế, Chiến lược, OKR / KPI**          | `Charon`, `Rasalgethi`  | `Kore`, `Zephyr`     | Trầm ấm, điềm đạm, phong thái chuyên gia uy tín         |
| **Khoa học, Lập trình, IT & Kỹ thuật**     | `Iapetus`, `Sadaltager` | `Erinome`, `Schedar` | Khúc chiết, mạch lạc, chính xác thuật ngữ                |
| **Kể chuyện, Động lực & Triết lý sống** | `Algenib`, `Puck`       | `Sulafat`, `Despina` | Ấm áp, truyền cảm hứng, giàu chất tự sự                 |

---

## 🎙️ Tuyển Tập Giọng Nam Ấm Áp (Warm Male Voices) Đã Tạo Mẫu Thử

Dưới đây là 7 giọng nam có chất âm **ấm áp, truyền cảm, tự nhiên** nhất được chọn lọc từ kho 30 giọng của Gemini, kèm file audio nghe thử trực tiếp:

| STT | Tên giọng             | Đặc tính âm sắc ấm áp                                 | Cảm giác khi nghe                                                          | File nghe thử mẫu                                                                                                                                                                                   |
| :-: | :---------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  1  | **Algieba**       | **Mượt mà (Smooth), lịch lãm, truyền cảm**      | Giọng MC/thầy giáo ấm áp, êm ái, rất dễ chịu và bắt tai          | [sample_algieba_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_algieba_warm.wav)             |
|  2  | **Charon**        | **Trầm ấm sâu (Deep resonance), đĩnh đạc**      | Trầm vang, dày dặn, phong thái chuyên gia/người thầy từng trải     | [sample_charon_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_charon_warm.wav)               |
|  3  | **Enceladus**     | **Trầm khẽ (Breathy), thì thầm nhẹ, êm dịu**    | Ấm áp thủ thỉ bên tai, gần gũi, lắng đọng, thư giãn              | [sample_enceladus_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_enceladus_warm.wav)         |
|  4  | **Umbriel**       | **Thư thả (Easy-going), mộc mạc tự nhiên**       | Ấm áp nhẹ nhàng đời thường, không gò bó, thân mật               | [sample_umbriel_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_umbriel_warm.wav)             |
|  5  | **Sadaltager**    | **Trí tuệ (Knowledgeable), trầm tĩnh, am tường** | Khoan thai, điềm tĩnh, ấm áp người thầy thông thái                 | [sample_sadaltager_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_sadaltager_warm.wav)       |
|  6  | **Zubenelgenubi** | **Bình dân (Casual), chân chất, gần gũi**        | Mộc mạc, gần gũi như anh bạn hàng xóm giải thích bài học         | [sample_zubenelgenubi_warm.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/warm_male_voices/sample_zubenelgenubi_warm.wav) |
|  7  | **Achird**        | **Thân mật (Friendly), trẻ trung 25 tuổi**         | Tươi tắn, nhiệt huyết, gia sư trẻ trung đồng hành cùng học viên | [sample_achird_25yo.wav](file:///Users/nguyendangkhoa/Documents/whiteboard-animation-video/projects/test_voice_there_is_there_are/voice_samples/sample_achird_25yo.wav)                                |

---

## 📋 Bảng Danh Sách Đầy Đủ 30 Giọng Nói

|     STT     | Tên giọng             | Giới tính | Đặc điểm chất âm                                      | Thể loại video phù hợp nhất                                                       |
| :----------: | :---------------------- | :---------: | :---------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| **1** | **Zephyr**        |     Nữ     | Tươi sáng (Bright), trong trẻo, tự nhiên              | Video giáo dục kỹ năng mềm, giải thích kiến thức thường thức               |
| **2** | **Puck**          |     Nam     | Lạc quan (Upbeat), sôi nổi, dí dỏm                     | Video giới thiệu sản phẩm, kể chuyện hài hước, startup                        |
| **3** | **Charon**        |     Nam     | Trầm ấm, điềm đạm, uy quyền (Informative/Deep)       | **Video triết lý, kinh tế vĩ mô, chiến lược doanh nghiệp, OKR/KPI**     |
| **4** | **Kore**          |     Nữ     | Quyết đoán, đĩnh đạc, tự tin (Firm)                 | Video đào tạo quản trị, phương pháp luận học tập, tài chính               |
| **5** | **Fenrir**        |     Nam     | Sôi nổi, tràn đầy năng lượng, dồn dập (Excitable) | Video truyền động lực mạnh mẽ, thể thao, xu hướng công nghệ                 |
| **6** | **Leda**          |     Nữ     | Trẻ trung, linh hoạt, thân thiện (Youthful)             | Video mẹo vặt, học ngoại ngữ A1, tâm lý đời sống                             |
| **7** | **Orus**          |     Nam     | Mạnh mẽ, kiên định, rắn rỏi (Firm)                   | Video quy trình kỹ thuật, kỷ luật bản thân, lịch sử quân sự                 |
| **8** | **Aoede**         |     Nữ     | Nhẹ nhàng, thanh thoát, bay bổng (Breezy)               | Video chữa lành, phong cách sống (lifestyle), sức khỏe tinh thần                |
| **9** | **Callirrhoe**    |     Nữ     | Thư thái, tự nhiên, dễ chịu (Easy-going)              | Video văn hóa, du lịch, chia sẻ trải nghiệm đời sống                          |
| **10** | **Autonoe**       |     Nữ     | Tươi mới, lanh lợi, dứt khoát (Bright)                | Video bài giảng sinh động, phân tích tình huống ngắn                          |
| **11** | **Enceladus**     |     Nam     | Trầm khẽ, thì thầm nhẹ, gần gũi (Breathy)            | Video tâm sự đêm muộn, tóm tắt sách tâm lý học                              |
| **12** | **Iapetus**       |     Nam     | Mạch lạc, chuẩn mực, khúc chiết (Clear)               | **Video lập trình, công nghệ IT, toán học, phân tích dữ liệu**         |
| **13** | **Umbriel**       |     Nam     | Thư thả, tự nhiên, không gò bó (Easy-going)          | Video podcast vẽ tay, câu chuyện đời thường mộc mạc                           |
| **14** | **Algieba**       |     Nam     | Mượt mà, lịch lãm, truyền cảm (Smooth)               | Video marketing, giới thiệu giải pháp dịch vụ cao cấp                           |
| **15** | **Despina**       |     Nữ     | Êm dịu, thanh lịch, uyển chuyển (Smooth)               | Video nghệ thuật, lịch sử hội họa, văn học                                     |
| **16** | **Erinome**       |     Nữ     | Sắc sảo, chuẩn xác, phát âm rõ từng chữ (Clear)    | **Video học thuật, giáo trình khoa học song ngữ Việt - Anh**              |
| **17** | **Algenib**       |     Nam     | Hơi khàn, dày dặn, trải đời (Gravelly)               | Video tóm tắt tiểu sử nhân vật, bài học kinh doanh xương máu                |
| **18** | **Rasalgethi**    |     Nam     | Phong thái chuyên gia, đáng tin cậy (Informative)      | **Video báo cáo thị trường, kinh doanh, đào tạo chuyên sâu**           |
| **19** | **Laomedeia**     |     Nữ     | Vui tươi, phấn khởi, lôi cuốn (Upbeat)                | Video gamification, hoạt động nhóm, ý tưởng sáng tạo                          |
| **20** | **Achernar**      |     Nữ     | Dịu dàng, đằm thắm, êm ái (Soft)                     | Video thiền định, tâm sự chia sẻ cảm xúc, chăm sóc bản thân                |
| **21** | **Alnilam**       |     Nam     | Đĩnh đạc, dứt khoát, quyền lực (Firm)               | Video định hướng chiến lược, quy tắc lãnh đạo, chính sách                 |
| **22** | **Schedar**       |     Nam     | Cân bằng, đều nhịp, trung tính (Even)                 | Video tài liệu khoa học, quy trình vận hành chuẩn (SOP)                         |
| **23** | **Gacrux**        |     Nữ     | Chững chạc, từng trải, đáng kính (Mature)            | Video bài học làm cha mẹ, đạo lý sống, kinh nghiệm quản lý                  |
| **24** | **Pulcherrima**   |     Nam     | Trực diện, thẳng thắn, dứt khoát (Forward)            | Video phê bình, tranh biện, giải quyết nút thắt tư duy                         |
| **25** | **Achird**        |     Nam     | Thân mật, như một người bạn đồng hành (Friendly)  | **Video Whiteboard phong cách gia sư / người hướng dẫn (tutor/coach)**    |
| **26** | **Zubenelgenubi** |     Nam     | Bình dân, gần gũi, đời thường (Casual)              | Video giải thích khái niệm phức tạp bằng ngôn ngữ bình dân                  |
| **27** | **Vindemiatrix**  |     Nữ     | Nhẹ nhàng, khiêm nhường, kiên nhẫn (Gentle)          | Video giáo dục trẻ em, bài học tiếng Anh vỡ lòng cho người mới              |
| **28** | **Sadachbia**     |     Nam     | Nhanh nhẹn, hóm hỉnh, bắt tai (Lively)                  | Video tin tức công nghệ, review nhanh xu hướng                                    |
| **29** | **Sadaltager**    |     Nam     | Trí tuệ, học giả, am tường (Knowledgeable)            | **Video nghiên cứu khoa học, lịch sử thế giới, phân tích case-study**   |
| **30** | **Sulafat**       |     Nữ     | Ấm áp, truyền cảm hứng, giàu cảm xúc (Warm)         | **Video truyền động lực, kể chuyện thành công, thông điệp ý nghĩa** |
