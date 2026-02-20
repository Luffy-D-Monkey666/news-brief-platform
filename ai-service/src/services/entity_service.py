# 实体知识库关联服务
# 复用 AI 输出的 entities 字段，自动关联到知识库

import logging
import requests
import os
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 后端 API 地址
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3001')


class EntityService:
    """实体知识库关联服务"""
    
    def __init__(self):
        self.api_base = f"{BACKEND_URL}/api/entities"
        logger.info(f"实体服务初始化，API: {self.api_base}")
    
    def process_brief_entities(self, brief: Dict, brief_id: str) -> int:
        """
        处理简报中的实体，关联到知识库
        
        Args:
            brief: 简报数据（含 entities 字段）
            brief_id: 已保存的简报 ID
            
        Returns:
            成功关联的实体数量
        """
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
                
                # 1. 查找或创建实体
                entity_id = self._find_or_create_entity(entity_data)
                if not entity_id:
                    continue
                
                # 2. 关联新闻到实体
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
                    
            except Exception as e:
                logger.warning(f"处理实体失败 [{entity_data.get('name')}]: {e}")
                continue
        
        return linked_count
    
    def _find_or_create_entity(self, entity_data: Dict) -> Optional[str]:
        """查找实体，不存在则创建"""
        name = entity_data.get('name', '').strip()
        entity_type = entity_data.get('type', 'concept')
        
        # 类型映射
        type_map = {
            'company': 'company',
            'person': 'person',
            'tech': 'concept',  # 技术术语映射到 concept
            'concept': 'concept',
            'event': 'event'
        }
        entity_type = type_map.get(entity_type, 'concept')
        
        try:
            # 1. 先搜索是否存在
            resp = requests.get(
                f"{self.api_base}/search/{name}",
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    return str(data['data']['_id'])
            
            # 2. 不存在，创建新实体
            create_data = {
                'name': name,
                'type': entity_type,
                'description': entity_data.get('context', ''),
                'aliases': [],
                'base_timeline': []
            }
            
            # 如果有 timeline，添加到基础时间线
            timeline = entity_data.get('timeline', [])
            if timeline:
                create_data['base_timeline'] = [
                    {'date': t.get('date', ''), 'event': t.get('event', ''), 'importance': 'normal'}
                    for t in timeline if t.get('date') and t.get('event')
                ]
            
            resp = requests.post(
                self.api_base,
                json=create_data,
                timeout=5
            )
            
            if resp.status_code == 201:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    logger.info(f"创建新实体: {name} ({entity_type})")
                    return str(data['data']['_id'])
            elif resp.status_code == 409:
                # 已存在（并发创建），获取现有的
                data = resp.json()
                if data.get('data'):
                    return str(data['data']['_id'])
            
            logger.warning(f"创建实体失败 [{name}]: {resp.status_code} - {resp.text[:100]}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"实体 API 请求失败 [{name}]: {e}")
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
