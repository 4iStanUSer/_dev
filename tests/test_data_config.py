import pytest
from iap.forecasting.workbench.configuration import DataConfiguration
from iap.common.helper import Meta


@pytest.fixture
def config():
    from iap.common.dev_template import dev_template_JJOralCare
    conf = DataConfiguration()
    conf.init_load(dev_template_JJOralCare['configuration'])
    return conf


def test_get_property(config):

    expected = ['Geography', 'Products']
    actual = config.get_property('dimensions')
    assert actual == expected

    expected = ['annual']
    actual = config.get_property('dash_timescales')
    assert actual == expected

    expected = ('2013', '2018')
    actual = config.get_property('dash_top_ts_period')
    assert actual == expected

    expected = ['annual']
    actual = config.get_property('dash_decomposition_timescales')
    assert actual == expected
    return


def test_get_vars_for_view(config):

    expected = [
        {
            'filter': {'type': 0},
            'variables': [
                {'id': 'value', 'type': 'output'},
                {'id': 'eq_volume', 'type': 'output'},
                {'id': 'eq_price', 'type': 'output'},
                {'id': 'unit_price', 'type': 'driver'},
                {'id': 'unit_size', 'type': 'driver'},
                {'id': 'distribution', 'type': 'driver'},
                {'id': 'innovations', 'type': 'driver'},
                {'id': 'premiumization', 'type': 'driver'},
                {'id': 'media', 'type': 'driver'},
                {'id': 'discount', 'type': 'driver'},
                {'id': 'support', 'type': 'driver'},
                {'id': 'ltt', 'type': 'driver'}
            ]
        },
        {
            'filter': {'type': 3, 'meta_filter': ('Geography', 'Country')},
            'variables': [
                {'id': 'population', 'type': 'driver'},
                {'id': 'cpi', 'type': 'driver'},
                {'id': 'gdp', 'type': 'driver'}
            ]
        }
    ]
    actual = config.get_vars_for_view(Meta('Product', 'Category'))

    assert actual == expected

    with pytest.raises(Exception):
        config.get_vars_for_view(Meta('Unknown', 'Unknown'))
    return


def test_get_decomp_vars_for_view(config):

    expected = [
        {
            'filter': {'type': 0},
            'variables': [
                {'id': 'dec_val_demo', 'type': 'value'},
                {'id': 'dec_val_economy', 'type': 'value'},
                {'id': 'dec_val_distribution', 'type': 'value'},
                {'id': 'dec_val_innovations', 'type': 'value'},
                {'id': 'dec_val_advertising', 'type': 'value'},
                {'id': 'dec_val_trade_promo_on_vol', 'type': 'value'},
                {'id': 'dec_val_price_on_vol', 'type': 'value'},
                {'id': 'dec_val_unit_size_on_vol', 'type': 'value'},
                {'id': 'dec_val_inflation', 'type': 'value'},
                {'id': 'dec_val_man_pricing', 'type': 'value'},
                {'id': 'dec_val_premiumization', 'type': 'value'},
                {'id': 'dec_val_trade_promo', 'type': 'value'},
                {'id': 'dec_val_unit_size', 'type': 'value'},
                {'id': 'dec_val_other', 'type': 'value'},
                {'id': 'dec_vol_demo', 'type': 'volume'},
                {'id': 'dec_vol_economy', 'type': 'volume'},
                {'id': 'dec_vol_distribution', 'type': 'volume'},
                {'id': 'dec_vol_innovations', 'type': 'volume'},
                {'id': 'dec_vol_advertising', 'type': 'volume'},
                {'id': 'dec_vol_trade_promo', 'type': 'volume'},
                {'id': 'dec_vol_price', 'type': 'volume'},
                {'id': 'dec_vol_unit_size', 'type': 'volume'},
                {'id': 'dec_vol_ltt', 'type': 'volume'}
            ]
        }
    ]
    actual = config.get_decomp_vars_for_view(Meta('Product', 'Category'))
    assert actual == expected

    with pytest.raises(Exception):
        config.get_decomp_vars_for_view(Meta('Unknown', 'Unknown'))
    return


def test_get_variables_properties(config):

    expected = [
        {'id': 'value', 'multiplier': 1000, 'format': '0,000', 'name': 'Sales',
                'metric': 'Local currency'},
        {'id': 'eq_volume', 'multiplier': 1000, 'format': '0,000',
         'name': 'Volume', 'metric': 'EQ'}
    ]
    actual = config.get_variables_properties(['value', 'eq_volume'], 'en',
                                         Meta('Product', 'Category'))
    assert actual == expected

    expected = [{'id': 'eq_volume', 'multiplier': 1000, 'format': '0,000',
                'name': 'Обьем продаж', 'metric': 'Эквивалетные единицы'}]
    actual = config.get_variables_properties(['eq_volume'], 'ru',
                                       Meta('Product', 'Category'))
    assert actual == expected

    expected = []
    actual = config.get_variables_properties(['Unknown'], 'en',
                                    Meta('Product', 'Category'))
    assert actual == expected

    with pytest.raises(Exception):
        config.get_variables_properties(['eq_volume'], 'Unknown',
                                    Meta('Product', 'Category'))

    with pytest.raises(Exception):
        config.get_variables_properties(['eq_volume'], 'en',
                                    Meta('Unknown', 'Unknown'))


