from iap.common.RunTimeCollection import (RunTimeCollection,
                                          exceptions as runTimeEx)
from iap.repository import (get_wh_interface, get_access_interface)

from .. import TOOL_NAME

# from ..workbench.workbench_engine import WorkbenchEngine  # TODO(1.0) - remove
# from ...repository import get_manage_access_interface  # TODO(1.0) - remove
# from iap.repository.storage import Storage  # TODO(1.0) - remove


tool_id = 1  # TODO via - imanage_access.get_tool(ssn, name='Forecast')
tool_name = TOOL_NAME
run_time_collection = RunTimeCollection(tool_name)


def get_permissions(req, tool_id, user_id):
    iaccess = get_access_interface()
    return iaccess.get_permissions(tool_id, user_id)


def tmp_workbench(req):
    # warehouse = get_wh_interface()

    user_id = 1
    wb = run_time_collection.get(user_id)

    # # TODO(1.0) - Remake, because default backup exists always
    # try:
    #     wb = run_time_collection.get(user_id)
    # except runTimeEx.BackupNotFound as error:
    #     # TODO(1.0) - Move this
    #     iman_acc = get_manage_access_interface(ssn=req.dbsession)
    #     user_roles = iman_acc.get_user_roles(user_id)
    #     user_roles_id = [x.id for x in user_roles]
    #
    #     # Load into RAM
    #     wb = WorkbenchEngine(user_id, user_roles_id)
    #     wb.load_data_from_repository(warehouse)
    #     run_time_collection.add(user_id, wb)
    #
    #     # Save into storage
    #     new_backup = wb.get_data_for_backup()
    #     s = Storage()
    #     s.save_backup(user_id, tool_id, new_backup, 'default')

    # wb.load_backup(new_backup)
    # wb.load_backup(tool_template)

    def _convert_hierarchy(node, selected):
        if isinstance(node, list):
            new_nodes = []
            for n in node:
                new_nodes.append(_convert_hierarchy(n, selected))
            return new_nodes
        else:
            new_node = {
                'id': node['data']['id'],
                'text': node['data']['name'],
                'type': None,
                'state': {
                    'opened': True,
                    'disabled': False,
                    'selected': True
                    if node['data']['id'] == selected else False
                },
                'children': []
            }
            if node['children']:
                for child in node['children']:
                    new_node['children'].append(
                        _convert_hierarchy(child, selected))
            return new_node

    def_sel = {
        'geography': 4,  #2,
        'time': 3,  #3,
        'products': 6  #5
    }

    selection = {
        'geography': req.json_body['geography']['id']
        if req.json_body.get('geography') else def_sel['geography'],
        'time': req.json_body['time']['id']
        if req.json_body.get('time') else def_sel['time'],
        'products': req.json_body['products']['id']
        if req.json_body.get('products') else def_sel['products'],
    }
    selection = wb.dimensions.correct_selection(selection)

    dims = wb.dimensions.get_dimensions()

    c_ent_path = wb.dimensions.get_c_entity_path_by_selection(selection)

    time_series = []
    if c_ent_path:
        entity = wb.container.get_entity_by_path(c_ent_path)
        if entity:
            timescale = 'weekly'  # TODO CHANGE
            entity_data = wb.container.get_entity_data(entity, timescale)
            if entity_data:
                time_labels = wb.container.timeline.time_scales[timescale]
                for var_name, values in entity_data.items():
                    time_series.append({
                        'options': {},
                        'head': [
                            {
                                'meta': 'Variable',
                                'value': var_name
                            }
                        ],
                        'cells': [{
                                      'value': value,
                                      'valueType': 'float',
                                      'meta': time_labels[ind]
                                  } for ind, value in enumerate(values)]
                    })

    data = {
        'nav_panel': {
            'order': dims,
            'dimensions': []
        },
        'content': {
            'order': ['drivers_grid'],
            'zones': [
                {
                    'name': 'drivers_grid',
                    'widget': 'timeseries',
                    'data': time_series
                }
            ]
        }
    }

    if dims:
        for dim in dims:
            items = wb.dimensions.get_dimension_items(dim, selection)
            hier = wb.dimensions.make_hierarchical(dim, items)
            data['nav_panel']['dimensions'].append({
                'name': dim,
                'widget': 'hierarchy',
                'data': _convert_hierarchy(hier, selection[dim])
            })

    return data


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


