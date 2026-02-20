import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 300))  # 5分钟

# ============================================================
# 来源可信度分级配置
# ============================================================
SOURCE_TIERS = {
    # 🏛️ 官方来源：公司/政府官方发布
    'official': [
        'openai.com', 'blog.google', 'apple.com', 'microsoft.com',
        'nvidia.com', 'tesla.com', 'anthropic.com', 'deepmind.com',
        'huggingface.co', 'github.blog', 'machinelearning.apple.com',
        'whitehouse.gov', 'imf.org', 'worldbank.org', 'oecd.org'
    ],
    # 📰 权威媒体：主流新闻机构
    'mainstream': [
        'nytimes.com', 'bbc.com', 'bbc.co.uk', 'reuters.com',
        'theguardian.com', 'bloomberg.com', 'ft.com', 'wsj.com',
        'economist.com', 'aljazeera.com', 'apnews.com'
    ],
    # 🔬 专业媒体：垂直领域媒体
    'specialized': [
        'techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
        'venturebeat.com', 'engadget.com', 'anandtech.com', 'tomshardware.com',
        'electrek.co', 'insideevs.com', 'semiengineering.com', 'eetimes.com',
        'statnews.com', 'fiercebiotech.com', 'variety.com', 'hollywoodreporter.com',
        '9to5mac.com', '9to5google.com', 'gsmarena.com', 'therobotreport.com',
        'cleantechnica.com', 'greentechmedia.com', 'carbonbrief.org',
        'technologyreview.com', 'cnet.com', 'theregister.com',  # 商业科技
        'techinasia.com', 'tech.eu',  # 区域科技
        'krebsonsecurity.com', 'spacenews.com',  # 安全+航天
        'news.crunchbase.com', 'spectrum.ieee.org',  # 创投+工程
        'nature.com', 'science.org'  # 学术科学
    ],
    # 💬 社区来源：Reddit、论坛、个人博客
    'community': [
        'reddit.com', 'news.ycombinator.com', 'medium.com',
        'substack.com', 'dev.to', 'hackernoon.com'
    ]
}

