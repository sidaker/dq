## README Notes
- docker-compose up --abort-on-container-exit --remove-orphans

- docker-compose exec schema-registry bash
- kafka-avro-console-consumer --topic normaliser-0.0.1 --bootstrap-server broker:9092  --from-beginning


### ERROR1:
ERROR Unknown error when running consumer:  (kafka.tools.ConsoleConsumer$)
org.apache.kafka.common.errors.SerializationException: Unknown magic byte!

- Solution
The Confluent Schema Registry serialiser/deserializer uses a wire format which includes information about the schema ID etc in the initial bytes of the message.

If your message has not been serialized using the Schema Registry serializer, then you won't be able to deserialize it with it, and will get the Unknown magic byte! error.

So you'll need to write a consumer that pulls the messages, does the deserialization using your Avro avsc schemas, and then assuming you want to preserve the data, re-serialize it using the Schema Registry serializer

Edit: I wrote an article recently that explains this whole thing in more depth: https://www.confluent.io/blog/kafka-connect-deep-dive-converters-serialization-explained

- https://stackoverflow.com/questions/52399417/unknown-magic-byte-with-kafka-avro-console-consumer


### ERROR2:
- ERROR Error while creating ephemeral at /brokers/ids/1, node already exists and owner '720584
73439756289' does not match current session '72058557409067009' (kafka.zk.KafkaZkClient$CheckedEphemeral)

- Solution
  - docker-compose down -v
  - docker-compose up --abort-on-container-exit --remove-orphans
