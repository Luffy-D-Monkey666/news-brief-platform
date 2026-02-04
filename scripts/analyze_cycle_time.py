#!/usr/bin/env python3
"""
新闻处理周期分析工具

用法:
1. 从Render Dashboard复制日志内容
2. 保存为 render_logs.txt
3. 运行: python analyze_cycle_time.py render_logs.txt

或者直接粘贴日志内容运行
"""

import re
import sys
from datetime import datetime
from typing import List, Tuple


def parse_log_file(content: str) -> dict:
    """解析日志内容，提取关键信息"""

    results = {
        'cycle_times': [],
        'skip_count': 0,
        'step_times': [],
        'ai_processing_times': []
    }

    # 提取总耗时
    pattern_cycle = r'本轮采集完成，耗时\s+([\d.]+)\s+秒'
    for match in re.finditer(pattern_cycle, content):
        elapsed = float(match.group(1))
        results['cycle_times'].append(elapsed)

    # 提取跳过次数
    pattern_skip = r'上一轮采集仍在进行中'
    results['skip_count'] = len(re.findall(pattern_skip, content))

    # 提取AI处理完成数量
    pattern_ai = r'步骤 4/5 完成: AI 处理完成，生成\s+(\d+)\s+条简报'
    for match in re.finditer(pattern_ai, content):
        count = int(match.group(1))
        results['ai_processing_times'].append(count)

    # 提取步骤完成信息
    steps = [
        (r'步骤 1/5 完成: 爬取到\s+(\d+)\s+条新闻', 'crawl'),
        (r'步骤 2/5 完成: 过滤后剩余\s+(\d+)\s+条新新闻', 'filter'),
        (r'步骤 3/5 完成: 已保存\s+(\d+)\s+条原始新闻', 'save_raw'),
        (r'步骤 4/5 完成: AI 处理完成，生成\s+(\d+)\s+条简报', 'ai_process'),
        (r'步骤 5/5 完成: 成功保存\s+(\d+)/(\d+)\s+条简报', 'save_brief')
    ]

    for pattern, step_name in steps:
        for match in re.finditer(pattern, content):
            if step_name == 'save_brief':
                saved = int(match.group(1))
                total = int(match.group(2))
                results['step_times'].append({
                    'step': step_name,
                    'saved': saved,
                    'total': total
                })
            else:
                count = int(match.group(1))
                results['step_times'].append({
                    'step': step_name,
                    'count': count
                })

    return results


def format_time(seconds: float) -> str:
    """格式化时间显示"""
    minutes = seconds / 60
    if minutes >= 1:
        return f"{minutes:.1f}分钟 ({seconds:.0f}秒)"
    else:
        return f"{seconds:.0f}秒"


