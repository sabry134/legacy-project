Test Plan
=========

Overview
--------

This document outlines the comprehensive test plan for the GeneWeb Python application. The testing strategy follows a three-tier approach: Unit Tests, Integration Tests, and End-to-End Tests.

Test Strategy
-------------

Testing Pyramid
~~~~~~~~~~~~~~~

::

         /\
        /  \  E2E Tests (10%)
       /----\
      /      \  Integration Tests (30%)
     /--------\
    /          \  Unit Tests (60%)
   /------------\

Test Types
~~~~~~~~~~

1. **Unit Tests**: Fast, isolated tests for domain entities, value objects, and pure functions
2. **Integration Tests**: Tests for use cases with repository implementations
3. **E2E Tests**: Full stack tests from API to database

Test Coverage Areas
-------------------

1. Domain Layer
~~~~~~~~~~~~~~~

Entities
^^^^^^^^

- **Person**

  - ✅ Creation with required fields
  - ✅ Name validation
  - ✅ Date handling (birth, death)
  - ✅ Place handling
  - ✅ Title management
  - ✅ Edge cases (missing dates, invalid names)

- **Family**

  - ✅ Creation with parents
  - ✅ Adding/removing children
  - ✅ Parent swapping
  - ✅ Family name generation
  - ✅ Completeness checks

- **PersonEvent**

  - ✅ Event type validation
  - ✅ Date and place handling
  - ✅ Notes management
  - ✅ Sources management
  - ✅ Witnesses management
  - ✅ Probability handling

- **FamilyEvent**

  - ✅ Similar to PersonEvent
  - ✅ Family association

- **Relationship**

  - ✅ Relationship type validation
  - ✅ Self-relationship prevention
  - ✅ Person relinking (for merge operations)

- **Source**

  - ✅ Description validation
  - ✅ CRUD operations

- **Title**

  - ✅ Title text validation
  - ✅ CRUD operations

Value Objects
^^^^^^^^^^^^^

- **EntityId**

  - ✅ ID generation and validation

- **Name**

  - ✅ String validation
  - ✅ Empty string handling

- **Date**

  - ✅ Exact date creation
  - ✅ Approximate date creation
  - ✅ Date qualifiers (ABT, CAL, EST, BEFORE, AFTER, BETWEEN)
  - ✅ GEDCOM date string formatting

- **Place**

  - ✅ Place name handling
  - ✅ Optional fields (country, region, city)

- **Gender**

  - ✅ Enum values (M, F, U)

2. Application Layer
~~~~~~~~~~~~~~~~~~~~

Use Cases
^^^^^^^^^

- **PersonUseCase**

  - ✅ Create person
  - ✅ Get person by ID
  - ✅ List all persons
  - ✅ Update person
  - ✅ Delete person
  - ✅ Pagination
  - ✅ Title management
  - ✅ Appearance count increment

- **FamilyUseCase**

  - ✅ Create family
  - ✅ Get family by ID
  - ✅ List families
  - ✅ Add/remove children
  - ✅ Set parents
  - ✅ Swap parents
  - ✅ Source and comment management

- **PersonEventUseCase**

  - ✅ Create person event
  - ✅ Get event by ID
  - ✅ List events
  - ✅ Update event
  - ✅ Delete event
  - ✅ Add/remove notes
  - ✅ Add/remove sources
  - ✅ Add/remove witnesses
  - ✅ Change probability
  - ✅ Find by person
  - ✅ Find by type
  - ✅ Pagination

- **FamilyEventUseCase**

  - ✅ Similar to PersonEventUseCase
  - ✅ Find by family

- **RelationshipUseCase**

  - ✅ Create relationship
  - ✅ Get relationship by ID
  - ✅ List relationships
  - ✅ Delete relationship
  - ✅ Pagination

- **SourceUseCase**

  - ✅ Create source
  - ✅ Get source by ID
  - ✅ List sources
  - ✅ Update source
  - ✅ Delete source
  - ✅ Search sources
  - ✅ Pagination

- **TitleUseCase**

  - ✅ Create title
  - ✅ Get title by ID
  - ✅ List titles
  - ✅ Update title
  - ✅ Delete title
  - ✅ Search titles
  - ✅ Pagination

- **GenealogyUseCase**

  - ✅ Get ancestors (with depth)
  - ✅ Get descendants (with depth)
  - ✅ Get relatives
  - ✅ Find kinship path
  - ✅ Merge duplicate persons
  - ✅ Edge cases (circular relationships, missing persons)

- **GedcomUseCase**

  - ✅ Import GEDCOM file
  - ✅ Import GEDCOM string
  - ✅ Export GEDCOM file
  - ✅ Export GEDCOM string
  - ✅ Event mapping
  - ✅ Date qualifier handling
  - ✅ Error reporting

3. Infrastructure Layer
~~~~~~~~~~~~~~~~~~~~~~~~

Repository Implementations
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **PostgreSQL Repositories**

  - ✅ Save operations
  - ✅ Get by ID
  - ✅ Get all
  - ✅ Delete operations
  - ✅ Find operations
  - ✅ Exists checks
  - ✅ Relationship persistence (join tables)
  - ✅ Notes persistence (JSON)
  - ✅ Sources/witnesses persistence (join tables)

- **In-Memory Repositories** (for testing)

  - ✅ Similar coverage as PostgreSQL repositories

GEDCOM Adapters
^^^^^^^^^^^^^^^

