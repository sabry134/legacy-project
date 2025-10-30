Postgres Adapters - Technical Guide
====================================

This document explains how the SQLAlchemy\-based Postgres adapters are structured, configured, and used across the project.

Overview
~~~~~~~~

- Adapters live under `src/infrastructure/adapters/persistence/postgres/`
- They implement outbound repository ports from `src/application/ports/outbound/`
- SQLAlchemy is used for ORM mapping; repositories translate between domain entities and DB models
- For tests/dev, adapters default to SQLite in\-memory unless `DATABASE_URL` is set

Files and Responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**base.py**

- Engine/session bootstrap (lazy)
- Defaults to `sqlite+pysqlite:///:memory:` when `DATABASE_URL` is not provided
- `init_db()`: create all tables
- `reset_db()`: drop and recreate all tables (test isolation)

**models.py**

- SQLAlchemy models: `PersonModel`, `FamilyModel`, `RelationshipModel`, `SourceModel`, `TitleModel`, `PersonEventModel`, `FamilyEventModel`, and `family_children` join table

**Repositories (implement outbound ports)**

- `person_repository.py` → `PostgresPersonRepository`
- `family_repository.py` → `PostgresFamilyRepository`
- `relationship_repository.py` → `PostgresRelationshipRepository`
- `source_repository.py` → `PostgresSourceRepository`
- `title_repository.py` → `PostgresTitleRepository`
- `person_event_repository.py` → `PostgresPersonEventRepository`
- `family_event_repository.py` → `PostgresFamilyEventRepository`

**Migrations (simple, metadata\-driven)**

- `migration_repository.py` → `PostgresMigrationRepository` (ensures tables, tracks version)
- `run_migrations.py` → CLI entry point

Configuration
~~~~~~~~~~~~~~

Adapters use one of the following to determine the connection string:

- `DATABASE_URL` (highest priority), e.g. `postgresql+psycopg2://user:pass@localhost:5432/geneweb`
- Otherwise falls back to `sqlite+pysqlite:///:memory:`

Export for Postgres:

.. code-block:: bash

    export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/geneweb

Table Initialization and Migrations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quick create (no version tracking):

.. code-block:: python

    from src.infrastructure.adapters.persistence.postgres.base import init_db
    init_db()

Migration repository (creates tables and stamps a version):

.. code-block:: bash

    python -m src.infrastructure.adapters.persistence.postgres.run_migrations

Domain ↔ Persistence Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Value objects are serialized:

  - `Date` → `{ type: 'exact'|'approximate'|..., value: 'YYYY-MM-DD'|... }`
  - `Place` → `{ name, country, region, city }`

- Enums are stored as strings (e.g., `Gender.MALE` → "M", event/relationship types → enum `value`)
- Many\-to\-many `Family.children` uses a join table `family_children`
- `FamilyEvent` includes a `family_id` FK to support `find_by_family`

Using Postgres Adapters via DI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default DI uses in\-memory repos. Override per environment to use Postgres:

.. code-block:: python

    from src.infrastructure.adapters.persistence.postgres.person_repository import PostgresPersonRepository
    from src.infrastructure.adapters.persistence.postgres.family_repository import PostgresFamilyRepository
    from src.shared.containers import container
    from dependency_injector import providers

    container.person_repository.override(providers.Factory(PostgresPersonRepository))
    container.family_repository.override(providers.Factory(PostgresFamilyRepository))

For tests (SQLite in\-memory): the fixtures set `DATABASE_URL` and call `reset_db()` automatically.

Testing Strategy
~~~~~~~~~~~~~~~~

- Unit tests (`tests/unit/*_pg_*`): validate repository behavior in isolation
- Integration tests (`tests/integration/pg/*.py`): one file per entity adapter covering CRUD + finders
- DI integration test: `tests/integration/test_pg_di_use_cases.py` wires use cases to Postgres adapters to validate end\-to\-end flows

Common Pitfalls and Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure engine is created lazily (handled in `base.py`) to allow tests to set `DATABASE_URL` before first use
- Deleting `Family` does not require manual cleanup of `family_children`; SQLAlchemy handles association row deletion
- If you switch to a real Postgres instance locally, ensure the DB exists and the user has privileges; run `run_migrations.py` before starting the app

Example: Switching the Flask App to Postgres
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In your app startup (before serving requests):

.. code-block:: python

    from dependency_injector import providers
    from src.shared.containers import container
    from src.infrastructure.adapters.persistence.postgres.person_repository import PostgresPersonRepository
    from src.infrastructure.adapters.persistence.postgres.family_repository import PostgresFamilyRepository
    from src.infrastructure.adapters.persistence.postgres.base import init_db

    init_db()
    container.person_repository.override(providers.Factory(PostgresPersonRepository))
    container.family_repository.override(providers.Factory(PostgresFamilyRepository))

Now the `PersonUseCase`/`FamilyUseCase` will operate against the SQL database.
