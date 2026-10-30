import fs from 'fs';

export class AudioUtils {
  /**
   * Tạo 44 bytes chuẩn WAV Header cho dữ liệu PCM 16-bit Mono.
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
   * Đảm bảo Buffer luôn có định dạng WAV hợp lệ (bổ sung header nếu là PCM thô).
   */
  public static standardizeToWav(
    rawBytes: Buffer,
    sampleRate: number = 24000,
    channels: number = 1,
    bitsPerSample: number = 16
  ): Buffer {
    // Kiểm tra 4 byte đầu tiên xem có chữ ký 'RIFF' hay không
    if (rawBytes.length >= 4 && rawBytes.toString('ascii', 0, 4) === 'RIFF') {
      return rawBytes;
    }

    // Nếu là PCM thô, tạo header và nối vào đầu
    const header = this.createWavHeader(rawBytes.length, sampleRate, channels, bitsPerSample);
    return Buffer.concat([header, rawBytes]);
  }

  /**
   * Nối nhiều file/buffer WAV lại với nhau thành 1 file WAV duy nhất
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
    if (wavBuffers.length === 1) {
      return this.standardizeToWav(wavBuffers[0], sampleRate, channels, bitsPerSample);
    }

    // Trích xuất phần raw PCM của từng buffer (bỏ qua 44 bytes header nếu đã có)
    const pcmChunks: Buffer[] = [];
    let totalPcmLength = 0;

    for (const buf of wavBuffers) {
      let pcm = buf;
      if (buf.length >= 44 && buf.toString('ascii', 0, 4) === 'RIFF') {
        pcm = buf.subarray(44);
      }
      pcmChunks.push(pcm);
      totalPcmLength += pcm.length;
    }

    const header = this.createWavHeader(totalPcmLength, sampleRate, channels, bitsPerSample);
    return Buffer.concat([header, ...pcmChunks]);
  }

  /**
   * Tính thời lượng ước tính của file WAV (giây)
   */
  public static getDurationSec(wavBuffer: Buffer, sampleRate: number = 24000, channels: number = 1, bitsPerSample: number = 16): number {
    let pcmLength = wavBuffer.length;
    if (wavBuffer.length >= 44 && wavBuffer.toString('ascii', 0, 4) === 'RIFF') {
      pcmLength = wavBuffer.length - 44;
    }
    const byteRate = (sampleRate * channels * bitsPerSample) / 8;
    return byteRate > 0 ? pcmLength / byteRate : 0;
  }
}
