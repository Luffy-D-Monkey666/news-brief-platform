import requests
import json
from typing import Dict, Optional, List
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

logger = logging.getLogger(__name__)

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

    def _call_api(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """调用API（支持OpenAI格式）"""
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
                return content
            else:
                logger.error(f"API错误: {response.status_code} - {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            logger.error("API调用超时")
            return None
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            return None

    def process_news_combined(self, title: str, content: str, prompt_template: str) -> Optional[Dict]:
        """
        合并处理：一次API调用完成标题翻译+分类+摘要
        返回: {"title_zh": str, "category": str, "summary": str} 或 None
        """
        # 截取内容前800字符（节省token）
        content_truncated = content[:800] if content else ""
        prompt = prompt_template.format(title=title, content=content_truncated)
        
        result = self._call_api(prompt, max_tokens=800)
        
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
    """新闻处理器（优化版：合并API调用）"""

    def __init__(self, ai_provider: str = 'deepseek'):
        try:
            self.ai = CloudAIProcessor(ai_provider)
            logger.info(f"使用云端AI: {ai_provider}")
        except ValueError as e:
            logger.error(f"AI初始化失败: {str(e)}")
            raise

    def process_news(self, news_item: Dict, process_prompt: str) -> Optional[Dict]:
        """处理单条新闻（合并摘要+分类为单次调用）"""
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
            
            # 获取股票数据（仅针对财经/商业/汽车/消费电子类新闻）
            stock_categories = ['finance_investment', 'business_tech', 'automotive', 'consumer_electronics', 'economy_policy']
            if result['category'] in stock_categories:
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

            importance_icon = '🔴' if result.get('importance') == 'breaking' else '🟡' if result.get('importance') == 'high' else '⚪'
            logger.info(f"{importance_icon} [{result['category']}] {result['title_zh'][:30]}...")
            return processed_news

        except Exception as e:
            logger.error(f"处理异常: {str(e)}")
            return None

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
