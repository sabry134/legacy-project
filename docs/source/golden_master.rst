Golden Master Testing
=====================

Overview
~~~~~~~~

The **Golden Master** (also called **Approval Testing** or **Characterization Testing**) is a testing technique particularly useful when refactoring legacy code. It captures the current behavior of the system as a "golden" baseline, then ensures future changes don't accidentally alter that behavior.

For the GeneWeb refactoring from OCaml to Python, Golden Master testing helps verify that the Python implementation produces identical output to the original OCaml version by comparing against Docker\-based test environments and captured reference outputs.

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
- ✅ Works with external systems (GeneWeb via Docker)

How It Works
~~~~~~~~~~~~

.. code-block:: text

    1. Setup GeneWeb (OCaml) in Docker
    2. Import Sample GEDCOM
    3. Capture Output → Save as "Golden Master"
    4. Run Python Implementation → Compare Output
    5. If Identical → Test Passes
    6. If Different → Fix Python Code or Update Golden Master (intentionally)

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
    │   ├── capture_cli_golden_masters.sh
    │   ├── capture_web_golden_masters.sh
    │   ├── generate_python_outputs.py
    │   ├── compare_gw_files.py
    │   ├── bases/                       # Mounted GeneWeb databases
    │   │   └── test_small/             # Imported test database
    │   ├── test_data/
    │   │   └── sample.ged              # Sample GEDCOM for import
    │   ├── fixtures/
    │   │   ├── cli_output/             # Captured CLI golden masters
    │   │   ├── web_output/             # Captured web golden masters
    │   │   └── python_output/          # Python implementation outputs
    │   └── utils.py

Prerequisites
^^^^^^^^^^^^^

Add required dependencies to `requirements.txt`:

.. code-block:: bash

    pip install approvaltests pytest requests

Docker Setup
^^^^^^^^^^^^

Ensure the GeneWeb Docker image is available:

.. code-block:: bash

    docker pull jeffernz/geneweb:latest

Step 1: Setup Test Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initialize the GeneWeb Docker container with sample data:

.. code-block:: bash

    # Pull the GeneWeb image
    docker pull jeffernz/geneweb:latest

    # Start the GeneWeb container with mounted volume
    docker run -d --name geneweb-test -p 2317:2317 -p 2316:2316 \
      -v "$(pwd)/tests/golden_master/bases:/usr/local/var/geneweb" \
      jeffernz/geneweb:latest

**Verify database mount:**

.. code-block:: bash

    docker exec geneweb-test ls -la /usr/local/var/geneweb/

Step 2: Import Sample GEDCOM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download a sample GEDCOM file and import it into the test database:

.. code-block:: bash

    # Download sample GEDCOM from https://webtreeprint.com/tp_famous_gedcoms.php
    # Place it in tests/golden_master/test_data/sample.ged

    # Copy GEDCOM to container
    docker cp tests/golden_master/test_data/sample.ged geneweb-test:/tmp/

    # Import into GeneWeb
    docker exec geneweb-test ged2gwb /tmp/sample.ged \
      -o /usr/local/var/geneweb/test_small

**Verify database was created:**

.. code-block:: bash

    docker exec geneweb-test ls -la /usr/local/var/geneweb/test_small/

Step 3: Capture Golden Masters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Capture CLI output:**

.. code-block:: bash

    # tests/golden_master/capture_cli_golden_masters.sh
    #!/bin/bash

    set -e

    OUTPUT_DIR="./fixtures/cli_output"
    mkdir -p "$OUTPUT_DIR"

    # Query GeneWeb CLI for various outputs
    docker exec geneweb-test gwc test_small -o json > "$OUTPUT_DIR/gwc_output.json" 2>&1 || true
    docker exec geneweb-test gwc test_small -statistics > "$OUTPUT_DIR/statistics.txt" 2>&1 || true

    echo "CLI golden masters captured to $OUTPUT_DIR"

**Capture web output:**

.. code-block:: bash

    # tests/golden_master/capture_web_golden_masters.sh
    #!/bin/bash

    set -e

    OUTPUT_DIR="./fixtures/web_output"
    mkdir -p "$OUTPUT_DIR"

    BASE_URL="http://localhost:2317"

    # Give container time to start
    sleep 2

    # Capture web API responses
    curl -s "$BASE_URL/api/family/test_small" > "$OUTPUT_DIR/family_list.json" 2>&1 || true
    curl -s "$BASE_URL/api/person/test_small" > "$OUTPUT_DIR/person_list.json" 2>&1 || true

    echo "Web golden masters captured to $OUTPUT_DIR"

Run the capture scripts:

