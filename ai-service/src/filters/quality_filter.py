"""
内容质量评估模块

用于评估新闻重要性和过滤低质量内容
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class ContentQualityFilter:
    """内容质量过滤器"""

    def __init__(self):
        # 低价值关键词（通用）- 出现在标题中会降低评分
        # 优化：精简列表，只保留明显低质量的内容，避免误伤正常新闻
        self.low_value_keywords = [
            # 教程指南类（保留明显教程性质的词）
            '入门指南', '新手指南', '基础教程', '初级教程',
            'tutorial for beginners', 'beginner guide', 'how to ',

            # 推荐排行类（保留明显的列表类内容）
            'top 10', 'top 5', 'best of 20', '必看清单',

            # 评测对比类（保留明显的个人体验类）
            '上手体验', '使用感受', '个人测评',

            # 营销软文类
            '限时优惠', '折扣促销', '秒杀活动',
            'buy now', 'limited deal', 'flash sale',

            # 个人观点类
            '我认为', '我的观点', '个人看法',
            '如何学会', '怎样做到', '心得体会',

            # 低质量标题（严格保留）
            '震惊', '竟然', '居然', '万万没想到', '不敢相信',
            '!!!', '???', '！！！', '？？？',
            
            # Twitter/X 特定低质量内容
            'rt @', 'retweet', '早上好', '晚上好',
            'good morning', 'good night', 'happy birthday',
            '节日快乐', '周末愉快', '打卡', '签到',
        ]

        # 高价值关键词（按分类）- 出现在标题中会提高评分
        self.high_value_keywords = {
            'ai_technology': [
                '发布', '推出', '开源', '研究', '论文', '突破',
                'release', 'launch', 'open source', 'research', 'paper', 'breakthrough',
                '官方', 'official', '宣布', 'announce'
            ],
            'robotics': [
                '研发', '量产', '商用', '应用', '技术', '系统',
                '新型', '创新', 'innovative', 'commercial', 'production'
            ],
            'ai_coding_agent': [
                '发布', '更新', '版本', '功能', '开源', 'Agent', 'Coding',
                'release', 'update', 'version', 'feature', 'open source', 'agent', 'coding'
            ],
            'anime_otaku': [
                '新番', '动画', '漫画', '剧场版', '声优', '制作',
                'anime', 'manga', 'new season', 'movie', 'voice actor', 'studio'
            ],
            'semiconductors': [
                '量产', '代工', '制程', '工艺', '晶圆厂',
                '订单', '财报', 'mass production', 'foundry', 'process'
            ],
            'opcg': [
                '禁卡', '限制', 'ban list', 'meta', '赛事', '锦标赛',
                '发售', '新卡', 'release', 'tournament', 'championship'
            ],
            'automotive': [
                '发布', '上市', '销量', '财报', '新车',
                'release', 'launch', 'sales', 'earnings', 'new model'
            ],
            'consumer_electronics': [
                '发布', '上市', '新品', '曝光', '官方',
                'release', 'launch', 'new product', 'leak', 'official'
            ],
            'one_piece': [
                '新章', '剧场版', '官方', '尾田', '发售',
                'new chapter', 'movie', 'official', 'oda', 'release'
            ],
            'podcasts': [
                '新节目', '新播客', '新系列', '首播',
                'new show', 'new podcast', 'premiere', 'launch',
                '嘉宾', 'guest', '访谈', 'interview',
                'episode', 'ep', '第', '期',
                '故事', 'story', '历史', 'history',
                '商业', 'business', '心理', 'psychology'
            ]
        }

    def evaluate_importance(self, title: str, content: str, category: str) -> int:
        """
        评估新闻重要性

        Args:
            title: 新闻标题
            content: 新闻内容（可选，当前未使用）
            category: 新闻分类

        Returns:
            评分（1-10），8-10为高价值，5-7为中等，1-4为低价值
        """
        score = 5  # 基础分

        title_lower = title.lower()

        # 检查低价值关键词（-2分，原来是-3分，降低惩罚力度）
        for keyword in self.low_value_keywords:
            if keyword in title_lower:
                score -= 2
                logger.debug(f"低价值关键词: {keyword} in {title[:50]}")
                break  # 只扣一次分

        # 检查高价值关键词（+3分，原来是+2分，提高奖励力度）
        category_keywords = self.high_value_keywords.get(category, [])
        for keyword in category_keywords:
            if keyword in title_lower:
                score += 3
                logger.debug(f"高价值关键词: {keyword} in {title[:50]}")
                break  # 只加一次分

        # 确保分数在1-10范围内
        score = max(1, min(10, score))

        return score

    def should_process(self, title: str, category: str, threshold: int = 3) -> bool:
        """
        判断是否应该处理这条新闻

        Args:
            title: 新闻标题
            category: 新闻分类
            threshold: 最低评分阈值（低于此分数不处理）

        Returns:
            True表示应该处理，False表示跳过
        """
        score = self.evaluate_importance(title, '', category)

        if score < threshold:
            logger.info(f"⏭️  跳过低质量新闻（评分{score} < {threshold}）: {title[:50]}...")
            return False
        
        logger.debug(f"✅ 通过质量检查（评分{score} >= {threshold}）: {title[:50]}...")
        return True

    def filter_news_list(self, news_list: List[Dict], category_key: str = 'category') -> List[Dict]:
        """
        批量过滤新闻列表

        Args:
            news_list: 新闻列表
            category_key: 分类字段名

        Returns:
            过滤后的新闻列表
        """
        filtered = []
        skipped_count = 0

        for news in news_list:
            title = news.get('title', '')
            category = news.get(category_key, 'general')
            
            # 记录过滤前的评分详情
            score = self.evaluate_importance(title, '', category)
            news['quality_score'] = score

            if self.should_process(title, category, threshold=3):
                filtered.append(news)
            else:
                skipped_count += 1
                logger.debug(f"  被过滤: {title[:60]}... (评分: {score})")

        if skipped_count > 0:
            logger.info(f"📊 质量过滤: 保留 {len(filtered)} 条，跳过 {skipped_count} 条低质量新闻")
            logger.info(f"   通过率: {len(filtered)}/{len(news_list)} ({len(filtered)/len(news_list)*100:.1f}%)")

        return filtered


# 播客内容识别辅助函数（用于未来可能的优化）
def is_podcast_content(title: str, content: str) -> bool:
    """
    识别是否为播客单集内容

    播客内容特征：
    - 标题包含"EP"、"第X期"、"嘉宾"
    - 内容是节目描述

    注：当前"播客推荐"分类就是用于展示播客内容，
         此函数保留用于未来可能的过滤优化。
    """
    podcast_indicators = [
        'ep ', 'ep.', 'episode', '第', '期',
        '嘉宾', 'guest', '本期', 'this episode',
        '播客', 'podcast', '节目', 'show'
    ]

    title_lower = title.lower()
    content_lower = content.lower()

    for indicator in podcast_indicators:
        if indicator in title_lower or indicator in content_lower:
            return True

    return False
