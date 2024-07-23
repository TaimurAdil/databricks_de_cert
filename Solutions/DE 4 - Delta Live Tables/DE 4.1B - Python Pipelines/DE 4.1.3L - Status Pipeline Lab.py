# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Troubleshooting DLT Python Syntax
# MAGIC
# MAGIC Now that we've gone through the process of configuring and running a pipeline with 2 notebooks, we'll simulate developing and adding a 3rd notebook.
# MAGIC
# MAGIC **DON'T PANIC!**
# MAGIC
# MAGIC The code provided below contains some intentional, small syntax errors. By troubleshooting these errors, you'll learn how to iteratively develop DLT code and identify errors in your syntax.
# MAGIC
# MAGIC This lesson is not meant to provide a robust solution for code development and testing; rather, it is intended to help users getting started with DLT and struggling with an unfamiliar syntax.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC By the end of this lesson, students should feel comfortable:
# MAGIC * Identifying and troubleshooting DLT syntax 
# MAGIC * Iteratively developing DLT pipelines with notebooks

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add this Notebook to a DLT Pipeline
# MAGIC
# MAGIC At this point in the course, you should have a DLT Pipeline configured with 2 notebook library.
# MAGIC
# MAGIC You should have processed several batches of records through this pipeline, and should understand how to trigger a new run of the pipeline and add an additional library.
# MAGIC
# MAGIC To begin this lesson, go through the process of adding this notebook to your pipeline using the DLT UI, and then trigger an update.
# MAGIC
# MAGIC <img src="https://files.training.databricks.com/images/icon_hint_24.png"> The link to this notebook can be found back in [DE 4.1 - DLT UI Walkthrough]($../DE 4.1 - DLT UI Walkthrough)<br/>
# MAGIC in the printed instructions for **Task #3** under the section **Generate Pipline Configuration**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Troubleshooting Errors
# MAGIC
# MAGIC Each of the 3 functions below contains a syntax error, but each of these errors will be detected and reported slightly differently by DLT.
# MAGIC
# MAGIC Some syntax errors will be detected during the **Initializing** stage, as DLT is not able to properly parse the commands.
# MAGIC
# MAGIC Other syntax errors will be deteced during the **Setting up tables** stage.
# MAGIC
# MAGIC Note that because of the way DLT resolves the order of tables in the pipeline at different steps, you may sometimes see errors thrown for later stages first.
# MAGIC
# MAGIC An approach that can work well is to fix one table at a time, starting at your earliest dataset and working toward your final. Commented code will be ignored automatically, so you can safely remove code from a development run without removing it entirely.
# MAGIC
# MAGIC Even if you can immediately spot the errors in the code below, try to use the error messages from the UI to guide your identification of these errors. Solution code follows in the cell below.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Solutions
# MAGIC
# MAGIC The correct syntax for each of our above functions is provided in a notebook by the same name in the Solutions folder.
# MAGIC
# MAGIC To address these errors you have serveral options:
# MAGIC * Work through each issue, fixing the problems above yourself
# MAGIC * Copy and paste the solution in the **`# ANSWER`** cell from the Solutions notebook of the same name
# MAGIC * Update your pipline to directly use the Solutions notebook of the same name
# MAGIC
# MAGIC **NOTE**: You won't be able to see any of the other errors until you add the **`import dlt`** statement to the cell above.
# MAGIC
# MAGIC The issues in each query:
# MAGIC 1. The **`@dlt.table`** decorator is missing before the function definition
# MAGIC 1. The correct keyword argument to provide a custom table name is **`name`** not **`table_name`**
# MAGIC 1. To perform a read on a table in the pipeline, use **`dlt.read`** not **`spark.read`**

# COMMAND ----------

# ANSWER
import dlt
import pyspark.sql.functions as F

source = spark.conf.get("source")


@dlt.table
def status_bronze():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load(f"{source}/status")
            .select(
                F.current_timestamp().alias("processing_time"), 
                F.input_file_name().alias("source_file"), 
                "*"
            )
    )

    
@dlt.table(
        name = "status_silver"
    )
@dlt.expect_or_drop("valid_timestamp", "status_timestamp > 1640995200")
def status_silver():
    return (
        dlt.read_stream("status_bronze")
            .drop("source_file", "_rescued_data")
    )

    
@dlt.table
def email_updates():
    return (
        dlt.read("status_silver").alias("a")
            .join(
                dlt.read("subscribed_order_emails_v").alias("b"), 
                on="order_id"
            ).select(
                "a.*", 
                "b.email"
            )
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC By reviewing this notebook, you should now feel comfortable:
# MAGIC * Identifying and troubleshooting DLT syntax 
# MAGIC * Iteratively developing DLT pipelines with notebooks

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>