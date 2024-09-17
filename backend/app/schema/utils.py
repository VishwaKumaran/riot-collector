import re


def convert_string(value):
    if isinstance(value, str):
        numeric_pattern = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$')
        return float(value) if bool(numeric_pattern.match(value)) else (value.strip() if value.strip() else None)
    return value


def remove_spaces(value: str) -> str:
    return re.sub(r'\s+', ' ', value)
