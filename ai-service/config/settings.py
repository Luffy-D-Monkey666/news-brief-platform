import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 120))  # 2分钟

# 新闻分类（优化后顺序）
CATEGORIES = [
    # 核心科技领域
    'ai_technology',         # AI技术
    'robotics',              # 机器人
    'ai_programming',        # AI编码与智能体
    'semiconductors',        # 芯片半导体
    'automotive',            # 汽车
    'consumer_electronics',  # 消费电子
    'podcasts',              # 播客推荐
    'finance_investment',    # 投资财经
    
    # 主流新闻分类
    'business_tech',         # 商业科技
    'politics_world',        # 政治国际
    'economy_policy',        # 经济政策
    'health_medical',        # 健康医疗
    'energy_environment',    # 能源环境
    'entertainment_sports',  # 娱乐体育
    
    # 兴趣领域（放在综合前）
    'anime',                 # 动漫二次元
    'one_piece',             # OP（海贼王）
    'tcg',                   # TCG集换式卡牌（OPCG/PTCG/游戏王等）
    
    'general'                # 综合
]

# 分类中文名称映射
CATEGORY_NAMES = {
    'ai_technology': 'AI技术',
    'robotics': '机器人',
    'ai_programming': 'AI编码与智能体',
    'semiconductors': '芯片',
    'automotive': '汽车',
    'consumer_electronics': '消费电子',
    'podcasts': '播客推荐',
    'finance_investment': '投资财经',
    'business_tech': '商业科技',
    'politics_world': '政治国际',
    'economy_policy': '经济政策',
    'health_medical': '健康医疗',
    'energy_environment': '能源环境',
    'entertainment_sports': '娱乐体育',
    'anime': '动漫二次元',
    'one_piece': 'OP',
    'tcg': 'TCG',
    'general': '综合'
}

