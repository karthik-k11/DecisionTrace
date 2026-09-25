from flask import Flask, render_template, request

from llm_client import analyze_decision


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    decision_text = ""
    result = None
    error = None

    if request.method == "POST":
        decision_text = request.form.get("decision_text", "").strip()

        if decision_text:
            try:
                result = analyze_decision(decision_text)
            except Exception as exc:
                error = str(exc)

    return render_template(
        "index.html",
        decision_text=decision_text,
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)