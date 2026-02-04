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
      'tcg_card_game',        // TCG卡牌游戏（PTCG宝可梦、OPCG海贼王、DBTCG龙珠等）
      'one_piece',            // 海贼王相关（One Piece所有内容）
      'anime_manga',          // 日本动画漫画
      'ai_robotics',          // AI与机器人
      'ev_automotive',        // 新能源汽车
      'finance_investment',   // 投资财经
      'business_tech',        // 商业科技
      'politics_world',       // 政治国际
      'economy_policy',       // 经济政策
      'health_medical',       // 健康医疗
      'energy_environment',   // 能源环境
      'entertainment_sports', // 娱乐体育
      'general'              // 综合
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
