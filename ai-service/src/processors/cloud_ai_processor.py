import requests
import json
from typing import Dict, Optional
import logging
import os

logger = logging.getLogger(__name__)


class CloudAIProcessor:
    """使用云端AI API进行处理（OpenAI/Claude）"""

    def __init__(self, provider: str = 'openai'):
        self.provider = provider.lower()

        if self.provider == 'openai':
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

    def generate(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """生成文本"""
        if self.provider == 'openai':
            return self._call_openai(prompt, max_tokens)
        elif self.provider == 'claude':
            return self._call_claude(prompt, max_tokens)

    def summarize_news(self, title: str, content: str, prompt_template: str) -> Optional[str]:
        """新闻摘要"""
        prompt = prompt_template.format(title=title, content=content[:500])
        summary = self.generate(prompt, max_tokens=150)
        return summary

    def classify_news(self, title: str, summary: str, prompt_template: str) -> str:
        """新闻分类"""
        prompt = prompt_template.format(title=title, summary=summary)
        category = self.generate(prompt, max_tokens=20)

        if category:
            # 清理和验证分类结果
            category = category.lower().strip()
            valid_categories = [
                'finance', 'technology', 'health', 'new_energy',
                'automotive', 'robotics', 'ai', 'general'
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
            # 1. 生成摘要
            summary = self.ai.summarize_news(
                news_item['title'],
                news_item['content'],
                summarize_prompt
            )

            if not summary:
                logger.warning(f"摘要生成失败: {news_item['title']}")
                summary = news_item['content'][:100] + '...'

            # 2. 分类
            category = self.ai.classify_news(
                news_item['title'],
                summary,
                classify_prompt
            )

            # 3. 构建处理后的新闻
            processed_news = {
                'title': news_item['title'],
                'summary': summary,
                'category': category,
                'source': news_item['source'],
                'source_url': news_item['source_url'],
                'link': news_item['link'],
                'published': news_item['published'],
                'created_at': news_item.get('created_at')
            }

            logger.info(f"处理完成: [{category}] {news_item['title'][:30]}...")
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