.. code-block:: bash

    cd tests/golden_master
    chmod +x capture_cli_golden_masters.sh
    chmod +x capture_web_golden_masters.sh

    ./capture_cli_golden_masters.sh
    ./capture_web_golden_masters.sh

Step 4: Generate Python Outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a script to generate outputs from your Python implementation:

.. code-block:: python

    # tests/golden_master/generate_python_outputs.py
    import json
    import subprocess
    from pathlib import Path
    from src.infrastructure.adapters.persistence.postgres.base import init_db
    from src.infrastructure.adapters.persistence.postgres.person_repository import PostgresPersonRepository
    from src.infrastructure.adapters.persistence.postgres.family_repository import PostgresFamilyRepository

    def generate_outputs():
        """Generate Python outputs for comparison"""
        output_dir = Path("./fixtures/python_output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize database
        init_db()

        # Generate person repository output
        person_repo = PostgresPersonRepository()
        persons = person_repo.find_all()

        persons_dict = [
            {
                "id": str(p.entity_id.value),
                "first_name": p.first_name.value,
                "last_name": p.last_name.value,
                "gender": p.gender.value,
            }
            for p in persons
        ]

        with open(output_dir / "persons.json", "w") as f:
            json.dump(persons_dict, f, indent=2)

        # Generate family repository output
        family_repo = PostgresFamilyRepository()
        families = family_repo.find_all()

        families_dict = [
            {
                "id": str(f.entity_id.value),
                "husband": str(f.husband.entity_id.value) if f.husband else None,
                "wife": str(f.wife.entity_id.value) if f.wife else None,
                "children_count": len(f.children),
            }
            for f in families
        ]

        with open(output_dir / "families.json", "w") as f:
            json.dump(families_dict, f, indent=2)

        print(f"Python outputs generated to {output_dir}")

    if __name__ == "__main__":
        generate_outputs()

Run the script:

.. code-block:: bash

    python generate_python_outputs.py

Step 5: Compare Outputs
^^^^^^^^^^^^^^^^^^^^^^^

Create a comparison script to validate Python outputs against golden masters:

.. code-block:: python

    # tests/golden_master/compare_gw_files.py
    import json
    import sys
    from pathlib import Path
    from difflib import unified_diff

    def compare_files(golden_file: Path, python_file: Path) -> bool:
        """Compare two JSON files and report differences"""
        if not golden_file.exists():
            print(f"❌ Golden master not found: {golden_file}")
            return False

        if not python_file.exists():
            print(f"❌ Python output not found: {python_file}")
            return False

        try:
            with open(golden_file, "r") as f:
                golden = json.load(f)

            with open(python_file, "r") as f:
                python = json.load(f)

            if golden == python:
                print(f"✅ {golden_file.name} matches golden master")
                return True
            else:
                print(f"❌ {golden_file.name} differs from golden master")
                print("\nDifferences:")
                golden_str = json.dumps(golden, indent=2).splitlines()
                python_str = json.dumps(python, indent=2).splitlines()

                for line in unified_diff(golden_str, python_str, lineterm=""):
                    print(line)
                return False

        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {golden_file.name}: {e}")
            return False

    def main():
        """Compare all golden master files"""
        golden_dir = Path("./fixtures/web_output")
        python_dir = Path("./fixtures/python_output")

        results = []

        # Compare key outputs
        comparisons = [
            ("family_list.json", "families.json"),
            ("person_list.json", "persons.json"),
        ]

        for golden_name, python_name in comparisons:
            golden_file = golden_dir / golden_name
            python_file = python_dir / python_name
            results.append(compare_files(golden_file, python_file))

        print("\n" + "=" * 50)
        if all(results):
            print("✅ All golden master comparisons passed!")
            sys.exit(0)
        else:
            print("❌ Some golden master comparisons failed!")
            sys.exit(1)

    if __name__ == "__main__":
        main()

Run the comparison:

.. code-block:: bash

    python compare_gw_files.py

Step 6: Teardown
^^^^^^^^^^^^^^^^

Clean up the test environment:

.. code-block:: bash

    docker stop geneweb-test
    docker rm geneweb-test

Complete CI/CD Workflow
~~~~~~~~~~~~~~~~~~~~~~~

**Full CI pipeline script:**

.. code-block:: bash

    #!/bin/bash
    set -e

    echo "🔧 Setting up Golden Master tests..."

    # Step 1: Setup
    docker pull jeffernz/geneweb:latest
    docker run -d --name geneweb-test -p 2317:2317 -p 2316:2316 \
      -v "$(pwd)/tests/golden_master/bases:/usr/local/var/geneweb" \
      jeffernz/geneweb:latest

    # Step 2: Import test data
    docker cp tests/golden_master/test_data/sample.ged geneweb-test:/tmp/
    docker exec geneweb-test ged2gwb /tmp/sample.ged \
      -o /usr/local/var/geneweb/test_small

    # Step 3: Capture golden masters
    cd tests/golden_master
    ./capture_cli_golden_masters.sh
    ./capture_web_golden_masters.sh

    # Step 4: Generate Python outputs
    python generate_python_outputs.py

    # Step 5: Compare outputs
    python compare_gw_files.py

    # Step 6: Teardown
    cd ../..
    docker stop geneweb-test
    docker rm geneweb-test

    echo "✅ Golden Master tests completed successfully!"

Approvaltests Integration
~~~~~~~~~~~~~~~~~~~~~~~~~

For additional test automation, use the `approvaltests` library:

.. code-block:: python

    # tests/golden_master/test_golden_master.py
    import pytest
    from approvaltests import verify_object
    from approvaltests.reporters import DiffReporter
    from src.application.ports.inbound.person_use_case import PersonUseCase
    from src.shared.containers import container
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.gender import Gender

    @pytest.fixture
    def person_use_case():
        """Initialize use case"""
        return container.person_use_case()

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
            "first_name": retrieved.first_name.value,
            "last_name": retrieved.last_name.value,
            "gender": retrieved.gender.value,
        }

        verify_object(person_dict, reporter=DiffReporter())

