# 实体知识库关联服务
# 复用 AI 输出的 entities 字段，自动关联到知识库

import logging
import requests
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 后端 API 地址
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3001')

# 实体激活阈值（被提及多少次后创建知识库页面）
ENTITY_ACTIVATION_THRESHOLD = int(os.getenv('ENTITY_ACTIVATION_THRESHOLD', '3'))

# 跳过实体关联的分类（节省 token）
SKIP_ENTITY_CATEGORIES = {'entertainment_sports', 'anime', 'one_piece', 'tcg'}


class EntityService:
    """实体知识库关联服务"""
    
    def __init__(self, ai_processor=None):
        """
        初始化实体服务
        
        Args:
            ai_processor: AI 处理器，用于生成实体时间轴（可选）
        """
        self.api_base = f"{BACKEND_URL}/api/entities"
        self.ai_processor = ai_processor
        logger.info(f"实体服务初始化，API: {self.api_base}, 激活阈值: {ENTITY_ACTIVATION_THRESHOLD}")
    
    def process_brief_entities(self, brief: Dict, brief_id: str) -> int:
        """
        处理简报中的实体，关联到知识库
        
        流程：
        1. 查找实体是否存在
        2. 如果存在且 news_count > 0（已激活），直接关联新闻
        3. 如果存在但未激活，增加提及计数，检查是否达到阈值
        4. 如果不存在，创建并记录提及
        5. 达到阈值时激活实体（可选：AI生成时间轴）
        
        Args:
            brief: 简报数据（含 entities 字段）
            brief_id: 已保存的简报 ID
            
        Returns:
            成功关联的实体数量
        """
        # 跳过特定分类的实体识别（娱乐、动漫、OP、TCG）
        category = brief.get('category', '')
        if category in SKIP_ENTITY_CATEGORIES:
            logger.debug(f"跳过实体识别: 分类 {category} 在排除列表中")
            return 0
        
        entities = brief.get('entities', [])
        if not entities:
            return 0
        
        linked_count = 0
        date_str = datetime.now().strftime('%Y-%m-%d')
        category = brief.get('category', 'general')
        
        for entity_data in entities:
            try:
                name = entity_data.get('name', '').strip()
                if not name:
                    continue
                
                # 1. 查找或记录提及
                entity_id, is_active = self._find_or_mention_entity(entity_data)
                if not entity_id:
                    continue
                
                # 2. 只有已激活的实体才关联新闻
                if is_active:
                    success = self._link_news_to_entity(
                        entity_id=entity_id,
                        brief_id=brief_id,
                        date=date_str,
                        category=category,
                        relevance=entity_data.get('relevance', '')
                    )
                    
                    if success:
                        linked_count += 1
                        logger.debug(f"实体关联成功: {name} -> {brief_id}")
                else:
                    logger.debug(f"实体未激活，跳过关联: {name}")
                    
            except Exception as e:
                logger.warning(f"处理实体失败 [{entity_data.get('name')}]: {e}")
                continue
        
        return linked_count
    
    def _find_or_mention_entity(self, entity_data: Dict) -> tuple:
        """
        查找实体，如果不存在则记录提及
        
        Returns:
            (entity_id, is_active): 实体ID 和 是否已激活
        """
        name = entity_data.get('name', '').strip()
        entity_type = entity_data.get('type', 'concept')
        context = entity_data.get('context', '')
        
        # 类型映射
        type_map = {
            'company': 'company',
            'person': 'person',
            'tech': 'concept',
            'concept': 'concept',
            'event': 'event'
        }
        entity_type = type_map.get(entity_type, 'concept')
        
        try:
            # 1. 先搜索是否存在
            resp = requests.get(
                f"{self.api_base}/search/{requests.utils.quote(name)}",
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    entity = data['data']
                    entity_id = str(entity['_id'])
                    
                    # 已激活（news_count > 0 或 is_preset）
                    if entity.get('news_count', 0) > 0 or entity.get('is_preset'):
                        return (entity_id, True)
                    
                    # 未激活，增加提及计数
                    mention_count = self._increment_mention(entity_id)
                    
                    # 检查是否达到阈值
                    if mention_count >= ENTITY_ACTIVATION_THRESHOLD:
                        self._activate_entity(entity_id, name, entity_type, context)
                        return (entity_id, True)
                    
                    return (entity_id, False)
            
            # 2. 不存在，记录提及
            resp = requests.post(
                f"{self.api_base}/mention",
                json={
                    'name': name,
                    'type': entity_type,
                    'context': context
                },
                timeout=5
            )
            
            if resp.status_code in [200, 201]:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    entity_id = str(data['data']['_id'])
                    mention_count = data.get('mention_count', 1)
                    
                    # 检查是否达到阈值（首次可能就达到，比如阈值=1）
                    if mention_count >= ENTITY_ACTIVATION_THRESHOLD:
                        self._activate_entity(entity_id, name, entity_type, context)
                        return (entity_id, True)
                    
                    logger.info(f"记录实体提及: {name} (count={mention_count})")
                    return (entity_id, False)
            
            logger.warning(f"记录提及失败 [{name}]: {resp.status_code}")
            return (None, False)
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"实体 API 请求失败 [{name}]: {e}")
            return (None, False)
    
    def _increment_mention(self, entity_id: str) -> int:
        """增加提及计数，返回新的计数"""
        try:
            resp = requests.post(
                f"{self.api_base}/mention",
                json={'entity_id': entity_id},
                timeout=5
            )
            if resp.status_code == 200:
                return resp.json().get('mention_count', 0)
        except:
            pass
        return 0
    
    def _activate_entity(self, entity_id: str, name: str, entity_type: str, context: str):
        """激活实体，可选生成 AI 时间轴"""
        logger.info(f"激活实体: {name} ({entity_type})")
        
        base_timeline = []
        description = context
        
        # 如果有 AI 处理器，生成时间轴
        if self.ai_processor:
            try:
                result = self._generate_timeline(name, entity_type)
                if result:
                    base_timeline = result.get('timeline', [])
                    if result.get('description'):
                        description = result['description']
                    logger.info(f"AI 生成时间轴: {name}, {len(base_timeline)} 个节点")
            except Exception as e:
                logger.warning(f"AI 生成时间轴失败 [{name}]: {e}")
        
        # 调用激活 API
        try:
            resp = requests.post(
                f"{self.api_base}/{entity_id}/activate",
                json={
                    'base_timeline': base_timeline,
                    'description': description
                },
                timeout=10
            )
            if resp.status_code == 200:
                logger.info(f"实体激活成功: {name}")
            else:
                logger.warning(f"实体激活失败 [{name}]: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"激活 API 请求失败 [{name}]: {e}")
    
    def _generate_timeline(self, name: str, entity_type: str) -> Optional[Dict]:
        """调用 AI 生成实体时间轴"""
        if not self.ai_processor:
            return None
        
        type_label = {
            'company': '公司',
            'person': '人物',
            'concept': '概念/技术',
            'event': '事件'
        }.get(entity_type, '实体')
        
        prompt = f"""为以下实体生成简要历史时间轴和介绍：

实体名称: {name}
实体类型: {type_label}

要求：
1. description: 一句话介绍（30-80字）
2. timeline: 5-8个关键历史节点，只包含公认的、可查证的重大事件
3. 时间格式: YYYY.MM 或 YYYY
4. 按时间正序排列

输出JSON格式（不要其他文字）:
{{"description": "...", "timeline": [{{"date": "YYYY.MM", "event": "..."}}]}}"""

        try:
            result = self.ai_processor._call_api(prompt, max_tokens=600)
            if result:
                # 解析 JSON
                if '```json' in result:
                    result = result.split('```json')[1].split('```')[0]
                elif '```' in result:
                    result = result.split('```')[1].split('```')[0]
                
                data = json.loads(result.strip())
                
                # 格式化 timeline
                if 'timeline' in data:
                    data['timeline'] = [
                        {'date': t.get('date', ''), 'event': t.get('event', ''), 'importance': 'milestone'}
                        for t in data['timeline'] if t.get('date') and t.get('event')
                    ]
                
                return data
        except Exception as e:
            logger.warning(f"解析 AI 时间轴响应失败: {e}")
        
        return None
    
    def _link_news_to_entity(self, entity_id: str, brief_id: str, 
                              date: str, category: str, relevance: str) -> bool:
        """关联新闻到实体"""
        try:
            resp = requests.post(
                f"{self.api_base}/{entity_id}/link-news",
                json={
                    'brief_id': brief_id,
                    'date': date,
                    'category': category,
                    'relevance': relevance
                },
                timeout=5
            )
            return resp.status_code in [200, 201]
        except requests.exceptions.RequestException as e:
            logger.warning(f"关联新闻失败: {e}")
            return False
