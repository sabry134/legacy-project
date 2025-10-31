End-to-End Tests Documentation
==============================

Overview
--------

The end-to-end (E2E) tests in ``tests/e2e/test_full_application_workflows.py`` verify the complete application stack from Flask API endpoints down to the database layer. These tests simulate realistic user workflows and ensure all components work together correctly.

Test Architecture
------------------

Stack Under Test
~~~~~~~~~~~~~~~~

The E2E tests exercise:

1. **Flask API Layer**: All HTTP endpoints and request/response handling
2. **Application Layer**: Use cases and business logic
3. **Repository Layer**: PostgreSQL/SQLite persistence
4. **Database**: SQLite in-memory database (or PostgreSQL if configured)

Test Setup
~~~~~~~~~~

.. code-block:: python

   @pytest.fixture(autouse=True)
   def _db():
       """Sets up in-memory SQLite database for each test"""
       # Creates fresh database for each test

   @pytest.fixture
   def app():
       """Creates Flask app with PostgreSQL repository implementations"""
       # Overrides DI container with PostgreSQL repositories

   @pytest.fixture
   def client(app):
       """Flask test client for making HTTP requests"""

Why PostgreSQL Adapters?
~~~~~~~~~~~~~~~~~~~~~~~~

Although the tests use SQLite in-memory by default, they use the **PostgreSQL adapter classes** (``PostgresPersonRepository``, etc.). This ensures:

- Tests use the same SQLAlchemy-based repositories as production
- Tests exercise real database interactions
- Switching to a real PostgreSQL database is straightforward (change ``DATABASE_URL``)

Test Suites
-----------

1. TestFullFamilyTreeWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify multi-generation family tree creation and querying.

**Test**: ``test_create_family_tree_with_generations``

**What it tests**:

- Creating persons across multiple generations
- Creating family relationships
- Adding children to families
- Querying ancestors through the API
- Verifying ancestor relationships are correctly returned

**Workflow**:

1. Create great-grandparents
2. Create their family
3. Add grandparents as children
4. Create parents generation
5. Create current generation
6. Query ancestors for a person
7. Verify all ancestor generations are returned

2. TestGEDCOMImportExportWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify GEDCOM import/export with events and date qualifiers.

**Test**: ``test_import_export_roundtrip_with_events_and_qualifiers``

**What it tests**:

- Importing GEDCOM data through the API
- Verifying imported persons, families, and sources
- Verifying events are imported
- Verifying date qualifiers are preserved
- Exporting data back to GEDCOM
- Verifying round-trip data integrity

**Workflow**:

1. Create GEDCOM string with events and date qualifiers
2. Import via ``/gedcom/import``
3. Verify import statistics
4. Retrieve imported persons and families
5. Verify events and dates
6. Export via ``/gedcom/export``
7. Verify exported GEDCOM matches original structure

3. TestEventManagementWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify event creation and enrichment features.

**Tests**:

- ``test_create_and_enrich_person_event``
- ``test_create_and_enrich_family_event``

**What it tests**:

- Creating person events (baptism, burial, etc.)
- Creating family events (marriage, divorce)
- Adding notes to events
- Adding sources to events
- Adding witnesses to events
- Changing event probability
- Retrieving enriched events

**Workflow** (Person Event):

1. Create a person
2. Create a person event
3. Add note to event
4. Create and add source to event
5. Verify event has note and source when retrieved

**Workflow** (Family Event):

1. Create parents and family
2. Create marriage event
3. Change event probability
4. Verify probability persists

4. TestGenealogyOperationsWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify genealogy operations through the API.

**Tests**:

- ``test_find_kinship_path``
- ``test_merge_duplicate_persons``

**What it tests**:

- Finding kinship paths between persons
- Merging duplicate person records
- Verifying family relationships are updated after merge
- Verifying merged person no longer exists

**Workflow** (Kinship Path):

1. Create multi-generation family tree
2. Find kinship path between distant relatives
3. Verify path is returned correctly

**Workflow** (Merge Duplicates):

1. Create two duplicate persons
2. Add one to a family
3. Merge duplicates
4. Verify duplicate is deleted
5. Verify family now references the primary person

5. TestSearchAndPaginationWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify search and pagination features.

**Tests**:

- ``test_person_search_and_pagination``
- ``test_source_search``

**What it tests**:

- Paginating through persons
- Searching sources by description
- Verifying pagination limits results correctly
- Verifying search returns relevant results

**Workflow**:

1. Create multiple persons/sources
2. Test pagination with page size limits
3. Test search functionality
4. Verify results are correct

6. TestRelationshipManagementWorkflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Verify relationship CRUD operations.

**Test**: ``test_create_and_list_relationships``

**What it tests**:

- Creating relationships between persons
- Listing relationships with pagination
- Verifying relationship types are correct

**Workflow**:

1. Create two persons
2. Create relationship between them
3. List relationships with pagination
4. Verify relationship appears in list

7. TestComplexWorkflow
~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Comprehensive end-to-end scenario testing multiple features.

**Test**: ``test_complete_genealogy_workflow``

**What it tests**:

- Complete workflow combining multiple features
- Creating persons, families, events
- Performing genealogy operations
- Verifying data integrity across operations

Running E2E Tests
-----------------

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Run all E2E tests
   pytest tests/e2e/

   # Run specific test class
   pytest tests/e2e/test_full_application_workflows.py::TestFullFamilyTreeWorkflow

   # Run specific test
   pytest tests/e2e/test_full_application_workflows.py::TestFullFamilyTreeWorkflow::test_create_family_tree_with_generations

   # Run with verbose output
   pytest tests/e2e/ -v

   # Run with extra verbose output (print statements)
   pytest tests/e2e/ -vv -s

With Coverage
~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/e2e/ --cov=src --cov-report=html

Using PostgreSQL Database
~~~~~~~~~~~~~~~~~~~~~~~~~

By default, tests use SQLite in-memory. To use PostgreSQL:

.. code-block:: bash

   export DATABASE_URL="postgresql://user:password@localhost:5432/test_db"
   pytest tests/e2e/

**Note**: Ensure the test database exists and is empty.

Test Data Management
--------------------

Database Isolation
~~~~~~~~~~~~~~~~~~

Each test runs with a fresh database:

- ``_db`` fixture resets the database before each test
- Tests are independent and can run in any order
- No test data leaks between tests

Test Fixtures
~~~~~~~~~~~~~

- ``_db``: Database setup/teardown (auto-use)
- ``app``: Flask application instance
- ``client``: Flask test client for HTTP requests

Best Practices
--------------

Writing E2E Tests
~~~~~~~~~~~~~~~~~

1. **Test Real Workflows**: Simulate actual user interactions
2. **Verify Complete Stack**: Test API → Use Case → Repository → Database
3. **Use Real Repositories**: Use PostgreSQL adapters, not mocks
4. **Assert on Responses**: Verify HTTP status codes and response data
5. **Test Error Cases**: Include negative test cases when relevant

Test Structure
~~~~~~~~~~~~~~

.. code-block:: python

   class TestFeatureWorkflow:
       def test_feature_name(self, client):
           """Brief description of what this test verifies"""
           # Arrange: Set up test data
           # Act: Make API calls
           # Assert: Verify results

Troubleshooting
---------------

Tests Failing with Database Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure ``DATABASE_URL`` is set correctly if using PostgreSQL
- Check database permissions
- Verify database schema is up to date

Tests Failing with Import Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure all dependencies are installed: ``pip install -r requirements.txt``
- Verify virtual environment is activated

Tests Timing Out
~~~~~~~~~~~~~~~~

- Check for infinite loops in test code
- Verify database operations are completing
- Consider increasing test timeout if using slow database

Coverage Goals
--------------

E2E tests should cover:

- ✅ All major API endpoints
- ✅ Complete workflows (create → read → update → delete)
- ✅ Cross-feature interactions (e.g., events with sources)
- ✅ Error handling and edge cases
- ✅ Data persistence and retrieval

Future Enhancements
-------------------

Potential additions to E2E test suite:

- Performance tests for large datasets
- Concurrent request handling
- API rate limiting
- Authentication/authorization (when implemented)
- Advanced genealogy operations edge cases
