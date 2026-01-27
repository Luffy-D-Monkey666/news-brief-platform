import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 180))  # 3分钟（阶段2：配合20条抓取）

# 新闻分类（基于国际新闻标准，突出用户关注领域）
CATEGORIES = [
    # 个人兴趣（最高优先级）
    'tcg_card_game',        # TCG卡牌游戏（宝可梦PTCG、海贼王OPCG、龙珠DBTCG等）
    'one_piece',            # 海贼王相关（One Piece所有内容）
    'anime_manga',          # 日本动画漫画

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
    'tcg_card_game': 'TCG信息',
    'one_piece': '海贼王',
    'anime_manga': '动画漫画',

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

# 新闻源配置（覆盖全球，100+新闻源）
NEWS_SOURCES = {
    'rss_feeds': [
        # ==================== 中国（中文源）====================
        'https://rsshub.app/36kr/newsflashes',  # 36Kr快讯（分钟级更新）
        'https://rsshub.app/sina/finance',  # 新浪财经
        'https://rsshub.app/thepaper/featured',  # 澎湃新闻
        'https://rsshub.app/zaobao/znews/china',  # 联合早报（新加坡中文）
        'https://rsshub.app/ifanr/rss',  # 爱范儿科技
        'https://rsshub.app/sspai/posts',  # 少数派

        # ==================== 美国主流媒体 ====================
        # 顶级综合
        'https://feeds.bbci.co.uk/news/rss.xml',  # BBC Top Stories（英国）
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC World（英国）
        'https://www.theguardian.com/world/rss',  # Guardian World（英国）
        'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/world/europe/rss.xml',  # NY Times 欧洲版
        'https://www.washingtonpost.com/world/rss.xml',  # 华盛顿邮报
        'https://rss.cnn.com/rss/edition.rss',  # CNN Edition
        'https://rss.cnn.com/rss/edition_world.rss',  # CNN World
        'https://www.aljazeera.com/xml/rss/all.xml',  # 半岛电视台全覆盖（中东视角）

        # 国际新闻
        'https://www.reuters.com/rssFeed/worldNews',  # 路透社世界新闻
        'https://www.reuters.com/rssFeed/technologyNews',  # 路透社科技
        'https://www.reuters.com/rssFeed/businessNews',  # 路透社商业

        # ==================== 科技类 ====================
        'https://www.wired.com/feed/rss',  # Wired（美国）
        'https://techcrunch.com/feed/',  # TechCrunch（美国）
        'https://www.theverge.com/rss/index.xml',  # The Verge（美国）
        'https://www.technologyreview.com/feed/',  # MIT Technology Review（美国）
        'https://venturebeat.com/feed/',  # VentureBeat（美国）
        'https://arstechnica.com/feed/',  # Ars Technica（美国）
        'https://www.engadget.com/feed.xml',  # Engadget（美国）
        'https://www.artificialintelligence-news.com/feed/',  # AI News（英国）
        'https://venturebeat.com/category/ai/feed/',  # VentureBeat AI

        # ==================== 财经类 ====================
        'https://feeds.bloomberg.com/markets/news.rss',  # Bloomberg Markets（美国）
        'https://feeds.bloomberg.com/technology/news.rss',  # Bloomberg Tech（美国）
        'https://www.cnbc.com/id/100003114/device/rss/rss.html',  # CNBC（美国）
        'https://www.ft.com/rss/home',  # Financial Times（英国）
        'https://www.wsj.com/rss/world',  # Wall Street Journal（美国）
        'https://seekingalpha.com/market_currents.xml',  # Seeking Alpha（美国）

        # ==================== 新能源汽车 ====================
        'https://www.motortrend.com/feed/',  # Motor Trend（美国）
        'https://insideevs.com/rss/',  # InsideEVs电动车（美国）
        'https://electrek.co/feed/',  # Electrek电动车（美国）
        'https://cleantechnica.com/feed/',  # CleanTechnica（美国）

        # ==================== 日本 ====================
        'https://www3.nhk.or.jp/rss/news/cat0.xml',  # NHK日本主要新闻

        # ==================== 欧洲媒体 ====================
        'https://www.lemonde.fr/rss/une.xml',  # 法国世界报
        'https://www.spiegel.de/schlagzeilen/index.rss',  # 德国明镜周刊
        'https://elpais.com/rss/elpais/portada.xml',  # 西班牙国家报

        # ==================== 北美洲（美国/加拿大）====================
        'https://www.abc.net.au/news/feed/51120/rss.xml',  # ABC News（澳大利亚-大洋洲）
        'https://www.cbc.ca/web/rss/rss-canada',  # CBC Canada（加拿大）

        # ==================== 健康医疗 ====================
        'https://www.who.int/rss-feeds/news-english.xml',  # 世界卫生组织
        'https://www.nature.com/nm.rss',  # Nature Medicine

        # ==================== 娱乐体育 ====================
        'https://www.espn.com/espn/rss/news',  # ESPN体育（美国）
        'https://variety.com/feed/',  # Variety娱乐（美国）
        'https://deadline.com/feed/',  # Deadline娱乐（美国）

        # ==================== 能源与环境 ====================
        'https://www.energycentral.com/feeds/content.xml',  # Energy Central

        # ==================== TCG卡牌游戏 ====================
        # 宝可梦TCG
        'https://www.pokemon.com/us/pokemon-news/rss',  # Pokemon Official News
        'https://www.pokebeach.com/feed',  # PokeBeach TCG News
        'https://www.pokeguardian.com/feed',  # PokeGuardian

        # 海贼王卡牌OPCG
        'https://rsshub.app/bandai/onepiece-cardgame',  # Bandai OPCG Official
        'https://onepiece-cardgame.com/news/rss',  # One Piece Card Game Official

        # 龙珠卡牌DBTCG
        'https://www.dbs-cardgame.com/us-en/news/rss',  # Dragon Ball Super Card Game

        # 游戏王
        'https://www.yugioh-card.com/en/news/rss.xml',  # Yu-Gi-Oh Official
        'https://ygoprodeck.com/feed/',  # YGOProDeck

        # 万智牌MTG
        'https://magic.wizards.com/en/rss/articles.xml',  # Magic: The Gathering Official
        'https://www.channelfireball.com/feed/',  # ChannelFireball MTG

        # TCG综合资讯
        'https://www.tcgplayer.com/feed',  # TCGPlayer
        'https://infinite.tcgplayer.com/feed',  # TCGPlayer Infinite

        # ==================== 海贼王（One Piece）====================
        # 官方与主流媒体
        'https://rsshub.app/onepiece/news',  # One Piece Official News
        'https://rsshub.app/shonenjump/series/one-piece',  # Shonen Jump One Piece
        'https://rsshub.app/animenewsnetwork/news/one-piece',  # ANN One Piece
        'https://www.crunchyroll.com/rss/anime?lang=enUS&tagged=one-piece',  # Crunchyroll OP
        'https://onepiecepodcast.com/feed/',  # One Piece Podcast
        'https://rsshub.app/bangumi/subject/1000',  # Bangumi One Piece

        # 商品与周边
        'https://rsshub.app/toei-anim/onepiece',  # Toei Animation One Piece

        # 漫画更新
        'https://rsshub.app/manga/onepiece',  # One Piece Manga Updates
        'https://ww8.readonepiece.com/feed/',  # Read One Piece (fan site)

        # ==================== 动画漫画（Anime & Manga）====================
        # 主流动漫新闻
        'https://www.animenewsnetwork.com/rss.xml',  # Anime News Network
        'https://www.crunchyroll.com/rss/news',  # Crunchyroll News
        'https://www.funimation.com/blog/feed/',  # Funimation Blog
        'https://myanimelist.net/rss/news.xml',  # MyAnimeList News
        'https://www.animenewsnetwork.com/all/rss.xml',  # ANN All Updates

        # 日本动画制作公司
        'https://rsshub.app/toei-anim',  # Toei Animation（东映）
        'https://rsshub.app/mappa',  # MAPPA Studio
        'https://rsshub.app/bones',  # Bones Studio
        'https://rsshub.app/kyotoanimation',  # Kyoto Animation

        # 漫画出版社
        'https://rsshub.app/shonenjump',  # Shonen Jump Weekly
        'https://rsshub.app/shueisha',  # 集英社（Shueisha）
        'https://rsshub.app/kodansha',  # 讲谈社（Kodansha）

        # 轻小说
        'https://rsshub.app/dengekionline',  # 电击文库（Dengeki）

        # 声优与ACG文化
        'https://rsshub.app/seiyuu',  # 声优情报
        'https://rsshub.app/bangumi/calendar',  # Bangumi放送日历
        'https://www.animatetimes.com/feed',  # Animate Times

        # 欧美动漫社区
        'https://kotaku.com/rss',  # Kotaku Anime
        'https://comicbook.com/anime/rss.xml',  # ComicBook Anime
    ]
}

# AI提示词模板
# DeepSeek优化Prompt（高级AI模型，支持结构化灵活中文摘要）
SUMMARIZE_PROMPT = """请分析以下新闻内容，用中文提炼成一条新闻总结。

核心要求：
1. 将标题翻译成中文（保留专有名词如"OpenAI"、"Tesla"、人名地名等）
2. 根据"事件概述"、"重要细节"、"后续影响"三段式结构总结
3. 每段之间用空行分隔，保持清晰结构
4. 根据新闻复杂度调整长度：
   - 简单新闻：每段30-50字
   - 一般新闻：每段50-80字
   - 复杂/重要新闻：每段80-120字

新闻标题: {title}
新闻内容: {content}

输出格式（严格按照以下格式，不加任何前缀）：

第1行：简洁的中文标题（不超过30字）

第2行开始（空一行）：

事件概述：
（简要说明新闻的核心内容，用1-2句话概括）

（空一行）

重要细节：
• 关键细节1
• 关键细节2
• 关键细节3
（列出3-5个重要要点，用•标记）

（空一行）

后续影响：
（分析事件的意义、影响和可能的发展，用1-2段文字）

注意：
- 段落之间必须有空行分隔
- 重要细节部分必须用•列表
- 整体简洁清晰，不要啰嗦
- 像专业新闻摘要一样结构化
"""

CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别。

分类规则：
- tcg_card_game: TCG卡牌游戏（宝可梦PTCG、海贼王OPCG、龙珠DBTCG、游戏王、万智牌等所有TCG）
- one_piece: 海贼王相关（海贼王动画、漫画、真人剧、手办、周边、卡牌、所有One Piece内容）
- anime_manga: 日本动画漫画（动画、漫画、轻小说、声优、日本ACG文化，不包括海贼王）
- ai_robotics: AI与机器人（人工智能、机器学习、自动化）
- ev_automotive: 新能源汽车（电动车、Tesla、BYD、充电桩）
- finance_investment: 投资财经（股票、加密货币、投资、金融市场）
- business_tech: 商业科技（科技公司、创业、商业新闻）
- politics_world: 政治国际（国际关系、政府、选举）
- economy_policy: 经济政策（GDP、通胀、经济政策、贸易）
- health_medical: 健康医疗（医疗、健康、疾病、药品）
- energy_environment: 能源环境（能源、气候、环保）
- entertainment_sports: 娱乐体育（体育赛事、电影、音乐，不包括动漫）
- general: 综合（其他不属于以上分类的新闻）

新闻标题: {title}
新闻摘要: {summary}

请只返回英文分类名称（如: tcg_card_game），不要有其他内容。
分类:"""
