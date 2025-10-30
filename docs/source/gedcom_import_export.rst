GEDCOM v5.5.1 Import/Export
============================

Overview
~~~~~~~~

GeneWeb Python provides comprehensive GEDCOM v5.5.1 support for importing and exporting genealogical data. GEDCOM (GEnealogical Data COMmunication) is the standard format for exchanging genealogy information between different software systems.

Supported Features
~~~~~~~~~~~~~~~~~~

✅ **Supported**

- Person records (INDI): Names, gender, birth/death dates and places, titles, occupation
- Family records (FAM): Parents (husband/wife) and children relationships
- Source records (SOUR): Basic source descriptions
- Person events: Birth, Death, Baptism (BAPM), Burial (BURI) with dates and places
- Family events: Marriage (MARR), Divorce (DIV) with dates and places
- Date qualifiers: ABT (about), CAL (calculated), EST (estimated), BEFORE, AFTER, BETWEEN
- Error reporting: Comprehensive error collection and reporting
- Round\-trip compatibility: Import → Export → Import preserves data

⚠️ **Known Limitations**

- Notes (NOTE tags) in events are not yet supported
- Source citations (SOUR with PAGE/DATA) in events are not yet exported
- Advanced place parsing (coordinates, structured formats) is limited
- Some GEDCOM tags are not yet supported (RESI, EMIG, IMMI, EDUC, etc.)

Basic Usage
~~~~~~~~~~~

Python API: Import from File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from src.shared.di_config import get_di_config
    from src.application.ports.inbound.gedcom_use_case import GedcomUseCase

    # Get the use case from DI container
    di_config = get_di_config()
    gedcom_use_case = di_config.get(GedcomUseCase)

    # Import from file
    persons, families, sources, errors = gedcom_use_case.import_gedcom("path/to/file.ged")

    print(f"Imported {len(persons)} persons, {len(families)} families, {len(sources)} sources")
    if errors:
        print(f"Errors encountered: {errors}")

Python API: Import from String
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    gedcom_string = """0 HEAD
    1 GEDC
    2 VERS 5.5.1
    0 @I1@ INDI
    1 NAME John /Doe/
    1 SEX M
    1 BIRT
    2 DATE ABT 1900
    2 PLAC Boston
    0 TRLR"""

    persons, families, sources, errors = gedcom_use_case.import_gedcom_string(gedcom_string)

Python API: Export to File
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Export all data to a GEDCOM file
    success = gedcom_use_case.export_gedcom("output.ged")
    if success:
        print("Export successful!")

Python API: Export to String
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Export all data to a string
    gedcom_output = gedcom_use_case.export_gedcom_string()
    print(gedcom_output)

REST API: Import GEDCOM
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    curl -X POST http://localhost:5000/gedcom/import \
      -F "file=@family_tree.ged"

Response:

.. code-block:: json

    {
      "persons_imported": 150,
      "families_imported": 45,
      "sources_imported": 23,
      "errors": []
    }

REST API: Export GEDCOM
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    curl -X GET http://localhost:5000/gedcom/export -o export.ged

Date Qualifiers
~~~~~~~~~~~~~~~

The system supports common GEDCOM date qualifiers:

- **ABT** (About): `2 DATE ABT 1900` - Approximate date
- **CAL** (Calculated): `2 DATE CAL 15 JAN 1850` - Calculated date
- **EST** (Estimated): `2 DATE EST 1920` - Estimated date
- **BEFORE**: `2 DATE BEFORE 1920` - Before a certain date
- **AFTER**: `2 DATE AFTER 1850` - After a certain date
- **BETWEEN**: `2 DATE BET 1890 AND 1895` - Date range

All qualifiers are preserved during import and export.

Example: Working with Date Qualifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from src.domain.value_objects.date import Date, DateType

    # Create dates with qualifiers
    approximate_date = Date.create_with_qualifier("ABT", "1900")
    before_date = Date.create_with_qualifier("BEFORE", "1920")
    between_date = Date.create_with_qualifier("BETWEEN", "1890 AND 1895")

    # Get GEDCOM\-formatted string
    print(approximate_date.get_gedcom_date_string())  # "ABT 1900"
    print(before_date.get_gedcom_date_string())       # "BEFORE 1920"
    print(between_date.get_gedcom_date_string())      # "BET 1890 AND 1895"

Events
~~~~~~

Person Events
^^^^^^^^^^^^^

Person events are automatically imported and exported:

- **BIRT** (Birth) → `PersonEventType.BIRTH`
- **DEAT** (Death) → `PersonEventType.DEATH`
- **BAPM** (Baptism) → `PersonEventType.BAPTISM`
- **BURI** (Burial) → `PersonEventType.BURIAL`

