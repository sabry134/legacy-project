Services Layer
==============

Each service is responsible for the business logic of its corresponding entity.

- ``PersonService`` → manage person-related queries
- ``FamilyService`` → family logic (children, parents)
- ``EventService`` → create, retrieve, and associate events
- ``PlaceService`` → manage locations
- ``RelationshipService`` → manage relationships and probabilities
- ``DateService`` → handle date types and events

Services interact with repositories but **do not know about infrastructure implementation** — enabling easy swapping between in-memory or SQL backends.
