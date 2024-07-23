from pyspark.sql import SparkSession


# Initialize Spark session
spark = SparkSession.builder \
    .appName("ReadParquetFiles") \
    .getOrCreate()

# Directory where Parquet files are stored
parquet_path = "data/output"

# Read Parquet files into DataFrame
df = spark.read.parquet(parquet_path)

# Show DataFrame schema and first few rows
df.printSchema()
df.show(truncate=False)

# Stop Spark session
spark.stop()
