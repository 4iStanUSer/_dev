import json
import pytest
from tests.conftest import TEST_FILES_FOLDER
from iap.forecasting.workbench.services import data_management


@pytest.fixture
def wb():
    from iap.repository import persistent_storage
    from iap.forecasting.workbench import Workbench
    backup = persistent_storage.load_backup('111', 'forecast', 'JJOralCare',
                                            'default')
    wb_instance = Workbench('111')
    wb_instance.load_from_backup(backup, None)
    return wb_instance


def test_get_entity_data_structure(wb, datadir):
    expected = json.load(datadir.join('data_for_dashboard.json'))['data']
    actual = data_management.get_entity_data(wb.container, wb.data_config,
                                             [2], 'en')
    assert type(actual) == dict
    assert sorted(list(actual.keys())) == sorted(['config', 'data'])
    assert sorted(list(actual['config'].keys())) == sorted([
        'decomp_timescales',
        'main_period',
        'decomp_period'
    ])
    assert sorted(list(actual['data'].keys())) == sorted([
        'insights', 'variables', 'variable_values', 'timescales',
        'timelabels', 'decomp_types', 'change_over_period', 'decomp',
        'factor_drivers'
    ])
    type(actual['data']['insights']) == list
    assert type(actual['data']['timescales']) == list
    assert type(actual['data']['variables']) == list
    assert type(actual['data']['decomp_types']) == list
    assert type(actual['data']['variable_values']) == dict
    assert type(actual['data']['timelabels']) == list
    assert type(actual['data']['change_over_period']) == dict

    dict_to_check = actual['data']['insights']
    item_keys = ['text']
    for item in dict_to_check:
        assert sorted(list(item.keys())) == sorted(item_keys)

    dict_to_check = actual['data']['timescales']
    item_keys = ['id', 'full_name', 'short_name', 'lag']
    for item in dict_to_check:
        assert sorted(list(item.keys())) == sorted(item_keys)

    dict_to_check = actual['data']['variables']
    item_keys = ['id', 'full_name', 'short_name', 'type', 'metric',
                 'format', 'hint']
    for item in dict_to_check:
        assert sorted(list(item.keys())) == sorted(item_keys)

    dict_to_check = actual['data']['decomp_types']
    item_keys = ['id', 'full_name', 'short_name']
    for item in dict_to_check:
        assert sorted(list(item.keys())) == sorted(item_keys)

    dict_to_check = actual['data']['timelabels']
    item_keys = ['id', 'full_name', 'short_name', 'parent_index',
                 'timescale']
    for item in dict_to_check:
        assert sorted(list(item.keys())) == sorted(item_keys)

    dict_to_check = actual['data']['change_over_period']
    item_keys = ['abs', 'rate', 'end', 'start']
    for k1, v1 in dict_to_check.items():
        for k2, v2 in v1.items():
            for item in v2:
                assert sorted(list(item.keys())) == sorted(item_keys)

    for item in actual['data']['variable_values'].values():
        assert type(item) == dict
