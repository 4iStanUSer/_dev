from collections import namedtuple

Variable = namedtuple('Variable', ['variable', 'timescale'])
Meta = namedtuple('Meta', ['dimension', 'level'])

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