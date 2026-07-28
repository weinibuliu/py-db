import pytest
from sqlalchemy import exc

from db import (
    BackendError,
    BackendTimeoutError,
    BackendUnavailableError,
    NotFoundError,
)
from db._db.engine import write_session


class FakeSession:
    def flush(self) -> None:
        pass


def _raise_from_write_session(error: Exception) -> None:
    with write_session(FakeSession()):  # type: ignore[arg-type]
        raise error


def test_db_error_passes_through_unchanged() -> None:
    error = NotFoundError()

    with pytest.raises(NotFoundError) as raised:
        _raise_from_write_session(error)

    assert raised.value is error


def test_pool_timeout_becomes_backend_timeout() -> None:
    error = exc.TimeoutError("pool timed out")

    with pytest.raises(BackendTimeoutError) as raised:
        _raise_from_write_session(error)

    assert raised.value.__cause__ is error


def test_invalidated_connection_becomes_backend_unavailable() -> None:
    error = exc.DBAPIError(
        statement=None,
        params=None,
        orig=ConnectionError("connection lost"),
        connection_invalidated=True,
    )

    with pytest.raises(BackendUnavailableError) as raised:
        _raise_from_write_session(error)

    assert raised.value.__cause__ is error


def test_other_dbapi_error_becomes_backend_error() -> None:
    error = exc.DBAPIError(
        statement=None,
        params=None,
        orig=RuntimeError("driver failed"),
    )

    with pytest.raises(BackendError) as raised:
        _raise_from_write_session(error)

    assert type(raised.value) is BackendError
    assert raised.value.__cause__ is error


def test_other_sqlalchemy_error_becomes_backend_error() -> None:
    error = exc.SQLAlchemyError("sqlalchemy failed")

    with pytest.raises(BackendError) as raised:
        _raise_from_write_session(error)

    assert type(raised.value) is BackendError
    assert raised.value.__cause__ is error
