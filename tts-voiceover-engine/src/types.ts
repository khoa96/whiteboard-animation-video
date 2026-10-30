export interface VoicePersonaConfig {
  voiceDesignPrompt: string;
  styleDirective: string;
  customVoiceId?: string;
  createdAt?: string;
  expireTime?: string;
}

export interface VoiceCreationResponse {
  id: string;
  model: string;
  type: string;
  expire_time?: string;
  display_name?: string;
  prompted?: {
    input: string;
  };
  sample_audio?: {
    mime_type: string;
    data: string;
  };
}

export interface TTSClientOptions {
  apiKey: string;
  modelMode?: string;
  customVoiceId?: string;
  fallbackVoice?: string;
}

export interface SynthesizeResult {
  audioBuffer: Buffer;
  durationSec: number;
  sampleRate: number;
  channels: number;
  mimeType: string;
}
