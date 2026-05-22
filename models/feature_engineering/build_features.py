import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAYERS_PATH = ROOT / "data" / "processed" / "players.json"
OUTPUT_PATH = ROOT / "models" / "feature_engineering" / "feature_vectors.json"

FEATURE_LABELS = ["Scoring", "Playmaking", "Rebounding", "Efficiency", "Defense"]


def clamp(value, lower=0.0, upper=1.0):
    return max(lower, min(value, upper))


def build_vector(player):
    stats = player["stats"]
    points = float(stats.get("points", 0))
    assists = float(stats.get("assists", 0))
    rebounds = float(stats.get("rebounds", 0))
    minutes = float(stats.get("minutes", 34))
    turnovers = float(stats.get("turnovers", 3))

    scoring = clamp(points / 35)
    playmaking = clamp(assists / 11)
    rebounding = clamp(rebounds / 13)
    efficiency = clamp((points * 0.52 + assists * 1.3 + rebounds * 0.7 - turnovers * 0.7) / 35)
    defense = clamp((rebounds * 0.75 + max(0, 36 - minutes) * 0.08) / 12)

    return [round(v, 2) for v in [scoring, playmaking, rebounding, efficiency, defense]]


def main():
    with PLAYERS_PATH.open("r", encoding="utf-8") as file:
        players = json.load(file)["players"]

    feature_vectors = {}
    for player in players:
        vector = build_vector(player)
        feature_vectors[player["player_id"]] = {
            "player_id": player["player_id"],
            "name": player["name"],
            "labels": FEATURE_LABELS,
            "vector": vector,
            "score": round(sum(vector) / len(vector) * 100),
        }

    payload = {
        "source": str(PLAYERS_PATH.relative_to(ROOT)),
        "method": "rule-based normalization for seminar prototype",
        "feature_labels": FEATURE_LABELS,
        "players": feature_vectors,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"Wrote feature vectors to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
