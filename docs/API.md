# NewsHub API 文档

Base URL: `https://your-backend.onrender.com/api`

## 简报 API

### 获取最新简报

```
GET /briefs/latest
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 分类筛选 |
| limit | number | 否 | 返回数量，默认 20 |
| hours | number | 否 | 时间范围（小时） |

**响应**:
```json
{
  "success": true,
  "count": 20,
  "data": [
    {
      "_id": "...",
      "title": "OpenAI发布GPT-5",
      "summary": "事件概述: ...",
      "category": "ai_technology",
      "importance": "breaking",
      "source": "OpenAI Blog",
      "source_tier": "official",
      "link": "https://...",
      "created_at": "2026-02-19T10:00:00Z"
    }
  ]
}
```

### 获取历史简报（分页）

```
GET /briefs/history
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 分类筛选 |
| page | number | 否 | 页码，默认 1 |
| limit | number | 否 | 每页数量，默认 20 |
| hours | number | 否 | 时间范围（小时） |

**响应**:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000,
    "pages": 50
  }
}
```

### 获取分类统计

```
GET /briefs/stats
```

**响应**:
```json
{
  "success": true,
  "data": [
    { "_id": "ai_technology", "count": 150, "latest": "2026-02-19T10:00:00Z" },
    { "_id": "robotics", "count": 80, "latest": "2026-02-19T09:30:00Z" }
  ]
}
```

### 获取简报详情

```
GET /briefs/:id
```

---

## 话题 API

### 获取热门话题

```
GET /topics/hot
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hours | number | 否 | 时间范围，默认 24 |
| limit | number | 否 | 返回数量，默认 10 |

### 获取话题详情

```
GET /topics/:id
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | number | 否 | 相关新闻数量，默认 20 |

---

## TTS API

### 获取可用音色

```
GET /tts/voices
```

### 合成语音

```
POST /tts/synthesize
Content-Type: application/json

{
  "text": "要合成的文本",
  "voice": "BV700_V2_streaming",
  "speed": 1.0,
  "volume": 1.0
}
```

**响应**: `audio/mpeg` 二进制数据

### 获取简报语音

```
GET /tts/brief/:id?voice=BV700_V2_streaming
```

**响应**: `audio/mpeg` 二进制数据

---

## 分类列表

| ID | 中文名 | 分组 |
|----|--------|------|
| ai_technology | AI技术 | 科技 |
| robotics | 机器人 | 科技 |
| ai_programming | AI编程 | 科技 |
| semiconductors | 芯片 | 科技 |
| automotive | 汽车 | 科技 |
| consumer_electronics | 消费电子 | 科技 |
| podcasts | 播客推荐 | 科技 |
| finance_investment | 投资财经 | 商业 |
| business_tech | 商业科技 | 商业 |
| politics_world | 政治国际 | 新闻 |
| economy_policy | 经济政策 | 新闻 |
| health_medical | 健康医疗 | 新闻 |
| energy_environment | 能源环境 | 新闻 |
| entertainment_sports | 娱乐体育 | 新闻 |
| anime | 动漫二次元 | 兴趣 |
| one_piece | OP | 兴趣 |
| tcg | TCG | 兴趣 |
| general | 综合 | 其他 |

---

## 错误响应

```json
{
  "success": false,
  "message": "错误描述"
}
```

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
