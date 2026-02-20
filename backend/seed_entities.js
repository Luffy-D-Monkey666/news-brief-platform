#!/usr/bin/env node
/**
 * 预置实体数据导入脚本
 * 
 * 使用方法:
 *   node scripts/seed_entities.js              # 导入所有实体
 *   node scripts/seed_entities.js --file tech_companies.json  # 导入指定文件
 *   node scripts/seed_entities.js --dry-run    # 仅预览，不写入
 */

const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../backend/.env') });

// Entity 模型定义（与 backend 保持一致）
const entitySchema = new mongoose.Schema({
  name: { type: String, required: true, unique: true },
  aliases: [String],
  type: {
    type: String,
    enum: ['company', 'person', 'event', 'concept'],
    required: true
  },
  description: String,
  image: String,
  metadata: {
    founded: String,
    founder: String,
    headquarters: String,
    industry: String,
    ticker: String,
    website: String
  },
  base_timeline: [{
    date: String,
    event: String,
    importance: { type: String, enum: ['milestone', 'major', 'normal'], default: 'normal' }
  }],
  is_preset: { type: Boolean, default: false },
  is_active: { type: Boolean, default: true },
  mention_count: { type: Number, default: 0 },
  news_count: { type: Number, default: 0 },
  last_news_at: Date,
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
});

const Entity = mongoose.model('Entity', entitySchema);

// 解析命令行参数
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const fileIndex = args.indexOf('--file');
const specificFile = fileIndex !== -1 ? args[fileIndex + 1] : null;

// 实体数据目录
const DATA_DIR = path.join(__dirname, '../data/entities');

async function loadEntityFiles() {
  const files = [];
  
  if (specificFile) {
    const filePath = path.join(DATA_DIR, specificFile);
    if (fs.existsSync(filePath)) {
      files.push(filePath);
    } else {
      console.error(`❌ 文件不存在: ${filePath}`);
      process.exit(1);
    }
  } else {
    // 加载所有 JSON 文件
    if (!fs.existsSync(DATA_DIR)) {
      console.error(`❌ 数据目录不存在: ${DATA_DIR}`);
      process.exit(1);
    }
    
    const dirFiles = fs.readdirSync(DATA_DIR).filter(f => f.endsWith('.json'));
    for (const f of dirFiles) {
      files.push(path.join(DATA_DIR, f));
    }
  }
  
  return files;
}

async function seedEntities() {
  console.log('🚀 开始导入预置实体数据...\n');
  
  if (dryRun) {
    console.log('📝 DRY RUN 模式 - 仅预览，不写入数据库\n');
  }
  
  // 连接数据库
  const mongoUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/newshub';
  console.log(`📦 连接数据库: ${mongoUri.replace(/\/\/[^:]+:[^@]+@/, '//***:***@')}`);
  
  if (!dryRun) {
    await mongoose.connect(mongoUri);
    console.log('✅ 数据库连接成功\n');
  }
  
  // 加载数据文件
  const files = await loadEntityFiles();
  console.log(`📁 找到 ${files.length} 个数据文件\n`);
  
  let totalCreated = 0;
  let totalUpdated = 0;
  let totalSkipped = 0;
  let totalErrors = 0;
  
  for (const filePath of files) {
    const fileName = path.basename(filePath);
    console.log(`\n📄 处理: ${fileName}`);
    console.log('─'.repeat(50));
    
    let entities;
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      entities = JSON.parse(content);
      if (!Array.isArray(entities)) {
        entities = [entities];
      }
    } catch (err) {
      console.error(`  ❌ 解析失败: ${err.message}`);
      totalErrors++;
      continue;
    }
    
    for (const entity of entities) {
      const { name, aliases, type, description, metadata, base_timeline } = entity;
      
      if (!name || !type) {
        console.log(`  ⚠️  跳过无效实体 (缺少 name 或 type)`);
        totalSkipped++;
        continue;
      }
      
      if (dryRun) {
        console.log(`  📝 [预览] ${name} (${type}) - ${base_timeline?.length || 0} 个时间轴节点`);
        totalCreated++;
        continue;
      }
      
      try {
        // Upsert: 存在则更新，不存在则创建
        const result = await Entity.findOneAndUpdate(
          { name },
          {
            $set: {
              aliases: aliases || [],
              type,
              description: description || '',
              metadata: metadata || {},
              base_timeline: base_timeline || [],
              is_preset: true,
              is_active: true,
              updated_at: new Date()
            },
            $setOnInsert: {
              mention_count: 0,
              news_count: 0,
              created_at: new Date()
            }
          },
          { upsert: true, new: true, rawResult: true }
        );
        
        if (result.lastErrorObject?.updatedExisting) {
          console.log(`  🔄 更新: ${name} (${base_timeline?.length || 0} 节点)`);
          totalUpdated++;
        } else {
          console.log(`  ✅ 创建: ${name} (${base_timeline?.length || 0} 节点)`);
          totalCreated++;
        }
      } catch (err) {
        console.error(`  ❌ 失败: ${name} - ${err.message}`);
        totalErrors++;
      }
    }
  }
  
  // 汇总
  console.log('\n' + '═'.repeat(50));
  console.log('📊 导入完成汇总:');
  console.log(`   ✅ 新建: ${totalCreated}`);
  console.log(`   🔄 更新: ${totalUpdated}`);
  console.log(`   ⚠️  跳过: ${totalSkipped}`);
  console.log(`   ❌ 错误: ${totalErrors}`);
  console.log('═'.repeat(50));
  
  if (!dryRun) {
    await mongoose.disconnect();
    console.log('\n📦 数据库连接已关闭');
  }
}

// 执行
seedEntities()
  .then(() => {
    console.log('\n🎉 脚本执行完毕');
    process.exit(0);
  })
  .catch(err => {
    console.error('\n💥 脚本执行失败:', err);
    process.exit(1);
  });
