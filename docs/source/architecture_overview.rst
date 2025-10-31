GeneWeb Python Architecture
================================

.. contents::
   :depth: 3
   :local:

Overview
========

The GeneWeb Python project implements a **Hexagonal Architecture** (also known as Ports and Adapters), which provides:

- **High Testability**: Each layer can be tested in isolation
- **High Modularity**: Clear separation of concerns
- **High Scalability**: Easy to add new features and adapters
- **Dependency Inversion**: Core business logic doesn't depend on external frameworks
- **Technology Independence**: Core business logic is independent of databases, web frameworks, and other external technologies

Architecture Principles
=======================

Dependency Rule
---------------

All dependencies point **inward** toward the domain layer:

.. code-block:: text

    External Systems → Infrastructure Layer → Application Layer → Domain Layer

This means:

- Domain layer has **zero dependencies** on external frameworks
- Application layer depends only on the Domain layer
- Infrastructure layer depends on Application and Domain layers
- External systems depend on Infrastructure adapters

Benefits
--------

- **Maintainability**: Clear separation makes code easy to understand and modify
- **Testability**: Each component can be tested independently with mocked dependencies
- **Flexibility**: Easy to swap implementations (e.g., in-memory to PostgreSQL)
- **Scalability**: Architecture supports growth and complexity
- **Reusability**: Components can be reused in different contexts
- **Extensibility**: Easy to add new adapters and interfaces

Architecture Layers
==================

The system is organized into three main layers:

1. **Domain Layer** (Core): Business logic, entities, value objects
2. **Application Layer**: Use cases and orchestration
3. **Infrastructure Layer**: Adapters for external systems

Layer 1: Domain Layer (Core Business Logic)
============================================

The domain layer contains the core business logic and is completely independent of external concerns. This is the **heart** of the application.

Directory Structure
-------------------

.. code-block:: text

    src/domain/
    ├── entities/          # Domain entities with identity and behavior
    ├── value_objects/     # Immutable value objects
    └── repositories/      # Repository interface definitions (ports)

Domain Entities
---------------

Entities represent the core business objects with **identity** and **behavior**:

Person
~~~~~~

Represents a person in the genealogy system.

**Location**: ``src/domain/entities/person.py``

**Properties**:
- Identity: ``id`` (EntityId)
- Names: ``first_name``, ``last_name``, ``public_name``, ``sobriquet``, ``alias``, ``alt_first_name``, ``alt_last_name``
- Personal info: ``gender``, ``occupation``, ``number_of_appearances``
- Dates: ``birth_date``, ``death_date`` (Date value objects)
- Places: ``birth_place``, ``death_place`` (Place value objects)
- Relationships: ``titles`` (list of Title entities)

**Key Behaviors**:
- ``change_first_name()``: Update first name with validation
- ``change_last_name()``: Update last name with validation
- ``add_title()``: Associate a title with this person
- ``increment_appearances()``: Increment appearance counter

Family
~~~~~~

Represents a family unit with parents and children.

**Location**: ``src/domain/entities/family.py``

**Properties**:
- Identity: ``id`` (EntityId)
- Parents: ``parent_1``, ``parent_2`` (Person entities, optional)
- Children: ``children`` (list of Person entities)
- Metadata: ``sources``, ``comments``, ``name``, ``complete``

**Key Behaviors**:
- ``add_child()``: Add a child to the family
- ``remove_child()``: Remove a child from the family
- ``set_parent_1()``: Set first parent
- ``set_parent_2()``: Set second parent
- ``swap_parents()``: Swap parent_1 and parent_2

Relationship
~~~~~~~~~~~~

Represents relationships between persons (sibling, spouse, etc.).

**Location**: ``src/domain/entities/relationship.py``

**Properties**:
- Identity: ``id`` (EntityId)
- ``person_1``, ``person_2`` (Person entities)
- ``relationship_type`` (enum: parent_child, sibling, spouse, etc.)

PersonEvent
~~~~~~~~~~~

Represents events related to persons (birth, death, baptism, burial, etc.).

**Location**: ``src/domain/entities/person_event.py``

**Properties**:
- Identity: ``id`` (EntityId)
- ``event_type`` (enum: birth, death, baptism, burial, marriage, divorce, etc.)
- ``concerned_person`` (Person entity, optional)
- ``date``, ``place`` (Date and Place value objects)
- ``probability`` (enum: certain, probable, possible, unknown)
- ``notes``, ``sources``, ``witnesses`` (lists)

