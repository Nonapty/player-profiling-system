from data.mock_db import PLAYERS
from data.real_db import get_player_from_real_db


class DataSwitcher:

    @staticmethod
    def get_player(player_id: str):

        # 1️⃣ 优先真实数据
        real_data = get_player_from_real_db(player_id)
        if real_data:
            return {
                "source": "real",
                "data": real_data
            }

        # 2️⃣ fallback mock数据
        mock_data = PLAYERS.get(player_id)

        if mock_data:
            return {
                "source": "mock",
                "data": mock_data
            }

        return {
            "source": "none",
            "data": None
        }