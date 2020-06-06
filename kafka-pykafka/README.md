virtualenv ./venv
source ./venv/bin/activate
pip install -r requirements.txt

zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
kafka-server-start /usr/local/etc/kafka/server.properties

kafka-topics --list --bootstrap-server localhost:9092

kafka-server-stop
zookeeper-server-stop

open-source Kafka-Python

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sgar

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 2 --topic raw_recipes

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 2 --topic parsed_recipes


bin/kafka-run-class.sh

make changes in config/server.properties file. We have to set advertised.listeners to PLAINTEXT://localhost:9092

/usr/local/etc/kafka/server.properties

(base) hodqadms-MacBook-Pro:~ sbommireddy$ kafka-topics --describe --bootstrap-server localhost:9092 --topic raw_recipes
Topic: raw_recipes	PartitionCount: 2	ReplicationFactor: 1	Configs: segment.bytes=1073741824
	Topic: raw_recipes	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	Topic: raw_recipes	Partition: 1	Leader: 0	Replicas: 0	Isr: 0
(base) hodqadms-MacBook-Pro:~ sbommireddy$

beautifulsoup4
requests
lxml
kafka-python

Replication factor cannot be more than the number of brokers.

kafka-topics --list --zookeeper localhost:2181
kafka-topics --list --zookeeper localhost:2181
kafka-topics --delete --zookeeper localhost:2181 --topic testtopic

kafka-consumer-groups –bootstrap-server localhost:9092 --list
kafka-consumer-groups –bootstrap-server localhost:9092 --describe --group name-ofmy-group