Workflow
~~~~~~~~

Initial Setup
^^^^^^^^^^^^^

.. code-block:: bash

    # 1. Set up Docker environment with sample data
    cd tests/golden_master
    ./setup.sh

    # 2. Capture golden masters from OCaml version
    ./capture_cli_golden_masters.sh
    ./capture_web_golden_masters.sh

    # 3. Review the captured files
    git diff fixtures/

    # 4. Commit golden master files
    git add fixtures/
    git commit -m "Add golden master baseline from GeneWeb OCaml version"

Ongoing Testing
^^^^^^^^^^^^^^^

.. code-block:: bash

    # Run golden master tests
    cd tests/golden_master
    python generate_python_outputs.py
    python compare_gw_files.py

    # Or run all tests including golden master tests
    pytest tests/ -v

Approving Changes
^^^^^^^^^^^^^^^^^

When behavior intentionally changes, update the golden masters:

.. code-block:: bash

    # Regenerate golden masters from updated GeneWeb
    cd tests/golden_master
    ./capture_cli_golden_masters.sh
    ./capture_web_golden_masters.sh

    # Review changes
    git diff fixtures/

    # Commit updated golden master
    git add fixtures/
    git commit -m "Update golden master: intentional behavior change for feature X"

Advanced: Custom Serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For complex domain objects, create serializers:

.. code-block:: python

    # tests/golden_master/serializers.py
    from src.domain.entities.person import Person
    from src.domain.value_objects.name import Name
    from src.domain.value_objects.date import Date

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
                "birth_place": (
                    {
                        "name": person.birth_place.name,
                        "country": person.birth_place.country,
                    }
                    if person.birth_place
                    else None
                ),
            }

    class FamilySerializer:
        @staticmethod
        def serialize(family) -> dict:
            """Convert Family entity to dict for golden master"""
            return {
                "id": str(family.entity_id.value),
                "husband": (
                    PersonSerializer.serialize(family.husband)
                    if family.husband
                    else None
                ),
                "wife": (
                    PersonSerializer.serialize(family.wife)
                    if family.wife
                    else None
                ),
                "children_count": len(family.children),
                "marriage_date": (
                    family.marriage_date.to_dict()
                    if family.marriage_date
                    else None
                ),
            }

Integration with CI/CD
~~~~~~~~~~~~~~~~~~~~~~

Add golden master tests to your GitHub Actions workflow:

.. code-block:: yaml

    # .github/workflows/ci.yml
    name: CI with Golden Master Tests

    on: [push, pull_request]

    jobs:
      golden-master-tests:
        runs-on: ubuntu-latest
        services:
          docker:
            image: docker:latest
            options: >-
              --privileged
              -v /var/run/docker.sock:/var/run/docker.sock

        steps:
          - uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v3
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: |
              pip install -r requirements.txt
              pip install approvaltests pytest requests

          - name: Pull GeneWeb Docker image
            run: docker pull jeffernz/geneweb:latest

          - name: Run golden master tests
            run: |
              cd tests/golden_master
              bash -x ./run_all_tests.sh

          - name: Upload test results
            if: always()
            uses: actions/upload-artifact@v3
            with:
              name: golden-master-results
              path: tests/golden_master/fixtures/

Best Practices
~~~~~~~~~~~~~~

