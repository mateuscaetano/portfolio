# List containers

docker ps

# Using spark submit

docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/pyspark_example.py

docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /scripts/pyspark_streaming_example.py

# Copying data
docker cp sample_data.csv spark-master:opt/sample_data.csv