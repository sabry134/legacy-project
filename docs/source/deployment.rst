Deployment Policy
=================

Overview
~~~~~~~~

The project uses a **CI/CD pipeline** where:

- **CI (Continuous Integration)**: Automated testing on each commit
- **CD (Continuous Deployment)**: Docker image pushed to Docker Hub and deployed via `run.sh` script

Deployment Workflow
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Git Push → CI Tests → Docker Build → Push to Docker Hub → run.sh Pulls & Launches

CI Pipeline
~~~~~~~~~~~

The CI pipeline automatically runs tests on every commit:

.. code-block:: bash

    # Tests are executed automatically
    pytest tests/ -v

CD Pipeline
~~~~~~~~~~~

The CD pipeline builds and pushes the Docker image:

.. code-block:: bash

    # Build Docker image
    docker build -t geneweb-python:latest .

    # Push to Docker Hub
    docker push <dockerhub-username>/geneweb-python:latest

Local Deployment
~~~~~~~~~~~~~~~~

To deploy locally, use the `run.sh` script:

.. code-block:: bash

    # Pull latest image and run container
    ./run.sh

The script handles:

- Pulling the latest Docker image from Docker Hub
- Starting the container with proper configuration
- Mounting volumes for data persistence
- Exposing necessary ports

Prerequisites
~~~~~~~~~~~~~

- Docker installed and running
- Docker Hub credentials configured (for pulling private images if needed)
- `run.sh` script with execute permissions: `chmod +x run.sh`

Manual Docker Deployment
~~~~~~~~~~~~~~~~~~~~~~~~

If needed, you can manually manage the Docker container:

.. code-block:: bash

    # Pull latest image
    docker pull <dockerhub-username>/geneweb-python:latest

    # Run container
    docker run -d \
      --name geneweb \
      -p 5000:5000 \
      <dockerhub-username>/geneweb-python:latest

    # View logs
    docker logs geneweb

    # Stop container
    docker stop geneweb

Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Set environment variables before running:

.. code-block:: bash

    export DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/geneweb
    export FLASK_ENV=production

    ./run.sh

Troubleshooting
~~~~~~~~~~~~~~~

**Container won't start:**

- Check Docker logs: `docker logs geneweb`
- Verify environment variables are set correctly
- Ensure required ports are available

**CI pipeline fails:**

- Check test output in CI logs
- Fix failing tests before next deployment
- Verify all dependencies in `requirements.txt`

**Docker image not updating:**

- Clear Docker cache: `docker system prune`
- Rebuild image: `docker build --no-cache -t geneweb-python:latest .`
- Verify image was pushed to Docker Hub

Rollback
~~~~~~~~

To rollback to a previous version:

.. code-block:: bash

    # Pull specific version tag
    docker pull <dockerhub-username>/geneweb-python:v1.0.0

    # Update run.sh or manually run
    docker run -d --name geneweb <dockerhub-username>/geneweb-python:v1.0.0
