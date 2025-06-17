import re


def regex(fieldname: str, pattern: str) -> bool:
    if not fieldname:
        return False

    p = re.compile(pattern)

    return bool(p.findall(fieldname))


def equal_to(fieldname: str, content: str) -> bool:
    return fieldname.lower() == content


def not_equal_to(fieldname: str, content: str) -> bool:
    return fieldname.lower() != content


def contains(fieldname: str, content: str) -> bool:
    return content in fieldname.lower()


def not_contains(fieldname: str, content: str) -> bool:
    return content not in fieldname.lower()
