from llm_client import analyze_decision


result = analyze_decision(
    "We should choose PostgreSQL because our application needs "
    "relational data, transactions, and complex queries."
)


print(result.model_dump_json(indent=2))