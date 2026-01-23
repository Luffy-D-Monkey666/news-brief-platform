# DeepSeek AI 配置指南（中国国内AI服务）

## 💰 为什么选择DeepSeek？

- ✅ **超便宜**: ¥0.001/千tokens（输入），¥0.002/千tokens（输出）
- ✅ **质量好**: 接近GPT-4水平的中文能力
- ✅ **国内支付**: 支持支付宝、微信支付
- ✅ **无需魔法**: 国内可直接访问
- ✅ **API兼容**: 完全兼容OpenAI格式

**价格对比**:
- OpenAI GPT-3.5: $0.50/1M tokens (约¥3.5/百万tokens)
- DeepSeek: ¥1/百万tokens
- **DeepSeek便宜350倍！**

---

## 📝 注册步骤

### 1. 访问DeepSeek官网
打开浏览器访问：**https://platform.deepseek.com**

### 2. 注册账号
1. 点击右上角 **"登录/注册"**
2. 使用手机号注册
3. 输入验证码
4. 设置密码

### 3. 充值（最低¥1起）
1. 登录后进入 **"账户"** → **"充值"**
2. 选择充值金额（建议先充¥10-20测试）
3. 使用支付宝或微信支付
4. 充值秒到账

### 4. 创建API Key
1. 进入 **"API Keys"** 页面
2. 点击 **"创建新密钥"**
3. 填写密钥名称：`NewsHub-Service`
4. 点击创建
5. **立即复制API Key**（格式：`sk-xxxxxxxxxxxxx`）
   ⚠️ 只显示一次，务必保存！

---

## 🔧 配置到Render

### 步骤1: 登录Render
访问：https://dashboard.render.com

### 步骤2: 配置环境变量
1. 点击 `news-ai-service`
2. 点击左侧 **"Environment"**
3. 修改现有的 `AI_PROVIDER`：
   - 将值从 `huggingface` 改为 `deepseek`
4. 添加新的环境变量：
   - **Key**: `DEEPSEEK_API_KEY`
   - **Value**: 粘贴你刚才复制的API Key
5. 点击 **"Save Changes"**

### 步骤3: 触发重新部署
1. 点击右上角 **"Manual Deploy"** → **"Deploy latest commit"**
2. 等待3-5分钟部署完成

---

## ✅ 验证配置

### 1. 查看部署日志
部署完成后，点击 **"Logs"**，应该看到：
```
使用DeepSeek AI（中国）
执行首次采集...
爬取到 187 条新闻
过滤后剩余 187 条新新闻
开始AI处理...
处理完成: [ai_robotics] OpenAI发布GPT-5模型...
处理完成: [politics_world] 英国首相宣布新政策...
成功保存 XXX 条简报
```

### 2. 检查数据库
大约10-15分钟后，运行：
```python
python3 -c "
from pymongo import MongoClient
client = MongoClient('mongodb+srv://newsuser:16800958@cluster0.qrke26f.mongodb.net/news-brief?retryWrites=true&w=majority&appName=Cluster0')
db = client['news-brief']
count = db['briefs'].count_documents({})
print(f'简报数量: {count}')
latest = db['briefs'].find_one({}, sort=[('created_at', -1)])
if latest:
    print(f'最新标题: {latest[\"title\"]}')
    print(f'摘要: {latest[\"summary\"][:100]}...')
"
```

### 3. 访问前端网站
打开：https://news-frontend-e14o.onrender.com

应该能看到中文新闻简报了！

---

## 💡 费用估算

### 你的使用场景：
- 44个新闻源
- 每5分钟爬取一次
- 每次约处理150-200条新闻
- 每天约5000-7000条新闻

### 费用计算：
```
每条新闻处理：
- 输入：约500 tokens（标题+内容）→ ¥0.0005
- 输出：约200 tokens（中文摘要）→ ¥0.0004
- 分类：约100 tokens → ¥0.0002
- 总计：约¥0.001/条

每天费用：
6000条 × ¥0.001 = ¥6/天

每月费用：
¥6 × 30 = ¥180/月
```

**实际可能更便宜**，因为：
- 很多新闻会被去重过滤
- 实际处理量可能更少

**建议**: 先充值¥20测试一周，看实际消耗

---

## 🆚 其他国内AI选择

如果DeepSeek有问题，可以考虑：

### 1. 阿里云百炼（通义千问）
- 官网：https://bailian.console.aliyun.com
- 价格：类似DeepSeek
- 需要：阿里云账号

### 2. 腾讯混元
- 官网：https://cloud.tencent.com/product/hunyuan
- 价格：略贵
- 需要：腾讯云账号

### 3. 智谱AI（ChatGLM）
- 官网：https://open.bigmodel.cn
- 价格：中等
- 质量：不错

**如需添加其他AI支持，告诉我即可！**

---

## ⚠️ 常见问题

### Q: API Key在哪里查看？
A: 登录后点击左侧 "API Keys"，但已创建的key无法再次查看，只能创建新的。

### Q: 充值最低多少？
A: ¥1起充，支持支付宝/微信。

### Q: 如何查看消费？
A: 登录后点击 "用量统计" 可以看到每天的token消耗和费用。

### Q: API会被墙吗？
A: DeepSeek的API地址(api.deepseek.com)在国内可直接访问，不需要魔法。

### Q: Render能访问DeepSeek吗？
A: 可以！Render在美国，但DeepSeek的API全球可访问。

---

## 📞 需要帮助？

如果遇到问题：
1. 检查API Key是否正确复制
2. 检查Render环境变量是否正确配置
3. 查看Render的Logs标签，找错误信息
4. 截图发给我，我会帮你诊断

---

**当前状态**: ✅ 代码已更新，支持DeepSeek
**下一步**: 注册DeepSeek → 获取API Key → 配置到Render → 等待15分钟看效果

祝你成功！🎉