Example: Person Events in GEDCOM

.. code-block:: gedcom

    0 @I1@ INDI
    1 NAME Jane /Smith/
    1 SEX F
    1 BAPM
    2 DATE 15 MAR 1900
    2 PLAC Church of St. Mary
    1 BURI
    2 DATE 1 JAN 1950
    2 PLAC Old Cemetery

Example: Working with Person Events

.. code-block:: python

    gedcom = """0 @I1@ INDI
    1 NAME Jane /Smith/
    1 SEX F
    1 BAPM
    2 DATE 15 MAR 1900
    2 PLAC Church of St. Mary
    1 BURI
    2 DATE 1 JAN 1950
    2 PLAC Old Cemetery
    0 TRLR"""

    persons, _, _, _ = gedcom_use_case.import_gedcom_string(gedcom)

    # Access events via repository
    from src.application.ports.outbound.person_event_repository_port import PersonEventRepositoryPort
    event_repo = di_config.get(PersonEventRepositoryPort)

    person = persons[0]
    events = event_repo.find_by_person(person)
    for event in events:
        print(f"{event.event_type}: {event.date} at {event.place}")

Family Events
^^^^^^^^^^^^^

Family events are also automatically imported and exported:

- **MARR** (Marriage) → `FamilyEventType.MARRIAGE`
- **DIV** (Divorce) → `FamilyEventType.DIVORCE`

Example: Family Events in GEDCOM

.. code-block:: gedcom

    0 @F1@ FAM
    1 HUSB @I1@
    1 WIFE @I2@
    1 MARR
    2 DATE 1 JAN 1950
    2 PLAC Las Vegas
    1 DIV
    2 DATE 1 JAN 1960

Example: Working with Family Events

.. code-block:: python

    gedcom = """0 @I1@ INDI
    1 NAME Husband /Smith/
    1 SEX M
    0 @I2@ INDI
    1 NAME Wife /Jones/
    1 SEX F
    0 @F1@ FAM
    1 HUSB @I1@
    1 WIFE @I2@
    1 MARR
    2 DATE 1 JAN 1950
    2 PLAC Las Vegas
    1 DIV
    2 DATE 1 JAN 1960
    0 TRLR"""

    _, families, _, _ = gedcom_use_case.import_gedcom_string(gedcom)

    # Access family events via repository
    from src.application.ports.outbound.family_event_repository_port import FamilyEventRepositoryPort
    family_event_repo = di_config.get(FamilyEventRepositoryPort)

    family = families[0]
    events = family_event_repo.find_by_family(family)
    for event in events:
        print(f"{event.event_type}: {event.date}")

Error Handling
~~~~~~~~~~~~~~

Errors are collected during parsing and returned without stopping the import:

.. code-block:: python

    persons, families, sources, errors = gedcom_use_case.import_gedcom("file.ged")

    if errors:
        for error in errors:
            print(f"Error: {error}")

Common error types:

- Parse errors: Invalid line format, missing required fields
- Mapping errors: Missing person references, invalid date formats
- Data errors: Empty records, invalid relationships

The system continues processing even when errors occur, so partial data is still imported.

Architecture
~~~~~~~~~~~~

Components
^^^^^^^^^^

1. **GedcomParser** (`src/infrastructure/adapters/gedcom/parser.py`)
   - Parses GEDCOM file format
   - Builds hierarchical record structure
   - Collects parse errors

2. **GedcomMapper** (`src/infrastructure/adapters/gedcom/mapper.py`)
   - Maps GEDCOM records to domain entities
   - Handles person, family, and source mapping
   - Creates event entities

3. **GedcomWriter** (`src/infrastructure/adapters/gedcom/writer.py`)
   - Converts domain entities to GEDCOM format
   - Handles XREF generation
   - Exports events with proper formatting

4. **GedcomUseCase** (`src/application/use_cases/gedcom_use_case_impl.py`)
   - Orchestrates import/export operations
   - Manages repositories
   - Handles errors

Data Flow
^^^^^^^^^

**Import Flow:**

.. code-block:: text

    GEDCOM File → Parser → Mapper → Domain Entities → Repositories → Database

**Export Flow:**

.. code-block:: text

    Database → Repositories → Domain Entities → Writer → GEDCOM File

Complete Examples
~~~~~~~~~~~~~~~~~

Round\-trip Example
^^^^^^^^^^^^^^^^^^^

Verify data integrity through import, export, and re\-import:

