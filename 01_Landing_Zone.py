# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 01_Landing_Zone
# MAGIC
# MAGIC ### Sprint 1 - Landing Zone
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC RetailMax has received today's source files.
# MAGIC
# MAGIC Before ingestion into the Bronze layer, the Data Engineering team must validate the incoming datasets.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Deliverables
# MAGIC
# MAGIC - Read source files
# MAGIC - Validate availability
# MAGIC - Profile datasets
# MAGIC - Generate Landing Validation Report

# COMMAND ----------

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

for folder, filename in DATASETS.items():
    print(f"Checking {folder}...")

    display(
        dbutils.fs.ls(f"{VOLUME_PATH}/{folder}")
    )

# COMMAND ----------

landing_summary = []

for dataset, filename in DATASETS.items():

    file_path = f"{VOLUME_PATH}/{dataset}/{filename}"

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(file_path)
    )

    landing_summary.append(
        (
            dataset,
            df.count(),
            len(df.columns),
            "SUCCESS"
        )
    )

# COMMAND ----------

summary_df = spark.createDataFrame(
    landing_summary,
    [
        "dataset",
        "row_count",
        "column_count",
        "status"
    ]
)

display(summary_df)

# COMMAND ----------

(
    summary_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retailmax.audit.landing_validation_report")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retailmax.audit.landing_validation_report;

# COMMAND ----------

