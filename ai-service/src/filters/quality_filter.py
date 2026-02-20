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
        # 高质量来源白名单 - 跳过质量过滤（仅限低频高质量源）
        self.trusted_sources = {
            'nature.com',           # Nature（日更 5-15）
            'science.org',          # Science（日更 3-10）
            'technologyreview.com', # MIT Technology Review（日更 3-8）
            'economist.com',        # 经济学人（周刊，日更 5-10）
        }
        # 注：Reuters/BBC/NYT/Guardian/WSJ 等高频源仍走质量过滤，避免 token 暴增
        
        # 低价值关键词（通用）- 出现在标题中会降低评分
        # 注意：已移除可能误杀重要新闻的关键词（如"评测""体验""如何"等）
        self.low_value_keywords = [
            # 教程指南类（保留明确的入门教程）
            '教程', '指南', '入门', '新手', '基础', '初级',
            'tutorial', 'beginner', 'basics',

            # 推荐排行类
            '推荐', '排行', '榜单', 'top 10', 'top 5', 'best of',
            '必看', '必读', '必学', '精选', '合集',

            # 营销软文类
            '优惠', '折扣', '促销', '秒杀',
            'deal', 'discount',

            # 低质量标题（只保留明确的标题党）
            '震惊', '竟然', '居然', '万万没想到', '不敢相信',
            '？？', '！！',
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
            'ai_programming': [
                '发布', '更新', '版本', '功能', '开源',
                'release', 'update', 'version', 'feature', 'open source'
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

        # 检查低价值关键词（-3分）
        for keyword in self.low_value_keywords:
            if keyword in title_lower:
                score -= 3
                logger.debug(f"低价值关键词: {keyword} in {title[:50]}")
                break  # 只扣一次分

        # 检查高价值关键词（+2分）
        category_keywords = self.high_value_keywords.get(category, [])
        for keyword in category_keywords:
            if keyword in title_lower:
                score += 2
                logger.debug(f"高价值关键词: {keyword} in {title[:50]}")
                break  # 只加一次分

        # 确保分数在1-10范围内
        score = max(1, min(10, score))

        return score

    def should_process(self, title: str, category: str, threshold: int = 3, source_url: str = None) -> bool:
        """
        判断是否应该处理这条新闻

        Args:
            title: 新闻标题
            category: 新闻分类
            threshold: 最低评分阈值（低于此分数不处理）
            source_url: 来源 URL（用于白名单检查）

        Returns:
            True表示应该处理，False表示跳过
        """
        # 检查是否为可信来源（白名单）
        if source_url:
            for trusted in self.trusted_sources:
                if trusted in source_url.lower():
                    logger.debug(f"✅ 可信来源跳过过滤: {trusted} - {title[:40]}...")
                    return True
        
        score = self.evaluate_importance(title, '', category)

        if score < threshold:
            logger.info(f"⏭️  跳过低质量新闻（评分{score}）: {title[:50]}...")
            return False

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
        trusted_count = 0

        for news in news_list:
            title = news.get('title', '')
            category = news.get(category_key, 'general')
            source_url = news.get('source_url', '') or news.get('link', '')

            if self.should_process(title, category, source_url=source_url):
                # 添加质量评分到新闻数据
                news['quality_score'] = self.evaluate_importance(title, '', category)
                filtered.append(news)
                
                # 统计可信来源
                for trusted in self.trusted_sources:
                    if trusted in source_url.lower():
                        trusted_count += 1
                        break
            else:
                skipped_count += 1

        if skipped_count > 0 or trusted_count > 0:
            logger.info(f"📊 质量过滤: 保留 {len(filtered)} 条（含 {trusted_count} 条可信来源），跳过 {skipped_count} 条")

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
