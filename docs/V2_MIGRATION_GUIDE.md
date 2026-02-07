# NewsHub V2 迁移指南

## 概述

NewsHub V2 引入了多源新闻采集系统，支持：
- ✅ RSS 订阅源
- ✅ X (Twitter) 社交媒体
- ✅ 微信公众号
- ✅ 知乎话题
- ✅ 即刻圈子

## 新特性

### 1. X (Twitter) 支持

通过 RSSHub 免费获取 Twitter 内容：

```python
# 格式
https://rsshub.app/twitter/user/{username}

# 示例
https://rsshub.app/twitter/user/OpenAI      # OpenAI 官方
https://rsshub.app/twitter/user/ylecun       # Yann LeCun
https://rsshub.app/twitter/user/elonmusk     # Elon Musk
```

**Twitter 内容过滤规则**：
- 跳过纯转推（RT @ 开头）
- 跳过内容过短（< 20字符）
- 保留原创推文和引用推文

### 2. 中文本土源

| 平台 | 示例 | 说明 |
|------|------|------|
| 微信公众号 | `https://rsshub.app/wechat/mp/阿里巴巴` | 企业官方账号 |
| 知乎话题 | `https://rsshub.app/zhihu/topic/19550517` | AI话题讨论 |
| 即刻圈子 | `https://rsshub.app/jike/topic/...` | 科技圈子动态 |

### 3. 信息源统计

| 类型 | 数量 | 说明 |
|------|------|------|
| RSS 源 | ~60个 | 精选高质量源（精简自100+） |
| Twitter | ~25个 | AI/机器人/芯片/汽车大佬 |
| 微信公众号 | 5个 | 头部科技公司 |
| 知乎话题 | 3个 | 热门技术话题 |
| 即刻圈子 | 2个 | 科技资讯圈子 |
| **总计** | **~95个** | 质量优先，减少噪音 |

## 迁移步骤

### 步骤 1：备份当前配置

```bash
cd ai-service/config
cp settings.py settings.py.backup
```

### 步骤 2：更新代码文件

已创建的新文件：
- `config/sources_v2.py` - 新的多源配置
- `src/crawlers/multi_source_crawler.py` - 多源爬虫
- `src/main_v2.py` - V2 主服务

### 步骤 3：切换主程序

```bash
cd ai-service/src
# 备份原 main.py
mv main.py main_v1.py
# 使用 V2
mv main_v2.py main.py
```

### 步骤 4：测试运行

```bash
cd ai-service
python src/main.py
```

应该看到：
```
NewsHub V2 新闻简报AI服务启动
总计新闻源: 95 个
支持源: RSS + Twitter/X + 微信公众号 + 知乎 + 即刻
```

## 回滚方案

如果出现问题，快速回滚到 V1：

```bash
cd ai-service/src
mv main.py main_v2.py
mv main_v1.py main.py
```

## 环境变量

V2 支持的环境变量：

```bash
# AI 提供商（新增 Kimi 支持）
AI_PROVIDER=kimi  # 或 deepseek, openai, claude
KIMI_API_KEY=your-kimi-api-key

# 数据库
MONGODB_URI=mongodb://...
REDIS_URL=redis://...

# 采集间隔
CRAWL_INTERVAL=600  # 10分钟

# 端口
PORT=10000
```

## 添加新的 Twitter 源

编辑 `config/sources_v2.py`：

```python
TWITTER_SOURCES = {
    'ai_technology': [
        # ... 现有源
        'https://rsshub.app/twitter/user/NewAccount',  # 添加新账号
    ],
}
```

## 注意事项

1. **RSSHub 稳定性**：Twitter/微信等源依赖 RSSHub，如果 RSSHub 不可用，对应源会跳过
2. **Rate Limiting**：Twitter 通过 RSSHub 有访问频率限制，不建议采集过于频繁
3. **内容质量**：Twitter 内容较短，AI 摘要效果可能不如长文章

## 验证

部署后检查健康端点：

```bash
curl https://your-service.onrender.com/health
```

应返回：
```json
{
  "status": "running",
  "service": "news-ai-service-v2",
  "version": "2.0.0",
  "features": ["rss", "twitter", "wechat", "zhihu", "jike"]
}
```
