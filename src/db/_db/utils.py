from contextlib import contextmanager
from collections.abc import Generator
from typing import Optional

from pymysql.constants import ER
from pymysql import err as pexc
from sqlalchemy import exc
from sqlmodel import Session

from .engine import DBEngine as db
from ..common import (
    DBError,
    AlreadyExistsError,
    BackendError,
    BackendTimeoutError,
    BackendUnavailableError,
    DataIntegrityError,
)


def is_unique_violation(error: exc.IntegrityError) -> bool:
    orig = error.orig

    return (
        isinstance(orig, pexc.IntegrityError)
        and bool(orig.args)
        and orig.args[0] == ER.DUP_ENTRY
    )


@contextmanager
def write_session(
    ss: Optional[Session] = None,
) -> Generator[Session, None, None]:
    try:
        if ss is None:
            with db.session() as session:
                yield session
                session.commit()
        else:
            yield ss
            ss.flush()

    except DBError:
        raise

    except exc.IntegrityError as e:
        if is_unique_violation(e):
            raise AlreadyExistsError() from e
        raise DataIntegrityError() from e

    except exc.TimeoutError as e:
        raise BackendTimeoutError() from e

    except exc.DBAPIError as e:
        if e.connection_invalidated:
            raise BackendUnavailableError() from e

        raise BackendError() from e

    except exc.SQLAlchemyError as e:
        raise BackendError() from e
