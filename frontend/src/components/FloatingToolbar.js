import React, { useState, useEffect } from 'react';
import { FaArrowUp, FaSearch, FaFilter, FaTimes } from 'react-icons/fa';

const FloatingToolbar = ({ 
  searchQuery, 
  setSearchQuery, 
  onSearch, 
  isSearching,
  selectedTimeFilter,
  setSelectedTimeFilter,
  timeFilters,
  onRefresh 
}) => {
  const [showBackToTop, setShowBackToTop] = useState(false);
  const [showToolbar, setShowToolbar] = useState(false);
  const [localSearchQuery, setLocalSearchQuery] = useState(searchQuery);

  // 监听滚动
  useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 500);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // 同步搜索词
  useEffect(() => {
    setLocalSearchQuery(searchQuery);
  }, [searchQuery]);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchQuery(localSearchQuery);
    onSearch(e);
    setShowToolbar(false);
  };

  return (
    <>
      {/* 浮动按钮组 - 右下角 */}
      <div className="fixed bottom-24 right-6 flex flex-col gap-3 z-40">
        {/* 工具栏切换按钮 */}
        <button
          onClick={() => setShowToolbar(!showToolbar)}
          className={`w-12 h-12 rounded-full shadow-lg flex items-center justify-center transition-all ${
            showToolbar 
              ? 'bg-black text-white' 
              : 'bg-white text-gray-700 hover:bg-gray-100'
          }`}
          title="快捷工具"
        >
          {showToolbar ? <FaTimes /> : <FaFilter />}
        </button>

        {/* 回到顶部按钮 */}
        {showBackToTop && (
          <button
            onClick={scrollToTop}
            className="w-12 h-12 bg-black text-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-800 transition-all animate-fade-in"
            title="回到顶部"
          >
            <FaArrowUp />
          </button>
        )}
      </div>

      {/* 浮动工具栏 */}
      {showToolbar && (
        <div className="fixed bottom-40 right-6 bg-white rounded-2xl shadow-2xl p-4 z-50 w-80 border border-gray-200 animate-slide-up">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-gray-800">快捷工具</h3>
            <button 
              onClick={() => setShowToolbar(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <FaTimes />
            </button>
          </div>

          {/* 搜索 */}
          <form onSubmit={handleSearchSubmit} className="mb-4">
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm" />
              <input
                type="text"
                placeholder="搜索新闻..."
                value={localSearchQuery}
                onChange={(e) => setLocalSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
              />
            </div>
            <button
              type="submit"
              disabled={isSearching || localSearchQuery.trim().length < 2}
              className="w-full mt-2 py-2 bg-black text-white text-sm rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              搜索
            </button>
          </form>

          {/* 时间筛选 */}
          <div>
            <p className="text-xs text-gray-500 mb-2">时间筛选</p>
            <div className="flex flex-wrap gap-1">
              {timeFilters.map((filter) => (
                <button
                  key={filter.key}
                  onClick={() => {
                    setSelectedTimeFilter(filter.key);
                    setShowToolbar(false);
                  }}
                  className={`px-3 py-1.5 text-xs rounded-md transition-all ${
                    selectedTimeFilter === filter.key
                      ? 'bg-black text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          {/* 刷新按钮 */}
          <button
            onClick={() => {
              onRefresh();
              setShowToolbar(false);
            }}
            className="w-full mt-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg hover:bg-gray-200 transition-colors"
          >
            刷新新闻
          </button>
        </div>
      )}

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slide-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.2s ease-out;
        }
        .animate-slide-up {
          animation: slide-up 0.2s ease-out;
        }
      `}</style>
    </>
  );
};

export default FloatingToolbar;
