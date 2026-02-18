"""
股票数据服务 - 使用 Yahoo Finance API
获取上市公司的市值、PE、当日涨跌等数据
"""
import requests
import logging
from typing import Dict, Optional, List
import re

logger = logging.getLogger(__name__)

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
    """股票数据服务"""
    
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.quote_url = "https://query1.finance.yahoo.com/v7/finance/quote"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
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
        try:
            url = f"{self.quote_url}?symbols={ticker}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"Yahoo Finance API 返回 {response.status_code}")
                return None
            
            data = response.json()
            
            if 'quoteResponse' not in data or 'result' not in data['quoteResponse']:
                return None
            
            results = data['quoteResponse']['result']
            if not results:
                return None
            
            quote = results[0]
            
            # 提取关键数据
            stock_info = {
                'ticker': ticker,
                'name': quote.get('shortName') or quote.get('longName', ''),
                'price': quote.get('regularMarketPrice'),
                'change': quote.get('regularMarketChange'),
                'change_percent': quote.get('regularMarketChangePercent'),
                'market_cap': quote.get('marketCap'),
                'pe_ratio': quote.get('trailingPE'),
                'pe_forward': quote.get('forwardPE'),
                'currency': quote.get('currency', 'USD'),
            }
            
            # 格式化市值
            if stock_info['market_cap']:
                market_cap = stock_info['market_cap']
                if market_cap >= 1e12:
                    stock_info['market_cap_formatted'] = f"{market_cap/1e12:.2f}万亿"
                elif market_cap >= 1e9:
                    stock_info['market_cap_formatted'] = f"{market_cap/1e9:.0f}亿"
                elif market_cap >= 1e6:
                    stock_info['market_cap_formatted'] = f"{market_cap/1e6:.0f}百万"
                else:
                    stock_info['market_cap_formatted'] = str(market_cap)
            
            # 格式化涨跌幅
            if stock_info['change_percent'] is not None:
                change_pct = stock_info['change_percent']
                stock_info['change_formatted'] = f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
            
            logger.info(f"获取股票数据成功: {ticker} - {stock_info['name']}")
            return stock_info
            
        except requests.exceptions.Timeout:
            logger.warning(f"获取 {ticker} 股票数据超时")
            return None
        except Exception as e:
            logger.error(f"获取 {ticker} 股票数据失败: {str(e)}")
            return None
    
    def get_stock_info_from_text(self, title: str, content: str) -> Optional[Dict]:
        """
        从新闻标题和内容中提取公司信息，并获取股票数据
        返回格式化的股票信息
        """
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
