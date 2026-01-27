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
            # 添加超时保护
            import socket
            socket.setdefaulttimeout(10)  # 10秒超时

            feed = feedparser.parse(feed_url)
            news_items = []

            for entry in feed.entries[:20]:  # 每个源取最新20条（阶段2：完整方案）
                news_item = {
                    'title': entry.get('title', ''),
                    'content': self._extract_content(entry),
                    'link': entry.get('link', ''),
                    'image': self._extract_image(entry),
                    'video': self._extract_video(entry),  # 添加视频提取（可选）
                    'published': self._parse_date(entry),
                    'source': feed.feed.get('title', feed_url),
                    'source_url': feed_url,
                    'raw_data': entry
                }
                news_items.append(news_item)

            logger.info(f"从 {self._get_short_url(feed_url)} 爬取到 {len(news_items)} 条新闻")
            # 添加超时重置
            socket.setdefaulttimeout(None)
            return news_items

        except Exception as e:
            logger.error(f"爬取RSS失败 {self._get_short_url(feed_url)}: {str(e)}")
            socket.setdefaulttimeout(None)
            return []

    def _get_short_url(self, url: str) -> str:
        """获取简短的URL用于日志"""
        if len(url) > 60:
            return url[:57] + "..."
        return url

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

    def _extract_image(self, entry) -> str:
        """提取新闻图片"""
        image_url = None

        # 尝试从media:content提取
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('url'):
                    # 检查是否是图片类型
                    media_type = media.get('type', '').lower()
                    url_lower = media.get('url', '').lower()
                    if 'image' in media_type or 'jpg' in url_lower or 'png' in url_lower or 'jpeg' in url_lower or 'webp' in url_lower:
                        logger.info(f"  从 media:content 找到图片: {media.get('url', '')}")
                        image_url = media.get('url', '')
                        break

        # 尝试从media:thumbnail提取
        if not image_url and hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            for thumbnail in entry.media_thumbnail:
                if thumbnail.get('url'):
                    logger.info(f"  从 media:thumbnail 找到图片: {thumbnail.get('url', '')}")
                    image_url = thumbnail.get('url', '')
                    break

        # 尝试从enclosure提取
        if not image_url and hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                enclosure_type = enclosure.get('type', '').lower()
                if 'image' in enclosure_type:
                    logger.info(f"  从 enclosure 找到图片: {enclosure.get('href', '')}")
                    image_url = enclosure.get('href', '')
                    break

        # 尝试从summary/description的HTML中提取第一张图片
        if not image_url:
            content = entry.get('summary', '') or entry.get('description', '')
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    logger.info(f"  从HTML img标签找到图片: {img.get('src', '')}")
                    image_url = img.get('src', '')

                # 尝试从media标签提取
                if not image_url:
                    media_tags = soup.find_all('media:thumbnail')
                    for media_tag in media_tags:
                        url = media_tag.get('url', '')
                        if url:
                            logger.info(f"  从 media:thumbnail标签找到图片: {url}")
                            image_url = url
                            break

                # 尝试从og:image元标签提取
                if not image_url:
                    og_image = soup.find('meta', property='og:image')
                    if og_image and og_image.get('content'):
                        logger.info(f"  从 og:image 找到图片: {og_image.get('content', '')}")
                        image_url = og_image.get('content', '')

        if image_url:
            logger.debug(f"  最终图片URL: {image_url}")
        else:
            logger.debug(f"  未找到图片")

        return image_url

    def _extract_video(self, entry) -> str:
        """提取新闻视频（可选，保守实现）"""
        video_url = None

        try:
            # 从media:content提取视频
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('url'):
                        media_type = media.get('type', '').lower()
                        url_lower = media.get('url', '').lower()
                        # 检查是否是视频类型
                        if 'video' in media_type or '.mp4' in url_lower or '.webm' in url_lower or '.mov' in url_lower:
                            logger.info(f"  从 media:content 找到视频: {media.get('url', '')}")
                            video_url = media.get('url', '')
                            break

            # 从enclosure提取视频
            if not video_url and hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    enclosure_type = enclosure.get('type', '').lower()
                    enclosure_url = enclosure.get('href', '').lower()
                    if 'video' in enclosure_type or '.mp4' in enclosure_url or '.webm' in enclosure_url:
                        logger.info(f"  从 enclosure 找到视频: {enclosure.get('href', '')}")
                        video_url = enclosure.get('href', '')
                        break

            if video_url:
                logger.debug(f"  最终视频URL: {video_url}")

        except Exception as e:
            # 视频提取失败不影响整体流程
            logger.debug(f"  视频提取失败（不影响功能）: {str(e)}")
            pass

        return video_url

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
        total_feeds = len(self.rss_feeds)

        for idx, feed_url in enumerate(self.rss_feeds, 1):
            try:
                # 每批10个源显示一次进度
                if idx % 10 == 1:
                    logger.info(f"正在爬取第 {idx}-{min(idx+9, total_feeds)}/{total_feeds} 个新闻源...")
                news = self.crawl_rss(feed_url)
                all_news.extend(news)
            except Exception as e:
                logger.error(f"爬取新闻源 {idx} 失败: {str(e)}")
                continue

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
