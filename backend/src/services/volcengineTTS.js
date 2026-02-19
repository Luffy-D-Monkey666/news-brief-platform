/**
 * 火山引擎 TTS 服务
 * 使用豆包语音合成大模型，提供高质量中文语音合成
 * 
 * 官方文档：https://www.volcengine.com/docs/6561/79820
 */

const https = require('https');

// 配置 - 从环境变量读取
const config = {
  appId: process.env.VOLC_APP_ID || '6922135515',
  accessToken: process.env.VOLC_ACCESS_TOKEN,
  // 语音合成大模型使用 volcano_mega 集群
  cluster: process.env.VOLC_CLUSTER || 'volcano_mega',
  // API 地址
  host: 'openspeech.bytedance.com',
  apiPath: '/api/v1/tts',
};

// 音色配置 - 语音合成大模型音色（从控制台截图获取）
const voiceTypes = {
  // 趣味方言
  'zh_female_wanqudashu_moon_bigtts': { name: '湾区大叔', description: '趣味方言' },
  'zh_female_daimengchuanmei_moon_bigtts': { name: '呆萌川妹', description: '趣味方言' },
  'zh_male_guozhoudege_moon_bigtts': { name: '广州德哥', description: '趣味方言' },
  'zh_male_beijingxiaoye_moon_bigtts': { name: '北京小爷', description: '趣味方言' },
  // 通用场景
  'zh_male_shaonianzixin_moon_bigtts': { name: '少年梓昕/Brayan', description: '通用场景，中/英' },
  // 角色扮演
  'zh_female_meilinvyou_moon_bigtts': { name: '魅力女友', description: '角色扮演' },
  'zh_male_shenyeboke_moon_bigtts': { name: '深夜播客', description: '角色扮演' },
  'zh_female_sajiaonvyou_moon_bigtts': { name: '柔美女友', description: '角色扮演' },
  'zh_female_yuanqinvyou_moon_bigtts': { name: '撒娇学妹', description: '角色扮演' },
  'zh_male_haoyuxiaoge_moon_bigtts': { name: '浩宇小哥', description: '趣味方言' },
};

// 默认音色 - 使用通用场景的少年梓昕
const DEFAULT_VOICE = 'zh_male_shaonianzixin_moon_bigtts';

/**
 * 调用火山引擎 TTS API（HTTP 一次性合成）
 * @param {string} text - 要合成的文本（最大1024字节）
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

  // 构建请求体（严格按照官方文档）
  const requestBody = {
    app: {
      appid: config.appId,
      token: 'access_token',  // Bearer Token 认证时可传任意非空值
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
      operation: 'query',  // HTTP 只能用 query（非流式）
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
        // 官方文档：Bearer和token使用分号分隔
        'Authorization': `Bearer;${config.accessToken}`,
      },
    };

    console.log(`[TTS] 请求参数: appId=${config.appId}, cluster=${config.cluster}, voice=${voiceType}, text_len=${text.length}`);

    const req = https.request(reqOptions, (res) => {
      const chunks = [];
      
      res.on('data', (chunk) => {
        chunks.push(chunk);
      });
      
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        const bodyStr = body.toString();
        
        try {
          const response = JSON.parse(bodyStr);
          
          console.log(`[TTS] 响应: code=${response.code}, message=${response.message}`);
          
          // 成功码是 3000
          if (response.code !== 3000) {
            console.error(`[TTS] API 错误详情:`, JSON.stringify(response, null, 2));
            reject(new Error(`TTS 合成失败: ${response.message || `错误码 ${response.code}`}`));
            return;
          }
          
          // 返回 base64 解码的音频数据
          if (response.data) {
            const audioBuffer = Buffer.from(response.data, 'base64');
            console.log(`[TTS] 合成成功: ${audioBuffer.length} bytes, duration=${response.addition?.duration || 'unknown'}ms`);
            resolve(audioBuffer);
          } else {
            reject(new Error('TTS 响应中没有音频数据'));
          }
        } catch (e) {
          console.error(`[TTS] 解析响应失败: ${e.message}`);
          console.error(`[TTS] 原始响应 (前500字符): ${bodyStr.substring(0, 500)}`);
          reject(new Error(`解析 TTS 响应失败: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      console.error(`[TTS] 网络请求失败: ${e.message}`);
      reject(new Error(`TTS 请求失败: ${e.message}`));
    });

    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('TTS 请求超时 (30s)'));
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
