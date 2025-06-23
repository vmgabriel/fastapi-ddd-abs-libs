from typing import Any, List

import pytest

from src.domain.models import filter as filter_domain
from src.infra.filter import postgres as filter_postgres


def test_asc_desc_filter_ok() -> None:
    expected_attribute = "test"
    definition_filter = filter_postgres.AscPostgresOrder(expected_attribute)

    assert definition_filter.to_definition() == "test ASC"

    definition = filter_postgres.DescPostgresOrder(expected_attribute)

    assert definition.to_definition() == "test DESC"


@pytest.mark.parametrize(
    "expected_value,values",
    [
        ("test", "'test'"),
        (1, "1"),
        (1.2, "1.2"),
        (True, "true"),
        (False, "false"),
    ],
)
def test_equal_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} = ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.EQUAL
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        ("test", "'test'"),
        (1, "1"),
        (1.2, "1.2"),
        (True, "true"),
        (False, "false"),
    ],
)
def test_not_equal_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} != ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.NOT_EQUAL
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        ("test", "'%test%'"),
    ],
)
def test_like_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} LIKE ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.LIKE
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        ("test", "'%test%'"),
    ],
)
def test_not_like_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} NOT LIKE ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.NOT_LIKE
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        (1, "1"),
        (1.2, "1.2"),
    ],
)
def test_greater_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} > ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.GREATER
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        (1, "1"),
        (1.2, "1.2"),
    ],
)
def test_lower_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} < ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.LOWER
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        (1, "1"),
        (1.2, "1.2"),
    ],
)
def test_greater_equal_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} >= ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.GREATER_EQUAL
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


@pytest.mark.parametrize(
    "expected_value,values",
    [
        (1, "1"),
        (1.2, "1.2"),
    ],
)
def test_lower_equal_definition_filter(expected_value: Any, values: str) -> None:
    expected_attribute = "test"
    expected_definition = "{attribute} <= ?".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.LOWER_EQUAL
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


def test_in_definition_filter() -> None:
    expected_value: List[Any] = [1, 2, 3, 4]
    values = "1,2,3,4"
    expected_attribute = "test"
    expected_definition = "{attribute} IN (%s)".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.IN
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values

    expected_value = ["a", "b", "c", "d"]
    values = "'a','b','c','d'"

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


def test_not_in_definition_filter() -> None:
    expected_value: List[Any] = [1, 2, 3, 4]
    values = "1,2,3,4"
    expected_attribute = "test"
    expected_definition = "{attribute} NOT IN (%s)".format(attribute=expected_attribute)
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.NOT_IN
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values

    expected_value = ["a", "b", "c", "d"]
    values = "'a','b','c','d'"

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == values


def test_between_definition_filter() -> None:
    expected_value = [1, 2]
    expected_attribute = "test"
    expected_definition = "{attribute} BETWEEN ? AND ?".format(
        attribute=expected_attribute
    )
    definition_filter = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.BETWEEN
    )(expected_attribute)

    assert isinstance(definition_filter, filter_domain.FilterDefinition)

    definition = definition_filter(expected_value)

    assert isinstance(definition, filter_domain.Filter)
    assert definition.to_definition() == expected_definition
    assert definition.get_values() == ["1", "2"]


def test_and_group_filters() -> None:
    expected_attribute = "test"
    expected_attribute2 = "test2"
    expected_value = "abc"
    expected_value2 = "def"

    definition_equal = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.EQUAL
    )(expected_attribute)
    definition_equal2 = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.EQUAL
    )(expected_attribute2)
    filter_equal = definition_equal(expected_value)
    filter_equal2 = definition_equal2(expected_value2)

    definition_group_filter = (
        filter_postgres.postgres_filter_builder.build_group_filter(
            filter_domain.GroupFilterType.AND
        )
    )(filters=[filter_equal, filter_equal2])

    assert definition_group_filter.to_definition() == "(test = ?) AND (test2 = ?)"
    assert definition_group_filter.get_values() == ["'abc'", "'def'"]


def test_or_group_filters() -> None:
    expected_attribute = "test"
    expected_attribute2 = "test2"
    expected_value = "abc"
    expected_value2 = "def"

    definition_equal = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.EQUAL
    )(expected_attribute)
    definition_equal2 = filter_postgres.postgres_filter_builder.build(
        type_filter=filter_domain.FilterType.EQUAL
    )(expected_attribute2)
    filter_equal = definition_equal(expected_value)
    filter_equal2 = definition_equal2(expected_value2)

    definition_group_filter = (
        filter_postgres.postgres_filter_builder.build_group_filter(
            filter_domain.GroupFilterType.OR
        )
    )(filters=[filter_equal, filter_equal2])

    assert definition_group_filter.to_definition() == "(test = ?) OR (test2 = ?)"
    assert definition_group_filter.get_values() == ["'abc'", "'def'"]
