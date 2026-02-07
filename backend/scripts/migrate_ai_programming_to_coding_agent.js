/**
 * 数据迁移脚本：将 'ai_programming' 分类迁移到 'ai_coding_agent'
 * 
 * 使用方法：
 * node backend/scripts/migrate_ai_programming_to_coding_agent.js
 */

const mongoose = require('mongoose');
const Brief = require('../src/models/Brief');
require('dotenv').config();

async function migrate() {
  try {
    // 连接数据库
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ 数据库连接成功');

    // 查找所有 ai_programming 分类的新闻
    const oldNews = await Brief.find({ category: 'ai_programming' });
    console.log(`找到 ${oldNews.length} 条 ai_programming 分类的新闻`);

    if (oldNews.length === 0) {
      console.log('✅ 没有需要迁移的数据');
      process.exit(0);
    }

    // 更新分类
    const result = await Brief.updateMany(
      { category: 'ai_programming' },
      { $set: { category: 'ai_coding_agent' } }
    );

    console.log(`✅ 迁移完成！更新了 ${result.modifiedCount} 条新闻`);
    
    // 验证迁移结果
    const verifyCount = await Brief.countDocuments({ category: 'ai_coding_agent' });
    console.log(`✅ 验证：现在有 ${verifyCount} 条 ai_coding_agent 分类的新闻`);
    
    const oldCount = await Brief.countDocuments({ category: 'ai_programming' });
    console.log(`✅ 验证：剩余 ${oldCount} 条 ai_programming 分类的新闻`);

    process.exit(0);
  } catch (error) {
    console.error('❌ 迁移失败:', error);
    process.exit(1);
  }
}

migrate();
