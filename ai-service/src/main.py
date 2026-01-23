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

        # Redis连接（可选，用于实时通知）
        try:
            self.redis_client = redis.from_url(REDIS_URL)
            # 测试连接
            self.redis_client.ping()
            self.redis_enabled = True
            logger.info("Redis连接成功")
        except Exception as e:
            logger.warning(f"Redis连接失败，将禁用实时通知功能: {str(e)}")
            self.redis_enabled = False
            self.redis_client = None

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
            logger.info("步骤 2/5: 批量过滤重复新闻...")
            step2_start = datetime.now()

            # 使用批量查询优化性能
            all_links = [news['link'] for news in raw_news]
            logger.info(f"准备检查 {len(all_links)} 个新闻链接...")

            # 如果链接过多，分批处理
            existing_links = set()
            BATCH_SIZE = 500

            if len(all_links) <= BATCH_SIZE:
                # 一次性查询
                existing_links = self.db.check_news_exists_batch(all_links)
            else:
                # 分批查询
                logger.info(f"链接数量较多，采用分批查询模式（每批{BATCH_SIZE}个）...")
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
        """发布简报到Redis（可选功能）"""
        if not self.redis_enabled or not self.redis_client:
            return  # Redis不可用，跳过发布

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
            # 连接失败时禁用Redis，避免重复报错
            logger.warning("禁用Redis实时通知功能")
            self.redis_enabled = False


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
