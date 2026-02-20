import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { getEntities } from '../services/api';
import { FaSpinner, FaSearch, FaBuilding, FaUser, FaLightbulb, FaCalendarAlt, FaNewspaper, FaArrowLeft } from 'react-icons/fa';

// 实体类型配置
const TYPE_CONFIG = {
  company: { icon: FaBuilding, label: '公司', color: 'bg-blue-100 text-blue-700' },
  person: { icon: FaUser, label: '人物', color: 'bg-purple-100 text-purple-700' },
  concept: { icon: FaLightbulb, label: '概念', color: 'bg-amber-100 text-amber-700' },
  event: { icon: FaCalendarAlt, label: '事件', color: 'bg-green-100 text-green-700' },
  product: { icon: FaNewspaper, label: '产品', color: 'bg-cyan-100 text-cyan-700' }
};

// 实体卡片组件
const EntityCard = ({ entity, onClick }) => {
  const config = TYPE_CONFIG[entity.type] || TYPE_CONFIG.concept;
  const Icon = config.icon;
  
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-lg hover:border-gray-300 transition-all cursor-pointer group"
    >
      <div className="flex items-start gap-4">
        {/* 图标 */}
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${config.color} group-hover:scale-105 transition-transform`}>
          <Icon className="text-xl" />
        </div>
        
        {/* 内容 */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-semibold text-gray-900 truncate">{entity.name}</h3>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          </div>
          
          {entity.description && (
            <p className="text-sm text-gray-500 line-clamp-2 mb-2">
              {entity.description}
            </p>
          )}
          
          <div className="flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <FaNewspaper />
              {entity.news_count || 0} 条新闻
            </span>
            {entity.last_news_at && (
              <span>
                最近更新: {new Date(entity.last_news_at).toLocaleDateString('zh-CN')}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const KnowledgePage = () => {
  const navigate = useNavigate();
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState(null);
  const [sortBy, setSortBy] = useState('news'); // news | recent | name
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 30;

  // 加载实体（首次或刷新）
  const loadEntities = useCallback(async () => {
    try {
      setLoading(true);
      const params = {
        sort: sortBy,
        limit: PAGE_SIZE,
        offset: 0
      };
      if (selectedType) params.type = selectedType;
      if (searchQuery) params.search = searchQuery;
      
      const response = await getEntities(params);
      const newData = response.data || [];
      
      setEntities(newData);
      setPage(1);
      setHasMore(newData.length === PAGE_SIZE);
    } catch (error) {
      console.error('加载实体失败:', error);
      setEntities([]);
    } finally {
      setLoading(false);
    }
  }, [selectedType, sortBy, searchQuery]);

  // 加载更多
  const handleLoadMore = async () => {
    if (loadingMore || !hasMore) return;
    
    try {
      setLoadingMore(true);
      const nextPage = page + 1;
      const params = {
        sort: sortBy,
        limit: PAGE_SIZE,
        offset: (nextPage - 1) * PAGE_SIZE
      };
      if (selectedType) params.type = selectedType;
      if (searchQuery) params.search = searchQuery;
      
      const response = await getEntities(params);
      const newData = response.data || [];
      
      setEntities(prev => [...prev, ...newData]);
      setPage(nextPage);
      setHasMore(newData.length === PAGE_SIZE);
    } catch (error) {
      console.error('加载更多失败:', error);
    } finally {
      setLoadingMore(false);
    }
  };

  // 筛选/排序变化时重新加载
  useEffect(() => {
    loadEntities();
  }, [loadEntities]);

  // 搜索防抖
  useEffect(() => {
    const timer = setTimeout(() => {
      loadEntities();
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-black shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <FaArrowLeft className="text-xl" />
              </button>
              <div>
                <h1 className="text-3xl font-bold text-white">知识库</h1>
                <p className="text-gray-400 text-sm mt-1">实体档案与时间轴追踪</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 搜索和筛选栏 */}
        <div className="mb-6 flex flex-wrap items-center gap-4">
          {/* 搜索框 */}
          <div className="relative flex-1 min-w-64">
            <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="搜索实体..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-11 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all"
            />
          </div>

          {/* 类型筛选 */}
          <div className="flex items-center gap-1 bg-white rounded-lg p-1 shadow-sm border border-gray-200">
            <button
              onClick={() => setSelectedType(null)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                !selectedType
                  ? 'bg-gray-900 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              全部
            </button>
            {Object.entries(TYPE_CONFIG).map(([key, config]) => (
              <button
                key={key}
                onClick={() => setSelectedType(key)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                  selectedType === key
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                {config.label}
              </button>
            ))}
          </div>

          {/* 排序 */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
          >
            <option value="news">按新闻数</option>
            <option value="recent">按最近更新</option>
            <option value="name">按名称</option>
          </select>
        </div>

        {/* 实体列表 */}
        {loading ? (
          <div className="flex items-center justify-center py-32">
            <FaSpinner className="animate-spin text-5xl text-black" />
            <span className="ml-4 text-gray-600 text-lg">加载中...</span>
          </div>
        ) : entities.length === 0 ? (
          <div className="text-center py-32 bg-white rounded-2xl">
            <FaLightbulb className="mx-auto text-6xl text-gray-300 mb-4" />
            <p className="text-gray-500 text-xl">暂无实体数据</p>
            <p className="text-gray-400 text-sm mt-2">
              当新闻被处理时，相关实体会自动添加到知识库
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {entities.map((entity) => (
                <EntityCard
                  key={entity._id}
                  entity={entity}
                  onClick={() => navigate(`/entity/${entity._id}`)}
                />
              ))}
            </div>
            
            {/* 加载更多按钮 */}
            {hasMore && (
              <div className="flex justify-center mt-8">
                <button
                  onClick={handleLoadMore}
                  disabled={loadingMore}
                  className="px-6 py-3 bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {loadingMore ? (
                    <>
                      <FaSpinner className="animate-spin" />
                      加载中...
                    </>
                  ) : (
                    '加载更多'
                  )}
                </button>
              </div>
            )}
            
            {/* 显示数量 */}
            <div className="text-center mt-4 text-sm text-gray-500">
              已显示 {entities.length} 个实体
            </div>
          </>
        )}
      </main>

      {/* 底部 */}
      <footer className="bg-black mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 NewsHub · AI驱动的新闻聚合平台 · Powered by DeepSeek
          </p>
        </div>
      </footer>
    </div>
  );
};

export default KnowledgePage;
