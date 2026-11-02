import fs from 'fs';

export class AudioUtils {
  /**
   * Tạo 44 bytes chuẩn WAV Header cho dữ liệu PCM 16-bit Mono/Stereo.
   */
  public static createWavHeader(
    dataLength: number,
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16
  ): Buffer {
    const buffer = Buffer.alloc(44);

    // RIFF chunk descriptor
    buffer.write('RIFF', 0); // ChunkID
    buffer.writeUInt32LE(36 + dataLength, 4); // ChunkSize (36 + data size)
    buffer.write('WAVE', 8); // Format

    // "fmt " sub-chunk
    buffer.write('fmt ', 12); // Subchunk1ID
    buffer.writeUInt32LE(16, 16); // Subchunk1Size (16 for PCM)
    buffer.writeUInt16LE(1, 20); // AudioFormat (1 for PCM)
    buffer.writeUInt16LE(channels, 22); // NumChannels
    buffer.writeUInt32LE(sampleRate, 24); // SampleRate
    const byteRate = (sampleRate * channels * bitsPerSample) / 8;
    buffer.writeUInt32LE(byteRate, 28); // ByteRate
    const blockAlign = (channels * bitsPerSample) / 8;
    buffer.writeUInt16LE(blockAlign, 32); // BlockAlign
    buffer.writeUInt16LE(bitsPerSample, 34); // BitsPerSample

    // "data" sub-chunk
    buffer.write('data', 36); // Subchunk2ID
    buffer.writeUInt32LE(dataLength, 40); // Subchunk2Size

    return buffer;
  }

  /**
   * Trích xuất chính xác dữ liệu PCM thô từ file/buffer WAV:
   * Bỏ qua toàn bộ metadata như C2PA (SynthID watermark manifest), LIST, INFO...
   * Chỉ lấy đúng phần payload âm thanh bên trong chunk 'data'.
   */
  public static extractPcmData(wavBuffer: Buffer): {
    pcm: Buffer;
    sampleRate: number;
    channels: number;
    bitsPerSample: number;
  } {
    // Nếu không phải định dạng RIFF, giả định là PCM thô 24000Hz 16-bit mono
    if (wavBuffer.length < 12 || wavBuffer.subarray(0, 4).toString('ascii') !== 'RIFF') {
      return {
        pcm: wavBuffer,
        sampleRate: 24000,
        channels: 1,
        bitsPerSample: 16,
      };
    }

    let offset = 12;
    let sampleRate = 24000;
    let channels = 1;
    let bitsPerSample = 16;
    let pcmData: Buffer | null = null;

    while (offset + 8 <= wavBuffer.length) {
      const chunkId = wavBuffer.subarray(offset, offset + 4).toString('ascii');
      const chunkSize = wavBuffer.readUInt32LE(offset + 4);
      const dataStart = offset + 8;
      const dataEnd = dataStart + chunkSize;

      if (chunkId === 'fmt ') {
        channels = wavBuffer.readUInt16LE(dataStart + 2);
        sampleRate = wavBuffer.readUInt32LE(dataStart + 4);
        bitsPerSample = wavBuffer.readUInt16LE(dataStart + 14);
      } else if (chunkId === 'data') {
        pcmData = wavBuffer.subarray(dataStart, Math.min(dataEnd, wavBuffer.length));
      }

      // Nhảy sang chunk tiếp theo (tính cả padding 2-byte alignment chuẩn RIFF)
      offset = dataEnd + (chunkSize % 2 !== 0 ? 1 : 0);
    }

    return {
      pcm: pcmData || Buffer.alloc(0),
      sampleRate,
      channels,
      bitsPerSample,
    };
  }

  /**
   * Áp dụng Micro-Fade (Hann Window) vào đầu và đuôi đoạn audio PCM 16-bit:
   * - Fade-in (10-15ms): Triệt tiêu tiếng click/pop khi bắt đầu phát.
   * - Fade-out (15-25ms): Triệt tiêu hoàn toàn DC Offset và tiếng sẹt sẹt khi kết thúc câu.
   * - Đảm bảo sample đầu tiên và cuối cùng có biên độ chính xác bằng 0.
   */
  public static applyMicroFades(
    pcmBuffer: Buffer,
    sampleRate: number = 24000,
    fadeInMs: number = 10,
    fadeOutMs: number = 20
  ): Buffer {
    if (pcmBuffer.length < 4) return pcmBuffer;

    // Tạo bản sao để không thay đổi buffer gốc ngoài ý muốn
    const cleanBuffer = Buffer.from(pcmBuffer);
    const samples = new Int16Array(
      cleanBuffer.buffer,
      cleanBuffer.byteOffset,
      cleanBuffer.byteLength / 2
    );

    const totalSamples = samples.length;
    const fadeInSamples = Math.min(
      Math.round((fadeInMs / 1000) * sampleRate),
      Math.floor(totalSamples / 2)
    );
    const fadeOutSamples = Math.min(
      Math.round((fadeOutMs / 1000) * sampleRate),
      Math.floor(totalSamples / 2)
    );

    // Fade-in theo đường cong Hann window: 0.5 * (1 - cos(pi * i / N))
    for (let i = 0; i < fadeInSamples; i++) {
      const factor = 0.5 * (1 - Math.cos((Math.PI * i) / fadeInSamples));
      samples[i] = Math.round(samples[i] * factor);
    }

    // Fade-out theo đường cong Hann window: 0.5 * (1 + cos(pi * i / M))
    for (let i = 0; i < fadeOutSamples; i++) {
      const factor = 0.5 * (1 + Math.cos((Math.PI * i) / fadeOutSamples));
      const idx = totalSamples - fadeOutSamples + i;
      samples[idx] = Math.round(samples[idx] * factor);
    }

    // Đảm bảo tuyệt đối 2 mốc biên bằng 0
    if (totalSamples > 0) {
      samples[0] = 0;
      samples[totalSamples - 1] = 0;
    }

    return cleanBuffer;
  }

