from __future__ import annotations

import abc
import enum
from typing import Any, Dict, List, Type, TypeVar

import pydantic

from . import repository

T = TypeVar("T")


class OrderType(enum.StrEnum):
    ASC = enum.auto()
    DESC = enum.auto()


class Paginator(pydantic.BaseModel):
    total: int = 0
    page: int = 0
    count: int = 0
    elements: List[repository.RepositoryData] = pydantic.Field(default_factory=list)

    @property
    def total_pages(self) -> int:
        return self.total // self.count

    @property
    def has_previous(self) -> bool:
        return self.page in (0, 1)

    @property
    def has_next(self) -> bool:
        return self.total_pages < self.page


class FilterDefinition:
    attribute: str

    def __init__(self, attribute: str):
        self.attribute = attribute

    def __call__(self, value: Any) -> "Filter":
        return Filter(filter_definition=self, value=value)

    @abc.abstractmethod
    def get_values(self, value: Any) -> str | List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def to_definition(self) -> str:
        raise NotImplementedError()


class Filter:
    value: Any
    filter_definition: FilterDefinition

    def __init__(self, filter_definition: FilterDefinition, value: Any) -> None:
        self.value = value
        self.filter_definition = filter_definition

    def get_values(self) -> str | List[str]:
        return self.filter_definition.get_values(self.value)

    def to_definition(self) -> str:
        return self.filter_definition.to_definition()


class Ordered(abc.ABC):
    type: OrderType = OrderType.ASC
    attribute: str

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    @abc.abstractmethod
    def to_definition(self) -> str:
        raise NotImplementedError()


class FilterType(enum.StrEnum):
    EQUAL = enum.auto()
    NOT_EQUAL = enum.auto()
    LIKE = enum.auto()
    NOT_LIKE = enum.auto()
    GREATER = enum.auto()
    LOWER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LOWER_EQUAL = enum.auto()
    IN = enum.auto()
    NOT_IN = enum.auto()
    BETWEEN = enum.auto()


class GroupFilterType(enum.StrEnum):
    AND = enum.auto()
    OR = enum.auto()
    NOT = enum.auto()


class AndFilters(abc.ABC):
    filters: List[Filter | AndFilters | OrFilters]

    def __init__(
        self,
        filters: List[Filter | AndFilters | OrFilters] | None = None,
    ) -> None:
        self.filters = filters or []

    @abc.abstractmethod
    def to_definition(self) -> str:
        raise NotImplementedError()

    def get_values(self) -> List[str | List[str]]:
        values = []
        for filter in self.filters:
            if isinstance(filter, Filter):
                values.append(filter.get_values())
                continue
            values += filter.get_values()
        return values


class OrFilters(abc.ABC):
    filters: List[Filter | AndFilters | OrFilters]

    def __init__(
        self,
        filters: List[Filter | AndFilters | OrFilters] | None,
    ) -> None:
        self.filters = filters or []

    @abc.abstractmethod
    def to_definition(self) -> str:
        raise NotImplementedError()

    def get_values(self) -> List[str | List[str]]:
        values = []
        for filter in self.filters:
            if isinstance(filter, Filter):
                values.append(filter.get_values())
                continue
            values += filter.get_values()
        return values


class FilterBuilder:
    filters: Dict[FilterType, Type[FilterDefinition]]
    group_filters: Dict[GroupFilterType, Type[AndFilters | OrFilters]]
    orders: Dict[OrderType, Type[Ordered]]

    def __init__(self) -> None:
        self.filters = {}
        self.orders = {}
        self.group_filters = {}

    def inject(
        self, type_filter: FilterType, filter_base: Type[FilterDefinition]
    ) -> None:
        self.filters[type_filter] = filter_base

    def inject_order(self, type_order: OrderType, order_base: Type[Ordered]) -> None:
        self.orders[type_order] = order_base

    def inject_group_filter(
        self,
        group_filter_type: GroupFilterType,
        group_filter: Type[AndFilters | OrFilters],
    ) -> None:
        self.group_filters[group_filter_type] = group_filter

    def build(self, type_filter: FilterType) -> Type[FilterDefinition]:
        if type_filter not in self.filters:
            raise ValueError(f"Filter type {type_filter} not exists")

        return self.filters[type_filter]

    def build_order(self, type_order: OrderType) -> Type[Ordered]:
        if type_order not in self.orders:
            raise NotImplementedError(f"Order type {type_order} not exists")

        return self.orders[type_order]

    def build_group_filter(
        self, group_filter: GroupFilterType
    ) -> Type[AndFilters | OrFilters]:
        if group_filter not in self.group_filters:
            raise NotImplementedError(f"group filter type {group_filter} not exists")

        return self.group_filters[group_filter]


class Criteria:
    filters: List[FilterDefinition | AndFilters | OrFilters]
    order_by: List[Ordered]
    page_quantity: int
    page_number: int

    def __init__(
        self,
        filters: List[FilterDefinition | AndFilters | OrFilters],
        order_by: List[Ordered],
        page_quantity: int,
        page_number: int,
    ) -> None:
        self.filters = filters
        self.order_by = order_by
        self.page_quantity = page_quantity
        self.page_number = page_number
