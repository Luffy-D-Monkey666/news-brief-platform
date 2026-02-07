"""
多源新闻爬虫 V2
支持 RSS、Twitter/X、微信公众号、知乎、即刻
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiSourceCrawler:
    """多源新闻爬虫"""

    def __init__(self, sources_config: Dict):
        """
        初始化爬虫
        
        Args:
            sources_config: 包含 rss_feeds, twitter, wechat, zhihu, jike 的配置
        """
        self.sources = sources_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def crawl_all(self) -> List[Dict]:
        """爬取所有来源的新闻"""
        all_news = []
        
        # 1. 爬取 RSS 源
        if self.sources.get('rss_feeds'):
            logger.info(f"开始爬取 {len(self.sources['rss_feeds'])} 个 RSS 源...")
            for feed_url in self.sources['rss_feeds']:
                try:
                    news = self._crawl_rss(feed_url)
                    all_news.extend(news)
                except Exception as e:
                    logger.error(f"RSS 源失败 {feed_url}: {e}")
        
        # 2. 爬取 Twitter/X 源
        if self.sources.get('twitter'):
            logger.info(f"开始爬取 {len(self.sources['twitter'])} 个 Twitter 源...")
            for twitter_url in self.sources['twitter']:
                try:
                    news = self._crawl_twitter(twitter_url)
                    all_news.extend(news)
                except Exception as e:
                    logger.error(f"Twitter 源失败 {twitter_url}: {e}")
        
        # 3. 爬取微信公众号
        if self.sources.get('wechat'):
            logger.info(f"开始爬取 {len(self.sources['wechat'])} 个微信公众号...")
            for wechat_url in self.sources['wechat']:
                try:
                    news = self._crawl_wechat(wechat_url)
                    all_news.extend(news)
                except Exception as e:
                    logger.error(f"微信公众号失败 {wechat_url}: {e}")
        
        # 4. 爬取知乎
        if self.sources.get('zhihu'):
            logger.info(f"开始爬取 {len(self.sources['zhihu'])} 个知乎话题...")
            for zhihu_url in self.sources['zhihu']:
                try:
                    news = self._crawl_zhihu(zhihu_url)
                    all_news.extend(news)
                except Exception as e:
                    logger.error(f"知乎话题失败 {zhihu_url}: {e}")
        
        # 5. 爬取即刻
        if self.sources.get('jike'):
            logger.info(f"开始爬取 {len(self.sources['jike'])} 个即刻圈子...")
            for jike_url in self.sources['jike']:
                try:
                    news = self._crawl_jike(jike_url)
                    all_news.extend(news)
                except Exception as e:
                    logger.error(f"即刻圈子失败 {jike_url}: {e}")
        
        logger.info(f"总共爬取到 {len(all_news)} 条新闻")
        return all_news

    def _crawl_rss(self, feed_url: str, source_type: str = 'rss') -> List[Dict]:
        """爬取 RSS 订阅源"""
        try:
            import socket
            socket.setdefaulttimeout(10)
            
            feed = feedparser.parse(feed_url)
            news_items = []
            
            # RSSHub Twitter 路由通常返回 20 条，取前10条
            limit = 10 if 'twitter' in feed_url else 10
            
            for entry in feed.entries[:limit]:
                news_item = {
                    'title': entry.get('title', ''),
                    'content': self._extract_content(entry),
                    'link': entry.get('link', ''),
                    'image': self._extract_image(entry),
                    'video': self._extract_video(entry),
                    'published': self._parse_date(entry),
                    'source': self._extract_source_name(feed, feed_url, source_type),
                    'source_url': feed_url,
                    'source_type': source_type,
                    'raw_data': entry
                }
                news_items.append(news_item)
            
            socket.setdefaulttimeout(None)
            logger.info(f"  ✓ {self._get_short_url(feed_url)}: {len(news_items)} 条")
            return news_items
            
        except Exception as e:
            logger.error(f"  ✗ {self._get_short_url(feed_url)}: {e}")
            return []

    def _crawl_twitter(self, twitter_url: str) -> List[Dict]:
        """
        爬取 Twitter/X 时间线
        
        Twitter URL 格式: https://rsshub.app/twitter/user/{username}
        """
        # Twitter 通过 RSSHub 提供 RSS 格式，直接使用 RSS 爬取
        return self._crawl_rss(twitter_url, source_type='twitter')

    def _crawl_wechat(self, wechat_url: str) -> List[Dict]:
        """爬取微信公众号"""
        # 微信公众号通过 RSSHub 提供
        return self._crawl_rss(wechat_url, source_type='wechat')

    def _crawl_zhihu(self, zhihu_url: str) -> List[Dict]:
        """爬取知乎话题"""
        # 知乎通过 RSSHub 提供
        return self._crawl_rss(zhihu_url, source_type='zhihu')

    def _crawl_jike(self, jike_url: str) -> List[Dict]:
        """爬取即刻圈子"""
        # 即刻通过 RSSHub 提供
        return self._crawl_rss(jike_url, source_type='jike')

    def _extract_content(self, entry) -> str:
        """提取新闻内容"""
        content = entry.get('summary', '')
        if not content:
            content = entry.get('description', '')
        if not content:
            content = entry.get('content', [{}])[0].get('value', '')
        
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.get_text(strip=True)
        
        return content[:1500]  # Twitter 内容可能更长

    def _extract_image(self, entry) -> Optional[str]:
        """提取图片"""
        image_url = None
        
        # media:content
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('url'):
                    media_type = media.get('type', '').lower()
                    url = media.get('url', '')
                    if 'image' in media_type or any(ext in url.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                        return url
        
        # media:thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            for thumbnail in entry.media_thumbnail:
                if thumbnail.get('url'):
                    return thumbnail.get('url')
        
        # enclosures
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if 'image' in enclosure.get('type', '').lower():
                    return enclosure.get('href')
        
        # HTML img
        content = entry.get('summary', '') or entry.get('description', '')
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                return img.get('src')
        
        return None

    def _extract_video(self, entry) -> Optional[str]:
        """提取视频"""
        video_url = None
        
        try:
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('url'):
                        media_type = media.get('type', '').lower()
                        url = media.get('url', '').lower()
                        if 'video' in media_type or any(ext in url for ext in ['.mp4', '.webm', '.mov']):
                            return media.get('url')
            
            if hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if 'video' in enclosure.get('type', '').lower():
                        return enclosure.get('href')
                        
        except Exception:
            pass
        
        return None

    def _extract_source_name(self, feed, feed_url: str, source_type: str) -> str:
        """提取来源名称"""
        # 尝试从 feed 信息获取
        if hasattr(feed, 'feed') and feed.feed.get('title'):
            return feed.feed.get('title')
        
        # 从 URL 提取
        if source_type == 'twitter':
            # https://rsshub.app/twitter/user/OpenAI -> OpenAI (Twitter)
            parts = feed_url.split('/')
            if len(parts) >= 2:
                username = parts[-1]
                return f"@{username} (X/Twitter)"
        
        if source_type == 'wechat':
            # 微信公众号名称在 URL 中
            parts = feed_url.split('/')
            if len(parts) >= 2:
                return f"{parts[-1]} (微信公众号)"
        
        if source_type == 'zhihu':
            return "知乎话题"
        
        if source_type == 'jike':
            return "即刻圈子"
        
        # 默认：使用域名
        try:
            from urllib.parse import urlparse
            domain = urlparse(feed_url).netloc
            return domain
        except:
            return feed_url

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

    def _get_short_url(self, url: str) -> str:
        """获取短 URL 用于日志"""
        if len(url) > 50:
            return url[:47] + "..."
        return url


# 使用示例
if __name__ == '__main__':
    from config.sources_v2 import NEWS_SOURCES_V2
    
    crawler = MultiSourceCrawler(NEWS_SOURCES_V2)
    news = crawler.crawl_all()
    
    # 按来源类型统计
    stats = {}
    for item in news:
        source_type = item.get('source_type', 'unknown')
        stats[source_type] = stats.get(source_type, 0) + 1
    
    print("\n爬取统计:")
    for source_type, count in stats.items():
        print(f"  {source_type}: {count} 条")
