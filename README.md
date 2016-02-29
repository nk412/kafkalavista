# kafkalavista
Kafkalavista is a CLI tool that lets you list and monitor Kafka topics, offsets and consumer lag by partition.

## Quick start
```
virtualenv env
source env/bin/activate
pip intall -r requirements.pip
```

Assuming you have zookeeper and kafka server running on the default ports, you can run `kafkalavista` with the following
```
python -m kafkalavista --zookeeper-hosts localhost:2181 --kafka-hosts 
```

