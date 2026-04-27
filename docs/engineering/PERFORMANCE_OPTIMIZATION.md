# 性能优化报告模板

## 1. 优化目标

系统集成阶段主要关注：

- 减少前端请求次数
- 降低接口响应延迟
- 避免重复计算模型结果
- 保证可视化页面加载稳定

## 2. 当前优化点

### 聚合接口

前端 Dashboard 不需要分别请求 trend、similarity、explanation，可以直接请求：

```text
GET /api/v1/players/{player_id}/dashboard
```

球员完整画像可以请求：

```text
GET /api/v1/players/{player_id}/profile
```

### Mock / Real 数据切换

`DataSwitcher` 支持真实数据优先，mock 数据兜底，便于联调早期不依赖完整数据库。

### 健康检查

`/api/v1/health` 可用于部署平台、前端联调和自动化监控。

## 3. 后续可扩展优化

- 对 `features`、`embedding`、`cluster` 等稳定结果增加缓存
- 对相似度计算使用预计算矩阵
- 对大规模球员列表增加分页
- 对前端静态资源启用 gzip / brotli
- 使用 Nginx 做反向代理和静态缓存
- 使用性能测试工具记录平均响应时间、P95、P99

## 4. 建议测试指标

| 指标 | 目标 |
|---|---|
| 健康检查响应时间 | < 50ms |
| 单个原子接口响应时间 | < 100ms |
| Dashboard 聚合接口响应时间 | < 300ms |
| 404 错误处理 | 稳定返回 |
| 前端首屏数据请求数 | 尽量 <= 3 |

## 5. 示例测试命令

```bash
curl -s http://127.0.0.1:8000/api/v1/health
curl -s http://127.0.0.1:8000/api/v1/players/123/profile
curl -s "http://127.0.0.1:8000/api/v1/players/compare?player1=123&player2=456"
```
