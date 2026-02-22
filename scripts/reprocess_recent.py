#!/usr/bin/env python3
"""
重新处理最近 N 小时内的新闻
使用恢复后的 PROCESS_PROMPT_V3（含原文引用+后续影响）

用法：
    python scripts/reprocess_recent.py --hours 6
    python scripts/reprocess_recent.py --hours 6 --dry-run  # 只统计，不处理
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

# 添加 ai-service 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai-service'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai-service', 'src'))

from config.prompt_v3 import PROCESS_PROMPT_V3

# MongoDB 连接（使用 Render 外部 URL）
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://newsbrief:Tq0cxAhnl5LoSxN7@cluster0.lixqn.mongodb.net/news-brief?retryWrites=true&w=majority')

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
DEEPSEEK_MODEL = 'deepseek-chat'


def call_deepseek(prompt: str, max_tokens: int = 800) -> str:
    """调用 DeepSeek API"""
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': DEEPSEEK_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.3
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"API 错误: {response.status_code} - {response.text[:200]}")


def process_news(title: str, content: str) -> dict:
    """处理单条新闻"""
    content_truncated = content[:800] if content else ""
    prompt = PROCESS_PROMPT_V3.format(title=title, content=content_truncated)
    
    result = call_deepseek(prompt)
    
    # 解析 JSON
    if '```json' in result:
        result = result.split('```json')[1].split('```')[0]
    elif '```' in result:
        result = result.split('```')[1].split('```')[0]
    
    return json.loads(result.strip())


def main():
    parser = argparse.ArgumentParser(description='重新处理最近的新闻')
    parser.add_argument('--hours', type=int, default=6, help='处理最近 N 小时内的新闻')
    parser.add_argument('--dry-run', action='store_true', help='只统计，不处理')
    parser.add_argument('--workers', type=int, default=3, help='并发数')
    args = parser.parse_args()
    
    if not DEEPSEEK_API_KEY:
        print("❌ 请设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)
    
    # 连接 MongoDB
    print(f"📦 连接 MongoDB...", flush=True)
    client = MongoClient(MONGODB_URI)
    db = client['news-brief']
    
    # 查询时间范围
    since = datetime.utcnow() - timedelta(hours=args.hours)
    print(f"🕐 查询 {args.hours} 小时内的新闻 (UTC: {since.isoformat()})", flush=True)
    
    # 查询 briefs（已处理的简报）
    briefs = list(db.briefs.find({
        'created_at': {'$gte': since}
    }).sort('created_at', -1))
    
    print(f"📊 找到 {len(briefs)} 条简报需要重新处理", flush=True)
    
    if args.dry_run:
        print("\n🔍 Dry-run 模式，以下是将要处理的新闻：")
        for i, brief in enumerate(briefs[:10], 1):
            print(f"  {i}. [{brief.get('category')}] {brief.get('title', '')[:50]}")
        if len(briefs) > 10:
            print(f"  ... 还有 {len(briefs) - 10} 条")
        return
    
    # 查询对应的 raw_news（获取原始内容）
    print(f"\n🔄 开始重新处理...", flush=True)
    
    success = 0
    failed = 0
    
    def process_one(brief):
        """处理单条"""
        try:
            # 查找对应的原始新闻
            raw = db.news.find_one({'link': brief.get('link')})
            if not raw:
                return None, "原始新闻未找到"
            
            # 重新处理
            result = process_news(raw.get('title', ''), raw.get('content', ''))
            
            # 更新字段
            update_fields = {
                'title': result.get('title_zh', brief.get('title')),
                'summary': result.get('summary', brief.get('summary')),
                'category': result.get('category', brief.get('category')),
                'importance': result.get('importance', 'normal'),
                'action_advice': result.get('action_advice'),
                'key_metrics': result.get('key_metrics', []),
                'background': result.get('background'),
                'tech_insight': result.get('tech_insight'),
                'funding_history': result.get('funding_history'),
                'supply_chain_insight': result.get('supply_chain_insight'),
                'entities': result.get('entities', []),
                'reprocessed_at': datetime.utcnow()
            }
            
            # 更新数据库
            db.briefs.update_one(
                {'_id': brief['_id']},
                {'$set': update_fields}
            )
            
            return result.get('title_zh', '')[:30], None
        except Exception as e:
            return None, str(e)
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_one, brief): brief for brief in briefs}
        
        for i, future in enumerate(as_completed(futures), 1):
            brief = futures[future]
            title, error = future.result()
            
            if error:
                failed += 1
                print(f"  ❌ [{i}/{len(briefs)}] 失败: {error[:50]}", flush=True)
            else:
                success += 1
                print(f"  ✅ [{i}/{len(briefs)}] {title}...", flush=True)
    
    print(f"\n📊 处理完成: 成功 {success}, 失败 {failed}")
    print(f"💰 预估消耗: ¥{success * 0.02:.2f}")


if __name__ == '__main__':
    main()
