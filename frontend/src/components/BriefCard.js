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
      className={`group bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-500 ${
        isNew ? 'animate-slide-in ring-2 ring-black' : ''
      }`}
    >
      {/* 图片区域 */}
      {brief.image && (
        <div className="relative w-full h-48 overflow-hidden bg-gray-100">
          <img
            src={brief.image}
            alt={brief.title}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          {/* 分类标签叠加在图片上 */}
          <div className="absolute top-3 left-3">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold backdrop-blur-md bg-white/90 ${colorClass}`}>
              {categoryName}
            </span>
          </div>
          {/* NEW标记 */}
          {isNew && (
            <div className="absolute top-3 right-3 bg-black text-white text-xs px-3 py-1 rounded-full font-bold animate-pulse">
              NEW
            </div>
          )}
        </div>
      )}

      {/* 内容区域 */}
      <div className="p-5">
        {/* 没有图片时显示分类和时间 */}
        {!brief.image && (
          <div className="flex items-center justify-between mb-3">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${colorClass}`}>
              {categoryName}
            </span>
            <div className="flex items-center text-gray-500 text-xs">
              <FaClock className="mr-1" />
              {formatDate(brief.created_at || brief.published)}
            </div>
          </div>
        )}

        {/* 标题 */}
        <h3 className="text-lg font-bold text-gray-900 mb-3 group-hover:text-black transition-colors">
          {brief.title}
        </h3>

        {/* 摘要 - 完整显示，不截断 */}
        <p className="text-gray-600 mb-4 leading-relaxed text-sm whitespace-pre-wrap">
          {brief.summary}
        </p>

        {/* 底部 - 来源和时间 */}
        <div className="flex items-center justify-between text-xs border-t pt-3">
          <div className="flex items-center text-gray-500">
            <FaLink className="mr-2" />
            <span className="truncate">{brief.source}</span>
          </div>
          {brief.image && (
            <div className="flex items-center text-gray-500">
              <FaClock className="mr-1" />
              {formatDate(brief.created_at || brief.published)}
            </div>
          )}
        </div>

        {/* 查看原文按钮 */}
        {brief.link && (
          <a
            href={brief.link}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-3 w-full flex items-center justify-center bg-black text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
          >
            查看原文
            <FaExternalLinkAlt className="ml-2 text-xs" />
          </a>
        )}
      </div>
    </div>
  );
};

export default BriefCard;
