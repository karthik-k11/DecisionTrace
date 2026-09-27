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