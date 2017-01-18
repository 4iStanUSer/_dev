from iap.forecasting.workbench.services import dimensions
from search_index import Input
import pytest


#1.1 initialise
#2.1 set entity selector config
#3.1 get options for entity selector

#get entity selector config
#get options for entity selections
#set entity selector

def prepare_wb():
    """
    WB preparation

    :return:
    :rtype:
    """
    pass

def test_search_by_query():

    query = {'geography': ['us', 'uk'], 'products': ['cars'], 'market': []}
    actual = dimensions.search_by_query(Input, query)
    expected = [18]
    print("Actual", actual[1])
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

