import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { VoiceManager } from './voice-manager.js';
import { ScriptPreprocessor } from './script-preprocessor.js';
import { GoogleTTSClient } from './tts-client.js';
import { AudioUtils } from './audio-utils.js';
import { TimingCue, TimingMasterData } from './types.js';
import { MultimodalAligner } from './multimodal-aligner.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(ROOT_DIR, '..');

// Đọc duy nhất file .env từ thư mục gốc của dự án
const parentEnv = path.join(PROJECT_ROOT, '.env');
if (fs.existsSync(parentEnv)) {
  dotenv.config({ path: parentEnv });
}

// Trích xuất API Key chuẩn xác
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

function getArgValue(args: string[], keys: string[]): string | undefined {
  for (const k of keys) {
    const idx = args.indexOf(k);
    if (idx !== -1 && args[idx + 1] && !args[idx + 1].startsWith('-')) {
      return args[idx + 1];
    }
  }
  return undefined;
}

function hasArg(args: string[], keys: string[]): boolean {
  return keys.some((k) => args.includes(k));
}

async function main() {
  const args = process.argv.slice(2);
  const isInitVoice = hasArg(args, ['--init-voice']);
  const isGenerate = !isInitVoice;

  if (!apiKey) {
    console.error('❌ [ERROR] Chưa cấu hình GEMINI_API_KEY trong file .env tại gốc dự án!');
    console.error('👉 Vui lòng điền GEMINI_API_KEY=your_key vào file .env');
    process.exit(1);
  }

  const voiceManager = new VoiceManager(apiKey);

  // 1. Chế độ khởi tạo Custom Voice ID độc quyền
  if (isInitVoice) {
    console.log('═'.repeat(70));
    console.log('🎙️ KHỞI TẠO CUSTOM VOICE ID QUA GOOGLE VOICE DESIGN API (PAID TIER)');
    console.log('═'.repeat(70));
    try {
      const voiceId = await voiceManager.ensureVoiceId(true);
      console.log(`\n✅ Hoàn tất! Mã giọng đặc trưng của kênh: ${voiceId}`);
      console.log('Mã này đã được lưu vào config/voice-persona.json và .env gốc');
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

    // Cho phép người dùng chọn giọng trực tiếp qua cờ --voice <tên_hoặc_id>
    const voiceArg = getArgValue(args, ['--voice', '-v']);
    let activeVoiceId: string | undefined;
    let selectedVoiceName = fallbackVoice;

    if (voiceArg) {
      if (voiceArg.startsWith('voice_')) {
        activeVoiceId = voiceArg;
        selectedVoiceName = '(Custom Voice ID)';
      } else {
        activeVoiceId = undefined;
        selectedVoiceName = voiceArg;
      }
    } else {
      // Ưu tiên config/voice-persona.json, sau đó tới .env
      try {
        const config = voiceManager.loadConfig();
        if (config.customVoiceId && config.customVoiceId.startsWith('voice_')) {
          activeVoiceId = config.customVoiceId;
        }
      } catch (_) {}

      if (!activeVoiceId && customVoiceId && customVoiceId.startsWith('voice_')) {
        activeVoiceId = customVoiceId;
      }
    }

    console.log(`[Config] Model Mode:     ${modelMode}`);
    console.log(`[Config] Custom Voice ID: ${activeVoiceId || '(Không dùng - Dùng prebuilt voice)'}`);
    console.log(`[Config] Voice Name:      ${activeVoiceId ? activeVoiceId : selectedVoiceName}`);

    // Xác định file kịch bản đầu vào
    const fileArg = getArgValue(args, ['--file', '--input', '-f', '-i']);
    let inputFile = path.join(ROOT_DIR, 'inputs', 'sample-script.txt');
    if (fileArg) {
      inputFile = path.resolve(fileArg);
    }

    if (!fs.existsSync(inputFile)) {
      console.error(`❌ [ERROR] Không tìm thấy file kịch bản đầu vào tại: ${inputFile}`);
      process.exit(1);
    }

    console.log(`[Input]  Đọc kịch bản:   ${inputFile}`);
    const rawScript = fs.readFileSync(inputFile, 'utf-8');

    // Các cờ cấu hình thời gian và file xuất
    const outputArg = getArgValue(args, ['--output', '-o']);
    const srtArg = getArgValue(args, ['--srt']);
    const cuesArg = getArgValue(args, ['--cues']);
    const forceSentenceMode = hasArg(args, ['--sentence', '--per-sentence', '--line']);
    const forceChunkMode = hasArg(args, ['--chunk', '--chunk-mode', '--continuous', '--single']);
    const gapSec = parseFloat(getArgValue(args, ['--gap', '--para-gap']) || '0.6');
    const intraGapSec = parseFloat(getArgValue(args, ['--intra-gap', '--micro-gap']) || '0.25');
    const leadInSec = parseFloat(getArgValue(args, ['--lead-in']) || '0.5');
    const tailSec = parseFloat(getArgValue(args, ['--tail']) || '2.0');

    // Xác định đường dẫn file âm thanh xuất
    let targetAudioPath: string;
    if (outputArg) {
      targetAudioPath = path.resolve(outputArg);
    } else {
      const outputsDir = path.join(ROOT_DIR, 'outputs');
      if (!fs.existsSync(outputsDir)) {
        fs.mkdirSync(outputsDir, { recursive: true });
      }
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      targetAudioPath = path.join(outputsDir, `voiceover_${timestamp}.wav`);
    }

    const outputDir = path.dirname(targetAudioPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Tự động xác định đường dẫn srt & cues nếu xuất vào thư mục scene
    let targetSrtPath = srtArg ? path.resolve(srtArg) : undefined;
    let targetCuesPath = cuesArg ? path.resolve(cuesArg) : undefined;

    // Khởi tạo TTS Client
    const ttsClient = new GoogleTTSClient({
      apiKey,
      modelMode,
      customVoiceId: activeVoiceId,
      fallbackVoice: selectedVoiceName,
    });

    // Trích xuất các đơn vị câu ngắn (Sentence-level Micro-segmentation)
    const speechUnits = ScriptPreprocessor.extractSpeechUnits(rawScript);

    // Quyết định chế độ xử lý:
    // 1. Chế độ Single-Request Multimodal Align (--single-request, --align, --batch): Gom 1 Scene = 1 Request TTS + 1 Gemini Flash Align
    // 2. Chế độ Master Clock từng câu (--sentence): Gọi API từng câu (độ chính xác cơ học tuyệt đối nhưng tốn request)
    // 3. Chế độ Chunk Mode (--chunk): Gom đoạn lớn không trích xuất cues
    const isSingleRequestMode = hasArg(args, ['--single-request', '--align', '--batch', '--scene-mode']);
    const useSentenceMode = !forceChunkMode && !isSingleRequestMode;

    let finalWavBuffer: Buffer;
    let totalSec = 0;
    let totalTokens = 0;
    let totalCostUsd = 0;

    if (isSingleRequestMode && speechUnits.length > 0) {
      console.log(`\n[CHẾ ĐỘ TIẾT KIỆM QUOTA] Single-Request Audio + Multimodal Alignment...`);
      console.log(`  -> Số câu thoại cần đồng bộ: ${speechUnits.length} câu`);

      // Ghép nối các câu thoại thành đoạn văn bản đọc tự nhiên
      const speechSentences: string[] = [];
      for (const unit of speechUnits) {
        if (!unit.isTechnicalPause) {
          const clean = ScriptPreprocessor.cleanTextForTts(unit.text);
          if (clean) speechSentences.push(clean);
        }
      }
      const fullSpokenText = speechSentences.join('\n\n');

      console.log(`  -> [Bước 1/2] Gọi Gemini TTS sinh toàn bộ âm thanh trong 1 request duy nhất...`);
      const ttsResult = await ttsClient.synthesizeSpeech(fullSpokenText);
      console.log(`     ✓ Đã nhận âm thanh hoàn chỉnh (${ttsResult.durationSec.toFixed(2)}s, ${ttsResult.audioTokens} audio tokens)`);

      finalWavBuffer = ttsResult.audioBuffer;
      totalSec = ttsResult.durationSec;
      totalTokens += ttsResult.audioTokens;
      totalCostUsd += ttsResult.estimatedCostUsd;

      console.log(`  -> [Bước 2/2] Dùng Gemini 3.8 Flash Multimodal nghe và gắn nhãn mili-giây từng câu...`);
      const aligner = new MultimodalAligner(apiKey, 'gemini-3.8-flash');
      const alignResult = await aligner.alignAudio(finalWavBuffer, speechUnits);
      console.log(`     ✓ Đã trích xuất chính xác ${alignResult.cues.length} mốc thời gian phụ đề!`);

      for (const cue of alignResult.cues) {
        console.log(`       [#${cue.index}] ${cue.startMs}ms -> ${cue.endMs}ms (${(cue.durationMs/1000).toFixed(2)}s): "${cue.text.slice(0, 45)}..."`);
      }

      // Xuất file SRT nếu có đường dẫn
      if (targetSrtPath) {
        const srtContent = alignResult.cues
          .map((cue) => {
            return `${cue.index}\n${AudioUtils.formatSrtTime(cue.startMs)} --> ${AudioUtils.formatSrtTime(cue.endMs)}\n${cue.text}\n`;
          })
          .join('\n');
        fs.writeFileSync(targetSrtPath, srtContent, 'utf-8');
        console.log(`  ✓ Đã xuất phụ đề: ${targetSrtPath}`);
      }

      // Xuất file timing_cues.json nếu có đường dẫn
      if (targetCuesPath) {
        const cuesData: TimingMasterData = {
          totalDurationMs: Math.round(totalSec * 1000),
          cues: alignResult.cues,
        };
        fs.writeFileSync(targetCuesPath, JSON.stringify(cuesData, null, 2), 'utf-8');
        console.log(`  ✓ Đã xuất mốc thời gian: ${targetCuesPath}`);
      }
    } else if (useSentenceMode && speechUnits.length > 0) {
      console.log(`\n[CHẾ ĐỘ] Audio Master Clock - Sinh từng câu phụ đề vi mô (${speechUnits.length} câu ngắn)...`);
      const audioBuffers: Buffer[] = [];
      const timingCues: TimingCue[] = [];

      let currentTimeSec = leadInSec;
      if (leadInSec > 0) {
        audioBuffers.push(AudioUtils.createSilenceBuffer(leadInSec, 24000, 1, 16));
      }

      let cueIndex = 1;
      for (let i = 0; i < speechUnits.length; i++) {
        const unit = speechUnits[i];

        // Hỗ trợ nhịp dừng kỹ thuật [PAUSE X SECONDS] hoặc [SILENCE: X]
        if (unit.isTechnicalPause) {
          const pauseDurationSec = unit.pauseDurationSec || 3.0;
          console.log(`  -> [Mục ${i + 1}/${speechUnits.length}] ⏸️ [TẠM DỪNG SUY NGHĨ ${pauseDurationSec}s - KHÔNG PHÁT ÂM]`);
          audioBuffers.push(AudioUtils.createSilenceBuffer(pauseDurationSec, 24000, 1, 16));
          currentTimeSec += pauseDurationSec;
          continue;
        }

        const cleanText = ScriptPreprocessor.cleanTextForTts(unit.text);
        if (!cleanText) continue;

        console.log(`  -> [Câu ${cueIndex}/${speechUnits.length}] "${cleanText.slice(0, 60)}..."`);
        const result = await ttsClient.synthesizeSpeech(cleanText);

        const startMs = Math.round(currentTimeSec * 1000);
        const durMs = Math.round(result.durationSec * 1000);
        const endMs = startMs + durMs;

        timingCues.push({
          index: cueIndex++,
          startMs,
          endMs,
          durationMs: durMs,
          text: cleanText,
        });

        audioBuffers.push(result.audioBuffer);
        totalTokens += result.audioTokens;
        totalCostUsd += result.estimatedCostUsd;

        const isLast = i + 1 === speechUnits.length;
        let currentPauseSec = 0;
        if (isLast) {
          currentPauseSec = tailSec;
        } else if (unit.isParagraphEnd) {
          currentPauseSec = gapSec;
        } else {
          currentPauseSec = intraGapSec;
        }

        if (currentPauseSec > 0) {
          audioBuffers.push(AudioUtils.createSilenceBuffer(currentPauseSec, 24000, 1, 16));
        }
        currentTimeSec = (endMs / 1000) + currentPauseSec;
        console.log(`     ✓ Xong câu ${cueIndex - 1} (${result.durationSec.toFixed(2)}s) -> Mốc: [${startMs}ms - ${endMs}ms] (Nghỉ sau câu: ${currentPauseSec.toFixed(2)}s)`);
      }

      finalWavBuffer = AudioUtils.concatenateWavBuffers(audioBuffers, 24000, 1, 16);
      totalSec = currentTimeSec;

      // Xuất file SRT nếu có đường dẫn
      if (targetSrtPath) {
        const srtContent = timingCues
          .map((cue) => {
            return `${cue.index}\n${AudioUtils.formatSrtTime(cue.startMs)} --> ${AudioUtils.formatSrtTime(cue.endMs)}\n${cue.text}\n`;
          })
          .join('\n');
        fs.writeFileSync(targetSrtPath, srtContent, 'utf-8');
        console.log(`  ✓ Đã xuất phụ đề: ${targetSrtPath}`);
      }

      // Xuất file timing_cues.json nếu có đường dẫn
      if (targetCuesPath) {
        const cuesData: TimingMasterData = {
          totalDurationMs: Math.round(totalSec * 1000),
          cues: timingCues,
        };
        fs.writeFileSync(targetCuesPath, JSON.stringify(cuesData, null, 2), 'utf-8');
        console.log(`  ✓ Đã xuất mốc thời gian: ${targetCuesPath}`);
      }
    } else {
      console.log(`\n[CHẾ ĐỘ] Chunk Mode - Ghép đoạn văn bản lớn...`);
      const preprocessedText = ScriptPreprocessor.preprocess(rawScript);
      const chunks = ScriptPreprocessor.splitIntoChunks(preprocessedText, 1800);
      console.log(`Gọi Gemini TTS API (Tổng cộng: ${chunks.length} mẻ)...`);

      const audioChunks: Buffer[] = [];
      for (let i = 0; i < chunks.length; i++) {
        console.log(`  -> Đang sinh mẻ ${i + 1}/${chunks.length} (${chunks[i].length} ký tự)...`);
        const result = await ttsClient.synthesizeSpeech(chunks[i]);
        audioChunks.push(result.audioBuffer);
        totalSec += result.durationSec;
        totalTokens += result.audioTokens;
        totalCostUsd += result.estimatedCostUsd;
        console.log(`     ✓ Xong mẻ ${i + 1} (${result.durationSec.toFixed(2)}s)`);
      }
      finalWavBuffer = AudioUtils.concatenateWavBuffers(audioChunks, 24000, 1, 16);
    }

    // Lưu file âm thanh
    const ext = path.extname(targetAudioPath).toLowerCase();
    if (ext === '.m4a' || ext === '.mp3' || ext === '.aac') {
      const tempWav = targetAudioPath.replace(/\.[^.]+$/, '.temp.wav');
      fs.writeFileSync(tempWav, finalWavBuffer);
      try {
        const codecParam = ext === '.mp3' ? '-c:a libmp3lame -q:a 2' : '-c:a aac -b:a 192k';
        execSync(`ffmpeg -y -loglevel error -i "${tempWav}" ${codecParam} "${targetAudioPath}"`);
        if (fs.existsSync(tempWav)) {
          fs.unlinkSync(tempWav);
        }
      } catch (err: any) {
        console.warn(`[Cảnh báo] Lỗi khi chuyển đổi định dạng qua ffmpeg (${err.message}). Lưu file dưới dạng WAV.`);
        fs.renameSync(tempWav, targetAudioPath.replace(/\.[^.]+$/, '.wav'));
      }
    } else {
      fs.writeFileSync(targetAudioPath, finalWavBuffer);
    }

    const totalCostVnd = Math.round(totalCostUsd * 25400);

    console.log('═'.repeat(70));
    console.log(`🎉 [XUẤT SẮC] ĐÃ SINH FILE VOICE-OVER HOÀN TẤT!`);
    console.log(`📁 Đường dẫn audio:     ${targetAudioPath}`);
    if (targetSrtPath) console.log(`📄 Đường dẫn subtitle:  ${targetSrtPath}`);
    if (targetCuesPath) console.log(`⏱️ Đường dẫn timing:    ${targetCuesPath}`);
    console.log(`⏱️ Tổng thời lượng:     ${totalSec.toFixed(2)} giây (~${(totalSec / 60).toFixed(1)} phút)`);
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
