import logging

from src import settings

from . import model


class LoggingAdapter(model.LogAdapter):
    log: logging.Logger
    level = {
        model.DebugLevelType.CRITICAL: 50,
        model.DebugLevelType.ERROR: 40,
        model.DebugLevelType.WARNING: 30,
        model.DebugLevelType.INFO: 30,
        model.DebugLevelType.NONE: 10,
    }

    def __init__(self, configuration: settings.BaseSettings) -> None:
        super().__init__(configuration=configuration)
        self.log = logging.getLogger(configuration.title)
        debug_level = model.DebugLevelType(configuration.debug_level.lower())
        self.log.setLevel(self.level[debug_level])

    def _message(self, msg: str, status: model.DebugLevelType) -> None:
        self.log.log(level=self.level[status], msg=msg)
