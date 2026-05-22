# Seminar Demo Guide

这份文档用于课堂展示或小组汇报时快速演示当前系统。

## 1. 启动方式

在项目根目录执行：

```bash
cd backend/player-profiling-api
source .venv/bin/activate
uvicorn main:app --reload
```

如果还没有安装依赖，先执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 展示入口

浏览器打开：

```text
http://127.0.0.1:8000/dashboard
```

API 文档入口：

```text
http://127.0.0.1:8000/docs
```

## 3. 推荐展示顺序

### Step 1：展示总览

打开 `/dashboard` 后先说明：

- 左侧可以选择分析球员和对比球员
- 顶部显示球员身份、球队、赛季和综合能力评分
- 页面数据来自 FastAPI 后端聚合接口

推荐讲法：

> 这里展示的是球员个体画像系统的前端工作台。它不是静态页面，而是通过后端 API 动态读取球员数据、能力向量、趋势、相似球员和解释性结果。

### Step 2：展示能力画像

看“能力雷达”区域：

- 得分
- 组织
- 篮板
- 效率
- 防守

推荐讲法：

> 雷达图把球员的多维能力压缩到一个直观图形中，方便快速判断球员是偏得分、组织、篮板还是全能型。

### Step 3：展示近期状态

看“近期状态”趋势图：

- 表示最近比赛或阶段的表现分数
- 用于判断状态上升、波动或下滑

推荐讲法：

> 趋势图用于补充单场均值的不足，因为同一个球员的表现不是静态的，状态波动对教练和管理层都有参考价值。

### Step 4：展示风格空间

看“风格空间”散点图：

- 横轴表示进攻创造
- 纵轴表示内线影响
- 颜色表示不同风格聚类

推荐讲法：

> 这里把球员映射到一个二维风格空间中。距离更近的球员说明风格更相似，颜色则代表后端生成的风格聚类。

### Step 5：展示相似球员与解释性

看右侧“相似球员”和“贡献解释”：

- 相似球员用于推荐同类型球员
- 贡献解释说明综合评分主要由哪些能力驱动

推荐讲法：

> 相似球员和解释性模块可以提高系统的决策价值。它不仅告诉我们谁更接近，还告诉我们为什么这个球员会获得这样的能力画像。

### Step 6：切换球员

在左侧选择不同球员，例如：

- Stephen Curry
- Nikola Jokic
- Luka Doncic

观察所有图表同步变化。

推荐讲法：

> 切换球员时，前端会重新请求后端聚合接口，整个页面同步刷新。这体现了 E 模块做的系统集成：前端无需知道数据和模型细节，只消费统一 API。

## 4. 当前数据说明

当前展示使用真实数据产物，包含 100 位 NBA 2024-25 赛季球员。

- Stephen Curry
- Giannis Antetokounmpo
- Jayson Tatum
- Shai Gilgeous-Alexander
- Luka Dončić
- Victor Wembanyama

真实数据接入规则：

```text
data/processed/players.json
```

或：

```text
data/processed/players.csv
```

如果真实数据不存在，系统自动使用 mock 数据，保证前后端可以继续联调。

## 5. 演示前检查

运行 smoke test：

```bash
cd backend/player-profiling-api
python3 tests/smoke_test.py
```

预期输出：

```text
Smoke test passed
Players: 100
Data source: real
```

## 6. 备用展示接口

如果前端页面临时打不开，可以打开 API 文档：

```text
http://127.0.0.1:8000/docs
```

重点展示这些接口：

- `GET /api/v1/players`
- `GET /api/v1/players/{player_id}/dashboard`
- `GET /api/v1/players/compare`
- `GET /api/v1/style-space`
