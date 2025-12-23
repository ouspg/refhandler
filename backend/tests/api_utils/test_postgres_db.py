# pylint: disable=invalid-name, missing-function-docstring
from backend.app.postgres_db import init_db_tables, create_default_admin


def test_init_db_tables(engine):
    init_db_tables(engine)
    

def test_create_default_admin(engine):
    init_db_tables(engine)
    create_default_admin(engine)

    # Try to create default admin again
    create_default_admin(engine)