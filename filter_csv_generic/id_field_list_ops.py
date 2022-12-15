def id_field_list_contains(fieldvalues: list, content: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            if content in fieldvalues[x]:
                return True
        return False


def equal_to(fieldvalues: list, content: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            entry_content_str = fieldvalues[x].split(";")[1]
            entry_content_int = fieldvalues[x].split(";")[0]
            if content == entry_content_str:
                return True
            elif content == entry_content_int:
                return True

        return False


def greater_than(fieldvalues: list, content: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            entry_content_int = fieldvalues[x].split(";")[0]
            if content < entry_content_int:
                return True

        return False


def less_than(fieldvalues: list, content: str) -> bool:

    if fieldvalues == []:
        return False
    else:
        for x in range(0, len(fieldvalues), 1):
            entry_content_int = fieldvalues[x].split(";")[0]
            if content > entry_content_int:
                return True

        return False
