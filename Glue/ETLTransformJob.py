import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import col, current_timestamp

# Get filename passed from Step Functions
args = getResolvedOptions(sys.argv, ['input_file'])

input_file = args['input_file']

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

print(f"Processing File : {input_file}")

df = spark.read.option(
    "header",
    "true"
).csv(
    f"s3://yash-etl-raw-zone/{input_file}"
)

df = df.filter(
    col("name").isNotNull() &
    col("salary").isNotNull()
)

df = df.withColumn(
    "salary",
    col("salary").cast("int")
)

df = df.withColumn(
    "processed_timestamp",
    current_timestamp()
)

df.write.mode("overwrite") \
.option("header","true") \
.csv(
    f"s3://yash-etl-processed-zone/{input_file.split('.')[0]}/"
)

print("ETL Completed Successfully")