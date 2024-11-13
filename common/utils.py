from rest_framework.exceptions import ParseError


def to_string(value: any) -> str:
    try:
        return str(value)
    except Exception as e:
        raise ParseError(str(e))
