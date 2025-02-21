from pyspark.sql import SparkSession

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("SimpleSparkExample").getOrCreate()

    data = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]

    # Parallelize the data and convert it to a DataFrame
    df = spark.sparkContext.parallelize(data).toDF(["id", "name"])# Read a text file
   
    # Count the number of lines in the file
    line_count = df.count()

    # Print the result
    print(f"Number of lines in the file: {line_count}")

    df = spark.read.csv("/shared/sample_data.csv", header=True, inferSchema=True)
    df.show()
    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
