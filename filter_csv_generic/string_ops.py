import re


def regex(fieldname: str, pattern: str) -> bool:
    if not fieldname:
        return False

    p = re.compile(pattern)

    if p.findall(fieldname):
        return True
    
    return False


def equal_to(fieldname: str, content: str) -> bool:

    return fieldname == content

def not_equal_to(fieldname: str, content: str) -> bool:

    return fieldname != content



def contains(fieldname: str, content: str) -> bool:
    return content in fieldname
