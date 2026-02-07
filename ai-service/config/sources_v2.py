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
# 3. YouTube 视频信息源
# ====================================
# 使用 RSSHub 的 YouTube 路由（免费）
# 格式: https://rsshub.app/youtube/user/{用户名}
#       https://rsshub.app/youtube/channel/{频道ID}

YOUTUBE_SOURCES = {
    'ai_technology': [
        # AI 技术频道
        'https://rsshub.app/youtube/channel/UCbfYPyITQ-7l4upoX8nvctg',  # Two Minute Papers
        'https://rsshub.app/youtube/channel/UCV0qA-eDDICsRRiR59ecugA',  # Computerphile
        'https://rsshub.app/youtube/channel/UCP7jMXSY2xbc3KCAE0MHQ-A',  # AI Explained
        'https://rsshub.app/youtube/channel/UCsBjURrPoezykLs9EqgamOA',  # Fireship
        'https://rsshub.app/youtube/channel/UCr8O1y-J6H8-rxODLdlB1nQ',  # MattVidPro AI
    ],
    'robotics': [
        # 机器人频道
        'https://rsshub.app/youtube/channel/UCqDMvCa1tqq2Z1VXTPkGg1g',  # Boston Dynamics
        'https://rsshub.app/youtube/channel/UCqJOD4fI2Xaam3bqH5iUKZQ',  # Tesla
        'https://rsshub.app/youtube/channel/UCq0mDCW_7jw3K36R5n8v8fg',  # Soft Robotics
        'https://rsshub.app/youtube/channel/UCXbY6bYYf3YZLBO2HDDPClQ',  # DroneBot Workshop
    ],
    'semiconductors': [
        # 芯片/硬件频道
        'https://rsshub.app/youtube/channel/UCkZRYzDz5Rsb4Rd3DtNHk3g',  # Gamers Nexus (硬件深度)
        'https://rsshub.app/youtube/channel/UC0vBXGSyV14OJGNnYm4xGqg',  # Moore's Law Is Dead
        'https://rsshub.app/youtube/channel/UC8CbFnDTYkiVweaz8JS9QEg',  # Coreteks (芯片分析)
        'https://rsshub.app/youtube/channel/UC6WDJm2CCczC9xT6J7E7gmg',  # Hardware Canucks
    ],
    'automotive': [
        # 汽车频道
        'https://rsshub.app/youtube/channel/UCBa659QWEk1AI4Tg--mrJ2A',  # Fully Charged Show
        'https://rsshub.app/youtube/channel/UCbprhISv-0ReKPPyhf7-Dtw',  # Out of Spec Reviews
        'https://rsshub.app/youtube/channel/UC9WCkA1UFtMKRAX8HSR-4zQ',  # The Fast Lane Car
        'https://rsshub.app/youtube/channel/UCc2qdh0ge_W1fQfTRa5mKwQ',  # Engineering Explained
    ],
    'consumer_electronics': [
        # 消费电子评测
        'https://rsshub.app/youtube/channel/UCBJycsmduvYEL83R_U4JriQ',  # MKBHD
        'https://rsshub.app/youtube/channel/UCX6OQ3DkcsbYNE6H8uQQuVA',  # Mrwhosetheboss
        'https://rsshub.app/youtube/channel/UCGy7SkBjcIAgTiwkXEtPnYg',  # Arun Maini
        'https://rsshub.app/youtube/channel/UCdBK94H6oZT2Q7l0-bWmxKA',  # The Verge
        'https://rsshub.app/youtube/channel/UCa6TeYZ2DlueFRne5DyAnyg',  # Unbox Therapy
        'https://rsshub.app/youtube/channel/UCR0AnF7hbhIJ9SjS5GzB9rw',  # Dave2D
        'https://rsshub.app/youtube/channel/UCy0tL1HwJ5d2LqKgeG4L2aw',  # Linus Tech Tips
    ],
    'opcg': [
        # OPCG 卡牌游戏
        'https://rsshub.app/youtube/channel/UCq6OWaxEmHyfGaf2oAYhm5g',  # Wossy Plays
        'https://rsshub.app/youtube/channel/UCmUl0hYlQ7_sM00JRIMcZtg',  # The Egman
        'https://rsshub.app/youtube/channel/UC3GumCi7KRNGRIFfI5nQSmw',  # VvTheory
        'https://rsshub.app/youtube/channel/UC6FFxWAuo47tSa1joqHqhlA',  # One Piece Card Game Official
    ],
    'one_piece': [
        # 海贼王动漫
        'https://rsshub.app/youtube/channel/UCMpWpGXG8PqAvM-HY2tfNtw',  # Library of Ohara
        'https://rsshub.app/youtube/channel/UCRwox6tQO5nDVx8_Lwoqybw',  # RogersBase
    ],
    'ai_programming': [
        # 编程/技术频道
        'https://rsshub.app/youtube/channel/UCsBjURrPoezykLs9EqgamOA',  # Fireship
        'https://rsshub.app/youtube/channel/UCS0N5baNlQWJCUrhCEo8WlA',  # Ben Eater
        'https://rsshub.app/youtube/channel/UC4JX40jDee_tINbkjycV4Sg',  # Tech With Tim
        'https://rsshub.app/youtube/channel/UC8OlhdAj0aZL9eeE7gPfHEA',  # Programming with Mosh
        'https://rsshub.app/youtube/channel/UCl5-BV9aRaeDVohpE4sqJiQ',  # The Coding Train
    ],
    'finance_investment': [
        # 财经投资频道
        'https://rsshub.app/youtube/channel/UCFCEuCsyWP0YkPbaXzF4G4w',  # Financial Times
        'https://rsshub.app/youtube/channel/UCrM7B7SL_g1edFOnmj-SDKg',  # Bloomberg Television
        'https://rsshub.app/youtube/channel/UC-4bDH2ApW2ZaAOUVZsn8cQ',  # CNBC Television
        'https://rsshub.app/youtube/channel/UCaqzC3nF9F2ZzmqXWWE9DlQ',  # Patrick Boyle
    ],
    'business_tech': [
        # 商业科技
        'https://rsshub.app/youtube/channel/UCdBK94H6oZT2Q7l0-bWmxKA',  # The Verge
        'https://rsshub.app/youtube/channel/UCj22tfcQr_F7l4KSeyRWu7Q',  # TechCrunch
        'https://rsshub.app/youtube/channel/UCVLZmDKeT-VDqxD2ExagzCw',  # Bloomberg Originals
    ],
    'general': [
        # 综合科技新闻
        'https://rsshub.app/youtube/channel/UC0vBXGSyV14OJGNnYm4xGqg',  # Moore's Law Is Dead
        'https://rsshub.app/youtube/channel/UCBJycsmduvYEL83R_U4JriQ',  # MKBHD
    ],
}

