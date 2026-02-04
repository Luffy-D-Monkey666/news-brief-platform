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
    'ai_programming',        # AI编程（原coding_development）
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
    'ai_programming': 'AI编程',
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

        # ==================== 具身智能（8个核心源）====================
        'https://rsshub.app/irobotnews',  # Robot News韩国（三星/现代机器人）
        'https://rsshub.app/robotstart',  # Robot Start日本（全球机器人密度最高国）
        'https://robohub.org/feed/',  # Robohub瑞士（顶尖学术背景物理AI）
        'https://rsshub.app/sps-magazin',  # SPS德国（工业4.0核心资讯）
        'https://www.ieee.org/about/news/rss.xml',  # IEEE官方新闻（机器人标准）
        'https://csail.mit.edu/news/rss.xml',  # MIT CSAIL（具身AI研究前沿）
        'https://www.cs.cmu.edu/news/rss.xml',  # CMU计算机（机器人与AI研究）
        'https://ai.stanford.edu/news/rss.xml',  # Stanford AI Lab（人形机器人）

        # ==================== Coding开发（15个核心源 - 重点覆盖AI编程工具）====================
        # AI编程工具官方源
        'https://github.blog/feed/',  # GitHub官方博客（Copilot更新）
        'https://code.visualstudio.com/feed.xml',  # VSCode官方（Copilot集成）
        'https://cursor.sh/blog/rss.xml',  # Cursor官方博客（如果有RSS）

        # 开发者社区（AI编程讨论热点）
        'https://rsshub.app/hackernews/best',  # Hacker News（AI工具讨论）
        'https://dev.to/feed',  # Dev.to（AI编程教程）
        'https://rsshub.app/reddit/topic/artificial',  # Reddit AI话题
        'https://rsshub.app/reddit/topic/programming',  # Reddit编程话题

        # 科技媒体（AI工具报道）
        'https://rsshub.app/infoq/topic/AI',  # InfoQ中国（AI技术栏目）
        'https://www.technologyreview.com/feed/',  # MIT Tech Review（AI工具评测）
        'https://arstechnica.com/gadgets/feed/',  # Ars Technica（开发工具）

        # 传统开发资讯
        'https://engineering.fb.com/feed/',  # Meta Engineering
        'https://stackoverflow.com/feeds/tag?tagnames=artificial-intelligence',  # Stack Overflow AI
        'https://www.freecodecamp.org/feed.xml',  # freeCodeCamp
        'https://rsshub.app/qiita/popular',  # Qiita日本

        # ==================== 新能源汽车（10个核心源）====================
        'https://rsshub.app/electrive',  # Electrive德国（欧洲电动车行业）
        'https://rsshub.app/autobit',  # 汽车之心（中国自动驾驶）
        'https://rsshub.app/dongchedi/news',  # 懂车帝科技（国产EV实测）
        'https://rsshub.app/elbil',  # Elbil挪威（最高电动化率国家）
        'https://electrek.co/feed/',  # Electrek（全球电动车新闻）
        'https://cleantechnica.com/feed/',  # CleanTechnica（清洁能源科技）
        'https://insideevs.com/rss/',  # InsideEVs电动车（美国）
        'https://www.greencarreports.com/feed/latest/rss.xml',  # Green Car Reports（美国权威）
        'https://www.caranddriver.com/research/news/rss.xml',  # Car and Driver（主流汽车）
        'https://feeds.bloomberg.com/markets/autos.rss',  # Bloomberg Autos（行业分析）

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

2. embodied_intelligence - 具身智能
   关键词：机器人, robot, 人形机器人, humanoid, 波士顿动力, Boston Dynamics,
           Tesla Bot, Optimus, Figure AI, 1X Technologies,
           自动驾驶, autonomous driving, FSD, 激光雷达, LiDAR,
           工业机器人, 服务机器人, 无人机, drone, 物理AI, embodied AI,
           机械臂, 传感器融合, sensor fusion, SLAM
   判断：AI在物理世界的应用，涉及硬件、传感器、执行器的智能系统

3. ai_programming - AI编程
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
1. 优先匹配核心分类（ai_technology, embodied_intelligence, ai_programming）
2. AI类新闻判断标准（重要：按以下顺序匹配）：
   a) **AI编程工具优先规则**：
      - 如果新闻提到Claude Code、Cursor、Copilot等AI编程助手 → ai_programming
      - 如果新闻主题是"AI用于编程"、"AI代码生成" → ai_programming
      - 如果新闻涉及GitHub、VSCode、IDE的AI功能 → ai_programming
   b) 纯AI算法/模型/理论（不涉及编程工具） → ai_technology
   c) AI在物理世界（机器人/硬件/传感器） → embodied_intelligence
   d) 自动驾驶系统（包含感知/决策/控制） → embodied_intelligence
   e) Tesla/电动车的自动驾驶功能 → embodied_intelligence
   f) Tesla/电动车的电池/续航/销量 → ev_automotive
3. 编程相关内容（包括AI编程助手和传统开发）必须归入ai_programming
4. 如果新闻同时涉及AI和编程，优先选择ai_programming而非ai_technology
5. 只返回分类代码，不要解释

新闻标题: {title}
新闻摘要: {summary}

请返回最合适的分类代码："""
