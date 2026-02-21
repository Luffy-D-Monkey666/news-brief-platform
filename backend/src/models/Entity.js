const mongoose = require('mongoose');

// 基础时间线事件 Schema
const baseTimelineSchema = new mongoose.Schema({
  date: { type: String, required: true },  // "2003" 或 "2008.02"
  event: { type: String, required: true },
  importance: {
    type: String,
    enum: ['milestone', 'major', 'normal'],
    default: 'normal'
  }
}, { _id: false });

// 实体元数据 Schema
const entityMetadataSchema = new mongoose.Schema({
  founded: String,      // 成立时间
  founder: String,      // 创始人
  headquarters: String, // 总部
  industry: String,     // 行业
  website: String,      // 官网
  ticker: String,       // 股票代码
  // 人物特有
  birth_date: String,
  nationality: String,
  title: String,        // 职位
  // 事件特有
  start_date: String,
  end_date: String,
  location: String
}, { _id: false });

// 主实体 Schema
const entitySchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  aliases: {
    type: [String],
    default: []
  },
  type: {
    type: String,
    enum: ['company', 'person', 'event', 'concept', 'product'],
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  image: {
    type: String,
    default: null
  },
  metadata: {
    type: entityMetadataSchema,
    default: {}
  },
  base_timeline: {
    type: [baseTimelineSchema],
    default: []
  },
  // 统计信息
  news_count: {
    type: Number,
    default: 0
  },
  last_news_at: {
    type: Date,
    default: null
  },
  // 是否为预置实体（手动添加的热门实体）
  is_preset: {
    type: Boolean,
    default: false
  },
  // 是否已激活（达到提及阈值后激活，用于非预置实体）
  is_active: {
    type: Boolean,
    default: false
  },
  // 提及次数（未创建知识库前的计数）
  mention_count: {
    type: Number,
    default: 0
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  updated_at: {
    type: Date,
    default: Date.now
  }
});

// 索引
entitySchema.index({ type: 1 });
entitySchema.index({ news_count: -1 });
entitySchema.index({ aliases: 1 });
entitySchema.index({ name: 'text', aliases: 'text', description: 'text' });

// 更新时自动更新 updated_at
entitySchema.pre('save', function(next) {
  this.updated_at = new Date();
  next();
});

module.exports = mongoose.model('Entity', entitySchema);
