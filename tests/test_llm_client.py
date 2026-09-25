import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llm_client import DecisionTraceResult


def test_decision_trace_schema():
    result = DecisionTraceResult(
        decision="Use PostgreSQL",
        evidence=[
            {
                "text": "The application needs relational data",
                "supports": "Relational database requirement"
            }
        ],
        assumptions=[
            "SQL is acceptable for the application"
        ],
        reasoning_links=[
            {
                "from": "Relational data",
                "to": "PostgreSQL",
                "reason": "PostgreSQL is a relational database"
            }
        ],
        gaps=[
            "Expected traffic is not specified"
        ]
    )

    assert result.decision == "Use PostgreSQL"
    assert len(result.evidence) == 1
    assert len(result.assumptions) == 1
    assert len(result.reasoning_links) == 1
    assert len(result.gaps) == 1