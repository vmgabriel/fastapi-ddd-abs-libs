from src.fastapi_ddd_abs_libs import __about__


def sum_context(a: int, b: int) -> int:
    return a + b


def test_check_unit_tests():
    expected = 3

    assert sum_context(1, 2) == expected


def test_has_about_version():
    assert bool(__about__.__version__)
