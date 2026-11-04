import re


_QUESTION_NUMBER = re.compile(r"^\s*(?:q(?:uestion)?\s*)?\d+\s*[.):]\s*", re.IGNORECASE)


def strip_question_number(text: str) -> str:
    return _QUESTION_NUMBER.sub("", text, count=1).strip()
