import React, { useState, useEffect } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  FaExternalLinkAlt,
  FaClock,
  FaLink,
  FaTimes,
  FaVolumeUp,
  FaPause,
  FaPlay,
  FaSpinner,
  FaChevronDown,
  FaChevronUp
} from 'react-icons/fa';
import { useAudioPlayer } from '../contexts/AudioPlayerContext';

// Apple风格配色（更简洁清爽）
const categoryColors = {
  ai_technology: 'text-purple-600',
  robotics: 'text-indigo-600',
  ai_programming: 'text-blue-600',
  semiconductors: 'text-gray-700',
  opcg: 'text-orange-600',
  automotive: 'text-emerald-600',
  consumer_electronics: 'text-cyan-600',
  one_piece: 'text-red-600',
  anime: 'text-pink-600',
  tcg: 'text-orange-500',
  podcasts: 'text-pink-600',
  finance_investment: 'text-rose-600',
  business_tech: 'text-blue-600',
  politics_world: 'text-indigo-600',
  economy_policy: 'text-yellow-600',
  health_medical: 'text-teal-600',
  energy_environment: 'text-cyan-600',
  entertainment_sports: 'text-orange-600',
  general: 'text-gray-600'
};

const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编程',
  semiconductors: '芯片',
  opcg: 'OPCG',
  automotive: '汽车',
  consumer_electronics: '消费电子',
  one_piece: 'OP',
  anime: '动漫',
  tcg: 'TCG',
  podcasts: '播客推荐',
  finance_investment: '投资财经',
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  general: '综合'
};

// 来源可信度配置
const sourceTierConfig = {
  official: { label: '官方', icon: '🏛️', color: 'bg-blue-100 text-blue-800' },
  mainstream: { label: '权威媒体', icon: '📰', color: 'bg-green-100 text-green-800' },
  specialized: { label: '专业媒体', icon: '🔬', color: 'bg-purple-100 text-purple-800' },
  community: { label: '社区', icon: '💬', color: 'bg-gray-100 text-gray-600' }
};

// 重要性配置
const importanceConfig = {
  breaking: { label: 'Breaking', color: 'bg-red-500 text-white', border: 'ring-2 ring-red-500' },
  high: { label: '重要', color: 'bg-orange-500 text-white', border: 'ring-2 ring-orange-300' },
  normal: { label: '', color: '', border: '' }
};

// 声音预设配置现在从 AudioPlayerContext 获取

// 图片放大Modal
const ImageModal = ({ src, alt, onClose }) => {
  return (
    <div
      className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-8"
      onClick={onClose}
    >
      <button
        className="absolute top-6 right-6 bg-white/10 hover:bg-white/20 rounded-full p-3 transition-all"
        onClick={onClose}
      >
        <FaTimes className="text-white w-6 h-6" />
      </button>
      <img
        src={src}
        alt={alt}
        className="max-w-full max-h-full object-contain rounded-2xl shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      />
    </div>
  );
};

