import json
import sys
from urllib.error import URLError
from urllib.request import urlopen


BASE_URL = "http://127.0.0.1:8000"


def get_json(path):
    with urlopen(f"{BASE_URL}{path}", timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


def assert_ok(path):
    payload = get_json(path)
    assert payload["code"] == 200, payload
    return payload["data"]


def main():
    try:
        health = assert_ok("/api/v1/health")
        players = assert_ok("/api/v1/players")
        assert len(players) >= 2
        player1 = players[0]["player_id"]
        player2 = players[1]["player_id"]
        dashboard = assert_ok(f"/api/v1/players/{player1}/dashboard")
        compare = assert_ok(f"/api/v1/players/compare?player1={player1}&player2={player2}")
    except (AssertionError, URLError, TimeoutError) as error:
        print(f"Smoke test failed: {error}")
        return 1

    assert health["status"] == "ok"
    assert "features" in dashboard
    assert "style_space" in dashboard
    assert "diff" in compare

    print("Smoke test passed")
    print(f"Players: {len(players)}")
    print(f"Checked players: {player1}, {player2}")
    print(f"Data source: {health['data_source']['active_source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
