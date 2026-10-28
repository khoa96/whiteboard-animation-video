#!/usr/bin/env python3
"""
Sinh âm thanh Master Clock cho Scene 05: COMMON EXAMPLES
Engine: Edge-TTS (en-US-AndrewMultilingualNeural)
Đo chính xác từng mili-giây, xuất narration.m4a, input.srt, timing_cues.json
Tự động dọn dẹp các tệp nháp line_*.mp3 sau khi hoàn thành.
"""
import asyncio
import subprocess
from pathlib import Path
import json
import edge_tts

DIR = Path(__file__).resolve().parent

sentences = [
    "Bây giờ, hãy thử với những từ quen thuộc.",
    "A book, a cat, a car, a dog, a tree, a ball. Các từ này đều bắt đầu bằng âm phụ âm.",
    "An apple, an egg, an umbrella, an ice cream, an orange, an elephant. Các từ này bắt đầu bằng âm nguyên âm.",
    "Mạo từ đứng ngay trước danh từ hoặc cụm danh từ. Hãy nghe từ được nói ngay sau A hoặc AN.",
    "Đừng chỉ học thuộc hình dáng chữ cái. Hãy kết hợp từ với cách phát âm của nó.",
    "Tiếp theo, chúng ta sẽ gặp những từ dễ gây nhầm lẫn hơn."
]

VOICE = "en-US-AndrewMultilingualNeural"

async def synthesize_all():
    print(f"[Scene 05] Synthesizing {len(sentences)} lines with {VOICE}...")
    for idx, s in enumerate(sentences, 1):
        c = edge_tts.Communicate(s, VOICE)
        out_f = DIR / f"line_{idx}.mp3"
        await c.save(str(out_f))
        print(f"  Line {idx} generated: {s[:35]}...")

def assemble_audio():
    gap = 0.5       # 0.5s pause
    lead_in = 0.5   # 0.5s lead in
    current_time = lead_in
    srt_cues = []

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

    tail = 2.5  # 2.5s tail freeze
    total_scene_ms = int(round((current_time - gap + tail) * 1000))
    print(f"[Scene 05] Total duration: {total_scene_ms} ms ({total_scene_ms/1000:.2f} s)")

    def format_srt_time(ms):
        h = ms // 3600000
        m = (ms % 3600000) // 60000
        s = (ms % 60000) // 1000
        sub_ms = ms % 1000
        return f"{h:02d}:{m:02d}:{s:02d},{sub_ms:03d}"

    srt_lines = []
    for cue in srt_cues:
        idx = cue["index"]
        s_str = format_srt_time(cue["startMs"])
        e_str = format_srt_time(cue["endMs"])
        txt = cue["text"]
        srt_lines.append(f"{idx}\n{s_str} --> {e_str}\n{txt}\n")

    srt_path = DIR / "input.srt"
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")

    inputs = []
    for idx in range(1, len(sentences) + 1):
        inputs.extend(["-i", str(DIR / f"line_{idx}.mp3")])

    filter_str = ""
    for i, cue in enumerate(srt_cues):
        delay_ms = cue["startMs"]
        filter_str += f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];"
    mix_inputs = "".join(f"[a{i}]" for i in range(len(srt_cues)))
    filter_str += f"{mix_inputs}amix=inputs={len(srt_cues)}:dropout_transition=0:normalize=0[outa]"

    out_audio = DIR / "narration.m4a"
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_str, "-map", "[outa]", "-c:a", "aac", "-b:a", "192k", str(out_audio)]
    subprocess.run(cmd, check=True, capture_output=True)

    (DIR / "timing_cues.json").write_text(json.dumps({
        "totalDurationMs": total_scene_ms,
        "cues": srt_cues
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[Scene 05] Audio Master Clock ready!")

    # Dọn dẹp các tệp nháp line_*.mp3
    for idx in range(1, len(sentences) + 1):
        (DIR / f"line_{idx}.mp3").unlink(missing_ok=True)

if __name__ == "__main__":
    asyncio.run(synthesize_all())
    assemble_audio()
