#!/usr/bin/env python3
"""测试AI Service的OpenAI集成"""

import os
import sys

# 添加AI Service到路径
sys.path.insert(0, 'ai-service/src')

from processors.cloud_ai_processor import NewsProcessor

# 测试OpenAI是否配置正确
def test_openai():
    print("=" * 50)
    print("测试OpenAI配置")
    print("=" * 50)

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ 错误: OPENAI_API_KEY环境变量未设置")
        print("\n请设置环境变量:")
        print("export OPENAI_API_KEY='your-api-key'")
        return False

    print(f"✅ API Key已设置: {api_key[:10]}...{api_key[-4:]}")

    try:
        processor = NewsProcessor('openai')
        print("✅ NewsProcessor初始化成功")

        # 测试摘要生成
        print("\n测试中文摘要生成...")
        test_title = "OpenAI Releases GPT-5 Model"
        test_content = "OpenAI announced today the release of GPT-5, their latest language model with improved reasoning capabilities."

        prompt_template = """请分析以下新闻内容，用中文提炼成一条详细的新闻总结。
要求：
1. 将标题翻译成中文（保留专有名词的英文）
2. 用中文详细总结核心内容（150-200字）

新闻标题：{title}
新闻内容：{content}

请按以下格式返回：
中文标题
详细总结
"""

        chinese_title, chinese_summary = processor.ai.summarize_news(
            test_title,
            test_content,
            prompt_template
        )

        if chinese_title and chinese_summary:
            print(f"\n✅ 成功生成中文摘要:")
            print(f"中文标题: {chinese_title}")
            print(f"中文摘要: {chinese_summary[:100]}...")
            return True
        else:
            print("\n❌ 错误: AI返回空结果")
            return False

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_openai()
    sys.exit(0 if success else 1)
