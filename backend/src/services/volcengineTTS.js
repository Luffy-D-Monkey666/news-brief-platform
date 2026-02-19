/**
 * 火山引擎 TTS 服务
 * 使用豆包语音合成模型，提供高质量中文语音合成
 */

const https = require('https');

// 配置
const config = {
  appId: process.env.VOLC_APP_ID || '6922135515',
  accessToken: process.env.VOLC_ACCESS_TOKEN,
  // 语音合成 API 地址
  host: 'openspeech.bytedance.com',
  apiPath: '/api/v1/tts',
  cluster: 'volcano_tts',  // 火山引擎 TTS cluster
};

// 音色配置 - 火山引擎豆包大模型语音（基于用户开通的音色）
const voiceTypes = {
  // 通用场景（推荐）
  'zh_female_vv_uranus_bigtts': { name: 'vivi 2.0', description: '通用场景，自然女声' },
  // 视频配音
  'zh_male_dayi_saturn_bigtts': { name: '大壹', description: '视频配音，男声' },
  'zh_female_mizai_saturn_bigtts': { name: '黑猫侦探社咪仔', description: '视频配音，活泼女声' },
  'zh_female_jitangnv_saturn_bigtts': { name: '鸡汤女', description: '视频配音，温柔女声' },
  'zh_female_meilinvyou_saturn_bigtts': { name: '魅力女友', description: '视频配音，甜美女声' },
  'zh_female_santongyongns_saturn_bigtts': { name: '流畅女声', description: '视频配音，流畅女声' },
  'zh_male_ruyayichen_saturn_bigtts': { name: '儒雅逸辰', description: '视频配音，儒雅男声' },
  // 角色扮演
  'saturn_zh_female_cancan_tob': { name: '知性灿灿', description: '角色扮演，知性女声' },
  'saturn_zh_female_keainvsheng_tob': { name: '可爱女生', description: '角色扮演，可爱女声' },
  'saturn_zh_female_tiaopigongzhu_tob': { name: '调皮公主', description: '角色扮演，活泼女声' },
};

// 默认音色
const DEFAULT_VOICE = 'zh_female_vv_uranus_bigtts';

/**
 * 调用火山引擎 TTS API
 * @param {string} text - 要合成的文本
 * @param {string} voiceType - 音色类型
 * @param {object} options - 其他选项
 * @returns {Promise<Buffer>} - 音频数据 (MP3)
 */
async function synthesize(text, voiceType = DEFAULT_VOICE, options = {}) {
  const {
    speed = 1.0,      // 语速 0.2-3.0
    volume = 1.0,     // 音量 0.1-3.0
    pitch = 1.0,      // 音调 0.1-3.0
  } = options;

  // 检查配置
  if (!config.accessToken) {
    throw new Error('火山引擎 TTS 未配置 Access Token (VOLC_ACCESS_TOKEN)');
  }

  // 生成唯一请求 ID
  const reqid = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // 构建请求体
  const requestBody = {
    app: {
      appid: config.appId,
      token: 'access_token', // 使用 Bearer Token 认证时这个字段可以是任意值
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
    const options = {
      hostname: config.host,
      port: 443,
      path: config.apiPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Authorization': `Bearer ${config.accessToken}`,
      },
    };

    console.log(`[TTS] 请求火山引擎: voice=${voiceType}, text_len=${text.length}`);

    const req = https.request(options, (res) => {
      const chunks = [];
      
      res.on('data', (chunk) => {
        chunks.push(chunk);
      });
      
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        
        try {
          const response = JSON.parse(body.toString());
          
          // 检查响应码
          if (response.code !== 3000) {
            console.error(`[TTS] API 错误: code=${response.code}, message=${response.message}`);
            reject(new Error(`TTS 合成失败: ${response.message || `错误码 ${response.code}`}`));
            return;
          }
          
          // 返回 base64 解码的音频数据
          if (response.data) {
            const audioBuffer = Buffer.from(response.data, 'base64');
            console.log(`[TTS] 合成成功: ${audioBuffer.length} bytes`);
            resolve(audioBuffer);
          } else {
            reject(new Error('TTS 响应中没有音频数据'));
          }
        } catch (e) {
          console.error(`[TTS] 解析响应失败: ${e.message}`);
          console.error(`[TTS] 原始响应: ${body.toString().substring(0, 200)}`);
          reject(new Error(`解析 TTS 响应失败: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      console.error(`[TTS] 请求失败: ${e.message}`);
      reject(new Error(`TTS 请求失败: ${e.message}`));
    });

    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('TTS 请求超时'));
    });

    req.write(postData);
    req.end();
  });
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
  getAvailableVoices,
  voiceTypes,
  DEFAULT_VOICE,
};
