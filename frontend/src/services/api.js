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
export const getLatestBriefs = async (category = null, limit = 20) => {
  const params = { limit };
  if (category) {
    params.category = category;
  }
  return api.get('/briefs/latest', { params });
};

// 获取历史简报
export const getHistoryBriefs = async (category = null, page = 1, limit = 20) => {
  const params = { page, limit };
  if (category) {
    params.category = category;
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

export default api;
