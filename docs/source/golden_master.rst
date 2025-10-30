Golden Master Testing
=====================

Overview
~~~~~~~~

The **Golden Master** (also called **Approval Testing** or **Characterization Testing**) is a testing technique particularly useful when refactoring legacy code. It captures the current behavior of the system as a "golden" baseline, then ensures future changes don't accidentally alter that behavior.

For the GeneWeb refactoring from OCaml to Python, Golden Master testing helps verify that the Python implementation produces identical output to the original OCaml version.

Why Golden Master Testing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When refactoring legacy systems like GeneWeb from OCaml to Python, you need confidence that:

- The new implementation produces identical results
- Edge cases are handled the same way
- No subtle behavioral changes occur
- Regressions are caught immediately

Golden Master testing is ideal because:

- ✅ No need to understand the original code logic
- ✅ Captures actual behavior, not assumptions
- ✅ Easy to set up for complex systems
- ✅ Provides regression detection
- ✅ Documents expected behavior

How It Works
~~~~~~~~~~~~

.. code-block:: text

    1. Run Legacy System (OCaml) → Capture Output → Save as "Golden Master"
    2. Run New System (Python) → Compare Output → If Identical → Test Passes
    3. If Different → Either Fix Python Code or Update Golden Master (intentionally)

Setup for GeneWeb
~~~~~~~~~~~~~~~~~

Directory Structure
^^^^^^^^^^^^^^^^^^^

Create a dedicated directory for Golden Master tests:

.. code-block:: text

    tests/
    ├── golden_master/
    │   ├── __init__.py
    │   ├── test_golden_master.py
    │   ├── fixtures/
    │   │   ├── input_data/          # Test input files
    │   │   └── expected_output/     # Captured golden master outputs
    │   └── utils.py

Installation
^^^^^^^^^^^^

Add the approval testing library to `requirements.txt`:

.. code-block:: bash

    pip install approvaltests

Step 1: Capture Golden Master Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, run the OCaml version and save its output:

.. code-block:: python

    # tests/golden_master/utils.py
    import json
    from pathlib import Path

    def save_golden_master(test_name: str, output: dict):
        """Save the golden master output from OCaml version"""
        golden_dir = Path(__file__).parent / "fixtures" / "expected_output"
        golden_dir.mkdir(parents=True, exist_ok=True)

        golden_file = golden_dir / f"{test_name}.json"
        with open(golden_file, "w") as f:
            json.dump(output, f, indent=2)

    def load_golden_master(test_name: str) -> dict:
        """Load the golden master output"""
        golden_dir = Path(__file__).parent / "fixtures" / "expected_output"
        golden_file = golden_dir / f"{test_name}.json"

        if not golden_file.exists():
            raise FileNotFoundError(f"Golden master not found: {golden_file}")

        with open(golden_file, "r") as f:
            return json.load(f)

Step 2: Create Golden Master Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # tests/golden_master/test_golden_master.py
    import pytest
    from approvaltests import verify_object
    from approvaltests.reporters import DiffReporter
    from src.application.ports.inbound.person_use_case import PersonUseCase
    from src.shared.di_container import DIContainer
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.gender import Gender

    @pytest.fixture
    def person_use_case():
        """Initialize use case"""
        container = DIContainer()
        return container.get(PersonUseCase)

    def test_create_person_golden_master(person_use_case):
        """Golden master test: verify person creation matches expected output"""
        # Create a person
        person = person_use_case.create_person(
            first_name=Name("John"),
            last_name=Name("Doe"),
            gender=Gender.MALE
        )

        # Convert to dict for comparison
        person_dict = {
            "id": str(person.entity_id.value),
            "first_name": person.first_name.value,
            "last_name": person.last_name.value,
            "gender": person.gender.value,
        }

        # Use approvaltests to compare with golden master
        verify_object(person_dict, reporter=DiffReporter())

    def test_find_person_golden_master(person_use_case):
        """Golden master test: verify person lookup matches expected output"""
        # Create and retrieve person
        created = person_use_case.create_person(
            first_name=Name("Jane"),
            last_name=Name("Smith"),
            gender=Gender.FEMALE
        )

        retrieved = person_use_case.get_person(created.entity_id)

        person_dict = {
            "id": str(retrieved.entity_id.value),
            "first_name": retrieved.first_name.value,
            "last_name": retrieved.last_name.value,
            "gender": retrieved.gender.value,
        }

        verify_object(person_dict, reporter=DiffReporter())

Manual Golden Master Capture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For complex OCaml outputs, capture them manually:

.. code-block:: bash

    # Step 1: Run OCaml version and save output
    ./geneweb_ocaml create_person "John" "Doe" "M" > /tmp/ocaml_output.json

    # Step 2: Copy to golden master directory
    cp /tmp/ocaml_output.json tests/golden_master/fixtures/expected_output/create_person.json

    # Step 3: Run Python tests
    pytest tests/golden_master/ -v

Workflow
~~~~~~~~

Initial Setup
^^^^^^^^^^^^^

.. code-block:: bash

    # 1. Create golden master files from OCaml version
    pytest tests/golden_master/ --approve

    # 2. Review the generated ".approved" files
    git diff tests/golden_master/fixtures/expected_output/

    # 3. Commit golden master files
    git add tests/golden_master/fixtures/expected_output/
    git commit -m "Add golden master baseline from OCaml version"

