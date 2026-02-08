import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 简单的内存缓存
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5分钟

const getCached = (key) => {
  const item = cache.get(key);
  if (item && Date.now() - item.ts < CACHE_TTL) {
    return item.data;
  }
  cache.delete(key);
  return null;
};

const setCache = (key, data) => {
  if (cache.size > 50) {
    const firstKey = cache.keys().next().value;
    cache.delete(firstKey);
  }
  cache.set(key, { data, ts: Date.now() });
};

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API错误:', error);
    return Promise.reject(error);
  }
);

// 获取最新简报（带缓存）
export const getLatestBriefs = async (category = null, limit = 20) => {
  const params = { limit };
  if (category) {
    params.category = category;
  }

  const cacheKey = `latest_${category || 'all'}_${limit}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const data = await api.get('/briefs/latest', { params });
  setCache(cacheKey, data);
  return data;
};

// 获取历史简报
export const getHistoryBriefs = async (category = null, page = 1, limit = 20) => {
  const params = { page, limit };
  if (category) {
    params.category = category;
  }
  return api.get('/briefs/history', { params });
};

// 搜索简报
export const searchBriefs = async (query, category = null) => {
  const params = { q: query };
  if (category) {
    params.category = category;
  }
  return api.get('/briefs/search', { params });
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
