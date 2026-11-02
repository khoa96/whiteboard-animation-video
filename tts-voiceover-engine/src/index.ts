import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { VoiceManager } from './voice-manager.js';
import { ScriptPreprocessor } from './script-preprocessor.js';
import { GoogleTTSClient } from './tts-client.js';
import { AudioUtils } from './audio-utils.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(ROOT_DIR, '..');

// Load .env đa tầng (Ưu tiên tts-voiceover-engine/.env, nếu không có thì đọc root .env)
const localEnv = path.join(ROOT_DIR, '.env');
const parentEnv = path.join(PROJECT_ROOT, '.env');
if (fs.existsSync(localEnv)) {
  dotenv.config({ path: localEnv });
}
if (fs.existsSync(parentEnv)) {
  dotenv.config({ path: parentEnv });
}

// Trích xuất API Key trả phí chuẩn xác, dọn dẹp các ký tự thừa
const rawKey =
  process.env.GEMINI_API_KEY ||
  process.env.GOOGLE_API_KEY ||
  process.env.GEMINI_API_KEYS ||
  process.env.GOOGLE_API_KEYS ||
  '';

const apiKey = rawKey
  .replace(/^GEMINI_API_KEYS=/, '')
  .split(/[,;\s]+/)[0]
  .trim();

const modelMode = process.env.GEMINI_MODEL || process.env.TTS_MODEL_MODE || 'gemini-3.8-flash-tts';
const customVoiceId = process.env.CUSTOM_VOICE_ID;
const fallbackVoice = process.env.PREBUILT_FALLBACK_VOICE || 'Achird';

