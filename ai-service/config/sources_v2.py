"""
新闻源配置 V2 - 全面升级信息源体系

核心改进：
1. 增加 X (Twitter) 社交媒体源
2. 增加微信公众号、知乎等中文源
3. 优化源质量，移除低价值RSS
4. 分类更精准，减少噪音
5. VIP账号机制：指定账号内容100%保留
"""

# ====================================
# VIP Twitter/X 账号（用户关注的重要账号，内容100%保留不过滤）
# ====================================
# 这些账号的所有内容都会进入简报，包括RT转推、短内容等
TWITTER_VIP_ACCOUNTS = {
    # === 海贼王官方账号 ===
    'mugistore_info',           # ONE PIECE 麦わらストア公式
    'op_kfpj',                  # ONE PIECE熊本復興プロジェクト
    'OPMerchandise',            # One Piece Merch News
    'OPcom_info',               # ONE PIECE.com
    'onepiece_mag',             # ワンピース・マガジン
    'Eiichiro_Staff',           # ONE PIECE スタッフ【公式】
    'OP_base_shop',             # 【公式】ONE PIECE BASE SHOP
    
    # === OPCG卡牌游戏官方 ===
    'ONEPIECE_tcg_EN',          # Official One Piece Card Game English
    'official_BCG_JP',          # 【OFFICIAL】BANDAI CARD GAMES
    'ONEPIECETcgSHOP',          # ONE PIECEカードゲーム 公式ショップ
    'ONEPIECE_tcg',             # 【公式】ONE PIECEカードゲーム
    
    # === 龙珠官方 ===
    '1kUJIdragonball',          # 一番くじ『ドラゴンボール』公式
    'dbfw_cgSTORE',             # ドラゴンボールスーパーカードゲーム
    'DB_official_jp',           # ドラゴンボールオフィシャル
    'DB_STORE_info',            # DRAGON BALL STORE TOKYO
    
    # === 其他卡牌/动漫 ===
    '1kuji_onepiece',           # 一番くじ海賊団
    'PokemonTCG',               # Pokémon TCG
    
    # === 网红/创作者 ===
    'sichuanc',                 # Pickle
    'ishowspeedsui',            # Speed
    'MrBeast',                  # MrBeast
    'LoganPaul',                # Logan Paul
    
    # === 汽车/科技 ===
    'electric_nick',            # Electric Nick
    'autogefuehl',              # Autogefühl
    
    # === 新闻媒体 ===
    'asahi_shinsen',            # 朝日新闻中文频道
    'kyodo_chinese',            # Kyodo News Chinese 日本共同社
    'bbcchinese',               # BBC News 中文
    'nytchinese',               # 纽约时报中文网
    'wangzhian8848',            # 王志安
    
    # === 音乐/娱乐 ===
    'Eminem',                   # Marshall Mathers
}

def is_twitter_vip(username: str) -> bool:
    """检查是否为VIP Twitter账号（内容100%保留）"""
    return username.lower() in {acc.lower() for acc in TWITTER_VIP_ACCOUNTS}

# ====================================
# 1. X (Twitter) 信息源
# ====================================
# 使用 RSSHub 的 Twitter 路由（免费）
# 格式: https://rsshub.app/twitter/user/{用户名}

