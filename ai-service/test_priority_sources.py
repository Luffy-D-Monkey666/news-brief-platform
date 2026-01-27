#!/usr/bin/env python3
"""
测试TCG/海贼王/动漫专门信息源的可用性
快速诊断哪些源能正常工作，哪些需要替换
"""

import feedparser
import sys
import time
from collections import defaultdict

# 提取配置文件中的TCG/海贼王/动漫相关源
PRIORITY_SOURCES = {
    'TCG卡牌游戏': [
        'https://www.pokemon.com/us/pokemon-news/rss',
        'https://www.pokebeach.com/feed',
        'https://www.pokeguardian.com/feed',
        'https://rsshub.app/bandai/onepiece-cardgame',
        'https://onepiece-cardgame.com/news/rss',
        'https://www.dbs-cardgame.com/us-en/news/rss',
        'https://www.yugioh-card.com/en/news/rss.xml',
        'https://ygoprodeck.com/feed/',
        'https://magic.wizards.com/en/rss/articles.xml',
        'https://www.channelfireball.com/feed/',
        'https://www.tcgplayer.com/feed',
        'https://infinite.tcgplayer.com/feed',
    ],
    '海贼王': [
        'https://rsshub.app/onepiece/news',
        'https://rsshub.app/shonenjump/series/one-piece',
        'https://rsshub.app/animenewsnetwork/news/one-piece',
        'https://www.crunchyroll.com/rss/anime?lang=enUS&tagged=one-piece',
        'https://onepiecepodcast.com/feed/',
        'https://rsshub.app/bangumi/subject/1000',
        'https://rsshub.app/toei-anim/onepiece',
        'https://rsshub.app/manga/onepiece',
        'https://ww8.readonepiece.com/feed/',
    ],
    '动画漫画': [
        'https://www.animenewsnetwork.com/rss.xml',
        'https://www.crunchyroll.com/rss/news',
        'https://www.funimation.com/blog/feed/',
        'https://myanimelist.net/rss/news.xml',
        'https://www.animenewsnetwork.com/all/rss.xml',
        'https://rsshub.app/toei-anim',
        'https://rsshub.app/mappa',
        'https://rsshub.app/bones',
        'https://rsshub.app/kyotoanimation',
        'https://rsshub.app/shonenjump',
        'https://rsshub.app/shueisha',
        'https://rsshub.app/kodansha',
        'https://rsshub.app/dengekionline',
        'https://rsshub.app/seiyuu',
        'https://rsshub.app/bangumi/calendar',
        'https://www.animatetimes.com/feed',
        'https://kotaku.com/rss',
        'https://comicbook.com/anime/rss.xml',
    ]
}


def test_feed(url, timeout=10):
    """测试单个RSS源"""
    try:
        import socket
        socket.setdefaulttimeout(timeout)
        
        start_time = time.time()
        feed = feedparser.parse(url)
        elapsed = time.time() - start_time
        
        socket.setdefaulttimeout(None)
        
        entry_count = len(feed.entries)
        status = feed.get('status', 0)
        
        if status == 200 and entry_count > 0:
            return {
                'status': 'SUCCESS',
                'entries': entry_count,
                'time': f'{elapsed:.2f}s',
                'title': feed.feed.get('title', 'N/A')[:50]
            }
        elif status == 200:
            return {
                'status': 'EMPTY',
                'entries': 0,
                'time': f'{elapsed:.2f}s',
                'error': '源返回空数据'
            }
        else:
            return {
                'status': 'FAILED',
                'entries': 0,
                'time': f'{elapsed:.2f}s',
                'error': f'HTTP {status}'
            }
            
    except Exception as e:
        return {
            'status': 'ERROR',
            'entries': 0,
            'time': 'N/A',
            'error': str(e)[:100]
        }


def main():
    """主测试函数"""
    print("=" * 80)
    print("TCG/海贼王/动漫信息源可用性测试")
    print("=" * 80)
    print()
    
    results = defaultdict(list)
    
    for category, sources in PRIORITY_SOURCES.items():
        print(f"\n{'='*80}")
        print(f"测试分类: {category} ({len(sources)}个源)")
        print(f"{'='*80}\n")
        
        for idx, url in enumerate(sources, 1):
            # 显示简短URL
            short_url = url if len(url) <= 70 else url[:67] + '...'
            print(f"[{idx}/{len(sources)}] {short_url}")
            
            result = test_feed(url)
            results[category].append({
                'url': url,
                **result
            })
            
            # 显示结果
            if result['status'] == 'SUCCESS':
                print(f"  ✅ 成功 - {result['entries']}条 - {result['time']} - {result['title']}")
            elif result['status'] == 'EMPTY':
                print(f"  ⚠️  空源 - {result['time']} - {result['error']}")
            elif result['status'] == 'FAILED':
                print(f"  ❌ 失败 - {result['time']} - {result['error']}")
            else:
                print(f"  ❌ 错误 - {result['error']}")
            
            # 避免请求过快
            time.sleep(0.5)
    
    # 统计总结
    print(f"\n\n{'='*80}")
    print("测试总结")
    print(f"{'='*80}\n")
    
    for category in PRIORITY_SOURCES.keys():
        cat_results = results[category]
        total = len(cat_results)
        success = sum(1 for r in cat_results if r['status'] == 'SUCCESS')
        empty = sum(1 for r in cat_results if r['status'] == 'EMPTY')
        failed = sum(1 for r in cat_results if r['status'] in ['FAILED', 'ERROR'])
        
        success_rate = (success / total * 100) if total > 0 else 0
        
        print(f"{category}:")
        print(f"  总计: {total}个源")
        print(f"  ✅ 成功: {success}个 ({success_rate:.1f}%)")
        print(f"  ⚠️  空源: {empty}个")
        print(f"  ❌ 失败: {failed}个")
        
        # 列出失败的源
        if failed > 0:
            print(f"\n  需要替换的源:")
            for r in cat_results:
                if r['status'] in ['FAILED', 'ERROR']:
                    short_url = r['url'] if len(r['url']) <= 60 else r['url'][:57] + '...'
                    print(f"    - {short_url}")
                    print(f"      原因: {r['error']}")
        print()
    
    # 给出建议
    total_sources = sum(len(sources) for sources in PRIORITY_SOURCES.values())
    total_success = sum(
        sum(1 for r in results[cat] if r['status'] == 'SUCCESS')
        for cat in PRIORITY_SOURCES.keys()
    )
    
    print(f"{'='*80}")
    print(f"整体统计: {total_success}/{total_sources}个源可用 ({total_success/total_sources*100:.1f}%)")
    
    if total_success / total_sources < 0.7:
        print("\n⚠️  警告: 超过30%的源不可用，建议:")
        print("  1. 替换失效的RSSHub源")
        print("  2. 增加更多官方RSS源")
        print("  3. 考虑使用备用信息源")
    elif total_success / total_sources < 0.9:
        print("\n⚠️  建议: 部分源不可用，建议替换失效源以提升内容覆盖率")
    else:
        print("\n✅ 信息源状态良好！")
    
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
