/**
 * 火山引擎 TTS 服务
 * 使用豆包语音合成，提供高质量中文语音合成
 * 
 * 官方文档：https://www.volcengine.com/docs/6561/79820
 */

const https = require('https');

// 配置 - 从环境变量读取
const config = {
  appId: process.env.VOLC_APP_ID || '6922135515',
  accessToken: process.env.VOLC_ACCESS_TOKEN,
  cluster: process.env.VOLC_CLUSTER || 'volcano_tts',
  host: 'openspeech.bytedance.com',
  apiPath: '/api/v1/tts',
};

// 音色配置 - 火山引擎 BV 系列音色
const voiceTypes = {
  // === 通用场景（推荐） ===
  'BV700_V2_streaming': { name: '灿灿 2.0', description: '通用场景', lang: 'cn' },
  'BV705_streaming': { name: '炀炀', description: '通用场景', lang: 'cn' },
  'BV701_V2_streaming': { name: '擎苍 2.0', description: '通用场景', lang: 'cn' },
  'BV001_V2_streaming': { name: '通用女声 2.0', description: '通用场景', lang: 'cn' },
  'BV001_streaming': { name: '通用女声', description: '通用场景', lang: 'cn' },
  'BV002_streaming': { name: '通用男声', description: '通用场景', lang: 'cn' },
  
  // === 超自然音色 ===
  'BV406_V2_streaming': { name: '梓梓 2.0', description: '超自然音色', lang: 'cn' },
  'BV407_V2_streaming': { name: '燃燃 2.0', description: '超自然音色', lang: 'cn' },
  
  // === 有声阅读 ===
  'BV701_streaming': { name: '擎苍', description: '有声阅读', lang: 'cn' },
  'BV123_streaming': { name: '阳光青年', description: '有声阅读', lang: 'cn' },
  'BV115_streaming': { name: '古风少御', description: '有声阅读', lang: 'cn' },
  'BV102_streaming': { name: '儒雅青年', description: '有声阅读', lang: 'cn' },
  'BV104_streaming': { name: '温柔淑女', description: '有声阅读', lang: 'cn' },
  'BV113_streaming': { name: '甜宠少御', description: '有声阅读', lang: 'cn' },
  
  // === 智能助手 ===
  'BV405_streaming': { name: '甜美小源', description: '智能助手', lang: 'cn' },
  'BV007_streaming': { name: '亲切女声', description: '智能助手', lang: 'cn' },
  'BV009_streaming': { name: '知性女声', description: '智能助手', lang: 'cn' },
  'BV008_streaming': { name: '亲切男声', description: '智能助手', lang: 'cn' },
  
  // === 视频配音 ===
  'BV056_streaming': { name: '阳光男声', description: '视频配音', lang: 'cn' },
  'BV005_streaming': { name: '活泼女声', description: '视频配音', lang: 'cn' },
  'BV411_streaming': { name: '影视解说小帅', description: '视频配音', lang: 'cn' },
  'BV412_streaming': { name: '影视解说小美', description: '视频配音', lang: 'cn' },
  'BV142_streaming': { name: '沉稳解说男', description: '视频配音', lang: 'cn' },
  
  // === 新闻播报 ===
  'BV011_streaming': { name: '新闻女声', description: '新闻播报', lang: 'cn' },
  'BV012_streaming': { name: '新闻男声', description: '新闻播报', lang: 'cn' },
  
  // === 特色音色 ===
  'BV051_streaming': { name: '奶气萌娃', description: '特色音色', lang: 'cn' },
  'BV061_streaming': { name: '天才童声', description: '特色音色', lang: 'cn' },
  
  // === 多语种 ===
  'BV504_streaming': { name: '活力男声-Jackson', description: '美式发音', lang: 'en' },
  'BV503_streaming': { name: '活力女声-Ariana', description: '美式发音', lang: 'en' },
};

// 默认音色 - 使用灿灿 2.0（通用场景推荐）
const DEFAULT_VOICE = 'BV700_V2_streaming';

/**
 * 调用火山引擎 TTS API
 */
async function synthesize(text, voiceType = DEFAULT_VOICE, options = {}) {
  const {
    speed = 1.0,
    volume = 1.0,
    pitch = 1.0,
  } = options;

  if (!config.accessToken) {
    throw new Error('火山引擎 TTS 未配置 Access Token (VOLC_ACCESS_TOKEN)');
  }

  // 验证音色
  if (!voiceTypes[voiceType]) {
    console.warn(`[TTS] 未知音色 ${voiceType}，使用默认音色 ${DEFAULT_VOICE}`);
    voiceType = DEFAULT_VOICE;
  }

  const reqid = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const requestBody = {
    app: {
      appid: config.appId,
      token: 'access_token',
      cluster: config.cluster,
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
      reqid: reqid,
      text: text,
      text_type: 'plain',
      operation: 'query',
    },
  };

  const postData = JSON.stringify(requestBody);
  
  return new Promise((resolve, reject) => {
    const reqOptions = {
      hostname: config.host,
      port: 443,
      path: config.apiPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Authorization': `Bearer;${config.accessToken}`,
      },
    };

    console.log(`[TTS] 请求: voice=${voiceType}, text_len=${text.length}`);

    const req = https.request(reqOptions, (res) => {
      const chunks = [];
      
      res.on('data', (chunk) => chunks.push(chunk));
      
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        const bodyStr = body.toString();
        
        try {
          const response = JSON.parse(bodyStr);
          
          if (response.code !== 3000) {
            console.error(`[TTS] 错误: code=${response.code}, msg=${response.message}`);
            reject(new Error(`TTS 合成失败: ${response.message || `错误码 ${response.code}`}`));
            return;
          }
          
          if (response.data) {
            const audioBuffer = Buffer.from(response.data, 'base64');
            console.log(`[TTS] 成功: ${audioBuffer.length} bytes`);
            resolve(audioBuffer);
          } else {
            reject(new Error('TTS 响应中没有音频数据'));
          }
        } catch (e) {
          reject(new Error(`解析 TTS 响应失败: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => reject(new Error(`TTS 请求失败: ${e.message}`)));
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('TTS 请求超时 (30s)'));
    });

    req.write(postData);
    req.end();
  });
}

function getAvailableVoices() {
  return Object.entries(voiceTypes).map(([id, info]) => ({
    id,
    ...info,
  }));
}

module.exports = {
  synthesize,
  getAvailableVoices,
  voiceTypes,
  DEFAULT_VOICE,
};
