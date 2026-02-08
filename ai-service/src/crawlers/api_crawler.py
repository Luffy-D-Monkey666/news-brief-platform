"""
官方 API 爬虫示例
需要申请各平台的 API Key
"""

import requests
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class TwitterAPICrawler:
    """Twitter 官方 API 爬虫 (需要 Twitter API Key)"""
    
    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_API_BEARER_TOKEN')
        if not self.bearer_token:
            logger.warning("未设置 TWITTER_API_BEARER_TOKEN，Twitter API 爬虫不可用")
        
        self.base_url = "https://api.twitter.com/2"
    
    def crawl_user_tweets(self, username: str, max_results: int = 20) -> List[Dict]:
        """获取指定用户的推文"""
        if not self.bearer_token:
            return []
        
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        
        # 1. 获取用户ID
        user_url = f"{self.base_url}/users/by/username/{username}"
        user_resp = requests.get(user_url, headers=headers)
        
        if user_resp.status_code != 200:
            logger.error(f"获取Twitter用户失败: {username}")
            return []
        
        user_id = user_resp.json()['data']['id']
        
        # 2. 获取用户推文
        tweets_url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,entities"
        }
        
        tweets_resp = requests.get(tweets_url, headers=headers, params=params)
        
        if tweets_resp.status_code != 200:
            logger.error(f"获取推文失败: {tweets_resp.text}")
            return []
        
        data = tweets_resp.json()
        tweets = data.get('data', [])
        
        # 转换为统一格式
        news_list = []
        for tweet in tweets:
            news_list.append({
                'title': tweet['text'][:100] + '...' if len(tweet['text']) > 100 else tweet['text'],
                'content': tweet['text'],
                'link': f"https://twitter.com/{username}/status/{tweet['id']}",
                'published': tweet['created_at'],
                'source': f"@{username} (Twitter)",
                'source_type': 'twitter'
            })
        
        return news_list


class WeiboAPICrawler:
    """微博官方 API 爬虫 (需要微博开放平台 App Key)"""
    
    def __init__(self):
        self.app_key = os.getenv('WEIBO_APP_KEY')
        self.app_secret = os.getenv('WEIBO_APP_SECRET')
        self.access_token = os.getenv('WEIBO_ACCESS_TOKEN')
        
        if not all([self.app_key, self.app_secret, self.access_token]):
            logger.warning("微博 API 配置不完整，爬虫不可用")
    
    def crawl_user_weibo(self, uid: str, count: int = 20) -> List[Dict]:
        """获取指定用户的微博"""
        if not self.access_token:
            return []
        
        url = "https://api.weibo.com/2/statuses/user_timeline.json"
        params = {
            "access_token": self.access_token,
            "uid": uid,
            "count": count
        }
        
        resp = requests.get(url, params=params)
        
        if resp.status_code != 200:
            logger.error(f"获取微博失败: {resp.text}")
            return []
        
        data = resp.json()
        statuses = data.get('statuses', [])
        
        news_list = []
        for status in statuses:
            news_list.append({
                'title': status['text'][:100] + '...' if len(status['text']) > 100 else status['text'],
                'content': status['text'],
                'link': status['url'] or f"https://weibo.com/{uid}/{status['id']}",
                'published': status['created_at'],
                'source': f"{status['user']['screen_name']} (微博)",
                'source_type': 'weibo'
            })
        
        return news_list


# 使用示例
if __name__ == '__main__':
    # Twitter API 需要申请：
    # https://developer.twitter.com/en/portal/dashboard
    
    # 微博 API 需要申请：
    # https://open.weibo.com/
    
    twitter = TwitterAPICrawler()
    # tweets = twitter.crawl_user_tweets('elonmusk')
    # print(f"获取到 {len(tweets)} 条推文")
    
    weibo = WeiboAPICrawler()
    # posts = weibo.crawl_user_weibo('1659809157')  # 李想的UID
    # print(f"获取到 {len(posts)} 条微博")
