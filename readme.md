Check java -
Java -version
brew install cask java8

Go to Kafka installation location - 
 cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1

————————
1. Start zookeeper - 
cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
./bin/zookeeper-server-start.sh config/zookeeper.properties

2. Start Kafka - 
 cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-server-start.sh config/server.properties

3. Create Kafka topic - 
 cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
bin/kafka-topics.sh --create --topic test_topic1 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

4. List Kafka topics - 
 cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092

5. Run producer code - 
python3 kafka_producer.py

For consuming messages (optional)
cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test_topic --from-beginning

6. Run consumer code - 
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 spark_streaming.py

Cleanup ————
For stopping zookeeper - 
 cd /Users/ruchaharshad/Documents/Setup/kafka_2.12-3.7.1
./bin/zookeeper-server-stop.sh

List Kafka processes live -
ps aux | grep kafka-server-start.sh

Kill Kafka server -
kill -9 PID
