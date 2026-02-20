const express = require('express');
const router = express.Router();
const Entity = require('../models/Entity');
const EntityNews = require('../models/EntityNews');
const Brief = require('../models/Brief');

// GET /api/entities - 获取实体列表
router.get('/', async (req, res) => {
  try {
    const {
      type,           // 实体类型筛选
      search,         // 搜索关键词
      sort = 'news',  // 排序: news(新闻数) | recent(最近更新) | name(名称)
      limit = 20,
      offset = 0
    } = req.query;

    const query = {};
    
    // 类型筛选
    if (type && ['company', 'person', 'event', 'concept', 'product'].includes(type)) {
      query.type = type;
    }
    
    // 搜索
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { aliases: { $regex: search, $options: 'i' } }
      ];
    }

    // 排序
    let sortOption = {};
    switch (sort) {
      case 'recent':
        sortOption = { last_news_at: -1, news_count: -1 };
        break;
      case 'name':
        sortOption = { name: 1 };
        break;
      case 'news':
      default:
        sortOption = { news_count: -1, last_news_at: -1 };
    }

    const [entities, total] = await Promise.all([
      Entity.find(query)
        .sort(sortOption)
        .skip(parseInt(offset))
        .limit(parseInt(limit))
        .select('-base_timeline'),  // 列表不返回时间线
      Entity.countDocuments(query)
    ]);

    res.json({
      success: true,
      data: entities,
      pagination: {
        total,
        limit: parseInt(limit),
        offset: parseInt(offset)
      }
    });
  } catch (error) {
    console.error('获取实体列表失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// GET /api/entities/search/:name - 按名称精确查找实体（必须在 /:id 前）
router.get('/search/:name', async (req, res) => {
  try {
    const name = decodeURIComponent(req.params.name);
    
    // 先精确匹配，再匹配别名
    let entity = await Entity.findOne({ name });
    if (!entity) {
      entity = await Entity.findOne({ aliases: name });
    }

    if (!entity) {
      return res.json({ success: true, data: null });
    }

    res.json({ success: true, data: entity });
  } catch (error) {
    console.error('搜索实体失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// GET /api/entities/:id - 获取实体详情
router.get('/:id', async (req, res) => {
  try {
    const entity = await Entity.findById(req.params.id);
    
    if (!entity) {
      return res.status(404).json({ success: false, error: '实体不存在' });
    }

    res.json({ success: true, data: entity });
  } catch (error) {
    console.error('获取实体详情失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// GET /api/entities/:id/timeline - 获取实体时间轴（含新闻）
router.get('/:id/timeline', async (req, res) => {
  try {
    const { limit = 50, before } = req.query;
    
    const entity = await Entity.findById(req.params.id);
    if (!entity) {
      return res.status(404).json({ success: false, error: '实体不存在' });
    }

    // 查询关联新闻
    const newsQuery = { entity_id: entity._id };
    if (before) {
      newsQuery.date = { $lt: before };
    }

    const entityNews = await EntityNews.find(newsQuery)
      .sort({ date: -1 })
      .limit(parseInt(limit))
      .populate('brief_id', 'title category link image created_at importance summary');

    // 按日期分组新闻
    const newsGrouped = {};
    entityNews.forEach(en => {
      if (!newsGrouped[en.date]) {
        newsGrouped[en.date] = [];
      }
      if (en.brief_id) {  // 确保brief存在
        newsGrouped[en.date].push({
          brief_id: en.brief_id._id,
          title: en.brief_id.title,
          category: en.brief_id.category,
          link: en.brief_id.link,
          image: en.brief_id.image,
          importance: en.brief_id.importance,
          relevance: en.relevance,
          created_at: en.brief_id.created_at,
          summary: en.brief_id.summary
        });
      }
    });

    // 合并基础时间线和新闻时间线
    const timeline = [];
    
    // 添加新闻节点
    Object.entries(newsGrouped).forEach(([date, news]) => {
      timeline.push({
        date,
        type: 'news',
        items: news
      });
    });
    
    // 添加基础历史节点
    entity.base_timeline.forEach(item => {
      timeline.push({
        date: item.date,
        type: 'milestone',
        event: item.event,
        importance: item.importance
      });
    });

    // 按日期排序（新的在前）
    timeline.sort((a, b) => {
      // 标准化日期格式用于比较
      const dateA = a.date.replace(/\./g, '-').padEnd(10, '-01');
      const dateB = b.date.replace(/\./g, '-').padEnd(10, '-01');
      return dateB.localeCompare(dateA);
    });

    res.json({
      success: true,
      data: {
        entity: {
          _id: entity._id,
          name: entity.name,
          type: entity.type,
          description: entity.description,
          image: entity.image,
          metadata: entity.metadata,
          news_count: entity.news_count
        },
        timeline
      }
    });
  } catch (error) {
    console.error('获取实体时间轴失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /api/entities - 创建新实体（内部使用）
router.post('/', async (req, res) => {
  try {
    const { name, aliases, type, description, image, metadata, base_timeline, is_preset } = req.body;

    if (!name || !type) {
      return res.status(400).json({ success: false, error: '缺少必要字段' });
    }

    // 检查是否已存在
    const existing = await Entity.findOne({
      $or: [{ name }, { aliases: name }]
    });
    if (existing) {
      return res.status(409).json({ success: false, error: '实体已存在', data: existing });
    }

    const entity = new Entity({
      name,
      aliases: aliases || [],
      type,
      description: description || '',
      image: image || null,
      metadata: metadata || {},
      base_timeline: base_timeline || [],
      is_preset: is_preset || false
    });

    await entity.save();
    res.status(201).json({ success: true, data: entity });
  } catch (error) {
    console.error('创建实体失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /api/entities/mention - 增加实体提及计数（用于阈值判断）
router.post('/mention', async (req, res) => {
  try {
    const { name, type, context } = req.body;
    
    if (!name) {
      return res.status(400).json({ success: false, error: '缺少实体名称' });
    }

    // 查找或创建"待激活"实体记录
    let entity = await Entity.findOne({
      $or: [{ name }, { aliases: name }]
    });

    if (entity) {
      // 已存在，增加提及计数
      entity.mention_count = (entity.mention_count || 0) + 1;
      await entity.save();
      
      return res.json({
        success: true,
        data: entity,
        action: 'incremented',
        mention_count: entity.mention_count
      });
    }

    // 不存在，创建新的（未激活状态，news_count=0）
    entity = new Entity({
      name,
      type: type || 'concept',
      description: context || '',
      aliases: [],
      base_timeline: [],
      mention_count: 1,
      news_count: 0  // 未激活时不关联新闻
    });
    await entity.save();

    res.status(201).json({
      success: true,
      data: entity,
      action: 'created',
      mention_count: 1
    });
  } catch (error) {
    console.error('记录实体提及失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /api/entities/:id/activate - 激活实体（达到阈值后调用）
router.post('/:id/activate', async (req, res) => {
  try {
    const { base_timeline, description } = req.body;

    const entity = await Entity.findById(req.params.id);
    if (!entity) {
      return res.status(404).json({ success: false, error: '实体不存在' });
    }

    // 更新基础时间轴和描述
    if (base_timeline && base_timeline.length > 0) {
      entity.base_timeline = base_timeline;
    }
    if (description) {
      entity.description = description;
    }
    entity.is_preset = false;  // 标记为非预置（AI生成）
    await entity.save();

    res.json({ success: true, data: entity });
  } catch (error) {
    console.error('激活实体失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /api/entities/:id/link-news - 关联新闻到实体
router.post('/:id/link-news', async (req, res) => {
  try {
    const { brief_id, date, category, relevance } = req.body;

    const entity = await Entity.findById(req.params.id);
    if (!entity) {
      return res.status(404).json({ success: false, error: '实体不存在' });
    }

    // 检查是否已关联
    const existing = await EntityNews.findOne({
      entity_id: entity._id,
      brief_id
    });
    if (existing) {
      return res.json({ success: true, data: existing, message: '已关联' });
    }

    // 创建关联
    const entityNews = new EntityNews({
      entity_id: entity._id,
      brief_id,
      date,
      category,
      relevance: relevance || ''
    });
    await entityNews.save();

    // 更新实体统计
    await Entity.findByIdAndUpdate(entity._id, {
      $inc: { news_count: 1 },
      last_news_at: new Date()
    });

    res.status(201).json({ success: true, data: entityNews });
  } catch (error) {
    console.error('关联新闻失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
