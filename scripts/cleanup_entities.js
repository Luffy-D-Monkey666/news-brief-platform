#!/usr/bin/env node
/**
 * 清理来自娱乐/动漫/OP/TCG分类的非预置实体
 */

const mongoose = require('mongoose');
require('dotenv').config({ path: require('path').join(__dirname, '../backend/.env') });

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/newshub';

// Entity Schema
const entitySchema = new mongoose.Schema({
  name: String,
  type: String,
  is_preset: Boolean,
  news_count: Number,
  description: String
});
const Entity = mongoose.model('Entity', entitySchema);

// 预置实体名单（不删除）
const PRESET_NAMES = new Set([
  '特斯拉', 'OpenAI', '苹果', '英伟达', '谷歌', '微软', 'Meta', '亚马逊',
  '字节跳动', '腾讯', '阿里巴巴', '百度', '华为', '小米', '比亚迪',
  'Anthropic', 'DeepMind', 'xAI', 'Mistral AI', '智谱AI', '月之暗面',
  'MiniMax', '零一万物', '深度求索', 'Stability AI',
  'AMD', '英特尔', '台积电', '高通', 'ARM',
  '马斯克', 'Sam Altman', '黄仁勋', '蒂姆·库克', '萨蒂亚·纳德拉',
  '马克·扎克伯格', '李彦宏', '雷军', '王传福', 'Dario Amodei',
  'GPT', '大模型', 'AGI', 'Transformer', 'FSD', '量子计算', '芯片制程', '智能体',
  '中美贸易', '俄乌冲突', '巴以冲突', '加密货币监管', 'AI监管'
]);

async function cleanup() {
  console.log('🔗 连接数据库...');
  await mongoose.connect(MONGODB_URI);
  console.log('✅ 已连接\n');

  // 查找所有非预置实体
  const entities = await Entity.find({ is_preset: { $ne: true } });
  console.log(`📊 找到 ${entities.length} 个非预置实体\n`);

  let deleted = 0;
  for (const entity of entities) {
    // 跳过预置名单
    if (PRESET_NAMES.has(entity.name)) {
      continue;
    }
    
    // 删除 news_count 为 0 的实体（说明没有关联到任何新闻）
    if (!entity.news_count || entity.news_count === 0) {
      console.log(`🗑️  删除: ${entity.name} (${entity.type})`);
      await Entity.deleteOne({ _id: entity._id });
      deleted++;
    }
  }

  console.log(`\n✅ 清理完成，删除了 ${deleted} 个无用实体`);
  
  // 统计剩余
  const remaining = await Entity.countDocuments();
  console.log(`📊 剩余 ${remaining} 个实体`);

  await mongoose.disconnect();
}

cleanup().catch(console.error);
