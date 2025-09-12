==============
Area Project
==============

Welcome to the documentation for the "Area" project! Area is a versatile automation platform that allows you to create actions, reactions, and triggers to automate various tasks similar to Zapier. This guide will walk you through the deployment of the "Area" project and explain how to create and trigger workflows.

Deployment
----------

To deploy the "Area" project, follow these steps:

1. **Clone the Repository**:

   .. code-block:: bash

      git clone git@github.com:EpitechPromo2026/B-DEV-500-PAR-5-1-area-aurelien.duval.git


2. **Configure Environment Variables**:

   Create a `.env` file in the project's root directory and configure the necessary environment variables. Here's an example:

   .. code-block:: plaintext

      SERVER_PORT=8080
      CLIENT_PORT=8081
      POSTGRES_PORT=5432


      PGHOST="db"
      POSTGRES_USER="postgres"
      POSTGRES_PASSWORD="postgres"
      POSTGRES_DB="areaapi_dev"


3. **Run the Server**:

   .. code-block:: bash

      ./start.sh

It should now be up and running!

Creating an Action
------------------

Actions in "Area" are the tasks you want to perform when a trigger condition is met. To create an action:

1. Log in to the "Area" web interface.

2. Navigate to the **Create** section.

3. Click on the **Add** button from "Select actions".

4. Provide a name for your action, select the type of action you want to create , and configure the specific settings for that action type.

5. Save the action.

Creating a Reaction
--------------------

Reactions in "Area" are the tasks you want to perform when an action is triggered. To create a reaction:

1. Log in to the "Area" web interface.

2. Navigate to the **Create** section.

3. Click on the **Add** button from "Select reactions".

4. Provide a name for your reaction, select the type of action you want to create , and configure the specific settings for that reaction type.

5. Save the action.

Triggering a Workflow
----------------------

To trigger a workflow in "Area," you'll need to set up a trigger condition that, when met, initiates the action and subsequently the reaction.

1. Log in to the "Area" web interface.

2. Swipe the button for "Connect".

3. That's it, your area is triggered

Now, whenever the trigger conditions are met, the specified action will be executed, followed by the reaction you've defined.

That's it! You've successfully deployed the "Area" project and created a workflow with actions, reactions, and triggers. You can now automate various tasks and streamline your workflows. For more advanced configuration and options, refer to the rest of the documentation.
