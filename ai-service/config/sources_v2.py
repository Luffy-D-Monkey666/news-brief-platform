"""
新闻源配置 V2 - 全面升级信息源体系

核心改进：
1. 增加 X (Twitter) 社交媒体源
2. 增加微信公众号、知乎等中文源
3. 优化源质量，移除低价值RSS
4. 分类更精准，减少噪音
"""

# ====================================
# 1. X (Twitter) 信息源
# ====================================
# 使用 RSSHub 的 Twitter 路由（免费）
# 格式: https://rsshub.app/twitter/user/{用户名}

TWITTER_SOURCES = {
    'ai_technology': [
        # AI 大佬与官方账号
        'https://rsshub.app/twitter/user/OpenAI',           # OpenAI 官方
        'https://rsshub.app/twitter/user/DeepMind',         # DeepMind 官方
        'https://rsshub.app/twitter/user/ylecun',           # Yann LeCun (Meta AI Chief)
        'https://rsshub.app/twitter/user/AndrewYNg',        # 吴恩达
        'https://rsshub.app/twitter/user/karpathy',         # Andrej Karpathy (前Tesla AI)
        'https://rsshub.app/twitter/user/goodfellow_ian',   # Ian Goodfellow (GAN之父)
        'https://rsshub.app/twitter/user/hardmaru',         # 知名AI博主
        'https://rsshub.app/twitter/user/nathanbenaich',    # AI投资者
    ],
    'robotics': [
        # 机器人公司与研究者
        'https://rsshub.app/twitter/user/BostonDynamics',   # 波士顿动力
        'https://rsshub.app/twitter/user/Tesla_Optimus',    # Tesla Bot
        'https://rsshub.app/twitter/user/1x_tech',          # 1X Technologies
        'https://rsshub.app/twitter/user/Figure_robot',     # Figure AI
        'https://rsshub.app/twitter/user/AgilityRobotics',  # Agility Robotics
    ],
    'semiconductors': [
        # 芯片行业
        'https://rsshub.app/twitter/user/nvidia',           # NVIDIA
        'https://rsshub.app/twitter/user/AMD',              # AMD
        'https://rsshub.app/twitter/user/Intel',            # Intel
        'https://rsshub.app/twitter/user/ARMCommunity',     # ARM
        'https://rsshub.app/twitter/user/anandshimpi',      # Anand Shimpi (AnandTech)
    ],
    'automotive': [
        # 汽车行业
        'https://rsshub.app/twitter/user/Tesla',            # Tesla
        'https://rsshub.app/twitter/user/elonmusk',         # Elon Musk
        'https://rsshub.app/twitter/user/ElectrekCo',       # Electrek
        'https://rsshub.app/twitter/user/InsideEVs',        # InsideEVs
    ],
    'consumer_electronics': [
        # 消费电子
        'https://rsshub.app/twitter/user/verge',            # The Verge
        'https://rsshub.app/twitter/user/engadget',         # Engadget
        'https://rsshub.app/twitter/user/MKBHD',            # Marques Brownlee
    ],
    'business_tech': [
        # 商业科技
        'https://rsshub.app/twitter/user/TechCrunch',       # TechCrunch
        'https://rsshub.app/twitter/user/BloombergTech',    # Bloomberg Tech
        'https://rsshub.app/twitter/user/recode',           # Recode
    ],
}

# ====================================
# 2. 中文本土信息源（WeChat/知乎/即刻）
# ====================================

CHINA_SOURCES = {
    'wechat_official': [
        # 微信公众号（通过 RSSHub）
        'https://rsshub.app/wechat/mp/抖音集团',             # 抖音技术团队
        'https://rsshub.app/wechat/mp/阿里巴巴',             # 阿里巴巴官方
        'https://rsshub.app/wechat/mp/腾讯科技',             # 腾讯科技
        'https://rsshub.app/wechat/mp/百度AI',               # 百度AI
        'https://rsshub.app/wechat/mp/华为开发者',           # 华为开发者
    ],
    'zhihu': [
        # 知乎专栏/话题
        'https://rsshub.app/zhihu/topic/19550517',           # 人工智能话题
        'https://rsshub.app/zhihu/topic/19550728',           # 机器学习话题
        'https://rsshub.app/zhihu/topic/19550538',           # 芯片话题
    ],
    'jike': [
        # 即刻圈子（通过 RSSHub）
        'https://rsshub.app/jike/topic/56d2f9b6cfe47312089448c6',  # 人工智能
        'https://rsshub.app/jike/topic/5b5e2f43c2e78d00172d9988',  # 科技资讯
    ],
}

# ====================================
# 3. 优化后的 RSS 源（精选高质量）
# ====================================

