# 精简版 Prompt v3.1 - 分级处理，进一步优化 token
# 改进：
# 1. 简化版 prompt 用于 normal 新闻（节省 60% token）
# 2. 完整版 prompt 只用于 breaking/high 新闻
# 3. 移除大多数新闻不需要的字段

# ============================================================
# 第一阶段：快速分类 + 摘要（所有新闻都用这个）
# 约 400 tokens input，200 tokens output
# ============================================================
QUICK_PROCESS_PROMPT = """新闻编辑，分析并输出JSON。

分类：ai_technology/robotics/ai_programming/semiconductors/automotive/consumer_electronics/finance_investment/business_tech/politics_world/economy_policy/health_medical/energy_environment/entertainment_sports/anime/one_piece/tcg/general

标题: {title}
内容: {content}

输出：
{{"title_zh":"中文标题≤25字","category":"分类","importance":"breaking/high/normal","summary":"事件概述(1句)+要点(2-3个bullet)"}}

importance判断：
- breaking: 重大发布/突发事件/行业变革
- high: 知名公司动态/重要数据/政策变化
- normal: 日常新闻/评论/分析

严格输出JSON："""


# ============================================================
# 第二阶段：详细处理（仅 breaking/high 新闻）
# 约 600 tokens input，400 tokens output
# ============================================================
DETAILED_PROCESS_PROMPT = """为重要新闻补充详细信息，输出JSON。

已有信息：
标题: {title_zh}
分类: {category}
摘要: {summary}

原文内容: {content}

根据分类补充对应字段：

1. key_metrics: 关键数字[{{name,value,unit}}]，无则[]

2. background: 背景知识（仅 breaking 需要）
   {{context:"一句话背景",timeline:[{{date,event}}]}}，普通新闻返回null

3. 分类专属字段（其他分类返回null）：
   - finance_investment/business_tech/economy_policy:
     action_advice: "风险提示+行动建议"
   - ai_technology/robotics/ai_programming/semiconductors:
     tech_insight: {{principle:"技术原理",comparison:"对比",maturity:"成熟度"}}
   - 融资新闻:
     funding_history: {{company,rounds:[{{round,amount,date}}],total_funding}}
   - consumer_electronics/automotive:
     supply_chain_insight: {{impact,related_companies:[{{name,role}}]}}

4. entities: 需要解释的非知名实体(0-2个)
   [{{name,type,context:"20字背景"}}]
   不提取：苹果/谷歌/微软/特斯拉/英伟达/OpenAI/马斯克等公众熟知实体

输出JSON："""


# ============================================================
# 兼容旧版：合并后的完整 prompt（保留用于特殊情况）
# ============================================================
PROCESS_PROMPT_V3 = """你是资深新闻编辑，分析新闻并输出JSON。

分类：ai_technology(AI技术)/robotics(机器人)/ai_programming(AI编程)/semiconductors(芯片)/automotive(汽车)/consumer_electronics(消费电子)/finance_investment(投资财经)/business_tech(商业科技)/politics_world(政治国际)/economy_policy(经济政策)/health_medical(健康医疗)/energy_environment(能源环境)/entertainment_sports(娱乐体育)/anime(动漫)/one_piece(海贼王)/tcg(TCG卡牌)/general(综合)

新闻标题: {title}
新闻内容: {content}

输出字段：
1. title_zh: 中文标题≤25字
2. category: 分类
3. importance: breaking(重大)/high(较重要)/normal(普通)
4. summary: 事件概述(1-2句)+要点(2-3个bullet)
5. key_metrics: 关键数字[{{name,value,unit}}]，无则[]
6. action_advice: 仅finance/business/economy需要，其他null
7. background: 仅breaking需要{{context,timeline}}，其他null
8. tech_insight: 仅tech类需要，其他null
9. funding_history: 仅融资新闻需要，其他null
10. supply_chain_insight: 仅electronics/automotive需要，其他null
11. entities: 非知名实体(0-2个)[{{name,type,context}}]，无则[]

示例（普通新闻）：
{{"title_zh":"某公司发布新产品","category":"business_tech","importance":"normal","summary":"事件概述：XX公司发布新品。\\n• 要点1\\n• 要点2","key_metrics":[],"action_advice":null,"background":null,"tech_insight":null,"funding_history":null,"supply_chain_insight":null,"entities":[]}}

严格输出JSON："""
