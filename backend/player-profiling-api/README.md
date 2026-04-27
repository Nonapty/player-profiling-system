# Player Profiling API

该目录是完整小组项目的后端 API 模块，由 E 块负责工程整合、接口统一、性能优化和模块联调。

## 本地运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 关键接口

| 接口 | 说明 |
|---|---|
| `GET /api/v1/health` | 服务健康检查 |
| `GET /api/v1/players/{player_id}` | 球员基础数据 |
| `GET /api/v1/players/{player_id}/profile` | 球员完整画像聚合数据 |
| `GET /api/v1/players/{player_id}/dashboard` | 前端 Dashboard 聚合数据 |
| `GET /api/v1/players/compare?player1=123&player2=456` | 球员对比 |

## 模块接入点

- 数据源接入：`data/real_db.py`
- mock 数据：`data/mock_db.py`
- AI/模型结果接入：`services/ml_service.py`
- 统一联调层：`services/integration_service.py`
- API 路由层：`api_main.py`
