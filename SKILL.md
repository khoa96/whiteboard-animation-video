---
name: whiteboard-video
description: Làm video vẽ tay bảng trắng (whiteboard animation) trên nền trắng thuần (#FFFFFF) từ một chủ đề, một kịch bản lời dẫn hoặc file phụ đề SRT, ra thành phẩm hoàn chỉnh có giọng đọc và phụ đề. Tối ưu cho giải thích kiến thức khoa học, đời sống, xã hội và bài giảng tiếng Anh. Quy trình - chủ đề → viết kịch bản 2 cột & phản biện trực quan → tạo giọng đọc sinh SRT theo giọng thật, hoặc đọc SRT → phân cảnh theo khối tri thức & chọn layout linh hoạt → tạo ảnh nét vẽ minh họa sơ đồ/từ khóa/câu ví dụ → chia vùng (annotation.json / sequence / startMs / protectedRegions, gán type text/box/arrow/underline/circle/colored_image) → chỉnh trên trang xem trước → render MP4 bằng nét bút liền mạch (tỉ lệ 90:10, 90% đi nét ink → 10% quét màu color siêu tốc; chữ và sơ đồ 100% ink) → ghép cảnh, gắn phụ đề, ghép giọng đọc. Dùng khi người dùng đưa chủ đề, kịch bản/lời dẫn hoặc file SRT và muốn làm video vẽ tay bảng trắng hoàn chỉnh.
---
# Video vẽ tay bảng trắng (whiteboard animation giải thích kiến thức & bài giảng)

Biến phụ đề và nội dung thuyết trình thành video vẽ tay bảng trắng sinh động. **Dàn dựng** theo cơ chế mặt nạ từng vùng: các vùng hiện ra lần lượt theo mạch bài giảng, vùng chưa tới lượt bị ẩn hoàn toàn, chỗ chồng lấn được bảo vệ bằng `protectedRegions`. **Cách vẽ** là nét bút liền mạch: trong phạm vi được phép của mỗi vùng, đầu bút trượt liên tục theo khung xương/lưới để đi nét (`ink`) rồi quét màu siêu tốc (`color`). Mọi vùng dùng chung một canvas, vùng đã vẽ xong được giữ lại để tạo nên một không gian tri thức tích lũy (Progressive Knowledge Canvas).

**Ngôn ngữ:** mọi lời giải thích, phân cảnh, nhãn vùng (`label`), `narrativeRole`, ghi chú, kịch bản và giao diện gửi cho người dùng đều viết bằng **tiếng Việt**, trừ khi người dùng yêu cầu ngôn ngữ khác.

Khác với kiểu nhảy từng khung hay xoá hình chữ nhật thô sơ, nét bút ở đây **chảy liền mạch**. Khác với kiểu vẽ cả ảnh một lượt hỗn loạn, skill này vẽ **theo từng vùng ứng với tiến trình bài giảng**, kiểm soát chính xác thứ tự và nhịp điệu xuất hiện của từng từ khóa, sơ đồ và hình vẽ.

## Tham số mặc định

| Hạng mục           | Yêu cầu mặc định                                                                                                                                           |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nền bảng**       | **Nền trắng thuần (`#FFFFFF`) cho 100% tất cả các chủ đề và video.** Tạo cảm giác bảng mica học đường hiện đại, độ tương phản sắc nét nhất cho nét bút đen và các màu nhấn. Cấm nền kem cũ, nền hoa văn hay vân giấy đốm. |
| **Cách vẽ & Tỉ lệ pha** | • **Đi nét phác thảo (`ink`): Chiếm 90% thời lượng của vùng.** Nét bút trượt liên tục để định hình khung tranh, chữ viết hoặc sơ đồ.<br>• **Tô màu siêu tốc (`color`): Chiếm tối đa 10% thời lượng của vùng.** Chỉ kích hoạt khi vùng có mảng màu thực sự. Đầu cọ lướt nhanh dứt khoát 1 nhịp để bung màu gốc, cấm di bút qua lại nhiều lần làm rối mắt.<br>• **Chữ viết, câu ví dụ, khung, mũi tên, sơ đồ nét đơn:** Dành **100% thời gian cho `ink`** (`colorMode: none`), thời gian tô màu = 0. |
| **Đường bút**        | `--ink-path grid` (lưới, mặc định, ổn định) hoặc `skeleton` (bám khung xương, hợp với nét vẽ mảnh).                                         |
| **Kiểu tô màu**       | `--color-fill contour-wipe` (quét theo viền nhanh, mặc định) hoặc `brush` (vệt cọ lướt nhanh).                                                             |
| **Vùng chưa vẽ**      | Phạm vi được phép của một vùng = khung `region` trừ đi các vùng vẽ sau và `protectedRegions`; vùng chưa tới lượt ẩn hoàn toàn.        |
| **Nguồn thời lượng** | `sceneDurationMs` của mỗi ảnh lấy từ khoảng thời gian phụ đề của cảnh đó (nên 20–35 giây/cảnh).                                             |
| **Khung chỉnh sửa**    | Trang xem trước mặc định hiện mọi khung vùng có đánh số; khung này không thuộc nội dung video.                                                  |

## Quy chuẩn Thiết kế Thị giác, Chữ viết & Sơ đồ Tư duy (Bắt buộc)

Bảng trắng sinh ra để **trực quan hóa bài thuyết trình và bài giảng**, không phải là nơi đọc chép tài liệu:

### 1. Quy tắc Chữ viết (Typography & Linguistic Elements)
- **Không bê nguyên si lời nói lên bảng (No Verbatim Clutter):**
  - Tuyệt đối không biến bảng trắng thành một slide chật ních chữ hay trang sách giáo khoa.
  - Giọng đọc (Voice-over) đảm nhận việc phân tích, giải thích chi tiết, dẫn dắt câu chuyện.
  - Bảng trắng chỉ hiển thị **Ngữ liệu trọng tâm, từ khóa mỏ neo và cấu trúc cần phân tích**.
- **Đối với Bài giảng Tiếng Anh (Language Teaching):**
  - **Được phép viết câu ví dụ dài (Full example sentences):** Để làm ngữ cảnh phân tích trực quan (ví dụ: *"She has lived in London since 2018."*).
  - **Được phép viết đầy đủ các yếu tố ngôn ngữ sư phạm:**
    - Từ vựng (Vocabulary) kèm từ loại: `noun`, `verb`, `adj`.
    - Phiên âm quốc tế chuẩn IPA: ví dụ `/ˌpreznˈteɪʃn/`, `/ˈpreznt/`.
    - Công thức & mẫu câu ngữ pháp: ví dụ `Subject + have/has + V3/Ved`.
    - Cặp từ đối chiếu / Cụm từ cố định (Collocations / Antonyms).
    - Câu hỏi trắc nghiệm & các lựa chọn (A, B, C, D).
- **Đối với Video Khoa học, Đời sống & Xã hội (Science & Explainer):**
  - Chữ chỉ giới hạn ở: **Tiêu đề cảnh**, **Từ khóa mỏ neo (Keywords)**, **Ký hiệu/Thuật ngữ khoa học** ($H_2O$, $CO_2$, Quang hợp), **Số liệu nổi bật**, và **Nhãn chú thích sơ đồ (Callouts)**.
- **Font chữ:** Dùng font Sans-serif rõ ràng, sạch sẽ (Arial, Helvetica, Inter). Không để AI tự sinh chữ nguệch ngoạc méo mó; các từ khóa/câu ví dụ phải sắc nét, chuẩn xác.

### 2. Tư duy Sơ đồ & Trực quan hóa (Diagrams & Mindmaps)
- Chuyển đổi tối đa các cơ chế và quan hệ logic thành **Sơ đồ trực quan**:
  - **Sơ đồ tư duy (Mindmap) / Sơ đồ khối (Flowchart):** Thể hiện các nhánh ý niệm, chu trình hoặc phân loại.
  - **Mũi tên liên kết (`arrow`):** Dẫn dắt ánh mắt từ nguyên nhân sang kết quả.
  - **Khung bao (`box`):** Đóng khung công thức hoặc quy tắc cốt lõi cần ghi nhớ.
  - **Gạch chân (`underline`) & Khoanh tròn (`circle`):** Làm nổi bật từ khóa trong câu ví dụ, khoanh tròn đáp án trắc nghiệm đúng, chỉ dấu hiệu nhận biết.

### 3. Thư viện Layout Sư phạm linh hoạt (Tùy biến theo nội dung)
Cấm áp dụng một bố cục rập khuôn duy nhất. Tùy vào nội dung bài giảng để chọn layout:
- **Layout So sánh Đối chiếu (Split A vs B):** Hai cột song song (Số ít vs Số nhiều, Hiện tại hoàn thành vs Quá khứ đơn, Động vật biến nhiệt vs Hằng nhiệt).
- **Layout Chu trình / Tuyến tính (Process Flow):** Các bước nối tiếp theo trục ngang hoặc vòng tròn xoay chiều (Quá trình cây hút nước, Vòng tuần hoàn nước, Quy trình sản xuất).
- **Layout Tâm điểm tỏa nhánh (Central Mindmap):** Khái niệm cốt lõi ở trung tâm, tỏa ra các nhánh tính chất, từ vựng liên quan.
- **Layout Cây phân cấp (Hierarchy Tree):** Phân loại danh từ (Đếm được / Không đếm được), tháp nhu cầu, hệ thống phân loại sinh học.
- **Layout Trắc nghiệm & Phân tích (Quiz & Breakdown):** Câu hỏi ở trên → Câu ví dụ với từ khóa được gạch chân → Khoanh tròn đáp án đúng → Khung tóm tắt quy tắc bên dưới.

### 4. Màu sắc & Phong cách vẽ
- **Nền:** Trắng sạch tinh `#FFFFFF`.
- **Nét phác:** Mực đen / xám đậm (`#1F2937`), nét vẽ tay tối giản phong cách Notion.
- **Màu nhấn:** Dùng tiết chế tối đa 3 màu: **Xanh dương (`#2563EB`)** cho liên kết/khái niệm, **Đỏ/Cam (`#DC2626` / `#EA580C`)** cho trọng tâm/khoanh tròn đáp án/lưu ý.
- **Tuyệt đối cấm:** Phong cách ảnh chụp tả thực (photorealistic), hiệu ứng 3D đổ bóng phức tạp, chất liệu tranh sơn dầu; hình nền dày đặc kín mít không có khoảng thở; chi tiết trang trí rườm rà không phục vụ việc giải thích nội dung.
- **Ngoại lệ bàn tay vẽ:** nếu người dùng nói rõ chữ trên thân bút trong `drawing-hand.png` là dấu nhận diện của họ và muốn giữ, thì được giữ; nó không tính là chữ trong ảnh cảnh.

## Điểm dừng xác nhận (bắt buộc)

Trong quy trình mặc định, **sau mỗi bước phải dừng lại và chờ người dùng xác nhận rõ ràng** rồi mới sang bước tiếp. Trước khi được xác nhận, không được tạo ảnh, annotation, ảnh xem trước, video hay file ghép của bước sau. Không được coi "chưa trả lời", "đã cho phép chung chung trước đó" hay "người dùng không phản đối" là xác nhận. Khi người dùng yêu cầu sửa bước trước, chỉ làm lại đúng bước đó, xong lại chờ xác nhận.

Ngoại lệ duy nhất: **tạo xong file annotation JSON thì phải lập tức mở trang xem trước và nạp thư mục chứa JSON đó**. Việc này thuộc kết quả của bước 3, không cần chờ xác nhận riêng. Nếu File System Access API của trình duyệt đòi thao tác của người dùng, dùng giao diện trình duyệt chọn đúng thư mục đã biết; không được vì thế mà hỏi thêm xác nhận hay bảo người dùng tự mở.

## Ba kiểu đầu vào

| Người dùng đưa                              | Bắt đầu từ bước                                         |
| ------------------------------------------------ | ------------------------------------------------------------- |
| **Chủ đề** (một câu, một ý tưởng) | Bước 0a: viết kịch bản                                   |
| **Kịch bản / lời dẫn** (đoạn văn)   | Bước 0b: tạo giọng đọc, sinh SRT                        |
| **File SRT**                               | Bước 1 (quy trình gốc); làm xong có thể thêm bước 8 |

Khi bắt đầu từ chủ đề hoặc kịch bản, dùng **giọng đọc dẫn nhịp**: tạo giọng trước, lấy độ dài giọng thật để sinh SRT; phân cảnh và thời gian vẽ đều theo SRT này, nên video tự nhiên không có khoảng lặng thừa, không cần bước nhịp gọn.

## Quy trình

0a. **Viết kịch bản sư phạm 2 cột & Phản biện trực quan (chỉ khi đầu vào là chủ đề).** Dựa vào chủ đề, thời lượng mục tiêu (mặc định 60 giây, khoảng 180–220 từ tiếng Việt hoặc 130–160 từ tiếng Anh), người xem và giọng văn. Phân bổ theo Khối Tri thức: mở đầu gây tò mò (5–8s) → các cảnh phát triển ý (20–35s/cảnh) → kết luận đọng lại (5–8s). Mỗi câu đọc không quá 3.5s – 5.0s (dưới 15 từ). Lưu vào `assets/whiteboard/<tên-dự-án>/script.md` theo cấu trúc 2 cột:
    - **Cột Thoại (Narration):** Lời giảng giải súc tích, tự nhiên, nhịp nhàng.
    - **Cột Thị giác (Visual Action):** Định hướng layout áp dụng (So sánh / Chu trình / Mindmap / Cây phân cấp / Quiz), các từ khóa mỏ neo, câu ví dụ tiếng Anh (nếu có), icon minh họa và các cử chỉ sư phạm (`arrow`, `underline`, `circle`, `box`). Tuyệt đối không bê nguyên lời nói lên bảng.
    - **Tự phản biện kịch bản:** Đảm bảo mỗi câu đều có hành động vẽ cụ thể tương ứng, thời lượng câu đủ cho nét vẽ hoàn thành.
    **Xong thì dừng, chờ người dùng duyệt kịch bản & phương án thị giác.**

0b. **Tạo giọng đọc, sinh SRT (đầu vào chủ đề/kịch bản).** Chỉ làm sau khi kịch bản được duyệt:

```bash
   python scripts/script_to_srt.py script.md --output draft.srt        # cắt câu; dòng cuối PAUSES=…
   <ENV_PY> scripts/tts_narration.py draft.srt --output narration.m4a \
       --retime-out input.srt --pause <từng mục trong PAUSES>            # độ dài giọng thật → mốc chính thức
```

   `input.srt` là phụ đề cho mọi bước sau; `narration.m4a` là giọng đọc cuối cùng (bước 8 dùng lại cache). Báo cho người dùng: cách cắt câu, tổng thời lượng, giọng đã dùng, và mời nghe thử `narration.m4a`. Giọng/tốc độ/engine lấy theo `.env` (`TTS_PROVIDER` / `TTS_VOICE` / `TTS_SPEED`); người dùng chỉ định thì dùng `--provider` / `--voice` / `--speed`. **Xong thì dừng, chờ người dùng duyệt giọng đọc và cách cắt câu.**

1. **Đọc phụ đề, lên phương án hình & chọn layout (chưa tạo ảnh).** Dùng `scripts/parse_srt.py` tách SRT thành từng câu và gợi ý chia cảnh 20–35 giây/cảnh theo từng Khối Tri thức. Từ đó đưa ra phương án: mỗi cảnh có số thứ tự, ý chính, dạng layout (So sánh, Chu trình, Mindmap, Quiz...), các đối tượng/từ khóa/câu ví dụ trong hình, khoảng phụ đề tương ứng và `sceneDurationMs`. Mỗi cảnh chỉ một ý chính trọn vẹn. **Xong thì dừng, chờ duyệt phương án.**
2. **Tạo ảnh nét vẽ.** Chỉ làm sau khi phương án được duyệt. Theo "Quy chuẩn Thiết kế Thị giác & Chữ viết", tạo từng ảnh 16:9 nền trắng thuần `#FFFFFF`. Bố cục thông thoáng, các đối tượng và từ khóa/công thức/câu ví dụ cách nhau đủ rộng để dễ chia vùng; nét vẽ tối giản Notion, chữ sắc nét rõ ràng, không có yếu tố trái quy chuẩn. Nếu không tự tạo ảnh được, ghi prompt từng cảnh vào `IMAGE_PROMPTS.md` và nhờ người dùng tạo, lưu đúng tên `scene-XX-<tên>.png`. **Xong thì dừng, cho xem ảnh và chờ duyệt.**
3. **Đọc phụ đề trước, xem ảnh sau, rồi chia vùng và mở trang xem trước.** Chỉ làm sau khi ảnh được duyệt. Đọc phụ đề của cảnh, **thực sự mở xem ảnh** và lấy kích thước pixel gốc; không được đoán hình chỉ từ phụ đề, cũng không được xếp thứ tự máy móc theo vị trí. Rút ra các sự kiện/từ khóa trong phụ đề, gắn từng đối tượng nhìn thấy trong ảnh với sự kiện, xếp thứ tự vẽ theo mạch sư phạm "tiêu đề → đối tượng/câu ví dụ → phân tích/từ khóa → cử chỉ nhấn mạnh (arrow, underline, circle, box) → kết luận". Gán đúng trường `type` (`text`, `box`, `underline`, `circle`, `arrow`, `colored_image`, `icon`) và `colorMode` (`"none"` cho chữ/kết cấu nét; `"wash"` hoặc `"auto"` cho icon có màu). Sau đó tạo `<tên-ảnh>.annotation.json`. Tạo xong, lập tức mở `assets/preview.html` bằng trình duyệt mặc định và dùng nút "Mở thư mục" nạp **thư mục chứa file annotation** (toàn bộ `<tên>.png` + `<tên>.annotation.json`); không được chỉ đưa đường dẫn hay bảo người dùng tự làm. **Trang xem trước đã nạp xong thì dừng, chờ duyệt annotation và bản xem trước.**
4. **Xuất ảnh kiểm tra vùng.** Chỉ làm sau khi annotation được duyệt. Dùng `render_annotation_preview.py` xuất ảnh đánh số/hướng vẽ, đối chiếu: thứ tự vùng khớp mạch truyện, mọi vùng nằm trong ảnh, đối tượng chồng lấn đã được `protectedRegions` bảo vệ. **Xong thì dừng, chờ duyệt ảnh kiểm tra.**
5. **Chỉnh và lưu trên trang xem trước.** Chỉ làm sau khi ảnh kiểm tra được duyệt, trên trang xem trước đã mở và nạp đúng thư mục. Mặc định (chưa phát) hiện ảnh đầy đủ và các khung vùng. Canvas là **bản mô phỏng bằng hình chữ nhật**: kéo cạnh/góc để sửa `region`; khung bên phải sửa tên, hướng, **bắt đầu (ms) / kết thúc (ms)** (thời lượng = kết thúc − bắt đầu, chỉ đọc) và **phụ đề**; kéo danh sách để **đổi thứ tự** (tự đánh lại `sequence`); chọn vùng nào thì phụ đề tương ứng được tô sáng; kéo thanh thời gian hoặc bấm phát để xem (vùng chưa tới lượt không hiện); `direction` chỉ ảnh hưởng bản mô phỏng. Sửa xong bấm "Lưu cảnh này / Lưu tất cả" để ghi lại `.annotation.json` gốc (kèm `subtitle` của từng vùng, và đặt `sceneDurationMs` = thời điểm vùng cuối kết thúc + 0,5 giây). **Lưu xong thì dừng, chờ duyệt annotation và thời gian cuối cùng.**
6. **Render bằng dòng lệnh.** Chỉ làm sau khi annotation và thời gian được duyệt. Dùng `render_stream_whiteboard.py` render từng cảnh ra MP4 (nền trắng `#FFFFFF`, tỉ lệ `ink:color = 90:10`), kiểm tra ba thời điểm: mở đầu, giữa một vùng có chồng lấn, và cuối cảnh. **Xong thì dừng, chờ duyệt video từng cảnh.**
7. **Ghép các cảnh (khi có nhiều cảnh).** Chỉ làm sau khi mọi cảnh được duyệt. Dùng `merge_scenes.py` ghép theo thứ tự thành một video. **Xong thì dừng, chờ duyệt video ghép.**
8. **Gắn phụ đề + ghép giọng đọc (mặc định với đầu vào chủ đề/kịch bản; với đầu vào SRT thì làm khi người dùng yêu cầu).** Chỉ làm sau khi video ghép được duyệt. Trước hết dùng filter `subtitles` của ffmpeg gắn `input.srt` vào hình (chữ xám đậm viền trắng sắc nét, nổi bật trên nền bảng trắng, xem mục "Lệnh" bước 8), sau đó chạy `tts_narration.py input.srt --video <video có phụ đề>` để ghép giọng (lấy từ cache, không gọi lại API). Kiểm tra khung đầu/giữa/cuối và phân bố khoảng lặng (`silencedetect`), bảo đảm giọng, phụ đề và hình khớp nhau. **Xong thì dừng, bàn giao video cuối.**

## Thư mục dự án

Tạo trong dự án của người dùng:

```text
assets/whiteboard/<tên-dự-án>/
  script.md                            # kịch bản (nếu bắt đầu từ chủ đề/kịch bản)
  input.srt                            # phụ đề chính thức
  scene-01-<tên>.png
  scene-01-<tên>.annotation.json       # cùng tên với png
  scene-01-<tên>-whiteboard.mp4        # video cảnh
  scene-01-<tên>-preview.mp4           # đoạn xem thử (trang xem trước tạo, độ phân giải thấp)
  tts-cache/                           # giọng đọc từng câu (dùng lại, không tốn phí lần 2)
```

Ảnh và cấu hình phải cùng tên: `foo.png` ↔ `foo.annotation.json`. Trang xem trước dựa vào đó để tự nạp cấu hình.

## Xếp thứ tự theo nghĩa và toạ độ pixel (bắt buộc)

1. **Căn cứ đọc:** trước khi chia vùng phải có cả phụ đề lẫn ảnh gốc đã được mở xem. Thiếu một trong hai thì hỏi trước, không được tạo annotation.
2. **Căn cứ thứ tự:** `sequence`, `startMs` và `label` phải phản ánh trình tự sự kiện trong phụ đề, không chỉ theo trái→phải, trên→dưới hay độ nổi bật.
3. **Căn cứ toạ độ:** mỗi vùng ghi `x`, `y`, `width`, `height` bằng số nguyên pixel trên hệ toạ độ ảnh gốc, gốc ở góc trên bên trái; cấm phần trăm, tỉ lệ, toạ độ ước lượng hay bỏ trống kích thước. `canvas.width` / `canvas.height` phải bằng đúng kích thước pixel ảnh gốc.
4. **Trường của mỗi vùng:** gồm `sequence`, `narrativeRole`, `subtitle`, `region`, `reveal`, `handPath`. `narrativeRole` mô tả bằng tiếng Việt vai trò của vùng trong mạch truyện; `subtitle` lưu câu phụ đề ứng với vùng (lấy từ SRT, để trang xem trước liên kết và dùng về sau); `sequence` liên tục từ 1.
5. **Kiểm tra:** trước khi xuất ảnh kiểm tra, xem từng vùng có nằm trong ảnh, có phủ đúng đối tượng, có khớp sự kiện phụ đề không; đối tượng chồng lấn phải được `protectedRegions` bảo vệ rồi mới vẽ.

## Mô hình thời gian & Phân loại đối tượng vẽ (chuẩn 90:10)

- **Tổng thời lượng cảnh** `sceneDurationMs` lấy từ khoảng phụ đề của cảnh (`scenes[].sceneDurationMs` của `parse_srt.py`).
- **Các vùng vẽ nối tiếp:** chỉ có một cây bút, nên các vùng trong cùng cảnh nên **nối tiếp nhau về thời gian** (`startMs` không chồng lên nhau): vùng sau bắt đầu tại `startMs + durationMs` của vùng trước (có thể thêm 100–300 ms nghỉ). Nếu `startMs` chồng nhau, renderer vẫn xử lý theo thứ tự, nhưng nhìn sẽ không còn là vẽ song song.
- **Phân loại đối tượng và tỉ lệ vẽ ink:color = 90:10:**
  - **Nhóm Chữ, Câu ví dụ, Sơ đồ & Cử chỉ (`text`, `box`, `underline`, `circle`, `arrow`):**
    - Đặt `type` tương ứng và `colorMode: "none"`.
    - Dành **100% thời gian cho `ink`**, thời gian tô màu = 0 (`color_frames = 0`).
  - **Nhóm Minh họa có mảng màu (`colored_image`, `icon` có màu nhấn):**
    - Chia theo tỉ lệ chuẩn mực **`ink:color = 90:10`**.
    - Pha đi nét `ink` chiếm 90% thời lượng của vùng; pha tô màu `color` chiếm tối đa 10% (khoảng 0.2s – 0.5s), cọ quét lướt nhanh dứt khoát 1 nhịp để bung màu, tuyệt đối không di bút qua lại nhiều lần.
  - **Nhóm Minh họa nét đơn sắc (`line_art`):** 100% thời gian cho `ink`.
- **Giữ hình cuối:** vẽ xong mọi vùng thì tự kéo dài tới `sceneDurationMs`, bảo đảm cuối cảnh giữ ảnh hoàn chỉnh ít nhất 0,5 – 1.0 giây để người xem kịp ghi chép và ghi nhớ toàn bộ bài học.
- `reveal.direction` với cách vẽ nét liền **không quyết định nét bút thật** (nét bút do khung xương/lưới tự sinh), chỉ dùng cho bản mô phỏng trên trang xem trước; giữ lại để trang xem trước hoạt động.

## Bất biến của mặt nạ (tầng dàn dựng, bắt buộc)

- Tại thời điểm `t`, một vùng chỉ được hiện các pixel khi `reveal.startMs ≤ t` và không vượt quá tiến độ vẽ hiện tại; vùng chưa bắt đầu không được lộ bất kỳ nét, mảng màu hay hình ảnh nào.
- **Phạm vi được phép** của mỗi vùng = khung `region` trừ đi `region` của **mọi vùng vẽ sau**, rồi trừ tiếp `reveal.protectedRegions` của chính nó. Nét bút bị giới hạn trong phạm vi này nên vùng sau không bị lộ sớm.
- `protectedRegions` dùng cùng hệ toạ độ pixel nguyên như `region`, dùng khi khung quá rộng, đối tượng chồng nhau hoặc nét nền có thể lộ ra.
- Renderer đã thực hiện đúng trình tự "chỉ vẽ trong phạm vi được phép → vùng sau và vùng bảo vệ tự nhiên không bị chạm"; bản mô phỏng trên trang xem trước dùng phép trừ `destination-out` tương đương để minh hoạ cùng cách dàn dựng.

## Ví dụ cấu hình

```json
{
  "sceneId": "scene-01",
  "canvas": { "width": 1920, "height": 1080 },
  "storyBasis": "Bài giảng tiếng Anh mẫu: Cấu trúc câu và từ khóa",
  "sceneDurationMs": 10000,
  "elements": [
    {
      "id": "title",
      "label": "Tiêu đề bài học",
      "type": "text",
      "colorMode": "none",
      "sequence": 1,
      "narrativeRole": "Giới thiệu chủ đề ngữ pháp",
      "subtitle": "Hôm nay chúng ta sẽ tìm hiểu thì Hiện tại hoàn thành.",
      "region": { "x": 100, "y": 60, "width": 1100, "height": 95 },
      "reveal": { "direction": "left_to_right", "startMs": 300, "durationMs": 1800, "maskPaddingPx": 10, "protectedRegions": [] }
    },
    {
      "id": "example_sentence",
      "label": "Câu ví dụ dài",
      "type": "text",
      "colorMode": "none",
      "sequence": 2,
      "narrativeRole": "Ngữ liệu ví dụ để phân tích",
      "subtitle": "Ví dụ: Cô ấy đã sống ở Luân Đôn từ năm 2018.",
      "region": { "x": 100, "y": 200, "width": 1250, "height": 85 },
      "reveal": { "direction": "left_to_right", "startMs": 2300, "durationMs": 2500, "maskPaddingPx": 10, "protectedRegions": [] }
    },
    {
      "id": "underline_since",
      "label": "Gạch chân dấu hiệu since 2018",
      "type": "underline",
      "colorMode": "none",
      "sequence": 3,
      "narrativeRole": "Nhấn mạnh dấu hiệu nhận biết thì",
      "subtitle": "Từ 'since 2018' là mốc thời gian rõ ràng trong quá khứ.",
      "region": { "x": 650, "y": 265, "width": 260, "height": 25 },
      "reveal": { "direction": "left_to_right", "startMs": 5000, "durationMs": 800, "maskPaddingPx": 5, "protectedRegions": [] }
    },
    {
      "id": "badge_icon",
      "label": "Icon minh họa đồng hồ thời gian",
      "type": "colored_image",
      "colorMode": "wash",
      "sequence": 4,
      "narrativeRole": "Biểu tượng trực quan hóa khái niệm thời gian",
      "subtitle": "Hành động bắt đầu trong quá khứ và kéo dài đến hiện tại.",
      "region": { "x": 1450, "y": 150, "width": 380, "height": 450 },
      "reveal": { "direction": "top_to_bottom", "startMs": 6000, "durationMs": 2800, "maskPaddingPx": 10, "protectedRegions": [] }
    }
  ]
}
```

> `direction` / `handPath` chỉ dùng cho bản mô phỏng trên trang xem trước; nét bút trong video do renderer tự sinh, không cần chỉnh kỹ.

## Lệnh

Mọi script render chạy bằng Python trong `.venv` của skill (cô lập thư viện). `<ENV_PY>` là `.venv\Scripts\python.exe` (Windows) hoặc `.venv/bin/python` (macOS/Linux).

1. **Chuẩn bị môi trường** (lần đầu hoặc khi thiếu thư viện):
   ```bash
   python scripts/prepare_env.py --check   # chỉ kiểm tra; thành công thì dòng cuối in ENV_PY=<đường dẫn>
   python scripts/prepare_env.py           # thiếu thì tạo .venv và cài opencv-python/numpy/av/Pillow/edge-tts
   ```
2. **Kịch bản → SRT nháp** (đầu vào chủ đề/kịch bản): cắt theo câu (lời thoại trong ngoặc kép không bị tách, câu quá dài cắt ở dấu phẩy, câu quá ngắn gộp với câu sau); dòng tiêu đề `#` và dòng trống không được đọc; dòng trống chia đoạn, dòng cuối `PAUSES=` liệt kê số thứ tự câu cuối mỗi đoạn, dùng làm các tham số `tts_narration.py --pause`.
   ```bash
   python scripts/script_to_srt.py script.md --output draft.srt [--max-chars 80] [--min-chars 12]
   ```
3. **Đọc phụ đề + gợi ý chia cảnh:**
   ```bash
   python scripts/parse_srt.py <phụ-đề.srt> --target-sec 30 --min-sec 25 --max-sec 35
   ```
4. **Ảnh kiểm tra vùng (đánh số):**
   ```bash
   <ENV_PY> scripts/render_annotation_preview.py <ảnh> <annotation> <ảnh-kiểm-tra>
   ```
5. **Trang xem trước (không cần server):** mở `assets/preview.html` bằng Chrome / Edge, bấm "Mở thư mục" chọn thư mục → nạp mọi ảnh + annotation cùng tên → kéo chỉnh → "Lưu" ghi lại file gốc. Ghi trực tiếp cần File System Access API (Chrome/Edge); trình duyệt khác thì tải về rồi chép đè thủ công. Render vẫn chạy bằng dòng lệnh (bước 6).
6. **Render một cảnh:**
   ```bash
   <ENV_PY> scripts/render_stream_whiteboard.py <ảnh> <annotation> <ra.mp4> assets/drawing-hand.png \
       [--ink-path grid|skeleton] [--color-fill contour-wipe|brush] [--canvas-hex #FFFFFF] [--total-ms <mili-giây>]
   ```

   Không có `--total-ms` thì dùng `sceneDurationMs` trong annotation. Mặc định nền canvas trắng thuần `#FFFFFF`, tỉ lệ đi nét:tô màu là 90:10. Dòng cuối in `OUTPUT=<đường dẫn>`.
7. **Ghép các cảnh:**
   ```bash
   <ENV_PY> scripts/merge_scenes.py --inputs canh1.mp4 canh2.mp4 canh3.mp4 --output final.mp4
   ```
8. **Gắn phụ đề** (chữ xám đậm viền trắng sắc nét, nổi bật trên nền bảng trắng, không đè nét vẽ):
   ```bash
   ffmpeg -i final.mp4 -vf "subtitles=input.srt:force_style='FontName=Arial,FontSize=15,PrimaryColour=&H001F2937,OutlineColour=&H00FFFFFF,BorderStyle=1,Outline=2,Shadow=0,MarginV=16'" \
       -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart final-sub.mp4
   ```

   Trên Windows, đường dẫn trong `subtitles=` nên là đường dẫn tương đối (tránh dấu hai chấm của ổ đĩa bị hiểu nhầm là cú pháp filter).
9. **Giọng đọc:** tạo giọng từng câu theo SRT, khớp mốc thời gian rồi ghép vào video (không render lại hình). Engine `--provider vbee|edge` (mặc định theo `TTS_PROVIDER` trong `.env`): `vbee` cần `VBEE_APP_ID` / `VBEE_ACCESS_TOKEN`, tính phí theo ký tự, `--voice` là **mã giọng đầy đủ** copy từ giao diện Vbee (gửi nguyên văn cho API); `edge` dùng [rany2/edge-tts](https://github.com/rany2/edge-tts), miễn phí, mặc định `vi-VN-NamMinhNeural` (nữ: `vi-VN-HoaiMyNeural`). Tốc độ `--speed` (1.0 = bình thường; với Edge, 1.1 → `+10%`). Giọng từng câu được lưu ở `<thư-mục-srt>/tts-cache/`, chạy lại không gọi API lần nữa.
   ```bash
   <ENV_PY> scripts/tts_narration.py <phụ-đề.srt> --output narration.m4a --video final-sub.mp4 \
       [--provider vbee|edge] [--voice <mã-giọng>] [--speed 1.1]
   ```

   Dòng cuối in `OUTPUT=<video có giọng>` (mặc định `<video>-voice.mp4`). Câu nào dài hơn khung thời gian thì tự tăng tốc và cảnh báo. Mặc định cắt khoảng lặng đầu/cuối mỗi câu (tắt bằng `--no-trim`).
10. **Nhịp gọn (tuỳ chọn, cho đầu vào SRT có nhiều khoảng lặng):** sắp lại phụ đề theo độ dài giọng thật, rồi co giãn thời gian vẽ trong annotation theo từng đoạn tuyến tính; render lại thì hình và giọng khớp nhau, gần như không có khoảng trống:
    ```bash
    <ENV_PY> scripts/tts_narration.py input.srt --output narration.m4a --provider edge \
        --retime-out input.tight.srt --gap 0.3 --pause 6=0.8 --tail 1.0
    <ENV_PY> scripts/retime_annotations.py --old-srt input.srt --new-srt input.tight.srt \
        --annotations canh1.annotation.json canh2.annotation.json   # ra <tên>.tight.annotation.json, file gốc giữ nguyên
    ```

    Sau đó render các cảnh bằng `.tight.annotation.json`, ghép, gắn phụ đề `input.tight.srt`, rồi chạy bước 9 với `input.tight.srt` (giọng lấy từ cache).

## Kiểm tra chất lượng

Trước/sau khi render, xác nhận:

- Khung đầu tiên là nền trắng thuần `#FFFFFF` sạch sẽ, chưa lộ nét nào.
- Đã đọc phụ đề tương ứng và thực sự xem ảnh gốc; `canvas` khớp kích thước ảnh, mọi `region` là pixel nguyên và nằm trong ảnh.
- `sequence`, `startMs` khớp trình tự bài giảng trong phụ đề; số thứ tự/nhãn/vùng trên ảnh kiểm tra lấy từ cùng một file annotation.
- Kiểm tra ba thời điểm: mở đầu, giữa một vùng chồng lấn, sau khi vẽ xong mọi vùng — vùng chưa vẽ không lộ, vùng bảo vệ không rò, khung cuối hiện đủ ảnh gốc.
- Đối tượng chữ và ký hiệu (`text`, `box`, `underline`, `circle`, `arrow`) đi nét sắc bén 100% ink, không bị pha màu đè lên; icon màu tô lướt cực nhanh (tối đa 10% thời lượng).
- Đầu bút bám sát nét đang vẽ; nét vẽ mảnh có thể dùng `--ink-path skeleton` cho nét bám hơn.
- Vẽ xong mọi vùng thì giữ bảng hoàn chỉnh ít nhất 0,5 – 1.0 giây để người xem kịp ghi chép.
- Ghép nhiều cảnh xong, thứ tự và thời lượng khớp phân cảnh.
- Có giọng đọc: giọng, phụ đề và hình khớp nhau; không có khoảng lặng dài ngoài các chỗ nghỉ cố ý.

Muốn đổi hiệu ứng thì chỉnh annotation (vùng/thứ tự/thời gian) trên trang xem trước (`assets/preview.html`) và lưu trước, rồi mới render bằng dòng lệnh; đừng render đi render lại khi chưa sửa gì.

