import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 120))  # 2分钟

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
        'cleantechnica.com', 'greentechmedia.com', 'carbonbrief.org'
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

# 合并的摘要+分类提示词（v2.1：三段式 + 原文引用 + 重要性 + 行动建议）
PROCESS_PROMPT = """你是资深新闻编辑，分析以下新闻并输出JSON。

分类（注意区分）：
- ai_technology: AI技术
- robotics: 机器人
- ai_programming: AI编程工具
- semiconductors: 芯片半导体
- automotive: 汽车
- consumer_electronics: 消费电子
- podcasts: 播客节目
- finance_investment: 投资财经
- business_tech: 商业科技
- politics_world: 政治国际
- economy_policy: 经济政策
- health_medical: 健康医疗
- energy_environment: 能源环境
- entertainment_sports: 娱乐体育
- anime: 动漫二次元（非海贼王的动漫）
- one_piece: 海贼王/One Piece（专门用于海贼王相关内容，包括漫画、动画、讨论）
- tcg: TCG卡牌游戏（游戏王/PTCG/OPCG/MTG等）
- general: 综合

新闻标题: {title}
新闻内容: {content}

输出要求：
1. title_zh: 中文标题，≤30字
2. category: 从上面分类中选一个
3. importance: 判断重要性
   - "breaking": 重大突发（战争/灾难/巨头重大发布/全球性事件）
   - "high": 较重要（行业重要动态）
   - "normal": 普通新闻
4. summary: 结构化摘要，必须包含以下部分：
   - "事件概述:" 1-2句话说清楚发生了什么
   - "原文引用:" 提取原文中最有价值的1句话（英文保留原文，标注说话人）
   - "重要细节:" 用•列出3-4个关键信息点
   - "后续影响:" 分析意义和后续发展
5. action_advice: 仅当category是finance_investment/business_tech/economy_policy时生成，包含风险提示和行动建议，其他分类设为null
6. key_metrics: 提取新闻中的关键数字/指标，数组格式，每个元素包含：
   - name: 指标名称（如"营收"、"用户数"、"股价"、"融资额"等）
   - value: 数值
   - unit: 单位（如"亿美元"、"万人"、"%"等）
   - entity: 关联实体（公司/产品名，如"OpenAI"、"GPT-5"）
   如果新闻中没有明确数字，设为空数组[]

输出示例：
{{
  "title_zh": "OpenAI发布GPT-5，性能提升3倍",
  "category": "ai_technology",
  "importance": "breaking",
  "summary": "事件概述: OpenAI正式发布GPT-5模型，在推理能力和多模态理解方面实现重大突破。\n\n原文引用: \"This is a pivotal moment for AI safety and capability.\" — Sam Altman, CEO\n\n重要细节:\n• 发布时间：2026年2月18日\n• 性能提升：推理速度提升3倍，准确率提高40%\n• 定价：API价格维持不变\n• 已向部分企业开放测试\n\n后续影响: GPT-5的发布将加速AI应用落地，预计对搜索、编程、教育等行业产生深远影响。竞争对手可能加快发布节奏。",
  "action_advice": null,
  "key_metrics": [
    {{"name": "性能提升", "value": 3, "unit": "倍", "entity": "GPT-5"}},
    {{"name": "准确率提升", "value": 40, "unit": "%", "entity": "GPT-5"}}
  ]
}}

财经类示例：
{{
  "title_zh": "特斯拉Q4营收251亿美元，同比增长3%",
  "category": "finance_investment",
  "importance": "high",
  "summary": "事件概述: 特斯拉发布2025年Q4财报，营收251亿美元，略低于市场预期。\n\n原文引用: \"We remain focused on cost reduction and new product launches.\" — Elon Musk\n\n重要细节:\n• Q4营收：251亿美元\n• 同比增长：3%\n• 汽车毛利率：17.6%\n• 全年交付量：180万辆\n\n后续影响: 增速放缓反映电动车市场竞争加剧，投资者关注Cybertruck量产进展和FSD收入增长。",
  "action_advice": "⚠️ 风险提示: 增速放缓，毛利率承压，需关注竞争格局变化\n\n✅ 行动建议:\n• 关注后续交付数据和新车型发布\n• 注意估值与增速匹配度",
  "key_metrics": [
    {{"name": "Q4营收", "value": 251, "unit": "亿美元", "entity": "特斯拉"}},
    {{"name": "同比增长", "value": 3, "unit": "%", "entity": "特斯拉"}},
    {{"name": "汽车毛利率", "value": 17.6, "unit": "%", "entity": "特斯拉"}},
    {{"name": "全年交付量", "value": 180, "unit": "万辆", "entity": "特斯拉"}}
  ]
}}

请严格按此格式输出JSON："""

# 保留旧变量名以兼容（但不再使用）
SUMMARIZE_PROMPT = PROCESS_PROMPT
CLASSIFY_PROMPT = ""
