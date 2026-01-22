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

# 新闻分类（基于国际新闻标准，突出用户关注领域）
CATEGORIES = [
    # 核心关注领域
    'ai_robotics',          # AI与机器人
    'ev_automotive',        # 新能源汽车
    'finance_investment',   # 投资财经

    # 主流新闻分类
    'business_tech',        # 商业科技
    'politics_world',       # 政治国际
    'economy_policy',       # 经济政策
    'health_medical',       # 健康医疗
    'energy_environment',   # 能源环境
    'entertainment_sports', # 娱乐体育
    'general'              # 综合
]

# 分类中文名称映射
CATEGORY_NAMES = {
    'ai_robotics': 'AI与机器人',
    'ev_automotive': '新能源汽车',
    'finance_investment': '投资财经',
    'business_tech': '商业科技',
    'politics_world': '政治国际',
    'economy_policy': '经济政策',
    'health_medical': '健康医疗',
    'energy_environment': '能源环境',
    'entertainment_sports': '娱乐体育',
    'general': '综合'
}

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

【核心关注类别】（优先匹配）
- ai_robotics: 人工智能、机器人、自动化、AGI、大模型、机器学习相关
- ev_automotive: 新能源汽车、电动车、特斯拉、比亚迪、汽车产业、自动驾驶
- finance_investment: 股市、投资、基金、加密货币、并购、IPO、金融市场波动

【主流新闻类别】
- business_tech: 企业经营、科技公司、创业、产品发布、商业模式
- politics_world: 政治、国际关系、地缘政治、外交、选举、政策
- economy_policy: 宏观经济、经济政策、GDP、通胀、央行、贸易
- health_medical: 医疗健康、疾病、药物、医疗技术、公共卫生
- energy_environment: 能源（石油、天然气、核能）、气候变化、环保、碳排放
- entertainment_sports: 娱乐、体育、文化、艺术、影视、游戏
- general: 其他不属于以上类别的新闻

新闻标题：{title}
新闻简报：{summary}

只返回类别英文名称（如 ai_robotics），不要其他内容。
类别："""
