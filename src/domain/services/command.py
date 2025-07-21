import abc
import uuid
from typing import Any, Dict, List, Type, cast

import pydantic

from src.domain.models import filter


class CommandFilter(pydantic.BaseModel):
    attribute: str
    type: filter.FilterType
    value: str | List[str]


class CommandOrderBy(pydantic.BaseModel):
    attribute: str
    type: filter.OrderType


class CommandRequest(pydantic.BaseModel):
    trace_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)


class CommandQueryRequest(CommandRequest):
    limit: int | None = None
    offset: int | None = None
    order_by: str | None = None
    filters: str | None = None

    def get_filters(self) -> List[CommandFilter]:
        separator_filters = "|"
        separator_filter = ","
        comparator_filter = "::"
        filter_type_separator = "__"

        in_filter_data = self.filters.split(separator_filters) if self.filters else []

        filters = []
        for in_filter in in_filter_data:
            filter_data = in_filter.split(comparator_filter)
            if len(filter_data) != 2:
                print(f"Filter Data Not Valid - {filter_data}")
                continue

            key = filter_data[0]
            value = filter_data[1]

            attribute_filter_key = key.split(filter_type_separator)

            if len(attribute_filter_key) != 2:
                print(f"Attribute Filter Key Not Valid - {attribute_filter_key}")
                continue

            attribute = attribute_filter_key[0]
            filter_type = attribute_filter_key[1]

            filters.append(
                CommandFilter(
                    attribute=attribute,
                    type=filter.FilterType(filter_type.upper()),
                    value=value.split(separator_filter),
                )
            )
        return filters

    def get_order_by(self) -> List[CommandOrderBy]:
        separator_order_by = ","

        in_order_by_data = (
            self.order_by.split(separator_order_by) if self.order_by else []
        )

        orders_by = []
        for in_order_by in in_order_by_data:
            order_by_type = filter.OrderType.ASC
            if in_order_by.startswith("-"):
                in_order_by = in_order_by.replace("-", "")
                order_by_type = filter.OrderType.DESC
            orders_by.append(
                CommandOrderBy(
                    attribute=in_order_by,
                    type=order_by_type,
                )
            )

        return orders_by


class CommandResponse(pydantic.BaseModel):
    trace_id: uuid.UUID
    payload: Dict[str, Any] = pydantic.Field(default_factory=lambda: {})
    errors: List[Dict[str, Any]] = pydantic.Field(default_factory=lambda: [])


class Command(abc.ABC):
    request_type: Type[CommandRequest]
    request: CommandRequest | None
    requirements: List[str]
    parameters: Dict[str, Any]

    _deps: Dict[str, Any]

    def __init__(
        self,
        requirements: List[str] | None = None,
        request_type: Type[CommandRequest] = CommandRequest,
    ):
        self.requirements = requirements or []
        self.request = None
        self.request_type = request_type
        self.parameters = {}

        self._deps = {}

    def inject_dependencies(self, infra_dependencies: Dict[str, Any]) -> None:
        for requirement in self.requirements:
            self._deps[requirement] = infra_dependencies[requirement]

    def inject_parameters(self, parameters: Dict[str, Any]) -> None:
        self.parameters = parameters

    def inject_request(self, request: Any) -> None:
        self.request = cast(CommandRequest, request)

    def inject_using_dict(
        self,
        request_dict: Dict[str, Any],
    ) -> None:
        self.request = self.request_type.model_validate(request_dict)

    @abc.abstractmethod
    async def execute(self) -> CommandResponse:
        raise NotImplementedError()
