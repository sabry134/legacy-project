Component Interactions
======================

This document provides detailed information about how components interact within the hexagonal architecture.

Architecture Layers and Components
----------------------------------

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                              EXTERNAL SYSTEMS                                  │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
    │  │   Web UI    │  │   REST API  │  │   CLI Tool  │  │   Database  │          │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                             │
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                        INFRASTRUCTURE LAYER (ADAPTERS)                         │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
    │  │ UI Adapter  │  │ API Adapter │  │ CLI Adapter │  │ DB Adapter  │          │
    │  │             │  │             │  │             │  │             │          │
    │  │ - HTTP      │  │ - REST      │  │ - Commands  │  │ - SQL       │          │
    │  │ - Forms     │  │ - JSON      │  │ - Args      │  │ - Models    │          │
    │  │ - Views     │  │ - Responses  │  │ - Output    │  │ - Queries   │          │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                             │
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                        APPLICATION LAYER (USE CASES)                           │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
    │  │ Person UC   │  │ Family UC   │  │ Relationship│  │ Event UC    │          │
    │  │             │  │             │  │ UC          │  │             │          │
    │  │ - Create    │  │ - Create    │  │ - Create    │  │ - Create    │          │
    │  │ - Update    │  │ - Add Child │  │ - Update    │  │ - Update    │          │
    │  │ - Delete    │  │ - Remove    │  │ - Delete    │  │ - Delete    │          │
    │  │ - Find      │  │ - Find      │  │ - Find      │  │ - Find      │          │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                             │
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                           DOMAIN LAYER (CORE)                                  │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
    │  │  Entities   │  │ Value Objects│  │ Repositories│  │   Services  │          │
    │  │             │  │             │  │             │  │             │          │
    │  │ - Person    │  │ - EntityId  │  │ - PersonRepo│  │ - Domain    │          │
    │  │ - Family    │  │ - Name      │  │ - FamilyRepo│  │   Services  │          │
    │  │ - Relationship│ │ - Date     │  │ - RelRepo   │  │ - Business  │          │
    │  │ - Event     │  │ - Gender    │  │ - EventRepo │  │   Rules     │          │
    │  │ - Source    │  │ - Place     │  │ - SourceRepo│  │ - Validation│          │
    │  │ - Title     │  │             │  │ - TitleRepo │  │             │          │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
    └─────────────────────────────────────────────────────────────────────────────────┘

Component Interaction Matrix
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 20 20 35

   * - Component
     - Interacts With
     - Interaction Type
     - Purpose
   * - **UI Adapter**
     - Person Use Case
     - Inbound Port
     - Handle user interface requests
   * - **API Adapter**
     - Person Use Case
     - Inbound Port
     - Handle REST API requests
   * - **CLI Adapter**
     - Person Use Case
     - Inbound Port
     - Handle command line requests
   * - **Person Use Case**
     - Person Repository
     - Outbound Port
     - Persist person data
   * - **Person Use Case**
     - Family Repository
     - Outbound Port
     - Manage family relationships
   * - **Family Use Case**
     - Family Repository
     - Outbound Port
     - Persist family data
   * - **Family Use Case**
     - Person Repository
     - Outbound Port
     - Manage family members
   * - **Person Repository**
     - DB Adapter
     - Implementation
     - Store/retrieve person data
   * - **Family Repository**
     - DB Adapter
     - Implementation
     - Store/retrieve family data
   * - **DB Adapter**
     - Database
     - External System
     - Execute database operations

Detailed Component Interactions
-------------------------------

Person Management Flow
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Client    │───▶│ UI/API/CLI  │───▶│ Person Use  │───▶│ Person      │
    │             │    │ Adapter     │    │ Case        │    │ Repository  │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                   │
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Database  │◀───│ DB Adapter  │◀───│ Person      │◀───│ Person      │
    │             │    │             │    │ Entity      │    │ Repository  │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

**Interaction Steps:**

1. Client sends request to Adapter
2. Adapter validates and converts request
3. Adapter calls Person Use Case
4. Use Case creates/validates Person Entity
5. Use Case calls Person Repository
6. Repository calls DB Adapter
7. DB Adapter executes database operation
8. Response flows back through the chain

Family Management Flow
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Client    │───▶│ UI/API/CLI  │───▶│ Family Use │───▶│ Family      │
    │             │    │ Adapter     │    │ Case        │    │ Repository  │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                   │
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Database  │◀───│ DB Adapter  │◀───│ Family      │◀───│ Family      │
    │             │    │             │    │ Entity      │    │ Repository  │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                   │
                                                                   ▼
                                                        ┌─────────────┐
                                                        │ Person      │
                                                        │ Repository  │
                                                        └─────────────┘

**Interaction Steps:**