TWITTER_SOURCES = {
    'ai_technology': [
        # AI 官方账号
        'https://rsshub.app/twitter/user/OpenAI',           # OpenAI 官方
        'https://rsshub.app/twitter/user/DeepMind',         # DeepMind 官方
        'https://rsshub.app/twitter/user/Anthropic',        # Anthropic (Claude)
        'https://rsshub.app/twitter/user/MistralAI',        # Mistral AI
        'https://rsshub.app/twitter/user/AIatMeta',         # Meta AI
        'https://rsshub.app/twitter/user/GoogleAI',         # Google AI
        'https://rsshub.app/twitter/user/MSFTResearch',     # Microsoft Research
        'https://rsshub.app/twitter/user/huggingface',      # Hugging Face
        
        # AI 大佬与研究者
        'https://rsshub.app/twitter/user/ylecun',           # Yann LeCun (Meta AI Chief)
        'https://rsshub.app/twitter/user/AndrewYNg',        # 吴恩达
        'https://rsshub.app/twitter/user/karpathy',         # Andrej Karpathy
        'https://rsshub.app/twitter/user/goodfellow_ian',   # Ian Goodfellow
        'https://rsshub.app/twitter/user/jeremyphoward',    # Jeremy Howard (fast.ai)
        'https://rsshub.app/twitter/user/hardmaru',         # 知名AI博主
        'https://rsshub.app/twitter/user/nathanbenaich',    # AI投资者
        'https://rsshub.app/twitter/user/lilianweng',       # Lilian Weng (OpenAI)
        'https://rsshub.app/twitter/user/petefw',           # Pete Warden (Google)
        'https://rsshub.app/twitter/user/DrJimFan',         # Jim Fan (NVIDIA)
        'https://rsshub.app/twitter/user/omarsar0',         # Elvis (Hugging Face)
        
        # AI 公司/产品
        'https://rsshub.app/twitter/user/weights_biases',   # Weights & Biases
        'https://rsshub.app/twitter/user/runwayml',         # Runway ML
        'https://rsshub.app/twitter/user/StabilityAI',      # Stability AI
        'https://rsshub.app/twitter/user/Midjourney',       # Midjourney
        'https://rsshub.app/twitter/user/perplexity_ai',    # Perplexity AI
    ],
    'robotics': [
        # 机器人官方账号
        'https://rsshub.app/twitter/user/BostonDynamics',   # 波士顿动力
        'https://rsshub.app/twitter/user/Tesla_Optimus',    # Tesla Bot
        'https://rsshub.app/twitter/user/1x_tech',          # 1X Technologies
        'https://rsshub.app/twitter/user/Figure_robot',     # Figure AI
        'https://rsshub.app/twitter/user/AgilityRobotics',  # Agility Robotics
        'https://rsshub.app/twitter/user/UnitreeRobotics',  # Unitree (宇树科技)
        'https://rsshub.app/twitter/user/UBTECHRobotics',   # 优必选
        'https://rsshub.app/twitter/user/DexterityAI',      # Dexterity AI
        'https://rsshub.app/twitter/user/SanctuaryAI',      # Sanctuary AI
        'https://rsshub.app/twitter/user/Apptronik',        # Apptronik
        'https://rsshub.app/twitter/user/aimotive',         # AImotive (自动驾驶)
        
        # 机器人研究者
        'https://rsshub.app/twitter/user/rodneybrooks',     # Rodney Brooks (MIT)
        'https://rsshub.app/twitter/user/PeterAbbeel',      # Peter Abbeel (UC Berkeley)
    ],
    'semiconductors': [
        # NVIDIA 生态（黄仁勋重点扩展）
        'https://rsshub.app/twitter/user/nvidia',           # NVIDIA
        'https://rsshub.app/twitter/user/NVIDIAAI',         # NVIDIA AI
        'https://rsshub.app/twitter/user/NVIDIADGX',        # NVIDIA DGX
        'https://rsshub.app/twitter/user/NVIDIAGame',       # NVIDIA GeForce
        'https://rsshub.app/twitter/user/NVIDIAHPC',        # NVIDIA HPC
        'https://rsshub.app/twitter/user/nvidiadeveloper',  # NVIDIA Developer
        'https://rsshub.app/twitter/user/NVIDIAGTC',        # NVIDIA GTC大会
        'https://rsshub.app/twitter/user/nvidiacorp',       # NVIDIA Corp
        'https://rsshub.app/twitter/user/NVIDIAGaming',     # NVIDIA Gaming
        'https://rsshub.app/twitter/user/NVIDIAAStudio',    # NVIDIA Studio
        'https://rsshub.app/twitter/user/NVIDIARobotics',   # NVIDIA Robotics
        'https://rsshub.app/twitter/user/NVIDIAOmniverse',  # NVIDIA Omniverse
        'https://rsshub.app/twitter/user/NVIDIADrive',      # NVIDIA Drive (自动驾驶)
        'https://rsshub.app/twitter/user/NVIDIAJetson',     # NVIDIA Jetson (边缘AI)
        'https://rsshub.app/twitter/user/NVIDIACN',         # NVIDIA 中国
        
        # 黄仁勋相关
        'https://rsshub.app/twitter/user/jensenhuangnvidia', # Jensen Huang (黄仁勋)
        
        # 其他芯片公司
        'https://rsshub.app/twitter/user/AMD',              # AMD
        'https://rsshub.app/twitter/user/Intel',            # Intel
        'https://rsshub.app/twitter/user/ARMCommunity',     # ARM
        'https://rsshub.app/twitter/user/Qualcomm',         # 高通
        'https://rsshub.app/twitter/user/SamsungSemiUS',    # 三星半导体
        'https://rsshub.app/twitter/user/TSMC',             # 台积电
        'https://rsshub.app/twitter/user/ASMLcompany',      # ASML
        'https://rsshub.app/twitter/user/MicronTech',       # 美光
        'https://rsshub.app/twitter/user/Broadcom',         # 博通
        'https://rsshub.app/twitter/user/MarvellTech',      # Marvell
        'https://rsshub.app/twitter/user/cerebras',         # Cerebras
        'https://rsshub.app/twitter/user/GroqInc',          # Groq (AI芯片)
        'https://rsshub.app/twitter/user/SambanovaSys',     # SambaNova
        'https://rsshub.app/twitter/user/GraphcoreAI',      # Graphcore
        'https://rsshub.app/twitter/user/tenstorrent',      # Tenstorrent (Jim Keller)
        'https://rsshub.app/twitter/user/Real_Hyun',        # Hyun (Tenstorrent)
        'https://rsshub.app/twitter/user/01Light_AI',       # 01.AI (零一万物，李开复)
        'https://rsshub.app/twitter/user/karpathy',         # Andrej Karpathy (前Tesla AI，现回归OpenAI)
        
        # 芯片分析师/媒体
        'https://rsshub.app/twitter/user/anandshimpi',      # Anand Shimpi
        'https://rsshub.app/twitter/user/IanCutress',       # Ian Cutress
        'https://rsshub.app/twitter/user/mooresislaw',      # Moore's Law Is Dead
        'https://rsshub.app/twitter/user/akibamark',        # Akiba Mark
        'https://rsshub.app/twitter/user/TechTechPotat',    # TechTechPotato (Ian Cutress)
        'https://rsshub.app/twitter/user/semianalysis',     # SemiAnalysis (芯片分析)
    ],
    'automotive': [
        # 特斯拉/Tesla 生态（重点扩展）
        'https://rsshub.app/twitter/user/Tesla',            # Tesla 官方
        'https://rsshub.app/twitter/user/elonmusk',         # Elon Musk
        'https://rsshub.app/twitter/user/Tesla_AI',         # Tesla AI (FSD/机器人)
        'https://rsshub.app/twitter/user/Tesla_Optimus',    # Tesla Optimus 机器人
        'https://rsshub.app/twitter/user/Tesla_Megapack',   # Tesla 能源
        'https://rsshub.app/twitter/user/ashleevance',      # Ashlee Vance (马斯克传记作者)
        'https://rsshub.app/twitter/user/TeslaPodcast',     # Tesla Podcast
        
        # 马斯克其他公司
        'https://rsshub.app/twitter/user/SpaceX',           # SpaceX
        'https://rsshub.app/twitter/user/Neuralink',        # Neuralink
        'https://rsshub.app/twitter/user/xai',              # xAI (Grok)
        'https://rsshub.app/twitter/user/TheBoringCompany', # Boring Company
        'https://rsshub.app/twitter/user/Hyperloop',        # Hyperloop
        'https://rsshub.app/twitter/user/Starlink',         # Starlink
        
        # 特斯拉媒体/分析师
        'https://rsshub.app/twitter/user/ElectrekCo',       # Electrek (Fred Lambert)
        'https://rsshub.app/twitter/user/FredericLambert',  # Fred Lambert (Electrek创始人)
        'https://rsshub.app/twitter/user/InsideEVs',        # InsideEVs
        'https://rsshub.app/twitter/user/SawyerMerritt',    # Sawyer Merritt (Tesla消息)
        'https://rsshub.app/twitter/user/WholeMarsBlog',    # Whole Mars Catalog (Omar)
        'https://rsshub.app/twitter/user/dima_zeniuk',      # Dima Zeniuk (科技爆料)
        'https://rsshub.app/twitter/user/teslaownersSV',    # Tesla Owners Silicon Valley
        'https://rsshub.app/twitter/user/TroyTeslike',      # Troy Teslike (Tesla数据分析)
        'https://rsshub.app/twitter/user/ray4tesla',        # Ray (Tesla视频博主)
        'https://rsshub.app/twitter/user/klwtts',           # Kelvin (Tesla分析师)
        'https://rsshub.app/twitter/user/EstherCrawford',   # Esther Crawford (前Twitter/Tesla)
        
        # 其他汽车公司
        'https://rsshub.app/twitter/user/Rivian',           # Rivian
        'https://rsshub.app/twitter/user/lucidmotors',      # Lucid Motors
        'https://rsshub.app/twitter/user/NIOGlobal',        # NIO 蔚来
        'https://rsshub.app/twitter/user/XPEV_Motors',      # 小鹏汽车
        'https://rsshub.app/twitter/user/LiAuto',           # 理想汽车
        'https://rsshub.app/twitter/user/BYDCompany',       # 比亚迪
        'https://rsshub.app/twitter/user/CatlBattery',      # 宁德时代
        'https://rsshub.app/twitter/user/Ford',             # 福特
        'https://rsshub.app/twitter/user/GM',               # 通用汽车
        'https://rsshub.app/twitter/user/VolvoCarUSA',      # 沃尔沃
        'https://rsshub.app/twitter/user/MercedesBenz',     # 奔驰
        'https://rsshub.app/twitter/user/BMW',              # 宝马
        'https://rsshub.app/twitter/user/Volkswagen',       # 大众
        'https://rsshub.app/twitter/user/Toyota',           # 丰田
        'https://rsshub.app/twitter/user/Honda',            # 本田
        
        # 汽车评测
        'https://rsshub.app/twitter/user/autogefuehl',      # Autogefühl 汽车评测
        'https://rsshub.app/twitter/user/electric_nick',    # Electric Nick (电动车)
    ],
    'consumer_electronics': [
        # 科技媒体
        'https://rsshub.app/twitter/user/verge',            # The Verge
        'https://rsshub.app/twitter/user/engadget',         # Engadget
        'https://rsshub.app/twitter/user/wired',            # Wired
        'https://rsshub.app/twitter/user/arstechnica',      # Ars Technica
        'https://rsshub.app/twitter/user/Gizmodo',          # Gizmodo
        'https://rsshub.app/twitter/user/CNET',             # CNET
        'https://rsshub.app/twitter/user/androidcentral',   # Android Central
        'https://rsshub.app/twitter/user/9to5mac',          # 9to5Mac
        'https://rsshub.app/twitter/user/9to5Google',       # 9to5Google
        'https://rsshub.app/twitter/user/DigitalTrends',    # Digital Trends
        
        # 科技博主
        'https://rsshub.app/twitter/user/MKBHD',            # Marques Brownlee
        'https://rsshub.app/twitter/user/UniverseIce',      # Ice Universe (三星爆料)
        'https://rsshub.app/twitter/user/markgurman',       # Mark Gurman (苹果爆料)
        'https://rsshub.app/twitter/user/jon_prosser',      # Jon Prosser (Front Page Tech)
        
        # 公司官方
        'https://rsshub.app/twitter/user/Apple',            # Apple
        'https://rsshub.app/twitter/user/SamsungMobile',    # 三星移动
        'https://rsshub.app/twitter/user/Google',           # Google
        'https://rsshub.app/twitter/user/Microsoft',        # Microsoft
        'https://rsshub.app/twitter/user/Android',          # Android
        'https://rsshub.app/twitter/user/OnePlus_USA',      # 一加
        'https://rsshub.app/twitter/user/Xiaomi',           # 小米
        'https://rsshub.app/twitter/user/Huawei',           # 华为
        'https://rsshub.app/twitter/user/oppo',             # OPPO
        'https://rsshub.app/twitter/user/vivo_global',      # vivo
    ],
    'business_tech': [
        # 科技媒体
        'https://rsshub.app/twitter/user/TechCrunch',       # TechCrunch
        'https://rsshub.app/twitter/user/BloombergTech',    # Bloomberg Tech
        'https://rsshub.app/twitter/user/recode',           # Recode
        'https://rsshub.app/twitter/user/axios',            # Axios
        'https://rsshub.app/twitter/user/PoliticoTech',     # Politico Tech
        'https://rsshub.app/twitter/user/FTTech',           # Financial Times Tech
        
        # 风投/创业
        'https://rsshub.app/twitter/user/a16z',             # Andreessen Horowitz
        'https://rsshub.app/twitter/user/sequoia',          # Sequoia Capital
        'https://rsshub.app/twitter/user/ycombinator',      # Y Combinator
        'https://rsshub.app/twitter/user/paulg',            # Paul Graham
        'https://rsshub.app/twitter/user/sama',             # Sam Altman
        'https://rsshub.app/twitter/user/jason',            # Jason Calacanis
        'https://rsshub.app/twitter/user/eladgil',          # Elad Gil
        'https://rsshub.app/twitter/user/fredwilson',       # Fred Wilson
        
        # 科技公司 CEO/高管
        'https://rsshub.app/twitter/user/satyanadella',     # Satya Nadella (Microsoft)
        'https://rsshub.app/twitter/user/tim_cook',         # Tim Cook (Apple)
        'https://rsshub.app/twitter/user/sundarpichai',     # Sundar Pichai (Google)
        'https://rsshub.app/twitter/user/jack',             # Jack Dorsey
    ],
    'finance_investment': [
        # 财经媒体
        'https://rsshub.app/twitter/user/Bloomberg',        # Bloomberg
        'https://rsshub.app/twitter/user/FinancialTimes',   # Financial Times
        'https://rsshub.app/twitter/user/Reuters',          # Reuters
        'https://rsshub.app/twitter/user/WallStreetJourn',  # WSJ
        'https://rsshub.app/twitter/user/CNBC',             # CNBC
        'https://rsshub.app/twitter/user/markets',          # Markets Insider
        'https://rsshub.app/twitter/user/zerohedge',        # Zero Hedge
        
        # 投资者/分析师
        'https://rsshub.app/twitter/user/RampCapitalLLC',   # Ramp Capital
        'https://rsshub.app/twitter/user/ycharts',          # YCharts
        'https://rsshub.app/twitter/user/Stocktwits',       # Stocktwits
        'https://rsshub.app/twitter/user/charliebilello',   # Charlie Bilello
        'https://rsshub.app/twitter/user/lhamtil',          # Lawrence Hamtil
        'https://rsshub.app/twitter/user/michaelbatnick',   # Michael Batnick
        'https://rsshub.app/twitter/user/downtownjbrown',   # Downtown Josh Brown
    ],
    'politics_world': [
        # 国际媒体
        'https://rsshub.app/twitter/user/BBCWorld',         # BBC World
        'https://rsshub.app/twitter/user/cnn',              # CNN
        'https://rsshub.app/twitter/user/ReutersWorld',     # Reuters World
        'https://rsshub.app/twitter/user/AFP',              # AFP
        'https://rsshub.app/twitter/user/dw_chinese',       # 德国之声中文
        'https://rsshub.app/twitter/user/RFA_Chinese',      # RFA 自由亚洲电台
        # 中文新闻媒体 (图片)
        'https://rsshub.app/twitter/user/asahi_shinsen',    # 朝日新闻中文频道
        'https://rsshub.app/twitter/user/kyodo_chinese',    # 共同社中文
        'https://rsshub.app/twitter/user/bbcchinese',       # BBC News 中文
        'https://rsshub.app/twitter/user/ChineseWSJ',       # 华尔街日报中文
        'https://rsshub.app/twitter/user/nytchinese',       # 纽约时报中文网
        'https://rsshub.app/twitter/user/wangzhian8848',    # 王志安
    ],
    'opcg': [
        # OPCG 官方与社区
        'https://rsshub.app/twitter/user/OnePieceCardGame', # OPCG 官方
        'https://rsshub.app/twitter/user/OnePieceUS',       # OPCG US
        'https://rsshub.app/twitter/user/BandaiNamcoUS',    # Bandai Namco
        'https://rsshub.app/twitter/user/ONEPIECE_tcg_EN',  # OPCG English (图片)
        'https://rsshub.app/twitter/user/official_BCG_JP',  # BANDAI CARD GAMES (图片)
        'https://rsshub.app/twitter/user/ONEPIECEtcgSHOP',  # OPCG Shop (图片)
        'https://rsshub.app/twitter/user/OP_BASE_tcg',      # ONE PIECE BASE (图片)
        'https://rsshub.app/twitter/user/PokemonTCG',       # Pokemon TCG (图片)
    ],
    'one_piece': [
        # 海贼王官方
        'https://rsshub.app/twitter/user/OnePieceAnime',    # 海贼王动画官方
        'https://rsshub.app/twitter/user/ToeiAnimation',    # 东映动画
        'https://rsshub.app/twitter/user/Eiichiro_Staff',   # 尾田荣一郎官方
        # 海贼王商店/周边 (图片)
        'https://rsshub.app/twitter/user/mugistore_info',   # ONE PIECE麦わらストア公式
        'https://rsshub.app/twitter/user/op_kfpj',          # ONE PIECE熊本復興プロジェクト
        'https://rsshub.app/twitter/user/OPMerchandise',    # One Piece Merch News
        'https://rsshub.app/twitter/user/OPcom_info',       # ONE PIECE.com
        'https://rsshub.app/twitter/user/onepiece_mag',     # ワンピース・マガジン
        # 一番くじ (图片)
        'https://rsshub.app/twitter/user/1kuji_dragonball', # 一番くじドラゴンボール
        'https://rsshub.app/twitter/user/1kuji_onepiece',   # 一番くじ海賊団
        # 龙珠 (图片)
        'https://rsshub.app/twitter/user/dbfw_cgSTORE',     # ドラゴンボールスーパーカードゲーム
        'https://rsshub.app/twitter/user/DB_official_jp',   # ドラゴンボールオフィシャル
    ],
    
    'entertainment_sports': [
        # 网红/创作者 (图片)
        'https://rsshub.app/twitter/user/MrBeast',          # MrBeast
        'https://rsshub.app/twitter/user/LoganPaul',        # Logan Paul
        'https://rsshub.app/twitter/user/ishowspeedsui',    # Speed (IShowSpeed)
        # 音乐/艺人 (图片)
        'https://rsshub.app/twitter/user/Eminem',           # Eminem (Marshall Mathers)
    ],
    
    'anime_otaku': [
        # 日本动漫官方/制作公司
        'https://rsshub.app/twitter/user/ToeiAnimation',    # 东映动画（龙珠、海贼王）
        'https://rsshub.app/twitter/user/MAPPA_Info',       # MAPPA（咒术回战、电锯人）
        'https://rsshub.app/twitter/user/ufotable',         # ufotable（鬼灭之刃、Fate）
        'https://rsshub.app/twitter/user/WIT_STUDIO',       # WIT STUDIO（进击的巨人、间谍过家家）
        'https://rsshub.app/twitter/user/CloverWorks',      # CloverWorks（更衣人偶、孤独摇滚）
        'https://rsshub.app/twitter/user/A_1Pictures',      # A-1 Pictures（刀剑神域、辉夜）
        'https://rsshub.app/twitter/user/bones_anime',      # BONES（文豪野犬、我的英雄学院）
        'https://rsshub.app/twitter/user/Trigger_TG',       # TRIGGER（赛博朋克、小魔女学园）
        'https://rsshub.app/twitter/user/KyotoAnimation',   # 京都动画（紫罗兰、声之形）
        'https://rsshub.app/twitter/user/ProductionIG',     # Production I.G（攻壳机动队）
        'https://rsshub.app/twitter/user/ScienceSARU',      # Science SARU（四畳半、犬王）
        
        # 日本动漫资讯/媒体
        'https://rsshub.app/twitter/user/AnimeNewsNet',     # Anime News Network
        'https://rsshub.app/twitter/user/Crunchyroll',      # Crunchyroll
        'https://rsshub.app/twitter/user/FUNimation',       # Funimation
        'https://rsshub.app/twitter/user/hulu_japan',       # Hulu Japan
        'https://rsshub.app/twitter/user/netflixjp_anime',  # Netflix Japan Anime
        
        # 日本漫画家/创作者
        'https://rsshub.app/twitter/user/Eiichiro_Staff',   # 尾田荣一郎官方（海贼王）
        'https://rsshub.app/twitter/user/horikoshiko',      # 堀越耕平（我的英雄学院）
        'https://rsshub.app/twitter/user/gegeakutami',      # 芥见下下（咒术回战）
        'https://rsshub.app/twitter/user/nagatoro_kuro',    # ナナシ（长瀞同学）
        
        # 欧洲动漫（法国、英国、德国）
        'https://rsshub.app/twitter/user/FolivariStudio',   # Folivari（法国，艾特熊和赛娜鼠）
        'https://rsshub.app/twitter/user/XilamAnimation',   # Xilam（法国，肥猫大战三小强）
        'https://rsshub.app/twitter/user/dargaudmedia',     # Dargaud Media（法国，高卢英雄）
        'https://rsshub.app/twitter/user/Aardman',          # Aardman（英国，小羊肖恩）
        'https://rsshub.app/twitter/user/studioaka',        # Studio AKA（英国，嗨！道奇）
        'https://rsshub.app/twitter/user/BlueZooAnims',     # Blue-Zoo（英国）
        'https://rsshub.app/twitter/user/StudioFilmBilder', # Studio Film Bilder（德国）
        'https://rsshub.app/twitter/user/MotionWorks_GmbH', # MotionWorks（德国）
        
        # 国际动漫展/活动
        'https://rsshub.app/twitter/user/animenyc',         # Anime NYC
        'https://rsshub.app/twitter/user/AnimeExpo',        # Anime Expo
        'https://rsshub.app/twitter/user/japan_anime',      # Japan Anime
    ],
}

