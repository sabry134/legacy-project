Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from src.shared.di_container import DIContainer
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.gender import Gender
    from src.application.ports.inbound.person_use_case import PersonUseCase

    # Initialize container
    container = DIContainer()

    # Get use case
    person_use_case = container.get(PersonUseCase)

    # Create a person
    person = person_use_case.create_person(
        first_name=Name("John"),
        last_name=Name("Doe"),
        gender=Gender.MALE
    )

Family Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from src.application.ports.inbound.family_use_case import FamilyUseCase

    # Get family use case
    family_use_case = container.get(FamilyUseCase)

    # Create a family
    family = family_use_case.create_family(parent_1=person1, parent_2=person2)

    # Add a child
    family_use_case.add_child_to_family(family.id, child)

Advanced Operations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Find persons by name
    doe_persons = person_use_case.find_persons_by_last_name(Name("Doe"))

    # Find families by parent
    parent_families = family_use_case.find_families_by_parent(parent)

    # Update person information
    person.change_first_name(Name("Jane"))
    updated_person = person_use_case.update_person(person)
