def my_sum(a: int, b: int) -> int:
    return a + b


def test_check_unit_tests():
    expected = 3

    assert my_sum(1, 2) == expected
