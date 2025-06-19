import abc
import contextlib
from typing import Generator, Tuple, Type

from src import settings
from src.infra.log import model as log_model


class Session(abc.ABC):
    logger: log_model.LogAdapter
    configuration: settings.BaseSettings

    _session: object
    _connection: object

    def __init__(
        self,
        configuration: settings.BaseSettings,
        logger: log_model.LogAdapter,
        _session: object,
        _connection: object,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self._session = _session
        self._connection = _connection

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def flush(self) -> None:
        raise NotImplementedError()


class UOW(abc.ABC):
    logger: log_model.LogAdapter
    configuration: settings.BaseSettings
    session_factory: Type[Session]

    def __init__(
        self,
        logger: log_model.LogAdapter,
        configuration: settings.BaseSettings,
        session_factory: Type[Session],
    ):
        self.configuration = configuration
        self.logger = logger
        self.session_factory = session_factory

    @contextlib.contextmanager
    def session(self) -> Generator[Session, Session, None]:
        _conn, _session = self._open()
        try:
            session = self.session_factory(
                configuration=self.configuration,
                logger=self.logger,
                _session=_session,
                _connection=_conn,
            )
            yield session
        finally:
            self._close(session=_session)

    @abc.abstractmethod
    def _open(self) -> Tuple[object, object]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _close(self, session: object | None) -> None:
        raise NotImplementedError()