def get_source_tier(source_url: str) -> str:
    """根据来源URL判断可信度等级"""
    if not source_url:
        return 'community'
    
    source_url = source_url.lower()
    
    for tier, domains in SOURCE_TIERS.items():
        for domain in domains:
            if domain in source_url:
                return tier
    
    return 'community'  # 默认为社区来源

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
# 新闻源配置（精选优质源，共约55个）
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

        # ==================== 机器人（6个核心源）====================
        'https://www.therobotreport.com/feed/',            # The Robot Report
        'https://robohub.org/feed/',                       # Robohub（学术机器人）
        'https://spectrum.ieee.org/feeds/topic/robotics.rss', # IEEE Spectrum机器人
        'https://spectrum.ieee.org/feeds/feed.rss',        # IEEE Spectrum综合（工程技术全领域）
        'https://www.automate.org/rss/news',               # Automate（工业机器人）
        'https://bdtechtalks.com/feed/',                   # BD Tech Talks 机器人
        # 已移除：Reddit 论坛类源（讨论帖多，新闻价值低，消耗token）
        # 'https://www.reddit.com/r/robotics/.rss',
        # 'https://www.reddit.com/r/teslabot/.rss',
        # 'https://www.reddit.com/r/singularity/.rss',

        # ==================== AI编程/Agent（7个核心源）====================
        'https://github.blog/feed/',                       # GitHub官方博客
        'https://code.visualstudio.com/feed.xml',          # VSCode官方
        'https://blog.stackblitz.com/rss/',                # StackBlitz
        'https://www.cursor.com/blog/rss.xml',             # Cursor官方
        'https://www.latent.space/feed',                   # Latent Space
        'https://lilianweng.github.io/index.xml',          # Lil'Log AI博客
        'https://simonwillison.net/atom/everything/',      # Simon Willison
        # 已移除：Reddit LocalLLaMA（技术讨论为主，非新闻）
        # 'https://www.reddit.com/r/LocalLLaMA/.rss',

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

        # ==================== 消费电子（3个核心源）====================
        'https://www.theverge.com/rss/index.xml',          # The Verge
        'https://9to5mac.com/feed/',                       # 9to5Mac
        'https://9to5google.com/feed/',                    # 9to5Google
        # 已移除：Engadget（与 Verge 重复）、GSMArena（手机评测为主）

        # ==================== 播客推荐 ====================
        # 已移除整个分类：播客内容不适合新闻聚合
        # 'https://lexfridman.com/feed/podcast/',
        # 'https://feeds.megaphone.fm/hubaborhood',
        # 'https://feeds.simplecast.com/54nAGcIl',
        # 'https://twimlai.com/feed/',

        # ==================== 投资财经（4个核心源）====================
        'https://feeds.bloomberg.com/markets/news.rss',    # Bloomberg Markets
        'https://www.ft.com/rss/home',                     # Financial Times
        'https://www.economist.com/finance-and-economics/rss.xml', # Economist
        'https://news.crunchbase.com/feed/',               # Crunchbase News（创投数据新闻）
        # 已移除：Seeking Alpha（UGC质量参差）、CoinDesk（加密货币）

        # ==================== 商业科技（9个核心源）====================
        'https://techcrunch.com/feed/',                    # TechCrunch
        'https://www.wired.com/feed/rss',                  # Wired
        'https://arstechnica.com/feed/',                   # Ars Technica
        'https://venturebeat.com/feed/',                   # VentureBeat
        'https://www.fastcompany.com/technology/rss',      # Fast Company Tech
        'https://www.technologyreview.com/feed/',          # MIT Technology Review（深度科技分析）
        'https://www.cnet.com/rss/news/',                  # CNET（消费科技全覆盖）
        'https://www.theregister.com/headlines.atom',      # The Register（英国IT深度报道）
        'https://krebsonsecurity.com/feed/',               # Krebs on Security（网络安全权威）

        # ==================== 政治国际（4个核心源）====================
        'https://www.theguardian.com/world/rss',           # Guardian World
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', # NYT World
        'https://feeds.bbci.co.uk/news/world/rss.xml',     # BBC World
        'https://www.aljazeera.com/xml/rss/all.xml',       # Al Jazeera

        # ==================== 经济政策（3个核心源）====================
        'https://www.imf.org/en/News/rss',                 # IMF
        'https://www.worldbank.org/en/news/rss.xml',       # World Bank
        'https://www.oecd.org/economy/rss.xml',            # OECD Economy

        # ==================== 健康医疗/科学（5个核心源）====================
        'https://www.statnews.com/feed/',                  # STAT News
        'https://www.fiercebiotech.com/rss/xml',           # Fierce Biotech
        'https://medicalxpress.com/rss-feed/',             # Medical Xpress
        'https://www.nature.com/nature.rss',               # Nature News（顶级科学期刊）
        'https://www.science.org/rss/news_current.xml',    # Science News（AAAS科学新闻）

        # ==================== 能源环境/航天（5个核心源）====================
        'https://www.greentechmedia.com/feed/',            # Greentech Media
        'https://www.renewableenergyworld.com/feed/',      # Renewable Energy World
        'https://www.carbonbrief.org/feed/',               # Carbon Brief
        'https://spacenews.com/feed/',                     # SpaceNews（航天产业）
        'https://arstechnica.com/space/feed/',             # Ars Technica Space

        # ==================== 娱乐体育（3个核心源）====================
        'https://variety.com/feed/',                       # Variety
        'https://www.hollywoodreporter.com/feed/',         # Hollywood Reporter
        'https://www.espn.com/espn/rss/news',              # ESPN

        # ==================== 动漫二次元（3个核心源）====================
        'https://www.animenewsnetwork.com/all/rss.xml',    # Anime News Network
        'https://www.crunchyroll.com/feed',                # Crunchyroll
        'https://myanimelist.net/rss/news.xml',            # MyAnimeList

        # ==================== OP海贼王（2个核心源）====================
        'https://onepiece.fandom.com/wiki/Special:NewPages?feed=rss', # OP Wiki
        'https://comicbook.com/anime/feed/',               # ComicBook Anime
        # 已移除：Reddit OnePiece（漫画讨论、剧透帖为主）
        # 'https://www.reddit.com/r/OnePiece/.rss',

        # ==================== TCG集换式卡牌（1个核心源）====================
        'https://www.tcgplayer.com/blog/feed/',            # TCGPlayer Blog（官方新闻）
        # 已移除：所有 Reddit TCG 论坛（卡组讨论、交易帖为主，非新闻）
        # 'https://www.reddit.com/r/OnePieceTCG/.rss',
        # 'https://www.reddit.com/r/PokemonTCG/.rss',
        # 'https://www.reddit.com/r/yugioh/.rss',
        # 'https://www.reddit.com/r/magicTCG/.rss',
        # 'https://www.reddit.com/r/DigimonCardGame2020/.rss',
        # 'https://www.reddit.com/r/WeissSchwarz/.rss',

        # ==================== 区域科技（亚洲+欧洲视角）====================
        'https://www.techinasia.com/feed',                 # Tech in Asia（亚洲科技创投）
        'https://tech.eu/feed/',                           # Tech.eu（欧洲科技生态）

        # ==================== 综合新闻（3个核心源）====================
        'https://feeds.feedburner.com/TechCrunch/',        # TechCrunch综合
        # 'https://news.ycombinator.com/rss',              # Hacker News（已移除：链接聚合站，内容多为外部网站转发）
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', # NYT首页
        'https://www.reuters.com/rssFeed/technologyNews',  # Reuters Tech
    ]
}

# ============================================================
# AI提示词模板（优化版：合并摘要+分类，大幅减少token）
# ============================================================

# AI提示词模板（v3精简版：减少约40% token）
# ============================================================

from config.prompt_v3 import PROCESS_PROMPT_V3

PROCESS_PROMPT = PROCESS_PROMPT_V3

# 保留旧变量名以兼容
SUMMARIZE_PROMPT = PROCESS_PROMPT
CLASSIFY_PROMPT = ""