FamilyEvent
~~~~~~~~~~~

Represents events related to families (marriage, divorce, separation, adoption, etc.).

**Location**: ``src/domain/entities/family_event.py``

**Properties**:
- Identity: ``id`` (EntityId)
- ``event_type`` (enum: marriage, divorce, separation, adoption, other)
- ``family`` (Family entity, optional)
- ``date``, ``place`` (Date and Place value objects)
- ``probability``, ``notes``, ``sources``, ``witnesses``

Source
~~~~~~

Represents sources of genealogical information.

**Location**: ``src/domain/entities/source.py``

**Properties**:
- Identity: ``id`` (EntityId)
- ``description`` (string)

Title
~~~~~

Represents titles held by persons (Dr., Mr., Prof., etc.).

**Location**: ``src/domain/entities/title.py``

**Properties**:
- Identity: ``id`` (EntityId)
- ``title`` (string)

Value Objects
----------

Value objects are **immutable** objects that represent concepts without identity. They are compared by value, not by reference.

EntityId
~~~~~~~~

Unique identifier for all entities.

**Location**: ``src/domain/value_objects/entity_id.py``

**Properties**:
- ``value`` (int): The numeric identifier

**Usage**: All entities have an ``EntityId`` as their primary identifier.

Name
~~~~

Immutable name value object with validation.

**Location**: ``src/domain/value_objects/name.py``

**Properties**:
- ``value`` (str): The name string

**Validation**: Ensures non-empty names

Gender
~~~~~~

Enumeration for person gender.

**Location**: ``src/domain/value_objects/gender.py``

**Values**: ``M`` (Male), ``F`` (Female), ``U`` (Unknown)

Date
~~~~

Date value object supporting exact and approximate dates, with GEDCOM qualifiers.

**Location**: ``src/domain/value_objects/date.py``

**Properties**:
- ``date_type`` (enum: exact, approximate)
- ``date_string`` (str): String representation of the date
- ``qualifier`` (optional): GEDCOM qualifiers (ABT, CAL, EST, BEFORE, AFTER, BETWEEN)

**Special Features**:
- GEDCOM date qualifier support
- ISO format for exact dates
- Flexible string format for approximate dates
- ``get_gedcom_date_string()``: Formats date for GEDCOM export

Place
~~~~~

Geographic location value object.

**Location**: ``src/domain/value_objects/place.py``

**Properties**:
- ``name`` (str, required)
- ``country`` (str, optional)
- ``region`` (str, optional)
- ``city`` (str, optional)

Repository Interfaces (Outbound Ports)
---------------------------------------

Repository interfaces define contracts for data access. These are **outbound ports** - they define what the application needs from infrastructure.

PersonRepositoryPort
~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/person_repository_port.py``

**Methods**:
- ``save(person: Person) -> Person``: Save or update a person
- ``get_by_id(id: EntityId) -> Optional[Person]``: Retrieve person by ID
- ``find_all() -> List[Person]``: Get all persons
- ``find_by_last_name(name: Name) -> List[Person]``: Search by last name
- ``delete(id: EntityId) -> bool``: Delete a person
- ``search(query: str) -> List[Person]``: Full-text search
- ``paginate(page: int, size: int) -> Tuple[List[Person], int]``: Paginated list

FamilyRepositoryPort
~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/family_repository_port.py``

**Methods**:
- ``save(family: Family) -> Family``: Save or update a family
- ``get_by_id(id: EntityId) -> Optional[Family]``: Retrieve family by ID
- ``find_all() -> List[Family]``: Get all families
- ``find_by_parent(parent: Person) -> List[Family]``: Find families by parent
- ``delete(id: EntityId) -> bool``: Delete a family

RelationshipRepositoryPort
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/relationship_repository_port.py``

**Methods**:
- ``save(relationship: Relationship) -> Relationship``
- ``get_by_id(id: EntityId) -> Optional[Relationship]``
- ``find_all() -> List[Relationship]``
- ``find_by_person(person: Person) -> List[Relationship]``
- ``delete(id: EntityId) -> bool``
- ``paginate(page: int, size: int) -> Tuple[List[Relationship], int]``

PersonEventRepositoryPort
~~~~~~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/person_event_repository_port.py``

**Methods**:
- ``save(event: PersonEvent) -> PersonEvent``
- ``get_by_id(id: EntityId) -> Optional[PersonEvent]``
- ``find_all() -> List[PersonEvent]``
- ``find_by_person(person: Person) -> List[PersonEvent]``
- ``delete(id: EntityId) -> bool``

