import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { VoicePersonaConfig, VoiceCreationResponse } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const CONFIG_PATH = path.resolve(__dirname, '../config/voice-persona.json');
const ENV_PATH = path.resolve(__dirname, '../.env');

export class VoiceManager {
  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  public loadConfig(): VoicePersonaConfig {
    if (fs.existsSync(CONFIG_PATH)) {
      const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
      return JSON.parse(raw);
    }
    throw new Error(`Không tìm thấy file cấu hình tại: ${CONFIG_PATH}`);
  }

  public async ensureVoiceId(forceRecreate: boolean = false): Promise<string> {
    const config = this.loadConfig();

    if (!forceRecreate && config.customVoiceId && config.customVoiceId.startsWith('voice_')) {
      console.log(`[VoiceManager] ✓ Sử dụng Custom Voice ID có sẵn: ${config.customVoiceId}`);
      return config.customVoiceId;
    }

    console.log(`[VoiceManager] 🚀 Bắt đầu tạo mới Custom Voice ID qua Google AI Studio Voice Design API...`);
    console.log(`[VoiceManager] Prompt: "${config.voiceDesignPrompt}"`);

    const url = `https://generativelanguage.googleapis.com/v1beta/voices?key=${this.apiKey}`;
    const payload = {
      store: true,
      voice: {
        model: 'gemini-3.8-flash-tts',
        type: 'prompted',
        display_name: 'Channel_Bilingual_Teacher_22',
        gender: 'male',
        language_code: 'vi-VN',
        prompted: {
          input: config.voiceDesignPrompt,
        },
      },
    };

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`[VoiceManager] Lỗi tạo Custom Voice (HTTP ${response.status}): ${errText}`);
    }

    const data = (await response.json()) as VoiceCreationResponse;
    const newVoiceId = data.id;

    console.log(`[VoiceManager] 🎉 TẠO CUSTOM VOICE THÀNH CÔNG! Voice ID: ${newVoiceId}`);

    // Cập nhật lại config/voice-persona.json
    config.customVoiceId = newVoiceId;
    config.createdAt = new Date().toISOString();
    if (data.expire_time) {
      config.expireTime = data.expire_time;
    }
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');

    // Cập nhật .env nếu có
    if (fs.existsSync(ENV_PATH)) {
      let envContent = fs.readFileSync(ENV_PATH, 'utf-8');
      if (envContent.includes('CUSTOM_VOICE_ID=')) {
        envContent = envContent.replace(/CUSTOM_VOICE_ID=.*/, `CUSTOM_VOICE_ID=${newVoiceId}`);
      } else {
        envContent += `\nCUSTOM_VOICE_ID=${newVoiceId}\n`;
      }
      fs.writeFileSync(ENV_PATH, envContent, 'utf-8');
    }

    return newVoiceId;
  }
}
