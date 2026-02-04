/**
 * MongoDB数据迁移脚本：ev_automotive → automotive
 *
 * 用途：将所有 ev_automotive 分类的新闻改为 automotive
 *
 * 使用方法：
 * 1. 本地测试（推荐）：
 *    node scripts/migrate_ev_to_automotive.js
 *
 * 2. 或直接在MongoDB Atlas执行（Web界面）：
 *    - 访问 https://cloud.mongodb.com/
 *    - 选择数据库 news-brief
 *    - 点击 Collections → briefs
 *    - 点击 Aggregation 标签
 *    - 复制下面的更新命令执行
 */

const mongoose = require('mongoose');
require('dotenv').config();

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/news-brief';

async function migrate() {
  try {
    console.log('🔗 连接到MongoDB...');
    console.log(`📍 URI: ${MONGODB_URI.replace(/:[^:]*@/, ':****@')}`); // 隐藏密码

    await mongoose.connect(MONGODB_URI);
    console.log('✅ MongoDB连接成功\n');

    const db = mongoose.connection.db;
    const collection = db.collection('briefs');

    // 1. 统计需要迁移的文档数量
    console.log('📊 统计数据...');
    const countBefore = await collection.countDocuments({ category: 'ev_automotive' });
    console.log(`   发现 ${countBefore} 条 ev_automotive 分类的新闻\n`);

    if (countBefore === 0) {
      console.log('✅ 没有需要迁移的数据');
      await mongoose.connection.close();
      return;
    }

    // 2. 显示一些示例数据
    console.log('📄 示例数据（前3条）:');
    const samples = await collection.find({ category: 'ev_automotive' })
      .limit(3)
      .project({ title: 1, category: 1, created_at: 1 })
      .toArray();

    samples.forEach((doc, i) => {
      console.log(`   ${i + 1}. ${doc.title.substring(0, 50)}...`);
      console.log(`      分类: ${doc.category}, 创建时间: ${doc.created_at}`);
    });
    console.log('');

    // 3. 执行更新
    console.log('🔄 开始迁移...');
    const result = await collection.updateMany(
      { category: 'ev_automotive' },
      { $set: { category: 'automotive' } }
    );

    console.log(`✅ 迁移完成！`);
    console.log(`   匹配文档: ${result.matchedCount}`);
    console.log(`   更新文档: ${result.modifiedCount}\n`);

    // 4. 验证迁移结果
    console.log('🔍 验证迁移结果...');
    const countAfter = await collection.countDocuments({ category: 'ev_automotive' });
    const countNew = await collection.countDocuments({ category: 'automotive' });

    console.log(`   ev_automotive 剩余: ${countAfter}`);
    console.log(`   automotive 总数: ${countNew}`);

    if (countAfter === 0) {
      console.log('\n✅ 数据迁移验证成功！所有数据已成功迁移');
    } else {
      console.log('\n⚠️  警告：仍有部分 ev_automotive 数据未迁移');
    }

    // 5. 关闭连接
    await mongoose.connection.close();
    console.log('\n📌 数据库连接已关闭');

  } catch (error) {
    console.error('❌ 迁移失败:', error);
    process.exit(1);
  }
}

// 执行迁移
migrate();
