GeneWeb Features
================

This document summarizes the comprehensive feature set of **GeneWeb**, grouped into categories for clarity.

Core Architecture & Deployment
------------------------------

- Web-based interface (runs as its own lightweight web server or under CGI), accessible via any browser (offline or online).
- Standalone daemon (``gwd``) or CGI mode; can be embedded behind a standard web server.
- Multi-platform: Linux/Unix, Windows, macOS.

Data Model & Storage
--------------------

- Person / Family / Event model with rich fields (names, dates, places, events, sources, notes).
- Support for large databases (designed to scale to millions of persons).
- Database tools for splitting/merging databases and rebuilding source files from the database.

Import / Export & Formats
--------------------------

- **GEDCOM v5.5.1 import and export** with comprehensive support for person records, family relationships, events, and date qualifiers. See :doc:`gedcom_import_export` for detailed documentation.
- Newer formats introduced in later versions (e.g., GWplus).

Relationship & Consanguinity Computations
------------------------------------------

- Efficient relationship chain computation.
- Consanguinity (coefficient of relationship) calculations, including multiple connecting branches.

User Interface & Displays
--------------------------

- Dynamic page generation — pages created on demand.
- Multiple view types: individual pages, family pages, relationship pages, pedigree/ancestor displays, lists (birthdays, last births, recent changes).
- Clickable links throughout for easy navigation.

Search & Name Handling
----------------------

- Flexible search by given and surname with spelling\-correction/tolerant matching.
- Search by title/nobility or place as surname for historical datasets.

Multilingual / Internationalization
------------------------------------

- Polyglot UI: interface translated into many languages; data remains in the language entered while UI strings adapt.

Editing, Collaboration & Permissions
-------------------------------------

- In\-browser editing of individuals and families (add/modify/delete).
- Multi\-wizard support: several authorized editors ("wizards") can manage a database.
- Password protection for editing and for access to recent/living individuals.
- Concurrency controls for multiple editors (more advanced on Unix/mac builds).

Notes, Sources, Wiki & Customization
-------------------------------------

- Notes and source citations attached to individuals/families/events.
- Wiki\-like syntax for notes and database pages (in many versions).
- Customizable pages: welcome page, associated pages, color/font/background, macros.

Media & Attachments
-------------------

- Pictures / associated media can be added to individual records.

Utilities, Reports & Convenience
---------------------------------

- Birthday listings, "last births", lists by date ranges.
- Relationship reports with detailed breakdowns.
- Tools for backup/export and rebuilding source files.

International / Historical Genealogy
------------------------------------

- Support for nobility titles with begin/end dates, selection and chronological lists (e.g., kings).

Performance, Security & Server Behavior
----------------------------------------

- Ability to limit request time, limit concurrency, disconnect remote access if load is high.
- Logging of requests; standard daemon behavior.

Development / Ecosystem
-----------------------

- Open\-source (GPL), codebase in OCaml, active GitHub development.
- Used as backend for public genealogy projects (e.g., Roglo).
