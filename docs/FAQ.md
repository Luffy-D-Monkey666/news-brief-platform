# 🐛 常见问题 (FAQ)

## AI Service 长时间没有新新闻
- Render 免费版 Worker 会休眠，访问前端会自动唤醒
- 检查 Render Dashboard → AI Service → Logs

## 简报只显示一句话
- 只有新抓取的新闻才会用新格式
- 旧数据需要等待新新闻自动进入

## 话题视图为空
- 话题需要同一事件≥2篇报道才会形成
- 新部署后需要等待数据积累

## 语音播放没声音
- 当前使用浏览器原生TTS，需要浏览器支持
- 火山引擎云端TTS正在开发中

## 502 Bad Gateway
- Render 免费版首次启动慢，等待 2-3 分钟

## 数据库连接失败
- 检查 `MONGODB_URI` 环境变量格式
- 确认 MongoDB Atlas 允许当前 IP 访问
