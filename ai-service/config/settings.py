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
# DeepSeek优化Prompt（高级AI模型，支持详细中文摘要）
SUMMARIZE_PROMPT = """请分析以下新闻内容，用中文提炼成一条详细的新闻总结。

要求：
1. 将标题翻译成中文（保留专有名词的英文，如"OpenAI"、"Tesla"、人名地名等）
2. 用中文详细总结核心内容（150-200字）
3. 总结必须包含以下结构化信息：
   - 【事件背景】简要说明事件的背景和起因
   - 【关键信息】列出核心要点（可使用多行列表）
   - 【影响分析】分析事件的影响和意义
   - 【相关数据】如有重要数据或数字，单独列出

新闻标题: {title}
新闻内容: {content}

输出格式（严格按照以下格式，不要添加任何前缀词如"中文标题"、"第一行"等）：

第1行：简洁的中文标题（不超过30字）

第2行开始：详细总结，必须包含以下结构：

【事件背景】
（背景描述文字）

【关键信息】
• 要点1
• 要点2
• 要点3

【影响分析】
（影响分析文字）

【相关数据】（如有）
• 数据1
• 数据2
"""

CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别。

分类规则：
- op_card_game: One Piece卡牌游戏（TCG、集换式卡牌）
- op_merchandise: One Piece周边（手办、服装、IP商品）
- ai_robotics: AI与机器人（人工智能、机器学习、自动化）
- ev_automotive: 新能源汽车（电动车、Tesla、BYD、充电桩）
- finance_investment: 投资财经（股票、加密货币、投资、金融市场）
- business_tech: 商业科技（科技公司、创业、商业新闻）
- politics_world: 政治国际（国际关系、政府、选举）
- economy_policy: 经济政策（GDP、通胀、经济政策、贸易）
- health_medical: 健康医疗（医疗、健康、疾病、药品）
- energy_environment: 能源环境（能源、气候、环保）
- entertainment_sports: 娱乐体育（体育赛事、电影、音乐）
- general: 综合（其他不属于以上分类的新闻）

新闻标题: {title}
新闻摘要: {summary}

请只返回英文分类名称（如: ai_robotics），不要有其他内容。
分类:"""
