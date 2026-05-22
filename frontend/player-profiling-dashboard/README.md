# Frontend Dashboard

D 块可视化系统开发目录。

当前版本已经实现：

- 球员多维能力雷达图
- 风格空间散点图
- 球员对比视图
- 表现趋势折线图
- 可解释性特征贡献图
- 相似球员推荐列表
- 可搜索球员选择框
- 左侧目录点击聚焦模块

## 访问方式

启动后端后访问：

```text
http://127.0.0.1:8000/dashboard
```

该前端由 FastAPI 静态托管，不需要单独运行 npm。

## 后端联调地址

本地后端默认地址：

```text
http://127.0.0.1:8000
```

优先使用聚合接口：

```text
GET /api/v1/players/{player_id}/profile
GET /api/v1/players/{player_id}/dashboard
GET /api/v1/players/compare?player1=curryst01&player2=gilgesh01
```