.. code-block:: python

    from src.shared.di_config import get_di_config
    from src.application.ports.inbound.gedcom_use_case import GedcomUseCase

    di_config = get_di_config()
    gedcom_use_case = di_config.get(GedcomUseCase)

    # Original GEDCOM
    original = """0 HEAD
    1 GEDC
    2 VERS 5.5.1
    0 @I1@ INDI
    1 NAME John /Doe/
    1 SEX M
    1 BIRT
    2 DATE ABT 1900
    2 PLAC Boston
    1 DEAT
    2 DATE 31 DEC 1990
    2 PLAC New York
    0 @I2@ INDI
    1 NAME Jane /Smith/
    1 SEX F
    0 @F1@ FAM
    1 HUSB @I1@
    1 WIFE @I2@
    1 MARR
    2 DATE 15 JUN 1920
    2 PLAC Paris
    0 TRLR"""

    # Import
    persons, families, sources, errors = gedcom_use_case.import_gedcom_string(original)
    assert len(persons) >= 2
    assert len(families) >= 1

    # Export
    exported = gedcom_use_case.export_gedcom_string()

    # Import again to verify round\-trip
    persons2, families2, sources2, errors2 = gedcom_use_case.import_gedcom_string(exported)
    assert len(persons2) >= 2
    assert len(families2) >= 1
    assert len(errors2) == 0

REST API Endpoints
~~~~~~~~~~~~~~~~~~

POST /gedcom/import
^^^^^^^^^^^^^^^^^^^

Import a GEDCOM file.

**Request:**

- Method: `POST`
- Content\-Type: `multipart/form-data`
- Body: `file` field with GEDCOM file

**Response:**

.. code-block:: json

    {
      "persons_imported": 150,
      "families_imported": 45,
      "sources_imported": 23,
      "errors": ["Error mapping FAM F1: Missing person reference"]
    }

**Status Codes:**

- `200`: Success
- `400`: Bad request (no file or invalid file)
- `500`: Internal server error

GET /gedcom/export
^^^^^^^^^^^^^^^^^^^

Export all data as GEDCOM file.

**Request:**

- Method: `GET`
- No parameters

**Response:**

- Content\-Type: `text/plain`
- Body: GEDCOM file content
- Headers: `Content-Disposition: attachment; filename=export.ged`

**Status Codes:**

- `200`: Success
- `500`: Internal server error

Testing
~~~~~~~

Run all GEDCOM\-related tests:

.. code-block:: bash

    # Unit tests for parser
    pytest tests/unit/test_gedcom_parser.py -v

    # Integration tests for import/export
    pytest tests/integration/test_gedcom_import_export.py -v
    pytest tests/integration/test_gedcom_roundtrip_and_events.py -v

    # API tests
    pytest tests/integration/test_flask_gedcom_api.py -v

Troubleshooting
~~~~~~~~~~~~~~~

Events Not Exporting
^^^^^^^^^^^^^^^^^^^^^

Ensure event repositories are properly configured in the DI container:

.. code-block:: python

    from src.application.ports.outbound.person_event_repository_port import PersonEventRepositoryPort
    from src.infrastructure.adapters.persistence.postgres.person_event_repository import PostgresPersonEventRepository

    container.bind(PersonEventRepositoryPort, PostgresPersonEventRepository)

Date Qualifiers Lost
^^^^^^^^^^^^^^^^^^^^

Verify you're using `get_gedcom_date_string()` instead of `date_string`:

.. code-block:: python

    # ✅ Correct
    date_str = date.get_gedcom_date_string()  # "ABT 1900"

    # ❌ Wrong
    date_str = date.date_string  # "1900" (qualifier lost)

Missing References
^^^^^^^^^^^^^^^^^^

GEDCOM files should declare persons before families that reference them:

.. code-block:: gedcom

    0 @I1@ INDI
    1 NAME Person One
    0 @I2@ INDI
    1 NAME Person Two
    0 @F1@ FAM
    1 HUSB @I1@
    1 WIFE @I2@

Encoding Issues
^^^^^^^^^^^^^^^

Files should be UTF\-8 encoded. Convert if necessary:

.. code-block:: bash

    file encoding:
    iconv -f ISO-8859-1 -t UTF-8 input.ged > output.ged

Debug Mode
^^^^^^^^^^

To see detailed error information:

.. code-block:: python

    persons, families, sources, errors = gedcom_use_case.import_gedcom("file.ged")
    for error in errors:
        print(f"ERROR: {error}")

Future Enhancements
~~~~~~~~~~~~~~~~~~~

Planned features:

- Notes support (NOTE tags)
- Source citations in events
- Additional event types (RESI, EMIG, IMMI, EDUC)
- Enhanced place parsing
- GEDCOM validation mode
- Performance optimizations for large files

References
~~~~~~~~~~

- `GEDCOM v5.5.1 Specification <https://wiki.genealogy.net/GEDCOM/5.5.1>`_
- `GeneWeb Project <https://geneweb.org/>`_