FamilyEventRepositoryPort
~~~~~~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/family_event_repository_port.py``

**Methods**:
- ``save(event: FamilyEvent) -> FamilyEvent``
- ``get_by_id(id: EntityId) -> Optional[FamilyEvent]``
- ``find_all() -> List[FamilyEvent]``
- ``find_by_family(family: Family) -> List[FamilyEvent]``
- ``delete(id: EntityId) -> bool``

SourceRepositoryPort
~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/source_repository_port.py``

**Methods**:
- ``save(source: Source) -> Source``
- ``get_by_id(id: EntityId) -> Optional[Source]``
- ``find_all() -> List[Source]``
- ``search(query: str) -> List[Source]``
- ``paginate(page: int, size: int) -> Tuple[List[Source], int]``
- ``delete(id: EntityId) -> bool``

TitleRepositoryPort
~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/outbound/title_repository_port.py``

**Methods**:
- ``save(title: Title) -> Title``
- ``get_by_id(id: EntityId) -> Optional[Title]``
- ``find_all() -> List[Title]``
- ``search(query: str) -> List[Title]``
- ``paginate(page: int, size: int) -> Tuple[List[Title], int]``
- ``delete(id: EntityId) -> bool``

Layer 2: Application Layer (Use Cases)
========================================

The application layer orchestrates business workflows by coordinating domain entities and outbound ports.

Directory Structure
-------------------

.. code-block:: text

    src/application/
    ├── ports/
    │   ├── inbound/      # Use case interfaces (what adapters call)
    │   └── outbound/     # Repository interfaces (what use cases need)
    └── use_cases/        # Use case implementations

Use Case Interfaces (Inbound Ports)
------------------------------------

Inbound ports define the application's public API. They are called by infrastructure adapters (e.g., REST controllers).

PersonUseCase
~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/person_use_case.py``

**Key Methods**:
- ``create_person(...) -> Person``: Create a new person with all optional fields
- ``get_person(id: EntityId) -> Optional[Person]``: Retrieve person by ID
- ``update_person(person: Person) -> Person``: Update person
- ``delete_person(id: EntityId) -> bool``: Delete person
- ``find_persons_by_last_name(name: Name) -> List[Person]``: Search by last name
- ``list_all_persons() -> List[Person]``: Get all persons
- ``search_persons(query: str) -> List[Person]``: Full-text search
- ``paginate_persons(page: int, size: int) -> Tuple[List[Person], int]``: Paginated list
- ``add_title_to_person(person_id: EntityId, title: Title) -> Person``: Associate title
- ``increment_person_appearances(person_id: EntityId) -> Person``: Increment counter

FamilyUseCase
~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/family_use_case.py``

**Key Methods**:
- ``create_family(parent_1: Optional[Person], parent_2: Optional[Person]) -> Family``
- ``get_family(id: EntityId) -> Optional[Family]``
- ``delete_family(id: EntityId) -> bool``
- ``add_child_to_family(family_id: EntityId, child: Person) -> Family``
- ``remove_child_from_family(family_id: EntityId, child: Person) -> Family``
- ``set_parent_1(family_id: EntityId, parent: Optional[Person]) -> bool``
- ``set_parent_2(family_id: EntityId, parent: Optional[Person]) -> bool``
- ``swap_parents(family_id: EntityId) -> bool``
- ``find_families_by_parent(parent: Person) -> List[Family]``
- ``add_source_to_family(family_id: EntityId, source: Source) -> Family``
- ``add_comment_to_family(family_id: EntityId, comment: str) -> Family``

RelationshipUseCase
~~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/relationship_use_case.py``

**Key Methods**:
- ``create_relationship(person_1: Person, person_2: Person, relationship_type: str) -> Relationship``
- ``get_relationship(id: EntityId) -> Optional[Relationship]``
- ``find_relationships_by_person(person: Person) -> List[Relationship]``
- ``delete_relationship(id: EntityId) -> bool``
- ``paginate_relationships(page: int, size: int) -> Tuple[List[Relationship], int]``

PersonEventUseCase
~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/person_event_use_case.py``

