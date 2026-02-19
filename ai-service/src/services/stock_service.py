"""
股票数据服务 - 使用 yfinance 库
获取上市公司的市值、PE、当日涨跌等数据
"""
import logging
from typing import Dict, Optional
import re

logger = logging.getLogger(__name__)

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
    'rivian': 'RIVN',
    'lucid': 'LCID',
    
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
    """股票数据服务 - 使用 yfinance"""
    
    def __init__(self):
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance 不可用，股票服务初始化失败")
    
    def _extract_ticker_from_text(self, text: str) -> Optional[str]:
        """从文本中提取股票代码"""
        text_lower = text.lower()
        
        # 先检查是否直接包含股票代码 (如 TSLA, AAPL)
        ticker_pattern = r'\b([A-Z]{1,5})\b'
        matches = re.findall(ticker_pattern, text)
        for match in matches:
            if match in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 
                        'AMD', 'INTC', 'QCOM', 'AVGO', 'NFLX', 'DIS', 'UBER', 
                        'ABNB', 'CRM', 'ORCL', 'IBM', 'CSCO', 'NIO', 'LI', 'XPEV',
                        'JD', 'BIDU', 'BABA', 'NTES', 'F', 'GM', 'RIVN', 'LCID']:
                return match
        
        # 检查公司名称映射
        for name, ticker in COMPANY_TICKER_MAP.items():
            if name in text_lower and ticker is not None:
                return ticker
        
        return None
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """获取单个股票的详细信息"""
        if not YFINANCE_AVAILABLE:
            logger.warning("yfinance 不可用")
            return None
            
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
                        logger.info(f"获取股票数据成功 (fast_info): {ticker}")
                        return stock_info
                except:
                    pass
                logger.warning(f"无法获取 {ticker} 的股票数据")
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
            
            logger.info(f"获取股票数据成功: {ticker} - {stock_info['name']}")
            return stock_info
            
        except Exception as e:
            logger.error(f"获取 {ticker} 股票数据失败: {str(e)}")
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
        """
        if not YFINANCE_AVAILABLE:
            return None
            
        # 合并标题和内容进行分析
        full_text = f"{title} {content[:500]}"
        
        # 提取股票代码
        ticker = self._extract_ticker_from_text(full_text)
        
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
