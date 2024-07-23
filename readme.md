```markdown
# Kafka Setup and Operations

## Summary

This project provides a comprehensive guide to setting up and using Apache Kafka for messaging and streaming applications. It covers the installation prerequisites, starting Zookeeper and Kafka servers, creating and managing Kafka topics, and running producer and consumer code. Additionally, it includes steps for cleanup and managing Kafka processes.

## Prerequisites

1. **Check Java Installation**
   Ensure that Java is installed on your system.
   ```sh
   java -version
   ```

   If Java is not installed, you can install it using Homebrew:
   ```sh
   brew install cask java8
   ```

2. **Kafka Installation Location**
   Navigate to the Kafka installation directory.
   ```sh
   cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
   ```

## Steps to Start and Use Kafka

### 1. Start Zookeeper

Zookeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. Kafka uses Zookeeper to manage distributed brokers.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
./bin/zookeeper-server-start.sh config/zookeeper.properties
```

### 2. Start Kafka

Start the Kafka server, which will allow you to produce and consume messages.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-server-start.sh config/server.properties
```

### 3. Create Kafka Topic

Create a new topic named `test_topic1` with a single partition and replication factor of 1.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
bin/kafka-topics.sh --create --topic test_topic1 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

### 4. List Kafka Topics

List all the topics currently available in the Kafka server.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 5. Run Producer Code

Execute the producer code to start sending messages to the Kafka topic.

```sh
python3 kafka_producer.py
```

### 6. Run Consumer Code

Execute the consumer code to start receiving messages from the Kafka topic.

```sh
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 spark_streaming.py
```

### Optional: Consume Messages from Console

Consume messages from the Kafka topic directly from the console for testing purposes.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test_topic --from-beginning
```

## Cleanup

### Stop Zookeeper

Stop the Zookeeper server gracefully.

```sh
cd /Users/<user_name>/Documents/Setup/kafka_2.12-3.7.1
./bin/zookeeper-server-stop.sh
```

### List Kafka Processes

List all the Kafka processes currently running.

```sh
ps aux | grep kafka-server-start.sh
```

### Kill Kafka Server

Terminate the Kafka server process using its PID (Process ID).

```sh
kill -9 PID
```

Replace `<user_name>` with your actual user name in the commands. This guide ensures you have a functional Kafka setup, from starting the necessary services to running producer and consumer code, and finally cleaning up.
```