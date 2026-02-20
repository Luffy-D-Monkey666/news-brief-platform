import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getEntityTimeline, synthesizeSpeech } from '../services/api';
import { FaSpinner, FaArrowLeft, FaBuilding, FaUser, FaLightbulb, FaCalendarAlt, FaNewspaper, FaExternalLinkAlt, FaVolumeUp, FaPause, FaStop, FaChevronDown, FaChevronUp } from 'react-icons/fa';

// 实体类型配置
const TYPE_CONFIG = {
  company: { icon: FaBuilding, label: '公司', color: 'bg-blue-100 text-blue-700', borderColor: 'border-blue-400' },
  person: { icon: FaUser, label: '人物', color: 'bg-purple-100 text-purple-700', borderColor: 'border-purple-400' },
  concept: { icon: FaLightbulb, label: '概念', color: 'bg-amber-100 text-amber-700', borderColor: 'border-amber-400' },
  event: { icon: FaCalendarAlt, label: '事件', color: 'bg-green-100 text-green-700', borderColor: 'border-green-400' },
  product: { icon: FaNewspaper, label: '产品', color: 'bg-cyan-100 text-cyan-700', borderColor: 'border-cyan-400' }
};

// 分类名称映射
const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编程',
  semiconductors: '芯片',
  automotive: '汽车',
  consumer_electronics: '消费电子',
  finance_investment: '投资财经',
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  anime: '动漫',
  one_piece: 'OP',
  tcg: 'TCG',
  general: '综合'
};

// 时间轴节点组件
const TimelineNode = ({ item, config }) => {
  if (item.type === 'milestone') {
    // 基础历史节点
    return (
      <div className="relative pl-8 pb-8">
        {/* 时间轴线 */}
        <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200" />
        {/* 节点点 */}
        <div className={`absolute left-1 top-1 w-5 h-5 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 border-2 border-white shadow-md flex items-center justify-center`}>
          <span className="text-white text-xs">🏛️</span>
        </div>
        
        <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-4 border border-gray-200 ml-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono text-gray-500 bg-white px-2 py-0.5 rounded border border-gray-200">
              {item.date}
            </span>
            {item.importance === 'milestone' && (
              <span className="text-xs text-gray-600 bg-gray-200 px-2 py-0.5 rounded font-medium">
                里程碑
              </span>
            )}
          </div>
          <p className="text-sm text-gray-700 font-medium">{item.event}</p>
        </div>
      </div>
    );
  }
  
  // 新闻节点
  return (
    <div className="relative pl-8 pb-8">
      {/* 时间轴线 */}
      <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200" />
      {/* 节点点 */}
      <div className={`absolute left-1 top-1 w-5 h-5 rounded-full ${config.color} border-2 border-white shadow-md flex items-center justify-center`}>
        <FaNewspaper className="text-xs" />
      </div>
      
      <div className="ml-4">
        <div className="text-xs font-mono text-gray-500 mb-2 bg-white inline-block px-2 py-0.5 rounded border border-gray-200">
          {item.date}
        </div>
        
        <div className="space-y-2">
          {item.items.map((news, idx) => (
            <NewsItemCard key={idx} news={news} config={config} categoryNames={categoryNames} />
          ))}
        </div>
      </div>
    </div>
  );
};

