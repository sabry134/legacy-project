GeneWeb Python - Component Interactions
========================================

This document provides detailed information about how components interact within the hexagonal architecture.

Architecture Layers and Components
==================================

.. mermaid::

    graph TB
        subgraph External["EXTERNAL SYSTEMS"]
            WebUI["Web UI"]
            RestAPI["REST API"]
            CLITool["CLI Tool"]
            Database[(Database)]
        end

        subgraph Infrastructure["INFRASTRUCTURE LAYER - ADAPTERS"]
            UIAdapter["UI Adapter<br/>- HTTP<br/>- Forms<br/>- Views"]
            APIAdapter["API Adapter<br/>- REST<br/>- JSON<br/>- Responses"]
            CLIAdapter["CLI Adapter<br/>- Commands<br/>- Args<br/>- Output"]
            DBAdapter["DB Adapter<br/>- SQL<br/>- Models<br/>- Queries"]
        end

        subgraph Application["APPLICATION LAYER - USE CASES"]
            PersonUC["Person UC<br/>- Create<br/>- Update<br/>- Delete<br/>- Find"]
            FamilyUC["Family UC<br/>- Create<br/>- Add Child<br/>- Remove<br/>- Find"]
            RelationshipUC["Relationship UC<br/>- Create<br/>- Update<br/>- Delete<br/>- Find"]
            EventUC["Event UC<br/>- Create<br/>- Update<br/>- Delete<br/>- Find"]
        end

        subgraph Domain["DOMAIN LAYER - CORE"]
            Entities["Entities<br/>- Person<br/>- Family<br/>- Relationship<br/>- Event<br/>- Source<br/>- Title"]
            ValueObjects["Value Objects<br/>- EntityId<br/>- Name<br/>- Date<br/>- Gender<br/>- Place"]
            Repositories["Repositories<br/>- PersonRepo<br/>- FamilyRepo<br/>- RelRepo<br/>- EventRepo<br/>- SourceRepo<br/>- TitleRepo"]
            Services["Services<br/>- Domain Services<br/>- Business Rules<br/>- Validation"]
        end

        WebUI --> UIAdapter
        RestAPI --> APIAdapter
        CLITool --> CLIAdapter
        Database --> DBAdapter

        UIAdapter --> PersonUC
        APIAdapter --> PersonUC
        CLIAdapter --> PersonUC

        UIAdapter --> FamilyUC
        APIAdapter --> FamilyUC
        CLIAdapter --> FamilyUC

        PersonUC --> Repositories
        FamilyUC --> Repositories

        Repositories --> DBAdapter
        Repositories --> Entities
        Repositories --> ValueObjects

        PersonUC --> Services
        FamilyUC --> Services
        RelationshipUC --> Services
        EventUC --> Services

        DBAdapter --> Database

Component Interaction Matrix
=============================

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
===============================

Person Management Flow
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        Client["Client"]
        Adapter["UI/API/CLI<br/>Adapter"]
        UseCase["Person<br/>Use Case"]
        Entity["Person<br/>Entity"]
        Repository["Person<br/>Repository"]
        DBAdapter["DB<br/>Adapter"]
        DB[(Database)]

        Client -->|Request| Adapter
        Adapter -->|Validate & Convert| UseCase
        UseCase -->|Create/Validate| Entity
        Entity -->|Pass to| Repository
        Repository -->|Call| DBAdapter
        DBAdapter -->|SQL Query| DB

        DB -->|Result| DBAdapter
        DBAdapter -->|Response| Repository
        Repository -->|Entity| UseCase
        UseCase -->|Response| Adapter
        Adapter -->|Format| Client

Family Management Flow
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        Client["Client"]
        Adapter["UI/API/CLI<br/>Adapter"]
        FamilyUC["Family<br/>Use Case"]
        FamilyEntity["Family<br/>Entity"]
        FamilyRepo["Family<br/>Repository"]
        PersonRepo["Person<br/>Repository"]
        DBAdapter["DB<br/>Adapter"]
        DB[(Database)]

        Client -->|Request| Adapter
        Adapter -->|Call| FamilyUC
        FamilyUC -->|Validate| FamilyEntity
        FamilyEntity -->|Validate Parents/Children| PersonRepo
        FamilyUC -->|Call| FamilyRepo
        FamilyRepo -->|Call| DBAdapter
        DBAdapter -->|Query| DB

        DB -->|Result| DBAdapter
        DBAdapter -->|Response| FamilyRepo
        FamilyRepo -->|Entity| FamilyUC
        FamilyUC -->|Response| Adapter
        Adapter -->|Format| Client