  /**
   * Chuẩn hóa bất kỳ buffer nào (kể cả có C2PA metadata) thành WAV sạch, hợp lệ.
   */
  public static standardizeToWav(
    rawBytes: Buffer,
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16,
    withMicroFades: boolean = true
  ): Buffer {
    const extracted = this.extractPcmData(rawBytes);
    let pcm = extracted.pcm;
    const actualRate = extracted.sampleRate || sampleRate;
    const actualChannels = extracted.channels || channels;
    const actualBits = extracted.bitsPerSample || bitsPerSample;

    if (withMicroFades && pcm.length > 0) {
      pcm = this.applyMicroFades(pcm, actualRate, 10, 20);
    }

    const header = this.createWavHeader(pcm.length, actualRate, actualChannels, actualBits);
    return Buffer.concat([header, pcm]);
  }

  /**
   * Ghép nhiều WAV buffers thành 1 WAV duy nhất:
   * - Tách bỏ sạch 100% metadata không phải audio (như C2PA, LIST, INFO).
   * - Áp dụng micro-fades vào từng đoạn nói.
   * - Nối liền mạch với các khoảng lặng mà không có tiếng bụp/sẹt.
   */
  public static concatenateWavBuffers(
    wavBuffers: Buffer[],
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16
  ): Buffer {
    if (wavBuffers.length === 0) {
      return Buffer.alloc(0);
    }

    const cleanPcmChunks: Buffer[] = [];
    let totalPcmLength = 0;

    for (const buf of wavBuffers) {
      if (buf.length === 0) continue;
      const extracted = this.extractPcmData(buf);
      let pcm = extracted.pcm;
      // Áp dụng micro-fade cho các đoạn audio có tín hiệu âm thanh
      if (pcm.length > 0) {
        pcm = this.applyMicroFades(pcm, sampleRate, 10, 20);
      }
      cleanPcmChunks.push(pcm);
      totalPcmLength += pcm.length;
    }

    const header = this.createWavHeader(totalPcmLength, sampleRate, channels, bitsPerSample);
    return Buffer.concat([header, ...cleanPcmChunks]);
  }

  /**
   * Tính thời lượng chính xác của âm thanh (bỏ qua metadata C2PA).
   */
  public static getDurationSec(
    wavBuffer: Buffer,
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16
  ): number {
    const extracted = this.extractPcmData(wavBuffer);
    const pcmLength = extracted.pcm.length;
    const rate = extracted.sampleRate || sampleRate;
    const ch = extracted.channels || channels;
    const bits = extracted.bitsPerSample || bitsPerSample;
    const byteRate = (rate * ch * bits) / 8;
    return byteRate > 0 ? pcmLength / byteRate : 0;
  }

  /**
   * Tạo buffer khoảng lặng PCM 16-bit Mono (tất cả byte = 0).
   * Luôn đảm bảo số byte là bội số của blockAlign (chẵn).
   */
  public static createSilenceBuffer(
    durationSec: number,
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16
  ): Buffer {
    const bytesPerSample = (channels * bitsPerSample) / 8;
    const numSamples = Math.round(durationSec * sampleRate);
    const length = numSamples * bytesPerSample;
    return Buffer.alloc(length);
  }

  /**
   * Chuyển đổi mili-giây sang định dạng thời gian SRT (HH:MM:SS,mmm).
   */
  public static formatSrtTime(ms: number): string {
    const hours = Math.floor(ms / 3600000);
    const minutes = Math.floor((ms % 3600000) / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const subMs = ms % 1000;
    const pad = (n: number, w: number = 2) => String(n).padStart(w, '0');
    return `${pad(hours)}:${pad(minutes)}:${pad(seconds)},${pad(subMs, 3)}`;
  }
}


