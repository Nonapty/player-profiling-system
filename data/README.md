# Data Module

A 块数据处理与数据工程目录。

## 目录说明

- `raw/`：原始数据，建议不直接在代码中使用
- `processed/`：清洗后的标准数据，可供模型和后端读取

## 后端真实数据接入

后端 API 会优先读取：

```text
data/processed/players.json
```

如果没有该文件，会尝试读取：

```text
data/processed/players.csv
```

如果两个真实数据文件都不存在，后端会自动 fallback 到 mock 数据：

```text
backend/player-profiling-api/data/mock_db.py
```

## JSON 格式

推荐 A 组输出 `players.json`：

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

项目中提供了样例：

```text
data/processed/players.sample.json
```

真实使用时，可以复制一份并改名为：

```text
data/processed/players.json
```

临时测试样例文件时，也可以在启动后端时指定：

```bash
cd backend/player-profiling-api
PLAYERS_DATA_PATH=data/processed/players.sample.json uvicorn main:app --reload
```

## CSV 格式

如果使用 CSV，字段应为：

```csv
player_id,name,team,season,points,assists,rebounds
real_001,Sample Star A,Demo Team,2024,28.4,7.2,8.9
```

保存路径：

```text
data/processed/players.csv
```

## 输出要求

数据模块应尽量输出统一字段：

- `player_id`
- `name`
- `team`
- `season`
- `stats.points`
- `stats.assists`
- `stats.rebounds`

详细字段以 `docs/project/Data Contract Table.md` 为准。

## GitHub 注意事项

`data/raw/` 和 `data/processed/` 下的真实数据默认不会上传到 GitHub，避免提交过大的数据文件或敏感数据。

可以上传的样例文件：

- `*.sample.json`
- `*.sample.csv`
