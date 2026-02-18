"""
话题聚合服务
基于标题相似度将新闻聚合成话题
"""
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

# 停用词（中英文）
STOP_WORDS = {
    # 中文
    '的', '了', '是', '在', '和', '与', '及', '或', '等', '将', '被', '对', '为', '到', '从',
    '上', '下', '中', '内', '外', '前', '后', '新', '大', '小', '多', '少', '全', '各',
    '这', '那', '其', '该', '某', '每', '已', '正', '可', '能', '会', '要', '也', '都',
    '发布', '公布', '宣布', '表示', '称', '报道', '消息', '显示', '据', '称',
    # 英文
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'can', 'must', 'shall', 'need', 'dare', 'ought', 'used',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'between',
    'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
    'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also',
    'now', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
    'new', 'first', 'last', 'long', 'great', 'little', 'other', 'old', 'right',
    'big', 'high', 'different', 'small', 'large', 'next', 'early', 'young',
    'important', 'few', 'public', 'bad', 'same', 'able'
}

# 重要实体关键词（公司、产品、人名等）
IMPORTANT_ENTITIES = {
    # 科技公司
    'openai', 'google', 'apple', 'microsoft', 'nvidia', 'tesla', 'meta', 'amazon',
    'anthropic', 'deepmind', 'huggingface', 'github', 'openai',
    # 产品
    'chatgpt', 'gpt-4', 'gpt-5', 'claude', 'gemini', 'copilot', 'iphone', 'ipad',
    'cybertruck', 'model 3', 'model y',
    # 人物
    'elon musk', 'sam altman', 'jensen huang', 'tim cook', 'satya nadella',
    # 中文
    '特斯拉', '苹果', '谷歌', '微软', '英伟达', '华为', '比亚迪', '小米',
    '马斯克', '库克', '雷军', '任正非',
    # 海贼王
    'one piece', '海贼王', '路飞', 'luffy', '尾田', 'oda',
    # TCG
    '游戏王', 'yugioh', 'pokemon tcg', 'opcg', 'ptcg'
}


def extract_keywords(text: str) -> set:
    """从文本提取关键词"""
    if not text:
        return set()
    
    # 转小写
    text_lower = text.lower()
    
    # 提取中文词（简单分词：连续中文字符）
    chinese_words = re.findall(r'[\u4e00-\u9fff]+', text)
    
    # 提取英文词
    english_words = re.findall(r'[a-zA-Z]+', text_lower)
    
    # 合并
    all_words = set()
    
    for word in chinese_words:
        if len(word) >= 2 and word not in STOP_WORDS:
            all_words.add(word)
    
    for word in english_words:
        if len(word) >= 3 and word not in STOP_WORDS:
            all_words.add(word)
    
    # 检查重要实体
    for entity in IMPORTANT_ENTITIES:
        if entity in text_lower:
            all_words.add(entity)
    
    return all_words


def calculate_similarity(keywords1: set, keywords2: set) -> float:
    """计算两组关键词的Jaccard相似度"""
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = keywords1 & keywords2
    union = keywords1 | keywords2
    
    if not union:
        return 0.0
    
    # 基础Jaccard相似度
    jaccard = len(intersection) / len(union)
    
    # 如果有重要实体匹配，提高权重
    entity_match = intersection & IMPORTANT_ENTITIES
    if entity_match:
        jaccard = min(1.0, jaccard + 0.2 * len(entity_match))
    
    return jaccard


class TopicService:
    """话题聚合服务"""
    
    def __init__(self, db):
        self.db = db
        self.topics_collection = db['topics']
        self.briefs_collection = db['briefs']
        
        # 创建索引
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """确保必要的索引存在"""
        try:
            self.topics_collection.create_index('created_at')
            self.topics_collection.create_index('updated_at')
            self.topics_collection.create_index('is_active')
            self.briefs_collection.create_index('topic_id')
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def find_or_create_topic(self, brief: Dict) -> Optional[str]:
        """
        为新闻找到匹配的话题，或创建新话题
        返回 topic_id
        """
        title = brief.get('title', '')
        category = brief.get('category', 'general')
        
        # 提取关键词
        brief_keywords = extract_keywords(title)
        if brief.get('summary'):
            # 只取摘要前200字提取关键词
            brief_keywords |= extract_keywords(brief['summary'][:200])
        
        if not brief_keywords:
            return None
        
        # 查找最近24小时内同分类的活跃话题
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        active_topics = list(self.topics_collection.find({
            'category': category,
            'is_active': True,
            'updated_at': {'$gte': cutoff_time}
        }).sort('updated_at', -1).limit(50))
        
        # 计算与每个话题的相似度
        best_match = None
        best_similarity = 0.0
        
        for topic in active_topics:
            topic_keywords = set(topic.get('keywords', []))
            similarity = calculate_similarity(brief_keywords, topic_keywords)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = topic
        
        # 相似度阈值：0.35（比较宽松，允许相关新闻聚合）
        SIMILARITY_THRESHOLD = 0.35
        
        if best_match and best_similarity >= SIMILARITY_THRESHOLD:
            # 加入已有话题
            topic_id = best_match['_id']
            
            # 更新话题
            merged_keywords = list(set(best_match.get('keywords', [])) | brief_keywords)[:20]
            
            self.topics_collection.update_one(
                {'_id': topic_id},
                {
                    '$set': {
                        'keywords': merged_keywords,
                        'updated_at': datetime.utcnow(),
                        'latest_title': title
                    },
                    '$inc': {'brief_count': 1}
                }
            )
            
            logger.info(f"📎 新闻加入话题 (相似度{best_similarity:.2f}): {title[:30]}...")
            return str(topic_id)
        
        else:
            # 创建新话题
            topic_doc = {
                'title': title,  # 用第一条新闻标题作为话题标题
                'keywords': list(brief_keywords)[:20],
                'category': category,
                'brief_count': 1,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'latest_title': title
            }
            
            result = self.topics_collection.insert_one(topic_doc)
            topic_id = result.inserted_id
            
            logger.info(f"📁 创建新话题: {title[:30]}...")
            return str(topic_id)
    
    def get_topic_briefs(self, topic_id: str, limit: int = 10) -> List[Dict]:
        """获取话题下的所有新闻"""
        from bson import ObjectId
        
        briefs = list(self.briefs_collection.find(
            {'topic_id': topic_id}
        ).sort('created_at', -1).limit(limit))
        
        return briefs
    
    def get_hot_topics(self, hours: int = 24, limit: int = 10) -> List[Dict]:
        """获取热门话题（按新闻数量排序）"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        topics = list(self.topics_collection.find({
            'is_active': True,
            'updated_at': {'$gte': cutoff_time},
            'brief_count': {'$gte': 2}  # 至少2条新闻才算话题
        }).sort('brief_count', -1).limit(limit))
        
        return topics
    
    def cleanup_old_topics(self, days: int = 7):
        """清理过期话题"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        result = self.topics_collection.update_many(
            {'updated_at': {'$lt': cutoff_time}},
            {'$set': {'is_active': False}}
        )
        
        if result.modified_count > 0:
            logger.info(f"🧹 清理了 {result.modified_count} 个过期话题")
