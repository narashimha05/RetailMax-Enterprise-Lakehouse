# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 07_Performance
# MAGIC
# MAGIC ### Sprint 7 - Performance Optimization
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC Optimize Spark jobs to improve performance and reduce execution time.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Deliverables
# MAGIC
# MAGIC - Compare file formats
# MAGIC - Learn caching
# MAGIC - Optimize joins
# MAGIC - Understand execution plans

# COMMAND ----------

orders_df = spark.table("retailmax.silver.orders")

# COMMAND ----------

orders_df.explain(True)

# COMMAND ----------

orders_df.cache()

# COMMAND ----------

orders_df.count()

# COMMAND ----------

orders_df.unpersist()

# COMMAND ----------

# RDD API is not supported on serverless - use alternative approach
from pyspark.sql import functions as F
print(orders_df.select(F.spark_partition_id()).distinct().count())

# COMMAND ----------

orders_repartitioned = orders_df.repartition(8)

# COMMAND ----------

print(
    orders_repartitioned.rdd.getNumPartitions()
)

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    current_timestamp,
    year,
    month,
    to_date,
    lit
)

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

write_audit_log(
    "Performance",
    "orders",
    orders_df.count(),
    "SUCCESS"
)

# COMMAND ----------

