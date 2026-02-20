import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { getLatestBriefs, getHistoryBriefs, getHotTopics, searchBriefs } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import { useAudioPlayer } from '../contexts/AudioPlayerContext';
import BriefCard from '../components/BriefCard';
import TopicCard from '../components/TopicCard';
import CategoryFilter from '../components/CategoryFilter';
import AudioViewCard from '../components/AudioViewCard';
import Masonry from 'react-masonry-css';
import { FaSpinner, FaTh, FaList, FaClock, FaSync, FaFolder, FaHeadphones, FaBook, FaSearch, FaTimes } from 'react-icons/fa';
import DonateButton from '../components/DonateButton';
import FloatingToolbar from '../components/FloatingToolbar';

// 时间筛选选项
const TIME_FILTERS = [
  { key: 'all', label: '全部', hours: null },
  { key: '1h', label: '1小时内', hours: 1 },
  { key: '24h', label: '今日', hours: 24 },
  { key: '7d', label: '本周', hours: 168 },
];

const HomePage = () => {
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedTimeFilter, setSelectedTimeFilter] = useState('all');
  const [viewMode, setViewMode] = useState('card'); // 'card' | 'list' | 'topics' | 'audio'
  const { setPlaylistFromBriefs } = useAudioPlayer();
  const [newBriefId, setNewBriefId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const [hotTopics, setHotTopics] = useState([]);
  const [topicsLoading, setTopicsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState(null);

  const { latestBrief } = useWebSocket();
  
  // 获取当前时间筛选的小时数
  const getHoursFromFilter = useCallback(() => {
    const filter = TIME_FILTERS.find(f => f.key === selectedTimeFilter);
    return filter?.hours || null;
  }, [selectedTimeFilter]);

  // 根据视图模式决定初始加载数量
  const getInitialLimit = useCallback(() => {
    return viewMode === 'audio' ? 10 : 50;
  }, [viewMode]);

  // 加载热门话题
  const loadTopics = async () => {
    try {
      setTopicsLoading(true);
      const result = await getHotTopics(24, 20);
      if (result.success) {
        setHotTopics(result.data || []);
      }
    } catch (error) {
      console.error('加载话题失败:', error);
    } finally {
      setTopicsLoading(false);
    }
  };

  // 搜索新闻 - 支持传入搜索词或使用当前 searchQuery
  const handleSearch = async (queryOrEvent) => {
    // 判断是事件还是直接传入的搜索词
    const isEvent = queryOrEvent?.preventDefault;
    if (isEvent) queryOrEvent.preventDefault();
    
    const query = typeof queryOrEvent === 'string' ? queryOrEvent : searchQuery;
    if (!query?.trim() || query.trim().length < 2) return;
    
    try {
      setIsSearching(true);
      const result = await searchBriefs(query.trim(), selectedCategory);
      if (result.success) {
        setSearchResults({
          query: query.trim(),
          data: result.data || [],
          total: result.pagination?.total || 0
        });
      }
    } catch (error) {
      console.error('搜索失败:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const loadBriefs = useCallback(async (retryCount = 0) => {
    try {
      setLoading(true);
      setCurrentPage(1);
      const hours = getHoursFromFilter();
      const initialLimit = getInitialLimit();
      // 使用 getHistoryBriefs 获取第一页，这样能拿到总数
      const response = await getHistoryBriefs(selectedCategory, 1, initialLimit, hours);
      const sortedData = (response.data || []).sort((a, b) => {
        const dateA = new Date(a.created_at || a.published);
        const dateB = new Date(b.created_at || b.published);
        return dateB - dateA; // 最新的在前
      });
      setBriefs(sortedData);
      // 设置真实总数
      if (response.pagination) {
        setTotalCount(response.pagination.total);
        setHasMore(1 < response.pagination.pages);
      } else {
        setTotalCount(sortedData.length);
        setHasMore(response.data && response.data.length === initialLimit);
      }
    } catch (error) {
      console.error('加载简报失败:', error);
      if (error.code === 'ECONNABORTED' && retryCount < 3) {
        console.log(`后端正在唤醒，第 ${retryCount + 1} 次重试中...`);
        setTimeout(() => loadBriefs(retryCount + 1), 3000);
      } else {
        setBriefs([]);
        setHasMore(false);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, getInitialLimit, getHoursFromFilter]);

  // 清除搜索 - 恢复当前筛选条件下的全量新闻
  const clearSearch = useCallback(() => {
    setSearchQuery('');
    setSearchResults(null);
    // 重新加载当前筛选条件的新闻
    loadBriefs();
  }, [loadBriefs]);

  // 加载初始数据
  useEffect(() => {
    loadBriefs();
    if (viewMode === 'topics') {
      loadTopics();
    }
  }, [loadBriefs, viewMode]);

  // 同步更新播放列表
  useEffect(() => {
    setPlaylistFromBriefs(briefs);
  }, [briefs, setPlaylistFromBriefs]);

  // 监听新简报
  useEffect(() => {
    if (latestBrief) {
      if (!selectedCategory || latestBrief.category === selectedCategory) {
        setBriefs((prev) => {
          const exists = prev.some((b) => b._id === latestBrief._id);
          if (!exists) {
            setNewBriefId(latestBrief._id);
            setTimeout(() => setNewBriefId(null), 5000);
            return [latestBrief, ...prev];
          }
          return prev;
        });
      }
    }
  }, [latestBrief, selectedCategory]);

  const loadMoreBriefs = async () => {
    if (loadingMore || !hasMore) return;

    try {
      setLoadingMore(true);
      const nextPage = currentPage + 1;
      const hours = getHoursFromFilter();
      // 音频视图每次加载 10 条，其他视图加载 20 条
      const loadLimit = viewMode === 'audio' ? 10 : 20;
      const response = await getHistoryBriefs(selectedCategory, nextPage, loadLimit, hours);

      if (response.data && response.data.length > 0) {
        setBriefs((prev) => [...prev, ...response.data]);
        setCurrentPage(nextPage);

        if (response.data.length < loadLimit) {
          setHasMore(false);
        }

        if (response.pagination) {
          setHasMore(nextPage < response.pagination.pages);
        }
      } else {
        setHasMore(false);
      }
    } catch (error) {
      console.error('加载更多失败:', error);
    } finally {
      setLoadingMore(false);
    }
  };

  // 分类中文名称映射
  const categoryNames = {
    ai_technology: 'AI技术',
    robotics: '机器人',
    ai_programming: 'AI编程',
    semiconductors: '芯片',
    opcg: 'OPCG',
    automotive: '汽车',
    consumer_electronics: '消费电子',
    one_piece: 'OP',
    anime: '动漫',
    tcg: 'TCG',
    // podcasts 已移除
    finance_investment: '投资财经',
    business_tech: '商业科技',
    politics_world: '政治国际',
    economy_policy: '经济政策',
    health_medical: '健康医疗',
    energy_environment: '能源环境',
    entertainment_sports: '娱乐体育',
    general: '综合'
  };

  // 分类颜色映射 - 收敛到5个主色调
  const categoryColors = {
    // 科技类 - Blue
    ai_technology: 'text-blue-600 bg-blue-50',
    robotics: 'text-blue-600 bg-blue-50',
    ai_programming: 'text-blue-600 bg-blue-50',
    semiconductors: 'text-blue-600 bg-blue-50',
    automotive: 'text-blue-600 bg-blue-50',
    consumer_electronics: 'text-blue-600 bg-blue-50',
    // 财经/商业类 - Green
    finance_investment: 'text-green-600 bg-green-50',
    business_tech: 'text-green-600 bg-green-50',
    economy_policy: 'text-green-600 bg-green-50',
    politics_world: 'text-green-600 bg-green-50',
    // 生活/健康类 - Gray
    health_medical: 'text-gray-700 bg-gray-100',
    energy_environment: 'text-gray-700 bg-gray-100',
    // 娱乐/兴趣类 - Orange
    entertainment_sports: 'text-orange-600 bg-orange-50',
    anime: 'text-orange-600 bg-orange-50',
    one_piece: 'text-orange-600 bg-orange-50',
    tcg: 'text-orange-600 bg-orange-50',
    opcg: 'text-orange-600 bg-orange-50',
    // 综合 - Gray
    general: 'text-gray-500 bg-gray-50'
  };

  // 列表视图的简报卡片
  const ListViewCard = ({ brief, isNew }) => (
    <div className={`bg-white rounded-xl p-4 mb-3 border border-gray-200 hover:shadow-md transition-all ${isNew ? 'ring-2 ring-blue-500' : ''}`}>
      <div className="flex items-start gap-4">
        {brief.image && (
          <img 
            src={brief.image} 
            alt={brief.title}
            className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
            onError={(e) => e.target.style.display = 'none'}
          />
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className={`text-xs font-medium px-2 py-0.5 rounded ${categoryColors[brief.category] || 'text-gray-500 bg-gray-50'}`}>
              {categoryNames[brief.category] || brief.category}
            </span>
            <span className="text-xs text-gray-400 flex items-center">
              <FaClock className="mr-1" />
              {new Date(brief.created_at || brief.published).toLocaleString('zh-CN')}
            </span>
          </div>
          <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{brief.title}</h3>
          <p className="text-sm text-gray-600 line-clamp-2">{brief.summary?.split('\n')[0]}</p>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-xs text-gray-400">{brief.source}</span>
            {brief.link && (
              <a 
                href={brief.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:underline"
              >
                查看原文 →
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-black shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">NewsHub</h1>
              <p className="text-gray-400 text-sm mt-1">AI驱动的全球新闻聚合平台</p>
            </div>
            <div className="flex items-center gap-3">
              <Link
                to="/knowledge"
                className="flex items-center gap-2 px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all font-medium"
              >
                <FaBook />
                知识库
              </Link>
              <DonateButton />
            </div>
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 分类筛选 */}
        <CategoryFilter
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />

        {/* 搜索框 */}
        <div className="mb-6">
          <form onSubmit={handleSearch} className="flex gap-2 max-w-xl">
            <div className="relative flex-1">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="搜索新闻标题或内容..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-10 py-2.5 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <FaTimes />
                </button>
              )}
            </div>
            <button
              type="submit"
              disabled={isSearching || searchQuery.trim().length < 2}
              className="px-4 py-2.5 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSearching ? <FaSpinner className="animate-spin" /> : '搜索'}
            </button>
          </form>
          
          {/* 搜索结果提示 */}
          {searchResults && (
            <div className="mt-3 flex items-center gap-2">
              <span className="text-sm text-gray-600">
                搜索 "<span className="font-medium text-black">{searchResults.query}</span>" 
                找到 <span className="font-medium text-black">{searchResults.total}</span> 条结果
              </span>
              <button
                onClick={clearSearch}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                清除搜索
              </button>
            </div>
          )}
        </div>

        {/* 工具栏：时间筛选 + 视图切换 */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <h2 className="text-2xl font-bold text-gray-900">
              {selectedCategory ? '分类简报' : '最新简报'}
            </h2>
            
            {/* 时间筛选器 */}
            <div className="flex items-center gap-1 bg-white rounded-lg p-1 shadow-sm border border-gray-200">
              {TIME_FILTERS.map(filter => (
                <button
                  key={filter.key}
                  onClick={() => setSelectedTimeFilter(filter.key)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                    selectedTimeFilter === filter.key
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* 视图切换 */}
            <div className="flex items-center bg-white rounded-lg p-1 shadow-sm border border-gray-200">
              <button
                onClick={() => setViewMode('card')}
                className={`p-2 rounded-md transition-all ${
                  viewMode === 'card'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="卡片视图"
              >
                <FaTh />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-md transition-all ${
                  viewMode === 'list'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="列表视图"
              >
                <FaList />
              </button>
              <button
                onClick={() => setViewMode('topics')}
                className={`p-2 rounded-md transition-all ${
                  viewMode === 'topics'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="话题视图"
              >
                <FaFolder />
              </button>
              <button
                onClick={() => setViewMode('audio')}
                className={`p-2 rounded-md transition-all ${
                  viewMode === 'audio'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="音频视图"
              >
                <FaHeadphones />
              </button>
            </div>

            {/* 刷新按钮 */}
            <button
              onClick={loadBriefs}
              className="flex items-center text-sm font-medium text-gray-700 hover:text-black transition-colors bg-white px-4 py-2 rounded-lg shadow-sm hover:shadow-md border border-gray-200"
            >
              <FaSync className="mr-2" />
              刷新
            </button>
          </div>
        </div>

        {/* 筛选结果统计 - 搜索时隐藏 */}
        {!searchResults && (
          <div className="mb-4 text-sm text-gray-500">
            找到 <span className="font-medium text-gray-900">{totalCount}</span> 条
            {selectedTimeFilter !== 'all' && TIME_FILTERS.find(f => f.key === selectedTimeFilter)?.label}
            新闻
            {briefs.length < totalCount && (
              <span className="text-gray-400">（已加载 {briefs.length} 条）</span>
            )}
          </div>
        )}

        {viewMode === 'topics' ? (
          // 话题视图
          topicsLoading ? (
            <div className="flex items-center justify-center py-32">
              <FaSpinner className="animate-spin text-5xl text-black" />
              <span className="ml-4 text-gray-600 text-lg">加载话题中...</span>
            </div>
          ) : hotTopics.length === 0 ? (
            <div className="text-center py-32 bg-white rounded-2xl">
              <p className="text-gray-500 text-xl">暂无热门话题</p>
              <p className="text-gray-400 text-sm mt-2">
                话题需要同一事件有2篇以上报道才会形成
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {hotTopics.map((topic) => (
                <TopicCard key={topic._id} topic={topic} />
              ))}
            </div>
          )
        ) : searchResults ? (
          // 搜索结果视图 - 根据当前视图模式渲染
          searchResults.data.length === 0 ? (
            <div className="text-center py-32 bg-white rounded-2xl">
              <p className="text-gray-500 text-xl">未找到相关新闻</p>
              <p className="text-gray-400 text-sm mt-2">
                试试其他关键词
              </p>
            </div>
          ) : viewMode === 'card' ? (
            <Masonry
              breakpointCols={{ default: 4, 1536: 4, 1280: 3, 1024: 3, 768: 2, 640: 1 }}
              className="masonry-grid"
              columnClassName="masonry-grid_column"
            >
              {searchResults.data.map((brief) => (
                <BriefCard key={brief._id} brief={brief} />
              ))}
            </Masonry>
          ) : viewMode === 'audio' ? (
            <div className="space-y-3 max-w-3xl mx-auto">
              {searchResults.data.map((brief, index) => (
                <AudioViewCard key={brief._id} brief={brief} index={index} />
              ))}
            </div>
          ) : (
            <div className="space-y-0">
              {searchResults.data.map((brief) => (
                <ListViewCard key={brief._id} brief={brief} />
              ))}
            </div>
          )
        ) : loading ? (
          <div className="flex items-center justify-center py-32">
            <FaSpinner className="animate-spin text-5xl text-black" />
            <span className="ml-4 text-gray-600 text-lg">加载中...</span>
          </div>
        ) : briefs.length === 0 ? (
          <div className="text-center py-32 bg-white rounded-2xl">
            <p className="text-gray-500 text-xl">暂无简报</p>
            <p className="text-gray-400 text-sm mt-2">
              {selectedTimeFilter !== 'all' 
                ? '该时间段内暂无新闻，试试其他时间范围' 
                : '尝试刷新或选择其他分类'}
            </p>
          </div>
        ) : viewMode === 'card' ? (
          // 卡片视图（瀑布流）
          <Masonry
            breakpointCols={{
              default: 4,
              1536: 4,
              1280: 3,
              1024: 3,
              768: 2,
              640: 1
            }}
            className="masonry-grid"
            columnClassName="masonry-grid_column"
          >
            {briefs.map((brief) => (
              <BriefCard
                key={brief._id}
                brief={brief}
                isNew={brief._id === newBriefId}
              />
            ))}
          </Masonry>
        ) : viewMode === 'audio' ? (
          // 音频视图
          <div className="space-y-3 max-w-3xl mx-auto">
            <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-4 mb-6 text-white">
              <div className="flex items-center gap-3">
                <FaHeadphones className="text-2xl" />
                <div>
                  <h3 className="font-semibold">音频模式</h3>
                  <p className="text-sm text-gray-300">
                    点击播放按钮收听单条新闻，或使用底部播放栏连续播放
                  </p>
                </div>
              </div>
            </div>
            {briefs.map((brief, index) => (
              <AudioViewCard
                key={brief._id}
                brief={brief}
                index={index}
                isNew={brief._id === newBriefId}
              />
            ))}
          </div>
        ) : (
          // 列表视图
          <div className="space-y-0">
            {briefs.map((brief) => (
              <ListViewCard
                key={brief._id}
                brief={brief}
                isNew={brief._id === newBriefId}
              />
            ))}
          </div>
        )}

        {/* 加载更多按钮 */}
        {!loading && briefs.length > 0 && viewMode !== 'topics' && (
          <div className="mt-8 flex justify-center">
            {hasMore ? (
              <button
                onClick={loadMoreBriefs}
                disabled={loadingMore}
                className={`
                  px-8 py-3 rounded-xl font-medium text-sm
                  transition-all duration-200 shadow-sm hover:shadow-md
                  ${loadingMore
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-900 hover:bg-gray-50 border border-gray-200'
                  }
                `}
              >
                {loadingMore ? '加载中...' : '加载更多'}
              </button>
            ) : (
              <div className="text-center py-4">
                <p className="text-gray-400 text-sm">没有更多了</p>
                <p className="text-gray-300 text-xs mt-1">
                  共 {briefs.length} 条新闻简报
                </p>
              </div>
            )}
          </div>
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

      {/* 浮动工具栏 */}
      <FloatingToolbar
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onSearch={handleSearch}
        isSearching={isSearching}
        viewMode={viewMode}
        setViewMode={setViewMode}
        onRefresh={loadBriefs}
        clearSearch={clearSearch}
      />
    </div>
  );
};

export default HomePage;
