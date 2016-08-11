import pytest
import os

# This is your Project Root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)


def demo_1(int_list):
    for i in int_list:
        if i == 0:
            raise ZeroDivisionError
        print(i)
    return 'OK'


def check():
    print('This method will not be used until we call it')


def test_1():
    demo_1([1, 2, 5, 3])
    # if not raise error then test fail
    pytest.raises(ZeroDivisionError, demo_1, [2, 0, 2])
    # Will check if function return wright result
    assert demo_1([1]) == 'OK'


@pytest.mark.skip(reason="no need to test now")
def test_2():
    print('Something')
