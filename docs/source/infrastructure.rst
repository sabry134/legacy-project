Infrastructure Layer
====================

In-Memory Repositories
----------------------

- Implement repository interfaces in memory.
- Useful for **unit testing** or temporary storage.
- Example: ``PersonRepositoryImpl`` in ``in_memory`` directory.

SQL Repositories
----------------

- Implement repository interfaces using **SQLAlchemy**.
- Example: ``SqlAlchemyPersonRepository`` uses ``PersonModel`` to persist data.
- Database connection managed in ``infrastructure/db/sql_db/db.py``.
- Initialization scripts in ``init_db.py``.
