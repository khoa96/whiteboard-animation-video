import { SpeechUnit } from './types.js';

export class ScriptPreprocessor {
  /**
   * Tiền xử lý các thẻ điều khiển ngữ âm (Pronunciation & Prosody Tags):
   * 1. [DRILL: word1, word2, word3] -> Tách từ bằng '... ' để mô hình bật rõ âm cuối
   * 2. [NATURAL: text], [FLUENT: text], [A1: text], [SLOW: text], [NATIVE: text] -> Giữ nguyên text, xóa tag
   */
  public static cleanTextForTts(rawText: string): string {
    let processed = rawText;

    // Xử lý [DRILL: ...]
    processed = processed.replace(/\[DRILL:\s*([^\]]+)\]/gi, (_, content: string) => {
      const words = content
        .split(/[,…\.\s]+/)
        .map((w: string) => w.trim())
        .filter((w: string) => w.length > 0);
      return words.join('... ');
    });

    // Xử lý [NATURAL: ...], [A1: ...], v.v.
    processed = processed.replace(
      /\[(?:NATURAL|FLUENT|A1|SLOW|NATIVE|PROSODY):\s*([^\]]+)\]/gi,
      (_, content: string) => {
        return content.trim();
      }
    );

    return processed.trim();
  }

  /**
   * Kiểm tra xem văn bản có dấu ngoặc kép chưa được đóng hay không.
   */
  private static isQuoteOpen(text: string): boolean {
    const doubleQuotes = (text.match(/"/g) || []).length;
    const curlyOpen = (text.match(/“/g) || []).length;
    const curlyClose = (text.match(/”/g) || []).length;
    return curlyOpen > curlyClose || doubleQuotes % 2 === 1;
  }

  /**
   * Chia nhỏ một câu quá dài (> maxChars) theo các vế câu (dấu phẩy, chấm phẩy, hai chấm)
   */
  private static splitLongSentence(sentence: string, maxChars: number = 110): string[] {
    if (sentence.length <= maxChars) {
      return [sentence];
    }
    const clauseRegex = /(?<=[,;:，；：])\s+/;
    const clauses = sentence.split(clauseRegex);
    const parts: string[] = [];
    let current = '';

    for (const c of clauses) {
      if (current && (current.length + 1 + c.length > maxChars)) {
        parts.push(current);
        current = c;
      } else {
        current = current ? `${current} ${c}` : c;
      }
    }
    if (current) {
      parts.push(current);
    }
    return parts;
  }

  /**
   * Thuật toán phân tách vi mô (Micro-segmentation) kịch bản thành các câu phụ đề chuẩn xác:
   * 1. Tôn trọng ranh giới đoạn văn (để quản lý nhịp thở và khoảng ngắt cảnh).
   * 2. Tách từng câu hoàn chỉnh theo [. ! ? … 。！？].
   * 3. Bảo vệ không cắt vỡ câu thoại nằm trong ngoặc kép.
   * 4. Cắt vế câu nếu câu vượt quá maxChars (mặc định 110 ký tự).
   * 5. Hợp nhất các mẩu quá vụn (< minChars) vào câu kế tiếp.
   */
  public static extractSpeechUnits(
    rawText: string,
    options: { maxChars?: number; minChars?: number } = {}
  ): SpeechUnit[] {
    const maxChars = options.maxChars ?? 110;
    const minChars = options.minChars ?? 12;

    // 1. Kiểm tra nếu là file SRT có sẵn (chứa mốc -->)
    if (/-->/.test(rawText)) {
      const srtBlocks = rawText.split(/\r?\n\r?\n+/);
      const units: SpeechUnit[] = [];
      for (let i = 0; i < srtBlocks.length; i++) {
        const lines = srtBlocks[i].split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
        const textLines = lines.filter((l) => !/^\d+$/.test(l) && !/-->/.test(l));
        if (textLines.length > 0) {
          const clean = textLines.join(' ').replace(/^\[SCENE\s*\d+\]\s*/i, '').trim();
          if (clean) {
            units.push({
              text: clean,
              isParagraphEnd: true,
            });
          }
        }
      }
      return units;
    }

    // 2. Tách theo dòng, loại bỏ các dòng tiêu đề Markdown (# Title)
    const lines = rawText
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter((l) => l.length > 0 && !l.startsWith('#'));

    // Gộp các dòng liên tiếp không có dòng trống vào cùng 1 paragraph
    const rawParagraphs: string[] = [];
    let currentParaLines: string[] = [];

    for (const line of rawLinesFromText(rawText)) {
      if (line.length === 0) {
        if (currentParaLines.length > 0) {
          rawParagraphs.push(currentParaLines.join(' '));
          currentParaLines = [];
        }
      } else if (!line.startsWith('#')) {
        currentParaLines.push(line);
      }
    }
    if (currentParaLines.length > 0) {
      rawParagraphs.push(currentParaLines.join(' '));
    }

    const units: SpeechUnit[] = [];
    const SENTENCE_REGEX = /.+?(?:[.!?…。！？]+["”’»)\]]*(?=\s|$)|$)/g;

    for (const para of rawParagraphs) {
      // Nhận diện thẻ tạm dừng kỹ thuật độc lập [PAUSE X SECONDS]
      const pauseMatch = para.match(/^\[(?:PAUSE|SILENCE)\s*:?\s*([0-9.]+)?/i);
      if (pauseMatch) {
        units.push({
          text: para,
          isParagraphEnd: true,
          isTechnicalPause: true,
          pauseDurationSec: pauseMatch[1] ? parseFloat(pauseMatch[1]) : 3.0,
        });
        continue;
      }

      const sentences: string[] = [];
      let pending = '';
      const matches = para.match(SENTENCE_REGEX) || [para];

      for (const m of matches) {
        const s = m.trim();
        if (!s) continue;
        pending = pending ? `${pending} ${s}` : s;

        // Nếu ngoặc kép chưa đóng, không ngắt câu bên trong
        if (this.isQuoteOpen(pending)) {
          continue;
        }

        if (pending.length <= maxChars) {
          sentences.push(pending);
        } else {
          const splitParts = this.splitLongSentence(pending, maxChars);
          sentences.push(...splitParts);
        }
        pending = '';
      }
      if (pending) {
        sentences.push(pending);
      }

      // Hợp nhất các mẩu câu quá ngắn (< minChars)
      const merged: string[] = [];
      for (const s of sentences) {
        if (
          merged.length > 0 &&
          merged[merged.length - 1].length < minChars &&
          merged[merged.length - 1].length + 1 + s.length <= maxChars
        ) {
          merged[merged.length - 1] += ' ' + s;
        } else {
          merged.push(s);
        }
      }

      merged.forEach((s, idx) => {
        units.push({
          text: s,
          isParagraphEnd: idx === merged.length - 1,
        });
      });
    }

    return units;
  }

  /**
   * Trích xuất danh sách câu dạng chuỗi (hỗ trợ tương thích ngược)
   */
  public static extractSentences(rawText: string): string[] {
    return this.extractSpeechUnits(rawText).map((u) => u.text);
  }

  /**
   * Tiền xử lý kịch bản cho chế độ Chunk lớn (hỗ trợ tương thích ngược)
   */
  public static preprocess(rawText: string): string {
    const units = this.extractSpeechUnits(rawText);
    return units.map((u) => u.text).join('\n\n');
  }

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

function rawLinesFromText(rawText: string): string[] {
  return rawText.split(/\r?\n/).map((l) => l.trim());
}
