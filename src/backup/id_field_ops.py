import re


def regex(fieldname: str, pattern: str) -> bool:
    fieldname = fieldname.split(";")[1]

    if not fieldname:
        return False

    p = re.compile(pattern)

    return bool(p.findall(fieldname))


def id_field_contains(fieldname: str, content: str) -> bool:
    # fieldname = fieldname.split(";")[1]

    if fieldname == "":
        return False
    else:
        return content in fieldname.lower()


def equal_to(fieldname: str, content: str) -> bool:
    fieldname = fieldname.split(";")[0]

    if fieldname == "":
        return False
    else:
        return int(fieldname) == int(content)


def not_equal_to(fieldname: str, content: str) -> bool:
    fieldname = fieldname.split(";")[0]

    if fieldname == "":
        return False
    else:
        return int(fieldname) != int(content)


def greater_than(fieldname: str, content: str) -> bool:
    fieldname = fieldname.split(";")[0]

    if fieldname == "":
        return False
    else:
        return int(fieldname) > int(content)


def less_than(fieldname: str, content: str) -> bool:
    fieldname = fieldname.split(";")[0]

    if fieldname == "":
        return False
    else:
        return int(fieldname) < int(content)