**Key Methods**:
- ``create_event(event_type: str, concerned_person: Optional[Person], date: Optional[Date], place: Optional[Place]) -> PersonEvent``
- ``get_event(id: EntityId) -> Optional[PersonEvent]``
- ``find_events_by_person(person: Person) -> List[PersonEvent]``
- ``update_event(event: PersonEvent) -> PersonEvent``
- ``delete_event(id: EntityId) -> bool``
- ``add_note(event_id: EntityId, note: str) -> PersonEvent``
- ``add_source(event_id: EntityId, source: Source) -> PersonEvent``
- ``add_witness(event_id: EntityId, witness: Person) -> PersonEvent``
- ``change_probability(event_id: EntityId, probability: str) -> PersonEvent``

FamilyEventUseCase
~~~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/family_event_use_case.py``

**Key Methods**:
- ``create_event(event_type: str, family: Optional[Family], date: Optional[Date], place: Optional[Place]) -> FamilyEvent``
- ``get_event(id: EntityId) -> Optional[FamilyEvent]``
- ``find_events_by_family(family: Family) -> List[FamilyEvent]``
- ``update_event(event: FamilyEvent) -> FamilyEvent``
- ``delete_event(id: EntityId) -> bool``
- ``add_note(event_id: EntityId, note: str) -> FamilyEvent``
- ``add_source(event_id: EntityId, source: Source) -> FamilyEvent``
- ``add_witness(event_id: EntityId, witness: Person) -> FamilyEvent``
- ``change_probability(event_id: EntityId, probability: str) -> FamilyEvent``

SourceUseCase
~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/source_use_case.py``

**Key Methods**:
- ``create_source(description: str) -> Source``
- ``get_source(id: EntityId) -> Optional[Source]``
- ``update_source(source: Source) -> Source``
- ``delete_source(id: EntityId) -> bool``
- ``search_sources(query: str) -> List[Source]``
- ``paginate_sources(page: int, size: int) -> Tuple[List[Source], int]``

TitleUseCase
~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/title_use_case.py``

**Key Methods**:
- ``create_title(title: str) -> Title``
- ``get_title(id: EntityId) -> Optional[Title]``
- ``update_title(title: Title) -> Title``
- ``delete_title(id: EntityId) -> bool``
- ``search_titles(query: str) -> List[Title]``
- ``paginate_titles(page: int, size: int) -> Tuple[List[Title], int]``

GenealogyUseCase
~~~~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/genealogy_use_case.py``

**Key Methods**:
- ``get_ancestors(person: Person, depth: Optional[int] = None) -> List[Person]``: Get ancestors up to specified depth
- ``get_descendants(person: Person, depth: Optional[int] = None) -> List[Person]``: Get descendants up to specified depth
- ``find_kinship_path(from_person: Person, to_person: Person) -> Optional[List[Person]]``: Find relationship path
- ``get_relatives(person: Person) -> List[Person]``: Get all relatives (ancestors, descendants, siblings)
- ``merge_persons(primary: Person, duplicate: Person) -> Person``: Merge duplicate person records

GedcomUseCase
~~~~~~~~~~~~~

**Location**: ``src/application/ports/inbound/gedcom_use_case.py``

**Key Methods**:
- ``import_gedcom(file_path: str) -> Tuple[List[Person], List[Family], List[Source], List[str]]``: Import GEDCOM v5.5.1 file
- ``export_gedcom_string() -> str``: Export all data as GEDCOM v5.5.1 format string

**Features**:
- Supports GEDCOM v5.5.1 standard
- Person and family events (birth, death, marriage, divorce, baptism, burial, etc.)
- Date qualifiers (ABT, CAL, EST, BEFORE, AFTER, BETWEEN)
- Error reporting for import issues
- Sources and notes support

Use Case Implementations
-------------------------

All use cases are implemented in ``src/application/use_cases/``:

- ``PersonUseCaseImpl``: Implements ``PersonUseCase``
- ``FamilyUseCaseImpl``: Implements ``FamilyUseCase``
- ``RelationshipUseCaseImpl``: Implements ``RelationshipUseCase``
- ``PersonEventUseCaseImpl``: Implements ``PersonEventUseCase``
- ``FamilyEventUseCaseImpl``: Implements ``FamilyEventUseCase``
- ``SourceUseCaseImpl``: Implements ``SourceUseCase``
- ``TitleUseCaseImpl``: Implements ``TitleUseCase``
- ``GenealogyUseCaseImpl``: Implements ``GenealogyUseCase``
- ``GedcomUseCaseImpl``: Implements ``GedcomUseCase``

