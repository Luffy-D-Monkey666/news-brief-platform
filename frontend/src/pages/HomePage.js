import React, { useState, useEffect, useCallback } from 'react';
import { getLatestBriefs, getHistoryBriefs } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import BriefCard from '../components/BriefCard';
import CategoryFilter from '../components/CategoryFilter';
import DonateButton from '../components/DonateButton';
import Masonry from 'react-masonry-css';
import { FaSpinner } from 'react-icons/fa';

const HomePage = () => {
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [newBriefId, setNewBriefId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const { latestBrief } = useWebSocket();

  const loadBriefs = useCallback(async (retryCount = 0) => {
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
  }, [selectedCategory]); // 依赖 selectedCategory

  // 加载初始数据
  useEffect(() => {
    loadBriefs();
  }, [loadBriefs]); // 添加 loadBriefs 依赖

  // 监听新简报
  useEffect(() => {
    let timer = null;

    if (latestBrief) {
      // 如果没有选择分类，或者新简报匹配当前分类
      if (!selectedCategory || latestBrief.category === selectedCategory) {
        setBriefs((prev) => {
          // 检查是否已存在
          const exists = prev.some((b) => b._id === latestBrief._id);
          if (!exists) {
            setNewBriefId(latestBrief._id);
            // 5秒后移除新标记，并保存timer以便清理
            timer = setTimeout(() => setNewBriefId(null), 5000);
            return [latestBrief, ...prev];
          }
          return prev;
        });
      }
    }

    // 清理函数：组件卸载或依赖变化时清除timer
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [latestBrief, selectedCategory]);

  const loadMoreBriefs = async () => {
    if (loadingMore || !hasMore) return;

    try {
      setLoadingMore(true);
      const nextPage = currentPage + 1;
      const response = await getHistoryBriefs(selectedCategory, nextPage, 20);

      if (response.data && response.data.length > 0) {
        setBriefs((prev) => [...prev, ...response.data]);
        setCurrentPage(nextPage);

        // 优先使用后端返回的分页信息
        if (response.pagination) {
          setHasMore(nextPage < response.pagination.pages);
        } else if (response.data.length < 20) {
          // 如果没有分页信息，根据返回数据量判断
          setHasMore(false);
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
            {/* 打赏按钮 */}
            <DonateButton />
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
