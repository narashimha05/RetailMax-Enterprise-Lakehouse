# Databricks notebook source
# MAGIC %md
# MAGIC # RetailMax Enterprise Lakehouse
# MAGIC
# MAGIC ## Notebook: 05_SQL_Analytics
# MAGIC
# MAGIC ### Sprint 5 - Business Analytics
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Business Story
# MAGIC
# MAGIC The Gold layer is now available.
# MAGIC
# MAGIC Business users require SQL reports to monitor sales, customers and products.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Deliverables
# MAGIC
# MAGIC - Sales Analytics
# MAGIC - Customer Analytics
# MAGIC - Product Analytics
# MAGIC - Executive KPIs

# COMMAND ----------

# MAGIC %md
# MAGIC # **Sales Analytics**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- what is our total revenue?
# MAGIC SELECT
# MAGIC     ROUND(SUM(daily_revenue),2) AS total_revenue
# MAGIC FROM retailmax.gold.daily_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- How many total orders have we processed?
# MAGIC SELECT
# MAGIC     SUM(total_orders) AS total_orders
# MAGIC FROM retailmax.gold.daily_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- What are the Top 10 sales days?
# MAGIC SELECT *
# MAGIC FROM retailmax.gold.daily_sales
# MAGIC ORDER BY daily_revenue DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Show monthly revenue trend
# MAGIC SELECT *
# MAGIC FROM retailmax.gold.monthly_sales
# MAGIC ORDER BY order_year, order_month;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Average order value per month
# MAGIC SELECT
# MAGIC     order_year,
# MAGIC     order_month,
# MAGIC
# MAGIC     ROUND(
# MAGIC         monthly_revenue / total_orders,
# MAGIC         2
# MAGIC     ) AS average_order_value
# MAGIC
# MAGIC FROM retailmax.gold.monthly_sales
# MAGIC
# MAGIC ORDER BY
# MAGIC order_year,
# MAGIC order_month;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # **Customer Analytics**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top 10 Customers
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.customer_summary
# MAGIC
# MAGIC ORDER BY total_spent DESC
# MAGIC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Customers with Most Orders
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.customer_summary
# MAGIC
# MAGIC ORDER BY total_orders DESC
# MAGIC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Average Customer Spend
# MAGIC SELECT
# MAGIC
# MAGIC ROUND(
# MAGIC AVG(total_spent),
# MAGIC 2
# MAGIC )
# MAGIC
# MAGIC AS average_customer_spend
# MAGIC
# MAGIC FROM retailmax.gold.customer_summary;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # **Product Analytics**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top Selling Products
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.product_summary
# MAGIC
# MAGIC ORDER BY revenue DESC
# MAGIC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Highest Quantity Sold
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.product_summary
# MAGIC
# MAGIC ORDER BY quantity_sold DESC
# MAGIC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Revenue by Category
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC category,
# MAGIC
# MAGIC ROUND(
# MAGIC SUM(revenue),
# MAGIC 2
# MAGIC )
# MAGIC
# MAGIC AS revenue
# MAGIC
# MAGIC FROM retailmax.gold.product_summary
# MAGIC
# MAGIC GROUP BY category
# MAGIC
# MAGIC ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC # **Executive Dashboard KPIs**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Total Customers
# MAGIC SELECT COUNT(*)
# MAGIC
# MAGIC FROM retailmax.silver.customers;
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC -- Total Products
# MAGIC SELECT COUNT(*)
# MAGIC
# MAGIC FROM retailmax.silver.products;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Total Orders
# MAGIC SELECT COUNT(*)
# MAGIC
# MAGIC FROM retailmax.silver.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC
# MAGIC ROUND(SUM(total_amount), 2)
# MAGIC
# MAGIC FROM retailmax.silver.orders;

# COMMAND ----------

# MAGIC %md
# MAGIC # **View**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW retailmax.gold.vw_sales_summary AS
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.daily_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.vw_sales_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- cte example
# MAGIC -- Business wants only days where revenue exceeded the average.
# MAGIC WITH avg_sales AS
# MAGIC (
# MAGIC SELECT
# MAGIC AVG(daily_revenue) avg_rev
# MAGIC
# MAGIC FROM retailmax.gold.daily_sales
# MAGIC )
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM retailmax.gold.daily_sales
# MAGIC
# MAGIC WHERE daily_revenue >
# MAGIC (
# MAGIC SELECT avg_rev
# MAGIC
# MAGIC FROM avg_sales
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Rank products by revenue.
# MAGIC SELECT
# MAGIC
# MAGIC product_name,
# MAGIC
# MAGIC revenue,
# MAGIC
# MAGIC RANK() OVER(
# MAGIC ORDER BY revenue DESC
# MAGIC )
# MAGIC
# MAGIC AS revenue_rank
# MAGIC
# MAGIC FROM retailmax.gold.product_summary;

# COMMAND ----------

