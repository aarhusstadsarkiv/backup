import re


def regex(_dict: dict[str, str], pattern: str) -> bool:
    if not _dict:
        return False

    p = re.compile(pattern)

    for key in _dict.keys():
        if p.findall(_dict[key]):
            return True
    
    return False


def hasKey(_dict: dict, content: str):
    return content in _dict


def contains(_dict: dict[str, str], content: str):
    key_value_pair = content.split(":")
    if len(key_value_pair) == 2 and _dict.get(key_value_pair[0]):
        return key_value_pair[1] in _dict.get(key_value_pair[0], [])
    else:
        return False
