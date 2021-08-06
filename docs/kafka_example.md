# kafka_example

This is a Django system that implements an example "round-trip" app implementing 3 basic steps of our data path:

- **Collection**
  - ![collection](diagrams/django-collection.png)
  - HTTP and [WebSocket](WebSockets.md) interfaces
  - Data is put into a Kafka queue
- **Archive**
  - ![archive](diagrams/django-archive.png)
  - Picks up message from Kafka
  - Saves in a storage layer
- **Distribution**
  - ![distribution](diagrams/django-distribution.png)
  - Pulls data from the database
  - HTTP and [WebSocket](WebSockets.md) interfaces