**Pattern**: Use cases receive repository dependencies via constructor injection and orchestrate business workflows by:

1. Validating inputs
2. Creating/updating domain entities
3. Calling repository ports to persist data
4. Returning results

Layer 3: Infrastructure Layer (Adapters)
==========================================

The infrastructure layer implements the ports defined in the application layer. These are the "adapters" in the Ports and Adapters pattern.

Directory Structure
-------------------

.. code-block:: text

    src/infrastructure/adapters/
    ├── persistence/
    │   ├── in_memory_*.py    # In-memory repository implementations
    │   └── postgres/          # PostgreSQL/SQLite implementations
    │       ├── base.py         # Database connection and initialization
    │       ├── models.py       # SQLAlchemy models
    │       └── *_repository.py # Repository implementations
    ├── web/
    │   ├── flask_app.py       # Flask application setup
    │   └── blueprints/        # REST API endpoints
    └── gedcom/
        ├── parser.py          # GEDCOM file parser
        ├── mapper.py          # Domain mapping
        └── writer.py          # GEDCOM export writer

Persistence Adapters
---------------------

Persistence adapters implement the repository outbound ports.

PostgreSQL Adapters
~~~~~~~~~~~~~~~~~~~

**Location**: ``src/infrastructure/adapters/persistence/postgres/``

All repositories use SQLAlchemy ORM with support for both PostgreSQL and SQLite:

- ``PostgresPersonRepository``: Implements ``PersonRepositoryPort``
- ``PostgresFamilyRepository``: Implements ``FamilyRepositoryPort``
- ``PostgresRelationshipRepository``: Implements ``RelationshipRepositoryPort``
- ``PostgresPersonEventRepository``: Implements ``PersonEventRepositoryPort``
- ``PostgresFamilyEventRepository``: Implements ``FamilyEventRepositoryPort``
- ``PostgresSourceRepository``: Implements ``SourceRepositoryPort``
- ``PostgresTitleRepository``: Implements ``TitleRepositoryPort``

**Database Models** (SQLAlchemy):

- ``PersonModel``: Maps to ``persons`` table
- ``FamilyModel``: Maps to ``families`` table
- ``RelationshipModel``: Maps to ``relationships`` table
- ``PersonEventModel``: Maps to ``person_events`` table
- ``FamilyEventModel``: Maps to ``family_events`` table
- ``SourceModel``: Maps to ``sources`` table
- ``TitleModel``: Maps to ``titles`` table
- Join tables: ``family_children``, ``person_event_sources``, ``person_event_witnesses``, etc.

**Database Configuration**:

- Default: SQLite file-based database (``geneweb.db``)
- Can be configured via ``DATABASE_URL`` environment variable
- Supports PostgreSQL: ``postgresql+psycopg2://user:pass@host:port/db``
- Supports SQLite: ``sqlite+pysqlite:///path/to/db.db``
- Automatic table creation via ``init_db()``

