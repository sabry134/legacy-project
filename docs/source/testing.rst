Testing Policy
==============

- All tests are located in the ``tests/`` folder.
- **Unit Tests:** Test individual services and repositories.
- **Integration Tests:** Ensure services work with both in-memory and SQL repositories.
- **Error Handling:** All repository methods raise clear exceptions for invalid operations.

Our testing strategy follows the **Golden Master** approach: instead of verifying individual assertions, we capture the current output of a function and compare it against a previously validated "gold standard." This ensures that any unintended changes in behavior are immediately detected, while also making it easier to refactor code with confidence.

Run tests:

.. code-block:: bash

    pytest tests/
