Domain Layer
============

The **domain layer** contains the core models and abstractions.

Entities
--------

Examples:  

- ``Person`` → first_name, last_name, birth_date, relationships  
- ``Family`` → husband, wife, children  
- ``Event`` → event_type, date, place  

Repositories Interfaces
-----------------------

Abstract classes like ``PersonRepository``, ``EventRepository``, etc., define methods to query or manipulate entities.

Example: ``PersonRepository`` interface

.. code-block:: python

    from abc import ABC, abstractmethod
    from abstract_repository import AbstractRepository

    class PersonRepository(AbstractRepository, ABC):
        @abstractmethod
        def find_by_first_name(self, first_name):
            pass

        @abstractmethod
        def find_by_last_name(self, last_name):
            pass

        @abstractmethod
        def find_by_full_name(self, first_name, last_name):
            pass