def print_analysis(results: dict):
    """打印分析结果"""

    print("=" * 60)
    print("新闻处理周期性能分析报告")
    print("=" * 60)
    print()

    # 总耗时统计
    if results['cycle_times']:
        print("📊 处理周期耗时统计")
        print("-" * 60)

        cycle_times = results['cycle_times']
        avg_time = sum(cycle_times) / len(cycle_times)
        min_time = min(cycle_times)
        max_time = max(cycle_times)

        print(f"样本数量: {len(cycle_times)}次")
        print(f"平均耗时: {format_time(avg_time)}")
        print(f"最快一次: {format_time(min_time)}")
        print(f"最慢一次: {format_time(max_time)}")
        print()

        print("最近10次耗时:")
        for i, elapsed in enumerate(cycle_times[-10:], 1):
            status = ""
            if elapsed > 600:
                status = "⚠️  过慢"
            elif elapsed > 300:
                status = "⚡ 可优化"
            else:
                status = "✅ 正常"

            print(f"  #{i}: {format_time(elapsed)} {status}")
        print()

        # 性能评级
        print("⏱️  性能评估:")
        if avg_time > 600:
            print("  🔴 Critical - 平均耗时>10分钟，建议将CRAWL_INTERVAL设为900秒(15分钟)")
        elif avg_time > 300:
            print("  🟡 Warning - 平均耗时>5分钟，建议将CRAWL_INTERVAL设为450秒(7.5分钟)")
        elif avg_time > 180:
            print("  🟢 Good - 平均耗时3-5分钟，建议将CRAWL_INTERVAL设为300秒(5分钟)")
        else:
            print("  🟢 Excellent - 平均耗时<3分钟，当前CRAWL_INTERVAL(120秒)可接受")
        print()
    else:
        print("⚠️  未找到处理周期耗时数据")
        print()

    # 跳过调度统计
    print("🚫 调度跳过统计")
    print("-" * 60)
    print(f"跳过次数: {results['skip_count']}次")

    if results['cycle_times'] and results['skip_count'] > 0:
        completed_cycles = len(results['cycle_times'])
        skip_ratio = results['skip_count'] / completed_cycles
        print(f"跳过比例: {skip_ratio:.1f}次/完成周期")

        if skip_ratio > 3:
            print("  🔴 严重 - 每次完成前平均跳过>3次，间隔严重过短")
        elif skip_ratio > 1:
            print("  🟡 警告 - 每次完成前平均跳过>1次，建议增加间隔")
        else:
            print("  🟢 正常 - 偶尔跳过，间隔基本合理")
    print()

    # AI处理统计
    if results['ai_processing_times']:
        print("🤖 AI处理统计")
        print("-" * 60)
        avg_count = sum(results['ai_processing_times']) / len(results['ai_processing_times'])
        print(f"平均处理数量: {avg_count:.0f}条/次")
        print(f"最多一次: {max(results['ai_processing_times'])}条")
        print(f"最少一次: {min(results['ai_processing_times'])}条")
        print()

        # 估算AI单条耗时
        if results['cycle_times'] and results['ai_processing_times']:
            avg_cycle = sum(results['cycle_times']) / len(results['cycle_times'])
            # AI处理大约占总时间的80%
            ai_time = avg_cycle * 0.8
            time_per_news = ai_time / avg_count if avg_count > 0 else 0
            print(f"估算AI单条耗时: {time_per_news:.1f}秒/条")

            if time_per_news > 15:
                print("  🔴 Critical - 单条耗时>15秒，DeepSeek API可能很慢或有限流")
            elif time_per_news > 8:
                print("  🟡 Warning - 单条耗时>8秒，建议考虑并发处理或限制数量")
            else:
                print("  🟢 Good - 单条耗时正常")
            print()

    # 建议
    print("💡 优化建议")
    print("-" * 60)

    if results['cycle_times']:
        avg_time = sum(results['cycle_times']) / len(results['cycle_times'])

        if avg_time > 600:
            print("1. 🔴 立即执行:")
            print("   - 将CRAWL_INTERVAL改为900秒(15分钟)")
            print("   - 在Render Dashboard → Environment → CRAWL_INTERVAL=900")
            print()
            print("2. 🟡 后续优化:")
            print("   - 实现AI并发处理（ThreadPoolExecutor）")
            print("   - 或限制每次最多处理30条新闻")
            print("   - 移除失效的RSS源")
        elif avg_time > 300:
            print("1. 建议将CRAWL_INTERVAL改为450-600秒(7.5-10分钟)")
            print("2. 考虑优化AI处理速度")
        elif avg_time > 180:
            print("1. 可以将CRAWL_INTERVAL保持在300秒(5分钟)")
            print("2. 或适当优化后降低到240秒(4分钟)")
        else:
            print("✅ 当前性能良好，无需优化")

    print()
    print("=" * 60)


def main():
    """主函数"""

    if len(sys.argv) > 1:
        # 从文件读取
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"错误: 文件 '{filename}' 不存在")
            sys.exit(1)
    else:
        # 交互式输入
        print("请粘贴Render日志内容，完成后按Ctrl+D (Mac/Linux) 或 Ctrl+Z (Windows):")
        print()
        content = sys.stdin.read()

    # 分析日志
    results = parse_log_file(content)

    # 打印结果
    print_analysis(results)


if __name__ == '__main__':
    main()
