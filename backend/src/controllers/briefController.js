const Brief = require('../models/Brief');

// 获取最新简报
exports.getLatestBriefs = async (req, res) => {
  try {
    const { category, limit = 20 } = req.query;

    const query = {};
    if (category) {
      query.category = category;
    }

    const briefs = await Brief.find(query)
      .sort({ created_at: -1 })
      .limit(parseInt(limit, 10));

    res.json({
      success: true,
      count: briefs.length,
      data: briefs
    });
  } catch (error) {
    console.error('获取简报失败:', error);
    res.status(500).json({
      success: false,
      message: '获取简报失败'
    });
  }
};

// 获取历史简报（分页）
exports.getHistoryBriefs = async (req, res) => {
  try {
    const { category, page = 1, limit = 20 } = req.query;
    const skip = (parseInt(page, 10) - 1) * parseInt(limit, 10);

    const query = {};
    if (category) {
      query.category = category;
    }

    const briefs = await Brief.find(query)
      .sort({ created_at: -1 })
      .skip(skip)
      .limit(parseInt(limit, 10));

    const total = await Brief.countDocuments(query);

    res.json({
      success: true,
      data: briefs,
      pagination: {
        page: parseInt(page, 10),
        limit: parseInt(limit, 10),
        total,
        pages: Math.ceil(total / parseInt(limit, 10))
      }
    });
  } catch (error) {
    console.error('获取历史简报失败:', error);
    res.status(500).json({
      success: false,
      message: '获取历史简报失败'
    });
  }
};

// 获取分类统计
exports.getCategoryStats = async (req, res) => {
  try {
    const stats = await Brief.aggregate([
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 },
          latest: { $max: '$created_at' }
        }
      },
      {
        $sort: { count: -1 }
      }
    ]);

    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    console.error('获取统计失败:', error);
    res.status(500).json({
      success: false,
      message: '获取统计失败'
    });
  }
};

// 根据ID获取简报详情
exports.getBriefById = async (req, res) => {
  try {
    const { id } = req.params;
    const brief = await Brief.findById(id);

    if (!brief) {
      return res.status(404).json({
        success: false,
        message: '简报不存在'
      });
    }

    res.json({
      success: true,
      data: brief
    });
  } catch (error) {
    console.error('获取简报详情失败:', error);
    res.status(500).json({
      success: false,
      message: '获取简报详情失败'
    });
  }
};
