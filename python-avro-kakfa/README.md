virtualenv ./venv
source ./venv/bin/activate
pip install -r requirements.txt


Installing collected packages: certifi, chardet, idna, urllib3, requests, avro-python3, pytz, fastavro, confluent-kafka
Successfully installed avro-python3-1.9.2.1 certifi-2020.4.5.1 chardet-3.0.4 confluent-kafka-1.4.0 fastavro-0.23.4 idna-2.9 pytz-2020.1 requests-2.23.0 urllib3-1.25.9


==> Caveats
==> zookeeper
To have launchd start zookeeper now and restart at login:
  brew services start zookeeper
Or, if you don't want/need a background service you can just run:
  zkServer start
==> kafka
To have launchd start kafka now and restart at login:
  brew services start kafka
Or, if you don't want/need a background service you can just run:
  zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
(venv) (base) hodqadms-MacBook-Pro:python-avro-kakfa sbommireddy$

zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sgar

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic create-user-request

kafka-topics --list --bootstrap-server localhost:9092
kafka-topics --zookeeper localhost:2181 --delete --topic sgar

python send_record.py --topic create-user-request --schema-file create-user-request.avsc --record-value '{"email": "email@email.com", "firstName": "Bob", "lastName": "Jones"}'

 kafka-server-start /usr/local/etc/kafka/server.properties
 kafka-server-stop

 zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
 zookeeper-server-stop

 python send_record.py --topic create-user-request --schema-file create-user-request.avsc --record-value '{"email": "email@email.com", "firstName": "Bob", "lastName": "Jones"}'

 https://github.com/confluentinc/schema-registry#installation

 Assuming you have Zookeeper/Kafka running already, you can easily run Confulent Schema Registry using Docker with running the following command:

docker run -p 8081:8081 -e \
    SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL=localhost:2181 \
    -e SCHEMA_REGISTRY_HOST_NAME=localhost \
    -e SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8081 \
    -e SCHEMA_REGISTRY_DEBUG=true confluentinc/cp-schema-registry:5.5
