from collections import namedtuple
Variable = namedtuple('Variable', ['variable', 'timescale', 'slot'])
Meta = namedtuple('Meta', ['dimension', 'level'])
import json
from pyramid.response import Response

def send_success_response(data=None):
    """
    Help function that set template answer in case of success responce
    :param data:
    :type data: Union[bool, None, List[Dict[str, str]], str, Dict[str, Dict[str, str]], List[Dict[str, str]], Dict[str, Dict[str, bool]]]
    :return:
    :rtype: Union[Dict[str, bool], Dict[str, NoneType], Dict[str, List[Dict[str, str]]], Dict[str, str], Dict[str, Dict[str, Dict[str, str]]], Dict[str, Dict[str, Dict[str, bool]]]]
    """
    return {'error': False,'data': data}

def send_error_response(data):
    """
    Help function that set template answer in case of error responce
    :param data:
    :type data: str
    :return:
    :rtype: Dict[str, str]
    """
    return {'error': True,'data': data}


def is_equal_path(path1, path2):
    """
    Check if path is equal
    :param path1:
    :type path1:
    :param path2:
    :type path2:
    :return:
    :rtype:
    """
    if len(path1) != len(path2):
        return False
    for i in range(len(path1)):
        if path1[i] != path2[i]:
            return False
    return True


def is_equal_meta(meta1, meta2):
    """
    Check if meta data is equal
    :param meta1:
    :type meta1: iap.common.helper.Meta
    :param meta2:
    :type meta2: iap.common.helper.Meta
    :return:
    :rtype: bool
    """
    if meta1.dimension == meta2.dimension and meta1.level == meta2.level:
        return True
    return False


def dicts_left_join(d1, d2):
    for key in d1.keys():
        if key in d2:
            d1[key] = d2[key]