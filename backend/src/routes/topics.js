const express = require('express');
const router = express.Router();
const { ObjectId } = require('mongodb');

// 获取热门话题
router.get('/hot', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const hours = parseInt(req.query.hours) || 24;
    const limit = parseInt(req.query.limit) || 10;
    
    const cutoffTime = new Date(Date.now() - hours * 60 * 60 * 1000);
    
    const topics = await db.collection('topics')
      .find({
        is_active: true,
        updated_at: { $gte: cutoffTime },
        brief_count: { $gte: 2 }  // 至少2条新闻
      })
      .sort({ brief_count: -1 })
      .limit(limit)
      .toArray();
    
    res.json({
      success: true,
      count: topics.length,
      data: topics.map(t => ({
        ...t,
        _id: t._id.toString()
      }))
    });
  } catch (error) {
    console.error('获取热门话题失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取话题详情及相关新闻
router.get('/:id', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const topicId = req.params.id;
    const limit = parseInt(req.query.limit) || 20;
    
    // 获取话题信息
    const topic = await db.collection('topics').findOne({
      _id: new ObjectId(topicId)
    });
    
    if (!topic) {
      return res.status(404).json({ success: false, error: '话题不存在' });
    }
    
    // 获取话题下的新闻
    const briefs = await db.collection('briefs')
      .find({ topic_id: topicId })
      .sort({ created_at: -1 })
      .limit(limit)
      .toArray();
    
    res.json({
      success: true,
      data: {
        topic: {
          ...topic,
          _id: topic._id.toString()
        },
        briefs: briefs.map(b => ({
          ...b,
          _id: b._id.toString()
        }))
      }
    });
  } catch (error) {
    console.error('获取话题详情失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取所有活跃话题
router.get('/', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const category = req.query.category;
    const limit = parseInt(req.query.limit) || 50;
    
    const query = { is_active: true };
    if (category) {
      query.category = category;
    }
    
    const topics = await db.collection('topics')
      .find(query)
      .sort({ updated_at: -1 })
      .limit(limit)
      .toArray();
    
    res.json({
      success: true,
      count: topics.length,
      data: topics.map(t => ({
        ...t,
        _id: t._id.toString()
      }))
    });
  } catch (error) {
    console.error('获取话题列表失败:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
