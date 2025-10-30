Testing Strategy
----------------

Unit Tests
~~~~~~~~~~

- **Scope**: Individual components in isolation
- **Dependencies**: Mocked external dependencies
- **Focus**: Business logic validation

.. code-block:: python

    def test_create_person():
        # Arrange
        person_repository = Mock()
        use_case = PersonUseCaseImpl(person_repository)

        # Act
        person = use_case.create_person(Name("John"), Name("Doe"), Gender.MALE)

        # Assert
        assert person.first_name == Name("John")
        person_repository.save.assert_called_once()

Integration Tests
~~~~~~~~~~~~~~~~~

- **Scope**: Interaction between layers
- **Dependencies**: Real implementations where appropriate
- **Focus**: Port-adapter contracts

.. code-block:: python

    def test_person_use_case_integration():
        # Arrange
        container = DIContainer()
        person_use_case = container.get(PersonUseCase)

        # Act
        person = person_use_case.create_person(Name("John"), Name("Doe"), Gender.MALE)
        retrieved = person_use_case.get_person(person.id)

        # Assert
        assert retrieved == person

End-to-End Tests
~~~~~~~~~~~~~~~~

- **Scope**: Complete user workflows
- **Dependencies**: Full application stack
- **Focus**: System behavior validation

.. code-block:: python

    def test_complete_genealogy_workflow():
        # Test complete workflow from API to database
        # Verify all interactions work together
