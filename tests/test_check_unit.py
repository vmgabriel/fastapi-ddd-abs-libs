from src import main
from src.fastapi_ddd_abs_libs import __about__


def test_check_unit_tests():
    expected = 3

    assert main.context(1, 2) == expected


def test_has_about_version():
    assert bool(__about__.__version__)
