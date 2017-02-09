from iap.forecasting.workbench.services import dimensions
from iap.common import runtime_storage as rt
from search_index import Input
import pytest


#1.1 initialise
#2.1 set entity selector config
#3.1 get options for entity selector

#get entity selector config
#get options for entity selections
#set entity selector


def test_search_by_query():

    query = {'geography': ['uk'], 'products': [], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [18]
    print("Actual", actual)
    assert expected == actual[1]


    query = {'geography': ['japan'], 'products': ['toothpaste'], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [24, 25, 26]
    print("Actual", actual[1])
    assert expected == actual[1]


    query = {'geography': ['us'], 'products': [], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [1, 11]
    print("Actual", actual[1])
    assert expected == actual[1]


    query = {'geography': ['us', 'uk'], 'products': ['toothpaste'], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [21, 22]
    print("Actual", actual[0])
    assert expected == actual[1]


    query = {'geography': ['us', 'uk'], 'products': [], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [1, 11, 8, 18, 19, 20, 21, 22]
    print("Actual", actual[0])
    assert expected == actual[1]


def test_search_by__query():

    query = {'geography': ['japan'], 'products': ['toothpaste'], 'market': []}
    actual = dimensions._search_by_query(Input, query)
    expected = [24, 25, 26]
    print("Actual", actual)
    assert expected==actual[1]

    query = {'geography': ['us'], 'products': [], 'market': []}
    actual = dimensions._search_by_query(Input, query)
    expected = [1, 11]
    print("Actual", actual)
    assert expected == actual[1]

    query = {'geography': ['us', 'uk'], 'products': ['toothpaste'], 'market': []}
    actual = dimensions._search_by_query(Input, query)
    expected = [21, 22]
    print("Actual", actual)
    assert expected == actual[1]

    query = {'geography': ['us', 'uk'], 'products': [], 'market': []}
    actual = dimensions._search_by_query(Input, query)
    expected = [1, 11, 8, 18, 19, 20, 21, 22]
    print("Actual", actual)
    assert expected == actual[1]
#test for get_options_for_entity_selector

#get_options_by_ents(wb.search_index, wb.selection, lang)

def test_get_options_by_ents():
    """
    Test for function get_options_by_ents

    :return:
    :rtype:

    """
    selection = [2, 28, 11]
    lang = "english"
    rt.update_state(user_id=2, tool_id="forecast", project_id=1)
    wb = rt.get_wb(user_id=2)
    actual = dimensions.get_options_by_ents(wb.search_index, selection, lang="english")
    print("Actual", actual)
    expected = {'geography':
                    {'data': [{'id': 'us', 'name': 'us', 'parent_id': None},
                              {'id': 'canada', 'name': 'canada', 'parent_id': None},
                              {'id': 'mexico', 'name': 'mexico', 'parent_id': None},
                              {'id': 'germany', 'name': 'germany', 'parent_id': None},
                              {'id': 'brazil', 'name': 'brazil', 'parent_id': None},
                              {'id': 'spain', 'name': 'spain', 'parent_id': None},
                              {'id': 'italy', 'name': 'italy', 'parent_id': None},
                              {'id': 'uk', 'name': 'uk', 'parent_id': None},
                              {'id': 'japan', 'name': 'japan', 'parent_id': None},
                              {'id': 'australia', 'name': 'australia', 'parent_id': None}],
                     'selected': ['canada|-|-|us|-|-|australia']},
                 'products': {'data': [{'id': 'mouthwash', 'name': 'mouthwash', 'parent_id': None}],
                                  'selected': ['|-|-|mouthwash']},
                 'market': {'data': [], 'selected': ['']}}
    assert expected==actual

    selection = [1, 2, 3]
    lang = "english"
    rt.update_state(user_id=2, tool_id="forecast", project_id=1)
    wb = rt.get_wb(user_id=2)
    actual = dimensions.get_options_by_ents(wb.search_index, selection, lang="english")
    expected = {'products':
                    {'selected': [''], 'data': [{'id': 'mouthwash', 'parent_id': None, 'name': 'mouthwash'}]},
                     'market': {'selected': [''], 'data': []},
                     'geography': {'selected': ['us|-|-|canada|-|-|mexico'],
                                   'data': [{'id': 'us', 'parent_id': None, 'name': 'us'},
                                            {'id': 'canada', 'parent_id': None, 'name': 'canada'},
                                            {'id': 'mexico', 'parent_id': None, 'name': 'mexico'},
                                            {'id': 'germany', 'parent_id': None, 'name': 'germany'},
                                            {'id': 'brazil', 'parent_id': None, 'name': 'brazil'},
                                            {'id': 'spain', 'parent_id': None, 'name': 'spain'},
                                            {'id': 'italy', 'parent_id': None, 'name': 'italy'},
                                            {'id': 'uk', 'parent_id': None, 'name': 'uk'},
                                            {'id': 'japan', 'parent_id': None, 'name': 'japan'},
                                            {'id': 'australia', 'parent_id': None, 'name': 'australia'}]}}
    assert actual == expected



#selectors_config = dimensions.get_selectors_config(wb.data_config, lang)