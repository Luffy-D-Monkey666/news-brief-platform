const mongoose = require('mongoose');

const briefSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: true
  },
  category: {
    type: String,
    required: true,
    enum: [
      'ai_technology',         // AI技术（机器学习、大语言模型、AI应用）
      'embodied_intelligence', // 具身智能（机器人、自动驾驶、物理世界AI）
      'ai_programming',        // AI编程（AI编程助手、传统开发工具、开源项目）
      'ev_automotive',         // 新能源汽车
      'finance_investment',    // 投资财经
      'business_tech',         // 商业科技
      'politics_world',        // 政治国际
      'economy_policy',        // 经济政策
      'health_medical',        // 健康医疗
      'energy_environment',    // 能源环境
      'entertainment_sports',  // 娱乐体育
      'general'               // 综合
    ]
  },
  source: {
    type: String,
    required: true
  },
  source_url: {
    type: String
  },
  link: {
    type: String,
    required: true
  },
  image: {
    type: String,
    default: null
  },
  published: {
    type: Date,
    default: Date.now
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  is_pushed: {
    type: Boolean,
    default: false
  },
  pushed_at: {
    type: Date
  }
});

// 创建索引
briefSchema.index({ created_at: -1 });
briefSchema.index({ category: 1 });
briefSchema.index({ is_pushed: 1 });

module.exports = mongoose.model('Brief', briefSchema);