Ongoing Testing
^^^^^^^^^^^^^^^

.. code-block:: bash

    # Run golden master tests
    pytest tests/golden_master/ -v

    # If there are differences, review them
    # If intentional, approve the new output
    pytest tests/golden_master/ --approve

    # If unintentional, fix the Python code

Approving Changes
^^^^^^^^^^^^^^^^^

When behavior intentionally changes, approve the new golden master:

.. code-block:: bash

    # Review differences
    pytest tests/golden_master/ -v

    # If changes are correct, approve them
    pytest tests/golden_master/ --approve

    # Commit the updated golden master
    git add tests/golden_master/fixtures/expected_output/
    git commit -m "Update golden master: intentional behavior change"

Advanced: Using approvaltests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Better Diff Reporting
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from approvaltests import verify_object
    from approvaltests.reporters import DiffReporter, AllFailingTestsReporter

    def test_with_diff_reporter():
        """Use built\-in diff reporter for better output"""
        data = {"name": "John", "age": 30}
        verify_object(data, reporter=DiffReporter())

Custom Reporters
^^^^^^^^^^^^^^^^

.. code-block:: python

    from approvaltests.reporters import Reporter

    class CustomReporter(Reporter):
        def report(self, received_path: str, approved_path: str):
            """Custom reporting logic"""
            print(f"Received: {received_path}")
            print(f"Approved: {approved_path}")

        def is_approved(self, received_path: str, approved_path: str) -> bool:
            # Compare files
            return compare_files(received_path, approved_path)

JSON Serialization
^^^^^^^^^^^^^^^^^^

For complex domain objects, create serializers:

.. code-block:: python

    # tests/golden_master/serializers.py
    from src.domain.entities.person import Person
    from src.domain.value_objects.name import Name

    class PersonSerializer:
        @staticmethod
        def serialize(person: Person) -> dict:
            """Convert Person entity to dict for golden master"""
            return {
                "id": str(person.entity_id.value),
                "first_name": person.first_name.value,
                "last_name": person.last_name.value,
                "gender": person.gender.value,
                "birth_date": (
                    person.birth_date.to_dict()
                    if person.birth_date
                    else None
                ),
            }

Integration with CI/CD
~~~~~~~~~~~~~~~~~~~~~~

Add golden master tests to your CI pipeline:

.. code-block:: yaml

    # .github/workflows/ci.yml
    name: CI

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2

          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: |
              pip install -r requirements.txt
              pip install approvaltests

          - name: Run golden master tests
            run: pytest tests/golden_master/ -v

          - name: Run all tests
            run: pytest tests/ -v

Best Practices
~~~~~~~~~~~~~~

- ✅ Keep golden master files in version control (git)
- ✅ Review golden master changes carefully before approving
- ✅ Document why changes were intentional
- ✅ Use meaningful test names that describe what's being tested
- ✅ Serialize complex objects consistently
- ✅ Run golden master tests in CI/CD pipeline
- ❌ Never manually edit golden master files (use `--approve`)
- ❌ Don't commit unapproved changes to golden masters
- ❌ Avoid golden master tests for UI/presentation logic only

Common Pitfalls
~~~~~~~~~~~~~~~

**Non\-deterministic Output**

If output includes timestamps or random data, normalize it:

.. code-block:: python

    def test_with_normalized_output(person_use_case):
        person = person_use_case.create_person(
            first_name=Name("John"),
            last_name=Name("Doe"),
            gender=Gender.MALE
        )

        # Normalize output for comparison
        person_dict = {
            "first_name": person.first_name.value,
            "last_name": person.last_name.value,
            "gender": person.gender.value,
            # Skip timestamps and IDs that change
        }

        verify_object(person_dict)

**Large Object Hierarchies**

For complex nested structures, serialize thoughtfully:

.. code-block:: python

    def test_family_hierarchy_golden_master(family_use_case):
        family = family_use_case.create_family(
            father=...,
            mother=...,
            children=[...]
        )

        # Only serialize relevant fields
        family_dict = {
            "parents": [p.first_name.value for p in family.parents],
            "children_count": len(family.children),
            "created_date": str(family.created_date),
        }

        verify_object(family_dict)

Example: Running Golden Master Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # First run: capture baseline from OCaml version
    $ pytest tests/golden_master/ --approve
    Approved output saved to:
    - tests/golden_master/fixtures/expected_output/test_create_person_golden_master.approved.json

    # Subsequent runs: verify Python matches OCaml
    $ pytest tests/golden_master/ -v
    test_create_person_golden_master PASSED
    test_find_person_golden_master PASSED

    # If behavior changes unexpectedly
    $ pytest tests/golden_master/ -v
    test_create_person_golden_master FAILED
    Expected output differs from approved

    # Review and approve if intentional
    $ pytest tests/golden_master/ --approve

Conclusion
~~~~~~~~~~

Golden Master testing is a powerful technique for legacy system refactoring. It ensures the Python implementation behaves identically to the OCaml version while providing confidence that regressions are caught immediately.

For GeneWeb, this approach guarantees behavioral parity between the original and refactored versions.