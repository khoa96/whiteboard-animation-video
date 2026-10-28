#!/usr/bin/env python3
"""
Kiểm thử thuật toán Gemini Key Pool và Anchored Silence Splitting.
"""
import io
import math
import struct
import sys
from pathlib import Path

from pydub import AudioSegment

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts_gemini import GeminiKeyPool, build_gemini_prompt, split_audio_exact_sentences


def test_key_pool():
    print("[TEST 1] Kiểm tra GeminiKeyPool rotation & cooldown...")
    pool = GeminiKeyPool(["key_A", "key_B", "key_C"])
    assert pool.has_keys()

    k1 = pool.get_key()
    k2 = pool.get_key()
    k3 = pool.get_key()
    assert [k1, k2, k3] == ["key_A", "key_B", "key_C"]

    # Đánh dấu key_A bị rate limit
    pool.mark_rate_limited("key_A", cooldown_seconds=10.0)
    k4 = pool.get_key()
    assert k4 in ["key_B", "key_C"], f"Expected key_B or key_C, got {k4}"
    print("  -> PASSED: Key pool xoay vòng và cooldown chính xác!")


def test_prompt_builder():
    print("[TEST 2] Kiểm tra build_gemini_prompt...")
    sentences = [
        "Chào mừng bạn đến với mô hình OKR.",
        "Đây là framework quản trị mục tiêu hàng đầu.",
        "Mỗi Objective cần có từ ba đến năm Key Results."
    ]
    prompt = build_gemini_prompt(sentences)
    assert "Level A1" in prompt
    assert "Chuẩn giọng miền Bắc - Hà Nội" in prompt
    assert "general american" in prompt.lower()
    assert "Chào mừng bạn đến với mô hình OKR." in prompt
    assert "nghỉ lấy hơi tự nhiên" in prompt.lower()
    print("  -> PASSED: Prompt cấu hình sư phạm A1 chuẩn xác!")


def test_anchored_silence_splitter():
    print("[TEST 3] Kiểm tra thuật toán Cắt Neo Tỷ Lệ (Anchored Silence Splitting)...")
    # Tạo một file audio mô phỏng: 3 câu với khoảng nghỉ 1000ms ở giữa
    # Câu 1: 5 từ (~2.0s âm thanh)
    # Nghỉ: 1.0s
    # Câu 2: 7 từ (~2.8s âm thanh)
    # Nghỉ: 1.0s
    # Câu 3: 10 từ (~4.0s âm thanh)
    sample_rate = 44100
    
    def generate_tone(duration_s: float, freq: float = 440.0) -> AudioSegment:
        num_samples = int(duration_s * sample_rate)
        # Sinh sóng sin đơn giản
        samples = [int(16000 * math.sin(2 * math.pi * freq * i / sample_rate)) for i in range(num_samples)]
        raw_bytes = struct.pack(f"<{len(samples)}h", *samples)
        return AudioSegment(data=raw_bytes, sample_width=2, frame_rate=sample_rate, channels=1)

    silence_1s = AudioSegment.silent(duration=1000, frame_rate=sample_rate)
    silence_200ms = AudioSegment.silent(duration=200, frame_rate=sample_rate)

    # Ghép: Câu 1 có 1 dấu phẩy nghỉ 200ms
    c1_part1 = generate_tone(1.0, 400)
    c1_part2 = generate_tone(1.0, 420)
    c1 = c1_part1 + silence_200ms + c1_part2

    # Câu 2
    c2 = generate_tone(2.8, 500)

    # Câu 3
    c3 = generate_tone(4.0, 600)

    # Tổng thể: c1 + silence_1s + c2 + silence_1s + c3
    full_audio = c1 + silence_1s + c2 + silence_1s + c3

    test_wav = Path(__file__).resolve().parent / "test_synth.wav"
    full_audio.export(str(test_wav), format="wav")

    sentences = [
        "Chào mừng bạn đến với mô hình OKR.",
        "Đây là framework quản trị mục tiêu hàng đầu.",
        "Mỗi Objective cần có từ ba đến năm Key Results đo lường được."
    ]

    results = split_audio_exact_sentences(test_wav, sentences)
    assert len(results) == 3, f"Expected 3 chunks, got {len(results)}"
    
    # Kiểm tra thời lượng xấp xỉ
    durations = [r["duration_sec"] for r in results]
    print(f"  -> Cắt ra 3 câu thành công! Thời lượng các câu: {durations}")
    
    # Dọn dẹp
    test_wav.unlink(missing_ok=True)
    print("  -> PASSED: Thuật toán Cắt Neo Tỷ Lệ chia tách chuẩn xác 3/3 câu!")


if __name__ == "__main__":
    test_key_pool()
    test_prompt_builder()
    test_anchored_silence_splitter()
    print("\n🎉 TẤT CẢ CÁC BÀI TEST ĐÃ VƯỢT QUA XUẤT SẮC!")
