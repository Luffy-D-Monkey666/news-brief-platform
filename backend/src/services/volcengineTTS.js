/**
 * 火山引擎 TTS 服务
 * 使用豆包语音合成模型，提供高质量中文语音合成
 */

const crypto = require('crypto');
const https = require('https');

// 配置
const config = {
  appId: process.env.VOLC_APP_ID || '1292782583',
  accessKeyId: process.env.VOLC_ACCESS_KEY_ID,
  secretAccessKey: process.env.VOLC_SECRET_ACCESS_KEY,
  // 语音合成 API 地址
  host: 'openspeech.bytedance.com',
  apiPath: '/api/v1/tts',
};

// 音色配置 - 火山引擎豆包语音
const voiceTypes = {
  // 女声
  'zh_female_tianmei': { name: '甜美女声', description: '甜美、温柔' },
  'zh_female_shuangkuai': { name: '爽快女声', description: '爽朗、活泼' },
  'BV001_streaming': { name: '通用女声', description: '自然、标准' },
  'BV002_streaming': { name: '通用男声', description: '自然、标准' },
  // 特色音色
  'zh_male_rap': { name: '说唱男声', description: '有节奏感' },
  'zh_female_story': { name: '故事女声', description: '娓娓道来，适合讲故事' },
  'zh_male_news': { name: '新闻男声', description: '播音腔，适合新闻播报' },
  'zh_female_news': { name: '新闻女声', description: '播音腔，适合新闻播报' },
};

// 默认音色
const DEFAULT_VOICE = 'zh_female_news';

/**
 * 生成签名
 */
function generateSignature(params, secretKey) {
  const sortedKeys = Object.keys(params).sort();
  const queryString = sortedKeys.map(key => `${key}=${params[key]}`).join('&');
  
  const hmac = crypto.createHmac('sha256', secretKey);
  hmac.update(queryString);
  return hmac.digest('hex');
}

/**
 * 调用火山引擎 TTS API
 * @param {string} text - 要合成的文本
 * @param {string} voiceType - 音色类型
 * @param {object} options - 其他选项
 * @returns {Promise<Buffer>} - 音频数据 (MP3)
 */
async function synthesize(text, voiceType = DEFAULT_VOICE, options = {}) {
  const {
    speed = 1.0,      // 语速 0.5-2.0
    volume = 1.0,     // 音量 0.5-2.0
    pitch = 1.0,      // 音调 0.5-2.0
  } = options;

  // 检查配置
  if (!config.accessKeyId || !config.secretAccessKey) {
    throw new Error('火山引擎 TTS 未配置 Access Key');
  }

  // 构建请求体
  const requestBody = {
    app: {
      appid: config.appId,
      token: 'access_token', // 使用 access key 认证时可以是任意值
      cluster: 'volcano_tts',
    },
    user: {
      uid: 'newshub_user',
    },
    audio: {
      voice_type: voiceType,
      encoding: 'mp3',
      speed_ratio: speed,
      volume_ratio: volume,
      pitch_ratio: pitch,
    },
    request: {
      reqid: `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      text: text,
      text_type: 'plain',
      operation: 'query',
    },
  };

  // 使用 HTTP API 调用
  const postData = JSON.stringify(requestBody);
  
  // 生成认证 header
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const nonce = crypto.randomBytes(16).toString('hex');
  
  return new Promise((resolve, reject) => {
    const options = {
      hostname: config.host,
      port: 443,
      path: config.apiPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Authorization': `Bearer; ${config.accessKeyId}; ${config.secretAccessKey}`,
      },
    };

    const req = https.request(options, (res) => {
      const chunks = [];
      
      res.on('data', (chunk) => {
        chunks.push(chunk);
      });
      
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        
        if (res.statusCode !== 200) {
          try {
            const errorData = JSON.parse(body.toString());
            reject(new Error(`TTS API 错误: ${errorData.message || res.statusCode}`));
          } catch {
            reject(new Error(`TTS API 错误: ${res.statusCode}`));
          }
          return;
        }
        
        try {
          const response = JSON.parse(body.toString());
          if (response.code !== 0 && response.code !== 3000) {
            reject(new Error(`TTS 合成失败: ${response.message}`));
            return;
          }
          
          // 返回 base64 编码的音频数据
          if (response.data) {
            const audioBuffer = Buffer.from(response.data, 'base64');
            resolve(audioBuffer);
          } else {
            reject(new Error('TTS 响应中没有音频数据'));
          }
        } catch (e) {
          reject(new Error(`解析 TTS 响应失败: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`TTS 请求失败: ${e.message}`));
    });

    req.write(postData);
    req.end();
  });
}

/**
 * 使用 WebSocket 流式合成（备用方案）
 * 火山引擎推荐使用 WebSocket 进行大段文本合成
 */
async function synthesizeWithWebSocket(text, voiceType = DEFAULT_VOICE, options = {}) {
  // WebSocket 实现（如需要可后续添加）
  // 目前先使用 HTTP API
  return synthesize(text, voiceType, options);
}

/**
 * 获取可用音色列表
 */
function getAvailableVoices() {
  return Object.entries(voiceTypes).map(([id, info]) => ({
    id,
    ...info,
  }));
}

module.exports = {
  synthesize,
  synthesizeWithWebSocket,
  getAvailableVoices,
  voiceTypes,
  DEFAULT_VOICE,
};
