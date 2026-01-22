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
  // One Piece 专区（特殊金黄色）
  op_card_game: 'bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-900 border-yellow-400',
  op_merchandise: 'bg-gradient-to-r from-orange-100 to-red-100 text-orange-900 border-orange-400',

  // 核心关注
  ai_robotics: 'bg-purple-100 text-purple-800 border-purple-300',
  ev_automotive: 'bg-green-100 text-green-800 border-green-300',
  finance_investment: 'bg-red-100 text-red-800 border-red-300',

  // 主流分类
  business_tech: 'bg-blue-100 text-blue-800 border-blue-300',
  politics_world: 'bg-indigo-100 text-indigo-800 border-indigo-300',
  economy_policy: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  health_medical: 'bg-pink-100 text-pink-800 border-pink-300',
  energy_environment: 'bg-teal-100 text-teal-800 border-teal-300',
  entertainment_sports: 'bg-orange-100 text-orange-800 border-orange-300',
  general: 'bg-gray-100 text-gray-800 border-gray-300'
};

const categoryNames = {
  // One Piece 专区
  op_card_game: 'OP卡牌游戏',
  op_merchandise: 'OP周边情报',

  // 核心关注
  ai_robotics: 'AI与机器人',
  ev_automotive: '新能源汽车',
  finance_investment: '投资财经',

  // 主流分类
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
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
