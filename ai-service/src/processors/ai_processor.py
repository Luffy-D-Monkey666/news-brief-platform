import requests
import json
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class OllamaProcessor:
    """使用Ollama进行AI处理"""

    def __init__(self, host: str, model: str):
        self.host = host
        self.model = model
        self.api_url = f"{host}/api/generate"

    def generate(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """调用Ollama生成文本"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": max_tokens
                }
            }

            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"Ollama API错误: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Ollama调用失败: {str(e)}")
            return None

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
    """新闻处理器"""

    def __init__(self, ollama_host: str, model_name: str):
        self.ollama = OllamaProcessor(ollama_host, model_name)

    def process_news(self, news_item: Dict, summarize_prompt: str, classify_prompt: str) -> Dict:
        """处理单条新闻"""
        try:
            # 1. 生成摘要
            summary = self.ollama.summarize_news(
                news_item['title'],
                news_item['content'],
                summarize_prompt
            )

            if not summary:
                logger.warning(f"摘要生成失败: {news_item['title']}")
                summary = news_item['content'][:100] + '...'

            # 2. 分类
            category = self.ollama.classify_news(
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