async function main() {
  const args = process.argv.slice(2);
  const isInitVoice = args.includes('--init-voice');
  const isGenerate = args.includes('--generate') || (!isInitVoice && args.length === 0);

  if (!apiKey) {
    console.error('❌ [ERROR] Chưa cấu hình GEMINI_API_KEY trong file .env!');
    console.error('👉 Vui lòng điền GEMINI_API_KEY=your_paid_api_key vào file .env');
    process.exit(1);
  }

  const voiceManager = new VoiceManager(apiKey);

  // 1. Chế độ khởi tạo Custom Voice ID
  if (isInitVoice) {
    console.log('═'.repeat(70));
    console.log('🎙️ KHỞI TẠO CUSTOM VOICE ID QUA GOOGLE VOICE DESIGN API (PAID TIER)');
    console.log('═'.repeat(70));
    try {
      const voiceId = await voiceManager.ensureVoiceId(true);
      console.log(`\n✅ Hoàn tất! Mã giọng đặc trưng của kênh: ${voiceId}`);
      console.log('Mã này đã được lưu vào config/voice-persona.json và .env');
    } catch (err: any) {
      console.error(`❌ Lỗi khi khởi tạo voice: ${err.message}`);
      process.exit(1);
    }
    return;
  }

  // 2. Chế độ tạo Voice-Over từ kịch bản
  if (isGenerate) {
    console.log('═'.repeat(70));
    console.log('🎙️ HỆ THỐNG TẠO VOICE-OVER ĐẶC TRƯNG CHO KÊNH (GOOGLE AI STUDIO TTS)');
    console.log('═'.repeat(70));

    // Đảm bảo có Voice ID hoặc fallback (Ưu tiên config/voice-persona.json, sau đó tới .env)
    let activeVoiceId: string | undefined;
    try {
      const config = voiceManager.loadConfig();
      if (config.customVoiceId && config.customVoiceId.startsWith('voice_')) {
        activeVoiceId = config.customVoiceId;
      }
    } catch (_) {}

    if (!activeVoiceId && customVoiceId && customVoiceId.startsWith('voice_')) {
      activeVoiceId = customVoiceId;
    }

    console.log(`[Config] Model Mode:     ${modelMode} (Khóa cố định, không trôi âm sắc)`);
    console.log(`[Config] Custom Voice ID: ${activeVoiceId || '(Chưa có - Dùng prebuilt fallback)'}`);
    console.log(`[Config] Fallback Voice:  ${fallbackVoice}`);

    // Xác định file kịch bản đầu vào
    let inputFile = path.join(ROOT_DIR, 'inputs', 'sample-script.txt');
    const fileArgIdx = args.indexOf('--file');
    if (fileArgIdx !== -1 && args[fileArgIdx + 1]) {
      inputFile = path.resolve(args[fileArgIdx + 1]);
    }

    if (!fs.existsSync(inputFile)) {
      console.error(`❌ [ERROR] Không tìm thấy file kịch bản đầu vào tại: ${inputFile}`);
      process.exit(1);
    }

    console.log(`[Input]  Đọc kịch bản:   ${inputFile}`);
    const rawScript = fs.readFileSync(inputFile, 'utf-8');

    // Tiền xử lý kịch bản chuẩn A1
    console.log(`\n[BƯỚC 1/3] Tiền xử lý kịch bản (Chuẩn A1, ngắt nhịp rõ âm cuối)...`);
    const preprocessedText = ScriptPreprocessor.preprocess(rawScript);
    console.log(`Kịch bản đã chuẩn hóa:\n---\n${preprocessedText}\n---`);

    // Chia chunk nếu kịch bản quá dài
    const chunks = ScriptPreprocessor.splitIntoChunks(preprocessedText, 1800);
    console.log(`\n[BƯỚC 2/3] Gọi Gemini TTS API (Tổng cộng: ${chunks.length} mẻ)...`);

    const ttsClient = new GoogleTTSClient({
      apiKey,
      modelMode,
      customVoiceId: activeVoiceId,
      fallbackVoice,
    });

    const audioChunks: Buffer[] = [];
    let totalSec = 0;
    let totalTokens = 0;
    let totalCostUsd = 0;

    for (let i = 0; i < chunks.length; i++) {
      console.log(`  -> Đang sinh mẻ ${i + 1}/${chunks.length} (${chunks[i].length} ký tự)...`);
      const result = await ttsClient.synthesizeSpeech(chunks[i]);
      audioChunks.push(result.audioBuffer);
      totalSec += result.durationSec;
      totalTokens += result.audioTokens;
      totalCostUsd += result.estimatedCostUsd;
      console.log(`     ✓ Xong mẻ ${i + 1} (${result.durationSec.toFixed(2)}s | ${result.audioTokens} tokens)`);
    }

    // Đóng gói và lưu file WAV
    console.log(`\n[BƯỚC 3/3] Đóng gói chuẩn WAV 44-byte Header...`);
    const finalWavBuffer = AudioUtils.concatenateWavBuffers(audioChunks, 24000, 1, 16);

    const outputsDir = path.join(ROOT_DIR, 'outputs');
    if (!fs.existsSync(outputsDir)) {
      fs.mkdirSync(outputsDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputFile = path.join(outputsDir, `voiceover_${timestamp}.wav`);
    fs.writeFileSync(outputFile, finalWavBuffer);

    const totalCostVnd = Math.round(totalCostUsd * 25400);

    console.log('═'.repeat(70));
    console.log(`🎉 [XUẤT SẮC] ĐÃ SINH FILE VOICE-OVER HOÀN TẤT!`);
    console.log(`📁 Đường dẫn file xuất: ${outputFile}`);
    console.log(`⏱️ Thời lượng audio:    ${totalSec.toFixed(2)} giây (~${(totalSec / 60).toFixed(1)} phút)`);
    console.log(`📦 Kích thước file:      ${(finalWavBuffer.length / 1024).toFixed(1)} KB`);
    console.log(`🎙️ Model sử dụng:       ${ttsClient.getModelName()}`);
    console.log(`🪙 Audio Tokens:        ${totalTokens.toLocaleString()} tokens`);
    console.log(`💵 Chi phí ước tính:    $${totalCostUsd.toFixed(4)} USD (~ ${totalCostVnd.toLocaleString('vi-VN')} VNĐ)`);
    console.log('═'.repeat(70));
  }
}

main().catch((err) => {
  console.error('\n❌ Uncaught Exception:', err);
  process.exit(1);
});
