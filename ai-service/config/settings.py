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