const BriefCard = ({ brief, isNew = false }) => {
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);
  const [showVoiceMenu, setShowVoiceMenu] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  // 检测屏幕宽度，768px 以下为手机端
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // 使用统一的 AudioPlayerContext（豆包 TTS）
  const {
    playlist,
    currentIndex,
    isPlaying: globalIsPlaying,
    isPaused: globalIsPaused,
    isLoading,
    selectedVoice,
    voicePresets,
    playSingle,
    togglePlay,
    stop,
    changeVoice,
  } = useAudioPlayer();

  // 判断当前卡片是否正在播放
  const cardIndex = playlist.findIndex(b => b._id === brief._id);
  // cardIndex >= 0 确保 brief 在 playlist 中，currentIndex >= 0 确保有正在播放的内容
  const isCurrentCard = cardIndex >= 0 && cardIndex === currentIndex && currentIndex >= 0;
  const isPlaying = isCurrentCard && globalIsPlaying;
  const isPaused = isCurrentCard && globalIsPaused;
  const isCardLoading = isCurrentCard && isLoading;

  // 点击朗读按钮 - 使用统一的底部播放栏
  const handleRead = () => {
    if (isCurrentCard) {
      // 当前卡片正在播放/暂停，切换播放状态
      togglePlay();
    } else {
      // 播放这条新闻
      playSingle(brief);
    }
  };

  // 停止朗读
  const handleStop = () => {
    stop();
  };

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

  // 格式化摘要为结构化内容（支持原文引用）
  const formatSummary = (text) => {
    const sections = {
      overview: null,
      quote: null,
      details: [],
      impact: null
    };

    // 提取"事件概述"
    const overviewMatch = text.match(/事件概述[:：]\s*([\s\S]*?)(?=原文引用|重要细节|后续影响|$)/);
    if (overviewMatch) {
      sections.overview = overviewMatch[1].trim();
    }

    // 提取"原文引用"
    const quoteMatch = text.match(/原文引用[:：]\s*([\s\S]*?)(?=重要细节|后续影响|$)/);
    if (quoteMatch) {
      sections.quote = quoteMatch[1].trim();
    }

    // 提取"重要细节"
    const detailsMatch = text.match(/重要细节[:：]\s*([\s\S]*?)(?=后续影响|$)/);
    if (detailsMatch) {
      const detailsText = detailsMatch[1].trim();
      sections.details = detailsText
        .split(/\n/)
        .filter(line => line.trim() && line.includes('•'))
        .map(line => line.replace(/^[•\-\*]\s*/, '').trim());
    }

    // 提取"后续影响"
    const impactMatch = text.match(/后续影响[:：]\s*([\s\S]*?)$/);
    if (impactMatch) {
      sections.impact = impactMatch[1].trim();
    }

    // 如果没有识别到结构，尝试用空行分割
    if (!sections.overview && !sections.details.length && !sections.impact) {
      const paragraphs = text.split(/\n\n+/).filter(p => p.trim());
      if (paragraphs.length >= 3) {
        sections.overview = paragraphs[0].trim();
        const middle = paragraphs[1].trim();
        sections.details = middle.split(/\n/).filter(l => l.trim() && l.includes('•')).map(l => l.replace(/^[•\-\*]\s*/, '').trim());
        sections.impact = paragraphs.slice(2).join('\n\n').trim();
      }
    }

    return {
      hasStructure: sections.overview || sections.details.length || sections.impact,
      overview: sections.overview,
      quote: sections.quote,
      details: sections.details,
      impact: sections.impact
    };
  };

  const summary = formatSummary(brief.summary);
  const sourceTier = sourceTierConfig[brief.source_tier] || sourceTierConfig.community;
  const importance = importanceConfig[brief.importance] || importanceConfig.normal;

  return (
    <>
      <div
        className={`group bg-white rounded-2xl overflow-hidden border border-gray-200/60 shadow-sm hover:shadow-2xl transition-all duration-500 hover:border-gray-300 ${
          isNew ? 'ring-2 ring-blue-500 ring-offset-2' : ''
        } ${importance.border}`}
      >
        {/* Breaking News 标签 */}
        {brief.importance === 'breaking' && (
          <div className="bg-red-500 text-white text-center py-1 text-xs font-bold tracking-wide">
            🔴 BREAKING NEWS
          </div>
        )}
        
        {/* 视频/图片区域 */}
        {(brief.video && !videoError) ? (
          <div
            className="relative w-full h-52 overflow-hidden bg-gray-50"
          >
            <video
              src={brief.video}
              className="w-full h-full object-cover"
              controls
              controlsList="nodownload"
              onError={(e) => {
                console.log('视频加载失败，切换到图片:', e);
                setVideoError(true);
              }}
            />
            <div className="absolute top-4 left-4 flex gap-2">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
              {brief.importance === 'high' && (
                <span className="px-2 py-1.5 rounded-full text-xs font-medium bg-orange-500 text-white">
                  重要
                </span>
              )}
            </div>
          </div>
        ) : brief.image && (
          <div
            className="relative w-full h-52 overflow-hidden bg-gray-50 cursor-pointer"
            onClick={() => setIsImageModalOpen(true)}
          >
            <img
              src={brief.image}
              alt={brief.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
              <span className="text-white text-sm font-medium">查看大图</span>
            </div>
            <div className="absolute top-4 left-4 flex gap-2">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
              {brief.importance === 'high' && (
                <span className="px-2 py-1.5 rounded-full text-xs font-medium bg-orange-500 text-white">
                  重要
                </span>
              )}
            </div>
          </div>
        )}

        {/* 内容区域 */}
        <div className="p-5">
          {/* 没有视频和图片时的分类标签 + 来源可信度 */}
          {!brief.video && !brief.image && (
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className={`text-xs font-semibold ${colorClass}`}>
                  {categoryName}
                </span>
                {brief.importance === 'high' && (
                  <span className="px-2 py-0.5 rounded text-xs font-medium bg-orange-500 text-white">
                    重要
                  </span>
                )}
              </div>
              <div className="flex items-center text-gray-400 text-xs">
                <FaClock className="mr-1.5" />
                {formatDate(brief.created_at || brief.published)}
              </div>
            </div>
          )}

          {/* 朗读控制栏 - 使用豆包 TTS */}
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              {isCardLoading ? (
                <button
                  disabled
                  className="flex items-center gap-2 px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed text-sm font-medium"
                >
                  <FaSpinner className="animate-spin" />
                  加载中...
                </button>
              ) : !isPlaying && !isPaused ? (
                <button
                  onClick={handleRead}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <FaVolumeUp />
                  朗读
                </button>
              ) : isPaused ? (
                <button
                  onClick={handleRead}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <FaPlay />
                  继续
                </button>
              ) : (
                <button
                  onClick={handleRead}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm font-medium"
                >
                  <FaPause />
                  暂停
                </button>
              )}

              {(isPlaying || isPaused) && (
                <button
                  onClick={handleStop}
                  className="px-3 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                >
                  停止
                </button>
              )}
            </div>

            {/* 声音选择器 - 豆包音色（分类显示） */}
            <div className="relative">
              <button
                onClick={() => setShowVoiceMenu(!showVoiceMenu)}
                className="flex items-center gap-2 px-3 py-2 text-xs text-gray-600 hover:text-gray-900 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <FaVolumeUp className="text-gray-400" />
                <span className="font-medium">{voicePresets[selectedVoice]?.name || '选择音色'}</span>
              </button>

              {showVoiceMenu && (
                <div className="absolute right-0 top-full mt-2 w-52 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-10 max-h-64 overflow-y-auto">
                  {/* 按分类分组显示 */}
                  {(() => {
                    const categories = {};
                    Object.entries(voicePresets).forEach(([key, preset]) => {
                      const cat = preset.description || '其他';
                      if (!categories[cat]) categories[cat] = [];
                      categories[cat].push({ key, ...preset });
                    });
                    
                    return Object.entries(categories).map(([category, voices]) => (
                      <div key={category}>
                        <div className="px-3 py-1.5 text-xs text-gray-800 font-semibold sticky top-0 bg-gray-100 border-b border-gray-200 shadow-sm">
                          {category}
                        </div>
                        {voices.map(({ key, name }) => (
                          <button
                            key={key}
                            onClick={() => {
                              changeVoice(key);
                              setShowVoiceMenu(false);
                            }}
                            className={`w-full px-4 py-1.5 text-left text-sm hover:bg-gray-50 transition-colors ${
                              selectedVoice === key ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
                            }`}
                          >
                            {name}
                          </button>
                        ))}
                      </div>
                    ));
                  })()}
                </div>
              )}
            </div>
          </div>

          {/* 标题 */}
          <h3 className="text-lg font-semibold text-gray-900 mb-4 leading-snug">
            {brief.title}
          </h3>

          {/* 来源可信度标签 */}
          <div className="flex items-center gap-2 mb-3">
            <span className={`px-2 py-1 rounded text-xs font-medium ${sourceTier.color}`}>
              {sourceTier.icon} {sourceTier.label}
            </span>
          </div>

          {/* 摘要 - 结构化显示 */}
          {summary.hasStructure ? (
            <div className="space-y-5 mb-5">
              {/* 事件概述 - 始终显示 */}
              {summary.overview && (
                <div>
                  <div className="flex items-center gap-2 mb-3 pb-2 border-b-2 border-dashed border-gray-200">
                    <div className="w-2 h-5 rounded-full bg-gradient-to-b from-blue-400 to-blue-600" />
                    <span className="text-sm font-bold text-gray-700 tracking-wide">事件概述</span>
                  </div>
                  <p className="text-sm text-gray-800 leading-relaxed pl-5">
                    {summary.overview}
                  </p>
                </div>
              )}

              {/* 手机端折叠内容 - 原文引用、重要细节、后续影响 */}
              {(!isMobile || isExpanded) && (
                <>
                  {/* 原文引用 */}
                  {summary.quote && (
                    <div className="bg-gray-50 border-l-4 border-blue-400 pl-4 pr-3 py-3 rounded-r-lg">
                      <div className="flex items-center gap-1 mb-2">
                        <span className="text-blue-500">💬</span>
                        <span className="text-xs font-medium text-gray-500">原文引用</span>
                      </div>
                      <p className="text-sm text-gray-700 italic leading-relaxed">
                        {summary.quote}
                      </p>
                    </div>
                  )}

                  {/* 重要细节 */}
                  {summary.details.length > 0 && (
                    <div>
                      <div className="flex items-center gap-2 mb-3 pb-2 border-b-2 border-dashed border-gray-200">
                        <div className="w-2 h-5 rounded-full bg-gradient-to-b from-purple-400 to-purple-600" />
                        <span className="text-sm font-bold text-gray-700 tracking-wide">重要细节</span>
                      </div>
                      <ul className="space-y-2 pl-5">
                        {summary.details.map((detail, i) => (
                          <li key={i} className="flex items-start text-sm text-gray-800 leading-relaxed">
                            <span className="w-2 h-2 rounded-full bg-purple-400 mt-2 mr-3 flex-shrink-0" />
                            <span className="flex-1">{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* 后续影响 */}
                  {summary.impact && (
                    <div>
                      <div className="flex items-center gap-2 mb-3 pb-2 border-b-2 border-dashed border-gray-200">
                        <div className="w-2 h-5 rounded-full bg-gradient-to-b from-green-400 to-green-600" />
                        <span className="text-sm font-bold text-gray-700 tracking-wide">后续影响</span>
                      </div>
                      <p className="text-sm text-gray-800 leading-relaxed pl-5">
                        {summary.impact}
                      </p>
                    </div>
                  )}
                </>
              )}

              {/* 手机端展开/收起按钮 */}
              {isMobile && (summary.quote || summary.details.length > 0 || summary.impact) && (
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="w-full flex items-center justify-center gap-2 py-2 text-sm text-blue-600 hover:text-blue-800 transition-colors"
                >
                  {isExpanded ? (
                    <>
                      <FaChevronUp className="text-xs" />
                      收起详情
                    </>
                  ) : (
                    <>
                      <FaChevronDown className="text-xs" />
                      展开详情
                    </>
                  )}
                </button>
              )}
            </div>
          ) : (
            // 非结构化摘要
            <div className="mb-5 p-4 bg-gray-50 rounded-xl text-sm text-gray-800 leading-relaxed whitespace-pre-line">
              {isMobile && !isExpanded ? (
                <>
                  {brief.summary.length > 150 ? `${brief.summary.slice(0, 150)}...` : brief.summary}
                  {brief.summary.length > 150 && (
                    <button
                      onClick={() => setIsExpanded(true)}
                      className="block mt-2 text-blue-600 hover:text-blue-800 text-sm"
                    >
                      展开全文
                    </button>
                  )}
                </>
              ) : (
                <>
                  {brief.summary}
                  {isMobile && brief.summary.length > 150 && (
                    <button
                      onClick={() => setIsExpanded(false)}
                      className="block mt-2 text-blue-600 hover:text-blue-800 text-sm"
                    >
                      收起
                    </button>
                  )}
                </>
              )}
            </div>
          )}

          {/* 附加信息区域 - 手机端需展开才显示 */}
          {(!isMobile || isExpanded) && (
            <>
          {/* 股票信息（仅财经/商业类显示） */}
          {brief.stock_info && brief.stock_info.ticker && (
            <div className="mb-5 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-green-600">📈</span>
                  <span className="text-xs font-bold text-green-800">实时股票数据</span>
                </div>
                <span className="text-xs text-gray-400">数据延迟约15分钟</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-lg font-bold text-gray-900">{brief.stock_info.ticker}</span>
                    <span className="text-sm text-gray-500">{brief.stock_info.name}</span>
                  </div>
                  {brief.stock_info.price && (
                    <div className="flex items-baseline gap-2 mt-1">
                      <span className="text-2xl font-bold text-gray-900">
                        {brief.stock_info.currency === 'USD' ? '$' : 
                         brief.stock_info.currency === 'HKD' ? 'HK$' : 
                         brief.stock_info.currency === 'CNY' ? '¥' : ''}
                        {brief.stock_info.price?.toFixed(2)}
                      </span>
                      {brief.stock_info.change_formatted && (
                        <span className={`text-sm font-medium ${
                          brief.stock_info.change_percent >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {brief.stock_info.change_formatted}
                        </span>
                      )}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  {brief.stock_info.market_cap_formatted && (
                    <div>
                      <span className="text-xs text-gray-500">市值</span>
                      <div className="text-sm font-bold text-gray-800">{brief.stock_info.market_cap_formatted}</div>
                    </div>
                  )}
                  {brief.stock_info.pe_ratio && (
                    <div className="mt-1">
                      <span className="text-xs text-gray-500">PE(TTM)</span>
                      <div className="text-sm font-bold text-gray-800">{brief.stock_info.pe_ratio?.toFixed(1)}</div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* 关键指标（如果有数字数据） */}
          {brief.key_metrics && brief.key_metrics.length > 0 && (
            <div className="mb-5 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-blue-600">📊</span>
                <span className="text-xs font-bold text-blue-800">关键数据</span>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {brief.key_metrics.slice(0, 4).map((metric, i) => {
                  // 判断值是否为数字
                  const isNumericValue = typeof metric.value === 'number' || !isNaN(parseFloat(metric.value));
                  // 格式化显示值
                  const displayValue = isNumericValue 
                    ? (typeof metric.value === 'number' ? metric.value.toLocaleString() : metric.value)
                    : metric.value;
                  
                  return (
                    <div key={i} className="bg-white/70 rounded-lg p-2.5 border border-blue-100/50 overflow-hidden">
                      <div className="text-xs text-gray-500 mb-1 truncate">{metric.name}</div>
                      <div className="flex items-baseline gap-1 flex-wrap">
                        {isNumericValue ? (
                          <>
                            <span className="text-lg font-bold text-gray-900 break-all">{displayValue}</span>
                            <span className="text-xs text-gray-500">{metric.unit}</span>
                          </>
                        ) : (
                          // 非数字值，用更紧凑的方式显示
                          <span className="text-sm font-semibold text-gray-800">
                            {displayValue}{metric.unit && ` ${metric.unit}`}
                          </span>
                        )}
                      </div>
                      {metric.entity && (
                        <div className="text-xs text-blue-600 mt-1 truncate">{metric.entity}</div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* 背景知识（仅重要新闻显示） */}
          {brief.background && brief.background.context && (
            <div className="mb-5 p-4 bg-gradient-to-r from-slate-50 to-gray-50 border border-slate-200 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-slate-600">📚</span>
                <span className="text-xs font-bold text-slate-700">背景知识</span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed mb-3">
                {brief.background.context}
              </p>
              
              {/* 时间线 */}
              {brief.background.timeline && brief.background.timeline.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-200">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-slate-500">⏱️</span>
                    <span className="text-xs font-medium text-slate-600">事件时间线</span>
                  </div>
                  <div className="space-y-2">
                    {brief.background.timeline.map((item, i) => (
                      <div key={i} className="flex items-start gap-2 text-xs">
                        <span className="text-slate-500 font-mono whitespace-nowrap">{item.date}</span>
                        <span className="text-slate-400">—</span>
                        <span className="text-slate-700">{item.event}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 技术解读（仅AI/机器人/芯片类显示） */}
          {brief.tech_insight && brief.tech_insight.principle && (
            <div className="mb-5 p-4 bg-gradient-to-r from-violet-50 to-purple-50 border border-violet-200 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-violet-600">🔬</span>
                <span className="text-xs font-bold text-violet-800">技术解读</span>
                {brief.tech_insight.maturity && (
                  <span className="ml-auto px-2 py-0.5 bg-violet-100 text-violet-700 rounded text-xs">
                    {brief.tech_insight.maturity}
                  </span>
                )}
              </div>
              <div className="space-y-3">
                {brief.tech_insight.principle && (
                  <div>
                    <div className="text-xs text-violet-600 font-medium mb-1">技术原理</div>
                    <p className="text-sm text-gray-700 leading-relaxed">{brief.tech_insight.principle}</p>
                  </div>
                )}
                {brief.tech_insight.comparison && (
                  <div>
                    <div className="text-xs text-violet-600 font-medium mb-1">技术对比</div>
                    <p className="text-sm text-gray-700 leading-relaxed">{brief.tech_insight.comparison}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* 融资历史（仅融资新闻显示） */}
          {brief.funding_history && brief.funding_history.company && (
            <div className="mb-5 p-4 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-emerald-600">💰</span>
                <span className="text-xs font-bold text-emerald-800">融资历史 · {brief.funding_history.company}</span>
              </div>
              
              {/* 融资轮次时间线 */}
              {brief.funding_history.rounds && brief.funding_history.rounds.length > 0 && (
                <div className="space-y-3 mb-3">
                  {brief.funding_history.rounds.map((round, i) => {
                    // 格式化金额：如果是纯数字，补上单位
                    const formatAmount = (amt) => {
                      if (!amt) return '未披露';
                      const str = String(amt);
                      // 如果已经有单位（包含$、¥、€、万、亿、M、B、K等），直接返回
                      if (/[$¥€万亿MBK]/.test(str)) return str;
                      // 纯数字，根据大小添加单位
                      const num = parseFloat(str);
                      if (isNaN(num)) return str;
                      if (num >= 1000) return `$${(num/1000).toFixed(1)}B`;
                      if (num >= 1) return `$${num}M`;
                      return `$${(num*1000).toFixed(0)}K`;
                    };
                    return (
                    <div key={i} className="text-sm">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded text-xs font-medium whitespace-nowrap shrink-0">
                          {round.round}
                        </span>
                        <span className="font-semibold text-gray-800 whitespace-nowrap">{formatAmount(round.amount)}</span>
                      </div>
                      <div className="mt-1 ml-0.5 text-xs text-gray-500">
                        {round.date && <span>{round.date}</span>}
                        {round.date && round.investors && round.investors.length > 0 && <span className="mx-1">·</span>}
                        {round.investors && round.investors.length > 0 && (
                          <span>投资方: {round.investors.join('、')}</span>
                        )}
                      </div>
                    </div>
                    );
                  })}
                </div>
              )}
              
              {/* 累计融资和估值 */}
              {(brief.funding_history.total_funding || brief.funding_history.valuation) && (
                <div className="grid grid-cols-2 gap-3 pt-3 border-t border-emerald-200">
                  <div>
                    <div className="text-xs text-gray-500 mb-0.5">累计融资</div>
                    <div className="text-sm font-bold text-emerald-700">
                      {brief.funding_history.total_funding || '未披露'}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-0.5">最新估值</div>
                    <div className="text-sm font-bold text-emerald-700">
                      {brief.funding_history.valuation || '未披露'}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 供应链视角（仅消费电子/汽车类显示） */}
          {brief.supply_chain_insight && brief.supply_chain_insight.impact && (
            <div className="mb-5 p-4 bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-orange-600">🔗</span>
                <span className="text-xs font-bold text-orange-800">供应链视角</span>
              </div>
              
              <p className="text-sm text-gray-700 leading-relaxed mb-3">{brief.supply_chain_insight.impact}</p>
              
              {/* 关联公司 */}
              {brief.supply_chain_insight.related_companies && brief.supply_chain_insight.related_companies.length > 0 && (
                <div className="space-y-2 mb-3">
                  <div className="text-xs text-orange-600 font-medium">关联供应商</div>
                  <div className="flex flex-wrap gap-2">
                    {brief.supply_chain_insight.related_companies.map((company, i) => (
                      <div key={i} className="inline-flex items-center gap-1.5 px-2 py-1 bg-white/70 rounded-lg border border-orange-100">
                        <span className="text-sm font-medium text-gray-800">{company.name}</span>
                        {company.role && <span className="text-xs text-gray-400">({company.role})</span>}
                        <span className={`text-xs px-1.5 py-0.5 rounded ${
                          company.effect === '利好' ? 'bg-green-100 text-green-700' :
                          company.effect === '利空' ? 'bg-red-100 text-red-700' :
                          'bg-gray-100 text-gray-600'
                        }`}>
                          {company.effect}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* 产能信息 */}
              {brief.supply_chain_insight.capacity_info && (
                <div className="pt-2 border-t border-orange-200">
                  <div className="text-xs text-orange-600 font-medium mb-1">产能/良率</div>
                  <p className="text-sm text-gray-600">{brief.supply_chain_insight.capacity_info}</p>
                </div>
              )}
            </div>
          )}

          {/* 行动建议（仅财经/商业类显示） */}
          {brief.action_advice && (
            <div className="mb-5 p-4 bg-amber-50 border border-amber-200 rounded-xl">
              <div className="text-sm text-amber-900 leading-relaxed whitespace-pre-line">
                {brief.action_advice}
              </div>
            </div>
          )}

          {/* 关键实体背景（entities） */}
          {brief.entities && brief.entities.length > 0 && (
            <div className="mb-5 p-4 bg-gradient-to-r from-cyan-50 to-sky-50 border border-cyan-200 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-cyan-600">📌</span>
                <span className="text-xs font-bold text-cyan-800">关键实体</span>
              </div>
              <div className="space-y-4">
                {brief.entities.map((entity, i) => {
                  // 实体类型图标和标签
                  const typeConfig = {
                    company: { icon: '🏢', label: '公司' },
                    person: { icon: '👤', label: '人物' },
                    tech: { icon: '⚙️', label: '技术' },
                    concept: { icon: '💡', label: '概念' },
                    event: { icon: '📅', label: '事件' }
                  };
                  const config = typeConfig[entity.type] || typeConfig.concept;
                  
                  return (
                    <div key={i} className="bg-white/60 rounded-lg p-3 border border-cyan-100">
                      {/* 实体名称和类型 */}
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-base">{config.icon}</span>
                        <span className="font-semibold text-gray-800">{entity.name}</span>
                        <span className="px-1.5 py-0.5 bg-cyan-100 text-cyan-700 rounded text-xs">
                          {config.label}
                        </span>
                      </div>
                      
                      {/* 背景说明 */}
                      {entity.context && (
                        <p className="text-sm text-gray-700 leading-relaxed mb-2">
                          {entity.context}
                        </p>
                      )}
                      
                      {/* 与本新闻关联 */}
                      {entity.relevance && (
                        <div className="text-xs text-cyan-600 mb-2">
                          <span className="font-medium">📎 关联：</span>
                          <span className="text-gray-600">{entity.relevance}</span>
                        </div>
                      )}
                      
                      {/* 实体时间线 */}
                      {entity.timeline && entity.timeline.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-cyan-100">
                          <div className="space-y-1">
                            {entity.timeline.map((item, j) => (
                              <div key={j} className="flex items-start gap-2 text-xs">
                                <span className="text-cyan-500 font-mono whitespace-nowrap">{item.date}</span>
                                <span className="text-gray-400">→</span>
                                <span className="text-gray-600">{item.event}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
            </>
          )}

          {/* 手机端附加信息展开按钮 - 仅当有附加内容时显示 */}
          {isMobile && !isExpanded && (
            brief.stock_info?.ticker || 
            (brief.key_metrics && brief.key_metrics.length > 0) ||
            brief.background?.context ||
            brief.tech_insight?.principle ||
            brief.funding_history?.company ||
            brief.supply_chain_insight?.impact ||
            brief.action_advice ||
            (brief.entities && brief.entities.length > 0)
          ) && (
            <button
              onClick={() => setIsExpanded(true)}
              className="w-full flex items-center justify-center gap-2 py-3 mb-4 text-sm text-gray-500 hover:text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors"
            >
              <FaChevronDown className="text-xs" />
              查看更多分析
            </button>
          )}

          {/* 底部信息 */}
          <div className="flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-100">
            <div className="flex items-center max-w-[45%]">
              <FaLink className="mr-1.5 flex-shrink-0" />
              <span className="truncate">{brief.source}</span>
            </div>
            {!brief.video && !brief.image && (
              <div className="flex items-center">
                <FaClock className="mr-1.5" />
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
              className="mt-4 w-full flex items-center justify-center bg-gray-900 text-white px-5 py-2.5 rounded-xl hover:bg-gray-800 transition-colors text-sm font-medium"
            >
              查看原文
              <FaExternalLinkAlt className="ml-2 text-xs" />
            </a>
          )}
        </div>
      </div>

      {/* 图片放大Modal */}
      {isImageModalOpen && brief.image && (
        <ImageModal
          src={brief.image}
          alt={brief.title}
          onClose={() => setIsImageModalOpen(false)}
        />
      )}
    </>
  );
};

export default BriefCard;
