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
  // One Piece 个人兴趣（顶部特殊显示）
  const onePieceCategories = ['op_card_game', 'op_merchandise'];
  // 核心关注领域
  const highlightCategories = ['ai_robotics', 'ev_automotive', 'finance_investment'];
  // 其他分类
  const otherCategories = Object.keys(categoryNames).filter(
    cat => !onePieceCategories.includes(cat) && !highlightCategories.includes(cat)
  );

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      {/* 全部分类按钮 */}
      <div className="mb-4">
        <button
          onClick={() => onCategoryChange(null)}
          className={`flex items-center justify-center px-6 py-3 rounded-lg transition-all font-medium ${
            selectedCategory === null
              ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg scale-105'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <FaGlobe className="text-xl mr-2" />
          <span>全部</span>
        </button>
      </div>

      {/* One Piece 个人兴趣 - 顶级优先 */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-500 mb-3 flex items-center">
          <span className="bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 text-white px-3 py-1 rounded-full text-xs mr-2 animate-pulse">
            ⚡ ONE PIECE 专区
          </span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {onePieceCategories.map((category) => {
            const { icon: Icon, color } = categoryIcons[category];
            const isSelected = selectedCategory === category;

            return (
              <button
                key={category}
                onClick={() => onCategoryChange(category)}
                className={`flex items-center justify-center p-5 rounded-xl transition-all font-bold text-lg ${
                  isSelected
                    ? 'bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 text-white shadow-2xl scale-110 ring-4 ring-yellow-300 animate-pulse'
                    : 'bg-gradient-to-br from-yellow-50 to-orange-50 hover:shadow-xl hover:scale-105 border-3 border-yellow-300'
                }`}
              >
                <Icon className={`text-4xl mr-3 ${isSelected ? 'text-white' : color}`} />
                <span className={`${isSelected ? 'text-white' : 'text-gray-900'}`}>
                  {categoryNames[category]}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 核心关注领域 */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-500 mb-3 flex items-center">
          <span className="bg-gradient-to-r from-red-500 to-pink-500 text-white px-2 py-1 rounded text-xs mr-2">
            ★ 重点关注
          </span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {highlightCategories.map((category) => {
            const { icon: Icon, color } = categoryIcons[category];
            const isSelected = selectedCategory === category;

            return (
              <button
                key={category}
                onClick={() => onCategoryChange(category)}
                className={`flex items-center justify-center p-4 rounded-lg transition-all font-medium ${
                  isSelected
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-xl scale-105 ring-4 ring-purple-200'
                    : 'bg-gradient-to-br from-gray-50 to-gray-100 hover:shadow-lg hover:scale-102 border-2 border-gray-200'
                }`}
              >
                <Icon className={`text-3xl mr-3 ${isSelected ? 'text-white' : color}`} />
                <span className={`text-base ${isSelected ? 'text-white' : 'text-gray-800'}`}>
                  {categoryNames[category]}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 其他分类 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-500 mb-3">其他分类</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
          {otherCategories.map((category) => {
            const { icon: Icon, color } = categoryIcons[category];
            const isSelected = selectedCategory === category;

            return (
              <button
                key={category}
                onClick={() => onCategoryChange(category)}
                className={`flex flex-col items-center justify-center p-3 rounded-lg transition-all ${
                  isSelected
                    ? 'bg-primary text-white shadow-lg scale-105'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                <Icon className={`text-2xl mb-1 ${isSelected ? 'text-white' : color}`} />
                <span className="text-xs font-medium">{categoryNames[category]}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default CategoryFilter;
