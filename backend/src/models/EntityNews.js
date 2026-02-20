const mongoose = require('mongoose');

// 实体-新闻关联 Schema
const entityNewsSchema = new mongoose.Schema({
  entity_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Entity',
    required: true,
    index: true
  },
  brief_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Brief',
    required: true,
    index: true
  },
  // 新闻日期（用于时间轴分组）
  date: {
    type: String,  // "2025-01-15"
    required: true,
    index: true
  },
  // 新闻分类
  category: {
    type: String,
    required: true
  },
  // 与实体的关联描述
  relevance: {
    type: String,
    default: ''
  },
  created_at: {
    type: Date,
    default: Date.now
  }
});

// 复合索引：按实体和日期查询
entityNewsSchema.index({ entity_id: 1, date: -1 });
// 防止重复关联
entityNewsSchema.index({ entity_id: 1, brief_id: 1 }, { unique: true });

module.exports = mongoose.model('EntityNews', entityNewsSchema);
