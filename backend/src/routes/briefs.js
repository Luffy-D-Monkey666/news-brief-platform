const express = require('express');
const router = express.Router();
const briefController = require('../controllers/briefController');

// 获取最新简报
router.get('/latest', briefController.getLatestBriefs);

// 获取历史简报（分页）
router.get('/history', briefController.getHistoryBriefs);

// 获取分类统计
router.get('/stats', briefController.getCategoryStats);

// 获取简报详情
router.get('/:id', briefController.getBriefById);

module.exports = router;
