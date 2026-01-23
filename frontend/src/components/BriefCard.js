import React, { useState, useEffect, useRef } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  FaExternalLinkAlt,
  FaClock,
  FaLink,
  FaTimes,
  FaVolumeUp,
  FaPause,
  FaPlay
} from 'react-icons/fa';

const categoryColors = {
  // One Piece 专区（Apple风格渐变）
  op_card_game: 'bg-gradient-to-br from-amber-50 to-orange-100 text-amber-900 border border-amber-200',
  op_merchandise: 'bg-gradient-to-br from-orange-50 to-red-100 text-orange-900 border border-orange-200',

  // 核心关注（柔和色彩）
  ai_robotics: 'bg-gradient-to-br from-purple-50 to-purple-100 text-purple-900 border border-purple-200',
  ev_automotive: 'bg-gradient-to-br from-emerald-50 to-teal-100 text-emerald-900 border border-emerald-200',
  finance_investment: 'bg-gradient-to-br from-rose-50 to-red-100 text-rose-900 border border-rose-200',

  // 主流分类（清新配色）
  business_tech: 'bg-gradient-to-brfrom-blue-50 to-indigo-100 text-blue-900 border border-blue-200',
  politics_world: 'bg-gradient-to-br from-indigo-50 to-violet-100 text-indigo-900 border border-indigo-200',
  economy_policy: 'bg-gradient-to-br from-yellow-50 to-amber-100 text-yellow-900 border border-yellow-200',
  health_medical: 'bg-gradient-to-br from-pink-50 to-rose-100 text-pink-900 border border-pink-200',
  energy_environment: 'bg-gradient-to-br from-cyan-50 to-teal-100 text-cyan-900 border border-cyan-200',
  entertainment_sports: 'bg-gradient-to-br from-orange-50 to-amber-100 text-orange-900 border border-orange-200',
  general: 'bg-gradient-to-br from-gray-50 to-slate-100 text-gray-900 border border-gray-200'
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

// 图片放大Modal
const ImageModal = ({ src, alt, onClose }) => {
  return (
    <div
      className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6 transition-opacity duration-300"
      onClick={onClose}
    >
      <button
        className="absolute top-6 right-6 bg-white/10 hover:bg-white/20 rounded-full p-3 transition-all duration-200"
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
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState('');
  const [isPaused, setIsPaused] = useState(false);
  const [showVoiceSelector, setShowVoiceSelector] = useState(false);

  const speechSynthesisRef = useRef(window.speechSynthesis);
  const utteranceRef = useRef(null);
  const voices = useRef([]);

  // 可用的声音（中文）
  const voicesRef = useRef([]);

  // 加载可用的声音
  useEffect(() => {
    const getVoices = () => {
      const allVoices = speechSynthesisRef.current.getVoices();
      // 优先选择中文声音
      const zhVoices = allVoices.filter(voice =>
        voice.lang.includes('zh') || voice.lang.includes('CN')
      );

      // 兼容不同的浏览器命名方式
      const preferredVoices = zhVoices.length > 0 ? zhVoices : allVoices;
      voices.current = preferredVoices;
      voicesRef.current = preferredVoices;

      // 自动选择第一个中文声音或Siri（如果可用）
      if (preferredVoices.length > 0) {
        const siriVoice = preferredVoices.find(v =>
          v.name.includes('Siri') || v.name.includes('Ting-Ting') || v.name.includes('Huihui')
        );
        setSelectedVoice(siriVoice ? siriVoice.name : preferredVoices[0].name);
      }
    };

    // Chrome需要事件触发
    speechSynthesisRef.current.onvoiceschanged = getVoices;
    getVoices();
  }, []);

  // 开始朗读
  const handleRead = () => {
    if (isPaused) {
      speechSynthesisRef.current.resume();
      setIsPaused(false);
      setIsPlaying(true);
      return;
    }

    if (isPlaying) {
      handlePause();
      return;
    }

    // 取消之前的朗读
    speechSynthesisRef.current.cancel();

    const text = `${brief.title}。${brief.summary}`;
    const utterance = new SpeechSynthesisUtterance(text);
    utteranceRef.current = utterance;

    // 设置中文语言
    utterance.lang = 'zh-CN';

    // 选择声音
    const selectedVoiceObj = voicesRef.current.find(v => v.name === selectedVoice);
    if (selectedVoiceObj) {
      utterance.voice = selectedVoiceObj;
    }

    // 语速和音调调整（自然叙述风格）
    utterance.rate = 0.95; // 稍慢，更自然
    utterance.pitch = 1.0;  // 正常音调

    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    utterance.onerror = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    speechSynthesisRef.current.speak(utterance);
    setIsPlaying(true);
  };

  // 暂停朗读
  const handlePause = () => {
    speechSynthesisRef.current.pause();
    setIsPaused(true);
    setIsPlaying(false);
  };

  // 停止朗读
  const handleStop = () => {
    speechSynthesisRef.current.cancel();
    setIsPlaying(false);
    setIsPaused(false);
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

  const formatSummary = (text) => {
    // 将 • 转换为自然段落
    if (text.includes('•')) {
      return text.split('•').map((part, i) => {
        const trimmed = part.trim();
        if (!trimmed) return null;
        return (
          <p key={i} className="mb-3 last:mb-0 leading-[1.8]">
            {trimmed}
          </p>
        );
      });
    }
    // 原始段落按换行符分割
    return text.split('\n').map((para, i) => (
      <p key={i} className="mb-3 last:mb-0 leading-[1.8]">
        {para}
      </p>
    ));
  };

  return (
    <>
      <div
        className={`group bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 hover:border-gray-200 ${
          isNew ? 'ring-2 ring-blue-500 ring-offset-2' : ''
        }`}
      >
        {/* 图片区域 - 可点击放大 */}
        {brief.image && (
          <div
            className="relative w-full h-56 overflow-hidden bg-gray-50 cursor-pointer"
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
            {/* 放大提示 */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6">
              <span className="text-white text-sm font-medium tracking-wide">
                查看大图
              </span>
            </div>
            {/* 分类标签叠加在图片上 */}
            <div className="absolute top-4 left-4">
              <span className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide backdrop-blur-xl shadow-lg ${colorClass}`}>
                {categoryName}
              </span>
            </div>
            {/* NEW标记 */}
            {isNew && (
              <div className="absolute top-4 right-4 bg-black text-white text-xs px-3 py-1.5 rounded-full font-medium shadow-lg">
                NEW
              </div>
            )}
          </div>
        )}

        {/* 内容区域 */}
        <div className="p-6">
          {/* 没有图片时显示分类和时间 */}
          {!brief.image && (
            <div className="flex items-center justify-between mb-4">
              <span className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide border ${colorClass}`}>
                {categoryName}
              </span>
              <div className="flex items-center text-gray-400 text-xs tracking-wide">
                <FaClock className="mr-1.5" />
                {formatDate(brief.created_at || brief.published)}
              </div>
            </div>
          )}

          {/* 朗读控制栏 */}
          <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-100">
            <div className="flex items-center gap-2">
              {/* 朗读按钮 */}
              {!isPlaying && !isPaused ? (
                <button
                  onClick={handleRead}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                >
                  <FaVolumeUp />
                  朗读
                </button>
              ) : isPaused ? (
                <button
                  onClick={handleRead}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                >
                  <FaPlay />
                  继续
                </button>
              ) : (
                <button
                  onClick={handlePause}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <FaPause />
                  暂停
                </button>
              )}

              {/* 停止按钮 */}
              {(isPlaying || isPaused) && (
                <button
                  onClick={handleStop}
                  className="px-3 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                >
                  停止
                </button>
              )}
            </div>

            {/* 声音选择器 */}
            <div className="relative">
              <button
                onClick={() => setShowVoiceSelector(!showVoiceSelector)}
                className="flex items-center gap-2 px-3 py-2 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <span>{voicesRef.current.find(v => v.name === selectedVoice)?.name?.split(' ')[0] || '选择声音'}</span>
                <FaTimes className={`transition-transform duration-200 ${showVoiceSelector ? 'rotate-45' : ''}`} />
              </button>

              {showVoiceSelector && voicesRef.current.length > 0 && (
                <div className="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-10 max-h-64 overflow-y-auto">
                  {voicesRef.current.map((voice, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSelectedVoice(voice.name);
                        setShowVoiceSelector(false);
                      }}
                      className={`w-full px-4 py-2.5 text-left text-xs hover:bg-gray-50 transition-colors ${
                        selectedVoice === voice.name ? 'bg-blue-50 text-blue-700' : 'text-gray-700'
                      }`}
                    >
                      {voice.name.split(' ').slice(0, 2).join(' ')}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* 标题 */}
          <h3 className="text-xl font-bold text-gray-900 mb-4 tracking-tight leading-tight group-hover:text-blue-600 transition-colors">
            {brief.title}
          </h3>

          {/* 摘要 - 自然段落格式 */}
          <div className="text-gray-700 mb-6 text-sm leading-[1.8] tracking-wide">
            {formatSummary(brief.summary)}
          </div>

          {/* 底部 - 来源和时间 */}
          <div className="flex items-center justify-between text-xs pt-4 border-t border-gray-100">
            <div className="flex items-center text-gray-400 tracking-wide">
              <FaLink className="mr-2" />
              <span className="truncate">{brief.source}</span>
            </div>
            {brief.image && (
              <div className="flex items-center text-gray-400 tracking-wide">
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
              className="mt-4 w-full flex items-center justify-center bg-gray-900 text-white px-6 py-3 rounded-xl hover:bg-gray-800 transition-colors text-sm font-medium tracking-wide"
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
