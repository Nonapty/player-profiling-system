# Player Profiling System

全球球星数据可视化与运动员个体表现画像系统。

本项目面向体育分析场景，将球员基础数据、能力特征、AI 分析结果和交互式可视化整合为一个完整系统，支持球员画像、风格聚类、相似球员推荐、趋势分析和可解释性分析。

## 项目目标

将抽象的球员能力转化为可解释、可比较、可交互展示的数据可视化系统。

核心能力：

- 多维球员能力画像
- 球员风格空间与聚类分析
- 球员对比分析
- 时间序列表现趋势
- 相似球员推荐
- AI 评分解释性展示

## 团队分工

| 模块 | 负责人方向 | 目录 |
|---|---|---|
| A | 数据处理与数据工程 | `data/` |
| B | 特征工程与球员能力建模 | `models/feature_engineering/` |
| C | AI 分析与建模 | `models/ml_analytics/` |
| D | 可视化系统开发 | `frontend/player-profiling-dashboard/` |
| E | 系统集成与性能优化 | `backend/player-profiling-api/`, `deployment/`, `docs/engineering/` |

## 项目结构

```text
player-profiling-system/
├── README.md
├── .gitignore
├── backend/
│   └── player-profiling-api/
├── frontend/
│   └── player-profiling-dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── feature_engineering/
│   └── ml_analytics/
├── deployment/
└── docs/
    ├── project/
    └── engineering/
```

## 快速启动后端 API

```bash
cd backend/player-profiling-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

访问：

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/v1/health
- 示例画像：http://127.0.0.1:8000/api/v1/players/curryst01/profile
- 可视化工作台：http://127.0.0.1:8000/dashboard

## 完整分析流水线

当前项目包含一条轻量的本地分析流水线，用于表达“数据清洗 → 特征工程 → AI分析 → 可视化”的完整过程：

```bash
python3 data/scripts/clean_players.py
python3 models/feature_engineering/build_features.py
python3 models/ml_analytics/run_analysis.py
```

运行后会生成：

- `data/processed/players.json`
- `models/feature_engineering/feature_vectors.json`
- `models/ml_analytics/analytics_results.json`

后端会优先读取 `models/ml_analytics/output/analytics_bundle.json`；如果不存在，再读取 `models/ml_analytics/analytics_results.json`。

当前展示版已经接入真实数据产物：

- 100 名 NBA 2024-25 赛季球员
- `data/processed/players.json`
- `models/feature_engineering/output/feature_vectors.json`
- `models/ml_analytics/output/analytics_bundle.json`

健康检查应显示 `real_players: 100` 和 `analytics_source: pipeline`。

详细说明见：

- [Pipeline Guide](docs/engineering/PIPELINE_GUIDE.md)

## 当前可展示版本

当前版本已经包含一个可直接展示的可视化 Dashboard：

- 可搜索的球员选择与全局对比选择
- 多维能力雷达图
- 近期表现趋势图
- 可点击切换球员的风格空间散点图
- 相似球员推荐
- 可解释性贡献条形图
- 球员差异对比

前端目录：

```text
frontend/player-profiling-dashboard/
```

后端会通过 `/dashboard` 提供该页面，不需要单独启动前端服务。

课堂展示可参考：

- [Seminar Demo Guide](docs/engineering/DEMO_GUIDE.md)

## 测试

先启动后端：

```bash
cd backend/player-profiling-api
uvicorn main:app --reload
```

另开一个终端，在同一目录运行：

```bash
python3 tests/smoke_test.py
```

## Docker 启动

在项目根目录执行：

```bash
docker compose -f deployment/docker-compose.yml up --build
```

Docker 镜像会从项目根目录构建，以便容器内同时包含后端、前端、真实数据和模型产物。

## 文档索引

- 项目需求：[docs/project/VR.md](docs/project/VR.md)
- 团队分工：[docs/project/分工.md](docs/project/分工.md)
- 数据契约：[docs/project/Data Contract Table.md](docs/project/Data%20Contract%20Table.md)
- API 契约：[docs/project/api.yaml](docs/project/api.yaml)
- E 块集成说明：[docs/engineering/E_BLOCK_INTEGRATION.md](docs/engineering/E_BLOCK_INTEGRATION.md)
- 展示指南：[docs/engineering/DEMO_GUIDE.md](docs/engineering/DEMO_GUIDE.md)
- 流水线说明：[docs/engineering/PIPELINE_GUIDE.md](docs/engineering/PIPELINE_GUIDE.md)
- 性能优化报告：[docs/engineering/PERFORMANCE_OPTIMIZATION.md](docs/engineering/PERFORMANCE_OPTIMIZATION.md)
- 部署说明：[docs/engineering/DEPLOYMENT.md](docs/engineering/DEPLOYMENT.md)
- GitHub 使用指南：[docs/engineering/GITHUB_GUIDE.md](docs/engineering/GITHUB_GUIDE.md)

## GitHub 首次上传

```bash
git init
git add .
git commit -m "Initial team project structure"
git branch -M main
git remote add origin https://github.com/你的用户名/player-profiling-system.git
git push -u origin main
```
