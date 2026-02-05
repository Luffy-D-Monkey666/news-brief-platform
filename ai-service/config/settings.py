import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/news-brief')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# 爬虫配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 300))  # 5分钟（优化Token消耗：降低60%调用频率）

# 新闻分类（基于国际新闻标准，突出用户关注领域）
CATEGORIES = [
    # 核心关注领域（最高优先级）
    'ai_technology',         # AI技术
    'robotics',              # 机器人（原embodied_intelligence）
    'ai_programming',        # AI编程（原coding_development）
    'semiconductors',        # 芯片半导体
    'opcg',                  # OPCG卡牌游戏（原opcg_tcg）
    'automotive',            # 汽车（原ev_automotive，现包含所有类型汽车）
    'consumer_electronics',  # 消费电子（手机、手表、眼镜、相机等）
    'one_piece',             # ONE PIECE（海贼王动漫周边）
    'podcasts',              # 播客节目
    'finance_investment',    # 投资财经

    # 主流新闻分类
    'business_tech',         # 商业科技
    'politics_world',        # 政治国际
    'economy_policy',        # 经济政策
    'health_medical',        # 健康医疗
    'energy_environment',    # 能源环境
    'entertainment_sports',  # 娱乐体育
    'general'               # 综合
]

# 分类中文名称映射
CATEGORY_NAMES = {
    # 核心关注领域
    'ai_technology': 'AI技术',
    'robotics': '机器人',
    'ai_programming': 'AI编程',
    'semiconductors': '芯片',
    'opcg': 'OPCG',
    'automotive': '汽车',
    'consumer_electronics': '消费电子',
    'one_piece': 'OP',
    'podcasts': '播客推荐',
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

# 新闻源配置（全球专业信源，100+新闻源）
NEWS_SOURCES = {
    'rss_feeds': [
        # ==================== AI技术（12个核心源）====================
        'https://rsshub.app/jiqizhixin/ai',  # 机器之心（中国最深度AI论文解读）
        'https://rsshub.app/qbitai',  # 量子位（AI产业动态与大模型落地）
        'https://rsshub.app/mistral/news',  # Mistral AI（欧洲最强开源模型）
        'https://rsshub.app/thenextweb/ai',  # TNW（欧洲AI监管与创新生态）
        'https://rsshub.app/ledge/news',  # Ledge.ai（日本AI商业应用）
        'https://rsshub.app/arxiv/cs.AI',  # arXiv AI论文（趋势预测）
        'https://openai.com/blog/rss/',  # OpenAI官方博客（最前沿AI研究与产品）
        'https://blog.research.google/rss/',  # Google AI Research（谷歌AI研究）
        'https://www.deepmind.com/blog/rss.xml',  # DeepMind官方（强化学习AlphaGo）
        'https://huggingface.co/blog/rss.xml',  # Hugging Face（开源模型社区）
        'https://www.unite.ai/feed/',  # Unite.AI（企业AI应用案例）
        'https://www.infoq.com/ai/rss',  # InfoQ AI（AI工程化最佳实践）

        # ==================== 机器人（8个核心源）====================
        'https://rsshub.app/irobotnews',  # Robot News韩国（三星/现代机器人）
        'https://rsshub.app/robotstart',  # Robot Start日本（全球机器人密度最高国）
        'https://robohub.org/feed/',  # Robohub瑞士（顶尖学术背景物理AI）
        'https://rsshub.app/sps-magazin',  # SPS德国（工业4.0核心资讯）
        'https://www.ieee.org/about/news/rss.xml',  # IEEE官方新闻（机器人标准）
        'https://csail.mit.edu/news/rss.xml',  # MIT CSAIL（具身AI研究前沿）
        'https://www.cs.cmu.edu/news/rss.xml',  # CMU计算机（机器人与AI研究）
        'https://ai.stanford.edu/news/rss.xml',  # Stanford AI Lab（人形机器人）

        # ==================== 芯片半导体（10个核心源）====================
        'https://rsshub.app/eet-china/news',  # 电子工程专辑（中国芯片产业）
        'https://rsshub.app/anandtech',  # AnandTech（最深度硬件测评）
        'https://rsshub.app/tomshardware',  # Tom's Hardware（硬件新闻）
        'https://www.eetimes.com/feed/',  # EE Times（全球半导体行业）
        'https://www.semiwiki.com/feed/',  # SemiWiki（芯片设计分析）
        'https://www.semiconductor-today.com/rss.xml',  # Semiconductor Today
        'https://semiengineering.com/feed/',  # Semiconductor Engineering
        'https://www.eetimes.eu/feed/',  # EE Times Europe（欧洲半导体）
        'https://www.electronicsweekly.com/feed/',  # Electronics Weekly
        'https://www.ednasia.com/feed/',  # EDN Asia（亚洲电子设计）

        # ==================== OPCG卡牌游戏（4个核心源）====================
        'https://rsshub.app/reddit/r/OnePieceTCG',  # Reddit OPCG社区（玩家讨论、Meta分析）
        'https://rsshub.app/youtube/user/@WossyPlays',  # Wossy Plays（最勤快的OPCG新闻博主）
        'https://rsshub.app/youtube/user/@TheEgman',  # The Egman（赛事数据分析）
        'https://rsshub.app/youtube/user/@VvTheory',  # VvTheory（深度对局复盘）

        # ==================== 消费电子（10个核心源）====================
        'https://www.theverge.com/tech/rss/index.xml',  # The Verge科技（消费电子测评）
        'https://www.engadget.com/rss.xml',  # Engadget（全球消费电子）
        'https://www.gsmarena.com/rss-news.php3',  # GSMArena（手机专业评测）
        'https://rsshub.app/ithome/it',  # IT之家（中国消费电子）
        'https://www.anandtech.com/rss/',  # AnandTech（硬件深度测评）
        'https://www.androidpolice.com/feed/',  # Android Police（安卓设备）
        'https://9to5mac.com/feed/',  # 9to5Mac（苹果产品）
        'https://www.dpreview.com/feeds/news.xml',  # DPReview（相机评测）
        'https://www.dronedj.com/feed/',  # DroneDJ（无人机新闻）
        'https://www.phonearena.com/rss/news',  # PhoneArena（手机行业）

        # ==================== ONE PIECE动漫周边（3个核心源 - 已清理低质量源）====================
        'https://rsshub.app/reddit/r/OnePiece',  # Reddit海贼王社区（社区讨论）
        'https://rsshub.app/youtube/user/@TheLibraryofOhara',  # Library of Ohara（OP深度解析）
        'https://www.animenewsnetwork.com/all/rss.xml',  # Anime News Network（动漫行业新闻）
        # 已移除：B站视频源（非新闻）、Wiki更新（非新闻）、Crunchyroll全动漫（OP占比低）、周边测评（非新闻）

        # ==================== Coding开发（15个核心源 - 重点覆盖AI编程工具）====================
        # AI编程工具官方源
        'https://github.blog/feed/',  # GitHub官方博客（Copilot更新）
        'https://code.visualstudio.com/feed.xml',  # VSCode官方（Copilot集成）
        'https://cursor.sh/blog/rss.xml',  # Cursor官方博客（如果有RSS）

        # 开发者社区（AI编程讨论热点 - 已降权）
        'https://rsshub.app/hackernews/best',  # Hacker News（AI工具讨论） - 仅采集前5条
        # 已移除：Dev.to（教程居多）、Reddit编程话题（UGC质量不稳定）

        # 科技媒体（AI工具报道）
        'https://rsshub.app/infoq/topic/AI',  # InfoQ中国（AI技术栏目）
        'https://www.technologyreview.com/feed/',  # MIT Tech Review（AI工具评测）
        'https://arstechnica.com/gadgets/feed/',  # Ars Technica（开发工具）

        # 传统开发资讯
        'https://engineering.fb.com/feed/',  # Meta Engineering
        'https://stackoverflow.com/feeds/tag?tagnames=artificial-intelligence',  # Stack Overflow AI
        'https://www.freecodecamp.org/feed.xml',  # freeCodeCamp
        'https://rsshub.app/qiita/popular',  # Qiita日本

        # ==================== 播客推荐（20个核心源 - 中文优质播客）====================
        # 说明：此分类推荐优质中文播客节目单集，而非播客行业新闻
        # 内容：播客单集更新、嘉宾介绍、节目内容摘要
        # 主题覆盖：科技、商业、历史、人文、心理学、故事叙事
        # 平台来源：小宇宙、Apple Podcast
        # 目标用户：中文播客爱好者，想发现和订阅优质节目

        # 小宇宙精选
        'https://rsshub.app/xiaoyuzhoufm/explore',  # 小宇宙精选播客（算法推荐优质内容）

        # 商业科技类
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff4492c',  # 罗永浩（商业、科技、创业）
        'https://rsshub.app/xiaoyuzhoufm/podcast/624ab95de2f18fa1a1fe5d0e',  # 张小珺商业访谈录
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f950a789fca4eff44930',  # 硅谷101（科技创业）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff4491f',  # 声东击西（商业访谈）
        'https://rsshub.app/xiaoyuzhoufm/podcast/60c2c908f58fc5806da89fcc',  # 疯投圈（投资理财）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6048f6fbe0f8e7a63d54e67a',  # 商业就是这样（商业分析）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44928',  # 科技早知道（科技趋势）

        # 社会观察类
        'https://rsshub.app/xiaoyuzhoufm/podcast/619aea7ef8f6e3ba4e23f9ac',  # 叭叭呜的世界（社会观察）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44933',  # 忽左忽右（文化社会）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44949',  # 随机波动（女性主义）
        'https://rsshub.app/xiaoyuzhoufm/podcast/60791551f9cd9b3b8d7e2964',  # 文化有限（艺术文化）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44946',  # 不合时宜（年轻人生活）

        # 历史人文类
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f94ba789fca4eff4497a',  # 东亚观察局（历史政治）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44948',  # 文化土豆（文化历史）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44943',  # 贝望录（历史人物）

        # 故事叙事类
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44934',  # 故事FM（真实故事）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44938',  # 日谈公园（生活故事）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f94ba789fca4eff4497c',  # 创业内幕（创业故事）
        'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff44947',  # 无聊斋（人物访谈）

        # ==================== 汽车（10个核心源 - 覆盖电动车、燃油车、行业）====================
        'https://rsshub.app/electrive',  # Electrive德国（欧洲电动车行业）
        'https://rsshub.app/autobit',  # 汽车之心（中国自动驾驶与智能汽车）
        'https://rsshub.app/dongchedi/news',  # 懂车帝科技（国产汽车实测）
        'https://rsshub.app/elbil',  # Elbil挪威（最高电动化率国家）
        'https://electrek.co/feed/',  # Electrek（全球电动车新闻）
        'https://cleantechnica.com/feed/',  # CleanTechnica（清洁能源汽车科技）
        'https://insideevs.com/rss/',  # InsideEVs电动车（美国）
        'https://www.greencarreports.com/feed/latest/rss.xml',  # Green Car Reports（美国权威）
        'https://www.caranddriver.com/research/news/rss.xml',  # Car and Driver（主流汽车全类型）
        'https://feeds.bloomberg.com/markets/autos.rss',  # Bloomberg Autos（汽车行业分析）

        # ==================== 投资财经（10个核心源）====================
        'https://rsshub.app/nikkei/index',  # Nikkei日经（亚洲商业最高裁判）
        'https://www.ft.com/rss/home',  # Financial Times（全球金融政策）
        'https://rsshub.app/businesstimes',  # Business Times新加坡（东南亚）
        'https://rsshub.app/caixin/finance',  # 财新网（中国经济政策）
        'https://feeds.bloomberg.com/markets/news.rss',  # Bloomberg Markets
        'https://seekingalpha.com/market_currents.xml',  # Seeking Alpha投资
        'https://www.economist.com/feeds/print-edition.rss',  # The Economist（全球经济）
        'https://www.forbes.com/feed2/?&topic=technology',  # Forbes Tech（创业融资）
        'https://feeds.fortune.com/fortune/latest',  # Fortune（财富500强）
        'https://feeds.marketwatch.com/marketwatch/topstories/',  # MarketWatch（美股实时）

        # ==================== 商业科技（10个核心源）====================
        'https://rsshub.app/heise/news',  # Heise德国（欧洲最严谨IT）
        'https://rsshub.app/36kr/newsflashes',  # 36氪（中国创业融资）
        'https://rsshub.app/techinasia',  # Tech in Asia（东南亚科技）
        'https://techcrunch.com/feed/',  # TechCrunch（美国科技新闻）
        'https://www.theverge.com/rss/index.xml',  # The Verge（科技产品）
        'https://venturebeat.com/feed/',  # VentureBeat（企业科技）
        'https://www.businessinsider.com/tech-feed',  # Business Insider Tech
        'https://feeds.cnbc.com/cnbc/news',  # CNBC Tech（商业科技）
        'https://www.fastcompany.com/feeds/rss',  # Fast Company（商业创新）
        'https://www.mediapost.com/publications/rss/feed.xml?pub=93',  # MediaPost（数字营销）

        # ==================== 政治国际（8个核心源）====================
        'https://rsshub.app/france24/latest',  # France 24（非美视角）
        'https://rsshub.app/channelnewsasia/world',  # CNA新加坡（亚洲地缘）
        'https://rsshub.app/euractiv/news',  # Euractiv（欧盟政策）
        'https://www.aljazeera.com/xml/rss/all.xml',  # Al Jazeera（中东）
        'https://www.theguardian.com/world/rss',  # Guardian World（英国）
        'https://thediplomat.com/rss/',  # The Diplomat（亚太地缘）
        'https://www.foreignaffairs.com/rss.xml',  # Foreign Affairs（国际关系）
        'https://foreignpolicy.com/feed/',  # Foreign Policy（全球政治）

        # ==================== 经济政策（6个核心源）====================
        'https://rsshub.app/imf/news',  # IMF（全球宏观经济）
        'https://rsshub.app/ecb/press',  # ECB欧洲央行（货币政策）
        'https://rsshub.app/miit/news',  # 工信部（中国工业政策）
        'https://www.worldbank.org/en/feeds/rss/all',  # World Bank（发展政策）
        'https://www.oecd.org/rss/all-en.xml',  # OECD（经合组织）
        'https://www.bis.org/about/rss_en.xml',  # BIS（国际清算银行）

        # ==================== 健康医疗（8个核心源）====================
        'https://rsshub.app/thelancet/current',  # The Lancet（顶尖医学）
        'https://rsshub.app/statnews',  # Stat News（制药生物）
        'https://rsshub.app/vcbeat',  # 动脉网（中国医疗投资）
        'https://www.who.int/rss-feeds/news-english.xml',  # WHO（世界卫生组织）
        'https://www.nejm.org/action/showFeed?type=etoc&format=rss',  # NEJM（新英格兰）
        'https://www.bmj.com/rss/current.xml',  # BMJ（英国医学）
        'https://jama.jamanetwork.com/collection.rss?collectionCode=medical&format=rss',  # JAMA
        'https://www.science.org/doi/10.1126/science.rss',  # Science Magazine

        # ==================== 能源环境（6个核心源）====================
        'https://rsshub.app/upstreamonline',  # Upstream挪威（海洋能源）
        'https://rsshub.app/iea/news',  # IEA（国际能源署）
        'https://www.energynewstoday.com/feed/',  # Energy News Today
        'https://www.renewableenergyworld.com/rss/',  # Renewable Energy World
        'https://www.greenbiz.com/rss.xml',  # GreenBiz（绿色商业）
        'https://www.carbon-brief.org/feed',  # Carbon Brief（气候科学）

        # ==================== 娱乐体育（6个核心源）====================
        'https://variety.com/feed/',  # Variety（全球娱乐工业）
        'https://rsshub.app/sportspro',  # SportsPro（体育科技）
        'https://www.hollywoodreporter.com/feed/rss.xml',  # The Hollywood Reporter
        'https://www.billboard.com/feed',  # Billboard（音乐产业）
        'https://www.sportsillustrated.com/feeds/rss/latest.xml',  # Sports Illustrated
        'https://www.espn.com/espn/rss.xml',  # ESPN（体育赛事）

        # ==================== 综合新闻（8个核心源）====================
        'https://feeds.apnews.com/apnews/TopNews',  # Associated Press（美联社）
        'https://feeds.washingtonpost.com/rss/world',  # Washington Post World
        'https://feeds.nytimes.com/services/xml/rss/nyt/HomePage.xml',  # New York Times
        'https://www.bbc.com/news/rss.xml',  # BBC News（英国广播）
        'https://feeds.reuters.com/reuters/businessNews',  # Reuters Business
        'https://feeds.theguardian.com/theguardian/international/rss',  # Guardian International
        'https://www.dw.com/en/latest/rss.xml',  # DW News（德国之声）
        'https://news.ycombinator.com/rss',  # Hacker News（科技热点）

        # ==================== 中国主流媒体（补充源）====================
        'https://rsshub.app/sina/finance',  # 新浪财经
        'https://rsshub.app/thepaper/featured',  # 澎湃新闻
        'https://rsshub.app/zaobao/znews/china',  # 联合早报
        'https://rsshub.app/ifanr/rss',  # 爱范儿科技

        # ==================== 国际顶级媒体（补充源）====================
        'https://feeds.bbci.co.uk/news/rss.xml',  # BBC Top Stories
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC World
        'https://rss.cnn.com/rss/edition.rss',  # CNN Edition
        'https://www.reuters.com/rssFeed/worldNews',  # 路透社世界
        'https://www.reuters.com/rssFeed/technologyNews',  # 路透社科技
        'https://www.wired.com/feed/rss',  # Wired
        'https://www.technologyreview.com/feed/',  # MIT Tech Review
        'https://arstechnica.com/feed/',  # Ars Technica

        # ==================== 日本/欧洲媒体（补充源）====================
        'https://www3.nhk.or.jp/rss/news/cat0.xml',  # NHK日本新闻
        'https://www.lemonde.fr/rss/une.xml',  # 法国世界报
        'https://www.spiegel.de/schlagzeilen/index.rss',  # 德国明镜周刊
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

🎯 核心分类（最高优先级）：

1. ai_technology - AI技术
   关键词：ChatGPT, GPT-4, GPT-5, Claude AI, Gemini, LLaMA, Mistral,
           OpenAI, Anthropic, DeepMind, Google AI, Meta AI,
           大语言模型, LLM, large language model, foundation model,
           机器学习, Machine Learning, 深度学习, Deep Learning,
           神经网络, neural network, 卷积神经网络, CNN, RNN, GAN,
           AI应用, AI模型, AI model, Transformer, attention mechanism,
           提示工程, prompt engineering, 微调, fine-tuning, RAG,
           AI安全, AI safety, AI对齐, alignment, AGI, 通用人工智能,
           人工智能, artificial intelligence, 自然语言处理, NLP,
           计算机视觉, computer vision, 图像识别, image recognition,
           语音识别, speech recognition, 文本生成, text generation
   判断：任何与AI算法、模型、应用相关的纯软件/算法层面内容（不包括AI编程工具）
   排除：如果新闻主题是"AI用于编程"或"AI编程助手"，应归入ai_programming而非此类

2. robotics - 机器人
   关键词：机器人, robot, robots, robotics, 机器人技术,

           # 具身智能与人形机器人
           具身智能, embodied intelligence, embodied AI, physical AI,
           人形机器人, humanoid robot, humanoid, 双足机器人, biped robot,
           Tesla Bot, Optimus, Figure AI, 1X Technologies, Figure 01, Figure 02,
           波士顿动力, Boston Dynamics, Atlas, Spot, Handle,
           优必选, UBTECH, Walker, 小鹏机器人, XPeng Robot,

           # 工业机器人
           工业机器人, industrial robot, 制造机器人, manufacturing robot,
           协作机器人, collaborative robot, cobot, 协作臂,
           机械臂, robotic arm, robot arm, manipulator, 机械手,
           焊接机器人, welding robot, 喷涂机器人, painting robot,
           搬运机器人, material handling robot, 码垛机器人, palletizing robot,
           装配机器人, assembly robot, 拧紧机器人, fastening robot,
           ABB机器人, KUKA, FANUC, Yaskawa, 安川, Universal Robots,
           工业4.0, Industry 4.0, 智能制造, smart manufacturing,

           # 服务机器人
           服务机器人, service robot, 家用机器人, domestic robot,
           扫地机器人, robotic vacuum, sweeping robot, 石头科技, Roborock,
           科沃斯, Ecovacs, iRobot, Roomba, 追觅, Dreame,
           送餐机器人, delivery robot, food delivery robot, 配送机器人,
           接待机器人, reception robot, 迎宾机器人, greeting robot,
           清洁机器人, cleaning robot, 医疗机器人, medical robot,
           手术机器人, surgical robot, da Vinci, 达芬奇手术机器人,
           康复机器人, rehabilitation robot, 护理机器人, care robot,

           # 移动机器人
           移动机器人, mobile robot, 自主移动, autonomous mobile robot, AMR,
           AGV, 自动导引车, automated guided vehicle,
           仓储机器人, warehouse robot, 物流机器人, logistics robot,
           亚马逊机器人, Amazon Robotics, Kiva, 快仓, Quicktron,
           海康机器人, Hikrobot, 极智嘉, Geek+,

           # 无人机
           无人机, drone, UAV, unmanned aerial vehicle, 飞行器,
           四旋翼, quadcopter, 多旋翼, multirotor,
           大疆, DJI, Mavic, Phantom, 亿航, EHang,
           配送无人机, delivery drone, 农业无人机, agricultural drone,

           # 自动驾驶（机器人视角）
           自动驾驶, autonomous driving, self-driving, 无人驾驶,
           自动驾驶汽车, autonomous vehicle, robotaxi, robo-taxi,
           FSD, Full Self-Driving, Autopilot, 自动泊车, auto parking,
           激光雷达, LiDAR, 毫米波雷达, millimeter wave radar,
           传感器融合, sensor fusion, SLAM, 同步定位与建图,
           Waymo, Cruise, 小马智行, Pony.ai, 文远知行, WeRide,

           # 智能座舱与驾驶员监控
           DMS, 驾驶员监控系统, driver monitoring system, 驾驶员监控,
           智能座舱, smart cabin, in-cabin monitoring, 车内监控,
           车内传感器, in-cabin sensor, 生命体征监测, vital signs monitoring,
           疲劳检测, fatigue detection, 分心检测, distraction detection,
           注意力监测, attention monitoring, 生物识别, biometric,
           Smart Eye, Seeing Machines, Affectiva, Mobileye,
           车内摄像头, in-cabin camera, 驾驶员状态, driver state,

           # 技术与组件
           机器人操作系统, ROS, Robot Operating System, ROS2,
           机器视觉, machine vision, computer vision for robotics,
           力控, force control, 力传感器, force sensor,
           抓取, grasping, manipulation, 路径规划, path planning,
           运动控制, motion control, 伺服, servo, 步进电机, stepper motor,
           电机驱动, motor driver, 减速器, reducer, 谐波减速器, harmonic drive,
           末端执行器, end effector, gripper, 夹爪,

           # 公司与研究
           波士顿动力, Boston Dynamics, 新松机器人, Siasun,
           库卡, KUKA, 发那科, FANUC, ABB Robotics,
           MIT CSAIL, CMU Robotics, Stanford Robotics,
           IEEE Robotics, ICRA, IROS, 机器人大会,

   判断：所有类型的机器人（工业/服务/人形/移动/无人机等）及相关技术、公司、应用
   核心特征：涉及物理世界交互、传感器、执行器、控制系统的智能硬件

3. semiconductors - 芯片半导体
   关键词：芯片, 半导体, semiconductor, chip,

           # 芯片制造与代工
           芯片制造, chip manufacturing, wafer, 晶圆, 晶圆厂, fab, foundry,
           台积电, TSMC, 三星, Samsung Foundry, 英特尔, Intel Foundry,
           中芯国际, SMIC, 联电, UMC, 格芯, GlobalFoundries,
           光刻, lithography, EUV, 极紫外光刻, 光刻机, ASML,
           蚀刻, etching, 薄膜沉积, deposition, CMP, 化学机械抛光,
           先进制程, advanced node, 3nm, 5nm, 7nm, 10nm, 14nm,

           # 芯片设计
           芯片设计, chip design, IC设计, integrated circuit,
           EDA, 电子设计自动化, electronic design automation,
           Synopsys, 新思科技, Cadence, 楷登电子, Siemens EDA,
           IP核, IP core, ARM, RISC-V, Arm架构,
           SoC, system on chip, 系统级芯片,
           ASIC, application-specific integrated circuit,
           FPGA, field-programmable gate array,

           # 处理器与GPU
           CPU, 中央处理器, processor, 处理器,
           GPU, 图形处理器, graphics processing unit,
           NVIDIA, 英伟达, AMD, 超威, Intel, 英特尔,
           高通, Qualcomm, 骁龙, Snapdragon, 联发科, MediaTek,
           海思, HiSilicon, 麒麟, Kirin, 展锐, UNISOC,
           苹果芯片, Apple Silicon, M1, M2, M3, A系列芯片,
           AI芯片, AI accelerator, NPU, neural processing unit,
           TPU, tensor processing unit, 昇腾, Ascend,

           # 存储芯片
           存储芯片, memory chip, DRAM, DDR, DDR5,
           闪存, flash memory, NAND, SSD, 固态硬盘,
           三星存储, SK海力士, SK Hynix, 美光, Micron,
           长江存储, YMTC, 长鑫存储, CXMT,

           # 模拟与功率芯片
           模拟芯片, analog chip, 功率芯片, power chip,
           德州仪器, TI, Texas Instruments, ADI, Analog Devices,
           英飞凌, Infineon, 意法半导体, STMicroelectronics,
           电源管理, power management, PMIC,
           功率半导体, power semiconductor, IGBT, GaN, 氮化镓,
           SiC, 碳化硅, silicon carbide,

           # 半导体设备与材料
           半导体设备, semiconductor equipment, 半导体材料,
           ASML, 应用材料, Applied Materials, 科磊, KLA,
           泛林集团, Lam Research, 东京电子, Tokyo Electron,
           硅片, silicon wafer, 光刻胶, photoresist,

           # 产业与市场
           半导体产业, semiconductor industry, 芯片产业链,
           芯片短缺, chip shortage, 芯片法案, CHIPS Act,
           去美化, decoupling, 芯片自主, chip independence,
           先进封装, advanced packaging, chiplet, 小芯片,
           2.5D封装, 3D封装, CoWoS, HBM, high bandwidth memory,

   判断：所有与芯片、半导体相关的新闻，包括设计、制造、设备、材料、市场动态
   核心特征：涉及芯片硬件、制造工艺、半导体产业链

4. ai_programming - AI编程
   关键词：AI编程助手, AI coding, AI代码助手, AI开发工具, AI programming,
           Claude Code, Cursor, GitHub Copilot, Copilot, Copilot Chat,
           Kimi Code, OpenClaw, Windsurf, Aider, Cody, Sourcegraph Cody,
           Replit AI, Ghostwriter, Tabnine, Codeium, Amazon CodeWhisperer,
           AI Agent, Code Agent, Coding Agent, 代码助手, coding assistant,
           智能编程, intelligent coding, AI代码生成, code generation,
           AI辅助编程, AI-assisted programming, pair programming,
           代码补全, code completion, autocomplete, IntelliSense,
           代码审查, code review, 代码分析, code analysis,
           自动化编程, automated coding, 代码优化, code optimization,
           编程, programming, 代码, code, coding, developer,
           GitHub, GitLab, 开源, open source, repository,
           Python, JavaScript, Rust, Go, TypeScript, Java, C++,
           React, Vue, Angular, Node.js, Django, Flask,
           VSCode, Visual Studio Code, IDE, JetBrains, WebStorm,
           编辑器, editor, compiler, 编译器, debugger, 调试器,
           API, SDK, framework, 框架, library, 库,
           开发工具, developer tools, dev tools,
           版本控制, version control, Git, CI/CD, DevOps,
           package, npm, pip, Maven, Gradle,
           软件开发, software development, 编程语言, programming language,
           代码编辑器, code editor, 集成开发环境
   判断：AI编程工具、代码助手、传统开发工具、开源项目、编程社区、软件开发相关内容

5. opcg - OPCG卡牌游戏
   关键词：OPCG, One Piece Card Game, 海贼王卡牌, OP TCG, OP卡牌,
           One Piece TCG, ワンピースカードゲーム,

           # 游戏机制与环境
           卡组, deck, Meta, 环境, 上位卡组, top deck,
           禁限表, Ban List, Restricted, Banned, Errata, 规则更新,
           锦标赛, tournament, championship, 旗舰赛, 比赛, 赛事,
           胜率, win rate, 对局, match, 复盘, deck building,

           # 卡片相关
           单卡, 卡面, card reveal, 新卡, 卡包, booster pack,
           异画, alternate art, AA卡, 平行卡, parallel,
           编号卡, 稀有度, rarity, SR, SEC, L卡, leader card,
           角色卡, character card, 事件卡, event card,
           场地卡, stage card, 船长卡, crew,

           # 市场与价格
           价格, price, 行情, market, 交易, trade,
           TCGPlayer, Cardmarket, Yu-Yu-Tei, 单卡价格,
           投资, collection, 收藏, 保值, value,

           # 官方与品牌
           万代, Bandai, 官方, official, 发售, release,
           中文版, 日版, 英文版, 亚洲版,
           onepiece-cardgame.com, onepiece-cardgame.cn,

           # 数据库与工具
           One Piece Top Decks, Ohara TCG, OP TCG Dex,
           OneCollector, 卡组数据库, deck database,

           # 玩家与社区
           Reddit OnePieceTCG, Wossy Plays, The Egman, VvTheory,
           玩家, player, 玩法, strategy, 攻略, guide,
           开箱, unboxing, 抽卡, pull, box break,

           # 相关角色和内容（需结合卡牌关键词）
           路飞, Luffy, 索隆, Zoro, 娜美, Nami,
           香吉士, Sanji, 乔巴, Chopper, 罗宾, Robin,
           布鲁克, Brook, 佛朗基, Franky, 乌索普, Usopp,
           艾斯, Ace, 白胡子, Whitebeard, 黑胡子, Blackbeard,
           凯多, Kaido, 大妈, Big Mom, 红发, Shanks,

   判断：所有与One Piece Card Game相关的内容，包括官方公告、赛事、卡片发售、价格行情、玩法攻略
   核心特征：必须同时包含"海贼王/One Piece"和"卡牌/TCG/Card Game"相关词汇
   排除：单纯的海贼王动漫/漫画新闻（无卡牌元素） → one_piece

6. consumer_electronics - 消费电子
   关键词：消费电子, consumer electronics, 电子产品,

           # 智能眼镜与AR/VR
           智能眼镜, smart glasses, AR眼镜, augmented reality glasses,
           VR眼镜, virtual reality headset, VR头显, MR眼镜, mixed reality,
           Meta Quest, Vision Pro, 苹果Vision Pro, Apple Vision Pro,
           雷鸟, Rokid, XREAL, Nreal, Meta Ray-Ban,
           Google Glass, HoloLens, Magic Leap,

           # 手机与平板
           手机, smartphone, 智能手机, mobile phone, phone,
           iPhone, 苹果手机, 三星手机, Samsung Galaxy,
           小米手机, Xiaomi, 华为手机, Huawei, OPPO, vivo,
           一加, OnePlus, realme, 荣耀, Honor, Nothing Phone,
           平板, tablet, iPad, 安卓平板, Android tablet,
           折叠屏, foldable, 翻盖手机, flip phone,
           屏幕, display, OLED, AMOLED, 高刷, 120Hz,
           手机芯片, 手机处理器, 骁龙, 天玑, Dimensity,
           手机摄像头, camera, 影像, 长焦, 微距,

           # 智能手表与可穿戴
           智能手表, smartwatch, 智能穿戴, wearable,
           Apple Watch, 苹果手表, Galaxy Watch, 华为手表,
           小米手环, Xiaomi Band, Fitbit, Garmin,
           运动手表, sports watch, 健康监测, health monitoring,
           心率监测, heart rate, 血氧, SpO2, ECG, 心电图,

           # 耳机与音频
           耳机, headphones, earphones, earbuds, TWS,
           AirPods, 苹果耳机, 降噪耳机, noise cancelling,
           Sony耳机, Bose, Sennheiser, 森海塞尔,
           小米耳机, 华为耳机, OPPO耳机, Nothing Ear,
           骨传导, bone conduction, 开放式耳机,
           蓝牙音箱, Bluetooth speaker, 智能音箱, smart speaker,

           # 充电宝与电源
           充电宝, power bank, 移动电源, portable charger,
           快充, fast charging, 无线充电, wireless charging,
           氮化镓, GaN charger, 充电器, charger, 充电头,
           Anker, 小米充电宝, 紫米, ZMI,

           # 相机与摄影
           相机, camera, 数码相机, digital camera,
           微单, mirrorless, 单反, DSLR,
           索尼相机, Sony Alpha, 佳能, Canon, 尼康, Nikon,
           富士, Fujifilm, 松下, Panasonic, 徕卡, Leica,
           镜头, lens, 传感器, sensor, 全画幅, full frame,
           运动相机, action camera, 云台, gimbal,

           # 无人机
           无人机, drone, 航拍, aerial photography,
           大疆, DJI, Mavic, Mini, Air, FPV,
           穿越机, FPV drone, 亿航, EHang,

           # 电子产品配件
           保护壳, case, 贴膜, screen protector,
           支架, stand, 数据线, cable, Type-C,
           移动硬盘, external drive, U盘, USB drive,
           键盘, keyboard, 鼠标, mouse, 触控板, trackpad,

   判断：所有消费类电子产品，包括手机、手表、眼镜、相机、无人机、充电宝、耳机等
   核心特征：面向个人消费者的电子设备和配件
   排除：芯片制造本身 → semiconductors

7. one_piece - ONE PIECE动漫周边
   关键词：海贼王, One Piece, ワンピース, ONE PIECE, OP,

           # 动漫内容
           动画, anime, 漫画, manga, 集英社, Shueisha,
           尾田荣一郎, Eiichiro Oda, 尾田, Oda,
           章节, chapter, 话数, episode, 剧情, story,
           新篇章, new arc, 新剧情, 和之国, Wano,
           最终章, final saga, 剧场版, movie, film,
           东映, Toei Animation, Netflix,

           # 角色与内容（非卡牌）
           路飞, Luffy, 草帽团, Straw Hat Pirates,
           索隆, Zoro, 娜美, Nami, 山治, Sanji,
           乔巴, Chopper, 罗宾, Robin, 弗兰奇, Franky,
           布鲁克, Brook, 乌索普, Usopp, 甚平, Jinbe,
           四皇, Yonko, 七武海, Shichibukai,
           海军, Marines, 世界政府, World Government,
           恶魔果实, Devil Fruit, 霸气, Haki,

           # 周边产品
           手办, figure, 模型, model, 玩具, toy,
           万代, Bandai, 景品, prize figure,
           Figure, Figuarts, Pop, Funko Pop,
           盲盒, blind box, 扭蛋, gashapon,
           海报, poster, 画集, artbook,
           服装, clothing, T恤, t-shirt, 卫衣, hoodie,
           包包, bag, 背包, backpack, 钱包, wallet,
           抱枕, pillow, 挂件, keychain, 徽章, badge,
           杯子, mug, cup, 水杯, bottle,

           # 商品与发售
           预售, pre-order, 发售, release, 上架, launch,
           限定, limited edition, 独家, exclusive,
           价格, price, 代购, resale, 转卖,
           周边店, merchandise store, 官方商店, official store,
           淘宝, taobao, 闲鱼, xianyu, 京东, JD,

           # 活动与社区
           展会, exhibition, 漫展, comic con, 活动, event,
           联动, collaboration, 联名, co-branded,
           cosplay, 同人, doujin, 二创, fan art,
           Reddit OnePiece, B站, Bilibili, 海贼王吧,

           # 游戏（非卡牌）
           海贼王游戏, One Piece game, 航海王,
           手游, mobile game, Steam游戏,
           PS游戏, PlayStation, 格斗游戏, fighting game,

   判断：所有与ONE PIECE相关的内容（除了OPCG卡牌游戏），包括动画、漫画、周边、手办、服装、活动、游戏
   核心特征：海贼王IP相关的任何非卡牌内容
   排除：One Piece Card Game相关 → opcg

8. podcasts - 播客推荐（节目内容推荐）
   关键词：播客, podcast, 音频节目, audio show,

           # 播客平台
           小宇宙, 小宇宙FM, xiaoyuzhou, xyzFM,
           Apple Podcasts, iTunes Podcasts, Spotify Podcasts,
           喜马拉雅, Himalaya, 荔枝FM, lizhi, 蜻蜓FM,
           网易云音乐, NetEase Music, QQ音乐播客,

           # 中文热门播客
           罗永浩, 罗翔, 老罗, Luo Yonghao,
           叭叭呜, 叭叭呜的世界,
           张小珺, 商业访谈录, 商业就是这样,
           硅谷101, 硅谷早知道, 声动活泼,
           随机波动, 不合时宜, 忽左忽右,
           文化土豆, 东亚观察局, 贝望录,
           创业内幕, 疯投圈, 科技早知道,

           # 英文热门播客
           Lex Fridman, Lex Fridman Podcast,
           Joe Rogan, Joe Rogan Experience, JRE,
           Tim Ferriss, The Tim Ferriss Show,
           a16z Podcast, Andreessen Horowitz,
           The Vergecast, Verge播客,
           This Week in Tech, TWiT,
           Acquired, acquired.fm,
           All-In Podcast, 硅谷四人帮,
           My First Million, MFM,
           The Changelog, changelog.com,

           # AI相关播客
           TWIML, This Week in Machine Learning,
           Practical AI, AI播客,
           AI Breakdown, AI解析,
           The Robot Brains, 机器人大脑,
           The AI Podcast, NVIDIA AI播客,

           # 汽车科技播客
           Ride the Lightning, 特斯拉播客,
           InsideEVs Podcast, 电动车播客,
           Autoline, 汽车产业播客,
           The Smoking Tire, 汽车测评,

           # 播客内容类型
           访谈, interview, 对话, conversation,
           深度讨论, deep dive, 分析, analysis,
           新闻解读, news breakdown, 商业分析,
           创业故事, startup story, 创始人访谈,
           技术讨论, tech discussion, 行业洞察,
           脱口秀, talk show, 闲聊, casual chat,

           # 播客相关词汇
           播客主持人, podcast host, podcaster,
           嘉宾, guest, 单集, episode, 系列, series,
           音频, audio, 订阅, subscribe, 收听, listen,
           播客节目, podcast show, 播客更新, new episode,

   判断：优质播客节目推荐，包括播客单集更新、嘉宾介绍、节目内容
   核心特征：音频节目形式的内容推荐（非播客行业新闻）
   说明：此分类展示播客节目本身的内容，而非播客行业动态
   排除：纯音乐、广播电台（非播客形式） → entertainment_sports

📌 其他分类：
- automotive: 汽车（电动车/燃油车/混动车, Tesla, 比亚迪, 丰田, 奔驰, 宝马, 充电桩, 电池技术, 新车发布, 汽车销量, 汽车行业 - 不含自动驾驶AI技术本身）
- finance_investment: 投资财经（股票, 加密货币, Bitcoin, 投资, 金融市场）
- business_tech: 商业科技（科技公司, startup, 融资, IPO, 商业新闻）
- politics_world: 政治国际（国际关系, 政府, 选举, 外交）
- economy_policy: 经济政策（GDP, 通胀, 经济政策, 贸易战）
- health_medical: 健康医疗（医疗, 健康, 疾病, 药品, 疫苗）
- energy_environment: 能源环境（能源, 气候变化, 环保, 可再生能源）
- entertainment_sports: 娱乐体育（体育赛事, 电影, 音乐, 明星）
- general: 综合（无法明确分类的其他新闻）

⚠️ 分类规则：
1. 优先匹配核心分类（ai_technology, robotics, ai_programming, semiconductors, opcg, consumer_electronics, one_piece, podcasts）
2. AI类新闻判断标准（重要：按以下顺序匹配）：
   a) **AI编程工具优先规则**：
      - 如果新闻提到Claude Code、Cursor、Copilot等AI编程助手 → ai_programming
      - 如果新闻主题是"AI用于编程"、"AI代码生成" → ai_programming
      - 如果新闻涉及GitHub、VSCode、IDE的AI功能 → ai_programming
   b) 纯AI算法/模型/理论（不涉及编程工具） → ai_technology
   c) AI在物理世界（机器人/硬件/传感器） → robotics
   d) 自动驾驶系统（包含感知/决策/控制） → robotics
   e) DMS/智能座舱/驾驶员监控系统 → robotics
   f) Tesla/汽车的自动驾驶技术 → robotics
   g) Tesla/汽车的电池/续航/销量/新车发布 → automotive
