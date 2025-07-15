import datetime
from typing import Any, List, Type

from src.domain.models import filter

_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
_DATE_FORMAT = "%Y-%m-%d"


class AscPostgresOrder(filter.Ordered):
    type: filter.OrderType = filter.OrderType.ASC

    def to_definition(self) -> str:
        return f"{self.attribute} ASC"


class DescPostgresOrder(filter.Ordered):
    type: filter.OrderType = filter.OrderType.DESC

    def to_definition(self) -> str:
        return f"{self.attribute} DESC"


class EqualPostgresDefinitionFilter(filter.FilterDefinition):

    def to_definition(self) -> str:
        return "{attr} = %s".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        response = ""
        if isinstance(value, str):
            response = value
        elif isinstance(value, bool):
            response = "true" if value else "false"
        elif isinstance(value, (int, float)):
            response = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return response


class NotEqualPostgresDefinitionFilter(filter.FilterDefinition):

    def to_definition(self) -> str:
        return "{attr} != ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, str):
            value = f"'{value}'"
        elif isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, (int, float)):
            value = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class LikePostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} LIKE ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, str):
            value = f"'%{value}%'"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class NotLikePostgresDefinitionFilter(filter.FilterDefinition):

    def to_definition(self) -> str:
        return "{attr} NOT LIKE ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, str):
            value = f"'%{value}%'"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class GreaterThanPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} > ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, (int, float)):
            value = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class LowerThanPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} < ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, (int, float)):
            value = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class GreaterEqualThanPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} >= ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, (int, float)):
            value = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class LowerEqualThanPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} <= ?".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if isinstance(value, (int, float)):
            value = f"{value}"
        else:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )
        return value


class InPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} IN (%s)".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if not isinstance(value, list):
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )

        values = []
        for val in value:
            if isinstance(val, (int, float)):
                values.append(f"{val}")
            elif isinstance(val, str):
                values.append(f"'{val}'")
            else:
                raise NotImplementedError(
                    "Definition for Type in {} is not implemented".format(
                        self.__class__.__name__
                    )
                )
        return ",".join(values)


class NotInPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return "{attr} NOT IN (%s)".format(attr=self.attribute)

    def get_values(self, value: Any) -> str | List[str]:
        if not isinstance(value, list):
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )

        values = []
        for val in value:
            if isinstance(val, (int, float)):
                values.append(f"{val}")
            elif isinstance(val, str):
                values.append(f"'{val}'")
            else:
                raise NotImplementedError(
                    "Definition for Type in {} is not implemented".format(
                        self.__class__.__name__
                    )
                )
        return ",".join(values)


class BetweenPostgresDefinitionFilter(filter.FilterDefinition):
    def to_definition(self) -> str:
        return f"{self.attribute} BETWEEN ? AND ?"

    def get_values(self, value: Any) -> str | List[str]:
        if not isinstance(value, list) or len(value) != 2:
            raise NotImplementedError(
                "Definition for Type in {} is not implemented".format(
                    self.__class__.__name__
                )
            )

        values = []
        for val in value:
            if isinstance(val, (int, float)):
                values.append(f"{val}")
            elif isinstance(val, str):
                values.append(f"'{val}'")
            elif isinstance(val, datetime.datetime):
                values.append(f"'{val.strftime(_DATETIME_FORMAT)}'")
            elif isinstance(val, datetime.date):
                values.append(f"'{val.strftime(_DATE_FORMAT)}'")
            else:
                raise NotImplementedError(
                    "Definition for Type in {} is not implemented".format(
                        self.__class__.__name__
                    )
                )
        return values


class PostgresAndFilters(filter.AndFilters):
    def to_definition(self) -> str:
        return " AND ".join(
            map(
                lambda current_filter: f"({current_filter.to_definition()})",
                self.filters,
            )
        )


class PostgresOrFilters(filter.OrFilters):
    def to_definition(self) -> str:
        return " OR ".join(
            map(
                lambda current_filter: f"({current_filter.to_definition()})",
                self.filters,
            )
        )


filters_definition = List[Type[filter.FilterDefinition]]
postgres_filter_builder = filter.FilterBuilder()

# Filter
postgres_filter_builder.inject(filter.FilterType.EQUAL, EqualPostgresDefinitionFilter)
postgres_filter_builder.inject(
    filter.FilterType.NOT_EQUAL, NotEqualPostgresDefinitionFilter
)
postgres_filter_builder.inject(filter.FilterType.LIKE, LikePostgresDefinitionFilter)
postgres_filter_builder.inject(
    filter.FilterType.NOT_LIKE, NotLikePostgresDefinitionFilter
)
postgres_filter_builder.inject(
    filter.FilterType.GREATER, GreaterThanPostgresDefinitionFilter
)
postgres_filter_builder.inject(
    filter.FilterType.LOWER, LowerThanPostgresDefinitionFilter
)
postgres_filter_builder.inject(
    filter.FilterType.GREATER_EQUAL, GreaterEqualThanPostgresDefinitionFilter
)
postgres_filter_builder.inject(
    filter.FilterType.LOWER_EQUAL, LowerEqualThanPostgresDefinitionFilter
)
postgres_filter_builder.inject(filter.FilterType.IN, InPostgresDefinitionFilter)
postgres_filter_builder.inject(filter.FilterType.NOT_IN, NotInPostgresDefinitionFilter)
postgres_filter_builder.inject(
    filter.FilterType.BETWEEN, BetweenPostgresDefinitionFilter
)

# Order
postgres_filter_builder.inject_order(filter.OrderType.ASC, AscPostgresOrder)
postgres_filter_builder.inject_order(filter.OrderType.DESC, DescPostgresOrder)

# Groups
postgres_filter_builder.inject_group_filter(
    filter.GroupFilterType.AND, PostgresAndFilters
)
postgres_filter_builder.inject_group_filter(
    filter.GroupFilterType.OR, PostgresOrFilters
)
