from typing import List, cast

from src.domain.models import filter as filter_domain
from src.domain.services import command


def command_query_to_criteria(
    query: command.CommandQueryRequest,
    filter_builder: filter_domain.FilterBuilder,
) -> filter_domain.Criteria:
    current_filters = [
        filter_builder.build(type_filter=filter.type)(filter.attribute)(filter.value)
        for filter in query.get_filters()
    ]
    current_order_by = [
        filter_builder.build_order(type_order=order_by.type)(order_by.attribute)
        for order_by in query.get_order_by()
    ]

    return filter_domain.Criteria(
        filters=cast(
            List[
                filter_domain.Filter
                | filter_domain.AndFilters
                | filter_domain.OrFilters
            ],
            current_filters,
        ),
        order_by=current_order_by,
        page_quantity=query.limit or 30,
        page_number=query.offset or 1,
    )
