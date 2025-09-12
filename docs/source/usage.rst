Example Usage
=============

.. code-block:: python

    from domain.entities.person import Person
    from services.person_service import PersonService
    from infrastructure.repositories.in_memory.person_repository_impl import PersonRepositoryImpl

    # Initialize repository
    repo = PersonRepositoryImpl()
    service = PersonService(repo)

    # Add a person
    person = Person(first_name="John", last_name="Doe")
    service.add_person(person)

    # Query by full name
    results = service.find_by_full_name("John", "Doe")
    print(results)
