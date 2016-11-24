import pytest
from iap.forecasting.workbench.configuration import DataConfiguration
from iap.common.helper import Meta


@pytest.fixture
def config():
    from iap.common.dev_template import dev_template_JJOralCare
    conf = DataConfiguration()
    conf.init_load(dev_template_JJOralCare['configuration'])
    return conf


#def test_config_load():
#    conf = DataConfiguration()
#    conf.init_load(dev_template_JJOralCare['configuration'])
#    return


def test_common_options_getter(config):

    expected = ['Geography', 'Products']
    actual = config.get_common_option('dimensions')
    assert actual == expected

    expected = 'annual'
    actual = config.get_common_option('dashboard_top_ts')
    assert actual == expected

    expected = {'annual': [('2013', '2015'), ('2015', '2018')]}
    actual = config.get_common_option('dashboard_cagr_periods')
    assert actual == expected
    return


def test_get_view_variables(config):

    expected = [
        {
            'meta': {'type': 0},
            'data': {
                'outputs': ['value', 'eq_volume', 'eq_price'],
                'drivers': ['unit_price', 'unit_size', 'distribution',
                            'innovations', 'premiumization', 'media',
                            'discount', 'support', 'ltt']
            }
        },
        {
            'meta': {'type': 3, 'meta_filter': ('Geography', 'Country')},
            'data': {'drivers': ['population', 'cpi', 'gdp']}
        }
    ]
    actual = config.get_view_variables(Meta('Product', 'Category'))

    assert actual == expected

    with pytest.raises(Exception):
        config.get_view_variables(Meta('Unknown', 'Unknown'))
    return

def test_get_view_decomposition(config):

    expected = [
        {
            'meta': {'type': 0},
            'data': {
                'value': [
                    'dec_val_demo', 'dec_val_economy',
                    'dec_val_distribution', 'dec_val_innovations',
                    'dec_val_advertising', 'dec_val_trade_promo_on_vol',
                    'dec_val_price_on_vol', 'dec_val_unit_size_on_vol',
                    'dec_val_inflation','dec_val_man_pricing',
                    'dec_val_premiumization',
                    'dec_val_trade_promo',
                    'dec_val_unit_size',
                    'dec_val_other'
                ],
                'volume': [
                    'dec_vol_demo', 'dec_vol_economy',
                    'dec_vol_distribution', 'dec_vol_innovations',
                    'dec_vol_advertising', 'dec_vol_trade_promo',
                    'dec_vol_price', 'dec_vol_unit_size',
                    'dec_vol_ltt'
                ]
            }
        }
    ]
    actual = config.get_view_decomposition(Meta('Product', 'Category'))
    assert actual == expected

    with pytest.raises(Exception):
        config.get_view_decomposition(Meta('Unknown', 'Unknown'))
    return


def test_var_options_getter(config):

    expected = {'multiplier': 1000, 'format': '0,000', 'name': 'Sales',
                'metric': 'Local currency'}
    actual = config.get_variable_options('value', 'en',
                                         Meta('Product', 'Category'))
    assert actual == expected

    expected = {'multiplier': 1000, 'format': '0,000', 'name': 'Обьем продаж',
                'metric': 'Эквивалетные единицы'}
    actual = config.get_variable_options('eq_volume', 'ru',
                                       Meta('Product', 'Category'))
    assert actual == expected

    with pytest.raises(Exception):
        config.get_variable_options('Unknown', 'en',
                                    Meta('Product', 'Category'))

    with pytest.raises(Exception):
        config.get_variable_options('eq_volume', 'Unknown',
                                    Meta('Product', 'Category'))

    with pytest.raises(Exception):
        config.get_variable_options('eq_volume', 'en',
                                    Meta('Unknown', 'Unknown'))


def test_config_serialization(config):
    backup = config.get_backup()
    recovered_config = DataConfiguration()
    recovered_config.load_from_backup(backup)

    expected = config.get_common_option('dimensions')
    actual = recovered_config.get_common_option('dimensions')
    assert actual == expected

    expected = config.get_view_variables(Meta('Product', 'Category'))
    actual = recovered_config.get_view_variables(Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_view_decomposition(Meta('Product', 'Category'))
    actual = \
        recovered_config.get_view_decomposition(Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_variable_options('eq_volume', 'ru',
                                           Meta('Product', 'Category'))
    actual = recovered_config.get_variable_options('eq_volume', 'ru',
                                                   Meta('Product', 'Category'))
    assert actual == expected
    return
