from typing import Tuple

import psycopg

from . import model


class PsycopgSession(model.Session):
    _session: psycopg.Cursor
    _connection: psycopg.Connection

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def flush(self) -> None:
        getattr(self._connection, "flush", lambda: None)()


class PsycopgUOW(model.UOW):
    _con_data: str

    con: psycopg.Connection

    def __init__(self, *args, **kwargs) -> None:
        kwargs["session_factory"] = PsycopgSession
        super().__init__(*args, **kwargs)
        self._con_data = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
            dbname=self.configuration.postgres_dbname,
            user=self.configuration.postgres_username,
            password=self.configuration.postgres_password,
            host=self.configuration.postgres_host,
            port=self.configuration.postgres_port,
        )

    def _open(self) -> Tuple[object, object]:
        self.con = psycopg.connect(conninfo=self._con_data)
        cur = self.con.cursor()
        self.logger.info("Opened connection to PostgreSQL")
        return self.con, cur

    def _close(self, session: object | None) -> None:
        if not session:
            return
        getattr(session, "close")()
        self.con.close()
        self.logger.info("Closed connection to PostgreSQL")
