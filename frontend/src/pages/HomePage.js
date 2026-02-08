import React, { useState, useEffect, useCallback, useRef } from 'react';
import { getLatestBriefs, getHistoryBriefs, searchBriefs } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import BriefCard from '../components/BriefCard';
import CategoryFilter from '../components/CategoryFilter';
import DonateButton from '../components/DonateButton';
import Masonry from 'react-masonry-css';
import { FaSpinner, FaSearch, FaTimes } from 'react-icons/fa';

const HomePage = () => {
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [newBriefId, setNewBriefId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  // 搜索相关状态
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const searchTimerRef = useRef(null);

  // 无限滚动 sentinel ref
  const sentinelRef = useRef(null);

  const { latestBrief } = useWebSocket();

  const loadBriefs = useCallback(async (retryCount = 0) => {
    try {
      setLoading(true);
      setCurrentPage(1);
      const response = await getLatestBriefs(selectedCategory, 100);
      setBriefs(response.data || []);
      setHasMore(response.data && response.data.length === 100);
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
  }, [selectedCategory]);

  // 加载初始数据
  useEffect(() => {
    setSearchQuery('');
    loadBriefs();
  }, [loadBriefs]);

  // 监听新简报
  useEffect(() => {
    let timer = null;

    if (latestBrief && !searchQuery) {
      if (!selectedCategory || latestBrief.category === selectedCategory) {
        setBriefs((prev) => {
          const exists = prev.some((b) => b._id === latestBrief._id);
          if (!exists) {
            setNewBriefId(latestBrief._id);
            timer = setTimeout(() => setNewBriefId(null), 5000);
            return [latestBrief, ...prev];
          }
          return prev;
        });
      }
    }

    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [latestBrief, selectedCategory, searchQuery]);

  const loadMoreBriefs = useCallback(async () => {
    if (loadingMore || !hasMore || searchQuery) return;

    try {
      setLoadingMore(true);
      const nextPage = currentPage + 1;
      const response = await getHistoryBriefs(selectedCategory, nextPage, 20);

      if (response.data && response.data.length > 0) {
        setBriefs((prev) => [...prev, ...response.data]);
        setCurrentPage(nextPage);

        if (response.pagination) {
          setHasMore(nextPage < response.pagination.pages);
        } else if (response.data.length < 20) {
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
  }, [loadingMore, hasMore, currentPage, selectedCategory, searchQuery]);

  // 无限滚动 - IntersectionObserver
  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !loading) {
          loadMoreBriefs();
        }
      },
      { rootMargin: '200px' }
    );

    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [loadMoreBriefs, loading]);

  // 搜索处理（防抖）
  const handleSearchChange = (e) => {
    const query = e.target.value;
    setSearchQuery(query);

    if (searchTimerRef.current) {
      clearTimeout(searchTimerRef.current);
    }

    if (!query.trim()) {
      loadBriefs();
      return;
    }

    searchTimerRef.current = setTimeout(async () => {
      try {
        setIsSearching(true);
        setLoading(true);
        const response = await searchBriefs(query, selectedCategory);
        setBriefs(response.data || []);
        setHasMore(false);
      } catch (error) {
        console.error('搜索失败:', error);
      } finally {
        setIsSearching(false);
        setLoading(false);
      }
    }, 500);
  };

  const clearSearch = () => {
    setSearchQuery('');
    loadBriefs();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 */}
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

        {/* 搜索框 + 标题栏 */}
        <div className="mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <h2 className="text-2xl font-bold text-gray-900">
            {searchQuery ? '搜索结果' : selectedCategory ? '分类简报' : '最新简报'}
          </h2>

          <div className="flex items-center gap-3">
            {/* 搜索框 */}
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm" />
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearchChange}
                placeholder="搜索新闻..."
                className="search-input pl-9 pr-8 py-2 w-48 sm:w-64 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:border-gray-400 transition-all"
              />
              {searchQuery && (
                <button
                  onClick={clearSearch}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <FaTimes className="text-xs" />
                </button>
              )}
            </div>

            {/* 刷新按钮 */}
            <button
              onClick={() => { setSearchQuery(''); loadBriefs(); }}
              className="flex items-center text-sm font-medium text-gray-700 hover:text-black transition-colors bg-white px-4 py-2 rounded-lg shadow-sm hover:shadow-md"
            >
              <FaSpinner className="mr-2" />
              刷新
            </button>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-32">
            <FaSpinner className="animate-spin text-5xl text-black" />
            <span className="ml-4 text-gray-600 text-lg">
              {isSearching ? '搜索中...' : '加载中...'}
            </span>
          </div>
        ) : briefs.length === 0 ? (
          <div className="text-center py-32 bg-white rounded-2xl">
            <p className="text-gray-500 text-xl">
              {searchQuery ? '没有找到相关新闻' : '暂无简报'}
            </p>
            <p className="text-gray-400 text-sm mt-2">
              {searchQuery ? '换个关键词试试' : '尝试刷新或选择其他分类'}
            </p>
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

        {/* 无限滚动 sentinel */}
        {!loading && briefs.length > 0 && !searchQuery && (
          <div ref={sentinelRef} className="mt-4 flex justify-center py-8">
            {loadingMore ? (
              <div className="flex items-center text-gray-400">
                <FaSpinner className="animate-spin mr-2" />
                <span className="text-sm">加载更多...</span>
              </div>
            ) : hasMore ? (
              <div className="text-gray-300 text-sm">向下滚动加载更多</div>
            ) : (
              <div className="text-center">
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
            © 2024 NewsHub · AI驱动的新闻聚合平台 · Powered by DeepSeek
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
