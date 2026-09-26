from flask import Flask, render_template, request

from analyzer import analyze
from validator import validate_input


app = Flask(__name__)


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