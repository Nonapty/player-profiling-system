# Frontend Dashboard

D 块可视化系统开发目录。

建议实现内容：

- 球员多维能力雷达图
- 风格空间散点图
- 球员对比视图
- 表现趋势折线图
- 相似球员网络图
- 可解释性特征贡献图

## 后端联调地址

本地后端默认地址：

```text
http://127.0.0.1:8000
```

优先使用聚合接口：

```text
GET /api/v1/players/{player_id}/profile
GET /api/v1/players/{player_id}/dashboard
GET /api/v1/players/compare?player1=123&player2=456
```
