# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 04_Gold_Analytics
# MAGIC
# MAGIC ### Sprint 4 - Gold Layer
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC The business teams require analytics-ready tables for reporting.
# MAGIC
# MAGIC Build Gold tables from the trusted Silver layer.

# COMMAND ----------

from pyspark.sql.functions import (
    sum,
    count,
    round,
    col
)

CATALOG = "retailmax"
SILVER = "silver"

# COMMAND ----------

customers_df = spark.table(f"{CATALOG}.{SILVER}.customers")

products_df = spark.table(f"{CATALOG}.{SILVER}.products")

orders_df = spark.table(f"{CATALOG}.{SILVER}.orders")

# COMMAND ----------

### Gold Table1 - Daily Sales
### How much revenue do we make every day?

daily_sales_df = (
    orders_df
    .groupBy("order_date_only")
    .agg(
        sum("total_amount").alias("daily_revenue"),
        count("order_id").alias("total_orders")
    )
)

# COMMAND ----------

daily_sales_df.write \
.mode("overwrite") \
.saveAsTable("retailmax.gold.daily_sales")

# COMMAND ----------

### Gold Table 2 — Monthly Sales
### What are monthly sales trends?

monthly_sales_df = (
    orders_df
    .groupBy(
        "order_year",
        "order_month"
    )
    .agg(
        sum("total_amount").alias("monthly_revenue"),
        count("order_id").alias("total_orders")
    )
)

# COMMAND ----------

monthly_sales_df.write \
.mode("overwrite") \
.saveAsTable("retailmax.gold.monthly_sales")

# COMMAND ----------

### Gold Table 3 — Customer Summary
### Who are our best customers?

customer_summary_df = (
    orders_df
    .join(
        customers_df,
        "customer_id"
    )
    .groupBy(
        "customer_id",
        "first_name",
        "last_name"
    )
    .agg(
        count("order_id").alias("total_orders"),
        round(
            sum("total_amount"),
            2
        ).alias("total_spent")
    )
)

# COMMAND ----------

customer_summary_df.write \
.mode("overwrite") \
.saveAsTable("retailmax.gold.customer_summary")

# COMMAND ----------

### Gold Table 4 — Product Summary
### Which products generate the most revenue?

product_summary_df = (
    orders_df
    .join(
        products_df,
        "product_id"
    )
    .groupBy(
        "product_id",
        "product_name",
        "category"
    )
    .agg(
        sum("quantity").alias("quantity_sold"),
        round(
            sum("total_amount"),
            2
        ).alias("revenue")
    )
)

# COMMAND ----------

product_summary_df.write \
.mode("overwrite") \
.saveAsTable("retailmax.gold.product_summary")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retailmax.gold;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.gold.daily_sales;

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

def write_audit_log(pipeline_name, dataset_name, row_count, status):

    audit_data = [
        (
            pipeline_name,
            dataset_name,
            row_count,
            status
        )
    ]

    audit_df = (
        spark.createDataFrame(
            audit_data,
            [
                "pipeline_name",
                "dataset_name",
                "row_count",
                "status"
            ]
        )
        .withColumn("load_timestamp", current_timestamp())
    )

    (
        audit_df.write
        .mode("append")
        .saveAsTable("retailmax.audit.pipeline_audit")
    )

# COMMAND ----------

write_audit_log(
    "Gold Analytics",
    "daily_sales",
    daily_sales_df.count(),
    "SUCCESS"
)

write_audit_log(
    "Gold Analytics",
    "monthly_sales",
    monthly_sales_df.count(),
    "SUCCESS"
)

write_audit_log(
    "Gold Analytics",
    "customer_summary",
    customer_summary_df.count(),
    "SUCCESS"
)

write_audit_log(
    "Gold Analytics",
    "product_summary",
    product_summary_df.count(),
    "SUCCESS"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.audit.pipeline_audit
# MAGIC ORDER BY load_timestamp DESC;

# COMMAND ----------

