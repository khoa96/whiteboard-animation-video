import { TimingCue, SpeechUnit } from './types.js';

export interface AlignmentResult {
  cues: TimingCue[];
  totalDurationMs: number;
}

export class MultimodalAligner {
  private apiKey: string;
  private alignModel: string;

  constructor(apiKey: string, alignModel: string = 'gemini-3.8-flash') {
    this.apiKey = apiKey;
    this.alignModel = alignModel;
  }

  /**
   * Sử dụng Gemini Flash Multimodal để nghe file audio và gắn nhãn thời gian
   * (startMs, endMs) cho từng câu thoại trong kịch bản.
   */
  public async alignAudio(
    audioBuffer: Buffer,
    speechUnits: SpeechUnit[],
    maxRetries: number = 3
  ): Promise<AlignmentResult> {
    const audioB64 = audioBuffer.toString('base64');
    const sentences = speechUnits.map((u, i) => `${i + 1}. ${u.text}`).join('\n');

    const prompt = `You are a professional audio-visual alignment and subtitle synchronization engineer.
Attached is a single audio recording containing spoken narration.
Here is the exact transcript of sentences in order:

<TRANSCRIPT>
${sentences}
</TRANSCRIPT>

Instructions:
1. Carefully listen to the audio waveform and identify the EXACT start time (startMs) and end time (endMs) in milliseconds for EACH numbered sentence.
2. Ensure timestamps are strictly increasing and relative to the beginning of the audio (0ms).
3. Return ONLY a valid JSON object matching this schema:
{
  "cues": [
    {
      "index": 1,
      "text": "sentence text",
      "startMs": 500,
      "endMs": 1740
    }
  ]
}
Do NOT output markdown code fences (like \`\`\`json). Output pure JSON only.`;

    const payload = {
      contents: [
        {
          parts: [
            {
              inlineData: {
                mimeType: 'audio/wav',
                data: audioB64,
              },
            },
            {
              text: prompt,
            },
          ],
        },
      ],
      generationConfig: {
        responseMimeType: 'application/json',
        temperature: 0.0,
      },
    };

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.alignModel}:generateContent?key=${this.apiKey}`;

    let attempt = 0;
    while (attempt < maxRetries) {
      attempt++;
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'tts-voiceover-engine/multimodal-aligner',
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Gemini Multimodal Alignment Error (${response.status}): ${errText}`);
        }

        const data = (await response.json()) as any;
        const candidates = data.candidates || [];
        if (candidates.length === 0) {
          throw new Error('Không nhận được candidate nào từ Gemini Multimodal Aligner.');
        }

        const rawText = candidates[0].content?.parts?.[0]?.text?.trim() || '';
        const cleanJson = rawText.replace(/^```json\s*/, '').replace(/\s*```$/, '');
        const parsed = JSON.parse(cleanJson);

        const rawCues = parsed.cues || [];
        const validatedCues: TimingCue[] = [];

        for (let i = 0; i < rawCues.length; i++) {
          const c = rawCues[i];
          const startMs = Math.max(0, parseInt(c.startMs, 10) || 0);
          const endMs = Math.max(startMs + 500, parseInt(c.endMs, 10) || startMs + 1000);
          const text = speechUnits[i]?.text || c.text || '';

          validatedCues.push({
            index: i + 1,
            startMs,
            endMs,
            durationMs: endMs - startMs,
            text,
          });
        }

        // Đảm bảo tính tuần tự không bị lùi thời gian
        for (let i = 1; i < validatedCues.length; i++) {
          if (validatedCues[i].startMs < validatedCues[i - 1].startMs) {
            validatedCues[i].startMs = validatedCues[i - 1].endMs + 150;
            validatedCues[i].endMs = validatedCues[i].startMs + validatedCues[i].durationMs;
          }
        }

        const lastCue = validatedCues[validatedCues.length - 1];
        const totalDurationMs = lastCue ? lastCue.endMs + 1000 : 0;

        return {
          cues: validatedCues,
          totalDurationMs,
        };
      } catch (err: any) {
        if (attempt >= maxRetries) {
          throw err;
        }
        console.warn(`[MultimodalAligner] Lỗi align lần ${attempt}/${maxRetries} (${err.message}). Thử lại sau 2s...`);
        await new Promise((r) => setTimeout(r, 2000));
      }
    }

    throw new Error('Thất bại khi thực hiện Multimodal Audio Alignment sau nhiều lần thử.');
  }
}

