Migration Guide: Custom DI to dependency-injector
==================================================

Dependency Management
---------------------

Dependency Injection Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project uses a custom dependency injection container that manages:

- **Service Lifecycles**: Singleton vs Transient
- **Dependency Resolution**: Automatic injection
- **Service Registration**: Clean API for registration

Service Registration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Register repositories as singletons
    container.register_singleton(PersonRepositoryPort, InMemoryPersonRepository)
    container.register_singleton(FamilyRepositoryPort, InMemoryFamilyRepository)

    # Register use cases
    container.register(PersonUseCase, PersonUseCaseImpl)
    container.register(FamilyUseCase, FamilyUseCaseImpl)

Service Resolution Example
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Get use case with automatic dependency injection
    person_use_case = container.get(PersonUseCase)
    # Dependencies are automatically injected

Dependency Rules
^^^^^^^^^^^^^^^^

1. **Domain Layer**: No dependencies on external layers
2. **Application Layer**: Depends only on Domain Layer
3. **Infrastructure Layer**: Depends on Application Layer
4. **Dependency Inversion**: All dependencies point inward

This guide explains how to migrate from the custom DI container to the new `dependency-injector` based system.

What Changed
------------

New Dependencies
~~~~~~~~~~~~~~~~

- Added `dependency-injector>=4.41.0` to `requirements.txt`
- Removed custom `DIContainer` class (kept for backward compatibility)

New Files
~~~~~~~~~

- `src/shared/containers.py` - DI container definitions
- `src/shared/di_config.py` - DI configuration and utilities
- `tests/test_helpers.py` - Test utilities for DI
- `examples/di_usage_example.py` - Usage examples

Updated Files
~~~~~~~~~~~~~

- `src/application/use_cases/person_use_case_impl.py` - Added DI decorators
- `src/application/use_cases/family_use_case_impl.py` - Added DI decorators
- `src/main.py` - Updated to use new DI system

Migration Steps
---------------

Step 1: Update Service Registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Old way:**

.. code-block:: python

    from src.shared.di_container import DIContainer

    container = DIContainer()
    container.register_singleton(PersonRepositoryPort, InMemoryPersonRepository)
    container.register(PersonUseCase, PersonUseCaseImpl)

**New way:**

.. code-block:: python

    from src.shared.containers import Container

    # Services are pre-registered in the container
    container = Container()

Step 2: Update Service Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Old way:**

.. code-block:: python

    person_use_case = container.get(PersonUseCase)

**New way:**

.. code-block:: python

    from src.shared.di_config import get_di_config

    di_config = get_di_config()
    di_config.initialize()
    person_use_case = di_config.get(PersonUseCase)

Step 3: Update Use Case Implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Old way:**

.. code-block:: python

    class PersonUseCaseImpl(PersonUseCase):
        def __init__(self, person_repository: PersonRepositoryPort):
            self._person_repository = person_repository

**New way:**

.. code-block:: python

    from dependency_injector.wiring import inject, Provide
    from src.shared.containers import Container

    class PersonUseCaseImpl(PersonUseCase):
        @inject
        def __init__(
            self,
            person_repository: PersonRepositoryPort = Provide[Container.person_repository]
        ):
            self._person_repository = person_repository

Step 4: Update Tests
~~~~~~~~~~~~~~~~~~~~

**Old way:**

.. code-block:: python

    def test_person_use_case():
        person_repo = Mock()
        use_case = PersonUseCaseImpl(person_repo)
        # test...

**New way:**

.. code-block:: python

    from tests.test_helpers import create_test_di_helper

    def test_person_use_case():
        di_helper = create_test_di_helper()
        try:
            use_case = di_helper.get_person_use_case()
            # test...
        finally:
            di_helper.cleanup()

Benefits of the New System
--------------------------

Automatic Dependency Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- No need to manually wire dependencies
- Type\-safe dependency injection
- Automatic singleton management

Better Testing Support
~~~~~~~~~~~~~~~~~~~~~~

- Dedicated test container with mocks
- Easy service overriding for tests
- Clean test setup and teardown

Configuration Support
~~~~~~~~~~~~~~~~~~~~~

- Built\-in configuration management
- Environment\-specific settings
- Runtime configuration changes

Lifecycle Management
~~~~~~~~~~~~~~~~~~~~

- Proper initialization and cleanup
- Resource management
- Error handling

Extensibility
~~~~~~~~~~~~~

- Easy to add new services
- Support for different scopes (singleton, factory, etc.)
- Plugin architecture

Advanced Usage
--------------

Service Overriding
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    di_config = get_di_config()
    di_config.initialize()

    # Override a service
    custom_repo = CustomPersonRepository()
    di_config.override(PersonRepositoryPort, custom_repo)

    # Use the overridden service
    person_use_case = di_config.get(PersonUseCase)

    # Reset to defaults
    di_config.reset_overrides()

Configuration
~~~~~~~~~~~~~

.. code-block:: python

    di_config = get_di_config()
    di_config.container.config.from_dict({
        'database': {
            'host': 'localhost',
            'port': 5432
        }
    })
    di_config.initialize()

Testing with Mocks
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from tests.test_helpers import create_test_di_helper

    def test_with_mocks():
        di_helper = create_test_di_helper()
        try:
            # All dependencies are automatically mocked
            use_case = di_helper.get_person_use_case()

            # Configure mock behavior
            di_helper.mock_person_repository.save.return_value = mock_person

            # Test your use case
            result = use_case.create_person(...)

            # Verify mock calls
            di_helper.mock_person_repository.save.assert_called_once()
        finally:
            di_helper.cleanup()

Backward Compatibility
----------------------

The old `DIContainer` class is still available in `src/shared/di_container.py` for backward compatibility, but it's recommended to migrate to the new system for better features and maintainability.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

1. **Import Errors**: Make sure `dependency-injector` is installed
2. **Wiring Issues**: Ensure modules are properly wired in the container
3. **Circular Dependencies**: Check for circular imports in your services
4. **Test Failures**: Use the test helper for proper mock setup

Debug Tips
~~~~~~~~~~

1. Enable debug logging in the container
2. Check service registration with `container.is_registered()`
3. Verify wiring with `container.wire()` calls
4. Use the example file to test your setup

Next Steps
----------

1. Update all tests to use the new DI system
2. Add configuration for different environments
3. Consider adding more advanced features like:

   - Service decorators
   - Event handling
   - Health checks
   - Metrics collection