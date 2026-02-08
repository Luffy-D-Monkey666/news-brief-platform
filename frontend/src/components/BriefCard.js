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
  FaPlay,
  FaTwitter,
  FaYoutube,
  FaWeixin,
  FaRobot
} from 'react-icons/fa';

// Apple风格配色（更简洁清爽）
const categoryColors = {
  ai_technology: 'text-purple-600',
  robotics: 'text-indigo-600',
  ai_coding_agent: 'text-blue-600',
  anime_otaku: 'text-pink-500',
  semiconductors: 'text-gray-700',
  opcg: 'text-orange-600',
  automotive: 'text-emerald-600',
  consumer_electronics: 'text-cyan-600',
  one_piece: 'text-red-600',
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
  ai_coding_agent: 'AI编码与智能体',
  anime_otaku: '动漫二次元',
  semiconductors: '芯片',
  opcg: 'OPCG',
  automotive: '汽车',
  consumer_electronics: '消费电子',
  one_piece: 'OP',
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

// 声音预设配置
const voicePresets = {
  siri_female: { pitch: 1.0, rate: 1.0, name: 'Siri (女声)' },
  siri_male: { pitch: 0.9, rate: 1.0, name: 'Siri (男声)' },
  // AI语音模拟
  xiao_ai: { pitch: 1.05, rate: 1.02, name: '小爱同学 (小米)' },  // 活泼、阳光、友好，年轻女声
  ideal_assistant: { pitch: 0.95, rate: 0.98, name: '理想同学 (理想汽车)' },  // 温暖、有亲和力、稍成熟女声
  nomi: { pitch: 0.92, rate: 1.0, name: 'NOMI (蔚来)' }  // 温柔、有温度、自然感
};

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
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState('siri_female');
  const [showVoiceMenu, setShowVoiceMenu] = useState(false);
  const [videoError, setVideoError] = useState(false);

  const speechSynthesisRef = useRef(window.speechSynthesis);
  const utteranceRef = useRef(null);
  const allVoicesRef = useRef([]);
  const currentVoiceRef = useRef(null);

  // 组件卸载时停止所有语音播放
  useEffect(() => {
    return () => {
      if (speechSynthesisRef.current) {
        speechSynthesisRef.current.cancel();
      }
    };
  }, []);

  // 只保留5种中文声音预设
  useEffect(() => {
    const loadVoices = () => {
      const allVoices = speechSynthesisRef.current.getVoices();

      // 打印所有语音到控制台（便于调试）
      console.log('=== 所有可用语音 ===');
      allVoices.forEach(v => console.log(`${v.name} (${v.lang})`));

      // 只保留中文声音
      const zhVoices = allVoices.filter(voice =>
        voice.lang === 'zh-CN' || voice.lang === 'zh'
      );

      console.log('=== 可用的中文语音 ===');
      zhVoices.forEach(v => console.log(`- ${v.name}`));

      // 为每个预设分配不同的声音
      // Siri女声 - 优先Ting-Ting
      const siriFemale = zhVoices.find(v =>
        v.name.includes('Ting-Ting') || v.name.includes('Huihui') || v.name.includes('Xiaoxiao')
      );

      // Siri男声 - 优先Kangkang
      const siriMale = zhVoices.find(v =>
        v.name.includes('Kangkang') || v.name.includes('Yunxi') || v.name.includes('Yaqi')
      );

      // 小爱同学（小米）- 活泼、阳光、友好的年轻女声
      const xiaoAiVoice = zhVoices.find(v =>
        v.name.includes('Xiaoxiao') || v.name.includes('Yaoyao')
      ) || siriFemale;

      // 理想同学（理想汽车）- 温暖、有亲和力、稍成熟的女声
      const idealVoice = zhVoices.find(v =>
        v.name.includes('Huihui') || v.name.includes('Xiaoyi') || v.name.includes('Lili')
      ) || siriFemale;

      // NOMI（蔚来）- 温柔、有温度、自然感的语音
      const nomiVoice = zhVoices.find(v =>
        v.name.includes('Xiaoyi') || v.name.includes('Yaoyao') || v.name.includes('Xiaoxiao')
      ) || siriFemale;

      // 声音预设映射
      const voiceMap = {
        siri_female: siriFemale || zhVoices[0],
        siri_male: siriMale || zhVoices[1] || zhVoices[0],
        xiao_ai: xiaoAiVoice || zhVoices[2] || siriFemale,
        ideal_assistant: idealVoice || zhVoices[3] || siriFemale,
        nomi: nomiVoice || zhVoices[4] || siriFemale
      };

      currentVoiceRef.current = voiceMap[selectedPreset];
      allVoicesRef.current = voiceMap;

      // 将可用语音保存到全局，供调试使用
      window.availableZhVoices = zhVoices;
    };

    speechSynthesisRef.current.onvoiceschanged = loadVoices;
    loadVoices();

    return () => {
      speechSynthesisRef.current.cancel();
    };
  }, [selectedPreset]);

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

    // 设置声音
    if (currentVoiceRef.current) {
      utterance.voice = currentVoiceRef.current;
    }

    // 应用声音预设的语调和语速
    const preset = voicePresets[selectedPreset];
    utterance.pitch = preset.pitch;
    utterance.rate = preset.rate;

    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    utterance.onerror = (e) => {
      console.error('Speech error:', e);
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

  // 格式化摘要为三段式结构
  const formatSummary = (text) => {
    const sections = {
      overview: null,
      details: [],
      impact: null
    };

    // 提取"事件概述"
    const overviewMatch = text.match(/事件概述[:：]\s*([\s\S]*?)(?=重要细节|后续影响|$)/);
    if (overviewMatch) {
      sections.overview = overviewMatch[1].trim();
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
      details: sections.details,
      impact: sections.impact
    };
  };

  const summary = formatSummary(brief.summary);

  return (
    <>
      <div
        className={`group bg-white rounded-2xl overflow-hidden border border-gray-200/60 shadow-sm hover:shadow-xl transition-all duration-300 hover:border-gray-300 hover:-translate-y-1 ${
          isNew ? 'ring-2 ring-blue-500 ring-offset-2 animate-pulse-once' : ''
        }`}
      >
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
            <div className="absolute top-4 left-4">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
            </div>
          </div>
        ) : (brief.video && videoError && brief.image) ? (
          // 视频加载失败，降级显示图片
          <div
            className="relative w-full h-52 overflow-hidden bg-gray-100 cursor-pointer"
            onClick={() => setIsImageModalOpen(true)}
          >
            <img
              src={brief.image}
              alt={brief.title}
              loading="lazy"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
              <span className="text-white text-sm font-medium">查看大图</span>
            </div>
            <div className="absolute top-4 left-4 flex flex-col gap-2">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
              <span className="px-3 py-1.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700 backdrop-blur-md">
                视频加载失败
              </span>
            </div>
          </div>
        ) : (brief.video && videoError && !brief.image) ? (
          // 视频和图片都不可用，显示占位符
          <div className="relative w-full h-52 overflow-hidden bg-gray-100 flex items-center justify-center">
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p className="text-sm text-gray-500">媒体内容无法加载</p>
            </div>
            <div className="absolute top-4 left-4">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
            </div>
          </div>
        ) : brief.image ? (
          // 只有图片
          <div
            className="relative w-full h-52 overflow-hidden bg-gray-100 cursor-pointer"
            onClick={() => setIsImageModalOpen(true)}
          >
            <img
              src={brief.image}
              alt={brief.title}
              loading="lazy"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
              onError={(e) => {
                e.target.parentElement.innerHTML = `
                  <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
                    <div class="text-center">
                      <svg class="mx-auto h-10 w-10 text-gray-300 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>`;
              }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
              <span className="text-white text-sm font-medium">查看大图</span>
            </div>
            <div className="absolute top-4 left-4">
              <span className={`px-3 py-1.5 rounded-full text-xs font-medium bg-white/90 backdrop-blur-md ${colorClass}`}>
                {categoryName}
              </span>
            </div>
          </div>
        ) : null}

        {/* 内容区域 */}
        <div className="p-5 space-y-1">
          {/* 没有视频和图片时的分类标签 */}
          {!brief.video && !brief.image && (
            <div className="flex items-center justify-between mb-3">
              <span className={`text-xs font-semibold ${colorClass}`}>
                {categoryName}
              </span>
              <div className="flex items-center text-gray-400 text-xs">
                <FaClock className="mr-1.5" />
                {formatDate(brief.created_at || brief.published)}
              </div>
            </div>
          )}

          {/* 朗读控制栏 */}
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              {!isPlaying && !isPaused ? (
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
                  onClick={handlePause}
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

            {/* 声音选择器 */}
            <div className="relative">
              <button
                onClick={() => setShowVoiceMenu(!showVoiceMenu)}
                className="flex items-center gap-2 px-3 py-2 text-xs text-gray-600 hover:text-gray-900 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <span className="font-medium">{voicePresets[selectedPreset].name}</span>
              </button>

              {showVoiceMenu && (
                <div className="absolute right-0 top-full mt-2 w-40 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-10">
                  {Object.entries(voicePresets).map(([key, preset]) => (
                    <button
                      key={key}
                      onClick={() => {
                        setSelectedPreset(key);
                        setShowVoiceMenu(false);
                      }}
                      className={`w-full px-4 py-2 text-left text-sm hover:bg-gray-50 transition-colors ${
                        selectedPreset === key ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
                      }`}
                    >
                      {preset.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* 标题 */}
          <h3 className="text-lg font-semibold text-gray-900 mb-4 leading-snug">
            {brief.title}
          </h3>

          {/* 摘要 - 结构化显示（增加间距和虚线） */}
          {summary.hasStructure ? (
            <div className="space-y-6 mb-5">
              {/* 事件概述 */}
              {summary.overview && (
                <div>
                  <div className="flex items-center gap-2 mb-4 pb-2 border-b-2 border-dashed border-gray-200">
                    <div className="w-2 h-5 rounded-full bg-gradient-to-b from-blue-400 to-blue-600" />
                    <span className="text-sm font-bold text-gray-700 tracking-wide">事件概述</span>
                  </div>
                  <p className="text-sm text-gray-800 leading-relaxed pl-5">
                    {summary.overview}
                  </p>
                </div>
              )}

              {/* 重要细节 */}
              {summary.details.length > 0 && (
                <div className={summary.overview ? "" : "mt-2"}>
                  <div className="flex items-center gap-2 mb-4 pb-2 border-b-2 border-dashed border-gray-200">
                    <div className="w-2 h-5 rounded-full bg-gradient-to-b from-purple-400 to-purple-600" />
                    <span className="text-sm font-bold text-gray-700 tracking-wide">重要细节</span>
                  </div>
                  <ul className="space-y-3 pl-5">
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
                <div className="mt-6">
                  <div className="flex items-center gap-2 mb-4 pb-2 border-b-2 border-dashed border-gray-200">
                    <div className="w-2 h-5 rounded-full bg-gradient-to-b from-green-400 to-green-600" />
                    <span className="text-sm font-bold text-gray-700 tracking-wide">后续影响</span>
                  </div>
                  <p className="text-sm text-gray-800 leading-relaxed pl-5">
                    {summary.impact}
                  </p>
                </div>
              )}
            </div>
          ) : (
            // 非结构化摘要
            <div className="mb-5 p-4 bg-gray-50 rounded-xl text-sm text-gray-800 leading-relaxed whitespace-pre-line">
              {brief.summary}
            </div>
          )}

          {/* 底部信息 */}
          <div className="flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-100">
            <div className="flex items-center max-w-[60%]">
              <FaLink className="mr-1.5 flex-shrink-0" />
              <span className="truncate">{brief.source}</span>
              {/* 来源类型标识 */}
              {brief.source_type === 'twitter' && (
                <span className="ml-2 px-1.5 py-0.5 bg-blue-50 text-blue-500 rounded text-[10px] flex items-center">
                  <FaTwitter className="mr-0.5" /> X
                </span>
              )}
              {brief.source_type === 'weibo' && (
                <span className="ml-2 px-1.5 py-0.5 bg-red-50 text-red-500 rounded text-[10px]">
                  微博
                </span>
              )}
              {brief.source_type === 'youtube' && (
                <span className="ml-2 px-1.5 py-0.5 bg-red-50 text-red-600 rounded text-[10px] flex items-center">
                  <FaYoutube className="mr-0.5" /> 
                </span>
              )}
              {brief.source_type === 'wechat' && (
                <span className="ml-2 px-1.5 py-0.5 bg-green-50 text-green-600 rounded text-[10px] flex items-center">
                  <FaWeixin className="mr-0.5" /> 公众号
                </span>
              )}
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
