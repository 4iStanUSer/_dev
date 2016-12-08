from collections import namedtuple
Variable = namedtuple('Variable', ['variable', 'timescale', 'slot'])
Meta = namedtuple('Meta', ['dimension', 'level'])


def send_success_response(data=None):
    return {
        'error': False,
        'data': data
    }


def send_error_response(data):
    return {
        'error': True,
        'data': data
    }


def is_equal_path(path1, path2):
    if len(path1) != len(path2):
        return False
    for i in range(len(path1)):
        if path1[i] != path2[i]:
            return False
    return True


def is_equal_meta(meta1, meta2):
    if meta1.dimension == meta2.dimension and meta1.level == meta2.level:
        return True
    return False


def dicts_left_join(d1, d2):
    for key in d1.keys():
        if key in d2:
            d1[key] = d2[key]