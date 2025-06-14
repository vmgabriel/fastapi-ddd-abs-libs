from logging import getLogger
from typing import cast

import pytest

from src import settings
from src.fastapi_ddd_abs_libs import base

logger = getLogger(__name__)


class Father:
    def __init__(self, infra2: object) -> None:
        self.infra2 = infra2


class Children(Father):
    pass


def test_has_concrete_data_infra() -> None:
    expected_infra1_title = "infra1"
    expected_infra1_option1_title = "infra1_option1"

    infra_options1 = [
        base.InfraOption(
            title=expected_infra1_option1_title, priority=1, type_adapter=Children
        )
    ]
    request_infra1 = base.InfraRequest(
        title=expected_infra1_title,
        requirements=["infra2"],
        options=infra_options1,
    )
    infra_1 = base.InfraBase(
        request=request_infra1,
        logger_adapter=logger,
        configurations=settings.DevSettings(),
    )
    dependencies = {"infra2": ...}

    assert infra_1.title == expected_infra1_title, "Check if exist title in infraBase"
    assert (
        infra_1.select(expected_infra1_option1_title) == Children
    ), "Check if get type in select"

    with pytest.raises(ValueError):
        infra_1.select("other_option_that_does_not_exist")

    assert infra_1.all() == [Children]

    children_instance: Father = cast(
        Father,
        infra_1.select_and_inject(
            option=expected_infra1_option1_title, dependencies=dependencies
        ),
    )
    assert isinstance(children_instance, Children), "Check if get type in select"
    with pytest.raises(TypeError):
        infra_1.select_and_inject(
            option=expected_infra1_option1_title, dependencies={"no": "fake"}
        )
