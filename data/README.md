# Data Module

A 块数据处理与数据工程目录。

## 目录说明

- `raw/`：原始数据，建议不直接在代码中使用
- `processed/`：清洗后的标准数据，可供模型和后端读取

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
