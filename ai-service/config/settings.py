import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 300))  # 5分钟

# 新闻分类（基于国际新闻标准，突出用户关注领域）
CATEGORIES = [
    # 个人兴趣（最高优先级）
    'op_card_game',         # One Piece卡牌游戏
    'op_merchandise',       # One Piece周边IP

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
    # 个人兴趣
    'op_card_game': 'OP卡牌游戏',
    'op_merchandise': 'OP周边情报',

    # 核心关注领域
    'ai_robotics': 'AI与机器人',
    'ev_automotive': '新能源汽车',
    'finance_investment': '投资财经',

    # 主流新闻分类
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
        # === One Piece 专区（顶级优先）===
        'https://rsshub.app/reddit/r/OnePieceTCG',  # One Piece TCG Reddit
        'https://rsshub.app/reddit/r/OnePiece',     # One Piece Reddit
        'https://rsshub.app/twitter/user/OP_CARD_GLOBAL',  # OP TCG官方推特

        # === 国际主流媒体 ===
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC英国
        'https://www.theguardian.com/world/rss',  # Guardian英国
        'https://rss.cnn.com/rss/edition_world.rss',  # CNN美国
        'https://www.aljazeera.com/xml/rss/all.xml',  # 半岛电视台-中东
        'https://www.reuters.com/rssFeed/worldNews',  # 路透社

        # === 科技类 ===
        'https://www.wired.com/feed/rss',
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.technologyreview.com/feed/',  # MIT科技评论
        'https://venturebeat.com/category/ai/feed/',  # VentureBeat AI

        # === 财经类 ===
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        'https://www.ft.com/rss/home',  # 金融时报

        # === AI与机器人 ===
        'https://www.artificialintelligence-news.com/feed/',

        # === 新能源汽车 ===
        'https://www.motortrend.com/feed/',
        'https://insideevs.com/rss/',  # InsideEVs电动车
        'https://electrek.co/feed/',  # Electrek电动车
        'https://cleantechnica.com/feed/',  # CleanTechnica清洁技术

        # === 中文源（增强）===
        'https://rsshub.app/36kr/newsflashes',
        'https://rsshub.app/sina/finance',
        'https://rsshub.app/thepaper/featured',  # 澎湃新闻
        'https://rsshub.app/wallstreetcn/news/global',  # 华尔街见闻
        'https://rsshub.app/caixin/latest',  # 财新网

        # === 亚洲 ===
        'https://www3.nhk.or.jp/rss/news/cat0.xml',  # NHK日本
        'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',  # 印度时报
        'https://rsshub.app/zaobao/znews/china',  # 联合早报-新加坡

        # === 欧洲 ===
        'https://www.lemonde.fr/rss/une.xml',  # 法国世界报
        'https://www.spiegel.de/schlagzeilen/index.rss',  # 德国明镜周刊

        # === 健康医疗 ===
        'https://www.who.int/rss-feeds/news-english.xml',  # 世界卫生组织

        # === 娱乐体育 ===
        'https://www.espn.com/espn/rss/news',  # ESPN体育
        'https://variety.com/feed/',  # Variety娱乐
    ],
    'api_endpoints': []
}

# AI提示词模板
# 为免费AI优化的简化Prompt（适配Hugging Face等免费模型）
SUMMARIZE_PROMPT = """Translate this news to Chinese and summarize it in 100-150 words.

Title: {title}
Content: {content}

Output format (Chinese only):
[Chinese Title]
[Chinese Summary 100-150 words]
"""

CLASSIFY_PROMPT = """Classify this news into one category:

Categories:
- op_card_game: One Piece TCG cards
- op_merchandise: One Piece merchandise
- ai_robotics: AI, robots, machine learning
- ev_automotive: Electric vehicles, Tesla, BYD
- finance_investment: Stock, investment, crypto
- business_tech: Business, tech companies
- politics_world: Politics, international
- economy_policy: Economy, GDP, policy
- health_medical: Health, medicine
- energy_environment: Energy, environment
- entertainment_sports: Entertainment, sports
- general: Other news

Title: {title}
Summary: {summary}

Return only the category name in English (like: ai_robotics)
Category:"""
