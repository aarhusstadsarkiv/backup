import re


def regex(datefield: str, pattern: str) -> bool:
    if not datefield:
        return False

    p = re.compile(pattern)

    if p.findall(datefield):
        return True

    return False


def equal_to(datefield: str, filter: str) -> bool:
    return datefield == filter


def not_equal_to(datefield: str, filter: str) -> bool:
    return datefield != filter


def greater_than(datefield: str, filter: str) -> bool:
    return datefield > filter


def less_than(datefield: str, filter: str) -> bool:
    return datefield < filter
