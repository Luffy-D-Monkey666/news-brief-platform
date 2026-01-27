import React, { useState, useEffect } from 'react';
import { getLatestBriefs, getHistoryBriefs } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import BriefCard from '../components/BriefCard';
import CategoryFilter from '../components/CategoryFilter';
import Masonry from 'react-masonry-css';
import { FaWifi, FaCircle, FaSpinner } from 'react-icons/fa';

const HomePage = () => {
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [newBriefId, setNewBriefId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const { isConnected, latestBrief } = useWebSocket();

  // 加载初始数据
  useEffect(() => {
    loadBriefs();
  }, [selectedCategory]);

  // 监听新简报
  useEffect(() => {
    if (latestBrief) {
      // 如果没有选择分类，或者新简报匹配当前分类
      if (!selectedCategory || latestBrief.category === selectedCategory) {
        setBriefs((prev) => {
          // 检查是否已存在
          const exists = prev.some((b) => b._id === latestBrief._id);
          if (!exists) {
            setNewBriefId(latestBrief._id);
            setTimeout(() => setNewBriefId(null), 5000); // 5秒后移除新标记
            return [latestBrief, ...prev];
          }
          return prev;
        });
      }
    }
  }, [latestBrief, selectedCategory]);

  const loadBriefs = async (retryCount = 0) => {
    try {
      setLoading(true);
      setCurrentPage(1);  // 重置页码
      const response = await getLatestBriefs(selectedCategory, 50);
      setBriefs(response.data || []);
      setHasMore(response.data && response.data.length === 50);  // 判断是否有更多
    } catch (error) {
      console.error('加载简报失败:', error);
      // 如果是超时错误（通常是后端正在从休眠中唤醒），自动重试
      if (error.code === 'ECONNABORTED' && retryCount < 3) {
        console.log(`后端正在唤醒，第 ${retryCount + 1} 次重试中...`);
        setTimeout(() => loadBriefs(retryCount + 1), 3000); // 3秒后重试
      } else {
        // 其他错误或重试次数耗尽，显示空数据
        setBriefs([]);
        setHasMore(false);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadMoreBriefs = async () => {
    if (loadingMore || !hasMore) return;

    try {
      setLoadingMore(true);
      const nextPage = currentPage + 1;
      const response = await getHistoryBriefs(selectedCategory, nextPage, 20);

      if (response.data && response.data.length > 0) {
        setBriefs((prev) => [...prev, ...response.data]);
        setCurrentPage(nextPage);

        if (response.data.length < 20) {
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 - Netflix风格 */}
      <header className="bg-black shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">
                NewsHub
              </h1>
              <p className="text-gray-400 text-sm mt-1">
                AI驱动的全球新闻聚合平台
              </p>
            </div>

            {/* 连接状态 */}
            <div className="flex items-center space-x-3 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full">
              <FaWifi className={isConnected ? 'text-green-400' : 'text-gray-500'} />
              <div className="flex items-center">
                <FaCircle
                  className={`text-xs mr-2 ${
                    isConnected ? 'text-green-400 animate-pulse' : 'text-gray-500'
                  }`}
                />
                <span className="text-sm font-medium text-white">
                  {isConnected ? '实时连接' : '连接断开'}
                </span>
              </div>
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

        {/* 简报列表标题 */}
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {selectedCategory ? '分类简报' : '最新简报'}
          </h2>
          <button
            onClick={loadBriefs}
            className="flex items-center text-sm font-medium text-gray-700 hover:text-black transition-colors bg-white px-4 py-2 rounded-lg shadow-sm hover:shadow-md"
          >
            <FaSpinner className="mr-2" />
            刷新
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-32">
            <FaSpinner className="animate-spin text-5xl text-black" />
            <span className="ml-4 text-gray-600 text-lg">加载中...</span>
          </div>
        ) : briefs.length === 0 ? (
          <div className="text-center py-32 bg-white rounded-2xl">
            <p className="text-gray-500 text-xl">暂无简报</p>
            <p className="text-gray-400 text-sm mt-2">尝试刷新或选择其他分类</p>
          </div>
        ) : (
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
        )}

        {/* 加载更多按钮 */}
        {!loading && briefs.length > 0 && (
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
                <p className="text-gray-400 text-sm">已经到底了</p>
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
            © 2024 NewsHub · AI驱动的新闻聚合平台 · Powered by OpenAI
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