- **Parser**

  - ✅ Parse HEAD record
  - ✅ Parse INDI records
  - ✅ Parse FAM records
  - ✅ Parse SOUR records
  - ✅ Handle nested tags
  - ✅ Extract XREF IDs
  - ✅ Error reporting for invalid lines

- **Mapper**

  - ✅ Map person records
  - ✅ Map family records
  - ✅ Map source records
  - ✅ Map events (birth, death, baptism, burial, marriage, divorce)
  - ✅ Parse dates with qualifiers
  - ✅ Handle missing references

- **Writer**

  - ✅ Write HEAD
  - ✅ Write INDI records
  - ✅ Write FAM records
  - ✅ Write SOUR records
  - ✅ Write events
  - ✅ Format dates with qualifiers
  - ✅ Generate XREF IDs

Web Adapters (Flask)
^^^^^^^^^^^^^^^^^^^^

- **API Endpoints**

  - ✅ All CRUD endpoints
  - ✅ Pagination endpoints
  - ✅ Search endpoints
  - ✅ Enrichment endpoints (notes, sources, witnesses)
  - ✅ Genealogy endpoints
  - ✅ GEDCOM endpoints
  - ✅ Error handling (400, 404, 500)
  - ✅ Request validation
  - ✅ Response serialization

- **Swagger Documentation**

  - ✅ All endpoints documented
  - ✅ Request/response schemas
  - ✅ Examples provided

4. End-to-End Workflows
~~~~~~~~~~~~~~~~~~~~~~~~

- ✅ Multi-generation family tree creation
- ✅ GEDCOM import/export round-trip
- ✅ Event creation and enrichment
- ✅ Genealogy operations (ancestors, descendants, kinship)
- ✅ Person duplicate merging
- ✅ Search and pagination
- ✅ Relationship management
- ✅ Complex multi-feature workflows

Test Execution
--------------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # All tests
   pytest

   # By category
   pytest tests/unit/
   pytest tests/integration/
   pytest tests/e2e/

   # With coverage
   pytest --cov=src --cov-report=html

   # Specific test
   pytest tests/unit/test_person.py::TestPerson::test_create_person

   # Verbose output
   pytest -v

   # Stop on first failure
   pytest -x

Test Environment
~~~~~~~~~~~~~~~~

- **Default**: SQLite in-memory database
- **Production-like**: Set ``DATABASE_URL`` for PostgreSQL
- **Isolation**: Each test gets a fresh database

Test Data Management
--------------------

Fixtures
~~~~~~~~

- ``_db``: Database setup/teardown (integration and E2E tests)
- Repository fixtures: PostgreSQL implementations for integration tests
- Mock repositories: In-memory implementations for unit tests

Test Data Patterns
~~~~~~~~~~~~~~~~~~~

- **Minimal Data**: Tests use only necessary data
- **Realistic Data**: E2E tests use realistic family tree structures
- **Edge Cases**: Tests include boundary conditions
- **Clean State**: Each test starts with a clean database

Coverage Metrics
----------------

Current Coverage
~~~~~~~~~~~~~~~~

- **Unit Tests**: ~60% of codebase
- **Integration Tests**: ~30% of codebase
- **E2E Tests**: ~10% of critical workflows

Target Coverage
~~~~~~~~~~~~~~~

- **Overall**: >80% code coverage
- **Critical Paths**: 100% coverage
- **Domain Layer**: 100% coverage
- **Use Cases**: >90% coverage

Test Maintenance
----------------

When to Add Tests
~~~~~~~~~~~~~~~~~

- New feature implementation
- Bug fixes (regression tests)
- Refactoring (ensure behavior unchanged)
- Performance improvements

Test Quality Checklist
~~~~~~~~~~~~~~~~~~~~~~

- [ ] Test name clearly describes what is being tested
- [ ] Test is independent (no dependencies on other tests)
- [ ] Test is repeatable (consistent results)
- [ ] Test covers both success and failure cases
- [ ] Test assertions are clear and specific
- [ ] Test data is minimal and appropriate

Known Test Limitations
----------------------

1. **Concurrency**: Tests don't currently cover concurrent access scenarios
2. **Performance**: No performance benchmarks in test suite
3. **Security**: Authentication/authorization tests pending implementation
4. **Large Datasets**: Limited testing with very large datasets (>1000 records)

Future Test Enhancements
------------------------

1. **Performance Tests**

   - Large dataset handling
   - Query performance benchmarks
   - Memory usage profiling

2. **Load Tests**

   - Concurrent request handling
   - Stress testing
   - Database connection pooling

3. **Security Tests**

   - Input sanitization
   - SQL injection prevention
   - Authentication/authorization

4. **Mutation Testing**

   - Validate test quality
   - Identify weak tests

Test Documentation
------------------

- **E2E Tests**: See :doc:`e2e_tests`
- **GEDCOM Tests**: See :doc:`gedcom_import_export` (see testing section)
- **Architecture**: See :doc:`architecture_overview`

Continuous Integration
----------------------

Recommended CI Setup
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Example GitHub Actions workflow
   - Run unit tests
   - Run integration tests
   - Run E2E tests
   - Generate coverage report
   - Upload coverage to service (Codecov, Coveralls)
   - Fail build if coverage drops below threshold

Pre-commit Hooks
~~~~~~~~~~~~~~~~

- Run linter
- Run unit tests
- Check code formatting

Conclusion
----------

This test plan ensures comprehensive coverage of the GeneWeb Python application across all layers. Regular test execution and maintenance are essential for maintaining code quality and preventing regressions.
