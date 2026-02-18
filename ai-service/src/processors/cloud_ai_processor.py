import requests
import json
from typing import Dict, Optional, List
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

logger = logging.getLogger(__name__)


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
        
        result = self._call_api(prompt, max_tokens=400)
        
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
                'source': news_item['source'],
                'source_url': news_item['source_url'],
                'source_tier': get_source_tier(news_item['source_url']),  # 来源可信度
                'link': news_item['link'],
                'image': news_item.get('image'),
                'video': news_item.get('video'),
                'published': news_item['published'],
                'created_at': news_item.get('created_at')
            }

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
