from pymysql.constants import ER
from pymysql import err as pexc
from sqlalchemy import exc


def is_unique_violation(error: exc.IntegrityError) -> bool:
    orig = error.orig

    return (
        isinstance(orig, pexc.IntegrityError)
        and bool(orig.args)
        and orig.args[0] == ER.DUP_ENTRY
    )
