"""
股票数据服务 - 使用 yfinance 库
获取上市公司的市值、PE、当日涨跌等数据
"""
import logging
from typing import Dict, Optional
import re
import time
from threading import Lock
from functools import lru_cache

logger = logging.getLogger(__name__)

# 限流配置
RATE_LIMIT_CALLS = 5  # 每个时间窗口最多请求数
RATE_LIMIT_WINDOW = 60  # 时间窗口（秒）
REQUEST_INTERVAL = 1.5  # 每次请求最小间隔（秒）

# 缓存配置
CACHE_TTL = 300  # 股票数据缓存时间（秒）

# 尝试导入 yfinance
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logger.warning("yfinance 未安装，股票功能将不可用。请运行: pip install yfinance")

# 常见公司名称到股票代码的映射
COMPANY_TICKER_MAP = {
    # 美股 - 科技巨头
    'openai': None,  # 未上市
    'anthropic': None,  # 未上市
    'apple': 'AAPL',
    '苹果': 'AAPL',
    'microsoft': 'MSFT',
    '微软': 'MSFT',
    'google': 'GOOGL',
    'alphabet': 'GOOGL',
    '谷歌': 'GOOGL',
    'amazon': 'AMZN',
    '亚马逊': 'AMZN',
    'meta': 'META',
    'facebook': 'META',
    'nvidia': 'NVDA',
    '英伟达': 'NVDA',
    'tesla': 'TSLA',
    '特斯拉': 'TSLA',
    'amd': 'AMD',
    'intel': 'INTC',
    '英特尔': 'INTC',
    'qualcomm': 'QCOM',
    '高通': 'QCOM',
    'broadcom': 'AVGO',
    '博通': 'AVGO',
    
    # 美股 - 其他
    'netflix': 'NFLX',
    'disney': 'DIS',
    '迪士尼': 'DIS',
    'uber': 'UBER',
    'airbnb': 'ABNB',
    'salesforce': 'CRM',
    'oracle': 'ORCL',
    '甲骨文': 'ORCL',
    'ibm': 'IBM',
    'cisco': 'CSCO',
    '思科': 'CSCO',
    
    # 美股 - 汽车
    'ford': 'F',
    '福特': 'F',
    'gm': 'GM',
    '通用汽车': 'GM',
    'general motors': 'GM',
    'stellantis': 'STLA',
    '斯特兰蒂斯': 'STLA',
    'rivian': 'RIVN',
    'lucid': 'LCID',
    'toyota': 'TM',
    '丰田': 'TM',
    'honda': 'HMC',
    '本田': 'HMC',
    'volkswagen': 'VWAGY',
    '大众': 'VWAGY',
    'bmw': 'BMWYY',
    '宝马': 'BMWYY',
    'mercedes': 'MBGYY',
    '奔驰': 'MBGYY',
    
    # 港股 (需要 .HK 后缀)
    '腾讯': '0700.HK',
    'tencent': '0700.HK',
    '阿里巴巴': '9988.HK',
    'alibaba': 'BABA',  # 美股ADR
    '小米': '1810.HK',
    'xiaomi': '1810.HK',
    '美团': '3690.HK',
    'meituan': '3690.HK',
    '京东': 'JD',  # 美股
    'jd': 'JD',
    '百度': 'BIDU',  # 美股
    'baidu': 'BIDU',
    '网易': 'NTES',
    'netease': 'NTES',
    '比亚迪': '1211.HK',
    'byd': '1211.HK',
    '蔚来': 'NIO',
    'nio': 'NIO',
    '理想': 'LI',
    'li auto': 'LI',
    '小鹏': 'XPEV',
    'xpeng': 'XPEV',
    
    # A股 (需要 .SS 或 .SZ 后缀)
    '京东方': '000725.SZ',
    'boe': '000725.SZ',
    '立讯精密': '002475.SZ',
    '舜宇光学': '2382.HK',
    '宁德时代': '300750.SZ',
    'catl': '300750.SZ',
    '隆基绿能': '601012.SS',
    '贵州茅台': '600519.SS',
    '中芯国际': '0981.HK',
    'smic': '0981.HK',
}


