def get_features(player_id):
    return {
        "player_id": player_id,
        "vector": [0.23, 0.91, 0.44, 0.12, 0.79]
    }

def get_embedding(player_id):
    return {
        "player_id": player_id,
        "embedding": [0.25, 0.68, 0.12, 0.92, 0.33]
    }

def get_cluster(player_id):
    return {
        "player_id": player_id,
        "cluster_id": 2
    }

def get_similarity(player_id, top_k=5):
    return {
        "player_id": player_id,
        "similar_players": ["456", "789", "101"][:top_k]
    }

def get_trend(player_id):
    return {
        "player_id": player_id,
        "values": [24.5, 26.7, 25.8, 27.0, 28.3, 29.2]
    }

def get_explanation(player_id):
    return {
        "player_id": player_id,
        "explanation": "Scoring ability and assist contribution are primary drivers of performance score."
    }

def compare_players(p1, p2):
    return {
        "player1": p1,
        "player2": p2,
        "diff": {
            "points": 2.5,
            "assists": 1.1
        }
    }