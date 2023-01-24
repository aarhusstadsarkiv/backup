import re


def regex(fieldname: list[str], pattern: str) -> bool:
    if not fieldname:
        return False

    p = re.compile(pattern)

    for x in fieldname:
        if p.findall(x):
            return True

    return False


def contains(fieldname: list[str], content: str) -> bool:
    return any(content in string.lower() for string in fieldname)


def equal_to(fieldname: list[str], content: str) -> bool:
    return content in [item.lower() for item in fieldname]  # exact equal to


def not_equal_to(fieldname: list[str], content: str) -> bool:
    return content not in [item.lower() for item in fieldname]
