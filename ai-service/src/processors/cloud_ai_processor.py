import requests
import json
import time
from typing import Dict, Optional, List, Tuple
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from threading import Lock
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ============================================================
# P2 优化：Token 使用统计
# ============================================================
@dataclass
class TokenStats:
    """Token 使用统计"""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_requests: int = 0
    stage1_requests: int = 0  # 第一阶段请求数
    stage2_requests: int = 0  # 第二阶段请求数
    failed_requests: int = 0
    last_reset: datetime = field(default_factory=datetime.now)
    
    def add(self, input_tokens: int, output_tokens: int, stage: int = 1):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_requests += 1
        if stage == 1:
            self.stage1_requests += 1
        else:
            self.stage2_requests += 1
    
    def add_failure(self):
        self.failed_requests += 1
    
    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens
    
    @property
    def estimated_cost_cny(self) -> float:
        """估算成本（DeepSeek 价格：输入 ¥1/1M，输出 ¥2/1M）"""
        input_cost = self.total_input_tokens / 1_000_000 * 1
        output_cost = self.total_output_tokens / 1_000_000 * 2
        return input_cost + output_cost
    
    def reset(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0
        self.stage1_requests = 0
        self.stage2_requests = 0
        self.failed_requests = 0
        self.last_reset = datetime.now()
    
    def summary(self) -> str:
        elapsed = (datetime.now() - self.last_reset).total_seconds() / 3600
        return (
            f"📊 Token 统计 (最近 {elapsed:.1f}h):\n"
            f"   总请求: {self.total_requests} (S1: {self.stage1_requests}, S2: {self.stage2_requests}, 失败: {self.failed_requests})\n"
            f"   输入: {self.total_input_tokens:,} tokens\n"
            f"   输出: {self.total_output_tokens:,} tokens\n"
            f"   总计: {self.total_tokens:,} tokens\n"
            f"   估算成本: ¥{self.estimated_cost_cny:.4f}"
        )


# 全局 token 统计（线程安全）
_token_stats = TokenStats()
_token_stats_lock = Lock()


def get_token_stats() -> TokenStats:
    """获取全局 token 统计"""
    return _token_stats


def reset_token_stats():
    """重置 token 统计"""
    global _token_stats
    with _token_stats_lock:
        _token_stats.reset()


# 股票服务（延迟导入以避免循环依赖）
_stock_service = None

def get_stock_service():
    """延迟加载股票服务"""
    global _stock_service
    if _stock_service is None:
        try:
            from services.stock_service import StockService
            _stock_service = StockService()
            logger.info("股票服务初始化成功")
        except Exception as e:
            logger.warning(f"股票服务初始化失败: {e}")
            _stock_service = False  # 标记为不可用
    return _stock_service if _stock_service else None


class CloudAIProcessor:
    """使用云端AI API进行处理（DeepSeek/OpenAI/Claude）"""

    def __init__(self, provider: str = 'deepseek'):
        self.provider = provider.lower()

        if self.provider == 'deepseek':
            self.api_key = os.getenv('DEEPSEEK_API_KEY')
            self.api_url = 'https://api.deepseek.com/v1/chat/completions'
            self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            logger.info("使用DeepSeek AI")
        elif self.provider == 'openai':
            self.api_key = os.getenv('OPENAI_API_KEY')
            self.api_url = 'https://api.openai.com/v1/chat/completions'
            self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        elif self.provider == 'claude':
            self.api_key = os.getenv('CLAUDE_API_KEY')
            self.api_url = 'https://api.anthropic.com/v1/messages'
            self.model = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        if not self.api_key:
            raise ValueError(f"API key not found for {provider}")

    def _call_api(self, prompt: str, max_tokens: int = 500, retries: int = 3, 
                  stage: int = 1) -> Tuple[Optional[str], int, int]:
        """
        调用API（支持OpenAI格式）
        
        增加指数退避重试策略：
        - 429 (Too Many Requests) 自动重试
        - 500/502/503 服务器错误重试
        
        Returns:
            (content, input_tokens, output_tokens)
        """
        last_error = None
        
        for attempt in range(retries):
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }

                data = {
                    'model': self.model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': max_tokens,
                    'temperature': 0.3
                }

                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # P2 优化：记录 token 使用
                    usage = result.get('usage', {})
                    input_tokens = usage.get('prompt_tokens', 0)
                    output_tokens = usage.get('completion_tokens', 0)
                    
                    with _token_stats_lock:
                        _token_stats.add(input_tokens, output_tokens, stage)
                    
                    return content, input_tokens, output_tokens
                elif response.status_code == 429:
                    # 速率限制，指数退避
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    logger.warning(f"API 速率限制 (429)，等待 {wait_time}s 后重试 ({attempt + 1}/{retries})")
                    time.sleep(wait_time)
                    last_error = f"429 Too Many Requests"
                    continue
                elif response.status_code in [500, 502, 503]:
                    # 服务器错误，重试
                    wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                    logger.warning(f"API 服务器错误 ({response.status_code})，等待 {wait_time}s 后重试 ({attempt + 1}/{retries})")
                    time.sleep(wait_time)
                    last_error = f"{response.status_code} Server Error"
                    continue
                else:
                    logger.error(f"API错误: {response.status_code} - {response.text[:200]}")
                    with _token_stats_lock:
                        _token_stats.add_failure()
                    return None, 0, 0

            except requests.exceptions.Timeout:
                wait_time = (2 ** attempt) * 1
                logger.warning(f"API 超时，等待 {wait_time}s 后重试 ({attempt + 1}/{retries})")
                time.sleep(wait_time)
                last_error = "Timeout"
                continue
            except Exception as e:
                logger.error(f"API调用失败: {str(e)}")
                with _token_stats_lock:
                    _token_stats.add_failure()
                return None, 0, 0
        
        logger.error(f"API调用失败，已重试 {retries} 次: {last_error}")
        with _token_stats_lock:
            _token_stats.add_failure()
        return None, 0, 0

    def process_news_two_stage(self, title: str, content: str, 
                                 quick_prompt: str, detailed_prompt: str) -> Optional[Dict]:
        """
        两阶段处理（P0 优化）：
        1. 快速分类：用简化 prompt，输出 title_zh/category/importance/summary
        2. 详细处理：仅对 breaking/high 新闻调用第二阶段补充详细字段
        
        预计节省 50-60% token（大多数 normal 新闻只需一阶段）
        """
        # 第一阶段：快速分类（所有新闻）
        # P2 优化：normal 新闻用 400 字内容，减少 token
        content_truncated = content[:400] if content else ""
        prompt = quick_prompt.format(title=title, content=content_truncated)
        
        result, _, _ = self._call_api(prompt, max_tokens=300, stage=1)
        
        if not result:
            return None
        
        try:
            # 解析第一阶段结果
            if '```json' in result:
                result = result.split('```json')[1].split('```')[0]
            elif '```' in result:
                result = result.split('```')[1].split('```')[0]
            
            data = json.loads(result.strip())
            
            # 验证必要字段
            if not all(k in data for k in ['title_zh', 'category', 'summary']):
                logger.warning(f"第一阶段缺少必要字段: {result[:100]}")
                return None
            
            # 验证分类
            valid_categories = [
                'ai_technology', 'robotics', 'ai_programming', 'semiconductors',
                'automotive', 'consumer_electronics', 'podcasts', 'finance_investment',
                'business_tech', 'politics_world', 'economy_policy', 'health_medical',
                'energy_environment', 'entertainment_sports', 'anime', 'one_piece', 
                'tcg', 'general'
            ]
            if data.get('category') not in valid_categories:
                data['category'] = 'general'
            
            # 验证重要性
            importance = data.get('importance', 'normal')
            if importance not in ['breaking', 'high', 'normal']:
                importance = 'normal'
            data['importance'] = importance
            
            # 初始化所有可选字段为默认值
            data['key_metrics'] = []
            data['action_advice'] = None
            data['background'] = None
            data['tech_insight'] = None
            data['funding_history'] = None
            data['supply_chain_insight'] = None
            data['entities'] = []
            
            # ========================================
            # 第二阶段：仅对 breaking/high 新闻补充详细信息
            # ========================================
            if importance in ['breaking', 'high']:
                logger.debug(f"📊 {importance} 新闻，启动第二阶段处理: {data['title_zh'][:30]}")
                
                # 用更长的内容进行详细处理
                content_detailed = content[:800] if content else ""
                detailed_prompt_filled = detailed_prompt.format(
                    title_zh=data['title_zh'],
                    category=data['category'],
                    summary=data['summary'],
                    content=content_detailed
                )
                
                detailed_result, _, _ = self._call_api(detailed_prompt_filled, max_tokens=500, stage=2)
                
                if detailed_result:
                    try:
                        if '```json' in detailed_result:
                            detailed_result = detailed_result.split('```json')[1].split('```')[0]
                        elif '```' in detailed_result:
                            detailed_result = detailed_result.split('```')[1].split('```')[0]
                        
                        detailed_data = json.loads(detailed_result.strip())
                        
                        # 合并详细字段
                        if 'key_metrics' in detailed_data and isinstance(detailed_data['key_metrics'], list):
                            data['key_metrics'] = detailed_data['key_metrics']
                        if 'background' in detailed_data:
                            data['background'] = detailed_data['background']
                        if 'action_advice' in detailed_data:
                            data['action_advice'] = detailed_data['action_advice']
                        if 'tech_insight' in detailed_data:
                            data['tech_insight'] = detailed_data['tech_insight']
                        if 'funding_history' in detailed_data:
                            data['funding_history'] = detailed_data['funding_history']
                        if 'supply_chain_insight' in detailed_data:
                            data['supply_chain_insight'] = detailed_data['supply_chain_insight']
                        if 'entities' in detailed_data and isinstance(detailed_data['entities'], list):
                            data['entities'] = detailed_data['entities']
                        
                        logger.debug(f"✅ 第二阶段处理完成: {data['title_zh'][:30]}")
                    except json.JSONDecodeError as e:
                        logger.warning(f"第二阶段 JSON 解析失败: {e}")
                else:
                    logger.warning(f"第二阶段 API 调用失败: {data['title_zh'][:30]}")
            
            return data
            
        except json.JSONDecodeError as e:
            logger.warning(f"第一阶段 JSON 解析失败: {e}, 原文: {result[:100]}")
            return None
    
    def process_news_combined(self, title: str, content: str, prompt_template: str) -> Optional[Dict]:
        """
        合并处理：一次API调用完成标题翻译+分类+摘要
        返回: {"title_zh": str, "category": str, "summary": str} 或 None
        
        注意：此方法保留用于兼容，建议使用 process_news_two_stage() 节省 token
        """
        # 截取内容前800字符（节省token）
        content_truncated = content[:800] if content else ""
        prompt = prompt_template.format(title=title, content=content_truncated)
        
        result, _, _ = self._call_api(prompt, max_tokens=800, stage=1)
        
        if not result:
            return None
            
        try:
            # 尝试解析JSON
            # 处理可能的markdown代码块
            if '```json' in result:
                result = result.split('```json')[1].split('```')[0]
            elif '```' in result:
                result = result.split('```')[1].split('```')[0]
            
            data = json.loads(result.strip())
            
            # 验证必要字段
            if 'title_zh' in data and 'category' in data and 'summary' in data:
                # 验证分类是否有效
                valid_categories = [
                    'ai_technology', 'robotics', 'ai_programming', 'semiconductors',
                    'automotive', 'consumer_electronics', 'podcasts', 'finance_investment',
                    'business_tech', 'politics_world', 'economy_policy', 'health_medical',
                    'energy_environment', 'entertainment_sports', 'anime', 'one_piece', 
                    'tcg', 'general'
                ]
                if data['category'] not in valid_categories:
                    data['category'] = 'general'
                
                # 验证重要性字段
                if 'importance' not in data or data['importance'] not in ['breaking', 'high', 'normal']:
                    data['importance'] = 'normal'
                
                # 处理行动建议字段（可能为null）
                if 'action_advice' not in data:
                    data['action_advice'] = None
                
                # 处理关键指标字段
                if 'key_metrics' not in data or not isinstance(data['key_metrics'], list):
                    data['key_metrics'] = []
                else:
                    # 验证每个指标的格式
                    valid_metrics = []
                    for metric in data['key_metrics']:
                        if isinstance(metric, dict) and 'name' in metric and 'value' in metric:
                            valid_metrics.append({
                                'name': metric.get('name', ''),
                                'value': metric.get('value', 0),
                                'unit': metric.get('unit', ''),
                                'entity': metric.get('entity', '')
                            })
                    data['key_metrics'] = valid_metrics
                
                # 处理背景知识字段
                if 'background' not in data or data['background'] is None:
                    data['background'] = None
                elif isinstance(data['background'], dict):
                    # 验证背景知识格式
                    bg = data['background']
                    valid_bg = {
                        'context': bg.get('context', ''),
                        'timeline': []
                    }
                    if 'timeline' in bg and isinstance(bg['timeline'], list):
                        for item in bg['timeline'][:4]:  # 最多4条
                            if isinstance(item, dict) and 'date' in item and 'event' in item:
                                valid_bg['timeline'].append({
                                    'date': item.get('date', ''),
                                    'event': item.get('event', '')
                                })
                    data['background'] = valid_bg if valid_bg['context'] else None
                else:
                    data['background'] = None
                
                # 处理技术解读字段（仅ai_technology/robotics/ai_programming/semiconductors）
                if 'tech_insight' not in data or data['tech_insight'] is None:
                    data['tech_insight'] = None
                elif isinstance(data['tech_insight'], dict):
                    ti = data['tech_insight']
                    valid_ti = {
                        'principle': ti.get('principle', ''),
                        'comparison': ti.get('comparison', ''),
                        'maturity': ti.get('maturity', '商用落地')
                    }
                    # 验证maturity值
                    valid_maturities = ['实验室阶段', '小规模试用', '商用落地', '大规模应用']
                    if valid_ti['maturity'] not in valid_maturities:
                        valid_ti['maturity'] = '商用落地'
                    data['tech_insight'] = valid_ti if valid_ti['principle'] else None
                else:
                    data['tech_insight'] = None
                
                # 处理融资历史字段
                if 'funding_history' not in data or data['funding_history'] is None:
                    data['funding_history'] = None
                elif isinstance(data['funding_history'], dict):
                    fh = data['funding_history']
                    valid_fh = {
                        'company': fh.get('company', ''),
                        'rounds': [],
                        'total_funding': fh.get('total_funding', ''),
                        'valuation': fh.get('valuation', '')
                    }
                    if 'rounds' in fh and isinstance(fh['rounds'], list):
                        for r in fh['rounds'][:6]:  # 最多6轮
                            if isinstance(r, dict) and 'round' in r:
                                valid_fh['rounds'].append({
                                    'round': r.get('round', ''),
                                    'amount': r.get('amount', ''),
                                    'date': r.get('date', ''),
                                    'investors': r.get('investors', []) if isinstance(r.get('investors'), list) else []
                                })
                    data['funding_history'] = valid_fh if valid_fh['company'] else None
                else:
                    data['funding_history'] = None
                
                # 处理供应链视角字段（仅consumer_electronics/automotive）
                if 'supply_chain_insight' not in data or data['supply_chain_insight'] is None:
                    data['supply_chain_insight'] = None
                elif isinstance(data['supply_chain_insight'], dict):
                    sci = data['supply_chain_insight']
                    valid_sci = {
                        'impact': sci.get('impact', ''),
                        'related_companies': [],
                        'capacity_info': sci.get('capacity_info', '')
                    }
                    if 'related_companies' in sci and isinstance(sci['related_companies'], list):
                        for c in sci['related_companies'][:6]:  # 最多6家
                            if isinstance(c, dict) and 'name' in c:
                                valid_sci['related_companies'].append({
                                    'name': c.get('name', ''),
                                    'role': c.get('role', ''),
                                    'effect': c.get('effect', '中性')
                                })
                    data['supply_chain_insight'] = valid_sci if valid_sci['impact'] else None
                else:
                    data['supply_chain_insight'] = None
                
                # 处理关键实体字段（entities）
                if 'entities' not in data or not isinstance(data['entities'], list):
                    data['entities'] = []
                else:
                    valid_entities = []
                    valid_types = ['company', 'person', 'tech', 'concept', 'event']
                    for entity in data['entities'][:3]:  # 最多3个实体
                        if isinstance(entity, dict) and 'name' in entity and 'context' in entity:
                            entity_type = entity.get('type', 'concept')
                            if entity_type not in valid_types:
                                entity_type = 'concept'
                            
                            valid_entity = {
                                'name': entity.get('name', ''),
                                'type': entity_type,
                                'context': entity.get('context', ''),
                                'relevance': entity.get('relevance', ''),
                                'timeline': []
                            }
                            # 处理实体时间线
                            if 'timeline' in entity and isinstance(entity['timeline'], list):
                                for item in entity['timeline'][:2]:  # 最多2条
                                    if isinstance(item, dict) and 'date' in item and 'event' in item:
                                        valid_entity['timeline'].append({
                                            'date': item.get('date', ''),
                                            'event': item.get('event', '')
                                        })
                            valid_entities.append(valid_entity)
                    data['entities'] = valid_entities
                    
                return data
            else:
                logger.warning(f"JSON缺少必要字段: {result[:100]}")
                return None
                
        except json.JSONDecodeError as e:
            logger.warning(f"JSON解析失败: {e}, 原文: {result[:100]}")
            return None