Cross\-Cutting Concerns
~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph TB
        Logging["Logging<br/>System"]
        Validation["Validation<br/>System"]
        Caching["Caching<br/>System"]

        Logging -->|Log Events| AllLayers["All Layers"]
        Validation -->|Validate Data| AllLayers
        Caching -->|Cache Results| Repository["Repository<br/>Layer"]

        AllLayers -->|Generate| LogFiles["Log Files"]
        AllLayers -->|Handle| Errors["Error Handling"]
        Repository -->|Store| CacheStore["Cache Store"]

Port and Adapter Interactions
=============================

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
===============

Dependency Direction Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Domain Layer**: No dependencies on external layers
2. **Application Layer**: Depends only on Domain Layer
3. **Infrastructure Layer**: Depends on Application Layer
4. **External Systems**: Depends on Infrastructure Layer

Dependency Injection Flow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph TB
        DIContainer["DI Container"]
        ServiceReg["Service<br/>Registration"]

        UseCases["Use Cases<br/>- Person UC<br/>- Family UC<br/>- Relationship UC<br/>- Event UC"]
        BusinessLogic["Business<br/>Logic"]

        Repositories["Repositories<br/>- Person Repo<br/>- Family Repo<br/>- Relationship Repo<br/>- Event Repo"]
        DataAccess["Data Access<br/>Logic"]

        DIContainer -->|Register| ServiceReg
        ServiceReg -->|Inject| UseCases
        UseCases -->|Implement| BusinessLogic
        ServiceReg -->|Inject| Repositories
        Repositories -->|Implement| DataAccess

Error Propagation
=================

Error Flow Through Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph TB
        subgraph Forward["Forward Flow"]
            DB1[(Database<br/>Error)]
            DBAdapter1["DB Adapter<br/>Error"]
            Repo1["Repository<br/>Error"]
            UC1["Use Case<br/>Error"]
        end

        subgraph Backward["Response Flow"]
            Adapter2["Adapter<br/>Error"]
            Response["HTTP Error<br/>Response"]
            Client["Client<br/>Error"]
        end

        DB1 -->|Wrap| DBAdapter1
        DBAdapter1 -->|Transform| Repo1
        Repo1 -->|Propagate| UC1
        UC1 -->|Convert| Adapter2
        Adapter2 -->|Format| Response
        Response -->|Return| Client

Performance Considerations
==========================

Caching Interactions
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        UC["Use Case"]
        Repo["Repository"]
        Cache["Cache<br/>Layer"]
        DB["Database<br/>Adapter"]

        UC -->|Query| Repo
        Repo -->|Check| Cache
        Cache -->|Hit| Repo
        Cache -->|Miss| DB
        DB -->|Result| Repo
        Repo -->|Store| Cache
        Repo -->|Return| UC

Lazy Loading Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        UC["Use Case"]
        Repo["Repository"]
        LazyProxy["Lazy Proxy<br/>Object"]
        DB["Database<br/>Adapter"]

        UC -->|Request| Repo
        Repo -->|Return| LazyProxy
        LazyProxy -->|Access Property| DB
        DB -->|Load Data| LazyProxy
        LazyProxy -->|Access Data| UC

Testing Interactions
====================

Unit Test Interactions
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        UnitTest["Unit Test"]
        UC["Use Case"]
        MockRepo["Mock<br/>Repository"]

        UnitTest -->|Instantiate| UC
        UnitTest -->|Inject| MockRepo
        UC -->|Call| MockRepo
        MockRepo -->|Return Mock Data| UC
        UnitTest -->|Assert| MockRepo

Integration Test Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        IntTest["Integration<br/>Test"]
        UC["Use Case"]
        Repo["Repository"]
        Adapter["Real<br/>Adapter"]

        IntTest -->|Setup| UC
        UC -->|Call| Repo
        Repo -->|Call| Adapter
        Adapter -->|Real Operation| Repo
        Repo -->|Result| UC
        UC -->|Return| IntTest

End\-to\-End Test Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
        E2ETest["E2E Test"]
        Adapter["Adapter"]
        UC["Use Case"]
        Repo["Repository"]
        DBAdapter["DB<br/>Adapter"]
        DB[(Database)]

        E2ETest -->|Request| Adapter
        Adapter -->|Call| UC
        UC -->|Call| Repo
        Repo -->|Call| DBAdapter
        DBAdapter -->|Query| DB
        DB -->|Result| DBAdapter
        DBAdapter -->|Response| Repo
        Repo -->|Entity| UC
        UC -->|Response| Adapter
        Adapter -->|Return| E2ETest

Summary
=======

This comprehensive documentation of component interactions provides a clear understanding of how the hexagonal architecture components communicate and work together, making it easier to maintain, extend, and debug the system.
