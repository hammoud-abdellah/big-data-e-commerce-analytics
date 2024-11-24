#HAMMOUD Abdellah
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum
import os

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Log Aggregation") \
    .config("spark.master", "local") \
    .getOrCreate()

# Input and Output Directories
input_dir = "D:/Cours et Labs/Big Data/e-commerce/backend/nifi_logs_output"  
output_dir = "D:/Cours et Labs/Big Data/e-commerce/backend/output"  

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Identify files that already exist in the output directory
existing_files = {file for file in os.listdir(output_dir) if file.endswith(".txt")}

# Read Input Logs
logs_df = spark.read.text(input_dir)

# Parse the Logs into Structured Data
parsed_logs = logs_df.selectExpr(
    "split(value, '\\\\|')[0] as timestamp",  # Full timestamp (e.g., 2024/11/18 13:46:37)
    "split(value, '\\\\|')[1] as product",    # Product name (e.g., Man T-shirt)
    "cast(split(value, '\\\\|')[3] as int) as price"  # Price (e.g., 2000)
)

# Extract Hour from Timestamp
parsed_logs = parsed_logs.withColumn("hour", col("timestamp").substr(1, 13))  # YYYY/MM/DD HH

# Aggregate Data: Total Price for Each Product Per Hour
aggregated_data = parsed_logs.groupBy("hour", "product").agg(
    _sum("price").alias("total_price")
)

# Collect the data for writing files
aggregated_data_list = aggregated_data.collect()

# Write each hour's data into a separate file
for row in aggregated_data_list:
    hour = row["hour"].replace("/", "").replace(" ", "")
    product = row["product"]
    total_price = row["total_price"]
    
    file_name = f"{hour}.txt"
    file_path = os.path.join(output_dir, file_name)
    
    # Skip writing if the file already existed before running the script
    if file_name in existing_files:
        print(f"File {file_name} already exists. Skipping.")
        continue
    
    # Write to the file
    with open(file_path, "a") as f:
        f.write(f"{row['hour']}|{row['product']}|{row['total_price']}\n")

print("Operation completed successfully.")

# Stop the Spark Session
spark.stop()