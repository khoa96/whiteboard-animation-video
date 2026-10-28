#!/usr/bin/env python3
"""
Google AI Studio (Gemini) TTS Engine cho Whiteboard Animation Video.

Tính năng:
  1. Hỗ trợ 30 giọng nói chuẩn phòng thu từ Google AI Studio (Gemini Audio Modality).
  2. Gom toàn bộ kịch bản và sinh giọng trong 1 lần gọi (One-shot Generation) để đảm bảo:
     - Không bao giờ bị lệch tông giọng (Timbre & Cadence drift) giữa các câu.
     - Tối ưu quota, không bị dính lỗi 429.
  3. Thuật toán Cắt Neo Tỷ Lệ (Anchored Silence Splitting) nâng cấp:
     - Ưu tiên bắt khoảng lặng liên câu (inter-sentence silences >= 600ms).
     - Điều tiết closed-loop adaptive duration theo tỷ lệ số từ/âm tiết tiếng Việt.
     - Cắt gọn Onset/Offset khoảng lặng dư thừa để khớp nét vẽ bảng trắng ngay lập tức.
  4. Quản lý Pool nhiều API Key:
     - Tự động nạp từ GEMINI_API_KEYS (cách nhau bởi dấu phẩy) hoặc GEMINI_API_KEY.
     - Tự động xoay tua key và cooldown khi gặp lỗi 429.
  5. Cấu hình giọng đọc sư phạm chuẩn:
     - Giọng miền Bắc - Hà Nội chuẩn.
     - Phát âm song ngữ chuẩn: Tiếng Việt Hà Nội, Tiếng Anh chuẩn Anh - Mỹ (General American).
     - Phát âm rõ từng âm cuối (endings), KHÔNG nối âm, KHÔNG nuốt âm, chuẩn A1.
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path
from typing import Any

from pydub import AudioSegment
from pydub.silence import detect_silence

DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_VOICE = "Alnilam"  # Giọng nam đĩnh đạc, chuẩn ngữ âm song ngữ Việt - Anh bản xứ
DEFAULT_SAMPLE_RATE = 24000
TARGET_SAMPLE_RATE = 44100


def load_voice_config() -> dict[str, Any]:
    """Đọc cấu hình giọng nói và model từ config/tts_voices.json (nếu có)."""
    cfg_file = Path(__file__).resolve().parent.parent / "config" / "tts_voices.json"
    if cfg_file.exists():
        try:
            return json.loads(cfg_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"active_voice": DEFAULT_VOICE, "selected_model": DEFAULT_MODEL}


# Prompt hệ thống khóa chặt chân dung giảng viên nam 25 tuổi, song ngữ Anh - Mỹ bản xứ
SYSTEM_INSTRUCTION = (
    "[BILINGUAL NATIVE SPEAKER PROFILE]\n"
    "Bạn là một thầy giáo dạy tiếng Anh 25 tuổi, người song ngữ bản địa (Bilingual Native Speaker) hoàn hảo cả tiếng Việt và tiếng Anh Mỹ.\n\n"
    "Yêu cầu về hình tượng giọng nói và phát âm:\n"
    "1. Độ tuổi & Chất giọng: Giọng nam thanh niên 25 tuổi, trẻ trung, thanh thoát, ấm áp, nhiệt huyết và tràn đầy năng lượng, như một người thầy/gia sư đang trực tiếp trò chuyện với học viên.\n"
    "2. Phát âm Tiếng Việt: Chuẩn giọng miền Bắc - Hà Nội, phát âm rõ ràng, tròn vành rõ chữ, chuẩn mọi thanh điệu, tự nhiên, không trịnh trọng già nua.\n"
    "3. Phát âm Tiếng Anh: 100% PHÁT ÂM CHUẨN ANH - MỸ BẢN XỨ (NATIVE GENERAL AMERICAN ACCENT).\n"
    "   - QUY TẮC BẮT BUỘC (ANTI-VINGLISH): Tuyệt đối KHÔNG đọc tiếng Anh bằng ngữ âm tiếng Việt (cấm tuyệt đối phát âm kiểu Vinglish). Bất cứ khi nào gặp từ, cụm từ hoặc câu tiếng Anh (ví dụ: 'There is', 'There are', 'cat', 'desk', 'books', 'table', 'students', 'milk', 'fridge'...), phải phát âm chuẩn xác như một người Mỹ bản địa với nguyên âm mở chuẩn và âm rhotic /r/ tự nhiên.\n"
    "   - RÕ CÁC ÂM CUỐI (CRISP FINAL CONSONANTS): Bật cực kỳ rõ ràng, chuẩn xác các phụ âm cuối (/t/, /d/, /s/, /z/, /k/, /p/, /ks/, /dʒ/...), ví dụ: âm /t/ trong 'cat', âm /k/ trong 'book', âm /ks/ trong 'books', âm /dʒ/ trong 'fridge'.\n"
    "   - KHÔNG NUỐT ÂM, KHÔNG NỐI ÂM QUÁ NHANH: Phát âm chuẩn sư phạm cho người mới bắt đầu (Level A1), nhả chữ rõ ràng, không lướt âm, không nuốt âm tiết để học viên nghe chuẩn từng âm vị.\n"
    "4. Ngữ điệu sống động (Dynamic Prosody): Lên giọng tự nhiên ở cuối câu hỏi (?), hào hứng ở câu cảm thán hoặc lưu ý (!), trầm ấm dứt khoát ở câu giải thích (.). Tuyệt đối không đọc đều đều một tông giọng.\n"
    "5. Nguyên tắc nguyên văn: Đọc chính xác từng từ trong kịch bản được giao, không tự ý thêm bớt lời dẫn.\n"
    "6. Quy tắc ngắt nghỉ: Sau mỗi câu (ngăn cách bởi dòng trống), dừng lại nghỉ lấy hơi tự nhiên khoảng 0.8 đến 1.0 giây."
)


class GeminiKeyPool:
    """Quản lý danh sách API Key với cơ chế xoay vòng và cooldown khi gặp 429."""

    def __init__(self, keys: list[str]) -> None:
        self.keys = [k.strip() for k in keys if k.strip()]
        self.cooldowns: dict[str, float] = {}  # key -> cooldown_until_timestamp
        self._current_index = 0

    @classmethod
    def from_env(cls) -> GeminiKeyPool:
        raw = os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY") or ""
        keys = re.split(r"[,;\n\r]+", raw)
        keys_file = Path(__file__).resolve().parent.parent / "gemini_keys.txt"
        if keys_file.exists():
            for line in keys_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    keys.append(line)
        return cls(keys)

    def has_keys(self) -> bool:
        return len(self.keys) > 0

    def get_key(self) -> str:
        if not self.keys:
            raise RuntimeError(
                "Chưa cấu hình GEMINI_API_KEYS trong file .env hoặc gemini_keys.txt!\n"
                "Vui lòng thêm: GEMINI_API_KEYS=key1,key2,key3 vào .env"
            )

        now = time.time()
        for _ in range(len(self.keys)):
            key = self.keys[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.keys)
            cooldown_until = self.cooldowns.get(key, 0)
            if now >= cooldown_until:
                return key

        min_key = min(self.keys, key=lambda k: self.cooldowns.get(k, 0))
        wait_seconds = max(0.5, self.cooldowns.get(min_key, 0) - now)
        print(f"  [gemini-pool] Tất cả API keys đang bận, chờ {wait_seconds:.1f}s trước khi thử lại...")
        time.sleep(wait_seconds)
        return min_key

    def mark_rate_limited(self, key: str, cooldown_seconds: float = 60.0) -> None:
        self.cooldowns[key] = time.time() + cooldown_seconds
        print(f"  [gemini-pool] Key ...{key[-6:]} đạt giới hạn quota (429), tạm khóa {cooldown_seconds:.0f}s.")

    def mark_invalid(self, key: str, reason: str = "") -> None:
        if key in self.keys:
            self.keys.remove(key)
            if self._current_index >= len(self.keys) and self.keys:
                self._current_index = 0
            print(f"  [gemini-pool] Key ...{key[-6:]} không khả dụng ({reason}), đã tạm loại khỏi pool.")


def build_gemini_prompt(sentences: list[str], system_instruction: str | None = None) -> str:
    """Tạo văn bản kịch bản bảo toàn dấu câu biểu cảm (?, !, .) và dòng trống ngắt nghỉ."""
    sys_inst = (
        system_instruction
        or load_voice_config().get("system_instruction")
        or SYSTEM_INSTRUCTION
    )
    formatted_sentences = []
    for s in sentences:
        text = s.strip()
        if not text:
            continue
        # Bảo toàn dấu câu biểu cảm (?, !, .), chỉ thêm dấu chấm nếu câu chưa có dấu kết thúc
        if not re.search(r"[.!?…]$", text):
            text = text + "."
        formatted_sentences.append(text)

    body = "\n\n".join(formatted_sentences)
    return (
        f"{sys_inst}\n\n"
        "--- BẮT ĐẦU KỊCH BẢN CẦN ĐỌC ---\n\n"
        f"{body}\n\n"
        "--- HẾT KỊCH BẢN ---"
    )


def call_gemini_speech_api(
    prompt: str,
    voice_name: str,
    key_pool: GeminiKeyPool,
    model: str = DEFAULT_MODEL,
    max_retries: int = 5,
) -> bytes:
    """Gọi Gemini generateContent với responseModalities=['AUDIO']."""
    url_base = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }
    data = json.dumps(payload).encode("utf-8")

    for attempt in range(max_retries):
        api_key = key_pool.get_key()
        req = urllib.request.Request(
            f"{url_base}?key={api_key}",
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "whiteboard-gemini-tts/1.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                candidates = resp_json.get("candidates") or []
                if not candidates:
                    raise RuntimeError(f"Gemini API không trả về candidate: {resp_json}")
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    inline_data = part.get("inlineData")
                    if inline_data and "data" in inline_data:
                        raw_base64 = inline_data["data"]
                        mime_type = inline_data.get("mimeType", "")
                        audio_bytes = base64.b64decode(raw_base64)
                        return _standardize_audio(audio_bytes, mime_type)
                raise RuntimeError(f"Không tìm thấy audio inlineData trong phản hồi: {resp_json}")

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            if e.code == 429:
                key_pool.mark_rate_limited(api_key, cooldown_seconds=60.0)
                print(f"  [warn] Lỗi 429 trên key ...{api_key[-6:]}, tự động đổi key và thử lại (lần {attempt + 1}/{max_retries})...")
                time.sleep(2)
                continue
            elif e.code in (400, 403):
                key_pool.mark_invalid(api_key, reason=f"HTTP {e.code}")
                if key_pool.has_keys():
                    print(f"  [warn] Key ...{api_key[-6:]} bị lỗi ({e.code}), tự động chuyển sang key khác trong pool...")
                    time.sleep(1)
                    continue
                else:
                    raise RuntimeError(f"Tất cả API keys trong pool đều bị lỗi {e.code}: {err_body}")
            else:
                raise RuntimeError(f"Gemini API HTTP Error {e.code}: {err_body}")
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"  [warn] Lỗi kết nối ({e}), đang thử lại...")
            time.sleep(2)

    raise RuntimeError(f"Không thể sinh âm thanh sau {max_retries} lần thử.")


def _standardize_audio(raw_bytes: bytes, mime_type: str) -> bytes:
    """Chuẩn hóa dữ liệu âm thanh trả về từ Gemini thành chuẩn WAV 44.1kHz Mono."""
    # Nếu là PCM thô (audio/pcm)
    if "pcm" in mime_type.lower():
        # Trích xuất sample rate nếu có (vd: audio/pcm;rate=24000)
        rate_match = re.search(r"rate=(\d+)", mime_type)
        sample_rate = int(rate_match.group(1)) if rate_match else DEFAULT_SAMPLE_RATE
        audio = AudioSegment(
            data=raw_bytes,
            sample_width=2,  # 16-bit
            frame_rate=sample_rate,
            channels=1
        )
    else:
        # Nếu là WAV, MP3 hoặc container khác
        import io
        audio = AudioSegment.from_file(io.BytesIO(raw_bytes))

    # Resample sang 44100Hz mono chuẩn phòng thu
    audio = audio.set_frame_rate(TARGET_SAMPLE_RATE).set_channels(1)
    import io
    out_io = io.BytesIO()
    audio.export(out_io, format="wav")
    return out_io.getvalue()


def split_audio_exact_sentences(
    audio_path: Path,
    sentences: list[str],
    min_silence_len: int = 350,
    silence_thresh_offset: float = 14.0,
) -> list[dict[str, Any]]:
    """
    Thuật toán Cắt Neo Tỷ Lệ (Anchored Silence Splitting) nâng cấp bằng Quy Hoạch Động (DP).

    Đảm bảo:
      - Đúng N câu đầu vào sẽ cắt ra chính xác N file audio.
      - Phân lập chính xác các khoảng lặng liên câu (inter-sentence pauses >= 800ms) khỏi dấu phẩy nội bộ.
      - Cắt gọn Onset/Offset khoảng lặng dư thừa để khớp nét vẽ bảng trắng ngay lập tức.
    """
    audio = AudioSegment.from_file(str(audio_path))
    total_duration = len(audio)  # milliseconds
    n = len(sentences)

    if n <= 1:
        trimmed = _tight_trim_silence(audio, silence_thresh=max(-50.0, audio.dBFS - silence_thresh_offset))
        return [{
            "index": 1,
            "text": sentences[0] if sentences else "",
            "audio_chunk": trimmed,
            "duration_sec": len(trimmed) / 1000.0,
        }]

    # 1. Trọng số ước tính theo số từ
    weights = [max(1, len(s.strip().split())) for s in sentences]
    total_w = sum(weights)

    # 2. Ngưỡng phát hiện khoảng lặng linh hoạt
    silence_thresh = max(-50.0, audio.dBFS - silence_thresh_offset)
    raw_silences = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # 3. Lọc tập ứng viên khoảng lặng liên câu bằng cách quét ngưỡng từ 1600ms xuống 350ms
    candidates = []
    for dur_th in range(1600, 300, -50):
        cands = [s for s in raw_silences if (s[1] - s[0]) >= dur_th]
        filtered = []
        for c in cands:
            if not filtered or c[0] - filtered[-1][1] >= 800:
                filtered.append(c)
        if len(filtered) >= n - 1:
            candidates = filtered
            break

    if not candidates:
        candidates = raw_silences

    m = len(candidates)
    if m == n - 1:
        cut_points = [0] + [(s[0] + s[1]) // 2 for s in candidates] + [total_duration]
    else:
        # 4. Quy hoạch động (DP) chọn n - 1 điểm cắt tối ưu từ m ứng viên
        cand_mids = [(s[0] + s[1]) // 2 for s in candidates]
        cand_durs = [s[1] - s[0] for s in candidates]

        # dp[(k, j)] = (cost, prev_j)
        dp = {}
        target_dur_1 = total_duration * (weights[0] / total_w)
        for j in range(m):
            dur_1 = cand_mids[j]
            cost = abs(dur_1 - target_dur_1) - cand_durs[j] * 0.3
            dp[(1, j)] = (cost, -1)

        for k in range(2, n):
            target_dur_k = total_duration * (weights[k - 1] / total_w)
            for j in range(k - 1, m):
                best_val = float("inf")
                best_prev = -1
                for pj in range(k - 2, j):
                    if (k - 1, pj) not in dp:
                        continue
                    prev_cost, _ = dp[(k - 1, pj)]
                    dur_k = cand_mids[j] - cand_mids[pj]
                    if dur_k < 600:
                        continue
                    step_cost = abs(dur_k - target_dur_k) - cand_durs[j] * 0.3
                    total_cost = prev_cost + step_cost
                    if total_cost < best_val:
                        best_val = total_cost
                        best_prev = pj
                if best_prev != -1:
                    dp[(k, j)] = (best_val, best_prev)

        target_dur_last = total_duration * (weights[-1] / total_w)
        best_final_val = float("inf")
        best_final_j = -1
        for j in range(n - 2, m):
            if (n - 1, j) not in dp:
                continue
            c, _ = dp[(n - 1, j)]
            dur_last = total_duration - cand_mids[j]
            if dur_last < 600:
                continue
            total_cost = c + abs(dur_last - target_dur_last)
            if total_cost < best_final_val:
                best_final_val = total_cost
                best_final_j = j

        if best_final_j != -1:
            curr = best_final_j
            chosen = []
            for k in range(n - 1, 0, -1):
                chosen.append(cand_mids[curr])
                _, curr = dp[(k, curr)]
            chosen.reverse()
            cut_points = [0] + chosen + [total_duration]
        else:
            # Fallback đều nhịp nếu DP không tìm thấy đường đi khả thi
            cut_points = [0]
            curr = 0
            for i in range(n - 1):
                curr += int(total_duration * (weights[i] / total_w))
                cut_points.append(curr)
            cut_points.append(total_duration)

    # 4. Trích xuất từng đoạn và tinh chỉnh Onset/Offset
    results = []
    for i in range(len(sentences)):
        raw_chunk = audio[cut_points[i]:cut_points[i + 1]]

        # Cắt bỏ khoảng lặng thừa đầu/cuối của chunk để tiếng nói bắt đầu ngay lập tức
        # Giữ lại đệm nhỏ 40ms đầu và 80ms cuối để không bị cụt âm
        trimmed_chunk = _tight_trim_silence(raw_chunk, silence_thresh=silence_thresh)

        results.append({
            "index": i + 1,
            "text": sentences[i],
            "audio_chunk": trimmed_chunk,
            "duration_sec": len(trimmed_chunk) / 1000.0,
        })

    return results


def _tight_trim_silence(chunk: AudioSegment, silence_thresh: float, lead_ms: int = 40, tail_ms: int = 80) -> AudioSegment:
    """Cắt bớt khoảng lặng ở đầu và đuôi của đoạn audio một cách mượt mà."""
    if len(chunk) < 200:
        return chunk

    # Tìm điểm bắt đầu có tiếng nói
    silences = detect_silence(chunk, min_silence_len=50, silence_thresh=silence_thresh)
    start_cut = 0
    end_cut = len(chunk)

    if silences:
        # Nếu khoảng lặng đầu tiên bắt đầu từ 0
        if silences[0][0] == 0:
            start_cut = max(0, silences[0][1] - lead_ms)
        # Nếu khoảng lặng cuối cùng chạm đến cuối file
        if silences[-1][1] >= len(chunk) - 20:
            end_cut = min(len(chunk), silences[-1][0] + tail_ms)

    if end_cut > start_cut + 100:
        return chunk[start_cut:end_cut]
    return chunk


BATCH_MAX_CUES = 35


def _synthesize_single_batch_and_split(
    cues: list[dict[str, Any]],
    cache_dir: Path,
    voice: str,
    speed: float,
    model: str,
    key_pool: GeminiKeyPool,
    batch_idx: int = 1,
    total_batches: int = 1,
) -> list[Path]:
    """Sinh âm thanh và cắt cho một mẻ (tối đa 35 câu)."""
    import hashlib
    sentences = [c["text"].strip() for c in cues]
    combined_text = "\n".join(sentences)

    script_hash = hashlib.sha1(f"gemini|{model}|{voice}|{speed}|{combined_text}".encode("utf-8")).hexdigest()[:12]
    master_path = cache_dir / f"gemini-master-b{batch_idx}-{script_hash}.wav"

    clips: list[Path] = []
    all_cached = True
    for cue in cues:
        cue_clip = cache_dir / f"cue-{cue['index']:03d}-{script_hash}.mp3"
        clips.append(cue_clip)
        if not cue_clip.exists():
            all_cached = False

    if all_cached:
        print(f"  [gemini-tts] Mẻ {batch_idx}/{total_batches} ({len(cues)} câu) đã có sẵn trong cache!")
        return clips

    # 1. Sinh file audio master của mẻ
    if not master_path.exists():
        prefix = f"Mẻ {batch_idx}/{total_batches}: " if total_batches > 1 else ""
        print(f"  [gemini-tts] {prefix}Đang gửi {len(sentences)} câu tới Gemini TTS (Voice: {voice})...")
        prompt = build_gemini_prompt(sentences)
        audio_bytes = call_gemini_speech_api(prompt, voice, key_pool, model=model)
        master_path.write_bytes(audio_bytes)
        print(f"  [gemini-tts] {prefix}Đã sinh master audio ({master_path.name}) thành công!")
    else:
        print(f"  [gemini-tts] Tái sử dụng master audio có sẵn: {master_path.name}")

    # Điều chỉnh tốc độ tổng thể nếu speed != 1.0
    effective_master = master_path
    if abs(speed - 1.0) > 1e-3:
        speed_master = cache_dir / f"gemini-master-b{batch_idx}-{script_hash}-speed{speed:.2f}.wav"
        if not speed_master.exists():
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(master_path),
                    "-filter:a", f"atempo={speed}",
                    "-ar", str(TARGET_SAMPLE_RATE),
                    str(speed_master)
                ],
                check=True,
            )
        effective_master = speed_master

    # 2. Tách master audio thành các câu
    chunks = split_audio_exact_sentences(effective_master, sentences)

    # 3. Xuất ra từng file cue
    for i, chunk_info in enumerate(chunks):
        out_file = clips[i]
        chunk_info["audio_chunk"].export(str(out_file), format="mp3", bitrate="192k")
        print(f"  • Câu {chunk_info['index']:>2}: {chunk_info['duration_sec']:.2f}s | {chunk_info['text'][:35]}...")

    return clips


def synthesize_gemini_master_and_split(
    cues: list[dict[str, Any]],
    cache_dir: Path,
    voice: str = DEFAULT_VOICE,
    speed: float = 1.0,
    model: str = DEFAULT_MODEL,
) -> list[Path]:
    """
    Hàm giao tiếp chính với tts_narration:
      - Tự động chia theo mẻ nếu số câu > 35 để không vượt quá giới hạn token audio của Gemini.
      - Gọi Gemini sinh giọng và chạy bộ Cắt Neo Tỷ Lệ cho từng mẻ.
      - Trả về danh sách file âm thanh của tất cả các câu theo đúng thứ tự.
    """
    key_pool = GeminiKeyPool.from_env()
    cache_dir.mkdir(parents=True, exist_ok=True)

    if len(cues) <= BATCH_MAX_CUES:
        return _synthesize_single_batch_and_split(
            cues, cache_dir, voice=voice, speed=speed, model=model, key_pool=key_pool,
            batch_idx=1, total_batches=1
        )

    # Chia thành các mẻ <= BATCH_MAX_CUES
    batch_list = [cues[i:i + BATCH_MAX_CUES] for i in range(0, len(cues), BATCH_MAX_CUES)]
    total_batches = len(batch_list)
    print(f"  [gemini-tts] Kịch bản dài ({len(cues)} câu) -> Tự động chia thành {total_batches} mẻ (mỗi mẻ ~{BATCH_MAX_CUES} câu)...")

    all_clips: list[Path] = []
    for idx, batch_cues in enumerate(batch_list, 1):
        batch_clips = _synthesize_single_batch_and_split(
            batch_cues, cache_dir, voice=voice, speed=speed, model=model, key_pool=key_pool,
            batch_idx=idx, total_batches=total_batches
        )
        all_clips.extend(batch_clips)

    return all_clips
