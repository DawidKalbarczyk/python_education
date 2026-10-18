import pytest
import time
import source.my_functions as my_functions

def test_add():
    result = my_functions.add(2, 3)
    assert result == 5


def test_add_string(): 
    result = my_functions.add("Hello, ", "World!")
    assert result == "Hello, World!"

def test_divide():
    result = my_functions.divide(10, 2)
    assert result == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        my_functions.divide(10, 0)

@pytest.mark.slow
def test_very_slow():
    time.sleep(5)
    result = my_functions.divide(10, 2)
    assert result == 5.0


@pytest.mark.skip(reason="This test is skipped for demonstration purposes")
def test_add():
    assert my_functions.add(1, 2) == 3


@pytest.mark.xfail(reason="This test is expected to fail for demonstration purposes")
def test_divide_broken():
    my_functions.divide(10, 0)