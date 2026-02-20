import React from 'react';
import {
  FaDollarSign,
  FaMicrochip,
  FaHeartbeat,
  FaLeaf,
  FaCar,
  FaRobot,
  FaBrain,
  FaGlobe,
  FaChartLine,
  FaBolt,
  FaLandmark,
  FaFilm,
  FaCode,
  FaMobileAlt,
  FaShip,
  FaLayerGroup,  // TCG卡牌图标
  FaPlay         // 动漫图标
} from 'react-icons/fa';

// 分类图标和颜色配置 - 收敛到5个主色调
// Blue: 科技类 | Green: 财经/商业类 | Orange: 娱乐/兴趣类 | Gray: 中性/综合类
const categoryIcons = {
  // 科技类 - Blue
  ai_technology: { icon: FaBrain, color: 'text-blue-600' },
  robotics: { icon: FaRobot, color: 'text-blue-600' },
  ai_programming: { icon: FaCode, color: 'text-blue-600' },
  semiconductors: { icon: FaMicrochip, color: 'text-blue-600' },
  automotive: { icon: FaCar, color: 'text-blue-600' },
  consumer_electronics: { icon: FaMobileAlt, color: 'text-blue-600' },
  
  // 财经/商业/政经类 - Green
  finance_investment: { icon: FaChartLine, color: 'text-green-600' },
  business_tech: { icon: FaBolt, color: 'text-green-600' },
  politics_world: { icon: FaLandmark, color: 'text-green-600' },
  economy_policy: { icon: FaDollarSign, color: 'text-green-600' },
  
  // 生活/健康类 - Gray
  health_medical: { icon: FaHeartbeat, color: 'text-gray-700' },
  energy_environment: { icon: FaLeaf, color: 'text-gray-700' },
  
  // 娱乐/兴趣类 - Orange
  entertainment_sports: { icon: FaFilm, color: 'text-orange-600' },
  anime: { icon: FaPlay, color: 'text-orange-600' },
  one_piece: { icon: FaShip, color: 'text-orange-600' },
  tcg: { icon: FaLayerGroup, color: 'text-orange-600' },
  
  // 综合 - Gray
  general: { icon: FaGlobe, color: 'text-gray-500' }
};

// 分类中文名称（按显示顺序）
const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编码与智能体',
  semiconductors: '芯片',
  automotive: '汽车',
  consumer_electronics: '消费电子',
  // podcasts 已移除
  finance_investment: '投资财经',
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  anime: '动漫二次元',
  one_piece: 'OP',
  tcg: 'TCG',
  general: '综合'
};

// 分类顺序（podcasts 已移除）
const categoryOrder = [
  'ai_technology',
  'robotics', 
  'ai_programming',
  'semiconductors',
  'automotive',
  'consumer_electronics',
  // 'podcasts' 已移除
  'finance_investment',
  'business_tech',
  'politics_world',
  'economy_policy',
  'health_medical',
  'energy_environment',
  'entertainment_sports',
  'anime',
  'one_piece',
  'tcg',
  'general'
];

const CategoryFilter = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="bg-white/80 backdrop-blur-sm shadow-sm rounded-2xl p-6 mb-8">
      {/* 全部分类按钮 */}
      <div className="mb-6">
        <button
          onClick={() => onCategoryChange(null)}
          className={`w-full flex items-center justify-center px-6 py-3 rounded-xl transition-all font-medium ${
            selectedCategory === null
              ? 'bg-black text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <FaGlobe className="text-xl mr-2" />
          <span>全部分类</span>
        </button>
      </div>

      {/* 所有分类统一展示 */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {categoryOrder.map((category) => {
          const iconConfig = categoryIcons[category];
          if (!iconConfig) return null;
          
          const { icon: Icon, color } = iconConfig;
          const isSelected = selectedCategory === category;

          return (
            <button
              key={category}
              onClick={() => onCategoryChange(category)}
              className={`flex flex-col items-center justify-center p-4 rounded-xl transition-all ${
                isSelected
                  ? 'bg-black text-white shadow-lg scale-105'
                  : 'bg-gray-50 hover:bg-gray-100 hover:shadow-md'
              }`}
            >
              <Icon className={`text-3xl mb-2 ${isSelected ? 'text-white' : color}`} />
              <span className="text-xs font-medium text-center">{categoryNames[category]}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default CategoryFilter;
