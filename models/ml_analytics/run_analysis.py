import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAYERS_PATH = ROOT / "data" / "processed" / "players.json"
FEATURES_PATH = ROOT / "models" / "feature_engineering" / "feature_vectors.json"
OUTPUT_PATH = ROOT / "models" / "ml_analytics" / "analytics_results.json"


def distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def cluster_id(vector):
    scoring, playmaking, rebounding, efficiency, defense = vector
    if scoring >= 0.86 and playmaking >= 0.7:
        return 4
    if rebounding >= 0.85:
        return 3
    if playmaking >= 0.7:
        return 2
    if scoring >= 0.75:
        return 1
    return 0


def embedding(vector):
    scoring, playmaking, rebounding, efficiency, defense = vector
    return [
        round(scoring * 0.7 + playmaking * 0.3, 2),
        round(rebounding * 0.65 + efficiency * 0.35, 2),
        round(defense * 0.55 + playmaking * 0.25 + scoring * 0.2, 2),
    ]


def trend_for(player):
    stats = player["stats"]
    base = stats.get("points", 20) * 0.55 + stats.get("assists", 5) * 1.25 + stats.get("rebounds", 6) * 0.75
    return {
        "labels": ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"],
        "values": [
            round(base - 2.1, 1),
            round(base - 0.6, 1),
            round(base + 0.4, 1),
            round(base - 0.2, 1),
            round(base + 1.1, 1),
            round(base + 1.8, 1),
            round(base + 1.3, 1),
            round(base + 2.4, 1),
        ],
    }


def main():
    with PLAYERS_PATH.open("r", encoding="utf-8") as file:
        players = json.load(file)["players"]
    with FEATURES_PATH.open("r", encoding="utf-8") as file:
        features = json.load(file)["players"]

    player_lookup = {player["player_id"]: player for player in players}
    vectors = {player_id: item["vector"] for player_id, item in features.items()}

    similarities = {}
    clusters = {}
    embeddings = {}
    explanations = {}
    trends = {}

    for player_id, vector in vectors.items():
        clusters[player_id] = {"player_id": player_id, "cluster_id": cluster_id(vector)}
        embeddings[player_id] = {"player_id": player_id, "embedding": embedding(vector)}
        trends[player_id] = {"player_id": player_id, **trend_for(player_lookup[player_id])}

        contributions = [
            {"feature": label, "value": round(value * 100)}
            for label, value in zip(features[player_id]["labels"], vector)
        ]
        contributions.sort(key=lambda item: item["value"], reverse=True)
        explanations[player_id] = {
            "player_id": player_id,
            "summary": "Feature contribution is derived from normalized player capability vector.",
            "contributions": contributions,
        }

        scored = []
        for other_id, other_vector in vectors.items():
            if other_id == player_id:
                continue
            score = max(0, 1 - distance(vector, other_vector) / math.sqrt(len(vector)))
            other = player_lookup[other_id]
            scored.append({
                "player_id": other_id,
                "name": other["name"],
                "team": other["team"],
                "style": other["style"],
                "score": round(score, 2),
            })
        scored.sort(key=lambda item: item["score"], reverse=True)
        similarities[player_id] = {"player_id": player_id, "similar_players": scored[:5]}

    max_points = max(player["stats"]["points"] for player in players)
    max_assists = max(player["stats"]["assists"] for player in players)
    max_rebounds = max(player["stats"]["rebounds"] for player in players)
    style_points = []
    for player in players:
        stats = player["stats"]
        player_id = player["player_id"]
        style_points.append({
            "player_id": player_id,
            "name": player["name"],
            "team": player["team"],
            "style": player["style"],
            "cluster_id": clusters[player_id]["cluster_id"],
            "x": round((stats["points"] / max_points) * 0.72 + (stats["assists"] / max_assists) * 0.18, 3),
            "y": round((stats["rebounds"] / max_rebounds) * 0.68 + (stats["assists"] / max_assists) * 0.2, 3),
        })

    payload = {
        "source": str(FEATURES_PATH.relative_to(ROOT)),
        "method": "prototype KNN-style similarity, rule-based clustering, and 2D style projection",
        "features": features,
        "embeddings": embeddings,
        "clusters": clusters,
        "similarities": similarities,
        "trends": trends,
        "explanations": explanations,
        "style_space": {"points": style_points},
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"Wrote analytics results to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
