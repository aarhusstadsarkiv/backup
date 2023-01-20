import re


def regex(_dict: dict[str, str], pattern: str) -> bool:
    """_dict is the dictionary from the backup database csv."""
    """pattern is the regex from the user"""
    if not _dict:
        return False

    p = re.compile(pattern)

    for key in _dict.keys():
        if p.findall(_dict[key]):
            return True

    return False


def hasKey(_dict: dict, content: str) -> bool:
    return content in _dict


def contains(_dict: dict[str, str], content: str) -> bool:
    """_dict is the dictionary from the backup database csv."""
    """Content is the key-value pair from the user."""
    key_value_pair = content.split(":")
    if len(key_value_pair) == 2 and _dict.get(key_value_pair[0]):
        value: str = key_value_pair[1]
        return value in _dict.get(key_value_pair[0], [])
    else:
        return False
