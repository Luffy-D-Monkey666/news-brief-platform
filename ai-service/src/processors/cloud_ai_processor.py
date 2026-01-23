import requests
import json
from typing import Dict, Optional
import logging
import os

logger = logging.getLogger(__name__)


class CloudAIProcessor:
    """使用云端AI API进行处理（OpenAI/Claude/HuggingFace）"""

    def __init__(self, provider: str = 'openai'):
        self.provider = provider.lower()

        if self.provider == 'openai':
            self.api_key = os.getenv('OPENAI_API_KEY')
            self.api_url = 'https://api.openai.com/v1/chat/completions'
            self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        elif self.provider == 'deepseek':
            # DeepSeek中国AI（超便宜，兼容OpenAI格式）
            self.api_key = os.getenv('DEEPSEEK_API_KEY')
            self.api_url = 'https://api.deepseek.com/v1/chat/completions'
            self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            logger.info("使用DeepSeek AI（中国）")
        elif self.provider == 'claude':
            self.api_key = os.getenv('CLAUDE_API_KEY')
            self.api_url = 'https://api.anthropic.com/v1/messages'
            self.model = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')
        elif self.provider == 'huggingface':
            # Hugging Face免费推理API（需要注册免费API Key）
            self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')
            if not self.api_key:
                logger.warning("未设置HUGGINGFACE_API_KEY，将使用基础文本处理")
                self.api_key = 'no_api'  # 标记为无API模式
            self.api_url = 'https://api-inference.huggingface.co/models/google/flan-t5-xxl'
            self.model = 'google/flan-t5-xxl'
            logger.info("使用Hugging Face API")
            return  # 跳过API key验证
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        if not self.api_key:
            raise ValueError(f"API key not found for {provider}")

    def _call_openai(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """调用OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': self.model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
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
                return result['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"OpenAI API错误: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"OpenAI调用失败: {str(e)}")
            return None

    def _call_claude(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """调用Claude API"""
        try:
            headers = {
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json'
            }

            data = {
                'model': self.model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
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
                return result['content'][0]['text'].strip()
            else:
                logger.error(f"Claude API错误: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Claude调用失败: {str(e)}")
            return None

    def _call_huggingface(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """调用Hugging Face免费推理API"""
        try:
            # 如果没有API Key，使用简单的文本处理作为后备
            if self.api_key == 'no_api':
                logger.warning("无Hugging Face API Key，返回原文")
                return None

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }

            data = {
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': max_tokens,
                    'temperature': 0.3,
                    'do_sample': True
                }
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=60  # Hugging Face免费API可能较慢
            )

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                elif isinstance(result, dict):
                    return result.get('generated_text', '').strip()
                return None
            elif response.status_code == 503:
                # 模型正在加载，等待重试
                logger.warning("Hugging Face模型正在加载，等待10秒后重试...")
                import time
                time.sleep(10)
                # 重试一次
                response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', '').strip()
                return None
            else:
                logger.error(f"Hugging Face API错误: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Hugging Face调用失败: {str(e)}")
            return None

    def generate(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """生成文本"""
        if self.provider == 'openai' or self.provider == 'deepseek':
            # DeepSeek使用OpenAI兼容格式
            return self._call_openai(prompt, max_tokens)
        elif self.provider == 'claude':
            return self._call_claude(prompt, max_tokens)
        elif self.provider == 'huggingface':
            return self._call_huggingface(prompt, max_tokens)

    def summarize_news(self, title: str, content: str, prompt_template: str) -> tuple[Optional[str], Optional[str]]:
        """新闻摘要 - 返回(中文标题, 详细总结)"""
        prompt = prompt_template.format(title=title, content=content[:1000])  # 增加输入内容长度
        result = self.generate(prompt, max_tokens=500)  # 增加输出长度以支持详细总结

        if result:
            # 解析返回的中文标题和详细总结（按行分割）
            lines = result.strip().split('\n')
            lines = [line.strip() for line in lines if line.strip()]

            if len(lines) >= 2:
                chinese_title = lines[0]
                chinese_summary = '\n'.join(lines[1:])
                return chinese_title, chinese_summary
            elif len(lines) == 1:
                # 如果只有一行，作为总结，标题保持原样
                return title, lines[0]

        return None, None

    def classify_news(self, title: str, summary: str, prompt_template: str) -> str:
        """新闻分类"""
        prompt = prompt_template.format(title=title, summary=summary)
        category = self.generate(prompt, max_tokens=20)

        if category:
            # 清理和验证分类结果
            category = category.lower().strip()
            valid_categories = [
                'op_card_game', 'op_merchandise',
                'ai_robotics', 'ev_automotive', 'finance_investment',
                'business_tech', 'politics_world', 'economy_policy',
                'health_medical', 'energy_environment', 'entertainment_sports',
                'general'
            ]

            for cat in valid_categories:
                if cat in category:
                    return cat

        return 'general'  # 默认分类


class NewsProcessor:
    """新闻处理器（云端版本）"""

    def __init__(self, ai_provider: str = 'openai'):
        """
        初始化处理器

        Args:
            ai_provider: 'openai' 或 'claude'
        """
        try:
            self.ai = CloudAIProcessor(ai_provider)
            logger.info(f"使用云端AI: {ai_provider}")
        except ValueError as e:
            logger.error(f"AI初始化失败: {str(e)}")
            raise

    def process_news(self, news_item: Dict, summarize_prompt: str, classify_prompt: str) -> Dict:
        """处理单条新闻"""
        try:
            # 1. 生成中文标题和摘要
            chinese_title, chinese_summary = self.ai.summarize_news(
                news_item['title'],
                news_item['content'],
                summarize_prompt
            )

            if not chinese_title or not chinese_summary:
                logger.warning(f"摘要生成失败: {news_item['title']}")
                chinese_title = news_item['title']
                chinese_summary = news_item['content'][:100] + '...'

            # 2. 分类
            category = self.ai.classify_news(
                chinese_title,
                chinese_summary,
                classify_prompt
            )

            # 3. 构建处理后的新闻
            processed_news = {
                'title': chinese_title,  # 使用中文标题
                'summary': chinese_summary,  # 使用中文简报
                'category': category,
                'source': news_item['source'],
                'source_url': news_item['source_url'],
                'link': news_item['link'],
                'image': news_item.get('image'),
                'published': news_item['published'],
                'created_at': news_item.get('created_at')
            }

            logger.info(f"处理完成: [{category}] {chinese_title[:30]}...")
            return processed_news

        except Exception as e:
            logger.error(f"新闻处理失败: {str(e)}")
            return None

    def batch_process(self, news_list: list, summarize_prompt: str, classify_prompt: str) -> list:
        """批量处理新闻"""
        processed = []
        for news in news_list:
            result = self.process_news(news, summarize_prompt, classify_prompt)
            if result:
                processed.append(result)

        logger.info(f"批量处理完成: {len(processed)}/{len(news_list)}")
        return processed
