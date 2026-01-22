import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsCrawler:
    """新闻爬虫类"""

    def __init__(self, rss_feeds: List[str]):
        self.rss_feeds = rss_feeds

    def crawl_rss(self, feed_url: str) -> List[Dict]:
        """爬取RSS订阅源"""
        try:
            feed = feedparser.parse(feed_url)
            news_items = []

            for entry in feed.entries[:10]:  # 每个源取最新10条
                news_item = {
                    'title': entry.get('title', ''),
                    'content': self._extract_content(entry),
                    'link': entry.get('link', ''),
                    'published': self._parse_date(entry),
                    'source': feed.feed.get('title', feed_url),
                    'source_url': feed_url,
                    'raw_data': entry
                }
                news_items.append(news_item)

            logger.info(f"从 {feed_url} 爬取到 {len(news_items)} 条新闻")
            return news_items

        except Exception as e:
            logger.error(f"爬取RSS失败 {feed_url}: {str(e)}")
            return []

    def _extract_content(self, entry) -> str:
        """提取新闻内容"""
        # 尝试多个可能的内容字段
        content = entry.get('summary', '')
        if not content:
            content = entry.get('description', '')
        if not content:
            content = entry.get('content', [{}])[0].get('value', '')

        # 清理HTML标签
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.get_text(strip=True)

        return content[:1000]  # 限制长度

    def _parse_date(self, entry) -> datetime:
        """解析发布时间"""
        date_str = entry.get('published', entry.get('updated', ''))
        if date_str:
            try:
                from dateutil import parser
                return parser.parse(date_str)
            except:
                pass
        return datetime.now()

    def crawl_all(self) -> List[Dict]:
        """爬取所有新闻源"""
        all_news = []
        for feed_url in self.rss_feeds:
            news = self.crawl_rss(feed_url)
            all_news.extend(news)

        logger.info(f"总共爬取到 {len(all_news)} 条新闻")
        return all_news


class WebPageCrawler:
    """网页爬虫类（备用）"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_article(self, url: str) -> Dict:
        """抓取单个文章"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 尝试提取标题和内容（需要根据实际网站调整）
            title = soup.find('h1')
            content = soup.find('article') or soup.find('div', class_='content')

            return {
                'title': title.get_text(strip=True) if title else '',
                'content': content.get_text(strip=True) if content else '',
                'link': url,
                'published': datetime.now(),
                'source': url.split('/')[2]
            }

        except Exception as e:
            logger.error(f"抓取网页失败 {url}: {str(e)}")
            return None
