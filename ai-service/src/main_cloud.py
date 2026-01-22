import sys
import os
import time
import schedule
import logging
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    NEWS_SOURCES, MONGODB_URI, CRAWL_INTERVAL,
    SUMMARIZE_PROMPT, CLASSIFY_PROMPT, REDIS_URL
)
from crawlers.news_crawler import NewsCrawler
from models.database import NewsDatabase
import redis

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsService:
    """新闻服务主类（云端版本）"""

    def __init__(self):
        self.crawler = NewsCrawler(NEWS_SOURCES['rss_feeds'])
        self.db = NewsDatabase(MONGODB_URI)
        self.redis_client = redis.from_url(REDIS_URL)

        # 根据环境变量选择AI处理器
        use_cloud_ai = os.getenv('USE_CLOUD_AI', 'false').lower() == 'true'
        ai_provider = os.getenv('AI_PROVIDER', 'openai').lower()

        if use_cloud_ai:
            logger.info(f"使用云端AI: {ai_provider}")
            from processors.cloud_ai_processor import NewsProcessor
            self.processor = NewsProcessor(ai_provider)
        else:
            logger.info("使用本地Ollama")
            from processors.ai_processor import NewsProcessor
            ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
            model_name = os.getenv('MODEL_NAME', 'qwen2:7b')
            self.processor = NewsProcessor(ollama_host, model_name)

    def run_cycle(self):
        """执行一次完整的新闻采集和处理循环"""
        try:
            logger.info("=" * 50)
            logger.info("开始新一轮新闻采集")

            # 1. 爬取新闻
            raw_news = self.crawler.crawl_all()
            logger.info(f"爬取到 {len(raw_news)} 条新闻")

            if not raw_news:
                logger.warning("没有爬取到新闻")
                return

            # 2. 过滤已存在的新闻
            new_news = []
            for news in raw_news:
                if not self.db.check_news_exists(news['link']):
                    new_news.append(news)

            logger.info(f"过滤后剩余 {len(new_news)} 条新新闻")

            if not new_news:
                logger.info("没有新新闻需要处理")
                return

            # 3. 保存原始新闻
            for news in new_news:
                self.db.save_raw_news(news)

            # 4. AI处理（摘要和分类）
            logger.info("开始AI处理...")
            processed_news = self.processor.batch_process(
                new_news,
                SUMMARIZE_PROMPT,
                CLASSIFY_PROMPT
            )

            # 5. 保存简报
            saved_count = 0
            for brief in processed_news:
                brief_id = self.db.save_brief(brief)
                if brief_id:
                    saved_count += 1
                    # 发布到Redis，通知后端服务
                    self.publish_brief(brief)

            logger.info(f"成功保存 {saved_count} 条简报")
            logger.info("本轮采集完成")
            logger.info("=" * 50)

        except Exception as e:
            logger.error(f"采集循环出错: {str(e)}", exc_info=True)

    def publish_brief(self, brief: dict):
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
    # 检查AI配置
    use_cloud_ai = os.getenv('USE_CLOUD_AI', 'false').lower() == 'true'

    if use_cloud_ai:
        ai_provider = os.getenv('AI_PROVIDER', 'openai')
        logger.info(f"新闻简报AI服务启动（云端模式: {ai_provider}）")

        # 检查API密钥
        if ai_provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
            logger.error("错误: 未设置 OPENAI_API_KEY 环境变量")
            return
        elif ai_provider == 'claude' and not os.getenv('CLAUDE_API_KEY'):
            logger.error("错误: 未设置 CLAUDE_API_KEY 环境变量")
            return
    else:
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        model_name = os.getenv('MODEL_NAME', 'qwen2:7b')
        logger.info(f"新闻简报AI服务启动（本地模式）")
        logger.info(f"Ollama地址: {ollama_host}")
        logger.info(f"使用模型: {model_name}")

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
