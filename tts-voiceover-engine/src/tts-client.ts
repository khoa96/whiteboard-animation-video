import { TTSClientOptions, SynthesizeResult } from './types.js';
import { AudioUtils } from './audio-utils.js';

const AVAILABLE_TTS_MODELS = [
  'gemini-3.8-flash-tts',
  'gemini-3.8-flash-lite-tts',
  'gemini-3.1-flash-tts-preview',
  'gemini-2.5-flash-preview-tts',
];

export class GoogleTTSClient {
  private apiKey: string;
  private modelMode: string;
  private customVoiceId?: string;
  private fallbackVoice: string;
  private currentModelIndex: number = 0;

  constructor(options: TTSClientOptions) {
    this.apiKey = options.apiKey;
    this.modelMode = options.modelMode || 'gemini-3.8-flash-tts';
    this.customVoiceId = options.customVoiceId;
    this.fallbackVoice = options.fallbackVoice || 'Achird';
    const initIdx = AVAILABLE_TTS_MODELS.indexOf(this.modelMode);
    this.currentModelIndex = initIdx >= 0 ? initIdx : 0;
  }

  public async synthesizeSpeech(text: string, maxRetries: number = 6): Promise<SynthesizeResult> {
    // Cấu hình voice: ưu tiên Custom Voice ID nếu có, nếu không thì dùng prebuiltVoiceConfig
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

    let attempt = 0;
    while (attempt < maxRetries) {
      attempt++;
      const currentModel = AVAILABLE_TTS_MODELS[this.currentModelIndex % AVAILABLE_TTS_MODELS.length];
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${currentModel}:generateContent?key=${this.apiKey}`;

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
          if (response.status === 429) {
            console.warn(`[GoogleTTSClient] ⚠️ Model ${currentModel} đạt hạn mức (429). Tự động xoay sang model tiếp theo...`);
            this.currentModelIndex++;
            await new Promise((r) => setTimeout(r, 1000));
            continue;
          }
          if (response.status === 503) {
            const backoffMs = Math.pow(2, attempt) * 1500;
            console.warn(`[GoogleTTSClient] ⚠️ Gặp lỗi HTTP 503. Chờ ${backoffMs}ms...`);
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

            return {
              audioBuffer: wavBuffer,
              durationSec: durationSec,
              sampleRate: 24000,
              channels: 1,
              mimeType: mimeType,
            };
          }
        }

        throw new Error('Không tìm thấy dữ liệu audio inlineData trong phản hồi của Gemini.');
      } catch (err: any) {
        if (attempt >= maxRetries) {
          throw err;
        }
        console.warn(`[GoogleTTSClient] Lỗi kết nối (${err.message}), đang thử lại...`);
        await new Promise((r) => setTimeout(r, 2000));
      }
    }

    throw new Error(`Không thể sinh giọng nói sau ${maxRetries} lần thử.`);
  }
}
