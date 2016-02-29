#!/usr/bin/env python

from kazoo.client import KazooClient
from pykafka import KafkaClient
from termcolor import colored
from tabulate import tabulate
import argparse
from pprint import pprint
import sys


def main():
    args = parse_args()
    kf = KafkaClient(args.kafka_hosts)
    zk = KazooClient(hosts=args.zookeeper_hosts, read_only=True)
    zk.start()

    topics2consumers = {}
    if args.topic:
        all_topics_to_consumers = get_topics_to_consumers(zk, kf)
        if args.topic not in all_topics_to_consumers.keys():
            raise SystemError("Could not find topic '{0}'".format(args.topic))
        selected_topic_consumers = all_topics_to_consumers.get(args.topic)
        if args.consumer:
            topics2consumers[args.topic] = filter(lambda x: x == args.consumer, selected_topic_consumers)
        else:
            topics2consumers[args.topic] = selected_topic_consumers
    else:
        topics2consumers = get_topics_to_consumers(zk, kf)

    for topic, consumers in topics2consumers.iteritems():
        print "Topic:", colored(topic, 'yellow')
        print "Active consumers:", colored(map(str, consumers), 'green')

        kafka_topic = kf.topics[topic]
        desc_topic(kafka_topic, args)
        print

        if args.show_consumer_lag:
            for cg in consumers:
                print "Consumer group:", colored(cg, 'green')
                show_consumer_lag(cg, kafka_topic, args)


def show_consumer_lag(cg, topic, args):
    simple_consumer = topic.get_simple_consumer(consumer_group=str(cg), auto_start=False)
    consumer_offset = simple_consumer.fetch_offsets()
    partitions = topic.partitions.values()
    data = []
    for c, p in zip(consumer_offset, partitions):
        current_offs = c[1].offset
        max_offs = p.latest_available_offset()
        data.append(
            [p.id, "{:,}".format(current_offs), "{:,}".format(max_offs), "{:,}".format(max_offs - current_offs)]
        )

    print tabulate(data, headers=['ID', 'Consumer offset', 'Largest offset', 'Lag (records)'],
                   tablefmt=args.table_format)


def desc_topic(kafka_topic, args):
    partitions = kafka_topic.partitions
    replicas = len(partitions.values()[0].replicas) - 1
    print "Number of partitions:", len(partitions)
    print "Number of replicas:", replicas

    if args.desc_partitions:
        data = []
        for id in sorted(partitions.keys()):
            p = partitions[id]
            leader = p.leader.host
            replicas = filter(lambda x: x != leader, map(lambda x: x.host, p.replicas))
            min_offset = p.earliest_available_offset()
            max_offset = p.latest_available_offset()
            data.append([id, leader, replicas, "{:,}".format(min_offset), "{:,}".format(max_offset),
                         "{:,}".format(max_offset - min_offset)])

        print tabulate(data, headers=['ID', 'Leader', 'Replicas', 'Smallest offset', 'Largest offset', 'Offset span'],
                       tablefmt=args.table_format)


def get_topics_to_consumers(zk, kf):
    """
    This function returns a dict where keys are kafka topics,
    and the values are a list of active consumers.
    :param zk: Kazoo zookeeper client
    :param kf: PyKafka client
    :returns dict
    """

    all_consumer_groups = zk.get_children('/consumers')
    all_topics = {}
    for topic in kf.topics:
        # We don't want kafka internal topics
        if topic.startswith('_'):
            continue
        all_topics[topic] = []

    for cg in all_consumer_groups:
        if zk.exists('/consumers/{0}/owners'.format(cg)):
            owners = zk.get_children('/consumers/{0}/owners'.format(cg))
            for owner in owners:
                if owner in all_topics:
                    all_topics[owner].append(cg)

    return all_topics


def parse_args():
    parser = argparse.ArgumentParser(description='Provide a quick overview of Kafka topics and consumers')
    parser.add_argument('--kafka-hosts', help="List of Kafka hosts", required=True)
    parser.add_argument('--zookeeper-hosts', help="List of ZooKeeper hosts", required=True)
    parser.add_argument('--topic', help='the name of a specific kafka topic')
    parser.add_argument('--consumer', help='to track a specific consumer for a topic')
    parser.add_argument('--desc-partitions', help='describe the partitions of a topic', action='store_true')
    parser.add_argument('--table-format', help='plain,simple,grid,fancy_grid,pipe,orgtbl,rst,mediawiki,html,latex')
    parser.add_argument('--show-consumer-lag', help='show lag for each consumer for topics', action='store_true')

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()
