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

### PHẦN 2: MÃ NGUỒN TỔNG HỢP ÂM THANH (`create_audio.py`)

Engine sử dụng giọng đọc đa ngữ `en-US-AndrewMultilingualNeural` của Microsoft Edge-TTS:
- Đọc tiếng Việt chuẩn giọng Bắc, tự nhiên, truyền cảm.
- Tự động chuyển đổi mượt mà sang phát âm tiếng Anh Mỹ bản xứ khi gặp các từ tiếng Anh.

```python
#!/usr/bin/env python3
import asyncio
import subprocess
from pathlib import Path
import json
import edge_tts

DIR = Path(__file__).resolve().parent

sentences = [
    "Chào các bạn, trong tiếng Anh, mạo từ - Articles - được chia làm ba nhóm chính.",
    "Nhóm thứ nhất là A và AN - dùng cho một vật chung chung, ví dụ: a book - một cuốn sách, hay an apple - một quả táo.",
    "Nhóm thứ hai là THE - dùng khi vật đã được xác định cụ thể, ví dụ: the book - chính cuốn sách này.",
    "Và nhóm thứ ba là Zero Article - những trường hợp không dùng mạo từ, ví dụ như water - nước nói chung.",
    "Để học thật vững, hôm nay chúng ta sẽ bắt đầu với nhóm nền tảng đầu tiên: A và AN."
]

VOICE = "en-US-AndrewMultilingualNeural"

async def synthesize_all():
    print(f"Synthesizing {len(sentences)} lines with {VOICE}...")
    for idx, s in enumerate(sentences, 1):
        c = edge_tts.Communicate(s, VOICE)
        out_f = DIR / f"line_{idx}.mp3"
        await c.save(str(out_f))
        print(f"  Line {idx} generated: {s[:40]}...")

def assemble_audio():
    gap = 0.5       # Khoảng nghỉ giữa các câu: 0.5s
    lead_in = 0.5   # Khoảng nghỉ vào đầu scene: 0.5s
    current_time = lead_in
    srt_cues = []

    # 1. Đo chính xác thời lượng từng câu bằng ffprobe
    for idx, s in enumerate(sentences, 1):
        f_path = DIR / f"line_{idx}.mp3"
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(f_path)]
        dur = float(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip())
        
        start_time = current_time
        end_time = start_time + dur
        srt_cues.append({
            "index": idx,
            "startMs": int(round(start_time * 1000)),
            "endMs": int(round(end_time * 1000)),
            "durationMs": int(round(dur * 1000)),
            "text": s
        })
        current_time = end_time + gap

    tail = 2.0  # Khoảng giữ tĩnh cuối scene: 2.0s
    total_scene_ms = int(round((current_time - gap + tail) * 1000))
    print(f"Total scene duration: {total_scene_ms} ms ({total_scene_ms/1000:.2f} s)")

    # 2. Xuất file input.srt
    def format_srt_time(ms):
        h = ms // 3600000
        m = (ms % 3600000) // 60000
        s = (ms % 60000) // 1000
        sub_ms = ms % 1000
        return f"{h:02d}:{m:02d}:{s:02d},{sub_ms:03d}"

    srt_lines = []
    for cue in srt_cues:
        s_str = format_srt_time(cue["startMs"])
        e_str = format_srt_time(cue["endMs"])
        srt_lines.append(f"{cue['index']}\n{s_str} --> {e_str}\n{cue['text']}\n")

    (DIR / "input.srt").write_text("\n".join(srt_lines), encoding="utf-8")

    # 3. Mux các file mp3 thành một file narration.m4a liên tục với bộ lọc adelay
    inputs = []
    filter_str = ""
    for i, cue in enumerate(srt_cues):
        inputs.extend(["-i", str(DIR / f"line_{i+1}.mp3")])
        delay_ms = cue["startMs"]
        filter_str += f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];"
    mix_inputs = "".join(f"[a{i}]" for i in range(len(srt_cues)))
    filter_str += f"{mix_inputs}amix=inputs={len(srt_cues)}:dropout_transition=0:normalize=0[outa]"

    out_audio = DIR / "narration.m4a"
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_str, "-map", "[outa]", "-c:a", "aac", "-b:a", "192k", str(out_audio)]
    subprocess.run(cmd, check=True, capture_output=True)

    # 4. Xuất file timing_cues.json làm đồng hồ chủ cho Bước 3
    (DIR / "timing_cues.json").write_text(json.dumps({
        "totalDurationMs": total_scene_ms,
        "cues": srt_cues
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # Dọn dẹp các file con
    for idx in range(1, len(sentences) + 1):
        (DIR / f"line_{idx}.mp3").unlink(missing_ok=True)

if __name__ == "__main__":
    asyncio.run(synthesize_all())
    assemble_audio()
```

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
