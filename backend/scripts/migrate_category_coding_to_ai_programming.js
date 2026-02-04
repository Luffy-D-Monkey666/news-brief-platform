/**
 * 数据迁移脚本：将 'coding_development' 分类迁移到 'ai_programming'
 *
 * 使用方法：
 * node backend/scripts/migrate_category_coding_to_ai_programming.js
 */

require('dotenv').config();
const mongoose = require('mongoose');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/news-brief';

async function migrateCodingCategory() {
  try {
    console.log('连接MongoDB...');
    await mongoose.connect(MONGODB_URI);
    console.log('MongoDB 已连接');

    // 直接使用collection，不使用model（避免schema验证失败）
    const db = mongoose.connection.db;
    const briefsCollection = db.collection('briefs');

    // 查找所有 coding_development 分类的文档
    const oldCategoryDocs = await briefsCollection.find({
      category: 'coding_development'
    }).toArray();

    console.log(`\n找到 ${oldCategoryDocs.length} 条 'coding_development' 分类的新闻`);

    if (oldCategoryDocs.length === 0) {
      console.log('无需迁移，程序退出');
      await mongoose.connection.close();
      return;
    }

    // 执行批量更新
    console.log('\n开始迁移...');
    const result = await briefsCollection.updateMany(
      { category: 'coding_development' },
      { $set: { category: 'ai_programming' } }
    );

    console.log(`\n迁移完成！`);
    console.log(`- 匹配文档数：${result.matchedCount}`);
    console.log(`- 修改文档数：${result.modifiedCount}`);

    // 验证迁移结果
    const remainingOldDocs = await briefsCollection.countDocuments({
      category: 'coding_development'
    });
    const newDocs = await briefsCollection.countDocuments({
      category: 'ai_programming'
    });

    console.log(`\n验证结果：`);
    console.log(`- 剩余 'coding_development'：${remainingOldDocs} 条（应为0）`);
    console.log(`- 新增 'ai_programming'：${newDocs} 条`);

    if (remainingOldDocs === 0) {
      console.log('\n✅ 迁移成功！所有数据已更新');
    } else {
      console.log('\n⚠️  警告：仍有数据未迁移完成');
    }

    await mongoose.connection.close();
    console.log('\n数据库连接已关闭');

  } catch (error) {
    console.error('❌ 迁移失败:', error);
    process.exit(1);
  }
}

// 执行迁移
migrateCodingCategory();