class StockService:
    """股票数据服务 - 使用 yfinance，带限流和缓存"""
    
    def __init__(self):
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance 不可用，股票服务初始化失败")
        
        # 限流控制
        self._last_request_time = 0
        self._request_lock = Lock()
        self._request_count = 0
        self._window_start = time.time()
        
        # 内存缓存 {ticker: (data, timestamp)}
        self._cache: Dict[str, tuple] = {}
        
        # 失败标记（避免重复请求失败的股票）
        self._failed_tickers: Dict[str, float] = {}
        self._fail_cooldown = 300  # 失败后冷却时间（秒）
    
    def _wait_for_rate_limit(self):
        """等待限流"""
        with self._request_lock:
            now = time.time()
            
            # 重置时间窗口
            if now - self._window_start > RATE_LIMIT_WINDOW:
                self._window_start = now
                self._request_count = 0
            
            # 检查是否超过限制
            if self._request_count >= RATE_LIMIT_CALLS:
                wait_time = RATE_LIMIT_WINDOW - (now - self._window_start)
                if wait_time > 0:
                    logger.info(f"股票API限流，等待 {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    self._window_start = time.time()
                    self._request_count = 0
            
            # 确保最小请求间隔
            elapsed = now - self._last_request_time
            if elapsed < REQUEST_INTERVAL:
                time.sleep(REQUEST_INTERVAL - elapsed)
            
            self._last_request_time = time.time()
            self._request_count += 1
    
    def _get_from_cache(self, ticker: str) -> Optional[Dict]:
        """从缓存获取"""
        if ticker in self._cache:
            data, ts = self._cache[ticker]
            if time.time() - ts < CACHE_TTL:
                logger.debug(f"股票缓存命中: {ticker}")
                return data
            else:
                del self._cache[ticker]
        return None
    
    def _put_to_cache(self, ticker: str, data: Dict):
        """写入缓存"""
        self._cache[ticker] = (data, time.time())
    
    def _is_in_cooldown(self, ticker: str) -> bool:
        """检查是否在失败冷却期"""
        if ticker in self._failed_tickers:
            if time.time() - self._failed_tickers[ticker] < self._fail_cooldown:
                return True
            else:
                del self._failed_tickers[ticker]
        return False
    
    def _mark_failed(self, ticker: str):
        """标记失败"""
        self._failed_tickers[ticker] = time.time()
    
    def _extract_ticker_from_text(self, text: str) -> Optional[str]:
        """从文本中提取股票代码"""
        text_lower = text.lower()
        
        # 排除误匹配的短词（这些词常出现但不是指股票）
        # JD Power (咨询公司), GM (General Manager), F (作为评级)
        FALSE_POSITIVE_PATTERNS = [
            r'\bJD\s+Power\b',      # JD Power 咨询公司
            r'\bJ\.?D\.?\s+Power\b', # J.D. Power
            r'\bGM\b(?=\s+of\b)',    # GM of (General Manager of)
        ]
        
        for pattern in FALSE_POSITIVE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                # 如果匹配到误报模式，从文本中移除该部分再继续
                text = re.sub(pattern, '', text, flags=re.IGNORECASE)
                text_lower = text.lower()
        
        # 先检查是否直接包含股票代码 (如 TSLA, AAPL)
        # 只匹配独立的大写字母组合，排除容易误报的短代码
        ticker_pattern = r'\b([A-Z]{2,5})\b'  # 至少2个字母，减少误报
        matches = re.findall(ticker_pattern, text)
        
        # 安全的股票代码列表（排除容易误报的 JD, F, GM 等短代码）
        SAFE_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 
                        'AMD', 'INTC', 'QCOM', 'AVGO', 'NFLX', 'DIS', 'UBER', 
                        'ABNB', 'CRM', 'ORCL', 'IBM', 'CSCO', 'NIO', 'XPEV',
                        'BIDU', 'BABA', 'NTES', 'RIVN', 'LCID', 'STLA']
        
        for match in matches:
            if match in SAFE_TICKERS:
                return match
        
        # 检查公司名称映射（更可靠，基于完整公司名）
        for name, ticker in COMPANY_TICKER_MAP.items():
            if name in text_lower and ticker is not None:
                return ticker
        
        return None
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """获取单个股票的详细信息（带缓存和限流）"""
        if not YFINANCE_AVAILABLE:
            logger.warning("yfinance 不可用")
            return None
        
        # 检查缓存
        cached = self._get_from_cache(ticker)
        if cached:
            return cached
        
        # 检查失败冷却期
        if self._is_in_cooldown(ticker):
            logger.debug(f"股票 {ticker} 在冷却期，跳过")
            return None
        
        # 等待限流
        self._wait_for_rate_limit()
            
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or 'regularMarketPrice' not in info:
                # 尝试获取 fast_info
                try:
                    fast_info = stock.fast_info
                    if hasattr(fast_info, 'last_price') and fast_info.last_price:
                        stock_info = {
                            'ticker': ticker,
                            'name': info.get('shortName') or info.get('longName', ticker),
                            'price': fast_info.last_price,
                            'change': None,
                            'change_percent': fast_info.last_price / fast_info.previous_close - 1 if hasattr(fast_info, 'previous_close') and fast_info.previous_close else None,
                            'market_cap': fast_info.market_cap if hasattr(fast_info, 'market_cap') else None,
                            'pe_ratio': None,
                            'pe_forward': None,
                            'currency': info.get('currency', 'USD'),
                        }
                        if stock_info['change_percent']:
                            stock_info['change_percent'] *= 100
                            stock_info['change_formatted'] = f"{'+' if stock_info['change_percent'] >= 0 else ''}{stock_info['change_percent']:.2f}%"
                        self._format_market_cap(stock_info)
                        self._put_to_cache(ticker, stock_info)
                        logger.info(f"获取股票数据成功 (fast_info): {ticker}")
                        return stock_info
                except:
                    pass
                logger.warning(f"无法获取 {ticker} 的股票数据")
                self._mark_failed(ticker)
                return None
            
            # 提取关键数据
            stock_info = {
                'ticker': ticker,
                'name': info.get('shortName') or info.get('longName', ''),
                'price': info.get('regularMarketPrice') or info.get('currentPrice'),
                'change': info.get('regularMarketChange'),
                'change_percent': info.get('regularMarketChangePercent'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'pe_forward': info.get('forwardPE'),
                'currency': info.get('currency', 'USD'),
            }
            
            # 格式化市值
            self._format_market_cap(stock_info)
            
            # 格式化涨跌幅
            if stock_info['change_percent'] is not None:
                change_pct = stock_info['change_percent']
                stock_info['change_formatted'] = f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
            
            # 写入缓存
            self._put_to_cache(ticker, stock_info)
            logger.info(f"获取股票数据成功: {ticker} - {stock_info['name']}")
            return stock_info
            
        except Exception as e:
            error_msg = str(e)
            if 'Too Many Requests' in error_msg or 'Rate limit' in error_msg.lower():
                logger.error(f"获取 {ticker} 股票数据失败: Too Many Requests. Rate limited. Try after a while.")
                self._mark_failed(ticker)
            else:
                logger.error(f"获取 {ticker} 股票数据失败: {error_msg}")
                self._mark_failed(ticker)
            return None
    
    def _format_market_cap(self, stock_info: Dict):
        """格式化市值"""
        if stock_info.get('market_cap'):
            market_cap = stock_info['market_cap']
            if market_cap >= 1e12:
                stock_info['market_cap_formatted'] = f"{market_cap/1e12:.2f}万亿"
            elif market_cap >= 1e9:
                stock_info['market_cap_formatted'] = f"{market_cap/1e9:.0f}亿"
            elif market_cap >= 1e6:
                stock_info['market_cap_formatted'] = f"{market_cap/1e6:.0f}百万"
            else:
                stock_info['market_cap_formatted'] = str(market_cap)
    
    def get_stock_info_from_text(self, title: str, content: str) -> Optional[Dict]:
        """
        从新闻标题和内容中提取公司信息，并获取股票数据
        返回格式化的股票信息
        优先匹配标题中的公司（新闻主角），其次才是内容
        """
        if not YFINANCE_AVAILABLE:
            return None
        
        # 优先从标题提取（标题中的公司通常是新闻主角）
        ticker = self._extract_ticker_from_text(title)
        
        # 标题没找到，再从内容提取
        if not ticker:
            ticker = self._extract_ticker_from_text(content[:500])
        
        if not ticker:
            return None
        
        # 获取股票数据
        stock_info = self.get_stock_info(ticker)
        
        if stock_info:
            return stock_info
        
        return None


# 模块级实例，便于导入使用
_stock_service = None

def get_stock_service() -> StockService:
    """获取 StockService 单例"""
    global _stock_service
    if _stock_service is None:
        _stock_service = StockService()
    return _stock_service


def enrich_news_with_stock_info(news_item: Dict) -> Dict:
    """
    为新闻条目添加股票信息
    直接修改并返回 news_item
    """
    if not YFINANCE_AVAILABLE:
        news_item['stock_info'] = None
        return news_item
        
    try:
        service = get_stock_service()
        
        title = news_item.get('title', '')
        content = news_item.get('summary', '') or news_item.get('content', '')
        
        stock_info = service.get_stock_info_from_text(title, content)
        
        if stock_info:
            news_item['stock_info'] = stock_info
            logger.info(f"为新闻添加股票数据: {stock_info['ticker']}")
        else:
            news_item['stock_info'] = None
            
    except Exception as e:
        logger.error(f"添加股票信息失败: {str(e)}")
        news_item['stock_info'] = None
    
    return news_item
