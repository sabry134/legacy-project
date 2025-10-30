Introduction
=============

Welcome to GeneWeb-Python, a genealogical database management system built with a modern **hexagonal architecture** (Ports and Adapters pattern) for maximum scalability, testability, and maintainability.

What is GeneWeb-Python?
~~~~~~~~~~~~~~~~~~~~~~~

GeneWeb-Python is a clean, modular implementation of a genealogical information system featuring:

- **Rich domain model** for managing persons, families, relationships, events, sources, and titles
- **Hexagonal architecture** providing clear separation of concerns and dependency inversion
- **Comprehensive testing** with 41 tests achieving 100% pass rate
- **Multiple persistence options** including in-memory storage and PostgreSQL adapters
- **Dependency injection system** for flexible, testable component management
- **CI/CD pipeline** with automated testing and Docker deployment

Architecture at a Glance
~~~~~~~~~~~~~~~~~~~~~~~~

GeneWeb-Python follows a **three-layer hexagonal architecture**:

.. code-block:: text

    External Systems → Infrastructure Layer → Application Layer → Domain Layer

**Domain Layer (Core)**

The heart of the system containing:

- **Entities**: Person, Family, Relationship, Event, Source, Title
- **Value Objects**: EntityId, Name, Date, Gender, Place (immutable, validated data structures)
- **Repository Interfaces**: Define contracts for data persistence

**Application Layer (Use Cases)**

Orchestrates business workflows:

- **Inbound Ports**: Use case interfaces consumed by adapters (e.g., controllers)
- **Outbound Ports**: Repository interfaces defining infrastructure dependencies
- **Use Cases**: Business logic orchestration with no framework coupling

**Infrastructure Layer (Adapters)**

Implements concrete integrations:

- **Persistence Adapters**: In-memory and PostgreSQL repositories
- **Web Adapters**: Flask blueprints for HTTP endpoints
- **Dependency Injection**: Container for automatic service wiring

Key Principles
~~~~~~~~~~~~~~

✅ **Dependency Inversion**
   Core business logic is independent of external frameworks and details depend on abstractions

✅ **High Testability**
   Each layer tested in isolation with mocks; no framework coupling in domain code

✅ **High Modularity**
   Clear boundaries enable easy feature addition and implementation swapping

✅ **High Scalability**
   Modular design supports growth from in-memory to distributed persistence strategies

Quick Start
~~~~~~~~~~~

Initialize and use the system in three steps:

.. code-block:: python

    from src.shared.di_container import DIContainer
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.gender import Gender
    from src.application.ports.inbound.person_use_case import PersonUseCase

    # 1. Initialize container
    container = DIContainer()

    # 2. Get use case
    person_use_case = container.get(PersonUseCase)

    # 3. Create a person
    person = person_use_case.create_person(
        first_name=Name("John"),
        last_name=Name("Doe"),
        gender=Gender.MALE
    )

Core Concepts
~~~~~~~~~~~~~

**Entities**
   Rich domain objects with business logic. Examples: Person, Family, Event

**Value Objects**
   Immutable, validated data structures. Examples: Name, Date, Gender, Place

**Repositories**
   Abstractions for data persistence. Multiple implementations (in-memory, SQL, NoSQL)

**Use Cases**
   Business workflow orchestrators. They coordinate entities and repositories

**Adapters**
   Concrete implementations of ports. Examples: PostgresPersonRepository, Flask blueprints

**Ports**
   Interfaces defining contracts between layers. Inbound (use cases) and outbound (repositories)

Key Features
~~~~~~~~~~~~

- ✅ Immutable value objects with validation
- ✅ Rich domain entities with business rules
- ✅ Repository pattern for data abstraction
- ✅ Dependency injection for loose coupling
- ✅ Multiple persistence backends (in-memory, PostgreSQL)
- ✅ RESTful API via Flask blueprints
- ✅ Comprehensive test coverage (unit, integration, e2e)
- ✅ Clean error handling and propagation
- ✅ Performance optimization (caching, lazy loading)

Next Steps
~~~~~~~~~~

1. **For Developers**: Start with :doc:`architecture_overview` to understand the structure
2. **For DevOps**: See :doc:`deployment` for CI/CD and Docker setup
3. **For Integration**: Check :doc:`usage` and :doc:`postgres_adapter` for integration examples
4. **For Contributors**: Review :doc:`standards` and :doc:`testing` for contribution guidelines

Benefits
~~~~~~~~

**Maintainability**
   Clear separation of concerns makes code easy to understand and modify

**Testability**
   Each layer independently testable; no framework dependencies in domain logic

**Flexibility**
   Easy to swap implementations (e.g., different databases, APIs)

**Scalability**
   Modular design supports growth from single-server to distributed systems

**Independence**
   Core business logic is framework-agnostic and reusable

Status
~~~~~~

✅ **Complete** – Hexagonal architecture fully implemented with 100% test coverage

- Domain Layer: Complete with entities, value objects, and repository interfaces
- Application Layer: Use cases and ports fully implemented
- Infrastructure Layer: In-memory and PostgreSQL adapters ready
- Dependency Injection: Custom container with automatic wiring
- Testing: Comprehensive coverage (unit, integration, e2e)
- Documentation: Complete architecture and technical guides

Questions?
~~~~~~~~~~

Refer to the relevant documentation sections or review the code examples throughout this documentation.

Happy coding! 🚀