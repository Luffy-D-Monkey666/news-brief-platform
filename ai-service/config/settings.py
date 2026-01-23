import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 180))  # 3分钟（更频繁更新）

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

        # === 国际主流媒体（更新频繁）===
        'https://feeds.bbci.co.uk/news/rss.xml',  # BBC Top Stories
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC World
        'https://www.theguardian.com/world/rss',  # Guardian World
        'https://rss.cnn.com/rss/edition.rss',  # CNN Top
        'https://rss.cnn.com/rss/edition_world.rss',  # CNN World
        'https://www.aljazeera.com/xml/rss/all.xml',  # 半岛电视台全覆盖
        'https://www.reuters.com/rssFeed/worldNews',  # 路透社世界新闻
        'https://www.reuters.com/rssFeed/technologyNews',  # 路透社科技
        'https://www.washingtonpost.com/world/rss.xml',  # 华盛顿邮报
        'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/world/europe/rss.xml',  # 纽约时报欧洲

        # === 科技类（实时更新）===
        'https://www.wired.com/feed/rss',
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.technologyreview.com/feed/',  # MIT科技评论
        'https://venturebeat.com/feed/',  # VentureBeat
        'https://arstechnica.com/feed/',  # Ars Technica
        'https://www.engadget.com/feed.xml',  # Engadget

        # === 财经类（实时更新）===
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.bloomberg.com/technology/news.rss',
        'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        'https://www.ft.com/rss/home',  # 金融时报
        'https://www.wsj.com/rss/world',  # 华尔街日报
        'https://seekingalpha.com/market_currents.xml',  # Seeking Alpha

        # === AI与机器人 ===
        'https://www.artificialintelligence-news.com/feed/',
        'https://venturebeat.com/category/ai/feed/',  # VentureBeat AI

        # === 新能源汽车 ===
        'https://www.motortrend.com/feed/',
        'https://insideevs.com/rss/',  # InsideEVs电动车
        'https://electrek.co/feed/',  # Electrek电动车
        'https://cleantechnica.com/feed/',  # CleanTechnica清洁技术

        # === 中文源（实时更新）===
        'https://rsshub.app/36kr/newsflashes',  # 36Kr快讯（分钟级更新）
        'https://rsshub.app/sina/finance',  # 新浪财经
        'https://rsshub.app/thepaper/featured',  # 澎湃新闻
        'https://rsshub.app/wallstreetcn/news/global',  # 华尔街见闻
        'https://rsshub.app/caixin/latest',  # 财新网
        'https://rsshub.app/ifanr/rss',  # 爱范儿
        'https://rsshub.app/sspai/posts',  # 少数派

        # === 亚洲媒体 ===
        'https://www3.nhk.or.jp/rss/news/cat0.xml',  # NHK日本主要新闻
        'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',  # 印度时报头版
        'https://rsshub.app/zaobao/znews/china',  # 联合早报-新加坡

        # === 欧洲媒体 ===
        'https://www.lemonde.fr/rss/une.xml',  # 法国世界报
        'https://www.spiegel.de/schlagzeilen/index.rss',  # 德国明镜周刊
        'https://elpais.com/rss/elpais/portada.xml',  # 西班牙国家报

        # === 澳大利亚 ===
        'https://www.abc.net.au/news/feed/51120/rss.xml',  # ABC News

        # === 健康医疗 ===
        'https://www.who.int/rss-feeds/news-english.xml',  # 世界卫生组织
        'https://www.nature.com/nm.rss',  # Nature Medicine

        # === 娱乐体育 ===
        'https://www.espn.com/espn/rss/news',  # ESPN体育
        'https://variety.com/feed/',  # Variety娱乐
        'https://deadline.com/feed/',  # Deadline娱乐

        # === 加拿大 ===
        'https://www.cbc.ca/web/rss/rss-canada',  # CBC Canada
    ],
    'api_endpoints': []
}

# AI提示词模板
# DeepSeek优化Prompt（高级AI模型，支持灵活中文摘要）
SUMMARIZE_PROMPT = """请分析以下新闻内容，用中文提炼成一条新闻总结。

核心要求：
1. 将标题翻译成中文（保留专有名词如"OpenAI"、"Tesla"、人名地名等）
2. 根据新闻的复杂度和重要性，灵活调整摘要长度：
   - 简单新闻：80-120字
   - 一般新闻：120-180字
   - 复杂/重要新闻：180-250字
3. 根据新闻类型选择合适的叙述方式：
   - 政治/经济：强调背景、数据、影响
   - 科技/商业：突出创新点、市场意义
   - 娱乐/体育：简洁生动，突出亮点
   - 突发事件：时间线、关键信息、最新进展
4. 自然流畅的叙述，不要机械地分成固定模块
5. 重要信息可以用"•"列表呈现，但要适度使用

新闻标题: {title}
新闻内容: {content}

输出格式：
第1行：简洁的中文标题（不超过30字，不加任何前缀）

第2行开始：
用自然、流畅的语言总结新闻，适当使用段落分隔。
如需强调要点，可用：
• 要点1
• 要点2

避免：
❌ 使用【事件背景】【关键信息】等生硬标签
❌ 机械地分成四个固定模块
✅ 像专业记者一样，用自然语言讲述新闻
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
