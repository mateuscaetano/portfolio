from pyspark.sql import SparkSession

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("SimpleSparkStreaming").getOrCreate()

    df = spark.readStream.format('kafka').option('kafka.bootstrap.servers', 'kafka:9092').option('subscribe', 'test-topic').load()
    
    df.selectExpr('CAST(key AS STRING)', 'CAST(value AS STRING)').writeStream.format('console').start().awaitTermination()

if __name__ == "__main__":
    main()
