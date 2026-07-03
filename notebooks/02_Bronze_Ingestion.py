# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 02_Bronze_Ingestion
# MAGIC
# MAGIC ### Sprint 2 - Bronze Layer
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC The Landing Zone has been validated successfully.
# MAGIC
# MAGIC Load all source datasets into the Bronze layer as raw Delta tables while preserving the source data.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

CATALOG = "retailmax"
SCHEMA = "default"
VOLUME = "raw_files"

VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"

DATASETS = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv"
}

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS retailmax.audit.pipeline_audit
# MAGIC (
# MAGIC     pipeline_name STRING,
# MAGIC     dataset_name STRING,
# MAGIC     row_count BIGINT,
# MAGIC     status STRING,
# MAGIC     load_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

def write_audit_log(pipeline_name, dataset_name, row_count, status):

    audit_df = spark.createDataFrame(
        [
            (
                pipeline_name,
                dataset_name,
                row_count,
                status
            )
        ],
        [
            "pipeline_name",
            "dataset_name",
            "row_count",
            "status"
        ]
    ).withColumn(
        "load_timestamp",
        current_timestamp()
    )

    (
        audit_df.write
        .mode("append")
        .saveAsTable("retailmax.audit.pipeline_audit")
    )

# COMMAND ----------

def ingest_to_bronze(dataset_name, file_name):

    file_path = f"{VOLUME_PATH}/{dataset_name}/{file_name}"

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(file_path)
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file", lit(file_name))
    )

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(f"retailmax.bronze.{dataset_name}")
    )

    write_audit_log(
        pipeline_name="Bronze Ingestion",
        dataset_name=dataset_name,
        row_count=df.count(),
        status="SUCCESS"
    )

    print(f"- {dataset_name} loaded successfully")

# COMMAND ----------

for dataset, filename in DATASETS.items():
    ingest_to_bronze(dataset, filename)

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retailmax.bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.bronze.orders
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.audit.pipeline_audit
# MAGIC ORDER BY load_timestamp DESC;

# COMMAND ----------

