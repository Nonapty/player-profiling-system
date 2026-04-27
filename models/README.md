# Models

B/C 两个建模模块目录。

- `feature_engineering/`：B 块，特征工程与球员能力建模
- `ml_analytics/`：C 块，AI 分析、聚类、相似度、趋势和解释性分析

模型输出应通过后端 `backend/player-profiling-api/services/ml_service.py` 接入统一 API。