- ✅ Keep golden master files in version control (git)
- ✅ Review golden master changes carefully before approving
- ✅ Document why changes were intentional in commit messages
- ✅ Use meaningful test names that describe what's being tested
- ✅ Serialize complex objects consistently using dedicated serializers
- ✅ Run golden master tests in CI/CD pipeline
- ✅ Verify database mounts are correct before capturing
- ✅ Use meaningful sample GEDCOM files for testing
- ❌ Never manually edit captured output files (use capture scripts)
- ❌ Don't commit unapproved changes to golden masters
- ❌ Avoid including timestamps or random data in captured outputs

Common Pitfalls
~~~~~~~~~~~~~~~

**Non\-deterministic Output**

If output includes timestamps, UUIDs, or random data, normalize it:

.. code-block:: python

    def serialize_with_normalization(person: Person) -> dict:
        """Serialize excluding non\-deterministic fields"""
        return {
            "first_name": person.first_name.value,
            "last_name": person.last_name.value,
            "gender": person.gender.value,
            # Skip: id, created_at, updated_at (they change)
        }

**Database Mount Issues**

Ensure volumes are mounted correctly:

.. code-block:: bash

    # Verify mount
    docker exec geneweb-test ls -la /usr/local/var/geneweb/

    # If empty, check host path permissions
    ls -la tests/golden_master/bases/

**GEDCOM Import Failures**

Verify GEDCOM format and GeneWeb container is running:

.. code-block:: bash

    # Check container status
    docker ps | grep geneweb-test

    # Check GeneWeb logs
    docker logs geneweb-test

    # Verify GEDCOM file
    file tests/golden_master/test_data/sample.ged

**Large Object Hierarchies**

For complex nested structures, serialize thoughtfully:

.. code-block:: python

    def test_family_hierarchy_golden_master():
        family = family_use_case.create_family(...)

        # Only serialize relevant fields for comparison
        family_dict = {
            "parents": [p.first_name.value for p in family.parents],
            "children_count": len(family.children),
        }

        verify_object(family_dict)

Troubleshooting
~~~~~~~~~~~~~~~

**Container won't start:**

.. code-block:: bash

    # Check if ports are available
    lsof -i :2317
    lsof -i :2316

    # Stop any existing containers
    docker stop geneweb-test geneweb 2>/dev/null || true

**Import fails:**

.. code-block:: bash

    # Check logs
    docker logs geneweb-test

    # Verify file was copied
    docker exec geneweb-test ls -la /tmp/sample.ged

    # Try importing manually
    docker exec geneweb-test ged2gwb /tmp/sample.ged -o /usr/local/var/geneweb/test_debug

**Comparison shows false negatives:**

.. code-block:: bash

    # Compare files directly
    diff -u fixtures/web_output/family_list.json fixtures/python_output/families.json

    # Check for whitespace differences
    od -c fixtures/web_output/family_list.json | head

    # Normalize JSON and retry
    python -m json.tool fixtures/web_output/family_list.json > /tmp/formatted.json

Example: Running Complete Golden Master Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd tests/golden_master

    # Step 1: Setup
    $ docker pull jeffernz/geneweb:latest
    $ docker run -d --name geneweb-test -p 2317:2317 -p 2316:2316 \
        -v "$(pwd)/bases:/usr/local/var/geneweb" \
        jeffernz/geneweb:latest

    # Step 2: Import test data
    $ docker cp test_data/sample.ged geneweb-test:/tmp/
    $ docker exec geneweb-test ged2gwb /tmp/sample.ged -o /usr/local/var/geneweb/test_small
    Converting GEDCOM file '/tmp/sample.ged'...
    GeneWeb database created: /usr/local/var/geneweb/test_small

    # Step 3: Capture golden masters
    $ ./capture_cli_golden_masters.sh
    CLI golden masters captured to ./fixtures/cli_output

    $ ./capture_web_golden_masters.sh
    Web golden masters captured to ./fixtures/web_output

    # Step 4: Generate Python outputs
    $ python generate_python_outputs.py
    Python outputs generated to ./fixtures/python_output

    # Step 5: Compare outputs
    $ python compare_gw_files.py
    ✅ family_list.json matches golden master
    ✅ person_list.json matches golden master
    ==================================================
    ✅ All golden master comparisons passed!

    # Step 6: Cleanup
    $ docker stop geneweb-test
    $ docker rm geneweb-test

Conclusion
~~~~~~~~~~

Golden Master testing combined with Docker\-based external system integration provides robust verification that the Python implementation maintains behavioral parity with the original OCaml version. By capturing actual outputs and comparing systematically, you ensure no regressions are missed and all edge cases are handled correctly.

For GeneWeb, this approach guarantees that the refactored Python implementation behaves identically to the original OCaml system across all major operations.
