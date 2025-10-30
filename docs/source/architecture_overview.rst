Architecture Quick Reference
=============================

**Hexagonal Architecture (Ports and Adapters)** with three main layers:

.. code-block:: text

    External Systems → Infrastructure Layer → Application Layer → Domain Layer

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    src/
    ├── domain/                    # Core business logic
    │   ├── entities/             # Domain entities (Person, Family, etc.)
    │   ├── value_objects/        # Immutable value objects
    │   └── repositories/         # Repository interfaces (ports)
    ├── application/              # Application layer
    │   ├── use_cases/           # Use case implementations
    │   └── ports/               # Application ports
    │       ├── inbound/         # Inbound ports (use case interfaces)
    │       └── outbound/        # Outbound ports (repository interfaces)
    ├── infrastructure/          # Infrastructure layer
    │   └── adapters/           # Adapters implementing ports
    │       └── persistence/    # Database adapters
    ├── shared/                 # Shared utilities
    │   └── di_container.py     # Dependency injection container
    └── main.py                 # Application entry point

    tests/
    ├── unit/                   # Unit tests (41 tests)
    ├── integration/            # Integration tests
    └── e2e/                   # End-to-end tests

Key Components
~~~~~~~~~~~~~~

Domain Layer (Core)
^^^^^^^^^^^^^^^^^^^

- **Entities**: Person, Family, Relationship, Event, Source, Title
- **Value Objects**: EntityId, Name, Date, Gender, Place
- **Repository Interfaces**: PersonRepository, FamilyRepository, etc.

Application Layer (Use Cases)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Use Cases (Application services)**: Orchestrate business flows by calling domain entities and outbound ports. They contain no framework code. Examples: `PersonUseCaseImpl`, `FamilyUseCaseImpl`.
- **Ports**:

  - **Inbound ports** define the use case API consumed by adapters (e.g., controllers): `src/application/ports/inbound/*`.
  - **Outbound ports** define dependencies on infrastructure (repositories): `src/application/ports/outbound/*`.

Infrastructure Layer (Adapters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Persistence adapters** implement outbound ports (e.g., `InMemoryPersonRepository`, `InMemoryFamilyRepository`).
- **Web adapters (Flask blueprints)** implement inbound delivery using HTTP but call only inbound ports (use cases). They never talk directly to repositories. See:

  - `src/infrastructure/adapters/web/blueprints/person_api.py`
  - `src/infrastructure/adapters/web/blueprints/family_api.py`
  - App factory: `src/infrastructure/adapters/web/flask_app.py`

Flow:

.. code-block:: text

    HTTP request → Flask blueprint (controller) → Inbound port (UseCase) → Outbound port (Repository Port) → Repository adapter (InMemory/DB)

Key rule: Controllers do not depend on repositories; they depend on use cases. Use cases depend on repository ports (interfaces), not concrete implementations.

Quick Start
~~~~~~~~~~~

.. code-block:: python

    from src.shared.di_container import DIContainer
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.gender import Gender
    from src.application.ports.inbound.person_use_case import PersonUseCase

    # Initialize container
    container = DIContainer()

    # Get use case
    person_use_case = container.get(PersonUseCase)

    # Create a person
    person = person_use_case.create_person(
        first_name=Name("John"),
        last_name=Name("Doe"),
        gender=Gender.MALE
    )

Common Patterns
~~~~~~~~~~~~~~~

Creating a New Entity
^^^^^^^^^^^^^^^^^^^^^

1. **Domain Entity**: `src/domain/entities/new_entity.py`
2. **Repository Interface**: `src/domain/repositories/new_entity_repository.py`
3. **Use Case Interface**: `src/application/ports/inbound/new_entity_use_case.py`
4. **Use Case Implementation**: `src/application/use_cases/new_entity_use_case_impl.py`
5. **Repository Adapter**: `src/infrastructure/adapters/persistence/in_memory_new_entity_repository.py`
6. **Register in DI Container**: `src/shared/di_container.py`

Adding a New Adapter
^^^^^^^^^^^^^^^^^^^^

1. **Implement existing port interface**
2. **Register in DI container**
3. **No changes needed to other layers**

Adding a New Interface
^^^^^^^^^^^^^^^^^^^^^^

1. **Create inbound port interface**
2. **Implement use case**
3. **Create adapter**
4. **Register in DI container**

Dependency Rules
~~~~~~~~~~~~~~~~

1. **Domain Layer**: No external dependencies
2. **Application Layer**: Depends only on Domain Layer
3. **Infrastructure Layer**: Depends on Application Layer
4. **Dependency Inversion**: All dependencies point inward

Common Issues
~~~~~~~~~~~~~

Import Errors
^^^^^^^^^^^^^

- Ensure all `__init__.py` files are present
- Check import paths are correct
- Verify DI container registration

Test Failures
^^^^^^^^^^^^^

- Check mock configurations
- Verify entity equality implementations
- Ensure proper dependency injection

Architecture Violations
^^^^^^^^^^^^^^^^^^^^^^^

- Domain layer should not import from other layers
- Use cases should only depend on domain and repository interfaces
- Adapters should implement port interfaces

Debugging Tips
~~~~~~~~~~~~~~

1. **Check DI Container**: Verify services are registered correctly
2. **Trace Dependencies**: Follow the dependency chain
3. **Test Isolation**: Run tests individually to identify issues
4. **Log Interactions**: Add logging to trace component interactions
5. **Validate Ports**: Ensure adapters implement port interfaces correctly
