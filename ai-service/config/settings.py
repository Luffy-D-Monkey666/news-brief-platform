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
SUMMARIZE_PROMPT = """请分析以下新闻内容，用中文提炼成一条详细的新闻总结。
要求：
1. 将标题翻译成中文（保留专有名词的英文）
2. 用中文详细总结核心内容（150-200字）
3. 包含：事件背景、关键信息、影响分析、相关数据
4. 使用简洁专业的语言
5. 确保读者无需查看原文就能了解新闻全貌

新闻标题：{title}
新闻内容：{content}

请按以下格式返回（只返回内容，不要任何标签）：
中文标题
详细总结（150-200字，包含背景、关键信息、影响）
"""

CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别中。

【个人兴趣类别】（最高优先级，严格匹配）
- op_card_game: One Piece卡牌游戏TCG相关，包括：
  * 卡片发布（任何语言版本：英语EN、日语JP、中文CN、法语FR等）
  * 新套装、新弹、限定卡、OP卡、SR卡、秘闪
  * 赛事信息、锦标赛、比赛规则
  * 卡组构筑、玩法攻略
  * One Piece Card Game、ワンピースカードゲーム

- op_merchandise: One Piece IP周边情报，包括：
  * 海贼王漫画更新、章节、剧情
  * 周边商品、手办、模型、Figure
  * 一番赏、盲盒
  * 主题店开业、Pop-up Store
  * 联名产品、服饰、鞋子
  * 动画、真人剧、电影
  * One Piece、海贼王、ワンピース相关的任何商品和活动

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
- entertainment_sports: 娱乐、体育、文化、艺术、影视、游戏（不包括One Piece）
- general: 其他不属于以上类别的新闻

新闻标题：{title}
新闻简报：{summary}

只返回类别英文名称（如 op_card_game），不要其他内容。
类别："""
