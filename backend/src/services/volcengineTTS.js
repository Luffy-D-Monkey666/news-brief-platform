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
  // 语音合成服务使用 volcano_tts 集群
  cluster: process.env.VOLC_CLUSTER || 'volcano_tts',
  // API 地址
  host: 'openspeech.bytedance.com',
  apiPath: '/api/v1/tts',
};

// 音色配置 - 与火山引擎控制台音色名称完全一致（根据用户提供的音色表）
const voiceTypes = {
  // === 通用场景 ===
  'zh_female_vv_uranus_bigtts': { name: 'vivi 2.0', description: '通用场景', lang: 'cn' },
  'zh_female_xiaohe_uranus_bigtts': { name: '小何', description: '通用场景', lang: 'cn' },
  'zh_male_m191_uranus_bigtts': { name: '云舟', description: '通用场景', lang: 'cn' },
  'zh_male_taocheng_uranus_bigtts': { name: '小天', description: '通用场景', lang: 'cn' },
  
  // === 视频配音 ===
  'zh_male_dayi_saturn_bigtts': { name: '大壹', description: '视频配音', lang: 'cn' },
  'zh_female_mizai_saturn_bigtts': { name: '黑猫侦探社咪仔', description: '视频配音', lang: 'cn' },
  'zh_female_jitangnv_saturn_bigtts': { name: '鸡汤女', description: '视频配音', lang: 'cn' },
  'zh_female_meilinvyou_saturn_bigtts': { name: '魅力女友', description: '视频配音', lang: 'cn' },
  'zh_female_santongyongns_saturn_bigtts': { name: '流畅女声', description: '视频配音', lang: 'cn' },
  'zh_male_ruyayichen_saturn_bigtts': { name: '儒雅逸辰', description: '视频配音', lang: 'cn' },
  
  // === 角色扮演 ===
  'saturn_zh_female_cancan_tob': { name: '知性灿灿', description: '角色扮演', lang: 'cn' },
  'saturn_zh_female_keainvsheng_tob': { name: '可爱女生', description: '角色扮演', lang: 'cn' },
  'saturn_zh_female_tiaopigongzhu_tob': { name: '调皮公主', description: '角色扮演', lang: 'cn' },
  'saturn_zh_male_shuanglangshaonian_tob': { name: '爽朗少年', description: '角色扮演', lang: 'cn' },
  'saturn_zh_male_tiancaitongzhuo_tob': { name: '天才同桌', description: '角色扮演', lang: 'cn' },
  
  // === 有声阅读 ===
  'zh_female_xueayi_saturn_bigtts': { name: '儿童绘本', description: '有声阅读', lang: 'cn' },
  
  // === 英文音色 ===
  'en_male_tim_uranus_bigtts': { name: 'Tim', description: '英文', lang: 'en' },
  'en_female_dacey_uranus_bigtts': { name: 'Dacey', description: '英文', lang: 'en' },
  'en_female_stokie_uranus_bigtts': { name: 'Stokie', description: '英文', lang: 'en' },
};

// 默认音色 - 使用知性灿灿（角色扮演类，适合新闻朗读）
const DEFAULT_VOICE = 'saturn_zh_female_cancan_tob';

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

  // 验证音色是否存在
  if (!voiceTypes[voiceType]) {
    console.warn(`[TTS] 未知音色 ${voiceType}，使用默认音色 ${DEFAULT_VOICE}`);
    voiceType = DEFAULT_VOICE;
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
