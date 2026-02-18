import React from 'react';
import { useAudioPlayer } from '../contexts/AudioPlayerContext';
import { FaPlay, FaPause, FaVolumeUp, FaClock, FaExternalLinkAlt } from 'react-icons/fa';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';

// 分类颜色
const categoryColors = {
  ai_technology: 'bg-purple-100 text-purple-700',
  robotics: 'bg-indigo-100 text-indigo-700',
  ai_programming: 'bg-blue-100 text-blue-700',
  semiconductors: 'bg-gray-100 text-gray-700',
  automotive: 'bg-emerald-100 text-emerald-700',
  consumer_electronics: 'bg-cyan-100 text-cyan-700',
  one_piece: 'bg-red-100 text-red-700',
  anime: 'bg-pink-100 text-pink-700',
  tcg: 'bg-orange-100 text-orange-700',
  podcasts: 'bg-pink-100 text-pink-700',
  finance_investment: 'bg-rose-100 text-rose-700',
  business_tech: 'bg-blue-100 text-blue-700',
  politics_world: 'bg-indigo-100 text-indigo-700',
  economy_policy: 'bg-yellow-100 text-yellow-700',
  health_medical: 'bg-teal-100 text-teal-700',
  energy_environment: 'bg-cyan-100 text-cyan-700',
  entertainment_sports: 'bg-orange-100 text-orange-700',
  general: 'bg-gray-100 text-gray-700'
};

const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编程',
  semiconductors: '芯片',
  automotive: '汽车',
  consumer_electronics: '消费电子',
  one_piece: 'OP',
  anime: '动漫',
  tcg: 'TCG',
  podcasts: '播客',
  finance_investment: '财经',
  business_tech: '商业科技',
  politics_world: '国际',
  economy_policy: '经济',
  health_medical: '医疗',
  energy_environment: '能源',
  entertainment_sports: '娱乐',
  general: '综合'
};

const AudioViewCard = ({ brief, index, isNew = false }) => {
  const { 
    currentIndex, 
    isPlaying, 
    isPaused,
    playSingle,
    togglePlay 
  } = useAudioPlayer();
  
  const isCurrentPlaying = currentIndex === index && (isPlaying || isPaused);
  const colorClass = categoryColors[brief.category] || categoryColors.general;
  const categoryName = categoryNames[brief.category] || '综合';
  
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
  
  // 估算阅读时长（中文约 200字/分钟）
  const estimateDuration = () => {
    const text = `${brief.title}${brief.summary}`;
    const charCount = text.length;
    const minutes = Math.ceil(charCount / 200);
    return minutes < 1 ? '< 1 分钟' : `${minutes} 分钟`;
  };
  
  const handlePlayClick = () => {
    if (isCurrentPlaying) {
      togglePlay();
    } else {
      playSingle(brief);
    }
  };
  
  return (
    <div 
      className={`
        bg-white rounded-xl p-4 border transition-all
        ${isCurrentPlaying 
          ? 'border-black shadow-lg ring-2 ring-black/5' 
          : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
        }
        ${isNew ? 'ring-2 ring-blue-500 ring-offset-2' : ''}
      `}
    >
      <div className="flex items-center gap-4">
        {/* 播放按钮 */}
        <button
          onClick={handlePlayClick}
          className={`
            flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center
            transition-all duration-200
            ${isCurrentPlaying
              ? 'bg-black text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }
          `}
        >
          {isCurrentPlaying && isPlaying ? (
            <FaPause className="text-lg" />
          ) : isCurrentPlaying && isPaused ? (
            <FaPlay className="text-lg ml-0.5" />
          ) : (
            <FaPlay className="text-lg ml-0.5" />
          )}
        </button>
        
        {/* 内容 */}
        <div className="flex-1 min-w-0">
          {/* 元信息 */}
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-medium px-2 py-0.5 rounded ${colorClass}`}>
              {categoryName}
            </span>
            <span className="text-xs text-gray-400 flex items-center">
              <FaClock className="mr-1 text-[10px]" />
              {formatDate(brief.created_at || brief.published)}
            </span>
            <span className="text-xs text-gray-400">
              · {estimateDuration()}
            </span>
            {brief.importance === 'breaking' && (
              <span className="text-xs bg-red-500 text-white px-1.5 py-0.5 rounded">
                Breaking
              </span>
            )}
            {brief.importance === 'high' && (
              <span className="text-xs bg-orange-500 text-white px-1.5 py-0.5 rounded">
                重要
              </span>
            )}
          </div>
          
          {/* 标题 */}
          <h3 className={`
            font-medium text-gray-900 line-clamp-2
            ${isCurrentPlaying ? 'text-black' : ''}
          `}>
            {brief.title}
          </h3>
          
          {/* 来源 */}
          <div className="mt-1 flex items-center justify-between">
            <span className="text-xs text-gray-400">{brief.source}</span>
            {brief.link && (
              <a
                href={brief.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-gray-400 hover:text-gray-600 flex items-center"
                onClick={(e) => e.stopPropagation()}
              >
                原文 <FaExternalLinkAlt className="ml-1 text-[10px]" />
              </a>
            )}
          </div>
        </div>
        
        {/* 播放指示器 */}
        {isCurrentPlaying && isPlaying && (
          <div className="flex-shrink-0 flex items-center gap-0.5">
            <span className="w-1 h-4 bg-black rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
            <span className="w-1 h-6 bg-black rounded-full animate-pulse" style={{ animationDelay: '150ms' }} />
            <span className="w-1 h-3 bg-black rounded-full animate-pulse" style={{ animationDelay: '300ms' }} />
            <span className="w-1 h-5 bg-black rounded-full animate-pulse" style={{ animationDelay: '450ms' }} />
          </div>
        )}
      </div>
    </div>
  );
};

export default AudioViewCard;
