from typing import Any, cast

import uvicorn

from . import model


class UvicornAdapter(model.ServerAdapter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def execute(self) -> None:
        port = self.http.execute()
        self.logger.info(f"port.app - {port.instance}")
        uvicorn.run(
            app=cast(Any, port.instance),
            host=self.configuration.host,
            port=self.configuration.port,
        )
