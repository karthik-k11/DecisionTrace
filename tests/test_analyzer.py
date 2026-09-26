import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analyzer import analyze


def test_analyzer_is_callable():
    assert callable(analyze)