# ============================================================
# 新闻源配置（精选优质源，共约70个）
# ============================================================
NEWS_SOURCES = {
    'rss_feeds': [
        # ==================== AI技术（6个核心源）====================
        'https://openai.com/blog/rss/',                    # OpenAI官方博客
        'https://www.anthropic.com/rss.xml',               # Anthropic官方
        'https://blog.google/technology/ai/rss/',          # Google AI Blog
        'https://huggingface.co/blog/feed.xml',            # Hugging Face
        'https://www.deepmind.com/blog/rss.xml',           # DeepMind
        'https://machinelearning.apple.com/rss.xml',       # Apple ML

        # ==================== 机器人（4个核心源）====================
        'https://www.therobotreport.com/feed/',            # The Robot Report
        'https://robohub.org/feed/',                       # Robohub（学术机器人）
        'https://spectrum.ieee.org/feeds/topic/robotics.rss', # IEEE Spectrum机器人
        'https://www.automate.org/rss/news',               # Automate（工业机器人）

        # ==================== AI编程（4个核心源）====================
        'https://github.blog/feed/',                       # GitHub官方博客
        'https://code.visualstudio.com/feed.xml',          # VSCode官方
        'https://blog.stackblitz.com/rss/',                # StackBlitz
        'https://www.cursor.com/blog/rss.xml',             # Cursor官方

        # ==================== 芯片半导体（4个核心源）====================
        'https://www.anandtech.com/rss/',                  # AnandTech
        'https://www.tomshardware.com/feeds/all',          # Tom's Hardware
        'https://semiengineering.com/feed/',               # Semiconductor Engineering
        'https://www.eetimes.com/feed/',                   # EE Times

        # ==================== 汽车（5个核心源）====================
        'https://electrek.co/feed/',                       # Electrek（电动车）
        'https://insideevs.com/rss/news/',                 # InsideEVs
        'https://www.thedrive.com/feed',                   # The Drive
        'https://www.caranddriver.com/rss/all.xml',        # Car and Driver
        'https://cleantechnica.com/feed/',                 # CleanTechnica

        # ==================== 消费电子（5个核心源）====================
        'https://www.theverge.com/rss/index.xml',          # The Verge
        'https://www.engadget.com/rss.xml',                # Engadget
        'https://9to5mac.com/feed/',                       # 9to5Mac
        'https://9to5google.com/feed/',                    # 9to5Google
        'https://www.gsmarena.com/rss-news-reviews.php3',  # GSMArena

        # ==================== 播客推荐（4个核心源）====================
        'https://lexfridman.com/feed/podcast/',            # Lex Fridman Podcast
        'https://feeds.megaphone.fm/hubaborhood',          # a16z Podcast
        'https://feeds.simplecast.com/54nAGcIl',           # The Vergecast
        'https://twimlai.com/feed/',                       # TWIML AI Podcast

        # ==================== 投资财经（5个核心源）====================
        'https://feeds.bloomberg.com/markets/news.rss',    # Bloomberg Markets
        'https://www.ft.com/rss/home',                     # Financial Times
        'https://seekingalpha.com/feed.xml',               # Seeking Alpha
        'https://www.coindesk.com/arc/outboundfeeds/rss/', # CoinDesk（加密）
        'https://www.economist.com/finance-and-economics/rss.xml', # Economist

        # ==================== 商业科技（5个核心源）====================
        'https://techcrunch.com/feed/',                    # TechCrunch
        'https://www.wired.com/feed/rss',                  # Wired
        'https://arstechnica.com/feed/',                   # Ars Technica
        'https://venturebeat.com/feed/',                   # VentureBeat
        'https://www.fastcompany.com/technology/rss',      # Fast Company Tech

        # ==================== 政治国际（4个核心源）====================
        'https://www.theguardian.com/world/rss',           # Guardian World
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', # NYT World
        'https://feeds.bbci.co.uk/news/world/rss.xml',     # BBC World
        'https://www.aljazeera.com/xml/rss/all.xml',       # Al Jazeera

        # ==================== 经济政策（3个核心源）====================
        'https://www.imf.org/en/News/rss',                 # IMF
        'https://www.worldbank.org/en/news/rss.xml',       # World Bank
        'https://www.oecd.org/economy/rss.xml',            # OECD Economy

        # ==================== 健康医疗（3个核心源）====================
        'https://www.statnews.com/feed/',                  # STAT News
        'https://www.fiercebiotech.com/rss/xml',           # Fierce Biotech
        'https://medicalxpress.com/rss-feed/',             # Medical Xpress

        # ==================== 能源环境（3个核心源）====================
        'https://www.greentechmedia.com/feed/',            # Greentech Media
        'https://www.renewableenergyworld.com/feed/',      # Renewable Energy World
        'https://www.carbonbrief.org/feed/',               # Carbon Brief

        # ==================== 娱乐体育（3个核心源）====================
        'https://variety.com/feed/',                       # Variety
        'https://www.hollywoodreporter.com/feed/',         # Hollywood Reporter
        'https://www.espn.com/espn/rss/news',              # ESPN

        # ==================== 动漫二次元（3个核心源）====================
        'https://www.animenewsnetwork.com/all/rss.xml',    # Anime News Network
        'https://www.crunchyroll.com/feed',                # Crunchyroll
        'https://myanimelist.net/rss/news.xml',            # MyAnimeList

        # ==================== OP海贼王（2个核心源）====================
        'https://www.reddit.com/r/OnePiece/.rss',          # Reddit OnePiece
        'https://onepiece.fandom.com/wiki/Special:NewPages?feed=rss', # OP Wiki

        # ==================== TCG集换式卡牌（5个核心源）====================
        'https://www.reddit.com/r/OnePieceTCG/.rss',       # Reddit OPCG
        'https://www.reddit.com/r/PokemonTCG/.rss',        # Reddit PTCG
        'https://www.reddit.com/r/yugioh/.rss',            # Reddit 游戏王
        'https://www.reddit.com/r/magicTCG/.rss',          # Reddit MTG
        'https://www.tcgplayer.com/blog/feed/',            # TCGPlayer Blog

        # ==================== 综合新闻（4个核心源）====================
        'https://feeds.feedburner.com/TechCrunch/',        # TechCrunch综合
        'https://news.ycombinator.com/rss',                # Hacker News
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', # NYT首页
        'https://www.reuters.com/rssFeed/technologyNews',  # Reuters Tech
    ]
}

# ============================================================
# AI提示词模板（优化版：合并摘要+分类，大幅减少token）
# ============================================================

# 合并的摘要+分类提示词（单次调用，结构化三段式输出）
PROCESS_PROMPT = """分析新闻并输出JSON格式结果。

分类列表：
ai_technology(AI技术), robotics(机器人), ai_programming(AI编程工具), 
semiconductors(芯片), automotive(汽车), consumer_electronics(消费电子), 
podcasts(播客), finance_investment(投资财经), business_tech(商业科技), 
politics_world(政治国际), economy_policy(经济政策), health_medical(健康医疗), 
energy_environment(能源环境), entertainment_sports(娱乐体育), 
anime(动漫二次元), one_piece(海贼王), tcg(TCG卡牌游戏), general(综合)

新闻标题: {title}
新闻内容: {content}

输出JSON（严格格式）:
{{
  "title_zh": "中文标题(≤30字)",
  "category": "分类代码",
  "summary": "事件概述: [1-2句话说清楚发生了什么]\n\n重要细节:\n• [关键信息点1：具体数据/人物/时间]\n• [关键信息点2：技术细节/产品规格]\n• [关键信息点3：涉及的公司/机构]\n• [关键信息点4：官方说法或权威引用]\n\n后续影响: [这件事对行业/市场/用户意味着什么，后续可能的发展方向]"
}}"""

# 保留旧变量名以兼容（但不再使用）
SUMMARIZE_PROMPT = PROCESS_PROMPT
CLASSIFY_PROMPT = ""
