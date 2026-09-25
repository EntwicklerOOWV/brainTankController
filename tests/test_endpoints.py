"""Tests für modules/endpoints.py -- aktuell nur send_push_notifications().

Nutzt ein Dummy-Objekt statt der echten user_config-Singleton-Instanz, damit
kein Zugriff auf die reale configs/user_config.json nötig ist und keine
Datei-Schreibvorgänge (save_to_file()) beim Testen ausgelöst werden.
"""

import pytest

from modules import endpoints


class DummyUserConfig:
    """Leichtgewichtiger Stand-in für UserConfig, ohne Datei-I/O."""

    def __init__(self, app_id="test-app-id", api_key="test-api-key", player_ids=None):
        self.onesignal_app_id = app_id
        self.onesignal_api_key = api_key
        self.player_ids = player_ids if player_ids is not None else []


@pytest.fixture
def dummy_user_config(monkeypatch):
    dummy = DummyUserConfig(player_ids=["player-1", "player-2"])
    # endpoints.py greift auf den Modul-Level-Namen "user_config" zu ->
    # wir tauschen genau den aus, nicht die Klasse/den Import selbst.
    monkeypatch.setattr(endpoints, "user_config", dummy)
    return dummy


ONESIGNAL_URL = "https://onesignal.com/api/v1/notifications"


def test_send_push_notifications_posts_correct_payload(requests_mock, dummy_user_config):
    requests_mock.post(ONESIGNAL_URL, json={"id": "abc"}, status_code=200)

    endpoints.send_push_notifications("Tank Entwässerung gestartet!")

    assert requests_mock.call_count == 1
    sent = requests_mock.last_request
    assert sent.json() == {
        "app_id": "test-app-id",
        "contents": {"en": "Tank Entwässerung gestartet!"},
        "include_player_ids": ["player-1", "player-2"],
    }
    assert sent.headers["Authorization"] == "Basic test-api-key"


def test_send_push_notifications_does_not_raise_on_error_status(
    requests_mock, dummy_user_config, capsys
):
    requests_mock.post(
        ONESIGNAL_URL, json={"errors": ["Invalid app_id"]}, status_code=400
    )

    # Darf NICHT werfen -- die Funktion soll Fehler nur loggen, nicht crashen
    endpoints.send_push_notifications("Test")

    captured = capsys.readouterr()
    assert "Failed to send notification" in captured.out


def test_send_push_notifications_uses_configured_key(requests_mock, dummy_user_config):
    """Regressionstest: stellt sicher, dass der Key aus user_config kommt
    und nicht (wieder) hartcodiert im Funktionskörper landet."""
    requests_mock.post(ONESIGNAL_URL, json={}, status_code=200)

    dummy_user_config.onesignal_api_key = "ein-anderer-key"
    endpoints.send_push_notifications("Test")

    assert requests_mock.last_request.headers["Authorization"] == "Basic ein-anderer-key"


def test_send_push_notifications_includes_all_player_ids(requests_mock, dummy_user_config):
    dummy_user_config.player_ids = ["a", "b", "c"]
    requests_mock.post(ONESIGNAL_URL, json={}, status_code=200)

    endpoints.send_push_notifications("Test")

    assert requests_mock.last_request.json()["include_player_ids"] == [
        "a", "b", "c"]
