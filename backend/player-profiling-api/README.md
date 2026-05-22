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
| `GET /api/v1/players/compare?player1=curryst01&player2=gilgesh01` | 球员对比 |

## 模块接入点

- 数据源接入：`data/real_db.py`
- mock 数据：`data/mock_db.py`
- AI/模型结果接入：`services/ml_service.py`
- 统一联调层：`services/integration_service.py`
- API 路由层：`api_main.py`

## 真实数据读取规则

后端会优先读取整体项目根目录下的真实数据：

```text
../../data/processed/players.json
```

如果不存在，则读取：

```text
../../data/processed/players.csv
```

如果真实数据文件都不存在，则 fallback 到：

```text
data/mock_db.py
```

临时指定其他数据文件时，可以使用环境变量：

```bash
PLAYERS_DATA_PATH=data/processed/players.sample.json uvicorn main:app --reload
```

健康检查接口会显示当前数据源状态：

```text
GET /api/v1/health
```