1. Client sends family request to Adapter
2. Adapter calls Family Use Case
3. Use Case creates/validates Family Entity
4. Use Case may call Person Repository for parent/child validation
5. Use Case calls Family Repository
6. Repository calls DB Adapter
7. Response flows back through the chain

Cross\-Cutting Concerns
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Logging   │───▶│ All Layers  │───▶│ Log Files   │
    └─────────────┘    └─────────────┘    └─────────────┘

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Validation  │───▶│ All Layers  │───▶│ Error       │
    └─────────────┘    └─────────────┘    └─────────────┘

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Caching     │───▶│ Repository  │───▶│ Cache Store │
    └─────────────┘    └─────────────┘    └─────────────┘

Port and Adapter Interactions
-------------------------------

Inbound Ports (Use Case Interfaces)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Person Use Case Interface
    class PersonUseCase(ABC):
        @abstractmethod
        def create_person(self, first_name: Name, last_name: Name, gender: Gender) -> Person:
            pass

        @abstractmethod
        def get_person(self, person_id: EntityId) -> Optional[Person]:
            pass

        @abstractmethod
        def update_person(self, person: Person) -> Person:
            pass

        @abstractmethod
        def delete_person(self, person_id: EntityId) -> bool:
            pass

**Adapters Implementing Inbound Ports:**

- UI Adapter: Handles web form submissions
- API Adapter: Handles REST API calls
- CLI Adapter: Handles command line arguments

Outbound Ports (Repository Interfaces)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Person Repository Interface
    class PersonRepository(ABC):
        @abstractmethod
        def save(self, person: Person) -> Person:
            pass

        @abstractmethod
        def get_by_id(self, person_id: EntityId) -> Optional[Person]:
            pass

        @abstractmethod
        def find_by_first_name(self, first_name: Name) -> List[Person]:
            pass

        @abstractmethod
        def delete(self, person_id: EntityId) -> bool:
            pass

**Adapters Implementing Outbound Ports:**

- InMemoryPersonRepository: Stores data in memory
- SQLPersonRepository: Stores data in SQL database
- NoSQLPersonRepository: Stores data in NoSQL database

Dependency Flow
----------------

Dependency Direction Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Domain Layer**: No dependencies on external layers
2. **Application Layer**: Depends only on Domain Layer
3. **Infrastructure Layer**: Depends on Application Layer
4. **External Systems**: Depends on Infrastructure Layer

Dependency Injection Flow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ DI Container│───▶│ Use Cases   │───▶│ Repositories│
    └─────────────┘    └─────────────┘    └─────────────┘
            │                   │                   │
            ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Service     │    │ Business    │    │ Data Access │
    │ Registration│    │ Logic       │    │ Logic       │
    └─────────────┘    └─────────────┘    └─────────────┘

Error Propagation
-----------------

Error Flow Through Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Database    │───▶│ DB Adapter  │───▶│ Repository  │───▶│ Use Case    │
    │ Error       │    │ Error       │    │ Error       │    │ Error       │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                   │
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Client      │◀───│ Adapter     │◀───│ HTTP Error │◀───│ Use Case    │
    │ Error       │    │ Error       │    │ Response    │    │ Error       │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Performance Considerations
--------------------------

Caching Interactions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Use Case    │───▶│ Repository  │───▶│ Cache       │
    │             │    │             │    │ Layer       │
    └─────────────┘    └─────────────┘    └─────────────┘
                                                │
                                                ▼
                                    ┌─────────────┐
                                    │ Database    │
                                    │ Adapter     │
                                    └─────────────┘

Lazy Loading Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Use Case    │───▶│ Repository  │───▶│ Lazy Proxy  │
    │             │    │             │    │             │
    └─────────────┘    └─────────────┘    └─────────────┘
                                                │
                                                ▼
                                    ┌─────────────┐
                                    │ Database    │
                                    │ Adapter     │
                                    └─────────────┘

Testing Interactions
--------------------

Unit Test Interactions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Unit Test   │───▶│ Use Case    │───▶│ Mock        │
    │             │    │             │    │ Repository  │
    └─────────────┘    └─────────────┘    └─────────────┘

Integration Test Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Integration │───▶│ Use Case    │───▶│ Repository  │───▶│ Real        │
    │ Test        │    │             │    │             │    │ Adapter     │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

End\-to\-End Test Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ E2E Test    │───▶│ Adapter     │───▶│ Use Case    │───▶│ Repository  │
    │             │    │             │    │             │    │             │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                   │
                                                                   ▼
                                                        ┌─────────────┐
                                                        │ Database    │
                                                        │ Adapter     │
                                                        └─────────────┘

Summary
-------

This comprehensive documentation of component interactions provides a clear understanding of how the hexagonal architecture components communicate and work together, making it easier to maintain, extend, and debug the system.