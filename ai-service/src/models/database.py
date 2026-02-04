from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class NewsDatabase:
    """新闻数据库操作类"""

    def __init__(self, mongodb_uri: str):
        self.client = MongoClient(mongodb_uri)

        # 从连接字符串中提取数据库名
        # 如果URI包含数据库名，使用它；否则使用默认值
        if '/' in mongodb_uri.rsplit('/', 1)[-1]:
            db_name = mongodb_uri.rsplit('/', 1)[-1].split('?')[0]  # 移除查询参数
        else:
            db_name = 'news-brief'  # 统一默认值与settings.py一致

        logger.info(f"使用数据库: {db_name}")
        self.db = self.client[db_name]
        self.news_collection = self.db['news']
        self.briefs_collection = self.db['briefs']

        # 创建索引
        self.news_collection.create_index('link', unique=True)
        self.news_collection.create_index([('published', -1)])
        self.briefs_collection.create_index([('created_at', -1)])
        self.briefs_collection.create_index('category')

    def save_raw_news(self, news_item: Dict) -> Optional[str]:
        """保存原始新闻"""
        try:
            news_item['created_at'] = datetime.now()
            result = self.news_collection.insert_one(news_item)
            return str(result.inserted_id)
        except Exception as e:
            if 'duplicate key' in str(e):
                logger.debug(f"新闻已存在: {news_item.get('link')}")
            else:
                logger.error(f"保存新闻失败: {str(e)}")
            return None

    def save_brief(self, brief: Dict) -> Optional[str]:
        """保存简报"""
        try:
            brief['created_at'] = datetime.now()
            brief['is_pushed'] = False
            result = self.briefs_collection.insert_one(brief)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"保存简报失败: {str(e)}")
            return None

    def get_unpushed_briefs(self, limit: int = 10) -> List[Dict]:
        """获取未推送的简报"""
        briefs = self.briefs_collection.find(
            {'is_pushed': False}
        ).sort('created_at', -1).limit(limit)
        return list(briefs)

    def mark_as_pushed(self, brief_id: str):
        """标记为已推送"""
        from bson.objectid import ObjectId
        self.briefs_collection.update_one(
            {'_id': ObjectId(brief_id)},
            {'$set': {'is_pushed': True, 'pushed_at': datetime.now()}}
        )

    def get_latest_briefs(self, category: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """获取最新简报"""
        query = {}
        if category:
            query['category'] = category

        briefs = self.briefs_collection.find(query).sort('created_at', -1).limit(limit)
        return list(briefs)

    def check_news_exists(self, link: str) -> bool:
        """检查新闻是否存在"""
        return self.news_collection.find_one({'link': link}) is not None

    def check_news_exists_batch(self, links: List[str]) -> set:
        """批量检查新闻是否存在（优化性能）"""
        try:
            logger.info(f"批量查询: 检查 {len(links)} 个链接...")
            existing = self.news_collection.find(
                {'link': {'$in': links}},
                {'link': 1, '_id': 0}
            )
            # 立即转换为列表并关闭cursor
            existing_list = list(existing)
            logger.info(f"批量查询结果: 找到 {len(existing_list)} 个已存在的链接")
            # 返回已存在的链接集合
            return {doc['link'] for doc in existing_list}
        except Exception as e:
            logger.error(f"批量检查新闻失败: {str(e)}", exc_info=True)
            return set()
