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
    assert b"Analysis Not Found" in response.data

def test_saved_analysis_page(monkeypatch):
    app_module.app.config["TESTING"] = True

    saved_analysis = {
        "id": 1,
        "created_at": "2026-10-07T21:00:00",
        "decision": "Use PostgreSQL",
        "input_summary": "The application needs relational data.",
        "result_json": """
        {
            "decision": "Use PostgreSQL",
            "evidence": [
                {
                    "text": "The application needs relational data.",
                    "supports": "Relational database requirements."
                }
            ],
            "assumptions": [
                "PostgreSQL is suitable for the application."
            ],
            "reasoning_links": [
                {
                    "from": "Relational data",
                    "to": "Use PostgreSQL",
                    "reason": "PostgreSQL supports relational data."
                }
            ],
            "gaps": [
                "Database alternatives were not evaluated."
            ]
        }
        """,
    }

    monkeypatch.setattr(
        app_module,
        "get_analysis",
        lambda analysis_id: saved_analysis,
    )

    client = app_module.app.test_client()

    response = client.get("/history/1")

    assert response.status_code == 200
    assert b"Use PostgreSQL" in response.data
    assert b"Relational database requirements." in response.data
    assert b"PostgreSQL is suitable for the application." in response.data
    assert b"Database alternatives were not evaluated." in response.data

def test_valid_decision_submission(monkeypatch):
    app_module.app.config["TESTING"] = True

    class MockResult:
        decision = "Use PostgreSQL"

        evidence = [
            type(
                "Evidence",
                (),
                {
                    "text": "The application needs relational data.",
                    "supports": "Relational database requirements.",
                },
            )()
        ]

        assumptions = [
            "PostgreSQL is suitable for the application."
        ]

        reasoning_links = [
            type(
                "ReasoningLink",
                (),
                {
                    "from_": "Relational data",
                    "to": "Use PostgreSQL",
                    "reason": "PostgreSQL supports relational data.",
                },
            )()
        ]

        gaps = [
            "Database alternatives were not evaluated."
        ]

    monkeypatch.setattr(
        app_module,
        "analyze",
        lambda text: MockResult(),
    )

    monkeypatch.setattr(
        app_module,
        "save_analysis",
        lambda input_text, result: None,
    )

    client = app_module.app.test_client()

    response = client.post(
        "/",
        data={
            "decision_text": (
                "We should use PostgreSQL because "
                "the application needs relational data."
            )
        },
    )

    assert response.status_code == 200
    assert b"Use PostgreSQL" in response.data
    assert b"Relational database requirements." in response.data
    assert b"PostgreSQL is suitable for the application." in response.data
def test_invalid_decision_submission(monkeypatch):
    app_module.app.config["TESTING"] = True

    def fail_if_called(text):
        raise AssertionError("analyze() should not be called")

    monkeypatch.setattr(
        app_module,
        "analyze",
        fail_if_called,
    )

    client = app_module.app.test_client()

    response = client.post(
        "/",
        data={
            "decision_text": "Too short",
        },
    )

    assert response.status_code == 200
    assert b"Decision input is too short." in response.data

def test_empty_decision_submission(monkeypatch):
    app_module.app.config["TESTING"] = True

    def fail_if_called(text):
        raise AssertionError("analyze() should not be called")

    monkeypatch.setattr(
        app_module,
        "analyze",
        fail_if_called,
    )

    client = app_module.app.test_client()

    response = client.post(
        "/",
        data={
            "decision_text": "",
        },
    )

    assert response.status_code == 200
    assert b"Decision input cannot be empty." in response.data


def test_maximum_length_decision_submission(monkeypatch):
    app_module.app.config["TESTING"] = True

    class MockResult:
        decision = "Test decision"
        evidence = []
        assumptions = []
        reasoning_links = []
        gaps = []

    monkeypatch.setattr(
        app_module,
        "analyze",
        lambda text: MockResult(),
    )

    monkeypatch.setattr(
        app_module,
        "save_analysis",
        lambda input_text, result: None,
    )

    client = app_module.app.test_client()

    response = client.post(
        "/",
        data={
            "decision_text": "A" * 5000,
        },
    )

    assert response.status_code == 200
    assert b"Test decision" in response.data

def test_oversized_decision_submission(monkeypatch):
    app_module.app.config["TESTING"] = True

    def fail_if_called(text):
        raise AssertionError("analyze() should not be called")

    monkeypatch.setattr(
        app_module,
        "analyze",
        fail_if_called,
    )

    client = app_module.app.test_client()

    response = client.post(
        "/",
        data={
            "decision_text": "A" * 5001,
        },
    )

    assert response.status_code == 200
    assert b"Decision input is too long." in response.data