3. 汽车类新闻判断标准：
   - 电动车/燃油车/混动车的产品、销量、评测 → automotive
   - 充电桩、电池技术、续航 → automotive
   - 汽车行业动态、车企财报、新车发布 → automotive
   - 自动驾驶技术本身（非车辆产品） → robotics
4. OPCG卡牌判断标准：
   - 必须同时包含"海贼王/One Piece"和"卡牌/TCG/Card"相关词汇
   - 单纯的海贼王动漫/漫画新闻（无卡牌元素） → one_piece
5. ONE PIECE动漫判断标准：
   - 海贼王相关的动画、漫画、周边、手办、服装、活动、游戏（非卡牌） → one_piece
   - 如果同时涉及卡牌游戏 → opcg
6. 消费电子判断标准：
   - 手机、平板、手表、眼镜、耳机、相机、无人机、充电宝等个人电子产品 → consumer_electronics
   - 芯片制造、半导体产业链 → semiconductors
   - 智能汽车产品本身 → automotive
7. 芯片分类判断标准：
   - 芯片设计、制造、设备、材料、产业链 → semiconductors
   - 芯片应用在消费电子产品中（如手机芯片评测） → consumer_electronics
8. 编程相关内容（包括AI编程助手和传统开发）必须归入ai_programming
9. 如果新闻同时涉及AI和编程，优先选择ai_programming而非ai_technology
10. 只返回分类代码，不要解释

新闻标题: {title}
新闻摘要: {summary}

请返回最合适的分类代码："""

# 合并提示词（一次性完成摘要+分类，节省50% Token）
COMBINED_PROMPT = """分析新闻，生成中文摘要并分类。

新闻标题: {title}
新闻内容: {content}

输出JSON格式:
{{
  "title": "简洁的中文标题（30字内）",
  "summary": "事件概述：...\\n\\n重要细节：\\n• 细节1\\n• 细节2\\n• 细节3\\n\\n后续影响：...",
  "category": "分类代码"
}}

分类必须从以下选择:
ai_technology(AI技术), robotics(机器人), ai_programming(AI编程),
semiconductors(芯片), opcg(OPCG卡牌), automotive(汽车),
consumer_electronics(消费电子), one_piece(海贼王), podcasts(播客),
finance_investment(投资), business_tech(商业), politics_world(政治),
economy_policy(经济), health_medical(健康), energy_environment(能源),
entertainment_sports(娱乐), general(综合)

规则:
- 标题翻译成中文，保留专有名词
- 摘要50-150字，结构化三段式
- 根据关键词精确分类
- AI编程工具→ai_programming，不是ai_technology
- 机器人相关→robotics
- 只返回JSON，不要其他内容
"""
