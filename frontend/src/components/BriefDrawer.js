import React, { useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import BriefCard from './BriefCard';

const BriefDrawer = ({ brief, isOpen, onClose }) => {
  // 打开时禁止背景滚动
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // ESC 键关闭
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleEsc);
    }
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen || !brief) return null;

  return (
    <>
      {/* 背景遮罩 */}
      <div
        className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 transition-opacity"
        onClick={onClose}
      />
      
      {/* 抽屉面板 */}
      <div className="fixed top-0 right-0 h-full w-full max-w-2xl bg-gray-50 shadow-2xl z-50 transform transition-transform duration-300 ease-out overflow-hidden flex flex-col">
        {/* 头部 */}
        <div className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200 flex-shrink-0">
          <h2 className="text-lg font-semibold text-gray-900 truncate pr-4">
            {brief.title}
          </h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors flex-shrink-0"
          >
            <FaTimes className="w-5 h-5" />
          </button>
        </div>
        
        {/* 内容区域 */}
        <div className="flex-1 overflow-y-auto p-6">
          <BriefCard brief={brief} globalCollapsed={false} />
        </div>
      </div>
    </>
  );
};

export default BriefDrawer;
