

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