In-Memory Adapters (Legacy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/infrastructure/adapters/persistence/in_memory_*.py``

Legacy in-memory implementations (now replaced by PostgreSQL adapters):

- ``InMemoryPersonRepository``
- ``InMemoryFamilyRepository``
- ``InMemoryRelationshipRepository``
- etc.

Web Adapters (REST API)
------------------------

**Location**: ``src/infrastructure/adapters/web/``

Flask blueprints implement REST API endpoints that call inbound ports (use cases).

Flask Application Setup
~~~~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/infrastructure/adapters/web/flask_app.py``

- Initializes database on startup
- Configures dependency injection
- Registers all blueprints
- Sets up Swagger documentation
- Provides HTML templates for web UI

REST API Blueprints
~~~~~~~~~~~~~~~~~~~

All endpoints are organized into blueprints:

**Person API** (``person_api.py``):
- ``GET /persons/``: List all persons
- ``GET /persons/paginate?page=1&size=10``: Paginated list
- ``GET /persons/<id>``: Get person by ID
- ``POST /persons/``: Create person
- ``PUT /persons/<id>``: Update person
- ``DELETE /persons/<id>``: Delete person
- ``POST /persons/<id>/titles``: Add title to person
- ``DELETE /persons/<id>/titles/<title_id>``: Remove title
- ``POST /persons/<id>/appearances/increment``: Increment appearances

**Family API** (``family_api.py``):
- ``GET /families/``: List all families
- ``GET /families/<id>``: Get family by ID
- ``POST /families/``: Create family
- ``DELETE /families/<id>``: Delete family
- ``POST /families/<id>/children``: Add child
- ``DELETE /families/<id>/children/<child_id>``: Remove child
- ``PUT /families/<id>/parents/<slot>``: Set parent (parent_1 or parent_2)
- ``POST /families/<id>/parents/swap``: Swap parents
- ``GET /families/<id>/children``: List children
- ``POST /families/<id>/sources``: Add source
- ``POST /families/<id>/comments``: Add comment

**Relationship API** (``relationship_api.py``):
- ``GET /relationships/``: List all relationships
- ``GET /relationships/paginate?page=1&size=10``: Paginated list
- ``GET /relationships/<id>``: Get relationship by ID
- ``POST /relationships/``: Create relationship
- ``DELETE /relationships/<id>``: Delete relationship

**Person Event API** (``person_event_api.py``):
- ``GET /person-events/``: List all person events
- ``GET /person-events/<id>``: Get event by ID
- ``POST /person-events/``: Create event
- ``PUT /person-events/<id>``: Update event
- ``DELETE /person-events/<id>``: Delete event
- ``POST /person-events/<id>/notes``: Add note
- ``POST /person-events/<id>/sources``: Add source
- ``POST /person-events/<id>/witnesses``: Add witness
- ``POST /person-events/<id>/probability``: Change probability

**Family Event API** (``family_event_api.py``):
- Similar endpoints as Person Event API

**Source API** (``source_api.py``):
- ``GET /sources/``: List all sources
- ``GET /sources/search?q=query``: Search sources
- ``GET /sources/paginate?page=1&size=10``: Paginated list
- ``GET /sources/<id>``: Get source by ID
- ``POST /sources/``: Create source
- ``PUT /sources/<id>``: Update source
- ``DELETE /sources/<id>``: Delete source

**Title API** (``title_api.py``):
- Similar endpoints as Source API

**Genealogy API** (``genealogy_api.py``):
- ``GET /genealogy/<person_id>/ancestors?depth=5``: Get ancestors
- ``GET /genealogy/<person_id>/descendants?depth=5``: Get descendants
- ``GET /genealogy/<person_id>/relatives``: Get all relatives
- ``GET /genealogy/kinship?from=<id>&to=<id>``: Find kinship path
- ``POST /genealogy/merge``: Merge duplicate persons

**GEDCOM API** (``gedcom_api.py``):
- ``POST /gedcom/import``: Import GEDCOM file (multipart/form-data)
- ``GET /gedcom/export``: Export all data as GEDCOM file

GEDCOM Adapters
---------------

**Location**: ``src/infrastructure/adapters/gedcom/``

GEDCOM v5.5.1 import/export implementation:

**Parser** (``parser.py``):
- Parses GEDCOM files into structured records
- Handles multi-line records and continuation lines
- Extracts INDI, FAM, SOUR, NOTE records

**Mapper** (``mapper.py``):
- Maps GEDCOM records to domain entities
- Handles person mapping (names, dates, places, events)
- Handles family mapping (parents, children, events)
- Parses date qualifiers (ABT, CAL, EST, BEFORE, AFTER, BETWEEN)
- Creates PersonEvent and FamilyEvent entities from GEDCOM events
- Returns errors for invalid data

**Writer** (``writer.py``):
- Converts domain entities to GEDCOM format
- Exports persons, families, and sources
- Handles person and family events (BIRT, DEAT, MARR, DIV, BAPM, BURI)
- Formats dates with qualifiers
- Ensures GEDCOM v5.5.1 compliance

Dependency Injection
====================

The system uses **dependency injection** to manage dependencies between layers.

DI Container
------------

**Location**: ``src/shared/containers.py``

Uses `dependency_injector` library to provide:

- **Container**: Production container with PostgreSQL adapters
- **TestContainer**: Test container with in-memory adapters

**Service Registration**:

.. code-block:: python

    Container.person_repository.override(PostgresPersonRepository())
    Container.family_repository.override(PostgresFamilyRepository())
    # ... etc

**Service Resolution**:

.. code-block:: python

    @inject
    def create_person(
        person_use_case: PersonUseCase = Provide[Container.person_use_case],
    ):
        # Use case is automatically injected
        person = person_use_case.create_person(...)

DI Configuration
-----------------

**Location**: ``src/shared/di_config.py``

- Manages container initialization
- Handles lifecycle management
- Provides factory methods for use cases

**Flask Integration**:

Flask blueprints use ``@inject`` decorator for automatic dependency injection:

.. code-block:: python

    from dependency_injector.wiring import inject, Provide

    @person_bp.route("/", methods=["POST"])
    @inject
    def create_person(
        person_use_case: PersonUseCase = Provide[Container.person_use_case],
    ):
        # person_use_case is automatically resolved from container
        ...

Data Flow
=========

Request Flow (Inbound)
----------------------

Typical flow when a client makes a request:

.. code-block:: text

    1. Client → REST API Endpoint (Flask Blueprint)
    2. Blueprint → Use Case (Inbound Port)
    3. Use Case → Domain Entity (Business Logic)
    4. Use Case → Repository (Outbound Port)
    5. Repository → Database Adapter (SQLAlchemy)
    6. Database Adapter → Database (PostgreSQL/SQLite)
    7. Database → Database Adapter → Repository → Use Case → Blueprint → Client

Example: Creating a Person
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    1. POST /persons/ with JSON body
    2. person_api.create_person() (Flask blueprint)
    3. PersonUseCase.create_person() (use case)
    4. Person(...) (create domain entity)
    5. PersonRepositoryPort.save(person) (repository port)
    6. PostgresPersonRepository.save() (adapter)
    7. SQLAlchemy session.save() → Database INSERT
    8. Return created Person entity back through layers

Persistence Flow (Outbound)
---------------------------

When data is saved:

.. code-block:: text

    1. Use Case calls Repository Port
    2. Repository Adapter converts Entity → Database Model
    3. Database Model is persisted via SQLAlchemy
    4. Database Model is converted back → Entity
    5. Entity is returned to Use Case

Example: Saving a Family
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    1. FamilyUseCase.create_family()
    2. FamilyRepositoryPort.save(family)
    3. PostgresFamilyRepository converts Family → FamilyModel
    4. SQLAlchemy saves FamilyModel to database
    5. FamilyModel → Family conversion on retrieval
    6. Family entity returned to use case

GEDCOM Import Flow
------------------

.. code-block:: text

    1. POST /gedcom/import with file
    2. gedcom_api.import_gedcom()
    3. GedcomUseCase.import_gedcom(file_path)
    4. GedcomParser.parse() → GEDCOM records
    5. GedcomMapper.map_person() → Person entities + PersonEvent entities
    6. GedcomMapper.map_family() → Family entities + FamilyEvent entities
    7. PersonRepositoryPort.save() for each person
    8. FamilyRepositoryPort.save() for each family
    9. PersonEventRepositoryPort.save() for each event
    10. FamilyEventRepositoryPort.save() for each event
    11. Return summary with counts and errors

GEDCOM Export Flow
------------------

.. code-block:: text

    1. GET /gedcom/export
    2. gedcom_api.export_gedcom()
    3. GedcomUseCase.export_gedcom_string()
    4. Fetch all persons, families, events from repositories
    5. GedcomWriter.write() converts entities to GEDCOM format
    6. Returns GEDCOM v5.5.1 formatted string

Testing Strategy
================

The architecture supports testing at multiple levels:

Unit Tests
----------

**Location**: ``tests/unit/``

- Test individual components in isolation
- Mock external dependencies
- Focus on business logic validation

**Example**: Testing Person entity behavior:

.. code-block:: python

    def test_person_add_title():
        person = Person(...)
        title = Title(...)
        person.add_title(title)
        assert title in person.titles

Integration Tests
-----------------

**Location**: ``tests/integration/``

- Test interaction between layers
- Use real implementations where appropriate
- Verify port-adapter contracts

**Example**: Testing PersonUseCase with repository:

.. code-block:: python

    def test_create_person_integration():
        use_case = PersonUseCaseImpl(person_repository)
        person = use_case.create_person(...)
        retrieved = use_case.get_person(person.id)
        assert retrieved == person

End-to-End Tests
----------------

**Location**: ``tests/e2e/``

- Test complete workflows
- Use full application stack
- Verify system behavior

**Example**: Testing complete API workflow:

.. code-block:: python

    def test_create_family_with_parents_and_children():
        # Create persons via API
        parent1 = client.post("/persons/", json={...})
        parent2 = client.post("/persons/", json={...})

        # Create family via API
        family = client.post("/families/", json={
            "parent_1_id": parent1["id"],
            "parent_2_id": parent2["id"]
        })

        # Add child via API
        child = client.post("/persons/", json={...})
        client.post(f"/families/{family['id']}/children", json={
            "child_id": child["id"]
        })

        # Verify via API
        result = client.get(f"/families/{family['id']}")
        assert len(result["children"]) == 1

API Tests
---------

**Location**: ``tests/integration/test_flask_*.py``

- Test REST API endpoints
- Verify request/response formats
- Test error handling

Repository Integration Tests
-----------------------------

**Location**: ``tests/integration/pg/test_*_repository_it.py``

- Test PostgreSQL repository adapters
- Verify database persistence
- Test SQLAlchemy mappings

Extension Points
================

Adding a New Entity
-------------------

1. **Create Domain Entity**:
   - Add entity class in ``src/domain/entities/``
   - Implement business logic methods

2. **Create Repository Interface**:
   - Add interface in ``src/application/ports/outbound/``
   - Define required methods (save, get_by_id, find_all, etc.)

3. **Create Use Case Interface**:
   - Add interface in ``src/application/ports/inbound/``
   - Define business operations

4. **Implement Use Case**:
   - Add implementation in ``src/application/use_cases/``
   - Inject repository dependencies

5. **Implement Repository Adapter**:
   - Add PostgreSQL adapter in ``src/infrastructure/adapters/persistence/postgres/``
   - Add SQLAlchemy model in ``models.py``

6. **Create REST API Blueprint**:
   - Add blueprint in ``src/infrastructure/adapters/web/blueprints/``
   - Define endpoints that call use case

7. **Register in DI Container**:
   - Update ``src/shared/containers.py``
   - Register repository and use case

Adding a New Adapter
--------------------

1. **Implement Repository Port**:
   - Create new class implementing the outbound port interface
   - Add conversion logic (Entity ↔ Model)

2. **Register in DI Container**:
   - Override the repository provider with new adapter

**Example**: Adding a MongoDB adapter:

.. code-block:: python

    class MongoPersonRepository(PersonRepositoryPort):
        def __init__(self, mongo_client):
            self._client = mongo_client

        def save(self, person: Person) -> Person:
            # Convert Person → MongoDB document
            # Save to MongoDB
            # Return Person
            ...

Adding a New Use Case
---------------------

1. **Define Inbound Port**:
   - Add interface in ``src/application/ports/inbound/``

2. **Implement Use Case**:
   - Add implementation in ``src/application/use_cases/``
   - Inject required repositories

3. **Create REST API Endpoint**:
   - Add endpoint in appropriate blueprint
   - Call use case from endpoint

4. **Register in DI Container**:
   - Add factory method in container

Best Practices
==============

Domain Layer
------------

- **Keep Pure**: No external dependencies
- **Rich Domain Models**: Entities contain business logic
- **Value Objects**: Use for immutable concepts
- **Validation**: Validate at entity boundaries

Application Layer
-----------------

- **Orchestration Only**: Coordinate domain and infrastructure
- **No Business Logic**: Business rules belong in domain
- **Transaction Boundaries**: Define transaction scope
- **Error Handling**: Convert domain exceptions to application exceptions

Infrastructure Layer
--------------------

- **Thin Adapters**: Minimal logic, focus on conversion
- **Framework Code Only**: Only framework-specific code here
- **No Business Logic**: Never put business rules in adapters
- **Error Translation**: Convert infrastructure errors to application errors

Testing
-------

- **Test at Right Level**: Unit for logic, integration for interactions
- **Mock Boundaries**: Mock at port boundaries
- **Test Contracts**: Verify port-adapter contracts
- **End-to-End**: Test complete workflows

Dependency Injection
--------------------

- **Constructor Injection**: Prefer constructor injection
- **Interface-Based**: Depend on interfaces, not implementations
- **Single Responsibility**: Each service has one reason to change
- **Explicit Dependencies**: Make dependencies explicit

Summary
=======

The GeneWeb Python architecture follows Hexagonal Architecture principles with:

- **Three Layers**: Domain, Application, Infrastructure
- **Ports and Adapters**: Clean boundaries via interfaces
- **Dependency Injection**: Loose coupling through DI
- **PostgreSQL Persistence**: SQLAlchemy-based adapters
- **REST API**: Flask-based web adapters
- **GEDCOM Support**: Full import/export capabilities
- **Comprehensive Testing**: Unit, integration, and E2E tests

This architecture provides a solid foundation for building a scalable, maintainable genealogy application that can grow and adapt to changing requirements.
