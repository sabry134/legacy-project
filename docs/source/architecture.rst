Hexagonal Architecture Documentation
===================================

The GeneWeb Python project implements a **Hexagonal Architecture** (also known as Ports and Adapters), which provides:

- **High Testability**: Each layer can be tested in isolation
- **High Modularity**: Clear separation of concerns
- **High Scalability**: Easy to add new features and adapters
- **Dependency Inversion**: Core business logic doesn't depend on external frameworks

.. mermaid::
   :zoom:
   :caption: GeneWeb-Python Architecture Diagram
   :align: center

    graph TB
        subgraph "External Systems"
            UI[User Interface]
            API[REST API]
            CLI[CLI Interface]
            DB[(Database)]
        end

        subgraph "Infrastructure Layer (Adapters)"
            UIAdapter[UI Adapter]
            APIAdapter[API Adapter]
            CLIAdapter[CLI Adapter]
            DBAdapter[Database Adapter]
        end

        subgraph "Application Layer (Use Cases)"
            PersonUC[Person Use Case]
            FamilyUC[Family Use Case]
            RelationshipUC[Relationship Use Case]
        end

        subgraph "Domain Layer (Core)"
            Person[Person Entity]
            Family[Family Entity]
            Relationship[Relationship Entity]
            PersonRepo[Person Repository Interface]
            FamilyRepo[Family Repository Interface]
        end

        UI --> UIAdapter
        API --> APIAdapter
        CLI --> CLIAdapter

        UIAdapter --> PersonUC
        APIAdapter --> PersonUC
        CLIAdapter --> PersonUC

        PersonUC --> PersonRepo
        FamilyUC --> FamilyRepo

        PersonRepo --> DBAdapter
        FamilyRepo --> DBAdapter

        DBAdapter --> DB

Layer Descriptions
------------------

Domain Layer (Core Business Logic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The domain layer contains the core business logic and is completely independent of external concerns.

Entities
^^^^^^^^

Domain entities represent the core business objects with identity and behavior:

- **Person**: Represents a person in the genealogy system
- **Family**: Represents a family unit with parents and children
- **Relationship**: Represents relationships between persons
- **FamilyEvent**: Represents events related to families
- **Source**: Represents sources of information
- **Title**: Represents titles held by persons

Value Objects
^^^^^^^^^^^^^

Immutable objects that represent concepts without identity:

- **EntityId**: Unique identifier for entities
- **Name**: Person's name with validation
- **Date**: Date with type information (exact, approximate, etc.)
- **Gender**: Gender enumeration
- **Place**: Geographic location

Repository Interfaces (Ports)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define contracts for data access:

- **PersonRepository**: Contract for person data operations
- **FamilyRepository**: Contract for family data operations
- **RelationshipRepository**: Contract for relationship data operations

Application Layer (Use Cases)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application layer orchestrates the domain and coordinates with external systems.

Use Cases
^^^^^^^^^

Implement business workflows:

- **PersonUseCase**: Person-related business operations
- **FamilyUseCase**: Family-related business operations
- **RelationshipUseCase**: Relationship-related business operations

Ports
^^^^^

Define interfaces for external communication:

- **Inbound Ports**: Interfaces for external systems to interact with the application
- **Outbound Ports**: Interfaces for the application to interact with external systems

Infrastructure Layer (Adapters)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The infrastructure layer implements the ports defined in the application layer.

Adapters
^^^^^^^^

Concrete implementations of ports:

- **InMemoryPersonRepository**: In-memory implementation of person repository
- **InMemoryFamilyRepository**: In-memory implementation of family repository
- **SQLPersonRepository**: SQL database implementation (future)
- **RESTAPIAdapter**: REST API implementation (future)

Component Interactions
----------------------

Request Flow (Inbound)
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    sequenceDiagram
        participant Client
        participant Adapter
        participant UseCase
        participant Repository
        participant Domain

        Client->>Adapter: HTTP Request
        Adapter->>UseCase: execute()
        UseCase->>Domain: createEntity()
        UseCase->>Repository: save()
        Repository->>Domain: return entity
        UseCase->>Adapter: return result
        Adapter->>Client: HTTP Response

Data Persistence Flow (Outbound)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    sequenceDiagram
        participant UseCase
        participant Repository
        participant Adapter
        participant Database

        UseCase->>Repository: save(entity)
        Repository->>Adapter: convertToModel(entity)
        Adapter->>Database: INSERT/UPDATE
        Database->>Adapter: return data
        Adapter->>Repository: convertToEntity(data)
        Repository->>UseCase: return entity

Dependency Injection Flow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        subgraph "DI Container"
            Container[DI Container]
        end

        subgraph "Service Registration"
            Reg[Service Registration]
        end

        subgraph "Service Resolution"
            Res[Service Resolution]
        end

        Reg --> Container
        Container --> Res
        Res --> UseCase[Use Case]
        Res --> Repository[Repository]
        Res --> Adapter[Adapter]

Data Flow
---------

Creating a Person
~~~~~~~~~~~~~~~~~

.. mermaid::

    flowchart TD
        A[Client Request] --> B[API Adapter]
        B --> C[Person Use Case]
        C --> D[Create Person Entity]
        D --> E[Validate Business Rules]
        E --> F[Person Repository]
        F --> G[Database Adapter]
        G --> H[Database]
        H --> G
        G --> F
        F --> C
        C --> B
        B --> A

Finding Families by Parent
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    flowchart TD
        A[Client Request] --> B[API Adapter]
        B --> C[Family Use Case]
        C --> D[Person Repository]
        D --> E[Get Person Entity]
        E --> F[Family Repository]
        F --> G[Database Adapter]
        G --> H[Query Database]
        H --> G
        G --> F
        F --> C
        C --> B
        B --> A

Benefits of This Architecture
------------------------------

1. **Maintainability**: Clear separation makes code easy to understand and modify
2. **Testability**: Each component can be tested independently
3. **Flexibility**: Easy to add new features or change implementations
4. **Scalability**: Architecture supports growth and complexity
5. **Independence**: Core business logic is independent of external frameworks
6. **Reusability**: Components can be reused in different contexts
7. **Extensibility**: Easy to add new adapters and interfaces

This architecture provides a solid foundation for building a scalable, maintainable genealogy application that can grow and adapt to changing requirements.