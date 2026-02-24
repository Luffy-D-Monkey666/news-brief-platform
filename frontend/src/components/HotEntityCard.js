import React from 'react';
import { Link } from 'react-router-dom';
import { FaNewspaper, FaChevronRight, FaFire } from 'react-icons/fa';

// 实体类型配置
const typeConfig = {
  company: { icon: '🏢', label: '公司', color: 'text-blue-600 bg-blue-50' },
  person: { icon: '👤', label: '人物', color: 'text-purple-600 bg-purple-50' },
  product: { icon: '📦', label: '产品', color: 'text-green-600 bg-green-50' },
  concept: { icon: '💡', label: '概念', color: 'text-orange-600 bg-orange-50' },
  event: { icon: '📅', label: '事件', color: 'text-red-600 bg-red-50' }
};

const HotEntityCard = ({ entity, rank }) => {
  const config = typeConfig[entity.type] || typeConfig.concept;
  
  return (
    <Link
      to={`/entity/${entity._id}`}
      className="block bg-white rounded-xl border border-gray-200 p-4 hover:shadow-lg hover:border-gray-300 transition-all group"
      style={{ boxShadow: '0 2px 12px -2px rgba(0, 0, 0, 0.08)' }}
    >
      <div className="flex items-start gap-3">
        {/* 排名 */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold ${
          rank <= 3 
            ? 'bg-gradient-to-br from-orange-400 to-red-500 text-white' 
            : 'bg-gray-100 text-gray-600'
        }`}>
          {rank}
        </div>
        
        {/* 内容 */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">{config.icon}</span>
            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors truncate">
              {entity.name}
            </h3>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          </div>
          
          {entity.description && (
            <p className="text-sm text-gray-500 line-clamp-2 mb-2">
              {entity.description}
            </p>
          )}
          
          <div className="flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <FaFire className="text-orange-500" />
              <span className="font-medium text-orange-600">{entity.recent_news_count}</span> 条今日新闻
            </span>
            <span className="flex items-center gap-1">
              <FaNewspaper />
              累计 {entity.news_count || 0} 条
            </span>
          </div>
        </div>
        
        {/* 箭头 */}
        <FaChevronRight className="flex-shrink-0 text-gray-300 group-hover:text-gray-500 transition-colors mt-2" />
      </div>
    </Link>
  );
};

export default HotEntityCard;
