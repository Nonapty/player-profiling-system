import csv
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional


REQUIRED_STATS = ("points", "assists", "rebounds")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _processed_data_dir() -> Path:
    return _project_root() / "data" / "processed"


def _configured_data_path() -> Optional[Path]:
    configured_path = os.getenv("PLAYERS_DATA_PATH")
    if not configured_path:
        return None

    path = Path(configured_path)
    if not path.is_absolute():
        path = _project_root() / path

    return path


def _normalize_player(row: dict[str, Any]) -> Optional[dict[str, Any]]:
    try:
        stats = row.get("stats") or {
            "points": row.get("points"),
            "assists": row.get("assists"),
            "rebounds": row.get("rebounds"),
        }

        normalized = {
            "player_id": str(row["player_id"]),
            "season": int(row["season"]),
            "stats": {
                key: float(stats[key])
                for key in REQUIRED_STATS
            },
        }

        if row.get("name"):
            normalized["name"] = str(row["name"])
        if row.get("team"):
            normalized["team"] = str(row["team"])

        return normalized
    except (KeyError, TypeError, ValueError):
        return None


def _load_json_players(path: Path) -> dict[str, dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    rows = payload["players"] if isinstance(payload, dict) and "players" in payload else payload
    if isinstance(rows, dict):
        rows = rows.values()

    players = {}
    for row in rows:
        normalized = _normalize_player(row)
        if normalized:
            players[normalized["player_id"]] = normalized

    return players


def _load_csv_players(path: Path) -> dict[str, dict[str, Any]]:
    players = {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            normalized = _normalize_player(row)
            if normalized:
                players[normalized["player_id"]] = normalized

    return players


@lru_cache(maxsize=1)
def load_real_players() -> dict[str, dict[str, Any]]:
    data_dir = _processed_data_dir()
    configured_path = _configured_data_path()
    json_path = data_dir / "players.json"
    csv_path = data_dir / "players.csv"

    if configured_path and configured_path.exists():
        if configured_path.suffix == ".json":
            return _load_json_players(configured_path)
        if configured_path.suffix == ".csv":
            return _load_csv_players(configured_path)
    if json_path.exists():
        return _load_json_players(json_path)
    if csv_path.exists():
        return _load_csv_players(csv_path)

    return {}


def get_player_from_real_db(player_id: str):
    return load_real_players().get(player_id)
