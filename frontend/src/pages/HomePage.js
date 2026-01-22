import React, { useState, useEffect } from 'react';
import { getLatestBriefs } from '../services/api';
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

  const loadBriefs = async () => {
    try {
      setLoading(true);
      const response = await getLatestBriefs(selectedCategory, 50);
      setBriefs(response.data || []);
    } catch (error) {
      console.error('加载简报失败:', error);
    } finally {
      setLoading(false);
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
