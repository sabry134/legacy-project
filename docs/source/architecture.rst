Architecture
============

GeneWeb-Python is structured in clear layers, and we plan to gradually evolve it
towards a **Hexagonal Architecture** (also known as *Ports and Adapters*) to improve
modularity and testability.

Domain Layer (``domain/``)
--------------------------
- **Entities:** Core objects like ``Person``, ``Family``, ``Event``, ``Place``, ``Relationship``.  
- **Repository Interfaces:** Abstract contracts for data access.  
- **Repository Base:** Generic CRUD operations as a foundation.  

Infrastructure Layer (``infrastructure/``)
------------------------------------------
- Implements repositories either **in-memory** or using **SQLAlchemy** (SQL backend).  
- Manages database sessions and models.  

Services Layer (``services/``)
------------------------------
- Contains business logic.  
- Operates on entities and coordinates repository actions.  

Application Entry Point (``main.py``)
-------------------------------------
- Initializes repositories and services.  
- Provides CLI or API integration for genealogical queries.  
