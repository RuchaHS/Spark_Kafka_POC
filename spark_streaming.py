from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr, udf, explode
from pyspark.sql.column import Column
from pyspark.sql.functions import xpath
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, ArrayType
import xml.etree.ElementTree as ET
import os

topic = "test_topic4"
spark = SparkSession \
    .builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
    .config("spark.sql.shuffle.partitions", 4) \
    .master("local[*]") \
    .getOrCreate()

log_schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("level", StringType(), True),
    StructField("message", StringType(), True)
])

def from_xml(col, schema, options={}):
  scala_datatype = spark._jsparkSession.parseDataType(schema.json())
  scala_options = sc._jvm.PythonUtils.toScalaMap(options)
  jc = sc._jvm.com.databricks.spark.xml.functions.from_xml(col._jc if isinstance(col, Column) else col, scala_datatype, scala_options)
  return Column(jc)

# Define schema for XML logs
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("level", StringType(), True),
    StructField("message", StringType(), True)
])

# Read from Kafka
print("Reading from topic", topic)
kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", topic).option("startingOffsets", "earliest").load()

print("Consumed data from topic", topic)
# FOR DEBUGGING PURPOSE
# kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#     .writeStream \
#     .format("console") \
#     .option("truncate", "false")\
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()

print("Starting to parse XML")
# Parse XML
# Define a UDF to parse the XML content
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    logs = []
    for log in root.findall('log'):
        timestamp = log.find('timestamp').text
        level = log.find('level').text
        message = log.find('message').text
        logs.append((timestamp, level, message))
    return logs

# Register the UDF
parse_xml_udf = udf(parse_xml, ArrayType(StructType([
    StructField("timestamp", StringType(), True),
    StructField("level", StringType(), True),
    StructField("message", StringType(), True)
])))

parsed_df = kafka_df.withColumn("parsed_logs", explode(parse_xml_udf(col("value"))))

# Select the required columns
final_parsed_df = parsed_df.selectExpr("parsed_logs.timestamp as timestamp", "parsed_logs.level as level", "parsed_logs.message as message")

print("Sucessfully parsed xml log messages to storage location")

# FOR DEBUGGING PURPOSE
# final_parsed_df.selectExpr("CAST(timestamp AS STRING)", "CAST(level AS STRING)", "CAST(message AS STRING)") \
#     .writeStream \
#     .format("console") \
#     .option("truncate", "false")\
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()

# Data validation (simple example)
validated_df = final_parsed_df.filter("timestamp IS NOT NULL AND level IS NOT NULL AND message IS NOT NULL")
print("Successfully completed data validation")

# Deduplication
deduplicated_df = validated_df.dropDuplicates(["timestamp", "message"])
print("Successfully completed data deduplication")

# Write to storage location
query = deduplicated_df.writeStream.format("parquet").option("checkpointLocation", "data/checkpointing").option("path", "data/output").start()

query.awaitTermination()
print("Successfully completed data writing to storage location")
