import json
import math
from functools import lru_cache
from pathlib import Path

from services import player_service


FEATURE_LABELS = ["Scoring", "Playmaking", "Rebounding", "Efficiency", "Defense"]
DERIVED_FEATURE_MAP = [
    ("Scoring", "offense_score"),
    ("Playmaking", "playmaking_score"),
    ("Rebounding", "rebounding_score"),
    ("Defense", "defense_score"),
    ("Shooting", "shooting_score"),
]


def _project_root():
    return Path(__file__).resolve().parents[3]


def _analytics_path():
    output_path = _project_root() / "models" / "ml_analytics" / "output" / "analytics_bundle.json"
    if output_path.exists():
        return output_path
    return _project_root() / "models" / "ml_analytics" / "analytics_results.json"


def _features_path():
    output_path = _project_root() / "models" / "feature_engineering" / "output" / "feature_vectors.json"
    if output_path.exists():
        return output_path
    return _project_root() / "models" / "feature_engineering" / "feature_vectors.json"


@lru_cache(maxsize=1)
def _analytics_results():
    path = _analytics_path()
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def _feature_results():
    path = _features_path()
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def _feature_index():
    payload = _feature_results()
    if not payload:
        return {}

    features = payload.get("features") or payload.get("players") or {}
    if isinstance(features, dict):
        return features
    return {
        item["player_id"]: item
        for item in features
    }


def _analytics_section(section, player_id=None):
    payload = _analytics_results()
    if not payload:
        return None
    section_data = payload.get(section)
    if section_data is None:
        return None
    if isinstance(section_data, list):
        section_data = {
            item["player_id"]: item
            for item in section_data
            if isinstance(item, dict) and "player_id" in item
        }
    if player_id is None:
        return section_data
    return section_data.get(player_id)


def _pipeline_feature_vector(player_id):
    feature = _feature_index().get(player_id)
    if not feature:
        return None

    derived = feature.get("derived_features", {})
    if not derived:
        return None

    return {
        "player_id": player_id,
        "labels": [label for label, _ in DERIVED_FEATURE_MAP],
        "vector": [
            round(float(derived.get(key, 0)), 2)
            for _, key in DERIVED_FEATURE_MAP
        ]
    }


def _player(player_id):
    return player_service.get_player(player_id) or {}


def _stats(player_id):
    return _player(player_id).get("stats", {})


def _feature_vector(player_id):
    stats = _stats(player_id)
    points = float(stats.get("points", 0))
    assists = float(stats.get("assists", 0))
    rebounds = float(stats.get("rebounds", 0))

    scoring = min(points / 35, 1)
    playmaking = min(assists / 11, 1)
    rebounding = min(rebounds / 13, 1)
    efficiency = min((points * 0.52 + assists * 1.3 + rebounds * 0.7) / 35, 1)
    defense = min((rebounds * 0.75 + max(0, 32 - points) * 0.08) / 12, 1)

    return [
        round(scoring, 2),
        round(playmaking, 2),
        round(rebounding, 2),
        round(efficiency, 2),
        round(defense, 2),
    ]


def _distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def list_style_space():
    analytics_style_space = _analytics_section("style_space")
    if analytics_style_space:
        return analytics_style_space

    embeddings = _analytics_section("embeddings")
    clusters = _analytics_section("clusters") or {}
    if embeddings:
        players = {
            player["player_id"]: player
            for player in player_service.list_players()
        }
        coords = [
            item["embedding"]
            for item in embeddings.values()
            if len(item.get("embedding", [])) >= 2
        ]
        xs = [coord[0] for coord in coords]
        ys = [coord[1] for coord in coords]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        def normalize(value, lower, upper):
            if upper == lower:
                return 0.5
            return (value - lower) / (upper - lower)

        points = []
        for player_id, item in embeddings.items():
            player = players.get(player_id, {"player_id": player_id})
            x_raw, y_raw = item["embedding"][:2]
            cluster = clusters.get(player_id, {}).get("cluster_id", 0)
            points.append({
                "player_id": player_id,
                "name": player.get("name", player_id),
                "team": player.get("team", "Unknown"),
                "style": player.get("style", player.get("position", "Balanced")),
                "cluster_id": cluster,
                "x": round(normalize(x_raw, min_x, max_x), 3),
                "y": round(normalize(y_raw, min_y, max_y), 3),
            })

        return {"points": points}

    players = player_service.list_players()
    points_values = [p["stats"]["points"] for p in players]
    assists_values = [p["stats"]["assists"] for p in players]
    rebounds_values = [p["stats"]["rebounds"] for p in players]

    max_points = max(points_values) or 1
    max_assists = max(assists_values) or 1
    max_rebounds = max(rebounds_values) or 1

    points = []
    for player in players:
        stats = player["stats"]
        x = round((stats["points"] / max_points) * 0.72 + (stats["assists"] / max_assists) * 0.18, 3)
        y = round((stats["rebounds"] / max_rebounds) * 0.68 + (stats["assists"] / max_assists) * 0.2, 3)
        cluster_id = get_cluster(player["player_id"])["cluster_id"]
        points.append({
            "player_id": player["player_id"],
            "name": player.get("name", player["player_id"]),
            "team": player.get("team", "Unknown"),
            "style": player.get("style", "Balanced"),
            "cluster_id": cluster_id,
            "x": x,
            "y": y
        })

    return {"points": points}


