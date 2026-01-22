import React from 'react';
import {
  FaDollarSign,
  FaMicrochip,
  FaHeartbeat,
  FaLeaf,
  FaCar,
  FaRobot,
  FaBrain,
  FaGlobe
} from 'react-icons/fa';

const categoryIcons = {
  finance: { icon: FaDollarSign, color: 'text-green-600' },
  technology: { icon: FaMicrochip, color: 'text-blue-600' },
  health: { icon: FaHeartbeat, color: 'text-red-600' },
  new_energy: { icon: FaLeaf, color: 'text-yellow-600' },
  automotive: { icon: FaCar, color: 'text-purple-600' },
  robotics: { icon: FaRobot, color: 'text-indigo-600' },
  ai: { icon: FaBrain, color: 'text-pink-600' },
  general: { icon: FaGlobe, color: 'text-gray-600' }
};

const categoryNames = {
  finance: '财经',
  technology: '科技',
  health: '健康',
  new_energy: '新能源',
  automotive: '汽车',
  robotics: '机器人',
  ai: 'AI',
  general: '综合'
};

const CategoryFilter = ({ selectedCategory, onCategoryChange }) => {
  const categories = Object.keys(categoryNames);

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800">新闻分类</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        {/* 全部分类 */}
        <button
          onClick={() => onCategoryChange(null)}
          className={`flex flex-col items-center justify-center p-3 rounded-lg transition-all ${
            selectedCategory === null
              ? 'bg-primary text-white shadow-lg scale-105'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <FaGlobe className="text-2xl mb-2" />
          <span className="text-sm font-medium">全部</span>
        </button>

        {/* 各个分类 */}
        {categories.map((category) => {
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
              <Icon className={`text-2xl mb-2 ${isSelected ? 'text-white' : color}`} />
              <span className="text-sm font-medium">{categoryNames[category]}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default CategoryFilter;
