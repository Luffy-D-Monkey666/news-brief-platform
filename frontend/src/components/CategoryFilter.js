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
  FaNewspaper,
  FaFilm,
  FaShip,
  FaTrophy
} from 'react-icons/fa';

const categoryIcons = {
  // 个人兴趣（最高优先级）
  op_card_game: { icon: FaTrophy, color: 'text-yellow-600', highlight: true, special: true },
  op_merchandise: { icon: FaShip, color: 'text-orange-600', highlight: true, special: true },

  // 核心关注领域
  ai_robotics: { icon: FaBrain, color: 'text-purple-600', highlight: true },
  ev_automotive: { icon: FaBolt, color: 'text-green-600', highlight: true },
  finance_investment: { icon: FaChartLine, color: 'text-red-600', highlight: true },

  // 主流新闻分类
  business_tech: { icon: FaMicrochip, color: 'text-blue-600' },
  politics_world: { icon: FaLandmark, color: 'text-indigo-600' },
  economy_policy: { icon: FaDollarSign, color: 'text-yellow-600' },
  health_medical: { icon: FaHeartbeat, color: 'text-pink-600' },
  energy_environment: { icon: FaLeaf, color: 'text-teal-600' },
  entertainment_sports: { icon: FaFilm, color: 'text-orange-600' },
  general: { icon: FaGlobe, color: 'text-gray-600' }
};

const categoryNames = {
  // 个人兴趣
  op_card_game: 'OP卡牌游戏',
  op_merchandise: 'OP周边情报',

  // 核心关注领域
  ai_robotics: 'AI与机器人',
  ev_automotive: '新能源汽车',
  finance_investment: '投资财经',

  // 主流新闻分类
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  general: '综合'
};

const CategoryFilter = ({ selectedCategory, onCategoryChange }) => {
  // 所有分类按顺序排列
  const allCategories = Object.keys(categoryNames);

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
        {allCategories.map((category) => {
          const { icon: Icon, color } = categoryIcons[category];
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