class NewsProcessor:
    """新闻处理器（优化版：支持两阶段分级处理）"""

    def __init__(self, ai_provider: str = 'deepseek'):
        try:
            self.ai = CloudAIProcessor(ai_provider)
            logger.info(f"使用云端AI: {ai_provider}")
        except ValueError as e:
            logger.error(f"AI初始化失败: {str(e)}")
            raise
        
        # 是否启用两阶段处理（P0 优化）
        self.use_two_stage = os.getenv('USE_TWO_STAGE_PROCESSING', 'true').lower() == 'true'
        if self.use_two_stage:
            logger.info("✅ 两阶段分级处理已启用（预计节省 50-60% token）")
    
    def process_news_optimized(self, news_item: Dict, quick_prompt: str, detailed_prompt: str) -> Optional[Dict]:
        """
        处理单条新闻（两阶段分级处理，P0 优化版本）
        
        - 所有新闻用 quick_prompt 快速分类
        - 仅 breaking/high 新闻用 detailed_prompt 补充详情
        """
        try:
            result = self.ai.process_news_two_stage(
                news_item['title'],
                news_item.get('content', ''),
                quick_prompt,
                detailed_prompt
            )
            
            if not result:
                logger.warning(f"处理失败: {news_item['title'][:50]}")
                return None
            
            return self._build_processed_news(result, news_item)
            
        except Exception as e:
            logger.error(f"处理异常: {str(e)}")
            return None

    def process_news(self, news_item: Dict, process_prompt: str) -> Optional[Dict]:
        """处理单条新闻（合并摘要+分类为单次调用）- 兼容旧版"""
        try:
            # 单次API调用完成所有处理
            result = self.ai.process_news_combined(
                news_item['title'],
                news_item.get('content', ''),
                process_prompt
            )

            if not result:
                logger.warning(f"处理失败: {news_item['title'][:50]}")
                return None

            return self._build_processed_news(result, news_item)

        except Exception as e:
            logger.error(f"处理异常: {str(e)}")
            return None
    
    def _build_processed_news(self, result: Dict, news_item: Dict) -> Dict:
        """构建处理后的新闻对象（公共方法）"""
        # 导入来源分级函数
        from config.settings import get_source_tier
        
        # 构建处理后的新闻
        processed_news = {
            'title': result['title_zh'],
            'summary': result['summary'],
            'category': result['category'],
            'importance': result.get('importance', 'normal'),
            'action_advice': result.get('action_advice'),
            'key_metrics': result.get('key_metrics', []),  # 关键指标
            'background': result.get('background'),  # 背景知识+时间线
            'tech_insight': result.get('tech_insight'),  # 技术解读
            'funding_history': result.get('funding_history'),  # 融资历史
            'supply_chain_insight': result.get('supply_chain_insight'),  # 供应链视角
            'entities': result.get('entities', []),  # 关键实体背景
            'stock_info': None,  # 股票信息（将在下方填充）
            'source': news_item['source'],
            'source_url': news_item['source_url'],
            'source_tier': get_source_tier(news_item['source_url']),  # 来源可信度
            'link': news_item['link'],
            'image': news_item.get('image'),
            'video': news_item.get('video'),
            'published': news_item['published'],
            'created_at': news_item.get('created_at')
        }
        
        # 娱乐/动漫/OP/TCG 分类不需要实体信息（节省展示空间）
        skip_entity_categories = {'entertainment_sports', 'anime', 'one_piece', 'tcg'}
        if result['category'] in skip_entity_categories:
            processed_news['entities'] = []
        
        # 获取股票数据（仅针对 breaking/high 财经/商业类新闻，P1 优化）
        stock_categories = ['finance_investment', 'business_tech', 'automotive', 'consumer_electronics', 'economy_policy']
        importance = result.get('importance', 'normal')
        
        # P1 优化：只有 breaking/high 新闻才查询股票数据
        if result['category'] in stock_categories and importance in ['breaking', 'high']:
            try:
                stock_service = get_stock_service()
                if stock_service:
                    stock_info = stock_service.get_stock_info_from_text(
                        result['title_zh'],
                        news_item.get('content', '')
                    )
                    if stock_info:
                        processed_news['stock_info'] = stock_info
                        logger.info(f"📈 添加股票数据: {stock_info['ticker']} - {stock_info.get('name', '')}")
            except Exception as e:
                logger.warning(f"获取股票数据失败: {e}")

        importance_icon = '🔴' if importance == 'breaking' else '🟡' if importance == 'high' else '⚪'
        logger.info(f"{importance_icon} [{result['category']}] {result['title_zh'][:30]}...")
        return processed_news

    def batch_process(self, news_list: list, process_prompt: str, classify_prompt: str = None) -> list:
        """
        批量处理新闻（使用并发）
        注意：classify_prompt 参数保留以兼容旧代码，但不再使用
        """
        start_time = datetime.now()
        max_workers = int(os.getenv('AI_CONCURRENT_WORKERS', 5))

        logger.info(f"开始处理 {len(news_list)} 条新闻（{max_workers}线程，合并API模式）...")

        processed = []
        failed_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_news = {
                executor.submit(self.process_news, news, process_prompt): news
                for news in news_list
            }

            for i, future in enumerate(as_completed(future_to_news), 1):
                try:
                    result = future.result(timeout=60)
                    if result:
                        processed.append(result)
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    logger.error(f"处理超时或异常: {str(e)}")

                # 进度报告
                if i % 10 == 0:
                    logger.info(f"进度: {i}/{len(news_list)}")

        elapsed = (datetime.now() - start_time).total_seconds()
        success_rate = len(processed) / len(news_list) * 100 if news_list else 0

        logger.info(f"处理完成: {len(processed)}/{len(news_list)} ({success_rate:.1f}%)")
        logger.info(f"耗时: {elapsed:.1f}秒, 平均: {elapsed/len(news_list):.2f}秒/条" if news_list else "无新闻")

        return processed
    
    def batch_process_optimized(self, news_list: list, quick_prompt: str, detailed_prompt: str) -> list:
        """
        批量处理新闻（两阶段分级处理，P0 优化版本）
        
        Args:
            news_list: 新闻列表
            quick_prompt: 快速分类 prompt（所有新闻用）
            detailed_prompt: 详细处理 prompt（仅 breaking/high 用）
        """
        start_time = datetime.now()
        max_workers = int(os.getenv('AI_CONCURRENT_WORKERS', 5))

        logger.info(f"🚀 开始处理 {len(news_list)} 条新闻（{max_workers}线程，两阶段分级模式）...")

        processed = []
        failed_count = 0
        stage2_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_news = {
                executor.submit(self.process_news_optimized, news, quick_prompt, detailed_prompt): news
                for news in news_list
            }

            for i, future in enumerate(as_completed(future_to_news), 1):
                try:
                    result = future.result(timeout=90)  # 两阶段需要更长超时
                    if result:
                        processed.append(result)
                        if result.get('importance') in ['breaking', 'high']:
                            stage2_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    logger.error(f"处理超时或异常: {str(e)}")

                # 进度报告
                if i % 10 == 0:
                    logger.info(f"进度: {i}/{len(news_list)}")

        elapsed = (datetime.now() - start_time).total_seconds()
        success_rate = len(processed) / len(news_list) * 100 if news_list else 0
        stage2_rate = stage2_count / len(processed) * 100 if processed else 0

        logger.info(f"✅ 处理完成: {len(processed)}/{len(news_list)} ({success_rate:.1f}%)")
        logger.info(f"📊 两阶段处理: {stage2_count} 条 ({stage2_rate:.1f}%) 需要第二阶段")
        logger.info(f"💰 预计节省 token: {100 - stage2_rate:.1f}% 新闻仅用第一阶段")
        logger.info(f"⏱️ 耗时: {elapsed:.1f}秒, 平均: {elapsed/len(news_list):.2f}秒/条" if news_list else "无新闻")
        
        # P2 优化：输出 token 使用统计
        logger.info(_token_stats.summary())

        return processed
