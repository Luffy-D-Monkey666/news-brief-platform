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
PROCESS_PROMPT = """你是新闻编辑，分析以下新闻并输出JSON。

分类：ai_technology, robotics, ai_programming, semiconductors, automotive, consumer_electronics, podcasts, finance_investment, business_tech, politics_world, economy_policy, health_medical, energy_environment, entertainment_sports, anime, one_piece, tcg, general

新闻标题: {title}
新闻内容: {content}

要求：
1. title_zh: 中文标题，≤30字
2. category: 从上面分类中选一个
3. summary: 必须包含三部分，用换行符分隔：
   - 第一行写"事件概述:"后面跟1-2句话概括发生了什么
   - 空一行后写"重要细节:"然后用•列出3-4个关键信息点
   - 空一行后写"后续影响:"分析这件事的意义和后续发展

输出示例：
{{
  "title_zh": "OpenAI发布GPT-5，性能提升3倍",
  "category": "ai_technology",
  "summary": "事件概述: OpenAI正式发布GPT-5模型，在推理能力和多模态理解方面实现重大突破。\n\n重要细节:\n• 发布时间：2026年2月18日\n• 性能提升：推理速度提升3倍，准确率提高40%\n• 定价：API价格维持不变\n• CEO Sam Altman称这是\"迈向AGI的关键一步\"\n\n后续影响: GPT-5的发布将加速AI应用落地，预计将对搜索、编程、教育等行业产生深远影响。竞争对手可能加快发布节奏。"
}}

请严格按此格式输出JSON："""

# 保留旧变量名以兼容（但不再使用）
SUMMARIZE_PROMPT = PROCESS_PROMPT
CLASSIFY_PROMPT = ""
