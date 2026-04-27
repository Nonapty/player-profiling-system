from fastapi import HTTPException
from services import player_service, ml_service


class IntegrationService:

    # =========================
    # 🧍 基础能力（统一校验入口）
    # =========================
    def _get_valid_player(self, player_id: str):
        player = player_service.get_player(player_id)

        if player is None:
            raise HTTPException(status_code=404, detail="player not found")

        return player

    def ok(self, data, message: str = "success"):
        return {
            "code": 200,
            "message": message,
            "data": data
        }

    def health(self):
        return {
            "status": "ok",
            "service": "player-profiling-api",
            "modules": {
                "data": "available",
                "ml": "available",
                "integration": "available"
            }
        }

    def player(self, player_id: str):
        return self._get_valid_player(player_id)

    # =========================
    # 🧮 Feature
    # =========================
    def features(self, player_id: str):
        self._get_valid_player(player_id)
        return ml_service.get_features(player_id)

    # =========================
    # 🧠 Embedding
    # =========================
    def embedding(self, player_id: str):
        self._get_valid_player(player_id)
        return ml_service.get_embedding(player_id)

    # =========================
    # 🧩 Cluster
    # =========================
    def cluster(self, player_id: str):
        self._get_valid_player(player_id)
        return ml_service.get_cluster(player_id)

    # =========================
    # 👥 Similarity
    # =========================
    def similarity(self, player_id: str, top_k: int = 5):
        self._get_valid_player(player_id)
        return ml_service.get_similarity(player_id, top_k)

    # =========================
    # 📈 Trend
    # =========================
    def trend(self, player_id: str):
        self._get_valid_player(player_id)
        return ml_service.get_trend(player_id)

    # =========================
    # 🧾 Explanation
    # =========================
    def explanation(self, player_id: str):
        self._get_valid_player(player_id)
        return ml_service.get_explanation(player_id)

    # =========================
    # 🔵 聚合接口：Profile
    # =========================
    def get_player_profile(self, player_id: str):
        player = self._get_valid_player(player_id)

        return {
            "player": player,
            "features": ml_service.get_features(player_id),
            "embedding": ml_service.get_embedding(player_id),
            "cluster": ml_service.get_cluster(player_id),
            "similarity": ml_service.get_similarity(player_id)
        }

    # =========================
    # 🔵 Dashboard（给前端用）
    # =========================
    def get_dashboard(self, player_id: str):
        self._get_valid_player(player_id)

        return {
            "player_id": player_id,
            "trend": ml_service.get_trend(player_id),
            "similarity": ml_service.get_similarity(player_id),
            "explanation": ml_service.get_explanation(player_id)
        }

    # =========================
    # 🔵 Compare
    # =========================
    def compare(self, p1: str, p2: str):
        self._get_valid_player(p1)
        self._get_valid_player(p2)

        return ml_service.compare_players(p1, p2)