RSS_SOURCES_V2 = {
    'ai_technology': [
        # 官方源（高优先级）
        'https://openai.com/blog/rss/',
        'https://blog.research.google/rss/',
        'https://www.deepmind.com/blog/rss.xml',
        'https://huggingface.co/blog/rss.xml',
        'https://mistral.ai/news/rss.xml',
        
        # 中国 AI 媒体
        'https://rsshub.app/jiqizhixin/ai',     # 机器之心
        'https://rsshub.app/qbitai',            # 量子位
        
        # 学术源
        'https://rsshub.app/arxiv/cs.AI',       # arXiv AI
        'https://syncedreview.com/feed/',       # Synced (英文)
    ],
    
    'robotics': [
        'https://robohub.org/feed/',
        'https://spectrum.ieee.org/robotics/rss',
        'https://rsshub.app/irobotnews',        # 韩国机器人新闻
        'https://csail.mit.edu/news/rss.xml',
    ],
    
    'ai_programming': [
        'https://github.blog/feed/',
        'https://code.visualstudio.com/feed.xml',
        'https://engineering.fb.com/feed/',
        'https://rsshub.app/hackernews/best',   # Hacker News 热门
    ],
    
    'semiconductors': [
        'https://www.eetimes.com/feed/',
        'https://semiengineering.com/feed/',
        'https://www.anandtech.com/rss/',
        'https://www.tomshardware.com/rss.xml',
    ],
    
    'opcg': [
        # Reddit 社区（保留）
        'https://rsshub.app/reddit/r/OnePieceTCG',
        # 日本官方
        'https://one-piece-cardgame.com/news/rss.xml',  # 日版官网（如有）
    ],
    
    'automotive': [
        'https://electrek.co/feed/',
        'https://insideevs.com/rss/',
        'https://rsshub.app/dongchedi/news',    # 懂车帝
        'https://feeds.bloomberg.com/markets/autos.rss',
    ],
    
    'consumer_electronics': [
        'https://www.theverge.com/tech/rss/index.xml',
        'https://www.engadget.com/rss.xml',
        'https://9to5mac.com/feed/',
        'https://rsshub.app/ithome/it',         # IT之家
    ],
    
    'one_piece': [
        'https://rsshub.app/reddit/r/OnePiece',
        'https://www.animenewsnetwork.com/all/rss.xml',
    ],
    
    # 播客推荐（减少数量，保留精品）
    'podcasts': [
        'https://rsshub.app/xiaoyuzhoufm/explore',  # 小宇宙精选
        # 仅保留头部播客
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff4492c',  # 罗永浩
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f950a789fca4eff44930',  # 硅谷101
        'https://rsshub.app/xiaoyuzhoufm/podcast/60c2c908f58fc5806da89fcc',  # 疯投圈
    ],
    
    'finance_investment': [
        'https://rsshub.app/caixin/finance',    # 财新
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.ft.com/rss/home',
        'https://rsshub.app/nikkei/index',      # 日经
    ],
    
    'business_tech': [
        'https://techcrunch.com/feed/',
        'https://rsshub.app/36kr/newsflashes',  # 36氪快讯
        'https://www.technologyreview.com/feed/',
    ],
    
    'politics_world': [
        'https://www.reuters.com/rssFeed/worldNews',
        'https://www.theguardian.com/world/rss',
        'https://thediplomat.com/rss/',
    ],
    
    'health_medical': [
        'https://rsshub.app/statnews',          # Stat News
        'https://www.who.int/rss-feeds/news-english.xml',
        'https://rsshub.app/thelancet/current', # The Lancet
    ],
    
    'energy_environment': [
        'https://rsshub.app/iea/news',          # IEA
        'https://www.carbon-brief.org/feed',
        'https://cleantechnica.com/feed/',
    ],
    
    # 综合新闻（精简）
    'general': [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://rsshub.app/thepaper/featured', # 澎湃新闻
    ],
}

# ====================================
# 4. 合并所有源
# ====================================

NEWS_SOURCES_V2 = {
    'rss_feeds': [],
    'twitter': [],
    'wechat': [],
    'zhihu': [],
    'jike': [],
}

# 合并 RSS 源
for category, urls in RSS_SOURCES_V2.items():
    NEWS_SOURCES_V2['rss_feeds'].extend(urls)

# 合并 Twitter 源
for category, urls in TWITTER_SOURCES.items():
    NEWS_SOURCES_V2['twitter'].extend(urls)

# 合并中文源
NEWS_SOURCES_V2['wechat'] = CHINA_SOURCES['wechat_official']
NEWS_SOURCES_V2['zhihu'] = CHINA_SOURCES['zhihu']
NEWS_SOURCES_V2['jike'] = CHINA_SOURCES['jike']

# 统计
TOTAL_SOURCES = (
    len(NEWS_SOURCES_V2['rss_feeds']) +
    len(NEWS_SOURCES_V2['twitter']) +
    len(NEWS_SOURCES_V2['wechat']) +
    len(NEWS_SOURCES_V2['zhihu']) +
    len(NEWS_SOURCES_V2['jike'])
)

print(f"新闻源 V2 统计:")
print(f"  - RSS 源: {len(NEWS_SOURCES_V2['rss_feeds'])} 个")
print(f"  - Twitter/X 源: {len(NEWS_SOURCES_V2['twitter'])} 个")
print(f"  - 微信公众号: {len(NEWS_SOURCES_V2['wechat'])} 个")
print(f"  - 知乎话题: {len(NEWS_SOURCES_V2['zhihu'])} 个")
print(f"  - 即刻圈子: {len(NEWS_SOURCES_V2['jike'])} 个")
print(f"  - 总计: {TOTAL_SOURCES} 个")
