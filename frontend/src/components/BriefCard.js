import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  FaNewspaper,
  FaExternalLinkAlt,
  FaClock,
  FaLink
} from 'react-icons/fa';

const categoryColors = {
  finance: 'bg-green-100 text-green-800 border-green-300',
  technology: 'bg-blue-100 text-blue-800 border-blue-300',
  health: 'bg-red-100 text-red-800 border-red-300',
  new_energy: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  automotive: 'bg-purple-100 text-purple-800 border-purple-300',
  robotics: 'bg-indigo-100 text-indigo-800 border-indigo-300',
  ai: 'bg-pink-100 text-pink-800 border-pink-300',
  general: 'bg-gray-100 text-gray-800 border-gray-300'
};

const categoryNames = {
  finance: '财经',
  technology: '科技',
  health: '健康',
  new_energy: '新能源',
  automotive: '汽车',
  robotics: '机器人',
  ai: 'AI',
  general: '综合'
};

const BriefCard = ({ brief, isNew = false }) => {
  const colorClass = categoryColors[brief.category] || categoryColors.general;
  const categoryName = categoryNames[brief.category] || '未分类';

  const formatDate = (date) => {
    try {
      return formatDistanceToNow(new Date(date), {
        addSuffix: true,
        locale: zhCN
      });
    } catch {
      return '刚刚';
    }
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 p-5 border-l-4 ${
        isNew ? 'animate-slide-in border-primary' : 'border-gray-200'
      }`}
    >
      {/* 头部 - 分类和时间 */}
      <div className="flex items-center justify-between mb-3">
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${colorClass}`}>
          {categoryName}
        </span>
        <div className="flex items-center text-gray-500 text-xs">
          <FaClock className="mr-1" />
          {formatDate(brief.created_at || brief.published)}
        </div>
      </div>

      {/* 标题 */}
      <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2 hover:text-primary transition-colors">
        <FaNewspaper className="inline mr-2 text-primary" />
        {brief.title}
      </h3>

      {/* 摘要 */}
      <p className="text-gray-700 mb-4 leading-relaxed text-sm">
        {brief.summary}
      </p>

      {/* 底部 - 来源信息 */}
      <div className="border-t pt-3 mt-3">
        <div className="flex items-start justify-between text-xs text-gray-600">
          <div className="flex-1">
            <div className="flex items-center mb-1">
              <FaLink className="mr-2 text-gray-400" />
              <span className="font-semibold">来源:</span>
            </div>
            <div className="ml-5">
              <p className="text-gray-700 font-medium">{brief.source}</p>
              {brief.source_url && (
                <a
                  href={brief.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 hover:underline break-all"
                >
                  {brief.source_url}
                </a>
              )}
            </div>
          </div>

          {brief.link && (
            <a
              href={brief.link}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-3 flex-shrink-0 bg-primary text-white px-3 py-2 rounded-md hover:bg-blue-600 transition-colors flex items-center"
            >
              查看原文
              <FaExternalLinkAlt className="ml-1" />
            </a>
          )}
        </div>
      </div>

      {/* 新消息标记 */}
      {isNew && (
        <div className="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full animate-pulse">
          NEW
        </div>
      )}
    </div>
  );
};

export default BriefCard;
