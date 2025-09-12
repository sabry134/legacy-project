Architecture
============

GeneWeb-Python follows **Domain-Driven Design (DDD)** principles:

1. **Domain Layer** (`domain/`):  
   - **Entities:** Represent core objects like ``Person``, ``Family``, ``Event``, ``Place``, ``Relationship``.
   - **Repositories Interfaces:** Abstract interfaces for accessing data.
   - **Repositories Base:** Abstract repository for generic CRUD operations.

2. **Infrastructure Layer** (`infrastructure/`):  
   - Implements repositories either **in-memory** or using **SQLAlchemy** (SQL backend).
   - Manages database sessions and models.

3. **Services Layer** (`services/`):  
   - Contains business logic.
   - Operates on entities and coordinates repository actions.

4. **Application Entry Point** (`main.py`):  
   - Initializes repositories and services.
   - Provides CLI or API integration for genealogical queries.
