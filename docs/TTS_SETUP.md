# 火山引擎 TTS 部署指南

本项目使用**火山引擎豆包语音合成**提供高质量中文 TTS 服务，支持 30+ 音色。

## Step 1: 注册火山引擎账号

1. 打开 https://www.volcengine.com/
2. 点击右上角 **「注册」**
3. 支持手机号/邮箱注册，完成实名认证（需要身份证）

## Step 2: 开通语音合成服务

1. 登录后进入控制台：https://console.volcengine.com/
2. 在顶部搜索框搜索 **「语音技术」**，或直接访问：
   - https://console.volcengine.com/speech/app
3. 首次进入会提示 **「开通服务」**，点击开通（免费）
4. 阅读并同意服务协议

## Step 3: 购买资源包（可选但推荐）

> ⚠️ 不购买也可以使用，会按量后付费。购买资源包更便宜。

1. 进入 https://console.volcengine.com/speech/usage
2. 点击 **「购买资源包」**
3. 选择 **「语音合成」** 类型
4. 推荐购买：
   - **通用语音合成 - 100万字符包** ≈ ¥20（够用很久）
   - 或先用免费额度试用

## Step 4: 创建应用并获取凭证

1. 进入应用管理页面：https://console.volcengine.com/speech/app
2. 点击 **「创建应用」** 按钮
3. 填写信息：
   - **应用名称**: 如 `NewsHub-TTS`
   - **应用描述**: 如 `新闻语音播报`
   - **使用场景**: 选择 `语音合成`
4. 创建成功后，在应用列表点击应用名称进入详情
5. 记录以下信息：
   - **App ID**: 页面顶部显示，如 `6922135515`
6. 点击 **「生成 Token」** 按钮，复制生成的 **Access Token**

## Step 5: 配置环境变量

在 Backend 服务的环境变量中添加：

```bash
# 火山引擎 TTS 配置（必填）
VOLC_APP_ID=你的AppID（如 6922135515）
VOLC_ACCESS_TOKEN=你的AccessToken（很长的字符串）

# 可选配置（有默认值）
VOLC_CLUSTER=volcano_tts
```

**Render 部署配置方法**：
1. 打开 https://dashboard.render.com/
2. 点击你的 **Backend Service**（如 `news-backend`）
3. 左侧菜单选择 **「Environment」**
4. 在 **「Environment Variables」** 区域点击 **「Add Environment Variable」**
5. 分别添加 `VOLC_APP_ID` 和 `VOLC_ACCESS_TOKEN`
6. 点击 **「Save Changes」**，服务会自动重新部署

## Step 6: 验证配置

部署完成后，访问以下 URL 测试：

```
https://你的backend域名/api/tts/voices
```

如果返回音色列表 JSON，说明配置成功！

---

## 可用音色（30+）

| 分类 | 音色 | Voice ID |
|------|------|----------|
| **通用场景** | 灿灿 2.0 ⭐ | `BV700_V2_streaming` |
| | 炀炀 | `BV705_streaming` |
| | 擎苍 2.0 | `BV701_V2_streaming` |
| | 通用女声 | `BV001_streaming` |
| | 通用男声 | `BV002_streaming` |
| **超自然音色** | 梓梓 2.0 | `BV406_V2_streaming` |
| | 燃燃 2.0 | `BV407_V2_streaming` |
| **有声阅读** | 擎苍 | `BV701_streaming` |
| | 阳光青年 | `BV123_streaming` |
| | 古风少御 | `BV115_streaming` |
| | 儒雅青年 | `BV102_streaming` |
| | 温柔淑女 | `BV104_streaming` |
| **智能助手** | 甜美小源 | `BV405_streaming` |
| | 亲切女声 | `BV007_streaming` |
| | 知性女声 | `BV009_streaming` |
| **新闻播报** | 新闻女声 | `BV011_streaming` |
| | 新闻男声 | `BV012_streaming` |
| **视频配音** | 影视解说小帅 | `BV411_streaming` |
| | 影视解说小美 | `BV412_streaming` |
| **特色音色** | 奶气萌娃 | `BV051_streaming` |
| | 天才童声 | `BV061_streaming` |
| **英文** | Jackson (美式男) | `BV504_streaming` |
| | Ariana (美式女) | `BV503_streaming` |

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tts/voices` | GET | 获取可用音色列表 |
| `/api/tts/synthesize` | POST | 合成语音 (body: `{text, voice?}`) |
| `/api/tts/brief/:id` | GET | 获取指定新闻的语音 (query: `?voice=xxx`) |

## 计费说明

- **计费单位**: 按字符数计费
- **价格**: 约 0.2 元 / 万字符（具体以官网为准）
- **免费额度**: 新用户有一定免费额度
- **缓存机制**: 系统内置 30 分钟音频缓存，减少重复调用

## 常见问题

**Q: 提示 "未配置 Access Token"？**
A: 检查环境变量 `VOLC_ACCESS_TOKEN` 是否正确设置。

**Q: 提示 "错误码 xxxx"？**
A: 参考[火山引擎错误码文档](https://www.volcengine.com/docs/6561/79820)排查。

**Q: 音频播放卡顿？**
A: 首次合成需要 1-2 秒，后续会命中缓存。检查网络状况。
