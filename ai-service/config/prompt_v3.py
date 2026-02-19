# 精简版 Prompt v3 - 减少约 40% token 消耗
# 只保留 1 个完整示例 + 1 个普通新闻简短示例

PROCESS_PROMPT_V3 = """你是资深新闻编辑，分析新闻并输出JSON。

分类：ai_technology(AI技术)/robotics(机器人)/ai_programming(AI编程)/semiconductors(芯片)/automotive(汽车)/consumer_electronics(消费电子)/podcasts(播客)/finance_investment(投资财经)/business_tech(商业科技)/politics_world(政治国际)/economy_policy(经济政策)/health_medical(健康医疗)/energy_environment(能源环境)/entertainment_sports(娱乐体育)/anime(动漫)/one_piece(海贼王)/tcg(TCG卡牌)/general(综合)

新闻标题: {title}
新闻内容: {content}

输出字段：
1. title_zh: 中文标题≤30字
2. category: 分类
3. importance: breaking(重大突发)/high(较重要)/normal(普通)
4. summary: 结构化摘要，格式：
   事件概述: 1-2句
   原文引用: "原文金句" — 说话人
   重要细节:
   • 要点1
   • 要点2
   • 要点3
   后续影响: 分析意义
5. action_advice: 仅finance_investment/business_tech/economy_policy需要，含风险提示和行动建议，其他null
6. key_metrics: 关键数字数组[{{name,value,unit,entity}}]，无则[]
7. background: 仅breaking/high需要{{context,timeline:[{{date,event}}]}}，其他null
8. tech_insight: 仅ai_technology/robotics/ai_programming/semiconductors需要{{principle,comparison,maturity}}，其他null
9. funding_history: 仅融资新闻需要{{company,rounds:[{{round,amount,date,investors}}],total_funding,valuation}}，其他null
10. supply_chain_insight: 仅consumer_electronics/automotive需要{{impact,related_companies:[{{name,role,effect}}],capacity_info}}，其他null

示例（重要AI新闻）：
{{
  "title_zh": "OpenAI发布GPT-5，性能提升3倍",
  "category": "ai_technology",
  "importance": "breaking",
  "summary": "事件概述: OpenAI发布GPT-5，推理能力和多模态理解重大突破。\\n\\n原文引用: \\"This is a pivotal moment.\\" — Sam Altman\\n\\n重要细节:\\n• 推理速度提升3倍\\n• 准确率提高40%\\n• API价格不变\\n\\n后续影响: 加速AI应用落地。",
  "action_advice": null,
  "key_metrics": [{{"name":"性能提升","value":3,"unit":"倍","entity":"GPT-5"}}],
  "background": {{"context":"OpenAI成立于2015年，2022年发布ChatGPT。","timeline":[{{"date":"2023.03","event":"GPT-4发布"}}]}},
  "tech_insight": {{"principle":"MoE架构，万亿参数。","comparison":"支持100万token上下文。","maturity":"商用落地"}},
  "funding_history": null,
  "supply_chain_insight": null
}}

普通新闻示例：
{{"title_zh":"某公司发布产品","category":"general","importance":"normal","summary":"事件概述:...","action_advice":null,"key_metrics":[],"background":null,"tech_insight":null,"funding_history":null,"supply_chain_insight":null}}

严格输出JSON："""
