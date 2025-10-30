Quick Start Guide
=================

This guide will help you get GeneWeb Python up and running quickly.

Running the DI Demo
~~~~~~~~~~~~~~~~~~~

The project includes a dependency injection demo:

.. code-block:: bash

    python -m src.main

This demonstrates the hexagonal architecture with automatic dependency resolution.

Running the Flask Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation
^^^^^^^^^^^^

Install dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Start the Server
^^^^^^^^^^^^^^^^

.. code-block:: bash

    python -m src.infrastructure.adapters.web.flask_app

The server starts on `http://localhost:8000` by default.

API Documentation
~~~~~~~~~~~~~~~~~

After starting the server, access Swagger UI:

- **Swagger UI**: `http://localhost:8000/apidocs`

Interactive API exploration with request/response examples.

REST Endpoints
~~~~~~~~~~~~~~

Persons Management
^^^^^^^^^^^^^^^^^^^

- `GET /persons/` - List all persons
- `POST /persons/` - Create a new person
- `GET /persons/<id>` - Get a specific person
- `PUT /persons/<id>` - Update a person
- `DELETE /persons/<id>` - Delete a person

Families Management
^^^^^^^^^^^^^^^^^^^

- `GET /families/` - List all families
- `POST /families/` - Create a new family
- `GET /families/<id>` - Get a specific family
- `DELETE /families/<id>` - Delete a family
- `POST /families/<id>/children` - Add children to a family

Quick curl Examples
~~~~~~~~~~~~~~~~~~~

List All Persons
^^^^^^^^^^^^^^^^

.. code-block:: bash

    curl -s http://localhost:8000/persons/ | jq

Create a Person
^^^^^^^^^^^^^^^

.. code-block:: bash

    curl -s -X POST http://localhost:8000/persons/ \
      -H 'Content-Type: application/json' \
      -d '{
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M"
      }' | jq

Create a Family
^^^^^^^^^^^^^^^

Assuming you already created two persons with IDs 1 and 2:

.. code-block:: bash

    curl -s -X POST http://localhost:8000/families/ \
      -H 'Content-Type: application/json' \
      -d '{
        "parent_1_id": 1,
        "parent_2_id": 2
      }' | jq

Postgres Persistence
~~~~~~~~~~~~~~~~~~~~

Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure Postgres connection via environment variables:

- `DATABASE_URL` - Full connection string (overrides all others)
  - Example: `postgresql+psycopg2://user:pass@localhost:5432/geneweb`
- `PGUSER` - Postgres username (default: `postgres`)
- `PGPASSWORD` - Postgres password (default: `postgres`)
- `PGHOST` - Postgres hostname (default: `localhost`)
- `PGPORT` - Postgres port (default: `5432`)
- `PGDATABASE` - Database name (default: `geneweb`)

Initialize Database
^^^^^^^^^^^^^^^^^^^

Initialize tables once using Python:

.. code-block:: python

    from src.infrastructure.adapters.persistence.postgres.base import init_db
    init_db()

Or run the migration script:

.. code-block:: bash

    python -m src.infrastructure.adapters.persistence.postgres.run_migrations

This creates tables and stamps a version.

Using Postgres Adapters
^^^^^^^^^^^^^^^^^^^^^^^

Override the default in\-memory repositories with Postgres adapters:

.. code-block:: python

    from src.infrastructure.adapters.persistence.postgres.person_repository import PostgresPersonRepository
    from src.infrastructure.adapters.persistence.postgres.family_repository import PostgresFamilyRepository
    from src.shared.containers import container

    # Override DI to use Postgres instead of in-memory
    container.person_repository.override(lambda: PostgresPersonRepository())
    container.family_repository.override(lambda: PostgresFamilyRepository())

**Note:** The default DI container uses in\-memory repositories for simplicity. Switch to Postgres overrides in your application startup when a database is available.

Next Steps
~~~~~~~~~~

- Read :doc:`gedcom_import_export` for GEDCOM import/export functionality
- Check :doc:`usage` for detailed API usage patterns
- See :doc:`testing` for running tests
