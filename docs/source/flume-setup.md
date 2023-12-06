# flume setup

## 1. before start

follow all steps in [hadoop-3.1.3 cluster setup on linux](https://cloud.tencent.com/developer/article/2354856)

and then switch to root user:

```bash
su
```

## 2. cp flume and extract

```bash
tar -xvzf /opt/software/apache-flume-1.9.0-bin.tar.gz -C /opt/module
```

## 3. set env variables

```bash
vi /etc/profile
```

add the following 2 lines:

```bash
export FLUME_HOME="/opt/module/apache-flume-1.9.0-bin"
export PATH=$PATH:$FLUME_HOME/bin
export CLASSPATH=$CLASSPATH:$FLUME_HOME/lib
```

source or re-login:

```bash
source /etc/profile
```

run `flume-ng version` to test

## 4. set flume env

```bash
vi $FLUME_HOME/conf/flume-env.sh
# add: export JAVA_HOME="/opt/module/jdk8u392-b08"
```

## 5. test netcat agent

```bash
cd $FLUME_HOME
vi conf/test.conf
```

add：

```bash
agent.sources=s1
agent.channels=c1
agent.sinks=k1
agent.sources.s1.type=netcat
agent.sources.s1.channels=c1
agent.sources.s1.bind=0.0.0.0
agent.sources.s1.port=1234
agent.channels.c1.type=memory
agent.sinks.k1.type=logger
agent.sinks.k1.channel=c1
```

run agent:

```bash
flume-ng agent -n agent -c conf -f conf/test.conf -Dflume.root.logger=INFO,console &
telnet localhost 1234
# input some text to check events
```

to exit:

`fg` and then `Ctrl-C` to end flume-ng agent


## 6. test spool agent

```bash
cd $FLUME_HOME
vi conf/spool.conf
# mkdir /opt/module/hadoop/logs -p
```

```bash
agent.sources=s1
agent.channels=c1
agent.sinks=k1
agent.sources.s1.type=spooldir
agent.sources.s1.channels=c1
agent.sources.s1.spoolDir=/opt/module/hadoop/logs
agent.sources.s1.fileHeader = true
agent.channels.c1.type=memory
agent.sinks.k1.type=logger
agent.sinks.k1.channel=c1
```

run spool agent:

```bash
cd $FLUME_HOME
flume-ng agent -n agent -c conf -f conf/spool.conf -Dflume.root.logger=INFO,console &
echo "test spool" >> /opt/module/hadoop/logs/a1
```

## 7. test arvo agent

```bash
cd $FLUME_HOME
vi conf/arvo.conf
```

```bash
agent.sources=s1
agent.channels=c1
agent.sinks=k1
agent.sources.s1.type=avro
agent.sources.s1.channels=c1
agent.sources.s1.bind=0.0.0.0
agent.sources.s1.port = 4141
agent.channels.c1.type=memory
agent.sinks.k1.type=logger
agent.sinks.k1.channel=c1
```

start arvo agent:

```bash
cd $FLUME_HOME
flume-ng agent -n agent -c conf -f conf/arvo.conf -Dflume.root.logger=INFO,console &
```

run arvo-client:
```bash
touch $HADOOP_HOME/logs/a.log
cd $FLUME_HOME
bin/flume-ng avro-client --conf conf -H localhost -p 4141 -F $HADOOP_HOME/logs/a.log
echo "test arvo agent" >> $HADOOP_HOME/logs/a.log
```



## 8. test hdfs sink:

```bash
cd $FLUME_HOME
vi conf/arvo2hdfs.conf
```

```bash
agent.sources=s1
agent.channels=c1
agent.sinks=k1
agent.sources.s1.type=avro
agent.sources.s1.channels=c1
agent.sources.s1.bind=0.0.0.0
agent.sources.s1.port = 4141
agent.channels.c1.type=memory
agent.sinks.k1.type=hdfs
agent.sinks.k1.channel=c1
agent.sinks.k1.hdfs.path = /tmp/flume/
agent.sinks.k1.hdfs.filePrefix = log-events-
agent.sinks.k1.hdfs.fileType = DataStream
agent.sinks.k1.hdfs.writeFormat = Text
agent.sinks.k1.hdfs.batchSize = 100
agent.sinks.k1.hdfs.rollSize = 0
agent.sinks.k1.hdfs.rollCount = 10000
agent.channels.c1.type = memory
agent.channels.c1.capacity = 10000
agent.channels.c1.transactionCapacity = 100
# https://flume.apache.org/FlumeUserGuide.html#hdfs-sink
# a1.sources.r1.interceptors = i1
# a1.sources.r1.interceptors.i1.type = org.apache.flume.interceptor.TimestampInterceptor$Builder
```

start hdfs:

```bash
$HADOOP_HOME/sbin/start-dfs.sh
hadoop dfs -mkdir /tmp/flume
```

start agent:

```bash
cd $FLUME_HOME
# fix guava issue:
mv lib/guava-11.0.2.jar lib/guava-11.0.2.jar1
cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar ./lib
# start agent:
flume-ng agent -n agent -c conf -f conf/arvo2hdfs.conf -Dflume.root.logger=INFO,console &
```

run arvo client:

```bash
cd $FLUME_HOME
bin/flume-ng avro-client --conf conf -H localhost -p 4141 -F $HADOOP_HOME/logs/hadoop-root-namenode-master.log
```

check sink result in hdfs

```bash
hadoop dfs -ls /tmp/flume
```

## 9. test kafka sink

```bash
cd $FLUME_HOME
vi conf/nc2kafka.conf
```


```bash
a1.sources=s1
a1.channels=c1
a1.sinks=k1
a1.sources.s1.type=netcat
a1.sources.s1.channels=c1
a1.sources.s1.bind=localhost
a1.sources.s1.port=10050
a1.channels.c1.type=memory
a1.channels.c1.capacity=1000
a1.channels.c1.transactionCapacity=1000
a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = order
a1.sinks.k1.kafka.bootstrap.servers = localhost:9092
a1.sinks.k1.kafka.flumeBatchSize = 20
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.k1.kafka.producer.compression.type = snappy
```

start kafka and create topic:

```bash
cd $KAFKA_HOME
# start zookeeper:
./bin/zookeeper-server-start.sh config/zookeeper.properties &
# start kafka server:
./bin/kafka-server-start.sh config/server.properties &
# create topic:
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 4 --topic order
# list topics:
./bin/kafka-topics.sh --list --zookeeper localhost:2181
# start comsumer
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic order &
```

start flume:

```bash
flume-ng agent -n a1 -c conf -f conf/nc2kafka.conf -Dflume.root.logger=INFO,console &
telnet localhost 10050
# input some text to check events
```


## 10. test backup to hdfs

```bash
cd $FLUME_HOME
vi conf/multi-channels.conf
```


```bash
a1.sources=s1
a1.channels=c1 c2
a1.sinks=k1 k2
a1.sources.s1.type=netcat
a1.sources.s1.channels=c1
a1.sources.s1.bind=localhost
a1.sources.s1.port=10050
# c1
a1.channels.c1.type=memory
a1.channels.c1.capacity=1000
a1.channels.c1.transactionCapacity=1000
# k1: kafka
a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.channel = c1
a1.sinks.k1.kafka.topic = order
a1.sinks.k1.kafka.bootstrap.servers = localhost:9092
a1.sinks.k1.kafka.flumeBatchSize = 20
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.k1.kafka.producer.compression.type = snappy
# c2
a1.channels.c2.type=file
a1.channels.c2.capacity=1000
a1.channels.c2.transactionCapacity=1000
# k2: hdfs
a1.sinks.k2.type=hdfs
a1.sinks.k2.channel=c2
a1.sinks.k2.hdfs.path = /user/test/flumebackup/
a1.sinks.k2.hdfs.filePrefix = kfaka-backup-
a1.sinks.k2.hdfs.fileType = DataStream
a1.sinks.k2.hdfs.writeFormat = Text
a1.sinks.k2.hdfs.batchSize = 1000
a1.sinks.k2.hdfs.rollSize = 0
a1.sinks.k2.hdfs.rollCount = 10000
```

start flume:

```bash
hadoop dfs -mkdir -p /user/test/flumebackup
cd $FLUME_HOME
flume-ng agent -n a1 -c conf -f conf/multi-channels.conf -Dflume.root.logger=INFO,console &
telnet localhost 10050
# input some text to check events
hadoop dfs -ls /user/test/flumebackup
```

#TODO: fix hdfs sink

## 10. more information

download archive version of pkgs, view http://archive.apache.org/dist/spark/

for more information, view 

https://flume.apache.org/FlumeUserGuide.html

https://www.tutorialspoint.com/apache_flume/apache_flume_quick_guide.htm

