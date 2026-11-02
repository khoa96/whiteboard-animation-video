import { TTSClientOptions, SynthesizeResult } from './types.js';
import { AudioUtils } from './audio-utils.js';

export class GoogleTTSClient {
  private apiKey: string;
  private modelMode: string;
  private customVoiceId?: string;
  private fallbackVoice: string;

  constructor(options: TTSClientOptions) {
    this.apiKey = options.apiKey;
    this.modelMode = options.modelMode || 'gemini-3.8-flash-tts';
    this.customVoiceId = options.customVoiceId;
    this.fallbackVoice = options.fallbackVoice || 'Achird';
  }

  public getModelName(): string {
    return this.modelMode;
  }

  public async synthesizeSpeech(text: string, maxRetries: number = 5): Promise<SynthesizeResult> {
    // Cấu hình voice: Ưu tiên Custom Voice ID nếu có, nếu không thì dùng fallback prebuiltVoiceConfig
    let voiceConfig: Record<string, any>;
    if (this.customVoiceId && this.customVoiceId.startsWith('voice_')) {
      voiceConfig = {
        voice: this.customVoiceId,
      };
    } else {
      voiceConfig = {
        prebuiltVoiceConfig: {
          voiceName: this.fallbackVoice,
        },
      };
    }

    const payload = {
      contents: [
        {
          parts: [{ text: text }],
        },
      ],
      generationConfig: {
        responseModalities: ['AUDIO'],
        speechConfig: {
          voiceConfig: voiceConfig,
        },
      },
    };

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.modelMode}:generateContent?key=${this.apiKey}`;

    let attempt = 0;
    while (attempt < maxRetries) {
      attempt++;
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'tts-voiceover-engine/1.0',
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errBody = await response.text();

          // Xử lý lỗi tạm thời (429 micro-spike hoặc 503 Server Busy): Thử lại trên CÙNG MODEL với Exponential Backoff & Jitter
          if (response.status === 429 || response.status === 503) {
            const backoffMs = Math.min(10000, Math.pow(2, attempt) * 1000 + Math.floor(Math.random() * 500));
            console.warn(
              `[GoogleTTSClient] ⚠️ Model ${this.modelMode} phản hồi HTTP ${response.status}. Thử lại sau ${backoffMs}ms (Lần ${attempt}/${maxRetries})...`
            );
            await new Promise((r) => setTimeout(r, backoffMs));
            continue;
          }

          throw new Error(`Google TTS API Error (${response.status}): ${errBody}`);
        }

        const data = (await response.json()) as any;
        const candidates = data.candidates || [];
        if (candidates.length === 0) {
          throw new Error(`Google TTS API không trả về candidate nào: ${JSON.stringify(data)}`);
        }

        const parts = candidates[0].content?.parts || [];
        for (const p of parts) {
          if (p.inlineData && p.inlineData.data) {
            const base64Data = p.inlineData.data;
            const mimeType = p.inlineData.mimeType || 'audio/l16; rate=24000';
            const rawBytes = Buffer.from(base64Data, 'base64');

            // Chuẩn hóa sang WAV 24000Hz 16-bit Mono
            const wavBuffer = AudioUtils.standardizeToWav(rawBytes, 24000, 1, 16);
            const durationSec = AudioUtils.getDurationSec(wavBuffer, 24000, 1, 16);

            // Tính toán số lượng audio token (25 tokens/giây) và ước tính chi phí
            const audioTokens = Math.round(durationSec * 25);
            const pricePerMillion = this.modelMode.toLowerCase().includes('lite') ? 6.0 : 9.0;
            const estimatedCostUsd = (audioTokens / 1_000_000) * pricePerMillion;

            return {
              audioBuffer: wavBuffer,
              durationSec: durationSec,
              sampleRate: 24000,
              channels: 1,
              mimeType: mimeType,
              audioTokens: audioTokens,
              estimatedCostUsd: estimatedCostUsd,
            };
          }
        }

        throw new Error('Không tìm thấy dữ liệu audio inlineData trong phản hồi của Gemini.');
      } catch (err: any) {
        if (attempt >= maxRetries) {
          throw err;
        }
        const waitMs = 2000 + attempt * 500;
        console.warn(`[GoogleTTSClient] Lỗi kết nối (${err.message}). Đang thử lại sau ${waitMs}ms...`);
        await new Promise((r) => setTimeout(r, waitMs));
      }
    }

    throw new Error(`Không thể sinh giọng nói sau ${maxRetries} lần thử với model ${this.modelMode}.`);
  }
}
