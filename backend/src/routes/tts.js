/**
 * TTS (文字转语音) API 路由
 * 使用火山引擎豆包语音合成
 */

const express = require('express');
const router = express.Router();

// 简单的内存缓存（生产环境建议使用 Redis）
const audioCache = new Map();
const CACHE_MAX_SIZE = 100;
const CACHE_TTL = 30 * 60 * 1000; // 30分钟

/**
 * 清理过期缓存
 */
function cleanupCache() {
  const now = Date.now();
  for (const [key, value] of audioCache.entries()) {
    if (now - value.timestamp > CACHE_TTL) {
      audioCache.delete(key);
    }
  }
  // 如果超过最大数量，删除最旧的
  if (audioCache.size > CACHE_MAX_SIZE) {
    const entries = Array.from(audioCache.entries())
      .sort((a, b) => a[1].timestamp - b[1].timestamp);
    const deleteCount = audioCache.size - CACHE_MAX_SIZE;
    for (let i = 0; i < deleteCount; i++) {
      audioCache.delete(entries[i][0]);
    }
  }
}

/**
 * 生成缓存 key
 */
function getCacheKey(text, voice) {
  const crypto = require('crypto');
  return crypto.createHash('md5').update(`${voice}:${text}`).digest('hex');
}

/**
 * GET /api/tts/voices
 * 获取可用音色列表
 */
router.get('/voices', (req, res) => {
  try {
    const volcTTS = require('../services/volcengineTTS');
    const voices = volcTTS.getAvailableVoices();
    res.json({
      success: true,
      data: voices,
      default: volcTTS.DEFAULT_VOICE,
    });
  } catch (error) {
    console.error('获取音色列表失败:', error);
    res.status(500).json({
      success: false,
      error: '获取音色列表失败',
    });
  }
});

/**
 * POST /api/tts/synthesize
 * 合成语音
 * Body: { text: string, voice?: string, speed?: number, volume?: number, pitch?: number }
 */
router.post('/synthesize', async (req, res) => {
  try {
    const { text, voice, speed, volume, pitch } = req.body;
    
    if (!text || typeof text !== 'string') {
      return res.status(400).json({
        success: false,
        error: '缺少 text 参数',
      });
    }
    
    // 限制文本长度（火山引擎单次最多 500 字符）
    if (text.length > 500) {
      return res.status(400).json({
        success: false,
        error: '文本过长，最多支持 500 字符',
      });
    }
    
    const volcTTS = require('../services/volcengineTTS');
    const voiceType = voice || volcTTS.DEFAULT_VOICE;
    
    // 检查缓存
    const cacheKey = getCacheKey(text, voiceType);
    if (audioCache.has(cacheKey)) {
      const cached = audioCache.get(cacheKey);
      console.log(`[TTS] 缓存命中: ${cacheKey.substring(0, 8)}...`);
      res.set('Content-Type', 'audio/mpeg');
      res.set('X-Cache', 'HIT');
      return res.send(cached.data);
    }
    
    // 调用 TTS API
    console.log(`[TTS] 合成请求: ${text.substring(0, 50)}... (voice: ${voiceType})`);
    const audioBuffer = await volcTTS.synthesize(text, voiceType, {
      speed: speed || 1.0,
      volume: volume || 1.0,
      pitch: pitch || 1.0,
    });
    
    // 存入缓存
    audioCache.set(cacheKey, {
      data: audioBuffer,
      timestamp: Date.now(),
    });
    cleanupCache();
    
    console.log(`[TTS] 合成成功: ${audioBuffer.length} bytes`);
    
    res.set('Content-Type', 'audio/mpeg');
    res.set('X-Cache', 'MISS');
    res.send(audioBuffer);
    
  } catch (error) {
    console.error('[TTS] 合成失败:', error);
    res.status(500).json({
      success: false,
      error: error.message || '语音合成失败',
    });
  }
});

/**
 * GET /api/tts/brief/:id
 * 获取指定新闻简报的语音
 */
router.get('/brief/:id', async (req, res) => {
  try {
    const Brief = require('../models/Brief');
    const brief = await Brief.findById(req.params.id);
    
    if (!brief) {
      return res.status(404).json({
        success: false,
        error: '简报不存在',
      });
    }
    
    // 构建朗读文本
    const text = `${brief.title}。${brief.summary}`;
    
    // 限制长度
    const truncatedText = text.length > 500 ? text.substring(0, 497) + '...' : text;
    
    const volcTTS = require('../services/volcengineTTS');
    const voice = req.query.voice || volcTTS.DEFAULT_VOICE;
    
    // 检查缓存
    const cacheKey = getCacheKey(truncatedText, voice);
    if (audioCache.has(cacheKey)) {
      const cached = audioCache.get(cacheKey);
      res.set('Content-Type', 'audio/mpeg');
      res.set('X-Cache', 'HIT');
      return res.send(cached.data);
    }
    
    // 合成
    const audioBuffer = await volcTTS.synthesize(truncatedText, voice);
    
    // 缓存
    audioCache.set(cacheKey, {
      data: audioBuffer,
      timestamp: Date.now(),
    });
    cleanupCache();
    
    res.set('Content-Type', 'audio/mpeg');
    res.set('X-Cache', 'MISS');
    res.send(audioBuffer);
    
  } catch (error) {
    console.error('[TTS] 简报语音合成失败:', error);
    res.status(500).json({
      success: false,
      error: error.message || '语音合成失败',
    });
  }
});

module.exports = router;
