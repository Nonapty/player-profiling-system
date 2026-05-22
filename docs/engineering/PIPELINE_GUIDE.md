# Data-to-Visualization Pipeline

本项目的完整预期流程是：

```text
数据获取 → 数据清洗 → 特征工程 → AI分析与建模 → 后端API → 前端可视化
```

当前版本为了课堂展示，使用一条轻量的本地流水线模拟完整过程。

## 1. 数据清洗

输入：

```text
data/raw/player_stats.sample.csv
```

运行：

```bash
python3 data/scripts/clean_players.py
```

输出：

```text
data/processed/players.json
```

清洗内容：

- 去除字符串空格
- 数值字段类型转换
- 将技术统计整理到 `stats`
- 根据简单规则推断球员风格标签

## 2. 特征工程

输入：

```text
data/processed/players.json
```

运行：

```bash
python3 models/feature_engineering/build_features.py
```

输出：

```text
models/feature_engineering/feature_vectors.json
```

特征维度：

- Scoring
- Playmaking
- Rebounding
- Efficiency
- Defense

当前采用规则化归一化方式，作为 seminar prototype。后续可以替换为更正式的特征工程与标准化 pipeline。

## 3. AI分析与建模

输入：

```text
models/feature_engineering/feature_vectors.json
```

运行：

```bash
python3 models/ml_analytics/run_analysis.py
```

输出：

```text
models/ml_analytics/analytics_results.json
```

当前分析内容：

- 球员 embedding
- 风格聚类
- KNN-style 相似球员推荐
- 近期趋势模拟
- 特征贡献解释
- 二维风格空间投影

## 4. 后端读取

后端会优先读取：

```text
models/ml_analytics/output/analytics_bundle.json
```

并读取：

```text
models/feature_engineering/output/feature_vectors.json
```

如果 `output/` 下的真实分析产物不存在，则回退到本项目原有的轻量产物或服务层运行时计算逻辑。

## 5. 当前真实数据集

当前项目已接入 `Tianyidiyi/player-profiling-system` 中的标准数据：

- 数据来源：Basketball-Reference 2024-25 NBA Per Game
- 球员数量：100
- 标准球员文件：`data/processed/players.json`
- 特征工程产物：`models/feature_engineering/output/feature_vectors.json`
- AI 分析产物：`models/ml_analytics/output/analytics_bundle.json`

后端健康检查中应显示：

```json
{
  "real_players": 100,
  "active_source": "real",
  "analytics_source": "pipeline"
}
```

## 6. 前端展示

启动后端：

```bash
cd backend/player-profiling-api
uvicorn main:app --reload
```

打开：

```text
http://127.0.0.1:8000/dashboard
```

## 7. 一次性运行完整流水线

在项目根目录执行：

```bash
python3 data/scripts/clean_players.py
python3 models/feature_engineering/build_features.py
python3 models/ml_analytics/run_analysis.py
```

然后重启后端或刷新页面。
