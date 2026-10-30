export class ScriptPreprocessor {
  /**
   * Tiền xử lý kịch bản:
   * 1. Hỗ trợ [NATURAL: ...] hoặc [FLUENT: ...] cho các câu giao tiếp trôi chảy, nối âm tự nhiên.
   * 2. Hỗ trợ [DRILL: ...] cho các đoạn luyện phát âm từng từ khóa (tách bằng dấu chấm lửng ... để bật rõ âm cuối).
   * 3. Hỗ trợ tương thích ngược [A1: ...], [SLOW: ...], [NATIVE: ...].
   * 4. Chuẩn hóa khoảng trắng, dấu câu và tạo nhịp nghỉ tự nhiên giữa các câu.
   */
  public static preprocess(rawText: string): string {
    let processed = rawText;

    // 1. Xử lý [DRILL: word1, word2, word3] hoặc [DRILL: word1... word2] -> Tách từ bằng '... '
    processed = processed.replace(/\[DRILL:\s*([^\]]+)\]/gi, (_, content: string) => {
      const words = content
        .split(/[,…\.\s]+/)
        .map((w) => w.trim())
        .filter((w) => w.length > 0);
      return words.join('... ');
    });

    // 2. Xử lý [NATURAL: text], [FLUENT: text], [A1: text], [SLOW: text], [NATIVE: text], [PROSODY: text]
    // Giữ nguyên câu mượt mà, loại bỏ thẻ tag
    processed = processed.replace(
      /\[(?:NATURAL|FLUENT|A1|SLOW|NATIVE|PROSODY):\s*([^\]]+)\]/gi,
      (_, content: string) => {
        return content.trim();
      }
    );

    // 3. Chuẩn hóa các dòng văn bản và tự động phân tách câu theo dấu kết thúc
    const rawLines = processed
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    const sentences: string[] = [];
    for (const line of rawLines) {
      // Tách câu khi gặp dấu . ! ? kèm khoảng trắng và chữ cái viết hoa tiếp theo
      const parts = line.split(/(?<=[.!?…])\s+(?=[A-Z0-9"“])/);
      for (const p of parts) {
        const clean = p.trim();
        if (clean.length > 0) {
          sentences.push(clean);
        }
      }
    }

    // 4. Đảm bảo mỗi câu kết thúc bằng dấu câu hợp lệ (. ! ?)
    const formattedSentences = sentences.map((s) => {
      let l = s;
      if (!/[.!?…]$/.test(l)) {
        l += '.';
      }
      return l;
    });

    // 5. Ngăn cách mỗi câu bằng 2 dòng trống (\n\n) để tạo khoảng nghỉ lấy hơi tự nhiên
    return formattedSentences.join('\n\n');
  }

  /**
   * Chia kịch bản dài thành các đoạn nhỏ an toàn (tối đa maxChars ký tự/đoạn)
   */
  public static splitIntoChunks(fullText: string, maxChars: number = 1800): string[] {
    const sentences = fullText.split(/\n\n+/);
    const chunks: string[] = [];
    let currentChunk = '';

    for (const s of sentences) {
      if ((currentChunk + '\n\n' + s).length > maxChars && currentChunk.length > 0) {
        chunks.push(currentChunk.trim());
        currentChunk = s;
      } else {
        currentChunk = currentChunk ? currentChunk + '\n\n' + s : s;
      }
    }

    if (currentChunk.trim().length > 0) {
      chunks.push(currentChunk.trim());
    }

    return chunks;
  }
}
