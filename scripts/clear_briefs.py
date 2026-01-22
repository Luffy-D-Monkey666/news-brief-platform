#!/usr/bin/env python3
"""清空 briefs 集合的脚本"""

from pymongo import MongoClient

# MongoDB 连接字符串
MONGODB_URI = "mongodb+srv://newsuser:16800958@cluster0.qrke26f.mongodb.net/news-brief?retryWrites=true&w=majority&appName=Cluster0"

def clear_briefs():
    """清空 briefs 集合"""
    try:
        # 连接 MongoDB
        client = MongoClient(MONGODB_URI)
        db = client['news-brief']
        briefs_collection = db['briefs']

        # 获取当前简报数量
        count_before = briefs_collection.count_documents({})
        print(f"清空前: {count_before} 条简报")

        # 清空集合
        result = briefs_collection.delete_many({})
        print(f"已删除: {result.deleted_count} 条简报")

        # 确认清空
        count_after = briefs_collection.count_documents({})
        print(f"清空后: {count_after} 条简报")

        client.close()
        print("\n✅ 数据库清空成功！")
        print("AI Service 将在下次运行时生成新的中文简报。")

    except Exception as e:
        print(f"❌ 清空失败: {str(e)}")

if __name__ == "__main__":
    confirm = input("确认要清空所有简报吗？(yes/no): ")
    if confirm.lower() == 'yes':
        clear_briefs()
    else:
        print("操作已取消")
