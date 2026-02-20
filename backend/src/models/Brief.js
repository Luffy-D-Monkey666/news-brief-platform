const mongoose = require('mongoose');

// 从共享配置读取分类（如果需要动态加载）
const VALID_CATEGORIES = [
  'ai_technology', 'robotics', 'ai_programming', 'semiconductors',
  'automotive', 'consumer_electronics', 'podcasts', 'finance_investment',
  'business_tech', 'politics_world', 'economy_policy', 'health_medical',
  'energy_environment', 'entertainment_sports', 'anime', 'one_piece',
  'tcg', 'general', 'opcg'  // opcg 为兼容旧数据
];

// 关键指标 Schema
const keyMetricSchema = new mongoose.Schema({
  name: String,
  value: mongoose.Schema.Types.Mixed,
  unit: String,
  entity: String
}, { _id: false });

// 时间线事件 Schema
const timelineEventSchema = new mongoose.Schema({
  date: String,
  event: String
}, { _id: false });

// 背景知识 Schema
const backgroundSchema = new mongoose.Schema({
  context: String,
  timeline: [timelineEventSchema]
}, { _id: false });

// 技术解读 Schema
const techInsightSchema = new mongoose.Schema({
  principle: String,
  comparison: String,
  maturity: {
    type: String,
    enum: ['实验室阶段', '小规模试用', '商用落地', '大规模应用']
  }
}, { _id: false });

// 融资轮次 Schema
const fundingRoundSchema = new mongoose.Schema({
  round: String,
  amount: String,
  date: String,
  investors: [String]
}, { _id: false });

// 融资历史 Schema
const fundingHistorySchema = new mongoose.Schema({
  company: String,
  rounds: [fundingRoundSchema],
  total_funding: String,
  valuation: String
}, { _id: false });

// 关联公司 Schema
const relatedCompanySchema = new mongoose.Schema({
  name: String,
  role: String,
  effect: {
    type: String,
    enum: ['利好', '利空', '中性']
  }
}, { _id: false });

// 供应链视角 Schema
const supplyChainInsightSchema = new mongoose.Schema({
  impact: String,
  related_companies: [relatedCompanySchema],
  capacity_info: String
}, { _id: false });

// 实体时间线事件 Schema
const entityTimelineSchema = new mongoose.Schema({
  date: String,
  event: String
}, { _id: false });

// 关键实体 Schema
const entitySchema = new mongoose.Schema({
  name: { type: String, required: true },
  type: {
    type: String,
    enum: ['company', 'person', 'tech', 'concept', 'event'],
    default: 'concept'
  },
  context: String,
  relevance: String,
  timeline: [entityTimelineSchema]
}, { _id: false });

// 股票信息 Schema
const stockInfoSchema = new mongoose.Schema({
  ticker: String,
  name: String,
  price: Number,
  change: Number,
  change_percent: Number,
  change_formatted: String,
  market_cap: Number,
  market_cap_formatted: String,
  pe_ratio: Number,
  currency: String
}, { _id: false });

// 主 Brief Schema
const briefSchema = new mongoose.Schema({
  // 基础字段
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
    enum: VALID_CATEGORIES
  },
  
  // 来源信息
  source: {
    type: String,
    required: true
  },
  source_url: String,
  source_tier: {
    type: String,
    enum: ['official', 'mainstream', 'specialized', 'community'],
    default: 'community'
  },
  link: {
    type: String,
    required: true
  },
  
  // 媒体
  image: {
    type: String,
    default: null
  },
  video: {
    type: String,
    default: null
  },
  
  // 重要性与建议
  importance: {
    type: String,
    enum: ['breaking', 'high', 'normal'],
    default: 'normal'
  },
  action_advice: {
    type: String,
    default: null
  },
  
  // 结构化数据
  key_metrics: {
    type: [keyMetricSchema],
    default: []
  },
  background: {
    type: backgroundSchema,
    default: null
  },
  tech_insight: {
    type: techInsightSchema,
    default: null
  },
  funding_history: {
    type: fundingHistorySchema,
    default: null
  },
  supply_chain_insight: {
    type: supplyChainInsightSchema,
    default: null
  },
  entities: {
    type: [entitySchema],
    default: []
  },
  stock_info: {
    type: stockInfoSchema,
    default: null
  },
  
  // 话题关联
  topic_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Topic',
    default: null
  },
  
  // 时间戳
  published: {
    type: Date,
    default: Date.now
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  
  // 推送状态
  is_pushed: {
    type: Boolean,
    default: false
  },
  pushed_at: Date
});

// 索引
briefSchema.index({ created_at: -1 });
briefSchema.index({ category: 1, created_at: -1 });
briefSchema.index({ importance: 1, created_at: -1 });
briefSchema.index({ is_pushed: 1 });
briefSchema.index({ topic_id: 1 });
briefSchema.index({ link: 1 }, { unique: true });

module.exports = mongoose.model('Brief', briefSchema);
