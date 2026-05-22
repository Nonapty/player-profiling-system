from data.mock_db import PLAYERS
from data.real_db import get_player_from_real_db, list_players_from_real_db, load_real_players


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

    @staticmethod
    def get_data_status():
        real_players = load_real_players()
        return {
            "real_players": len(real_players),
            "mock_players": len(PLAYERS),
            "active_source": "real" if real_players else "mock"
        }

    @staticmethod
    def list_players():
        real_players = list_players_from_real_db()
        if real_players:
            return {
                "source": "real",
                "data": real_players
            }

        return {
            "source": "mock",
            "data": list(PLAYERS.values())
        }
