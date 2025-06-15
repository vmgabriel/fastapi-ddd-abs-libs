import logging

from src import settings

from . import model


class LoggingAdapter(model.LogAdapter):
    log: logging.Logger
    level = {
        model.DebugLevelType.CRITICAL: 10,
        model.DebugLevelType.ERROR: 20,
        model.DebugLevelType.WARNING: 30,
        model.DebugLevelType.INFO: 40,
        model.DebugLevelType.NONE: 50,
    }

    def __init__(self, configuration: settings.BaseSettings) -> None:
        super().__init__(configuration=configuration)
        self.log = logging.getLogger(configuration.title)
        debug_level = model.DebugLevelType(configuration.debug_level.lower())
        self.log.setLevel(self.level[debug_level])

    def _message(self, msg: str, status: model.DebugLevelType) -> None:
        self.log._log(level=self.level[status], msg=msg, args=tuple())
