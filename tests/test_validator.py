from validator import validate_input


def test_empty_input():
    valid, message = validate_input("")

    assert valid is False
    assert message == "Decision input cannot be empty."


def test_short_input():
    valid, message = validate_input("Use PostgreSQL")

    assert valid is False
    assert message == "Decision input is too short."


def test_valid_input():
    text = (
        "We should choose PostgreSQL because "
        "our application needs relational data."
    )

    valid, message = validate_input(text)

    assert valid is True
    assert message == ""


def test_large_input():
    text = "a" * 5001

    valid, message = validate_input(text)

    assert valid is False
    assert message == "Decision input is too long."