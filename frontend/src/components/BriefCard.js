import React, { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  FaNewspaper,
  FaExternalLinkAlt,
  FaClock,
  FaLink,
  FaTimes
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

// 关键词高亮和链接组件
const HighlightedText = ({ text }) => {
  // 匹配专有名词、人名、地名、公司名、产品名等（大写字母开头的英文词或中文专有名词）
  const keywordPattern = /([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)*|特朗普|拜登|OpenAI|Tesla|DeepSeek|ChatGPT|GPT-\d+|Daniel\s+Naroditsky|Modi|DMK)/g;

  const parts = text.split(keywordPattern);

  return (
    <>
      {parts.map((part, index) => {
        if (part.match(keywordPattern)) {
          return (
            <a
              key={index}
              href={`https://gemini.google.com/app?q=${encodeURIComponent(part)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="keyword-link text-blue-600 hover:text-blue-800 border-b border-blue-300 border-dotted transition-all duration-200 hover:border-solid hover:animate-bounce-subtle"
              onClick={(e) => e.stopPropagation()}
            >
              {part}
            </a>
          );
        }
        return <span key={index}>{part}</span>;
      })}
    </>
  );
};

// 格式化摘要内容，添加结构化显示
const FormattedSummary = ({ summary }) => {
  // 解析不同部分
  const sections = {
    background: null,
    keyInfo: [],
    impact: null,
    data: []
  };

  // 提取【事件背景】
  const backgroundMatch = summary.match(/【事件背景】\s*([\s\S]*?)(?=【|$)/);
  if (backgroundMatch) {
    sections.background = backgroundMatch[1].trim();
  }

  // 提取【关键信息】
  const keyInfoMatch = summary.match(/【关键信息】\s*([\s\S]*?)(?=【|$)/);
  if (keyInfoMatch) {
    const infoText = keyInfoMatch[1].trim();
    sections.keyInfo = infoText
      .split(/\n/)
      .filter(line => line.trim() && line.includes('•'))
      .map(line => line.replace(/^[•\-\*]\s*/, '').trim());
  }

  // 提取【影响分析】
  const impactMatch = summary.match(/【影响分析】\s*([\s\S]*?)(?=【|$)/);
  if (impactMatch) {
    sections.impact = impactMatch[1].trim();
  }

  // 提取【相关数据】
  const dataMatch = summary.match(/【相关数据】\s*([\s\S]*?)$/);
  if (dataMatch) {
    const dataText = dataMatch[1].trim();
    sections.data = dataText
      .split(/\n/)
      .filter(line => line.trim() && line.includes('•'))
      .map(line => line.replace(/^[•\-\*]\s*/, '').trim());
  }

  return (
    <div className="space-y-4">
      {/* 事件背景 */}
      {sections.background && (
        <div className="bg-blue-50 p-3 rounded-lg border-l-4 border-blue-400">
          <h4 className="text-xs font-bold text-blue-700 mb-2">📋 事件背景</h4>
          <p className="text-sm text-gray-700 leading-relaxed">
            <HighlightedText text={sections.background} />
          </p>
        </div>
      )}

      {/* 关键信息 */}
      {sections.keyInfo.length > 0 && (
        <div className="bg-purple-50 p-3 rounded-lg border-l-4 border-purple-400">
          <h4 className="text-xs font-bold text-purple-700 mb-2">💡 关键信息</h4>
          <ul className="space-y-1.5">
            {sections.keyInfo.map((info, i) => (
              <li key={i} className="flex items-start text-sm text-gray-700">
                <span className="text-purple-500 mr-2 mt-0.5">▪</span>
                <span className="flex-1">
                  <HighlightedText text={info} />
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 影响分析 */}
      {sections.impact && (
        <div className="bg-green-50 p-3 rounded-lg border-l-4 border-green-400">
          <h4 className="text-xs font-bold text-green-700 mb-2">📊 影响分析</h4>
          <p className="text-sm text-gray-700 leading-relaxed">
            <HighlightedText text={sections.impact} />
          </p>
        </div>
      )}

      {/* 相关数据 */}
      {sections.data.length > 0 && (
        <div className="bg-orange-50 p-3 rounded-lg border-l-4 border-orange-400">
          <h4 className="text-xs font-bold text-orange-700 mb-2">📈 相关数据</h4>
          <ul className="space-y-1.5">
            {sections.data.map((datum, i) => (
              <li key={i} className="flex items-start text-sm text-gray-700">
                <span className="text-orange-500 mr-2 mt-0.5">▪</span>
                <span className="flex-1">
                  <HighlightedText text={datum} />
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 如果没有结构化内容，显示原文 */}
      {!sections.background && !sections.keyInfo.length && !sections.impact && !sections.data.length && (
        <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
          <HighlightedText text={summary} />
        </p>
      )}
    </div>
  );
};

// 图片放大Modal
const ImageModal = ({ src, alt, onClose }) => {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <button
        className="absolute top-4 right-4 text-white hover:text-gray-300 text-3xl"
        onClick={onClose}
      >
        <FaTimes />
      </button>
      <img
        src={src}
        alt={alt}
        className="max-w-full max-h-full object-contain"
        onClick={(e) => e.stopPropagation()}
      />
    </div>
  );
};

const BriefCard = ({ brief, isNew = false }) => {
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);
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
    <>
      <div
        className={`group bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-500 ${
          isNew ? 'animate-slide-in ring-2 ring-black' : ''
        }`}
      >
        {/* 图片区域 - 可点击放大 */}
        {brief.image && (
          <div
            className="relative w-full h-48 overflow-hidden bg-gray-100 cursor-pointer"
            onClick={() => setIsImageModalOpen(true)}
          >
            <img
              src={brief.image}
              alt={brief.title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
            {/* 放大提示 */}
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
              <span className="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-sm font-medium">
                点击查看大图
              </span>
            </div>
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

          {/* 标题 - 使用关键词高亮 */}
          <h3 className="text-lg font-bold text-gray-900 mb-4 group-hover:text-black transition-colors">
            <HighlightedText text={brief.title} />
          </h3>

          {/* 摘要 - 结构化显示 */}
          <FormattedSummary summary={brief.summary} />

          {/* 底部 - 来源和时间 */}
          <div className="flex items-center justify-between text-xs border-t pt-3 mt-4">
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