# ====================================
# 4. 优化后的 RSS 源（精选高质量）
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
    'youtube': [],
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

# 合并 YouTube 源
for category, urls in YOUTUBE_SOURCES.items():
    NEWS_SOURCES_V2['youtube'].extend(urls)

# 统计
TOTAL_SOURCES = (
    len(NEWS_SOURCES_V2['rss_feeds']) +
    len(NEWS_SOURCES_V2['twitter']) +
    len(NEWS_SOURCES_V2['wechat']) +
    len(NEWS_SOURCES_V2['zhihu']) +
    len(NEWS_SOURCES_V2['jike']) +
    len(NEWS_SOURCES_V2['youtube'])
)

print(f"新闻源 V2 统计:")
print(f"  - RSS 源: {len(NEWS_SOURCES_V2['rss_feeds'])} 个")
print(f"  - Twitter/X 源: {len(NEWS_SOURCES_V2['twitter'])} 个")
print(f"  - 微信公众号: {len(NEWS_SOURCES_V2['wechat'])} 个")
print(f"  - 知乎话题: {len(NEWS_SOURCES_V2['zhihu'])} 个")
print(f"  - 即刻圈子: {len(NEWS_SOURCES_V2['jike'])} 个")
print(f"  - YouTube 频道: {len(NEWS_SOURCES_V2['youtube'])} 个")
print(f"  - 总计: {TOTAL_SOURCES} 个")
