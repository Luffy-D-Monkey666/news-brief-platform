import os
from dotenv import load_dotenv

load_dotenv()

# Ollama配置
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'qwen2:7b')

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 300))  # 5分钟

# 新闻分类
CATEGORIES = [
    'finance',      # 财经
    'technology',   # 科技
    'health',       # 健康
    'new_energy',   # 新能源
    'automotive',   # 汽车
    'robotics',     # 机器人
    'ai',          # AI
    'general'      # 综合
]

# 新闻源配置
NEWS_SOURCES = {
    'rss_feeds': [
        # 科技类
        'https://www.wired.com/feed/rss',
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',

        # 财经类
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.cnbc.com/id/100003114/device/rss/rss.html',

        # AI类
        'https://www.artificialintelligence-news.com/feed/',

        # 汽车类
        'https://www.motortrend.com/feed/',

        # 中文源
        'https://rsshub.app/36kr/newsflashes',
        'https://rsshub.app/sina/finance',
    ],
    'api_endpoints': [
        # 可以添加NewsAPI等
    ]
}

# AI提示词模板
SUMMARIZE_PROMPT = """请分析以下新闻内容，用中文提炼成一条简洁的新闻简报。
要求：
1. 将标题翻译成中文（保留专有名词的英文）
2. 用中文总结核心内容（50-100字）
3. 使用简洁专业的语言
4. 突出新闻价值和影响

新闻标题：{title}
新闻内容：{content}

请按以下格式返回（只返回内容，不要任何标签）：
中文标题
中文简报
"""

CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别中。
可选类别：财经(finance)、科技(technology)、健康(health)、新能源(new_energy)、汽车(automotive)、机器人(robotics)、AI(ai)、综合(general)

新闻标题：{title}
新闻简报：{summary}

只返回类别英文名称，不要其他内容。
类别："""
