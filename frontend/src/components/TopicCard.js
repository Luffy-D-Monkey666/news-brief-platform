import React, { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { FaChevronDown, FaChevronUp, FaNewspaper, FaExternalLinkAlt } from 'react-icons/fa';
import { getTopicDetail } from '../services/api';

// 来源可信度配置
const sourceTierConfig = {
  official: { label: '官方', icon: '🏛️', color: 'text-blue-600' },
  mainstream: { label: '权威', icon: '📰', color: 'text-green-600' },
  specialized: { label: '专业', icon: '🔬', color: 'text-purple-600' },
  community: { label: '社区', icon: '💬', color: 'text-gray-500' }
};

const TopicCard = ({ topic }) => {
  const [expanded, setExpanded] = useState(false);
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleExpand = async () => {
    if (expanded) {
      setExpanded(false);
      return;
    }

    if (briefs.length === 0) {
      setLoading(true);
      try {
        const result = await getTopicDetail(topic._id, 10);
        if (result.success && result.data.briefs) {
          setBriefs(result.data.briefs);
        }
      } catch (error) {
        console.error('加载话题详情失败:', error);
      } finally {
        setLoading(false);
      }
    }
    setExpanded(true);
  };

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
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
      {/* 话题头部 */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={handleExpand}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg">📁</span>
              <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                话题
              </span>
              <span className="text-xs text-gray-400">
                {topic.brief_count} 篇报道
              </span>
            </div>
            <h3 className="font-semibold text-gray-900 line-clamp-2 mb-1">
              {topic.title}
            </h3>
            <div className="text-xs text-gray-400">
              最后更新: {formatDate(topic.updated_at)}
            </div>
          </div>
          <div className="ml-3 text-gray-400">
            {expanded ? <FaChevronUp /> : <FaChevronDown />}
          </div>
        </div>

        {/* 关键词标签 */}
        {topic.keywords && topic.keywords.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {topic.keywords.slice(0, 5).map((keyword, i) => (
              <span 
                key={i}
                className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded"
              >
                {keyword}
              </span>
            ))}
            {topic.keywords.length > 5 && (
              <span className="text-xs text-gray-400">+{topic.keywords.length - 5}</span>
            )}
          </div>
        )}
      </div>

      {/* 展开的新闻列表 */}
      {expanded && (
        <div className="border-t border-gray-100 bg-gray-50">
          {loading ? (
            <div className="p-4 text-center text-gray-500 text-sm">
              加载中...
            </div>
          ) : briefs.length > 0 ? (
            <div className="divide-y divide-gray-100">
              {briefs.map((brief, index) => {
                const tier = sourceTierConfig[brief.source_tier] || sourceTierConfig.community;
                return (
                  <div key={brief._id} className="p-3 hover:bg-white transition-colors">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-medium">
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1 flex-wrap">
                          <span className={`text-xs whitespace-nowrap flex-shrink-0 ${tier.color}`}>
                            {tier.icon} {tier.label}
                          </span>
                          <span className="text-xs text-gray-400 truncate">
                            {brief.source && brief.source.length > 30 
                              ? brief.source.split(' ').slice(0, 3).join(' ') 
                              : brief.source}
                          </span>
                        </div>
                        <h4 className="text-sm font-medium text-gray-800 line-clamp-2 mb-1">
                          {brief.title}
                        </h4>
                        <div className="text-xs text-gray-400">
                          {formatDate(brief.created_at)}
                        </div>
                      </div>
                      {brief.link && (
                        <a
                          href={brief.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-shrink-0 text-gray-400 hover:text-blue-600 transition-colors"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <FaExternalLinkAlt className="text-xs" />
                        </a>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="p-4 text-center text-gray-500 text-sm">
              暂无相关报道
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TopicCard;
