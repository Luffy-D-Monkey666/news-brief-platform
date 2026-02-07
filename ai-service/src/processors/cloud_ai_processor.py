import requests
import json
from typing import Dict, Optional, List
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

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
        elif self.provider == 'kimi':
            # Kimi (Moonshot AI) - 兼容OpenAI格式
            self.api_key = os.getenv('KIMI_API_KEY')
            self.api_url = 'https://api.moonshot.cn/v1/chat/completions'
            self.model = os.getenv('KIMI_MODEL', 'moonshot-v1-8k')
            logger.info("使用Kimi AI（Moonshot）")
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
            if not self.api_key:
                logger.error(f"❌ {self.provider.upper()} API Key 未设置")
                logger.error(f"   请设置环境变量: {self.provider.upper()}_API_KEY")
                return None

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

            logger.info(f"🤖 正在调用 {self.provider} API (model: {self.model})...")
            logger.debug(f"   API URL: {self.api_url}")
            logger.debug(f"   Prompt长度: {len(prompt)} 字符")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                logger.info(f"✅ {self.provider} API 调用成功，返回 {len(content)} 字符")
                logger.debug(f"   返回内容预览: {content[:100]}...")
                return content
            else:
                logger.error(f"❌ {self.provider} API错误: {response.status_code}")
                logger.error(f"   响应内容: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            logger.error(f"❌ {self.provider} API 调用超时（30秒）")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ {self.provider} API 连接失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ {self.provider} 调用失败: {str(e)}")
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
        if self.provider in ('openai', 'deepseek', 'kimi'):
            # DeepSeek和Kimi都使用OpenAI兼容格式
            return self._call_openai(prompt, max_tokens)
        elif self.provider == 'claude':
            return self._call_claude(prompt, max_tokens)
        elif self.provider == 'huggingface':
            return self._call_huggingface(prompt, max_tokens)

    def summarize_news(self, title: str, content: str, prompt_template: str) -> tuple[Optional[str], Optional[str]]:
        """新闻摘要 - 返回(中文标题, 详细总结)"""
        # 增加内容长度到3000字符，保留更多上下文信息
        content_truncated = content[:3000] if len(content) > 3000 else content
        prompt = prompt_template.format(title=title, content=content_truncated)
        # 增加输出长度以支持详细总结（无字数限制，让AI充分表达）
        result = self.generate(prompt, max_tokens=1500)

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
                'ai_technology', 'robotics', 'ai_coding_agent', 'semiconductors', 'opcg',
                'automotive', 'consumer_electronics', 'one_piece', 'podcasts',
                'finance_investment', 'business_tech', 'politics_world', 'economy_policy',
                'health_medical', 'energy_environment', 'entertainment_sports',
                'general'
            ]

            for cat in valid_categories:
                if cat in category:
                    return cat

        return 'general'  # 默认分类

    def process_combined(self, title: str, content: str, prompt_template: str) -> tuple[Optional[str], Optional[str], str]:
        """
        合并处理：一次调用完成摘要+分类 (Token优化: 节省50%)
        返回: (中文标题, 摘要, 分类)
        
        内容处理策略:
        - 限制输入内容长度，避免超出模型上下文限制
        - 优先保留文章开头部分（通常包含关键信息）
        """
        # 增加内容截断长度到3000字符，保留更多上下文
        content_truncated = content[:3000] if len(content) > 3000 else content
        prompt = prompt_template.format(title=title, content=content_truncated)
        # 增加max_tokens以支持更长摘要（无字数限制，让AI充分表达）
        result = self.generate(prompt, max_tokens=1500)

        if result:
            try:
                # 尝试解析JSON
                import json
                # 清理可能的markdown代码块标记
                cleaned = result.strip()
                if cleaned.startswith('```'):
                    # 移除开头的```json或```
                    cleaned = '\n'.join(cleaned.split('\n')[1:])
                if cleaned.endswith('```'):
                    # 移除结尾的```
                    cleaned = '\n'.join(cleaned.split('\n')[:-1])

                data = json.loads(cleaned.strip())
                chinese_title = data.get('title', title)
                chinese_summary = data.get('summary', '')
                category = data.get('category', 'general')

                # 验证分类
                valid_categories = [
                    'ai_technology', 'robotics', 'ai_coding_agent', 'semiconductors', 'opcg',
                    'automotive', 'consumer_electronics', 'one_piece', 'anime_otaku', 'podcasts',
                    'finance_investment', 'business_tech', 'politics_world', 'economy_policy',
                    'health_medical', 'energy_environment', 'entertainment_sports',
                    'general'
                ]

                if category not in valid_categories:
                    # 尝试从分类字符串中提取
                    for cat in valid_categories:
                        if cat in category.lower():
                            category = cat
                            break
                    else:
                        category = 'general'

                logger.debug(f"✅ 成功解析AI响应: 标题={chinese_title[:30]}..., 分类={category}")
                return chinese_title, chinese_summary, category

            except json.JSONDecodeError as e:
                logger.warning(f"⚠️ JSON解析失败: {e}")
                logger.debug(f"   AI返回内容: {result[:200]}...")
                # Fallback: 尝试分行解析
                lines = result.strip().split('\n')
                lines = [line.strip() for line in lines if line.strip()]
                if len(lines) >= 2:
                    logger.debug(f"   使用fallback解析: {len(lines)} 行")
                    return lines[0], '\n'.join(lines[1:-1]), lines[-1] if len(lines) > 2 else 'general'
            except Exception as e:
                logger.error(f"❌ 处理AI响应时出错: {str(e)}")

        logger.warning(f"⚠️ AI处理返回空结果，将使用fallback")
        return None, None, 'general'


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
                logger.warning(f"摘要生成失败，使用fallback: {news_item['title']}")
                chinese_title = news_item['title'][:100]  # 限制长度
                # fallback时保留更多内容（500字符）
                content = news_item['content']
                chinese_summary = content[:500] + '...' if len(content) > 500 else content
                if not chinese_summary:
                    chinese_summary = '暂无摘要'

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
                'video': news_item.get('video'),  # 添加video字段
                'published': news_item['published'],
                'created_at': news_item.get('created_at'),
                'source_type': news_item.get('source_type', 'rss')  # 保留来源类型
            }
            
            # 视频特有字段
            if news_item.get('source_type') == 'youtube':
                if 'video_duration' in news_item:
                    processed_news['video_duration'] = news_item['video_duration']
                if 'video_author' in news_item:
                    processed_news['video_author'] = news_item['video_author']
                if 'video_views' in news_item:
                    processed_news['video_views'] = news_item['video_views']

            logger.info(f"处理完成: [{category}] {chinese_title[:30]}...")
            return processed_news

        except Exception as e:
            logger.error(f"新闻处理失败: {str(e)}")
            return None

    def process_news_combined(self, news_item: Dict, combined_prompt: str) -> Dict:
        """
        使用合并提示词处理单条新闻 (Token优化: 一次调用完成摘要+分类)
        """
        try:
            original_title = news_item.get('title', '')
            content = news_item.get('content', '')
            
            logger.debug(f"📝 处理新闻: {original_title[:50]}...")
            
            # 使用合并提示词一次性完成摘要和分类
            chinese_title, chinese_summary, category = self.ai.process_combined(
                original_title,
                content,
                combined_prompt
            )

            if not chinese_title or not chinese_summary:
                logger.debug(f"   AI返回空结果，使用fallback处理")
                chinese_title = original_title[:100]
                # fallback时保留更多内容（500字符）
                chinese_summary = content[:500] + '...' if len(content) > 500 else content
                if not chinese_summary:
                    chinese_summary = '暂无摘要'
                category = 'general'
                logger.debug(f"   Fallback分类: {category}")
            else:
                logger.debug(f"   AI处理成功: 分类={category}")

            # 构建处理后的新闻
            processed_news = {
                'title': chinese_title,
                'summary': chinese_summary,
                'category': category,
                'source': news_item['source'],
                'source_url': news_item['source_url'],
                'link': news_item['link'],
                'image': news_item.get('image'),
                'video': news_item.get('video'),
                'published': news_item['published'],
                'created_at': news_item.get('created_at'),
                'source_type': news_item.get('source_type', 'rss')  # 保留来源类型
            }
            
            # 视频特有字段
            if news_item.get('source_type') == 'youtube':
                if 'video_duration' in news_item:
                    processed_news['video_duration'] = news_item['video_duration']
                if 'video_author' in news_item:
                    processed_news['video_author'] = news_item['video_author']
                if 'video_views' in news_item:
                    processed_news['video_views'] = news_item['video_views']

            return processed_news

        except Exception as e:
            logger.error(f"❌ 处理新闻失败: {str(e)[:100]}")
            logger.debug(f"   标题: {news_item.get('title', 'N/A')[:50]}...")
            return None

    def batch_process(self, news_list: list, summarize_prompt: str, classify_prompt: str) -> list:
        """批量处理新闻（使用并发加速）"""
        start_time = datetime.now()

        # 获取并发线程数（从环境变量或使用默认值5）
        max_workers = int(os.getenv('AI_CONCURRENT_WORKERS', 5))

        logger.info(f"开始并发处理 {len(news_list)} 条新闻（{max_workers}个线程）...")

        processed = []
        failed = []

        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_news = {
                executor.submit(self.process_news, news, summarize_prompt, classify_prompt): news
                for news in news_list
            }

            # 处理完成的任务
            completed_count = 0
            for future in as_completed(future_to_news):
                news = future_to_news[future]
                completed_count += 1

                try:
                    result = future.result(timeout=120)  # 增加超时到120秒，避免长内容处理失败  # 单条新闻最多60秒
                    if result:
                        processed.append(result)
                        # 每10条报告一次进度
                        if completed_count % 10 == 0:
                            logger.info(f"进度: {completed_count}/{len(news_list)} 条已处理")
                    else:
                        failed.append(news['title'][:50])
                        logger.warning(f"处理失败: {news['title'][:50]}")
                except Exception as e:
                    failed.append(news['title'][:50])
                    logger.error(f"处理异常: {news['title'][:50]} - {str(e)}")

        # 计算统计信息
        elapsed = (datetime.now() - start_time).total_seconds()
        success_rate = len(processed) / len(news_list) * 100 if news_list else 0
        avg_time_per_news = elapsed / len(news_list) if news_list else 0

        logger.info(f"批量处理完成: {len(processed)}/{len(news_list)} ({success_rate:.1f}%)")
        logger.info(f"总耗时: {elapsed:.1f}秒, 平均: {avg_time_per_news:.2f}秒/条")

        # 如果失败率超过10%，记录警告
        if success_rate < 90 and len(news_list) > 0:
            logger.warning(f"⚠️  高失败率检测: {100-success_rate:.1f}% 的新闻处理失败")
            logger.warning(f"失败的新闻示例: {failed[:3]}")

        return processed

    def batch_process_combined(self, news_list: list, combined_prompt: str) -> list:
        """
        批量处理新闻（使用合并提示词，Token优化: 一次调用完成摘要+分类）
        """
        start_time = datetime.now()

        # 获取并发线程数
        max_workers = int(os.getenv('AI_CONCURRENT_WORKERS', 5))

        logger.info(f"🚀 开始批量AI处理: {len(news_list)} 条新闻")
        logger.info(f"   并发线程: {max_workers}个")
        logger.info(f"   AI Provider: {self.ai.provider}")
        logger.info(f"   模型: {self.ai.model}")

        processed = []
        failed = []
        api_errors = 0

        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_news = {
                executor.submit(self.process_news_combined, news, combined_prompt): news
                for news in news_list
            }

            # 处理完成的任务
            completed_count = 0
            for future in as_completed(future_to_news):
                news = future_to_news[future]
                completed_count += 1

                try:
                    result = future.result(timeout=60)
                    if result:
                        processed.append(result)
                        if completed_count % 5 == 0 or completed_count == len(news_list):
                            logger.info(f"   进度: {completed_count}/{len(news_list)} 条已处理 ({completed_count/len(news_list)*100:.0f}%)")
                    else:
                        failed.append(news['title'][:50])
                        api_errors += 1
                        if api_errors <= 3:  # 只显示前3个失败
                            logger.warning(f"   ⚠️ 处理失败 ({api_errors}): {news['title'][:50]}...")
                except Exception as e:
                    failed.append(news['title'][:50])
                    api_errors += 1
                    if api_errors <= 3:
                        logger.error(f"   ❌ 处理异常 ({api_errors}): {news['title'][:50]}... - {str(e)[:50]}")
                        
        # 如果有失败的新闻，尝试简化重试
        if failed and len(failed) > 0:
            logger.info(f"   尝试简化处理 {len(failed)} 条失败新闻...")
            for news_title in failed[:3]:  # 最多重试3条
                # 这里可以添加简化重试逻辑
                pass

        # 计算统计信息
        elapsed = (datetime.now() - start_time).total_seconds()
        success_rate = len(processed) / len(news_list) * 100 if news_list else 0
        avg_time_per_news = elapsed / len(news_list) if news_list else 0

        logger.info(f"✅ 批量处理完成:")
        logger.info(f"   成功: {len(processed)}/{len(news_list)} ({success_rate:.1f}%)")
        logger.info(f"   失败: {len(failed)}")
        logger.info(f"   总耗时: {elapsed:.1f}秒")
        logger.info(f"   平均: {avg_time_per_news:.2f}秒/条")

        if success_rate < 90 and len(news_list) > 0:
            logger.warning(f"⚠️  高失败率警告: {100-success_rate:.1f}% 的新闻处理失败")
            if failed:
                logger.warning(f"   失败示例: {failed[:3]}")

        return processed
