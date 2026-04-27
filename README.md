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
- 示例画像：http://127.0.0.1:8000/api/v1/players/123/profile

## Docker 启动

在项目根目录执行：

```bash
docker compose -f deployment/docker-compose.yml up --build
```

## 文档索引

- 项目需求：[docs/project/VR.md](docs/project/VR.md)
- 团队分工：[docs/project/分工.md](docs/project/分工.md)
- 数据契约：[docs/project/Data Contract Table.md](docs/project/Data%20Contract%20Table.md)
- API 契约：[docs/project/api.yaml](docs/project/api.yaml)
- E 块集成说明：[docs/engineering/E_BLOCK_INTEGRATION.md](docs/engineering/E_BLOCK_INTEGRATION.md)
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
