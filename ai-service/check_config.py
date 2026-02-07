#!/usr/bin/env python3
"""
配置检查脚本 - 验证AI服务配置是否正确
"""

import os
import sys

# 添加src到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import NEWS_SOURCES, CATEGORIES
from config.sources_v2 import NEWS_SOURCES_V2, TOTAL_SOURCES

def check_env_variables():
    """检查环境变量"""
    print("=" * 60)
    print("🔍 环境变量检查")
    print("=" * 60)
    
    # 必需的环境变量
    required_vars = {
        'MONGODB_URI': 'MongoDB连接字符串',
        'AI_PROVIDER': 'AI提供商 (kimi/deepseek/openai/claude)',
    }
    
    # API Key变量（根据AI_PROVIDER选择）
    ai_provider = os.getenv('AI_PROVIDER', 'kimi')
    api_key_var = f"{ai_provider.upper()}_API_KEY"
    
    print(f"\n1. AI提供商: {ai_provider}")
    
    all_ok = True
    
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            # 隐藏敏感信息
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: 未设置 ({desc})")
            all_ok = False
    
    # 检查API Key
    api_key = os.getenv(api_key_var)
    if api_key:
        print(f"   ✅ {api_key_var}: 已设置 ({len(api_key)} 字符)")
    else:
        print(f"   ❌ {api_key_var}: 未设置!")
        print(f"      请设置环境变量: export {api_key_var}=your_api_key")
        all_ok = False
    
    # 可选变量
    optional_vars = {
        'REDIS_URL': 'Redis连接字符串',
        'CRAWL_INTERVAL': '爬取间隔(秒)',
        'AI_CONCURRENT_WORKERS': 'AI并发线程数',
    }
    
    print(f"\n2. 可选配置:")
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚪ {var}: 使用默认值 ({desc})")
    
    return all_ok

def check_news_sources():
    """检查新闻源配置"""
    print("\n" + "=" * 60)
    print("📰 新闻源检查")
    print("=" * 60)
    
    print(f"\n1. V2版本新闻源:")
    print(f"   - RSS源: {len(NEWS_SOURCES_V2.get('rss_feeds', []))} 个")
    print(f"   - Twitter源: {len(NEWS_SOURCES_V2.get('twitter', []))} 个")
    print(f"   - 微信公众号: {len(NEWS_SOURCES_V2.get('wechat', []))} 个")
    print(f"   - 微博大V: {len(NEWS_SOURCES_V2.get('weibo', []))} 个")
    print(f"   - YouTube频道: {len(NEWS_SOURCES_V2.get('youtube', []))} 个")
    print(f"   - 总计: {TOTAL_SOURCES} 个")
    
    # 中文源详情
    from config.sources_v2 import CHINA_SOURCES
    print(f"\n2. 中文源分类统计:")
    print(f"   - 微信公众号: {len(CHINA_SOURCES.get('wechat_official', []))} 个")
    print(f"   - 微博大V: {len(CHINA_SOURCES.get('weibo', []))} 个")
    
    # YouTube 频道详情
    from config.sources_v2 import YOUTUBE_SOURCES
    print(f"\n3. YouTube 频道分类统计:")
    for category, urls in YOUTUBE_SOURCES.items():
        print(f"   - {category}: {len(urls)} 个频道")
    
    print(f"\n3. 支持的新闻分类 ({len(CATEGORIES)} 个):")
    for cat in CATEGORIES[:10]:  # 只显示前10个
        print(f"   - {cat}")
    if len(CATEGORIES) > 10:
        print(f"   ... 还有 {len(CATEGORIES) - 10} 个分类")

def check_ai_processor():
    """检查AI处理器"""
    print("\n" + "=" * 60)
    print("🤖 AI处理器检查")
    print("=" * 60)
    
    ai_provider = os.getenv('AI_PROVIDER', 'kimi')
    api_key_var = f"{ai_provider.upper()}_API_KEY"
    api_key = os.getenv(api_key_var)
    
    if not api_key:
        print(f"\n❌ AI处理器无法初始化: {api_key_var} 未设置")
        return False
    
    try:
        from processors.cloud_ai_processor import NewsProcessor
        processor = NewsProcessor(ai_provider)
        print(f"\n✅ AI处理器初始化成功")
        print(f"   提供商: {ai_provider}")
        print(f"   模型: {processor.ai.model}")
        print(f"   API URL: {processor.ai.api_url}")
        return True
    except Exception as e:
        print(f"\n❌ AI处理器初始化失败: {str(e)}")
        return False

def check_database():
    """检查数据库连接"""
    print("\n" + "=" * 60)
    print("🗄️  数据库检查")
    print("=" * 60)
    
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        print("\n❌ MONGODB_URI 未设置")
        return False
    
    try:
        from models.database import NewsDatabase
        db = NewsDatabase(mongodb_uri)
        # 尝试连接
        db.client.server_info()
        print(f"\n✅ MongoDB连接成功")
        print(f"   数据库: {db.db.name}")
        
        # 统计集合
        collections = db.db.list_collection_names()
        print(f"   集合: {', '.join(collections) if collections else '暂无集合'}")
        return True
    except Exception as e:
        print(f"\n❌ MongoDB连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🚀 NewsHub AI服务配置检查")
    print("=" * 60)
    
    env_ok = check_env_variables()
    check_news_sources()
    
    ai_ok = check_ai_processor()
    db_ok = check_database()
    
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    
    if env_ok and ai_ok and db_ok:
        print("\n✅ 所有检查通过！服务可以正常运行。")
        return 0
    else:
        print("\n⚠️  部分检查未通过，请根据上方提示修复配置。")
        if not env_ok:
            print("   - 环境变量配置有问题")
        if not ai_ok:
            print("   - AI处理器初始化失败")
        if not db_ok:
            print("   - 数据库连接失败")
        return 1

if __name__ == '__main__':
    exit(main())
