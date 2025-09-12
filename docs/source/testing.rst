Testing Policy
==============

- All tests are located in the ``tests/`` folder.
- **Unit Tests:** Test individual services and repositories.
- **Integration Tests:** Ensure services work with both in-memory and SQL repositories.
- **Error Handling:** All repository methods raise clear exceptions for invalid operations.

Run tests:

.. code-block:: bash

    pytest tests/
