MIN_INPUT_LENGTH = 20
MAX_INPUT_LENGTH = 5000


def validate_input(text: str) -> tuple[bool, str]:
    text = text.strip()

    if not text:
        return False, "Decision input cannot be empty."

    if len(text) < MIN_INPUT_LENGTH:
        return False, "Decision input is too short."

    if len(text) > MAX_INPUT_LENGTH:
        return False, "Decision input is too long."

    return True, ""