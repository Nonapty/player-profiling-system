import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "player_stats.sample.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "players.json"

NUMERIC_FIELDS = ("age", "season", "points", "assists", "rebounds", "minutes", "turnovers")


def parse_float(value, fallback=0.0):
    try:
        if value is None or value == "":
            return fallback
        return float(value)
    except ValueError:
        return fallback


def infer_style(row):
    points = row["points"]
    assists = row["assists"]
    rebounds = row["rebounds"]

    if points >= 32 and assists >= 8:
        return "High-usage creator"
    if rebounds >= 11 and assists >= 7:
        return "Playmaking big"
    if rebounds >= 10 and points >= 28:
        return "Rim pressure"
    if assists >= 7:
        return "All-around creator"
    if points >= 25 and row["position"] == "Guard":
        return "Perimeter scorer"
    return "Two-way wing"


def clean_row(raw):
    row = {key: raw.get(key, "").strip() for key in raw}
    for field in NUMERIC_FIELDS:
        row[field] = parse_float(row.get(field))

    return {
        "player_id": str(row["player_id"]),
        "name": row["name"],
        "team": row["team"],
        "position": row["position"],
        "age": int(row["age"]),
        "season": int(row["season"]),
        "stats": {
            "points": round(row["points"], 1),
            "assists": round(row["assists"], 1),
            "rebounds": round(row["rebounds"], 1),
            "minutes": round(row["minutes"], 1),
            "turnovers": round(row["turnovers"], 1),
        },
        "style": infer_style(row),
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RAW_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        players = [clean_row(row) for row in csv.DictReader(file)]

    payload = {
        "source": str(RAW_PATH.relative_to(ROOT)),
        "cleaning_steps": [
            "trim string fields",
            "cast numeric fields",
            "nest box-score metrics under stats",
            "infer player style label from simple rules",
        ],
        "players": players,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"Wrote {len(players)} cleaned players to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