def test_get_timescales_info(config):

    expected = [
        {'id': 'annual', 'full_name': 'Annual', 'short_name': 'A', 'lag': 1}
    ]
    actual = config.get_timescales_info(['annual'], 'en')
    assert actual == expected
    expected = [
        {'id': 'annual', 'full_name': 'Годовой', 'short_name': 'Г', 'lag': 1}
    ]
    actual = config.get_timescales_info(['annual'], 'ru')
    assert actual == expected

def test_get_dec_types_info(config):

    expected = [
        {'id': 'value', 'full_name': 'Sales Value', 'short_name': 'S'},
        {'id': 'volume', 'full_name': 'Volume', 'short_name': 'V'}
    ]
    actual = config.get_dec_types_info('en', Meta('Product', 'Category'))
    assert actual == expected

    expected = [
        {'id': 'value', 'full_name': 'Продажи', 'short_name': 'П'},
        {'id': 'volume', 'full_name': 'Обьем продаж', 'short_name': 'О'}
    ]
    actual = config.get_dec_types_info('ru', Meta('Product', 'Category'))
    assert actual == expected

def test_get_factor_drivers_relations(config):

    expected = {
        'dec_val_demo': [('dec_val_demo', 'population')],
        'dec_val_economy': [('dec_val_economy', 'gdp')],
        'dec_val_distribution': [('dec_val_distribution', 'distribution')],
        'dec_val_innovations': [('dec_val_innovations', 'innovations')],
        'dec_val_advertising': [('dec_val_advertising', 'media')],
        'dec_val_trade_promo_on_vol': [
            ('dec_val_trade_on_vol','discount'),
            ('dec_val_promo_on_vol', 'support')
        ],
        'dec_val_price_on_vol': [('dec_val_price_on_vol','unit_price')],
        'dec_val_unit_size_on_vol': [('dec_val_unit_size_on_vol','unit_size')],
        'dec_val_inflation': [('dec_val_inflation', 'cpi')],
        'dec_val_man_pricing': [(None, None)],
        'dec_val_premiumization': [('dec_val_premiumization', 'premiumization')],
        'dec_val_trade_promo': [
            ('dec_val_trade', 'discount'),
            ('dec_val_promo', 'support')
        ],
        'dec_val_unit_size': [('dec_val_unit_size','unit_size')],
        'dec_val_other': [(None, None)],
        'dec_vol_demo': [('dec_vol_demo', 'population')],
        'dec_vol_economy': ['dec_val_economy', 'gdp'],
        'dec_vol_distribution': [('dec_vol_distribution', 'distribution')],
        'dec_vol_innovations': [('dec_vol_innovations', 'innovations')],
        'dec_vol_advertising': [('dec_vol_advertising', 'media')],
        'dec_vol_trade_promo': [
            ('dec_vol_trade', 'discount'),
            ('dec_vol_promo', 'support')
        ],
        'dec_vol_price': [('dec_vol_price','unit_price')],
        'dec_vol_unit_size': [('dec_vol_unit_size', 'unit_size')],
        'dec_vol_ltt': [('dec_vol_ltt', 'ltt')]
    }
    actual = config.get_factor_drivers_relations(Meta('Product', 'Category'))
    assert actual == expected


def test_config_serialization(config):
    backup = config.get_backup()
    recovered_config = DataConfiguration()
    recovered_config.load_from_backup(backup)

    expected = config.get_property('dimensions')
    actual = recovered_config.get_property('dimensions')
    assert actual == expected

    expected = config.get_vars_for_view(Meta('Product', 'Category'))
    actual = recovered_config.get_vars_for_view(Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_decomp_vars_for_view(Meta('Product', 'Category'))
    actual = \
        recovered_config.get_decomp_vars_for_view(Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_variables_properties(['eq_volume'], 'ru',
                                           Meta('Product', 'Category'))
    actual = recovered_config.get_variables_properties(['eq_volume'], 'ru',
                                                   Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_timescales_info('en', Meta('Product', 'Category'))
    actual = \
        recovered_config.get_timescales_info('en', Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_dec_types_info('en', Meta('Product', 'Category'))
    actual = \
        recovered_config.get_dec_types_info('en', Meta('Product', 'Category'))
    assert actual == expected

    expected = config.get_factor_drivers_relations(Meta('Product', 'Category'))
    actual = recovered_config\
        .get_factor_drivers_relations(Meta('Product', 'Category'))
    assert actual == expected

    return
