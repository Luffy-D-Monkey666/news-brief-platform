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
    # 核心关注领域（最高优先级）
    'ai_technology',         # AI技术
    'embodied_intelligence', # 具身智能
    'coding_development',    # Coding开发
    'ev_automotive',         # 新能源汽车
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
    'embodied_intelligence': '具身智能',
    'coding_development': 'Coding',
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

# 新闻源配置（全球专业信源，70+新闻源）
NEWS_SOURCES = {
    'rss_feeds': [
        # ==================== AI技术（6个核心源）====================
        'https://rsshub.app/jiqizhixin/ai',  # 机器之心（中国最深度AI论文解读）
        'https://rsshub.app/qbitai',  # 量子位（AI产业动态与大模型落地）
        'https://rsshub.app/mistral/news',  # Mistral AI（欧洲最强开源模型）
        'https://rsshub.app/thenextweb/ai',  # TNW（欧洲AI监管与创新生态）
        'https://rsshub.app/ledge/news',  # Ledge.ai（日本AI商业应用）
        'https://rsshub.app/arxiv/cs.AI',  # arXiv AI论文（趋势预测）

        # ==================== 具身智能（4个核心源）====================
        'https://rsshub.app/irobotnews',  # Robot News韩国（三星/现代机器人）
        'https://rsshub.app/robotstart',  # Robot Start日本（全球机器人密度最高国）
        'https://robohub.org/feed/',  # Robohub瑞士（顶尖学术背景物理AI）
        'https://rsshub.app/sps-magazin',  # SPS德国（工业4.0核心资讯）

        # ==================== Coding开发（3个核心源）====================
        'https://rsshub.app/infoq/topic/AI',  # InfoQ中国（架构师技术演进）
        'https://rsshub.app/hackernews/best',  # Hacker News（全球开发者社区）
        'https://rsshub.app/qiita/popular',  # Qiita日本（日本技术分享社区）

        # ==================== 新能源汽车（7个核心源）====================
        'https://rsshub.app/electrive',  # Electrive德国（欧洲电动车行业）
        'https://rsshub.app/autobit',  # 汽车之心（中国自动驾驶与智能座舱）
        'https://rsshub.app/dongchedi/news',  # 懂车帝科技（国产EV实测数据）
        'https://rsshub.app/elbil',  # Elbil挪威（全球最高电动化率国家）
        'https://electrek.co/feed/',  # Electrek（全球电动车新闻）
        'https://cleantechnica.com/feed/',  # CleanTechnica（清洁能源科技）
        'https://insideevs.com/rss/',  # InsideEVs电动车（美国）

        # ==================== 投资财经（6个核心源）====================
        'https://rsshub.app/nikkei/index',  # Nikkei日经（亚洲商业最高裁判）
        'https://www.ft.com/rss/home',  # Financial Times（全球金融政策权威）
        'https://rsshub.app/businesstimes',  # Business Times新加坡（东南亚金融）
        'https://rsshub.app/caixin/finance',  # 财新网（中国经济政策深度）
        'https://feeds.bloomberg.com/markets/news.rss',  # Bloomberg Markets
        'https://seekingalpha.com/market_currents.xml',  # Seeking Alpha投资分析

        # ==================== 商业科技（6个核心源）====================
        'https://rsshub.app/heise/news',  # Heise德国（欧洲最严谨IT分析）
        'https://rsshub.app/36kr/newsflashes',  # 36氪（中国创业融资动态）
        'https://rsshub.app/techinasia',  # Tech in Asia（东南亚科技商业）
        'https://techcrunch.com/feed/',  # TechCrunch（美国科技新闻）
        'https://www.theverge.com/rss/index.xml',  # The Verge（科技产品评测）
        'https://venturebeat.com/feed/',  # VentureBeat（企业科技）

        # ==================== 政治国际（5个核心源）====================
        'https://rsshub.app/france24/latest',  # France 24（非美视角地缘政治）
        'https://rsshub.app/channelnewsasia/world',  # CNA新加坡（亚洲地缘政治）
        'https://rsshub.app/euractiv/news',  # Euractiv（欧盟政策与AI法案）
        'https://www.aljazeera.com/xml/rss/all.xml',  # Al Jazeera（中东视角）
        'https://www.theguardian.com/world/rss',  # Guardian World（英国）

        # ==================== 经济政策（3个核心源）====================
        'https://rsshub.app/imf/news',  # IMF国际货币基金（全球宏观经济）
        'https://rsshub.app/ecb/press',  # ECB欧洲央行（欧洲货币政策）
        'https://rsshub.app/miit/news',  # 工信部（中国工业政策）

        # ==================== 健康医疗（4个核心源）====================
        'https://rsshub.app/thelancet/current',  # The Lancet（顶尖医学期刊）
        'https://rsshub.app/statnews',  # Stat News（制药生物技术）
        'https://rsshub.app/vcbeat',  # 动脉网（中国医疗健康投融资）
        'https://www.who.int/rss-feeds/news-english.xml',  # WHO世界卫生组织

        # ==================== 能源环境（2个核心源）====================
        'https://rsshub.app/upstreamonline',  # Upstream挪威（海洋能源转型）
        'https://rsshub.app/iea/news',  # IEA国际能源署（全球能源平衡）

        # ==================== 娱乐体育（2个核心源）====================
        'https://variety.com/feed/',  # Variety（全球娱乐工业）
        'https://rsshub.app/sportspro',  # SportsPro（体育科技与版权）

        # ==================== 中国主流媒体（4个补充源）====================
        'https://rsshub.app/sina/finance',  # 新浪财经
        'https://rsshub.app/thepaper/featured',  # 澎湃新闻
        'https://rsshub.app/zaobao/znews/china',  # 联合早报
        'https://rsshub.app/ifanr/rss',  # 爱范儿科技

        # ==================== 国际主流媒体（8个补充源）====================
        'https://feeds.bbci.co.uk/news/rss.xml',  # BBC Top Stories
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC World
        'https://rss.cnn.com/rss/edition.rss',  # CNN Edition
        'https://www.reuters.com/rssFeed/worldNews',  # 路透社世界
        'https://www.reuters.com/rssFeed/technologyNews',  # 路透社科技
        'https://www.wired.com/feed/rss',  # Wired
        'https://www.technologyreview.com/feed/',  # MIT Tech Review
        'https://arstechnica.com/feed/',  # Ars Technica

        # ==================== 日本媒体（1个补充源）====================
        'https://www3.nhk.or.jp/rss/news/cat0.xml',  # NHK日本主要新闻

        # ==================== 欧洲媒体（2个补充源）====================
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
   关键词：ChatGPT, GPT-4, Claude, OpenAI, Anthropic, DeepMind, 大语言模型, LLM,
           机器学习, Machine Learning, 深度学习, Deep Learning, 神经网络,
           AI应用, AI模型, Transformer, 提示工程, prompt engineering,
           AI安全, AI对齐, AGI, 人工智能, artificial intelligence
   判断：任何与AI算法、模型、应用相关的纯软件/算法层面内容

2. embodied_intelligence - 具身智能
   关键词：机器人, robot, 人形机器人, humanoid, 波士顿动力, Boston Dynamics,
           Tesla Bot, Optimus, Figure AI, 1X Technologies,
           自动驾驶, autonomous driving, FSD, 激光雷达, LiDAR,
           工业机器人, 服务机器人, 无人机, drone, 物理AI, embodied AI,
           机械臂, 传感器融合, sensor fusion, SLAM
   判断：AI在物理世界的应用，涉及硬件、传感器、执行器的智能系统

3. coding_development - Coding开发
   关键词：编程, programming, 代码, code, GitHub, GitLab, 开源, open source,
           Python, JavaScript, Rust, Go, TypeScript, React, Vue, Node.js,
           VSCode, IDE, 编辑器, compiler, 编译器, API, SDK,
           开发工具, developer tools, 版本控制, CI/CD, DevOps,
           框架, framework, 库, library, package, npm, pip,
           算法竞赛, LeetCode, 编程语言, programming language
   判断：编程语言、开发工具、开源项目、编程社区相关内容

📌 其他分类：
- ev_automotive: 新能源汽车（Tesla车辆, 比亚迪, 电动车, 充电桩, 电池技术 - 不含自动驾驶AI）
- finance_investment: 投资财经（股票, 加密货币, Bitcoin, 投资, 金融市场）
- business_tech: 商业科技（科技公司, startup, 融资, IPO, 商业新闻）
- politics_world: 政治国际（国际关系, 政府, 选举, 外交）
- economy_policy: 经济政策（GDP, 通胀, 经济政策, 贸易战）
- health_medical: 健康医疗（医疗, 健康, 疾病, 药品, 疫苗）
- energy_environment: 能源环境（能源, 气候变化, 环保, 可再生能源）
- entertainment_sports: 娱乐体育（体育赛事, 电影, 音乐, 明星）
- general: 综合（无法明确分类的其他新闻）

⚠️ 分类规则：
1. 优先匹配核心分类（ai_technology, embodied_intelligence, coding_development）
2. AI类新闻判断标准：
   - 纯算法/模型/软件应用 → ai_technology
   - 涉及机器人/物理世界/硬件 → embodied_intelligence
   - 自动驾驶系统（包含感知/决策/控制） → embodied_intelligence
   - Tesla/电动车的自动驾驶功能 → embodied_intelligence
   - Tesla/电动车的电池/续航/销量 → ev_automotive
3. 编程相关内容必须归入coding_development
4. 如果无法确定，优先选择更具体的分类
5. 只返回分类代码，不要解释

新闻标题: {title}
新闻摘要: {summary}

请返回最合适的分类代码："""
