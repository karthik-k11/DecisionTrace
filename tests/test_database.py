import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import database


class MockResult:
    decision = "Use PostgreSQL"

    def model_dump(self):
        return {
            "decision": "Use PostgreSQL",
            "evidence": [],
            "assumptions": [],
            "reasoning_links": [],
            "gaps": [],
        }


def test_save_analysis(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        database_path
    )

    database.initialize_database()

    database.save_analysis(
        "We should use PostgreSQL for our application.",
        MockResult()
    )

    connection = database.get_connection()

    row = connection.execute(
        "SELECT * FROM decisions"
    ).fetchone()

    connection.close()

    assert row is not None
    assert row["decision"] == "Use PostgreSQL"
    assert row["input_summary"] == (
        "We should use PostgreSQL for our application."
    )

def test_get_history(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        database_path
    )

    database.initialize_database()

    database.save_analysis(
        "We should use PostgreSQL.",
        MockResult()
    )

    history = database.get_history()

    assert len(history) == 1
    assert history[0]["decision"] == "Use PostgreSQL"
    assert "result_json" in history[0]

def test_get_analysis(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        database_path
    )

    database.initialize_database()

    database.save_analysis(
        "We should use PostgreSQL.",
        MockResult()
    )

    history = database.get_history()

    analysis_id = history[0]["id"]

    analysis = database.get_analysis(analysis_id)

    assert analysis is not None
    assert analysis["id"] == analysis_id
    assert analysis["decision"] == "Use PostgreSQL"

def test_analysis_persists_after_reopening_connection(
    monkeypatch,
    tmp_path,
):
    import database

    monkeypatch.setattr(database, "DATABASE_DIR", tmp_path)
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "decisiontrace.db",
    )

    database.initialize_database()

    class MockResult:
        decision = "Use PostgreSQL"

        def model_dump(self):
            return {
                "decision": "Use PostgreSQL",
                "evidence": [],
                "assumptions": [],
                "reasoning_links": [],
                "gaps": [],
            }

    database.save_analysis(
        "The application needs relational data.",
        MockResult(),
    )

    # Open a fresh connection and retrieve the saved analysis.
    connection = database.get_connection()

    row = connection.execute(
        "SELECT id FROM decisions"
    ).fetchone()

    connection.close()

    analysis = database.get_analysis(row["id"])

    assert analysis is not None
    assert analysis["decision"] == "Use PostgreSQL"

def test_history_returns_newest_first(
    monkeypatch,
    tmp_path,
):
    import database

    monkeypatch.setattr(database, "DATABASE_DIR", tmp_path)
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "decisiontrace.db",
    )

    database.initialize_database()

    class MockResult:
        def __init__(self, decision):
            self.decision = decision

        def model_dump(self):
            return {
                "decision": self.decision,
                "evidence": [],
                "assumptions": [],
                "reasoning_links": [],
                "gaps": [],
            }

    database.save_analysis(
        "The first decision needs enough context to pass validation.",
        MockResult("First Decision"),
    )

    database.save_analysis(
        "The second decision needs enough context to pass validation.",
        MockResult("Second Decision"),
    )

    history = database.get_history()

    assert len(history) == 2
    assert history[0]["decision"] == "Second Decision"
    assert history[1]["decision"] == "First Decision"