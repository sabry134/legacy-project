Architecture diagram
====================
.. mermaid::
   :zoom:
   :caption: GeneWeb-Python Architecture Diagram:
   :align:

    classDiagram
        %% Abstract base classes and interfaces
        class AbstractEntity {
            <<abstract>>
            id
        }
        class AbstractRepository {
            <<abstract>>
        }
        class IPerson {
            <<interface>>
        }
        class IEvent {
            <<interface>>
        }
        class IFamily {
            <<interface>>
        }
        class IRelationship {
            <<interface>>
        }
        class IPlace {
            <<interface>>
        }
        class IDate {
            <<interface>>
        }

        %% Entities
        class Family {
            events
            parent1
            parent2
            children
            sources
            comments
            id
        }
        class Event {
            event_type
            place
            date
            notes
            sources
            witnesses
            probability
            id
        }
        class Person {
            first_name
            last_name
            occupation
            sobriquet
            alias
            altFirstName
            altLastName
            birthDate
            deathDate
            parent1
            parent2
            relationships
            titles
            id
        }
        class Relationship {
            relationship_type
            person_1
            person_2
            id
        }
        class Place {
            name
            id
        }
        class Date {
            date_str
            date_type
            id
        }
        class Source {
            description
            id
        }
        class Title {
            title
            id
        }
        class EventType
        class ProbabilityType
        class RelationshipType
        class DateType

        %% Repositories
        class FamilyRepository {
            <<abstract>>
        }
        class PersonRepository {
            <<abstract>>
        }
        class EventRepository {
            <<abstract>>
        }
        class RelationshipRepository {
            <<abstract>>
        }
        class PlaceRepository {
            <<abstract>>
        }
        class DateRepository {
            <<abstract>>
        }

        %% Infrastructure repository implementations
        class InMemoryFamilyRepository
        class InMemoryPersonRepository
        class InMemoryEventRepository
        class InMemoryRelationshipRepository
        class InMemoryPlaceRepository
        class InMemoryDateRepository

        %% Services
        class FamilyService
        class PersonService
        class EventService
        class RelationshipService
        class PlaceService
        class DateService

        %% Inheritance and implementation
        Family --|> AbstractEntity
        Event --|> AbstractEntity
        Person --|> AbstractEntity
        Relationship --|> AbstractEntity
        Place --|> AbstractEntity
        Date --|> AbstractEntity

        FamilyRepository --|> AbstractRepository
        PersonRepository --|> AbstractRepository
        EventRepository --|> AbstractRepository
        RelationshipRepository --|> AbstractRepository
        PlaceRepository --|> AbstractRepository
        DateRepository --|> AbstractRepository

        Person ..|> IPerson
        Family ..|> IFamily
        Event ..|> IEvent
        Relationship ..|> IRelationship
        Place ..|> IPlace
        Date ..|> IDate

        %% Associations
        Family "1" o-- "*" IEvent
        Family "1" o-- "1" IPerson : parent1
        Family "1" o-- "1" IPerson : parent2
        Family "1" o-- "*" IPerson : children
        Family "1" o-- "*" Source
        Event "1" o-- "1" EventType
        Event "1" o-- "1" IPlace
        Event "1" o-- "1" IDate
        Event "1" o-- "*" Source
        Event "1" o-- "*" IPerson : witnesses
        Event "1" o-- "1" ProbabilityType
        Person "1" o-- "1" IDate : birthDate
        Person "1" o-- "1" IDate : deathDate
        Person "1" o-- "1" IPerson : parent1
        Person "1" o-- "1" IPerson : parent2
        Person "1" o-- "*" IRelationship
        Person "1" o-- "*" Title
        Relationship "1" o-- "1" RelationshipType
        Relationship "1" o-- "1" IPerson : person_1
        Relationship "1" o-- "1" IPerson : person_2
        Date "1" o-- "1" DateType

        %% Repository implementations
        InMemoryFamilyRepository --|> FamilyRepository
        InMemoryPersonRepository --|> PersonRepository
        InMemoryEventRepository --|> EventRepository
        InMemoryRelationshipRepository --|> RelationshipRepository
        InMemoryPlaceRepository --|> PlaceRepository
        InMemoryDateRepository --|> DateRepository

        %% Services depend on repositories and entities
        FamilyService ..> InMemoryFamilyRepository
        FamilyService ..> Family
        PersonService ..> InMemoryPersonRepository
        PersonService ..> Person
        EventService ..> InMemoryEventRepository
        EventService ..> Event
        RelationshipService ..> InMemoryRelationshipRepository
        RelationshipService ..> Relationship
        PlaceService ..> InMemoryPlaceRepository
        PlaceService ..> Place
        DateService ..> InMemoryDateRepository
        DateService ..> Date