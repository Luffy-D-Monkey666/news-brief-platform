import React, { useState, useEffect } from 'react';
import { getLatestBriefs } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import BriefCard from '../components/BriefCard';
import CategoryFilter from '../components/CategoryFilter';
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* 头部 */}
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                📰 实时新闻简报
              </h1>
              <p className="text-gray-600 text-sm mt-1">
                AI智能提炼 · 全网新闻聚合 · 实时推送
              </p>
            </div>

            {/* 连接状态 */}
            <div className="flex items-center space-x-2">
              <FaWifi className={isConnected ? 'text-green-500' : 'text-gray-400'} />
              <div className="flex items-center">
                <FaCircle
                  className={`text-xs mr-2 ${
                    isConnected ? 'text-green-500 animate-pulse' : 'text-gray-400'
                  }`}
                />
                <span className="text-sm font-medium text-gray-700">
                  {isConnected ? '实时连接中' : '连接断开'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* 分类筛选 */}
        <CategoryFilter
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />

        {/* 简报列表 */}
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">
            {selectedCategory ? '分类简报' : '最新简报'}
          </h2>
          <button
            onClick={loadBriefs}
            className="text-primary hover:text-blue-700 flex items-center text-sm font-medium"
          >
            <FaSpinner className="mr-2" />
            刷新
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <FaSpinner className="animate-spin text-4xl text-primary" />
            <span className="ml-4 text-gray-600">加载中...</span>
          </div>
        ) : briefs.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-500 text-lg">暂无简报</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {briefs.map((brief) => (
              <BriefCard
                key={brief._id}
                brief={brief}
                isNew={brief._id === newBriefId}
              />
            ))}
          </div>
        )}
      </main>

      {/* 底部 */}
      <footer className="bg-white shadow-lg mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
          <p>© 2024 实时新闻简报平台 · 基于开源AI模型 · Powered by Ollama</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
