from utils.data_switcher import DataSwitcher
import logging

# 创建一个日志记录器
logger = logging.getLogger(__name__)

def get_player(player_id: str):
    result = DataSwitcher.get_player(player_id)

    if result["data"] is None:
        return None

    return result["data"]


def list_players():
    return DataSwitcher.list_players()["data"]
