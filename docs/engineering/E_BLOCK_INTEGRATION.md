# E 块：系统集成与模块联调说明

## 1. 职责范围

E 块负责把 A/B/C/D 四个模块整合成可运行系统：

- A 数据层：提供球员基础数据与统计数据
- B 特征工程：输出能力特征向量
- C AI 分析：输出聚类、相似度、趋势、解释性分析
- D 可视化层：消费 API 并渲染 Dashboard
- E 集成层：统一接口、统一响应、健康检查、部署与性能优化

## 2. 当前工程骨架

```text
frontend/player-profiling-dashboard
        |
        v
backend/player-profiling-api/api_main.py
        |
        v
backend/player-profiling-api/services/integration_service.py
        |
        +--> player_service.py -> DataSwitcher -> mock/real data
        |
        +--> ml_service.py -> features / embedding / cluster / similarity / trend / explanation
```

## 3. 模块接入规则

### 数据模块接入

A 组处理后的数据放在：

```text
data/processed/
```

推荐文件名：

```text
data/processed/players.json
```

或：

```text
data/processed/players.csv
```

后端真实数据读取逻辑接入：

```text
backend/player-profiling-api/data/real_db.py
```

如果真实数据不可用，系统会 fallback 到：

```text
backend/player-profiling-api/data/mock_db.py
```

### 特征工程模块接入

B 组代码放在：

```text
models/feature_engineering/
```

稳定输出应同步到后端：

```text
backend/player-profiling-api/services/ml_service.py
```

### AI 模块接入

C 组代码放在：

```text
models/ml_analytics/
```

后端服务层应保持以下函数名稳定：

- `get_features(player_id)`
- `get_embedding(player_id)`
- `get_cluster(player_id)`
- `get_similarity(player_id, top_k=5)`
- `get_trend(player_id)`
- `get_explanation(player_id)`
- `compare_players(p1, p2)`

### 可视化模块接入

D 组前端目录：

```text
frontend/player-profiling-dashboard/
```

前端优先使用聚合接口，减少多次请求：

- `/api/v1/players/{player_id}/profile`
- `/api/v1/players/{player_id}/dashboard`
- `/api/v1/players/compare?player1=123&player2=456`

## 4. 统一响应格式

所有成功响应统一为：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

前端读取业务字段时统一从 `response.data.data` 开始。

## 5. 联调检查清单

- 后端服务可以启动：`cd backend/player-profiling-api && uvicorn main:app --reload`
- `/api/v1/health` 返回 `status=ok`
- mock 球员 `123` 能返回完整 profile
- mock 球员 `456` 能参与 compare
- 不存在的球员返回 404
- 前端只依赖 `/api/v1` 下的接口
- 新模型输出必须先更新 `docs/project/Data Contract Table.md`
- 真实数据文件存在时，`/api/v1/health` 中 `data_source.active_source` 应为 `real`
