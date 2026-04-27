## 🧍 1. Player（基础球员数据）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| name | string | 球员姓名 |
| team | string | 所属球队 |
| season | int | 赛季年份 |
| stats.points | float | 场均得分 |
| stats.assists | float | 场均助攻 |
| stats.rebounds | float | 场均篮板 |

### 存放位置

真实数据应放在整体项目根目录：

```text
data/processed/players.json
```

或：

```text
data/processed/players.csv
```

后端 API 会优先读取 `players.json`，其次读取 `players.csv`。如果两个文件都不存在，则使用后端 mock 数据。

### JSON 示例

```json
{
  "players": [
    {
      "player_id": "real_001",
      "name": "Sample Star A",
      "team": "Demo Team",
      "season": 2024,
      "stats": {
        "points": 28.4,
        "assists": 7.2,
        "rebounds": 8.9
      }
    }
  ]
}
```

### CSV 示例

```csv
player_id,name,team,season,points,assists,rebounds
real_001,Sample Star A,Demo Team,2024,28.4,7.2,8.9
```

---

## 🧮 2. Feature Vector（特征工程输出）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| vector | array[float] | 球员能力特征向量（多维统计/工程特征） |

---

## 🧠 3. Embedding（语义向量表示）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| embedding | array[float] | 模型学习得到的语义表示向量（用于相似度/聚类） |

---

## 🧩 4. Cluster（风格聚类结果）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| cluster_id | int | 球员风格类别编号（如：得分型、防守型等） |

---

## 👥 5. Similarity（相似球员推荐）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 当前球员ID |
| similar_players | array[string] | 与该球员相似的球员ID列表 |

---

## 📈 6. Trend（表现趋势）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| values | array[float] | 时间序列表现数据（如每场/每阶段评分） |

---

## 🧾 7. Explanation（可解释性分析）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 球员唯一标识 |
| explanation | string | 模型对评分或表现的解释文本 |

---

## 🔌 8. 通用 API 返回结构（全系统统一）

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| code | int | 状态码（200=成功） |
| message | string | 返回提示信息 |
| data | object | 实际业务数据内容 |

---

## 🆔 9. 全局关键字段规范

| 数据名称 | 类型 | 含义 |
|----------|------|------|
| player_id | string | 全系统唯一球员ID（核心主键） |
