# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 03_Silver_Transformation
# MAGIC
# MAGIC ### Sprint 3 - Silver Layer
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC Build trusted Silver tables by validating Bronze data.
# MAGIC
# MAGIC Invalid records must be moved to Quarantine.
# MAGIC
# MAGIC Valid records become the source for analytics.

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    current_timestamp,
    year,
    month,
    to_date,
    lit
)

CATALOG = "retailmax"

BRONZE = "bronze"
SILVER = "silver"
QUARANTINE = "quarantine"

# COMMAND ----------

customers_df = spark.table(f"{CATALOG}.{BRONZE}.customers")

products_df = spark.table(f"{CATALOG}.{BRONZE}.products")

orders_df = spark.table(f"{CATALOG}.{BRONZE}.orders")

# COMMAND ----------

valid_customers = customers_df.filter(
    col("customer_id").isNotNull() &
    col("email").isNotNull() &
    col("customer_status").isin("Active", "Inactive")
)

invalid_customers = customers_df.subtract(valid_customers)

# COMMAND ----------

valid_products = products_df.filter(
    col("product_id").isNotNull() &
    (col("unit_price") > 0) &
    col("category").isNotNull()
)

invalid_products = products_df.subtract(valid_products)

# COMMAND ----------

valid_orders = orders_df.filter(
    col("order_id").isNotNull() &
    col("customer_id").isNotNull() &
    col("product_id").isNotNull() &
    (col("quantity") > 0) &
    (col("delivery_date") >= col("order_date"))
)

invalid_orders = orders_df.subtract(valid_orders)

# COMMAND ----------

valid_orders = (
    valid_orders
    .withColumn(
        "order_date_only",
        to_date("order_date")
    )
    .withColumn(
        "order_year",
        year("order_date")
    )
    .withColumn(
        "order_month",
        month("order_date")
    )
)

# COMMAND ----------

valid_customers.write.mode("overwrite").saveAsTable(
    "retailmax.silver.customers"
)

valid_products.write.mode("overwrite").saveAsTable(
    "retailmax.silver.products"
)

valid_orders.write.mode("overwrite").saveAsTable(
    "retailmax.silver.orders"
)

# COMMAND ----------

invalid_customers.write.mode("overwrite").saveAsTable(
    "retailmax.quarantine.customers"
)

invalid_products.write.mode("overwrite").saveAsTable(
    "retailmax.quarantine.products"
)

invalid_orders.write.mode("overwrite").saveAsTable(
    "retailmax.quarantine.orders"
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
    "Silver Transformation",
    "customers",
    valid_customers.count(),
    "SUCCESS"
)

write_audit_log(
    "Silver Transformation",
    "products",
    valid_products.count(),
    "SUCCESS"
)

write_audit_log(
    "Silver Transformation",
    "orders",
    valid_orders.count(),
    "SUCCESS"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM retailmax.silver.customers;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retailmax.silver.products;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM retailmax.quarantine.customers;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retailmax.quarantine.products;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retailmax.quarantine.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.audit.pipeline_audit
# MAGIC ORDER BY load_timestamp DESC;

# COMMAND ----------

