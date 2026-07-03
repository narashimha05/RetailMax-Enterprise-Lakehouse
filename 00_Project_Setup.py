# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 00_Project_Setup
# MAGIC
# MAGIC ### Sprint 0 - Environment Setup
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Business Story
# MAGIC
# MAGIC RetailMax is migrating its reporting platform to Databricks.
# MAGIC
# MAGIC The Data Engineering team must prepare the Lakehouse environment before any data is loaded.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Deliverables
# MAGIC
# MAGIC - Create Catalog
# MAGIC - Create Schemas
# MAGIC - Create Volume
# MAGIC - Verify Environment

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS retailmax;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG retailmax;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS landing;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS silver;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS gold;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS audit;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS quarantine;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS sandbox;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS raw_files;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

CATALOG = "retailmax"
SCHEMA = "default"
VOLUME = "raw_files"

VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"

display(dbutils.fs.ls(VOLUME_PATH))

# COMMAND ----------

display(dbutils.fs.ls(f"{VOLUME_PATH}/customers"))

# COMMAND ----------

