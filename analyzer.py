from llm_client import DecisionTraceResult, analyze_decision


def analyze(text: str) -> DecisionTraceResult:
    return analyze_decision(text)