def get_features(player_id):
    pipeline_features = _pipeline_feature_vector(player_id)
    if pipeline_features:
        return pipeline_features

    analytics_features = _analytics_section("features", player_id)
    if analytics_features:
        return {
            "player_id": analytics_features["player_id"],
            "labels": analytics_features["labels"],
            "vector": analytics_features["vector"]
        }

    vector = _feature_vector(player_id)
    return {
        "player_id": player_id,
        "labels": FEATURE_LABELS,
        "vector": vector
    }

def get_embedding(player_id):
    analytics_embedding = _analytics_section("embeddings", player_id)
    if analytics_embedding:
        return analytics_embedding

    features = _feature_vector(player_id)
    return {
        "player_id": player_id,
        "embedding": [
            round(features[0] * 0.7 + features[1] * 0.3, 2),
            round(features[2] * 0.65 + features[3] * 0.35, 2),
            round(features[4] * 0.55 + features[1] * 0.25 + features[0] * 0.2, 2)
        ]
    }

def get_cluster(player_id):
    analytics_cluster = _analytics_section("clusters", player_id)
    if analytics_cluster:
        return analytics_cluster

    features = _feature_vector(player_id)
    if features[0] >= 0.86 and features[1] >= 0.7:
        cluster_id = 4
    elif features[2] >= 0.85:
        cluster_id = 3
    elif features[1] >= 0.7:
        cluster_id = 2
    elif features[0] >= 0.75:
        cluster_id = 1
    else:
        cluster_id = 0

    return {
        "player_id": player_id,
        "cluster_id": cluster_id
    }

def get_similarity(player_id, top_k=5):
    analytics_similarity = _analytics_section("similarities", player_id)
    if analytics_similarity:
        players = {
            player["player_id"]: player
            for player in player_service.list_players()
        }
        similar_items = []
        for index, item in enumerate(analytics_similarity["similar_players"][:top_k]):
            if isinstance(item, dict):
                other_id = item["player_id"]
                score = item.get("score", round(0.92 - index * 0.06, 2))
            else:
                other_id = item
                score = round(0.92 - index * 0.06, 2)
            player = players.get(other_id, {"player_id": other_id})
            similar_items.append({
                "player_id": other_id,
                "name": player.get("name", other_id),
                "team": player.get("team", "Unknown"),
                "style": player.get("style", player.get("position", "Balanced")),
                "score": score
            })

        return {
            "player_id": player_id,
            "similar_players": similar_items
        }

    target = _feature_vector(player_id)
    scored = []
    for player in player_service.list_players():
        other_id = player["player_id"]
        if other_id == player_id:
            continue
        vector = _feature_vector(other_id)
        similarity = max(0, 1 - _distance(target, vector) / math.sqrt(len(target)))
        scored.append({
            "player_id": other_id,
            "name": player.get("name", other_id),
            "team": player.get("team", "Unknown"),
            "style": player.get("style", "Balanced"),
            "score": round(similarity, 2)
        })

    scored.sort(key=lambda item: item["score"], reverse=True)
    return {
        "player_id": player_id,
        "similar_players": scored[:top_k]
    }

def get_trend(player_id):
    analytics_trend = _analytics_section("trends", player_id)
    if analytics_trend:
        values = analytics_trend.get("values", [])
        return {
            "player_id": player_id,
            "labels": analytics_trend.get("labels") or [f"G{i + 1}" for i in range(len(values))],
            "values": values
        }

    stats = _stats(player_id)
    base = stats.get("points", 20) * 0.55 + stats.get("assists", 5) * 1.25 + stats.get("rebounds", 6) * 0.75
    values = [
        round(base - 2.1, 1),
        round(base - 0.6, 1),
        round(base + 0.4, 1),
        round(base - 0.2, 1),
        round(base + 1.1, 1),
        round(base + 1.8, 1),
        round(base + 1.3, 1),
        round(base + 2.4, 1)
    ]
    return {
        "player_id": player_id,
        "labels": ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"],
        "values": values
    }

def get_explanation(player_id):
    analytics_explanation = _analytics_section("explanations", player_id)
    if analytics_explanation:
        features = get_features(player_id)
        contributions = [
            {"feature": label, "value": round(value * 100)}
            for label, value in zip(features["labels"], features["vector"])
        ]
        contributions.sort(key=lambda item: item["value"], reverse=True)
        return {
            "player_id": player_id,
            "summary": analytics_explanation.get("explanation", ""),
            "contributions": contributions
        }

    features = get_features(player_id)
    contributions = [
        {"feature": label, "value": round(value * 100, 0)}
        for label, value in zip(features["labels"], features["vector"])
    ]
    contributions.sort(key=lambda item: item["value"], reverse=True)

    return {
        "player_id": player_id,
        "summary": "The integrated score is driven by the strongest dimensions in the player's current statistical profile.",
        "contributions": contributions
    }

def compare_players(p1, p2):
    player1 = _player(p1)
    player2 = _player(p2)
    features1 = get_features(p1)
    features2 = get_features(p2)
    diff = {}
    for label, value1, value2 in zip(features1["labels"], features1["vector"], features2["vector"]):
        diff[label] = round((value1 - value2) * 100, 1)

    return {
        "player1": p1,
        "player2": p2,
        "player1_name": player1.get("name", p1),
        "player2_name": player2.get("name", p2),
        "diff": diff
    }
