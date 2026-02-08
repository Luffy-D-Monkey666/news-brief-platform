"""
新闻简报系统全面诊断脚本
检查所有可能的新闻流程阻断点
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.sources_v2 import NEWS_SOURCES_V2
from config.settings import MONGODB_URI
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests

print("=" * 70)
print("🔍 新闻简报系统全面诊断")
print("=" * 70)

# 1. 检查环境变量
print("\n📋 1. 环境变量检查")
print("-" * 50)
required_vars = [
    'KIMI_API_KEY',
    'MONGODB_URI', 
    'REDIS_URL',
    'AI_PROVIDER',
    'SKIP_DB_DEDUPE'
]

for var in required_vars:
    value = os.getenv(var)
    if value:
        masked = value[:10] + "..." if len(value) > 10 else value
        print(f"  ✅ {var}: {masked}")
    else:
        print(f"  ⚠️  {var}: 未设置")

# 2. 检查新闻源配置
print("\n📡 2. 新闻源配置检查")
print("-" * 50)

total_sources = 0
for source_type, urls in NEWS_SOURCES_V2.items():
    count = len(urls) if isinstance(urls, list) else sum(len(v) for v in urls.values())
    total_sources += count
    print(f"  📁 {source_type}: {count} 个源")

print(f"\n  📊 总计: {total_sources} 个新闻源")

# 3. 测试 RSSHub 连通性
print("\n🌐 3. RSSHub 连通性测试")
print("-" * 50)

test_urls = [
    ("量子位 RSS", "https://rsshub.app/qbitai"),
    ("机器之心 RSS", "https://rsshub.app/jiqizhixin/ai"),
    ("36氪 RSS", "https://rsshub.app/36kr/newsflashes"),
]

for name, url in test_urls:
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            # 简单检查是否有内容
            has_entries = '<entry' in resp.text or '<item' in resp.text
            if has_entries:
                print(f"  ✅ {name}: 正常 ({len(resp.text)} 字符)")
            else:
                print(f"  ⚠️  {name}: 返回空内容")
        else:
            print(f"  ❌ {name}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  ❌ {name}: {str(e)[:50]}")

# 4. 数据库连接和统计
print("\n💾 4. 数据库状态检查")
print("-" * 50)

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print(f"  ✅ MongoDB 连接: 正常")
    
    # 获取数据库名称
    if '/' in MONGODB_URI.rsplit('/', 1)[-1]:
        db_name = MONGODB_URI.rsplit('/', 1)[-1].split('?')[0]
    else:
        db_name = 'news-brief'
    
    db = client[db_name]
    
    # 统计集合
    raw_count = db['news'].count_documents({})
    brief_count = db['briefs'].count_documents({})
    
    print(f"  📄 raw_news 集合: {raw_count} 条")
    print(f"  📰 briefs 集合: {brief_count} 条")
    
    # 最近24小时的简报
    recent_briefs = db['briefs'].count_documents({
        'created_at': {'$gte': datetime.now() - timedelta(hours=24)}
    })
    print(f"  📈 最近24小时新增: {recent_briefs} 条简报")
    
    # 按分类统计
    print(f"\n  📊 分类统计:")
    category_stats = db['briefs'].aggregate([
        {'$group': {'_id': '$category', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])
    for stat in category_stats:
        print(f"     - {stat['_id']}: {stat['count']} 条")
    
    # 最近的一条简报
    latest = db['briefs'].find_one(sort=[('created_at', -1)])
    if latest:
        print(f"\n  🕐 最新简报:")
        print(f"     标题: {latest.get('title', 'N/A')[:50]}...")
        print(f"     分类: {latest.get('category', 'N/A')}")
        print(f"     时间: {latest.get('created_at', 'N/A')}")
    else:
        print(f"\n  ⚠️  数据库中没有简报！")
        
except Exception as e:
    print(f"  ❌ MongoDB 错误: {str(e)}")

# 5. API 测试
print("\n🤖 5. AI API 测试")
print("-" * 50)

ai_provider = os.getenv('AI_PROVIDER', 'kimi')
api_key = os.getenv(f'{ai_provider.upper()}_API_KEY')

if not api_key:
    print(f"  ❌ {ai_provider.upper()}_API_KEY 未设置")
else:
    print(f"  ✅ {ai_provider} API Key 已设置")
    
    # 简单测试API
    if ai_provider == 'kimi':
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            resp = requests.get('https://api.moonshot.cn/v1/models', headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"  ✅ Kimi API 连接: 正常")
            else:
                print(f"  ❌ Kimi API 错误: HTTP {resp.status_code}")
        except Exception as e:
            print(f"  ❌ Kimi API 测试失败: {str(e)[:50]}")

# 6. 给出建议
print("\n" + "=" * 70)
print("💡 诊断建议")
print("=" * 70)

print("""
如果新闻进不来，按以下顺序排查：

1. 【SKIP_DB_DEDUPE】检查是否设置为 true
   - 在 Render 环境变量中设置 SKIP_DB_DEDUPE=true
   - 这会跳过数据库去重，强制处理所有新闻

2. 【RSSHub 状态】如果测试显示 RSSHub 返回空
   - RSSHub 免费服务不稳定
   - 考虑自建 RSSHub 实例
   - 或申请官方 API Key

3. 【AI API】如果 API 测试失败
   - 检查 API Key 是否正确
   - 检查是否有余额

4. 【数据库】如果简报数为 0
   - 检查 AI 处理是否成功
   - 查看日志中的 AI 处理成功率

5. 【时间窗口】如果时间过滤过多
   - 当前设置为 7 天 (168 小时)
   - 可以延长到 30 天获取更多历史新闻

快速修复命令（MongoDB）：
  # 清空数据库重新开始
  db.news.deleteMany({})
  db.briefs.deleteMany({})
""")

print("=" * 70)
