# kafkalavista
Kafkalavista is a CLI tool that lets you list and monitor Kafka topics, offsets and consumer lag by partition.

## Quick start
```
virtualenv env
source env/bin/activate
pip install -r requirements.pip
```

Assuming you have zookeeper and kafka server running on the default ports, you can run `kafkalavista` with the following:
```
python -m kafkalavista --zookeeper-hosts localhost:2181 --kafka-hosts localhost:9092
```
This will list all available topics and active consumers.

## Basic Usage
The following options can be used to further select and drill down on to a topic/consumer.

#### List a specific topic
`--topic <topic name>`

#### List a specific consumer for a topic
`--consumer <consumer group name>`

#### Describe a partition and offsets
`--desc-partitions`

*(If a specific topic is not selected, all kafka topics are described)*

#### Show consumer lag by partition
`--show-consumer-lag`

*(If a specific topic/consumer is not selected, all kakfa topics and their consumer lags are listed)*

