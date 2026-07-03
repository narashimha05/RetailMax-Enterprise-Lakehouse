# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC
# MAGIC #Title
# MAGIC
# MAGIC Manage Changes in the Lakehouse
# MAGIC
# MAGIC ##Business Requirement
# MAGIC
# MAGIC RetailMax has already built its data platform.
# MAGIC
# MAGIC Now business data changes every day.
# MAGIC
# MAGIC ###Examples:
# MAGIC
# MAGIC Product prices change.
# MAGIC Customers become inactive.
# MAGIC Orders are cancelled.
# MAGIC New orders arrive.
# MAGIC Wrong records need correction.
# MAGIC
# MAGIC The Data Engineering team must manage these changes without recreating the entire table.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY retailmax.silver.orders;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Customer Support informs us that all Pending orders should now be marked as Completed.
# MAGIC UPDATE retailmax.silver.orders
# MAGIC
# MAGIC SET order_status = 'Completed'
# MAGIC
# MAGIC WHERE order_status = 'Pending';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT order_status
# MAGIC
# MAGIC FROM retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- business wants cancelled orders to be deleted
# MAGIC
# MAGIC DELETE FROM retailmax.silver.orders
# MAGIC
# MAGIC WHERE order_status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.silver.orders
# MAGIC
# MAGIC WHERE order_status='Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DESCRIBE HISTORY retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.silver.orders
# MAGIC
# MAGIC VERSION AS OF 0
# MAGIC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE retailmax.sandbox.order_updates AS
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.silver.orders
# MAGIC
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE retailmax.sandbox.order_updates
# MAGIC
# MAGIC SET total_amount = total_amount + 500;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO retailmax.silver.orders target
# MAGIC
# MAGIC USING retailmax.sandbox.order_updates source
# MAGIC
# MAGIC ON target.order_id = source.order_id
# MAGIC
# MAGIC WHEN MATCHED THEN
# MAGIC
# MAGIC UPDATE SET *
# MAGIC
# MAGIC WHEN NOT MATCHED THEN
# MAGIC
# MAGIC INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.sandbox.order_updates;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Business adds a new column.
# MAGIC
# MAGIC ALTER TABLE retailmax.silver.orders
# MAGIC
# MAGIC ADD COLUMNS (discount DOUBLE);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY retailmax.silver.orders;

# COMMAND ----------

