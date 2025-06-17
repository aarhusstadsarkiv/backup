import re


def regex(datefield: str, pattern: str) -> bool:
    if not datefield:
        return False

    p = re.compile(pattern)

    return bool(p.findall(datefield))


def equal_to(datefield: str, filter_: str) -> bool:
    return datefield == filter_


def not_equal_to(datefield: str, filter_: str) -> bool:
    return datefield != filter_


def greater_than(datefield: str, filter_: str) -> bool:
    return datefield > filter_


def less_than(datefield: str, filter_: str) -> bool:
    return datefield < filter_
