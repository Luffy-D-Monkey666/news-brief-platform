import sys
import os
import time
import schedule
import logging
from datetime import datetime
from typing import Dict

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    NEWS_SOURCES, MONGODB_URI, CRAWL_INTERVAL,
    SUMMARIZE_PROMPT, CLASSIFY_PROMPT, REDIS_URL
)
from crawlers.news_crawler import NewsCrawler
from processors.cloud_ai_processor import NewsProcessor
from models.database import NewsDatabase
import redis

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsService:
    """新闻服务主类"""

    def __init__(self):
        self.crawler = NewsCrawler(NEWS_SOURCES['rss_feeds'])
        # 使用云端AI处理器（OpenAI/Claude）
        ai_provider = os.getenv('AI_PROVIDER', 'openai')
        self.processor = NewsProcessor(ai_provider)
        self.db = NewsDatabase(MONGODB_URI)
        self.redis_client = redis.from_url(REDIS_URL)

    def run_cycle(self):
        """执行一次完整的新闻采集和处理循环"""
        start_time = datetime.now()
        try:
            logger.info("=" * 50)
            logger.info("开始新一轮新闻采集")

            # 1. 爬取新闻
            logger.info("步骤 1/5: 开始爬取 RSS 订阅源...")
            raw_news = self.crawler.crawl_all()
            logger.info(f"步骤 1/5 完成: 爬取到 {len(raw_news)} 条新闻")

            if not raw_news:
                logger.warning("没有爬取到新闻")
                return

            # 2. 过滤已存在的新闻
            logger.info("步骤 2/5: 过滤重复新闻...")
            new_news = []
            for news in raw_news:
                if not self.db.check_news_exists(news['link']):
                    new_news.append(news)

            logger.info(f"步骤 2/5 完成: 过滤后剩余 {len(new_news)} 条新新闻")

            if not new_news:
                logger.info("没有新新闻需要处理")
                return

            # 3. 保存原始新闻
            logger.info("步骤 3/5: 保存原始新闻到数据库...")
            for news in new_news:
                self.db.save_raw_news(news)
            logger.info(f"步骤 3/5 完成: 已保存 {len(new_news)} 条原始新闻")

            # 4. AI处理（摘要和分类）
            logger.info(f"步骤 4/5: 开始 AI 处理 ({len(new_news)} 条新闻)...")
            logger.info(f"当前 AI Provider: {os.getenv('AI_PROVIDER', 'openai')}")

            processed_news = self.processor.batch_process(
                new_news,
                SUMMARIZE_PROMPT,
                CLASSIFY_PROMPT
            )
            logger.info(f"步骤 4/5 完成: AI 处理完成，生成 {len(processed_news)} 条简报")

            # 5. 保存简报
            logger.info("步骤 5/5: 保存简报到数据库...")
            saved_count = 0
            for brief in processed_news:
                brief_id = self.db.save_brief(brief)
                if brief_id:
                    saved_count += 1
                    # 发布到Redis，通知后端服务
                    self.publish_brief(brief)

            logger.info(f"步骤 5/5 完成: 成功保存 {saved_count}/{len(processed_news)} 条简报")

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"本轮采集完成，耗时 {elapsed:.1f} 秒")
            logger.info("=" * 50)

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.error(f"采集循环出错（耗时 {elapsed:.1f} 秒）: {str(e)}", exc_info=True)

    def publish_brief(self, brief: Dict):
        """发布简报到Redis"""
        try:
            # 将ObjectId转换为字符串
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


def main():
    """主函数"""
    logger.info("新闻简报AI服务启动")
    logger.info(f"AI提供商: {os.getenv('AI_PROVIDER', 'openai')}")
    logger.info(f"采集间隔: {CRAWL_INTERVAL}秒")

    service = NewsService()

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
