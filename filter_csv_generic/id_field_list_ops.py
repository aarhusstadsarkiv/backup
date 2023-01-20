import re


def regex(fieldvalues: list, pattern: str) -> bool:
    if not fieldvalues:
        return False

    p = re.compile(pattern)

    for x in fieldvalues:
        if p.findall(x):
            return True

    return False


def id_field_list_contains(fieldvalues: list, value: str) -> bool:

    if not fieldvalues:
        return False

    for x in fieldvalues:
        if value in x:
            return True
    return False


def equal_to(fieldvalues: list, value: str) -> bool:
    """fieldvalues from the csv database in the form [""1;Aarhus Stadsarkiv""]"""
    """value is user input"""
    if fieldvalues == []:
        return False
    else:
        for i in range(0, len(fieldvalues), 1):
            entry_content_str = fieldvalues[i].split(";")[1]
            entry_content_int = fieldvalues[i].split(";")[0]
            if value == entry_content_str:
                return True
            elif value == entry_content_int:
                return True

        return False


def not_equal_to(fieldvalues: list, value: str) -> bool:
    """Same as above, but negative search"""

    if fieldvalues == []:
        return False
    else:
        for i in range(0, len(fieldvalues), 1):
            entry_content_str = fieldvalues[i].split(";")[1]
            entry_content_int = fieldvalues[i].split(";")[0]
            if value != entry_content_str:
                return True
            elif value != entry_content_int:
                return True

        return False


def greater_than(fieldvalues: list, value: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            entry_content_int = fieldvalues[x].split(";")[0]
            if value < entry_content_int:
                return True

        return False


def less_than(fieldvalues: list, value: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            entry_content_int = fieldvalues[x].split(";")[0]
            if value > entry_content_int:
                return True

        return False