// 新闻条目卡片（支持展开/收起）
const NewsItemCard = ({ news, config, categoryNames }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // 从 summary 中提取事件概述（第一段）
  const getEventOverview = (summary) => {
    if (!summary) return null;
    // summary 格式通常是 "事件概述: xxx\n\n原文引用: ..."
    const lines = summary.split('\n');
    for (const line of lines) {
      if (line.startsWith('事件概述:') || line.startsWith('事件概述：')) {
        return line.replace(/^事件概述[:：]\s*/, '').trim();
      }
    }
    // 如果没有明确的事件概述标记，取第一行非空内容
    return lines[0]?.trim() || null;
  };
  
  const eventOverview = getEventOverview(news.summary);
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 hover:shadow-md hover:border-gray-300 transition-all group">
      <div className="p-4">
        <div className="flex items-start gap-3">
          {news.image && (
            <img
              src={news.image}
              alt={news.title}
              className="w-16 h-16 object-cover rounded-lg flex-shrink-0"
              onError={(e) => e.target.style.display = 'none'}
            />
          )}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${config.color}`}>
                {categoryNames[news.category] || news.category}
              </span>
              {news.importance === 'high' && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-orange-100 text-orange-700">
                  重要
                </span>
              )}
              {news.importance === 'breaking' && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-700">
                  突发
                </span>
              )}
            </div>
            <h4 className="text-sm font-medium text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors">
              {news.title}
            </h4>
            {/* 事件概述 */}
            {eventOverview && (
              <p className="text-xs text-gray-600 mt-1.5 line-clamp-2">
                {eventOverview}
              </p>
            )}
            {news.relevance && (
              <p className="text-xs text-gray-500 mt-1">
                📎 {news.relevance}
              </p>
            )}
            <div className="flex items-center gap-3 mt-2">
              {news.link && (
                <a
                  href={news.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-xs text-blue-600 hover:underline"
                >
                  查看原文 <FaExternalLinkAlt className="text-xs" />
                </a>
              )}
            </div>
          </div>
          {/* 展开/收起按钮 */}
          {news.summary && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              title={isExpanded ? '收起详情' : '展开详情'}
            >
              {isExpanded ? <FaChevronUp /> : <FaChevronDown />}
            </button>
          )}
        </div>
      </div>
      
      {/* 展开的完整内容 */}
      {isExpanded && news.summary && (
        <div className="px-4 pb-4 pt-0 border-t border-gray-100">
          <div className="mt-3 text-sm text-gray-700 whitespace-pre-line leading-relaxed bg-gray-50 rounded-lg p-3">
            {news.summary}
          </div>
        </div>
      )}
    </div>
  );
};

const EntityPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 语音播放状态
  const [isPlaying, setIsPlaying] = useState(false);
  const [isSpeechLoading, setIsSpeechLoading] = useState(false);
  const audioRef = useRef(null);
  const audioUrlRef = useRef(null);

  // 生成朗读文本
  const generateSpeechText = (entity, timeline) => {
    const typeLabel = TYPE_CONFIG[entity.type]?.label || '实体';
    let text = `${entity.name}，${typeLabel}。`;
    
    if (entity.description) {
      text += `${entity.description} `;
    }
    
    // 添加时间轴里程碑
    const milestones = timeline.filter(t => t.type === 'milestone');
    if (milestones.length > 0) {
      text += `主要里程碑包括：`;
      milestones.slice(0, 5).forEach((m, i) => {
        text += `${m.date}，${m.event}。`;
      });
    }
    
    // 添加近期新闻概要
    const newsItems = timeline.filter(t => t.type === 'news');
    if (newsItems.length > 0) {
      text += `近期动态：`;
      newsItems.slice(0, 3).forEach(news => {
        if (news.items && news.items.length > 0) {
          text += `${news.date}，${news.items[0].title}。`;
        }
      });
    }
    
    return text;
  };

  // 播放语音
  const handlePlaySpeech = async () => {
    if (!data) return;
    
    if (isPlaying) {
      // 暂停
      if (audioRef.current) {
        audioRef.current.pause();
      }
      setIsPlaying(false);
      return;
    }
    
    // 如果已有音频URL，继续播放
    if (audioUrlRef.current && audioRef.current) {
      audioRef.current.play();
      setIsPlaying(true);
      return;
    }
    
    // 生成新音频
    try {
      setIsSpeechLoading(true);
      const text = generateSpeechText(data.entity, data.timeline);
      const audioUrl = await synthesizeSpeech(text);
      audioUrlRef.current = audioUrl;
      
      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      
      audio.onended = () => {
        setIsPlaying(false);
      };
      
      audio.onerror = () => {
        setIsPlaying(false);
        setIsSpeechLoading(false);
      };
      
      await audio.play();
      setIsPlaying(true);
    } catch (err) {
      console.error('语音合成失败:', err);
    } finally {
      setIsSpeechLoading(false);
    }
  };

  // 停止播放
  const handleStopSpeech = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
  };

  // 清理音频资源
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
    };
  }, []);

  useEffect(() => {
    // 页面加载时滚动到顶部
    window.scrollTo(0, 0);
    
    const loadEntity = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await getEntityTimeline(id);
        setData(response.data);
      } catch (err) {
        console.error('加载实体失败:', err);
        setError('无法加载实体信息');
      } finally {
        setLoading(false);
      }
    };
    
    loadEntity();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <FaSpinner className="animate-spin text-5xl text-black" />
        <span className="ml-4 text-gray-600 text-lg">加载中...</span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <p className="text-gray-500 text-xl mb-4">{error || '实体不存在'}</p>
        <button
          onClick={() => navigate('/knowledge')}
          className="text-blue-600 hover:underline"
        >
          返回知识库
        </button>
      </div>
    );
  }

  const { entity, timeline } = data;
  const config = TYPE_CONFIG[entity.type] || TYPE_CONFIG.concept;
  const Icon = config.icon;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-black shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/knowledge')}
                className="text-gray-400 hover:text-white transition-colors"
                title="返回知识库"
              >
                <FaArrowLeft className="text-xl" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-white">{entity.name}</h1>
                <p className="text-gray-400 text-sm mt-0.5">知识库 · 时间轴</p>
              </div>
            </div>
            <Link
              to="/"
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all text-sm font-medium"
            >
              <span>🏠</span>
              <span>主页</span>
            </Link>
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 实体信息卡片 */}
        <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm mb-8">
          <div className="flex items-start gap-5">
            {/* 图标 */}
            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${config.color}`}>
              <Icon className="text-3xl" />
            </div>
            
            {/* 信息 */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h2 className="text-2xl font-bold text-gray-900">{entity.name}</h2>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
                  {config.label}
                </span>
              </div>
              
              {entity.description && (
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {entity.description}
                </p>
              )}
              
              {/* 元数据 */}
              {entity.metadata && Object.keys(entity.metadata).length > 0 && (
                <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                  {entity.metadata.founded && (
                    <span>成立: {entity.metadata.founded}</span>
                  )}
                  {entity.metadata.founder && (
                    <span>创始人: {entity.metadata.founder}</span>
                  )}
                  {entity.metadata.headquarters && (
                    <span>总部: {entity.metadata.headquarters}</span>
                  )}
                  {entity.metadata.ticker && (
                    <span>股票: {entity.metadata.ticker}</span>
                  )}
                </div>
              )}
              
              {/* 统计 + 语音按钮 */}
              <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center gap-2 text-sm">
                  <FaNewspaper className="text-gray-400" />
                  <span className="font-medium text-gray-900">{entity.news_count || 0}</span>
                  <span className="text-gray-500">条相关新闻</span>
                </div>
                
                {/* 语音朗读按钮 */}
                <div className="flex items-center gap-2">
                  {isSpeechLoading ? (
                    <button
                      disabled
                      className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-400 rounded-lg text-sm cursor-not-allowed"
                    >
                      <FaSpinner className="animate-spin" />
                      生成中...
                    </button>
                  ) : isPlaying ? (
                    <>
                      <button
                        onClick={handlePlaySpeech}
                        className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm font-medium"
                      >
                        <FaPause />
                        暂停
                      </button>
                      <button
                        onClick={handleStopSpeech}
                        className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
                      >
                        <FaStop />
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={handlePlaySpeech}
                      className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
                    >
                      <FaVolumeUp />
                      语音介绍
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 时间轴标题 */}
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-900">📅 时间轴</h3>
          <span className="text-sm text-gray-500">
            {timeline.length} 个节点
          </span>
        </div>

        {/* 时间轴 */}
        {timeline.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl border border-gray-200">
            <FaCalendarAlt className="mx-auto text-5xl text-gray-300 mb-4" />
            <p className="text-gray-500">暂无时间轴数据</p>
            <p className="text-gray-400 text-sm mt-1">
              当有相关新闻时，会自动添加到时间轴
            </p>
          </div>
        ) : (
          <div className="relative">
            {timeline.map((item, index) => (
              <TimelineNode key={index} item={item} config={config} />
            ))}
            {/* 时间轴结束点 */}
            <div className="relative pl-8">
              <div className="absolute left-3 top-0 w-0.5 h-4 bg-gray-200" />
              <div className="absolute left-2 top-4 w-3 h-3 rounded-full bg-gray-300" />
            </div>
          </div>
        )}
      </main>

      {/* 底部 */}
      <footer className="bg-black mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 NewsHub · AI驱动的新闻聚合平台 · Powered by DeepSeek
          </p>
        </div>
      </footer>
    </div>
  );
};

export default EntityPage;
