import React, { useState, useEffect } from 'react';
import { FaArrowUp, FaSearch, FaFilter, FaTimes, FaTh, FaList, FaFolder, FaHeadphones } from 'react-icons/fa';

// 重要性筛选选项
const IMPORTANCE_FILTERS = [
  { key: 'all', label: '全部', value: null },
  { key: 'breaking', label: '突发', value: 'breaking' },
  { key: 'high', label: '重要', value: 'high' },
  { key: 'normal', label: '普通', value: 'normal' },
];

const FloatingToolbar = ({ 
  searchQuery, 
  setSearchQuery, 
  onSearch, 
  isSearching,
  viewMode,
  setViewMode,
  onRefresh,
  clearSearch,
  selectedImportance,
  setSelectedImportance
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

  // 滚动到搜索栏位置（分类区域下方，搜索框紧贴 header）
  const scrollToToolbar = () => {
    // 查找搜索框容器（包含 "搜索新闻标题或内容..." 的 div）
    const searchContainer = document.querySelector('main > div:nth-child(2)');
    const header = document.querySelector('header');
    const headerHeight = header ? header.offsetHeight : 0;
    
    if (searchContainer) {
      // 滚动到搜索框位置，让它紧贴 header 下方
      const targetPosition = searchContainer.offsetTop - headerHeight - 10;
      window.scrollTo({ top: Math.max(0, targetPosition), behavior: 'smooth' });
    } else {
      // 备用：通过 form 元素定位
      const searchForm = document.querySelector('main form');
      if (searchForm) {
        const targetPosition = searchForm.offsetTop - headerHeight - 20;
        window.scrollTo({ top: Math.max(0, targetPosition), behavior: 'smooth' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  };

  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    if (localSearchQuery.trim().length < 2) return;
    // 先更新搜索词，再执行搜索
    setSearchQuery(localSearchQuery);
    setShowToolbar(false);
    // 直接调用搜索，传入搜索词
    await onSearch(localSearchQuery.trim());
    // 搜索后滚动到新闻列表
    setTimeout(scrollToToolbar, 300);
  };

  const handleRefresh = () => {
    onRefresh();
    setShowToolbar(false);
    // 刷新后滚动到新闻列表
    setTimeout(scrollToToolbar, 300);
  };

  const handleViewChange = (mode) => {
    setViewMode(mode);
    setShowToolbar(false);
    // 视图切换后滚动到新闻列表
    setTimeout(scrollToToolbar, 100);
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

          {/* 重要性筛选 */}
          <div className="mb-4">
            <p className="text-xs text-gray-500 mb-2">重要性筛选</p>
            <div className="grid grid-cols-4 gap-1">
              {IMPORTANCE_FILTERS.map(filter => (
                <button
                  key={filter.key}
                  onClick={() => {
                    setSelectedImportance(filter.key);
                    setShowToolbar(false);
                    setTimeout(scrollToToolbar, 100);
                  }}
                  className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all text-[10px] ${
                    selectedImportance === filter.key 
                      ? filter.key === 'breaking'
                        ? 'bg-red-600 text-white'
                        : filter.key === 'high'
                          ? 'bg-orange-500 text-white'
                          : 'bg-black text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {filter.key === 'breaking' && '🔴'}
                  {filter.key === 'high' && '🟡'}
                  {filter.key === 'all' && '📰'}
                  {filter.key === 'normal' && '⚪'}
                  <span>{filter.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* 视图切换 */}
          <div>
            <p className="text-xs text-gray-500 mb-2">视图切换</p>
            <div className="grid grid-cols-4 gap-1">
              <button
                onClick={() => handleViewChange('card')}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
                  viewMode === 'card' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <FaTh className="text-sm" />
                <span className="text-[10px]">卡片</span>
              </button>
              <button
                onClick={() => handleViewChange('list')}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
                  viewMode === 'list' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <FaList className="text-sm" />
                <span className="text-[10px]">列表</span>
              </button>
              <button
                onClick={() => handleViewChange('topics')}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
                  viewMode === 'topics' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <FaFolder className="text-sm" />
                <span className="text-[10px]">话题</span>
              </button>
              <button
                onClick={() => handleViewChange('audio')}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
                  viewMode === 'audio' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <FaHeadphones className="text-sm" />
                <span className="text-[10px]">音频</span>
              </button>
            </div>
          </div>

          {/* 刷新按钮 */}
          <button
            onClick={handleRefresh}
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
