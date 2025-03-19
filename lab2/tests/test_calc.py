import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(3, 5) == 8
    assert calc.add(-1, 1) == 0

def test_subtract(calc):
    assert calc.subtract(10, 5) == 5
    assert calc.subtract(0, 0) == 0

def test_multiply(calc):
    assert calc.multiply(4, 3) == 12
    assert calc.multiply(-1, -1) == 1

def test_divide(calc):
    assert calc.divide(10, 2) == 5
    with pytest.raises(ValueError):
        calc.divide(5, 0)

def test_power(calc):
    assert calc.power(2, 3) == 8
    assert calc.power(5, 0) == 1

def test_sqrt(calc):
    assert calc.sqrt(9) == 3
    with pytest.raises(ValueError):
        calc.sqrt(-4)

def test_factorial(calc):
    assert calc.factorial(5) == 120
    assert calc.factorial(0) == 1
    with pytest.raises(ValueError):
        calc.factorial(-3)
