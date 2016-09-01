from iap.repository import istorage, imanage_access, iaccess
from ..workbench import WorkbenchEngine

from ..template import tool_template  # TODO - REMOVE THIS
# import transaction

tool_id = 1  # TODO via - imanage_access.get_tool(ssn, name='Forecast')


def _get_ssn(req):
    return req.dbsession


def get_permissions(req, tool_id, user_id):
    ssn = _get_ssn(req)
    return iaccess.get_permissions(ssn, tool_id, user_id)


def tmp_workbench(req):
    ssn = _get_ssn(req)
    user_id = 1

    wb = WorkbenchEngine(user_id, imanage_access, ssn)
    wb.load_backup(tool_template)

    selection = {
        'geography': 2,
        'time': 3,  # 3
        'products': 5
    }
    dims = wb.dimensions.get_dimensions()
    dims_hier = {}
    if dims:
        for dim in dims:
            items = wb.dimensions.get_dimension_items(dim, selection)
            dims_hier[dim] = wb.dimensions.make_hierarchical(dim, items)

    print(1)


# def init_user_wb(req, tool_id, user_id):
#     ssn = _get_ssn(req)
#     #with transaction.manager:
#     return imanage_access.init_user_wb(ssn, tool_id, user_id)


# def update_user_perms(req):
#     ssn = _get_ssn(req)
#
#     permissions = [
#         {
#             'mask': 9,
#             'path': ['Argentina', 'Chocolate'],
#             'name': 'Praline',
#             'node_type': 'ent'
#         },
#         {
#             'mask': 7,
#             'path': ['Argentina', 'Chocolate', 'Praline'],
#             'name': 'Unit',
#             'node_type': 'var'
#         },
#         {
#             'mask': 5,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit'],
#             'name': 'Quarterly',
#             'node_type': 'ts'
#         },
#         {
#             'mask': 4,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit'],
#             'name': 'Annual',
#             'node_type': 'ts'
#         },
#         {
#             'mask': 3,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit',
#                      'Annual'],
#             'name': '2014',
#             'node_type': 'tp'
#         },
#         {
#             'mask': 2,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit',
#                      'Annual'],
#             'name': '2015',
#             'node_type': 'tp'
#         },
#         {
#             'mask': 6,
#             'path': ['Argentina', 'Chocolate', 'Praline'],
#             'name': 'Dollars',
#             'node_type': 'var'
#         },
#         {
#             'mask': 8,
#             'path': ['Brazil', 'Chocolate'],
#             'name': 'Praline',
#             'node_type': 'ent'
#         },
#         {
#             'mask': 1,
#             'path': ['Brazil', 'Chocolate', 'Praline', 'Unit', 'Annual'],
#             'name': '2015',
#             'node_type': 'tp'
#
#         },
#     ]
#
#     #with transaction.manager:
#     imanage_access.update_user_data_permissions(ssn, 1, 1, permissions)


# def set_permissions_template(req):
#     ssn = _get_ssn(req)
#
#     template = tool_template
#
#     #with transaction.manager:
#     imanage_access.set_permissions_template(ssn, tool_id, template)
#     #transaction.manager.commit()








def get_time_series():
    return [
        {
            'head': [
                {
                    'value': 'Population',
                    'meta': 'Variable'
                },
                {
                    'value': 'Billion',
                    'meta': 'Metric'
                }
            ],
            'cells': [
                {
                    'value': 123,
                    'valueType': 'int',
                    'meta': 'April'
                },
                {
                    'value': 124,
                    'valueType': 'int',
                    'meta': 'May'
                },
                {
                    'value': 125,
                    'valueType': 'int',
                    'meta': 'June'
                },
                {
                    'value': 126,
                    'valueType': 'int',
                    'meta': 'July'
                }
            ],
            'options': {}
        },
        {
            'head': [
                {
                    'value': 'GDP',
                    'meta': 'Variable'
                },
                {
                    'value': '$',
                    'meta': 'Metric'
                }
            ],
            'cells': [
                {
                    'value': 1230,
                    'valueType': 'int',
                    'meta': 'April'
                },
                {
                    'value': 1240,
                    'valueType': 'int',
                    'meta': 'May'
                },
                {
                    'value': 1250,
                    'valueType': 'int',
                    'meta': 'June'
                },
                {
                    'value': 1260,
                    'valueType': 'int',
                    'meta': 'July'
                }
            ],
            'options': {}
        }
    ]


def get_hierarchy():
    return [
        {
            "id": 27536, "text": "New node", "type": "parent",
            "state": {
                "opened": True,
                "disabled": False,
                "selected": True
            },
            "children": [
                {
                    "id": 27524, "text": "ss", "type": "parent",
                    "children": False
                },
                {
                    "id": 27521, "text": "ss", "type": "child",
                    "children": False
                }
            ]
        },
        {
            "id": 27529, "text": "New node", "type": "parent",
            "children": False
        },
        {
            "id": 27532, "text": "New node", "type": "child",
            "state": {
                "opened": False,
                "disabled": True,
                "selected": False
            },
            "children": False
        },
        {
            "id": 27538, "text": "New node", "type": "parent",
            "state": {
                "opened": False,
                "disabled": False,
                "selected": False
            },
            "children": [
                {
                    "id": 7524, "text": "ss", "type": "parent",
                    "children": False
                },
                {
                    "id": 7521, "text": "ss", "type": "child",
                    "children": False
                }
            ]
        }
    ]


def get_hierarchy1():
    return [
        {
            'id': 1, 'text': 'root1',
            "state": {
                "opened": False,
                "disabled": False,
                "selected": False
            },
            'children': [
                {
                    'id': 2,
                    'text': 'child1',
                    "state": {
                        "opened": False,
                        "disabled": False,
                        "selected": True
                    },
                }, {
                    'id': 3,
                    'text': 'child2',
                    "state": {
                        "opened": False,
                        "disabled": False,
                        "selected": False
                    },
                }
            ]
        },
        {
            'id': 4,
            'text': 'root2',
            "state": {
                "opened": True,
                "disabled": True,
                "selected": False
            },
            'children': [
                {
                    'id': 5,
                    'text': 'child2.1',
                    "state": {
                        "opened": False,
                        "disabled": False,
                        "selected": False
                    },
                },
                {
                    'id': 6,
                    'text': 'child2.2',
                    "state": {
                        "opened": False,
                        "disabled": False,
                        "selected": False
                    },
                    'children': [
                        {
                            'id': 7,
                            'text': 'subsub',
                            "state": {
                                "opened": False,
                                "disabled": False,
                                "selected": False
                            },
                        }
                    ]
                }
            ]
        },
        {
            'id': 8,
            'text': 'asyncroot',
            "state": {
                "opened": False,
                "disabled": False,
                "selected": False
            },
        }
    ]


def get_dropdown():
    return [
        {
            "id": 27524, "text": "First variant",
            "state": {
                "disabled": False,
                "selected": False
            },
        },
        {
            "id": 27525, "text": "ss1",
            "state": {
                "disabled": True,
                "selected": False
            },
        },
        {
            "id": 27526, "text": "ss2",
            "state": {
                "disabled": False,
                "selected": False
            },
        },
        {
            "id": 27527, "text": "dd",
            "state": {
                "disabled": False,
                "selected": False
            },
        },
        {
            "id": 27530, "text": "Some another",
            "state": {
                "disabled": False,
                "selected": True
            },
        },
    ]