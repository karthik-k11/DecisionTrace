from flask import Flask, render_template, request
import json

from analyzer import analyze
from database import (
    get_analysis,
    get_history,
    initialize_database,
    save_analysis,
)
from validator import validate_input

app = Flask(__name__)

app.jinja_env.filters["from_json"] = json.loads

initialize_database()


@app.route("/", methods=["GET", "POST"])
def home():
    decision_text = ""
    result = None
    error = None

    if request.method == "POST":
        decision_text = request.form.get("decision_text", "").strip()

        valid, validation_message = validate_input(decision_text)

        if not valid:
            error = validation_message
        else:
            try:
                result = analyze(decision_text)
                save_analysis(decision_text, result)
            except Exception as exc:
                error = str(exc)

    return render_template(
        "index.html",
        decision_text=decision_text,
        result=result,
        error=error,
    )


@app.route("/history")
def history():
    decisions = get_history()
    return render_template("history.html", decisions=decisions)


@app.route("/history/<int:analysis_id>")
def history_detail(analysis_id):
    analysis = get_analysis(analysis_id)

    if analysis is None:
        return render_template("404.html"), 404

    return render_template(
        "history_detail.html",
        analysis=analysis,
    )


if __name__ == "__main__":
    app.run(debug=True)