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

    // 3. Chuẩn hóa các dòng văn bản: Tôn trọng cấu trúc dòng của kịch bản
    const rawLines = processed
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    const speechUnits: string[] = [];
    for (const line of rawLines) {
      // Chỉ tách câu bên trong dòng nếu dòng quá dài (> 250 ký tự) để tránh làm vỡ mạch nói tự nhiên
      if (line.length > 250) {
        const parts = line.split(/(?<=[.!?…])\s+(?=[A-Z0-9"“])/);
        for (const p of parts) {
          const clean = p.trim();
          if (clean.length > 0) {
            speechUnits.push(clean);
          }
        }
      } else {
        speechUnits.push(line);
      }
    }

    // 4. Đảm bảo mỗi đơn vị câu/dòng kết thúc bằng dấu câu hợp lệ (. ! ?)
    const formattedUnits = speechUnits.map((s) => {
      let l = s;
      if (!/[.!?…]$/.test(l)) {
        l += '.';
      }
      return l;
    });

    // 5. Ngăn cách mỗi đơn vị bằng 2 dòng trống (\n\n) để tạo nhịp nghỉ tự nhiên
    return formattedUnits.join('\n\n');
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

  /**
   * Trích xuất danh sách các câu từ kịch bản (hỗ trợ .txt, .md và .srt)
   */
  public static extractSentences(rawText: string): string[] {
    // 1. Kiểm tra nếu là định dạng file SRT (chứa mốc -->)
    if (/-->/.test(rawText)) {
      const srtBlocks = rawText.split(/\r?\n\r?\n+/);
      const srtSentences: string[] = [];
      for (const block of srtBlocks) {
        const lines = block.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
        // Bỏ dòng số thứ tự và dòng timestamp (00:00:00,000 --> 00:00:05,000)
        const textLines = lines.filter((l) => !/^\d+$/.test(l) && !/-->/.test(l));
        if (textLines.length > 0) {
          const joined = textLines.join(' ');
          // Bỏ tag scene [SCENE 01] nếu có ở đầu
          const clean = joined.replace(/^\[SCENE\s*\d+\]\s*/i, '').trim();
          if (clean) {
            srtSentences.push(clean);
          }
        }
      }
      if (srtSentences.length > 0) {
        return srtSentences;
      }
    }

    // 2. Nếu là text hoặc markdown thông thường: lọc bỏ các tiêu đề Markdown (# Title)
    const strippedLines = rawText
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter((l) => l.length > 0 && !l.startsWith('#'))
      .join('\n');

    const preprocessed = this.preprocess(strippedLines);
    return preprocessed.split(/\n\n+/).map((s) => s.trim()).filter((s) => s.length > 0);
  }
}

