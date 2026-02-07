"""
新闻简报AI服务 V2 - 多源支持
支持 RSS、Twitter/X、微信公众号、知乎、即刻
"""

import sys
import os
import time
import schedule
import logging
from datetime import datetime
from typing import Dict
from threading import Lock, Thread
from flask import Flask, jsonify

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入 V2 配置
from config.sources_v2 import NEWS_SOURCES_V2
from config.settings import (
    MONGODB_URI, CRAWL_INTERVAL,
    SUMMARIZE_PROMPT, CLASSIFY_PROMPT, COMBINED_PROMPT, REDIS_URL
)
from crawlers.multi_source_crawler import MultiSourceCrawler
from processors.cloud_ai_processor import NewsProcessor
from models.database import NewsDatabase
from filters.quality_filter import ContentQualityFilter
import redis

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsServiceV2:
    """新闻服务主类 V2"""

    def __init__(self):
        # 使用多源爬虫
        self.crawler = MultiSourceCrawler(NEWS_SOURCES_V2)
        
        # 使用云端AI处理器（Kimi/DeepSeek/OpenAI/Claude）
        ai_provider = os.getenv('AI_PROVIDER', 'kimi')
        self.processor = NewsProcessor(ai_provider)
        self.db = NewsDatabase(MONGODB_URI)

        # 内容质量过滤器
        self.quality_filter = ContentQualityFilter()
        logger.info("内容质量过滤器已启用")

        # 添加锁，防止并发执行
        self._lock = Lock()
        self._is_running = False

        # Redis连接（可选，用于实时通知）
        try:
            self.redis_client = redis.from_url(REDIS_URL)
            self.redis_client.ping()
            self.redis_enabled = True
            logger.info("Redis连接成功")
        except Exception as e:
            logger.warning(f"Redis连接失败，将禁用实时通知功能: {str(e)}")
            self.redis_enabled = False
            self.redis_client = None

    def run_cycle(self):
        """执行一次完整的新闻采集和处理循环"""
        if not self._lock.acquire(blocking=False):
            logger.warning("⚠️  上一轮采集仍在进行中，跳过本次调度")
            return

        try:
            self._is_running = True
            start_time = datetime.now()

            logger.info("=" * 60)
            logger.info("NewsHub V2 - 开始新一轮新闻采集")
            logger.info(f"支持源: RSS + Twitter/X + 微信公众号 + 知乎 + 即刻")

            # 1. 爬取新闻（多源）
            logger.info("步骤 1/5: 开始爬取所有新闻源...")
            raw_news = self.crawler.crawl_all()
            
            # 按来源类型统计
            source_stats = {}
            for news in raw_news:
                source_type = news.get('source_type', 'unknown')
                source_stats[source_type] = source_stats.get(source_type, 0) + 1
            
            logger.info(f"步骤 1/5 完成: 爬取到 {len(raw_news)} 条新闻")
            logger.info(f"  来源分布: {source_stats}")

            if not raw_news:
                logger.warning("没有爬取到新闻")
                return

            # 2. 过滤已存在的新闻
            logger.info("步骤 2/5: 批量过滤重复新闻...")
            step2_start = datetime.now()

            all_links = [news['link'] for news in raw_news]
            existing_links = set()
            BATCH_SIZE = 500

            if len(all_links) <= BATCH_SIZE:
                existing_links = self.db.check_news_exists_batch(all_links)
            else:
                batch_count = (len(all_links) + BATCH_SIZE - 1) // BATCH_SIZE
                for i in range(0, len(all_links), BATCH_SIZE):
                    batch = all_links[i:i + BATCH_SIZE]
                    batch_num = i // BATCH_SIZE + 1
                    logger.info(f"  处理第 {batch_num}/{batch_count} 批...")
                    existing_links.update(self.db.check_news_exists_batch(batch))

            step2_elapsed = (datetime.now() - step2_start).total_seconds()
            logger.info(f"批量查询总计耗时: {step2_elapsed:.1f} 秒")

            new_news = [news for news in raw_news if news['link'] not in existing_links]
            logger.info(f"步骤 2/5 完成: 过滤后剩余 {len(new_news)} 条新新闻")

            if not new_news:
                logger.info("没有新新闻需要处理")
                return

            # 2.5. 内容质量过滤
            logger.info("步骤 2.5/5: 内容质量过滤...")
            before_filter = len(new_news)

            quality_filtered_news = []
            for news in new_news:
                title = news.get('title', '')
                # Twitter 内容需要特殊处理（RT、@mention 过滤）
                if news.get('source_type') == 'twitter':
                    # 跳过纯转推（RT 开头）
                    if title.startswith('RT @'):
                        continue
                    # 跳过低质量 Twitter 内容（如纯表情、过短）
                    if len(title) < 20:
                        continue
                
                if self.quality_filter.should_process(title, 'general', threshold=3):
                    quality_filtered_news.append(news)

            after_filter = len(quality_filtered_news)
            filtered_count = before_filter - after_filter

            if filtered_count > 0:
                logger.info(f"步骤 2.5/5 完成: 质量过滤移除 {filtered_count} 条，剩余 {after_filter} 条")
            else:
                logger.info(f"步骤 2.5/5 完成: 所有内容通过质量检查")

            if not quality_filtered_news:
                logger.info("质量过滤后没有剩余新闻")
                return

            new_news = quality_filtered_news

            # 3. 保存原始新闻
            logger.info("步骤 3/5: 保存原始新闻到数据库...")
            for news in new_news:
                self.db.save_raw_news(news)
            logger.info(f"步骤 3/5 完成: 已保存 {len(new_news)} 条原始新闻")

            # 4. AI处理
            logger.info(f"步骤 4/5: 开始 AI 处理 ({len(new_news)} 条新闻)...")
            logger.info(f"当前 AI Provider: {os.getenv('AI_PROVIDER', 'kimi')}")
            logger.info(f"Token优化: 使用合并提示词，一次调用完成摘要+分类")

            processed_news = self.processor.batch_process_combined(
                new_news,
                COMBINED_PROMPT
            )
            logger.info(f"步骤 4/5 完成: AI 处理完成，生成 {len(processed_news)} 条简报")

            # 5. 保存简报
            logger.info("步骤 5/5: 保存简报到数据库...")
            saved_count = 0
            for brief in processed_news:
                brief_id = self.db.save_brief(brief)
                if brief_id:
                    saved_count += 1
                    self.publish_brief(brief)

            logger.info(f"步骤 5/5 完成: 成功保存 {saved_count}/{len(processed_news)} 条简报")

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"本轮采集完成，耗时 {elapsed:.1f} 秒")
            logger.info("=" * 60)

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.error(f"采集循环出错（耗时 {elapsed:.1f} 秒）: {str(e)}", exc_info=True)

        finally:
            self._is_running = False
            self._lock.release()
            logger.debug("采集锁已释放")

    def publish_brief(self, brief: Dict):
        """发布简报到Redis"""
        if not self.redis_enabled or not self.redis_client:
            return

        try:
            if '_id' in brief:
                brief['_id'] = str(brief['_id'])
            if 'published' in brief:
                brief['published'] = brief['published'].isoformat()
            if 'created_at' in brief:
                brief['created_at'] = brief['created_at'].isoformat()

            import json
            self.redis_client.publish('news:new', json.dumps(brief, ensure_ascii=False))
            logger.debug(f"发布简报到Redis: [{brief['category']}] {brief['title'][:30]}")
        except Exception as e:
            logger.error(f"发布到Redis失败: {str(e)}")
            self.redis_enabled = False


# Flask应用
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "running",
        "service": "news-ai-service-v2",
        "version": "2.0.0",
        "features": ["rss", "twitter", "wechat", "zhihu", "jike"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def root():
    """根路径"""
    return jsonify({
        "service": "NewsHub AI Service V2",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "/health": "Health check endpoint"
        }
    })


def run_flask():
    """在后台线程运行Flask"""
    port = int(os.getenv('PORT', 10000))
    logger.info(f"启动Flask健康检查服务在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("NewsHub V2 新闻简报AI服务启动")
    logger.info("=" * 60)
    logger.info(f"AI提供商: {os.getenv('AI_PROVIDER', 'kimi')}")
    logger.info(f"采集间隔: {CRAWL_INTERVAL}秒")
    
    # 显示源统计
    from config.sources_v2 import TOTAL_SOURCES
    logger.info(f"总计新闻源: {TOTAL_SOURCES} 个")
    
    # 启动Flask
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask健康检查服务已启动")

    service = NewsServiceV2()

    # 立即执行一次
    logger.info("执行首次采集...")
    service.run_cycle()

    # 定时任务
    schedule.every(CRAWL_INTERVAL).seconds.do(service.run_cycle)

    logger.info("进入定时循环...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