# ====================================
# 2. 中文本土信息源（微信公众号/微博）
# ====================================

CHINA_SOURCES = {
    'wechat_official': [
        # ===== 科技/互联网大厂 =====
        'https://rsshub.app/wechat/mp/抖音集团',             # 抖音技术团队
        'https://rsshub.app/wechat/mp/阿里巴巴',             # 阿里巴巴官方
        'https://rsshub.app/wechat/mp/腾讯科技',             # 腾讯科技
        'https://rsshub.app/wechat/mp/百度AI',               # 百度AI
        'https://rsshub.app/wechat/mp/华为开发者',           # 华为开发者
        'https://rsshub.app/wechat/mp/京东技术',             # 京东技术
        'https://rsshub.app/wechat/mp/美团技术团队',         # 美团技术团队
        'https://rsshub.app/wechat/mp/字节跳动技术团队',     # 字节跳动技术团队
        
        # ===== AI/大模型 =====
        'https://rsshub.app/wechat/mp/机器之心',             # 机器之心（AI媒体）
        'https://rsshub.app/wechat/mp/量子位',               # 量子位（AI媒体）
        'https://rsshub.app/wechat/mp/新智元',               # 新智元（AI媒体）
        'https://rsshub.app/wechat/mp/AI科技评论',           # AI科技评论
        'https://rsshub.app/wechat/mp/智东西',               # 智东西
        'https://rsshub.app/wechat/mp/大数据文摘',           # 大数据文摘
        'https://rsshub.app/wechat/mp/InfoQ',                # InfoQ中国
        
        # ===== 投资/财经 =====
        'https://rsshub.app/wechat/mp/36氪',                 # 36氪
        'https://rsshub.app/wechat/mp/虎嗅APP',              # 虎嗅
        'https://rsshub.app/wechat/mp/晚点LatePost',         # 晚点LatePost
        'https://rsshub.app/wechat/mp/投资界',               # 投资界
        'https://rsshub.app/wechat/mp/投中网',               # 投中网
        'https://rsshub.app/wechat/mp/动脉网',               # 动脉网（医疗投资）
        
        # ===== 汽车/新能源 =====
        'https://rsshub.app/wechat/mp/电动汽车观察家',       # 电动汽车观察家
        'https://rsshub.app/wechat/mp/42号车库',             # 42号车库
        'https://rsshub.app/wechat/mp/汽车之心',             # 汽车之心
        'https://rsshub.app/wechat/mp/高工智能汽车',         # 高工智能汽车
        
        # ===== 半导体/硬科技 =====
        'https://rsshub.app/wechat/mp/芯智讯',               # 芯智讯
        'https://rsshub.app/wechat/mp/半导体行业观察',       # 半导体行业观察
        'https://rsshub.app/wechat/mp/芯东西',               # 芯东西
        
        # ===== 创业/商业 =====
        'https://rsshub.app/wechat/mp/创业邦',               # 创业邦
        'https://rsshub.app/wechat/mp/字母榜',               # 字母榜
        'https://rsshub.app/wechat/mp/晚点',                 # 晚点
        
        # ===== 深度/评论 =====
        'https://rsshub.app/wechat/mp/知识分子',             # 知识分子
        'https://rsshub.app/wechat/mp/第一财经',             # 第一财经
        'https://rsshub.app/wechat/mp/财新网',               # 财新网
        'https://rsshub.app/wechat/mp/澎湃新闻',             # 澎湃新闻
    ],
    
    'weibo': [
        # ===== 科技/互联网大佬 =====
        'https://rsshub.app/weibo/user/1111681197',          # 雷军（小米创始人）
        'https://rsshub.app/weibo/user/1750070171',          # 周鸿祎（360创始人）
        'https://rsshub.app/weibo/user/1494759802',          # 罗永浩
        'https://rsshub.app/weibo/user/1892653243',          # 王兴（美团创始人）
        'https://rsshub.app/weibo/user/1650111241',          # 张一鸣（字节跳动，如公开）
        'https://rsshub.app/weibo/user/1659809157',          # 李想（理想汽车）
        'https://rsshub.app/weibo/user/1632078473',          # 何小鹏（小鹏汽车）
        'https://rsshub.app/weibo/user/1656801620',          # 李斌（蔚来汽车）
        
        # ===== AI/科技大V =====
        'https://rsshub.app/weibo/user/1402400261',          # 李开复（创新工场）
        'https://rsshub.app/weibo/user/1288915263',          # 王思聪
        'https://rsshub.app/weibo/user/1195242865',          # 霍金（官方账号）
        'https://rsshub.app/weibo/user/1566936885',          # 薛兆丰
        
        # ===== 财经/投资大V =====
        'https://rsshub.app/weibo/user/1364707591',          # 但斌（投资人）
        'https://rsshub.app/weibo/user/1318599007',          # 李大霄
        'https://rsshub.app/weibo/user/1737878851',          # 洪灝（交银国际）
        'https://rsshub.app/weibo/user/1239883480',          # 叶檀（财经评论家）
        
        # ===== 汽车/评测大V =====
        'https://rsshub.app/weibo/user/1651428902',          # 韩路（汽车之家创始人）
        'https://rsshub.app/weibo/user/1641523987',          # 陈震（萝卜报告）
        'https://rsshub.app/weibo/user/1700648435',          # 闫闯
        
        # ===== 媒体/机构 =====
        'https://rsshub.app/weibo/user/1618051664',          # 人民日报
        'https://rsshub.app/weibo/user/1974576991',          # 新华社
        'https://rsshub.app/weibo/user/1634489957',          # 央视财经
        'https://rsshub.app/weibo/user/1644114654',          # 中国新闻周刊
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
    
    'anime_otaku': [
        # 日本动漫评论/分析
        'https://rsshub.app/youtube/channel/UCpuT8AlP9P9EgW_pZ0_xInQ',  # Gigguk (Anime YouTuber)
        'https://rsshub.app/youtube/channel/UCAz5YVPud6U3a8r4tLdRmcQ',  # The Anime Man
        'https://rsshub.app/youtube/channel/UC0Yp3P8T_t8rvVj0E3bBq1A',  # Mother's Basement
        'https://rsshub.app/youtube/channel/UC0mqX9fGFjGkHKGrNbH0omw',  # Super Eyepatch Wolf
        'https://rsshub.app/youtube/channel/UCB7hFdJhT5q8J7n5z8g2rXQ',  # Under The Scope
        'https://rsshub.app/youtube/channel/UCzRJl9x3_h3l_h5Y9-Z7r2A',  # AnimeEveryday
        'https://rsshub.app/youtube/channel/UCnJ8P7gNXHYSM8Vr7p8v3eQ',  # Canipa Effect (日本动画产业)
        
        # 欧洲动漫
        'https://rsshub.app/youtube/channel/UC8fF3q1qF5z2F1xP3v7f9dA',  # Toniko Pantoja (欧洲动画师)
        'https://rsshub.app/youtube/channel/UCYIQ2P8hL4QeC3XwC7e6Dqg',  # Frame by Frame (动画分析)
        
        # 动漫新闻/资讯
        'https://rsshub.app/youtube/channel/UCy5L3QpCIYgQwj9_NP9Z4TQ',  # Crunchyroll Collection
        'https://rsshub.app/youtube/channel/UC6-1kwiMfB4qw47LM4qC7wQ',  # Funimation
    ],
    'ai_coding_agent': [  # AI编码与智能体（原ai_programming）
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
    
    'ai_coding_agent': [  # AI编码与智能体
        # AI编码工具
        'https://github.blog/feed/',            # GitHub 官方博客
        'https://code.visualstudio.com/feed.xml',  # VSCode 官方
        'https://engineering.fb.com/feed/',     # Meta Engineering
        
        # AI Agent 公司/项目
        'https://rsshub.app/twitter/user/AutoGPT',           # AutoGPT
        'https://rsshub.app/twitter/user/CrewAIInc',         # CrewAI
        'https://rsshub.app/twitter/user/LangChainAI',       # LangChain
        'https://rsshub.app/twitter/user/llama_index',       # LlamaIndex
        'https://rsshub.app/twitter/user/pinecone',          # Pinecone
        'https://rsshub.app/twitter/user/vectara',           # Vectara
        'https://rsshub.app/twitter/user/Weaviate_io',       # Weaviate
        'https://rsshub.app/twitter/user/chromadb',          # Chroma
        'https://rsshub.app/twitter/user/unitycatalog',      # Unity Catalog
        
        # AI Agent 开发者/研究者
        'https://rsshub.app/twitter/user/hwchase17',         # Harrison Chase (LangChain创始人)
        'https://rsshub.app/twitter/user/jerryjliu0',        # Jerry Liu (LlamaIndex创始人)
        'https://rsshub.app/twitter/user/yoheinakajima',     # Yohei Nakajima (BabyAGI)
        'https://rsshub.app/twitter/user/bindureddy',        # Bindu Reddy (Abacus AI)
        'https://rsshub.app/twitter/user/alexalbert__',      # Alex Albert (Cursor)
        'https://rsshub.app/twitter/user/amanrs',            # Aman Sanger (Cursor)
    ],
    
    'semiconductors': [
        'https://www.eetimes.com/feed/',
        'https://semiengineering.com/feed/',
        'https://www.anandtech.com/rss/',
        'https://www.tomshardware.com/rss.xml',
    ],
    
    'opcg': [
        # 日本官方
        'https://one-piece-cardgame.com/news/rss.xml',  # 日版官网
    ],
    
    'anime_otaku': [
        # 动漫新闻
        'https://www.animenewsnetwork.com/all/rss.xml',      # Anime News Network (英文)
        'https://rsshub.app/crunchyroll/news',               # Crunchyroll News
        'https://rsshub.app/funimation/news',                # Funimation News
        'https://rsshub.app/myanimelist/news',               # MyAnimeList News
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
        'https://www.animenewsnetwork.com/all/rss.xml',  # 动漫新闻网
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
    'weibo': [],
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
NEWS_SOURCES_V2['weibo'] = CHINA_SOURCES['weibo']

# 合并 YouTube 源
for category, urls in YOUTUBE_SOURCES.items():
    NEWS_SOURCES_V2['youtube'].extend(urls)

# 统计
TOTAL_SOURCES = (
    len(NEWS_SOURCES_V2['rss_feeds']) +
    len(NEWS_SOURCES_V2['twitter']) +
    len(NEWS_SOURCES_V2['wechat']) +
    len(NEWS_SOURCES_V2['weibo']) +
    len(NEWS_SOURCES_V2['youtube'])
)

print(f"新闻源 V2 统计:")
print(f"  - RSS 源: {len(NEWS_SOURCES_V2['rss_feeds'])} 个")
print(f"  - Twitter/X 源: {len(NEWS_SOURCES_V2['twitter'])} 个")
print(f"  - 微信公众号: {len(NEWS_SOURCES_V2['wechat'])} 个")
print(f"  - 微博大V: {len(NEWS_SOURCES_V2['weibo'])} 个")
print(f"  - YouTube 频道: {len(NEWS_SOURCES_V2['youtube'])} 个")
print(f"  - 总计: {TOTAL_SOURCES} 个")
