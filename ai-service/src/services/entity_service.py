# 实体知识库关联服务
# 复用 AI 输出的 entities 字段，自动关联到知识库
# 同时支持预置实体的自动匹配（基于标题/摘要文本）

import logging
import requests
import json
import os
import re
from typing import Dict, List, Optional, Set
from datetime import datetime

logger = logging.getLogger(__name__)

# 后端 API 地址
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3001')

# 实体激活阈值（被提及多少次后创建知识库页面）
ENTITY_ACTIVATION_THRESHOLD = int(os.getenv('ENTITY_ACTIVATION_THRESHOLD', '3'))

# 跳过实体关联的分类（节省 token）
SKIP_ENTITY_CATEGORIES = {'entertainment_sports', 'anime', 'one_piece', 'tcg'}

# 预置实体缓存（启动时加载）
_preset_entities_cache: List[Dict] = []
_preset_cache_loaded = False


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
        
        # 加载预置实体缓存
        self._load_preset_entities()
    
    def _load_preset_entities(self):
        """加载所有预置实体到缓存（用于文本匹配）"""
        global _preset_entities_cache, _preset_cache_loaded
        
        if _preset_cache_loaded:
            return
        
        try:
            # 获取所有预置实体（is_preset=true 或 news_count>0）
            resp = requests.get(
                f"{self.api_base}",
                params={'limit': 500},  # 获取足够多的实体
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    entities = data['data']
                    # 只缓存已激活的实体（is_preset=true 或有新闻关联的）
                    for entity in entities:
                        if entity.get('is_preset') or entity.get('news_count', 0) > 0:
                            _preset_entities_cache.append({
                                'id': str(entity['_id']),
                                'name': entity['name'],
                                'aliases': entity.get('aliases', []),
                                'type': entity.get('type', 'concept')
                            })
                    
                    _preset_cache_loaded = True
                    logger.info(f"预置实体缓存已加载: {len(_preset_entities_cache)} 个实体")
        except Exception as e:
            logger.warning(f"加载预置实体缓存失败: {e}")
    
    def refresh_preset_cache(self):
        """强制刷新预置实体缓存"""
        global _preset_entities_cache, _preset_cache_loaded
        _preset_entities_cache = []
        _preset_cache_loaded = False
        self._load_preset_entities()
        logger.info("预置实体缓存已刷新")
    
    def _match_preset_entities(self, text: str) -> List[Dict]:
        """
        在文本中匹配预置实体
        
        Args:
            text: 要匹配的文本（标题+摘要）
            
        Returns:
            匹配到的实体列表 [{'id': ..., 'name': ..., 'type': ...}]
        """
        if not _preset_entities_cache:
            self._load_preset_entities()
        
        matched = []
        matched_ids: Set[str] = set()
        
        for entity in _preset_entities_cache:
            entity_id = entity['id']
            if entity_id in matched_ids:
                continue
            
            # 检查主名称
            name = entity['name']
            if name and len(name) >= 2 and name in text:
                matched.append(entity)
                matched_ids.add(entity_id)
                continue
            
            # 检查别名
            for alias in entity.get('aliases', []):
                if alias and len(alias) >= 2 and alias in text:
                    matched.append(entity)
                    matched_ids.add(entity_id)
                    break
        
        return matched
    
    def process_brief_entities(self, brief: Dict, brief_id: str) -> int:
        """
        处理简报中的实体，关联到知识库
        
        流程：
        1. 先基于标题/摘要匹配预置实体（知名实体）
        2. 再处理 AI 识别的 entities 字段（非知名实体）
        3. 关联新闻到所有匹配的实体
        
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
        
        linked_count = 0
        date_str = datetime.now().strftime('%Y-%m-%d')
        category = brief.get('category', 'general')
        linked_entity_ids: Set[str] = set()
        
        # === 第一步：匹配预置实体（基于标题+摘要文本） ===
        title = brief.get('title', '') or brief.get('title_zh', '')
        summary = brief.get('summary', '')
        search_text = f"{title} {summary}"
        
        preset_matches = self._match_preset_entities(search_text)
        
        for entity in preset_matches:
            entity_id = entity['id']
            if entity_id in linked_entity_ids:
                continue
            
            try:
                success = self._link_news_to_entity(
                    entity_id=entity_id,
                    brief_id=brief_id,
                    date=date_str,
                    category=category,
                    relevance=f"文本匹配: {entity['name']}"
                )
                
                if success:
                    linked_count += 1
                    linked_entity_ids.add(entity_id)
                    logger.debug(f"预置实体关联成功: {entity['name']} -> {brief_id}")
            except Exception as e:
                logger.warning(f"预置实体关联失败 [{entity['name']}]: {e}")
        
        # === 第二步：处理 AI 识别的实体（非知名实体） ===
        entities = brief.get('entities', [])
        
        for entity_data in entities:
            try:
                name = entity_data.get('name', '').strip()
                if not name:
                    continue
                
                # 1. 查找或记录提及
                entity_id, is_active = self._find_or_mention_entity(entity_data)
                if not entity_id:
                    continue
                
                # 跳过已经关联过的（避免和预置实体重复）
                if entity_id in linked_entity_ids:
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
                        linked_entity_ids.add(entity_id)
                        logger.debug(f"实体关联成功: {name} -> {brief_id}")
                else:
                    logger.debug(f"实体未激活，跳过关联: {name}")
                    
            except Exception as e:
                logger.warning(f"处理实体失败 [{entity_data.get('name')}]: {e}")
                continue
        
        if linked_count > 0:
            logger.info(f"简报 {brief_id} 关联了 {linked_count} 个实体")
        
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
