# After installing Docker Desktop run

docker-compose up

# Using spark submit

1. Find container id for the spark-master

docker ps

2. Execute from local
docker exec -it spark-master spark-submit --master spark://spark-master:7077 /shared/example.py

docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /shared/example_streaming.py

docker cp sample_data.csv spark-master:/opt/sample_data.csv

# Kafka

# Access the Kafka container
docker exec -it kafka /bin/bash

# Create a Kafka topic named 'test-topic'
/usr/bin/kafka-topics --create --topic test-topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

# Monitoring Kafka server

# Access the Kafka container
docker exec -it kafka /bin/bash

# List all Kafka topics
/usr/bin/kafka-topics --list --bootstrap-server kafka:9092

# Describe a Kafka topic to monitor its details
/usr/bin/kafka-topics --describe --topic test-topic --bootstrap-server kafka:9092

# See latest messages in a Kafka topic - Consume messages from the Kafka topic 'test-topic'
/usr/bin/kafka-console-consumer --bootstrap-server kafka:9092 --topic test-topic --from-beginning --timeout-ms 10000


# Access the HDFS namenode container
docker exec -it hdfs-namenode /bin/bash

# Put the CSV file into HDFS
hdfs dfs -put /sample_data/sample_data.csv /

# Grant write Access to jovyan user
docker exec -it hdfs-namenode /bin/bash

hdfs dfs -chmod -R 777 /

# For Delta Table support

docker exec -it spark-master /bin/bash

spark-shell --packages io.delta:delta-spark_2.12:3.3.0 --conf "spark.hadoop.fs.defaultFS=hdfs://hdfs-namenode:8020" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"

 