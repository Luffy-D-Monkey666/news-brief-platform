import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 30000, // 增加到30秒，避免Render休眠唤醒时超时
  headers: {
    'Content-Type': 'application/json'
  }
});

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API错误:', error);
    return Promise.reject(error);
  }
);

// 获取最新简报
export const getLatestBriefs = async (category = null, limit = 20, hours = null) => {
  const params = { limit };
  if (category) {
    params.category = category;
  }
  if (hours) {
    params.hours = hours;
  }
  return api.get('/briefs/latest', { params });
};

// 获取历史简报
export const getHistoryBriefs = async (category = null, page = 1, limit = 20, hours = null) => {
  const params = { page, limit };
  if (category) {
    params.category = category;
  }
  if (hours) {
    params.hours = hours;
  }
  return api.get('/briefs/history', { params });
};

// 获取分类统计
export const getCategoryStats = async () => {
  return api.get('/briefs/stats');
};

// 获取简报详情
export const getBriefById = async (id) => {
  return api.get(`/briefs/${id}`);
};

// 搜索新闻
export const searchBriefs = async (query, category = null, page = 1, limit = 50) => {
  const params = { q: query, page, limit };
  if (category) params.category = category;
  return api.get('/briefs/search', { params });
};

// 获取热门话题
export const getHotTopics = async (hours = 24, limit = 10) => {
  return api.get('/topics/hot', { params: { hours, limit } });
};

// 获取话题详情及相关新闻
export const getTopicDetail = async (topicId, limit = 20) => {
  return api.get(`/topics/${topicId}`, { params: { limit } });
};

// 获取所有话题
export const getTopics = async (category = null, limit = 50) => {
  const params = { limit };
  if (category) {
    params.category = category;
  }
  return api.get('/topics', { params });
};

// ==================== TTS 相关 API ====================

// 获取可用音色列表
export const getTTSVoices = async () => {
  return api.get('/tts/voices');
};

// 默认音色（与后端保持一致）
const DEFAULT_VOICE = 'BV700_V2_streaming';

// 合成语音（返回音频 URL）
export const synthesizeSpeech = async (text, voice = DEFAULT_VOICE, options = {}) => {
  const response = await fetch(`${API_URL}/api/tts/synthesize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      voice,
      ...options,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || '语音合成失败');
  }
  
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

// 获取简报语音 URL
export const getBriefAudioUrl = (briefId, voice = DEFAULT_VOICE) => {
  return `${API_URL}/api/tts/brief/${briefId}?voice=${voice}`;
};

// ==================== 实体知识库 API ====================

// 获取实体列表
export const getEntities = async (params = {}) => {
  return api.get('/entities', { params });
};

// 获取实体详情
export const getEntityById = async (id) => {
  return api.get(`/entities/${id}`);
};

// 获取实体时间轴（含关联新闻）
export const getEntityTimeline = async (id, limit = 50, before = null) => {
  const params = { limit };
  if (before) params.before = before;
  return api.get(`/entities/${id}/timeline`, { params });
};

// 按名称搜索实体
export const searchEntityByName = async (name) => {
  return api.get(`/entities/search/${encodeURIComponent(name)}`);
};

export default api;
