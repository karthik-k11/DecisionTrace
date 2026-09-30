import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module


def test_home_page():
    app_module.app.config["TESTING"] = True

    client = app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DecisionTrace" in response.data


def test_history_page():
    app_module.app.config["TESTING"] = True

    client = app_module.app.test_client()

    response = client.get("/history")

    assert response.status_code == 200
    assert b"Decision History" in response.data


def test_missing_analysis():
    app_module.app.config["TESTING"] = True

    client = app_module.app.test_client()

    response = client.get("/history/999999")

    assert response.status_code == 404
    assert b"Analysis not found" in response.data