# def get_time_series():
#     return [
#         {
#             'head': [
#                 {
#                     'value': 'Population',
#                     'meta': 'Variable'
#                 },
#                 {
#                     'value': 'Billion',
#                     'meta': 'Metric'
#                 }
#             ],
#             'cells': [
#                 {
#                     'value': 123,
#                     'valueType': 'int',
#                     'meta': 'April'
#                 },
#                 {
#                     'value': 124,
#                     'valueType': 'int',
#                     'meta': 'May'
#                 },
#                 {
#                     'value': 125,
#                     'valueType': 'int',
#                     'meta': 'June'
#                 },
#                 {
#                     'value': 126,
#                     'valueType': 'int',
#                     'meta': 'July'
#                 }
#             ],
#             'options': {}
#         },
#         {
#             'head': [
#                 {
#                     'value': 'GDP',
#                     'meta': 'Variable'
#                 },
#                 {
#                     'value': '$',
#                     'meta': 'Metric'
#                 }
#             ],
#             'cells': [
#                 {
#                     'value': 1230,
#                     'valueType': 'int',
#                     'meta': 'April'
#                 },
#                 {
#                     'value': 1240,
#                     'valueType': 'int',
#                     'meta': 'May'
#                 },
#                 {
#                     'value': 1250,
#                     'valueType': 'int',
#                     'meta': 'June'
#                 },
#                 {
#                     'value': 1260,
#                     'valueType': 'int',
#                     'meta': 'July'
#                 }
#             ],
#             'options': {}
#         }
#     ]


# def get_hierarchy():
#     return [
#         {
#             "id": 27536, "text": "New node", "type": "parent",
#             "state": {
#                 "opened": True,
#                 "disabled": False,
#                 "selected": True
#             },
#             "children": [
#                 {
#                     "id": 27524, "text": "ss", "type": "parent",
#                     "children": False
#                 },
#                 {
#                     "id": 27521, "text": "ss", "type": "child",
#                     "children": False
#                 }
#             ]
#         },
#         {
#             "id": 27529, "text": "New node", "type": "parent",
#             "children": False
#         },
#         {
#             "id": 27532, "text": "New node", "type": "child",
#             "state": {
#                 "opened": False,
#                 "disabled": True,
#                 "selected": False
#             },
#             "children": False
#         },
#         {
#             "id": 27538, "text": "New node", "type": "parent",
#             "state": {
#                 "opened": False,
#                 "disabled": False,
#                 "selected": False
#             },
#             "children": [
#                 {
#                     "id": 7524, "text": "ss", "type": "parent",
#                     "children": False
#                 },
#                 {
#                     "id": 7521, "text": "ss", "type": "child",
#                     "children": False
#                 }
#             ]
#         }
#     ]
#
#
# def get_hierarchy1():
#     return [
#         {
#             'id': 1, 'text': 'root1',
#             "state": {
#                 "opened": False,
#                 "disabled": False,
#                 "selected": False
#             },
#             'children': [
#                 {
#                     'id': 2,
#                     'text': 'child1',
#                     "state": {
#                         "opened": False,
#                         "disabled": False,
#                         "selected": True
#                     },
#                 }, {
#                     'id': 3,
#                     'text': 'child2',
#                     "state": {
#                         "opened": False,
#                         "disabled": False,
#                         "selected": False
#                     },
#                 }
#             ]
#         },
#         {
#             'id': 4,
#             'text': 'root2',
#             "state": {
#                 "opened": True,
#                 "disabled": True,
#                 "selected": False
#             },
#             'children': [
#                 {
#                     'id': 5,
#                     'text': 'child2.1',
#                     "state": {
#                         "opened": False,
#                         "disabled": False,
#                         "selected": False
#                     },
#                 },
#                 {
#                     'id': 6,
#                     'text': 'child2.2',
#                     "state": {
#                         "opened": False,
#                         "disabled": False,
#                         "selected": False
#                     },
#                     'children': [
#                         {
#                             'id': 7,
#                             'text': 'subsub',
#                             "state": {
#                                 "opened": False,
#                                 "disabled": False,
#                                 "selected": False
#                             },
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             'id': 8,
#             'text': 'asyncroot',
#             "state": {
#                 "opened": False,
#                 "disabled": False,
#                 "selected": False
#             },
#         }
#     ]
