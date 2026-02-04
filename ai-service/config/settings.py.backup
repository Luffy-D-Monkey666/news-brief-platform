import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 120))  # 2分钟（优化后：配合47个高质量源）

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
        # 宝可梦TCG（Pokemon Trading Card Game）
        'https://www.pokemon.com/us/pokemon-news/',  # Pokemon官方新闻（无RSS但可爬）
        'https://pokemonblog.com/feed/',  # Pokemon非官方博客
        'https://www.thegamer.com/tag/pokemon-tcg/feed/',  # TheGamer Pokemon TCG
        'https://www.dicebreaker.com/games/pokemon-trading-card-game/news/feed',  # Dicebreaker Pokemon
        
        # 海贼王卡牌OPCG（One Piece Card Game）
        'https://en.onepiece-cardgame.com/news/',  # OPCG英文官网
        'https://onepiece-cardgame.dev/news.xml',  # OPCG社区
        'https://www.dicebreaker.com/games/one-piece-card-game/news/feed',  # Dicebreaker OPCG
        
        # 龙珠卡牌DBTCG（Dragon Ball Super Card Game）
        'https://www.dbs-cardgame.com/us-en/news/',  # 龙珠卡牌官网
        'https://www.dicebreaker.com/categories/dragon-ball/news/feed',  # Dicebreaker龙珠
        
        # 游戏王（Yu-Gi-Oh）
        'https://www.yugioh-card.com/en/news/',  # 游戏王官网
        'https://ygoprodeck.com/blog/feed/',  # YGOProDeck博客
        'https://www.dicebreaker.com/games/yu-gi-oh-trading-card-game/news/feed',  # Dicebreaker游戏王
        
        # 万智牌MTG（Magic: The Gathering）
        'https://magic.wizards.com/en/news',  # 万智牌官网新闻
        'https://www.channelfireball.com/articles/feed/',  # ChannelFireball文章
        'https://www.mtggoldfish.com/articles/feed',  # MTGGoldfish
        
        # TCG综合资讯
        'https://www.dicebreaker.com/categories/trading-card-game/news/feed',  # Dicebreaker TCG综合
        'https://www.thegamer.com/category/tabletop/trading-card-games/feed/',  # TheGamer TCG
        'https://cardgamebase.com/feed/',  # Card Game Base

        # ==================== 海贼王（One Piece）====================
        # 官方与主流媒体（保留可用源）
        'https://www.crunchyroll.com/rss/anime?lang=enUS&tagged=one-piece',  # ✅ Crunchyroll OP
        'https://www.viz.com/shonenjump/chapters/one-piece',  # Viz Shonen Jump
        'https://onepiece.fandom.com/wiki/Special:NewPages?feed=rss',  # OP Wiki更新
        
        # 英文社区
        'https://thelibraryofohara.com/feed/',  # The Library of Ohara
        'https://onepiecepodcast.com/feed',  # One Piece Podcast（修正URL）
        'https://www.opfanpage.com/feed/',  # OP Fan Page
        
        # 新闻聚合
        'https://comicbook.com/anime/news/one-piece/feed/',  # ComicBook OP
        'https://www.animenewsnetwork.com/news/one-piece/rss.xml',  # ANN OP专区
        'https://www.cbr.com/tag/one-piece/feed/',  # CBR One Piece
        
        # 日本官方（可能需要代理但值得保留）
        'https://one-piece.com/news.xml',  # OP日本官网

        # ==================== 动画漫画（Anime & Manga）====================
        # 主流动漫新闻（保留可用源并修正）
        'https://www.animenewsnetwork.com/newsroom/rss.xml',  # ✅ ANN修正URL
        'https://www.crunchyroll.com/rss/news',  # ✅ Crunchyroll News
        'https://myanimelist.net/rss/news.xml',  # ✅ MyAnimeList News
        'https://www.animenewsnetwork.com/encyclopedia/rss.xml',  # ANN百科更新
        
        # 英文动漫媒体
        'https://www.crunchyroll.com/news-feed',  # Crunchyroll新闻页
        'https://www.cbr.com/category/anime-news/feed/',  # CBR动漫新闻
        'https://www.sportskeeda.com/anime/feed',  # Sportskeeda动漫
        'https://animecorner.me/feed/',  # Anime Corner
        'https://www.animenewsnetwork.com/interest/rss.xml',  # ANN Interest
        
        # 漫画新闻
        'https://www.mangaupdates.com/rss.php',  # MangaUpdates
        'https://www.cbr.com/category/manga-news/feed/',  # CBR漫画新闻
        'https://www.viz.com/blog/feed',  # Viz漫画博客
        
        # 日本动画工作室（替代方案）
        'https://www.toei-anim.co.jp/en/news/feed/',  # Toei官方英文
        'https://mappa.co.jp/news/feed/',  # MAPPA官网
        
        # 综合ACG资讯
        'https://www.animenewsnetwork.com/oped/rss.xml',  # ANN评论
        'https://comicbook.com/anime/news/feed/',  # ComicBook动漫
        'https://www.dualshockers.com/anime/feed/',  # DualShockers动漫
        'https://gamerant.com/anime/feed/',  # Game Rant动漫
        
        # Reddit动漫社区（高质量）
        'https://www.reddit.com/r/anime/.rss',  # Reddit r/anime
        'https://www.reddit.com/r/manga/.rss',  # Reddit r/manga
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

CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别。必须严格按照优先级和关键词进行分类。

🎯 核心分类（最高优先级，必须优先匹配）：

1. tcg_card_game - TCG卡牌游戏
   关键词：Pokemon TCG, PTCG, 宝可梦卡牌, One Piece Card Game, OPCG, 海贼王卡牌, 
           Dragon Ball TCG, DBTCG, 龙珠卡牌, Yu-Gi-Oh, 游戏王, Magic The Gathering, MTG, 万智牌,
           卡包, booster pack, 稀有卡, rare card, meta deck, tournament, 锦标赛,
           trading card game, TCG, 集换式卡牌
   判断：只要提到任何TCG卡牌游戏的比赛、发售、新卡、赛事，必须分为此类

2. one_piece - 海贼王（One Piece）
   关键词：One Piece, 海贼王, Luffy, 路飞, Straw Hat, 草帽, Eiichiro Oda, 尾田荣一郎,
           Jump, 周刊少年, Wano, 和之国, Netflix live action, 真人剧, 
           海贼王剧场版, One Piece film, OP手办, OP周边
   判断：任何与海贼王相关的内容（动画/漫画/真人剧/商品），但如果专门讲海贼王卡牌则归tcg_card_game

3. anime_manga - 日本动画漫画  
   关键词：anime, manga, 动画, 漫画, 新番, 声优, seiyuu, light novel, 轻小说,
           Studio Ghibli, 吉卜力, Crunchyroll, 京都动画, KyoAni, MAPPA, Toei Animation,
           Shonen Jump, 少年Jump, 漫画连载, anime adaptation, 动画化
   判断：日本动漫相关，但海贼王专门归one_piece类

📌 其他分类：
- ai_robotics: AI与机器人（ChatGPT, OpenAI, 机器学习, 人工智能, 自动驾驶AI）
- ev_automotive: 新能源汽车（Tesla, 特斯拉, BYD, 比亚迪, 电动车, EV, 充电桩）
- finance_investment: 投资财经（股票, 加密货币, Bitcoin, 投资, 金融市场）
- business_tech: 商业科技（科技公司, startup, 融资, IPO, 商业新闻）
- politics_world: 政治国际（国际关系, 政府, 选举, 外交）
- economy_policy: 经济政策（GDP, 通胀, 经济政策, 贸易战）
- health_medical: 健康医疗（医疗, 健康, 疾病, 药品, 疫苗）
- energy_environment: 能源环境（能源, 气候变化, 环保, 可再生能源）
- entertainment_sports: 娱乐体育（体育赛事, 电影, 音乐, 明星，不包括动漫）
- general: 综合（无法明确分类的其他新闻）

⚠️ 分类规则：
1. 优先匹配核心分类（tcg_card_game, one_piece, anime_manga）
2. 如果新闻同时涉及多个类别，选择最主要的
3. 海贼王卡牌游戏 → tcg_card_game（因为重点是卡牌）
4. 海贼王动画/漫画 → one_piece
5. 其他动漫 → anime_manga

新闻标题: {title}
新闻摘要: {summary}

请只返回英文分类名称（如: tcg_card_game），不要有其他内容。
分类:"""
