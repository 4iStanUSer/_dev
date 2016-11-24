import json
from pytest import fixture
from tests.conftest import TEST_FILES_FOLDER
from iap.forecasting.workbench.services import data_management


@fixture
def wb():
    from iap.repository import persistent_storage
    from iap.forecasting.workbench import Workbench
    backup = persistent_storage.load_backup('111', 'forecast', 'JJOralCare',
                                            'default')
    wb_instance = Workbench('111')
    wb_instance.load_from_backup(backup, None)
    return wb_instance


def test_get_entity_data(wb, datadir):
    expected = json.load(datadir.join('data_for_dashboard.json'))
    actual = data_management.get_entity_data(wb.container, wb.data_config,
                                             ['2'])
    assert actual == expected
