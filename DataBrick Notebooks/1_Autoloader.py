# Databricks notebook source
# MAGIC %md
# MAGIC # Incremental data loading using Autoloader

# COMMAND ----------

# MAGIC %sql
# MAGIC create schema netflix_catalog.net_schema;

# COMMAND ----------

checkpoint_location="abfss://silver@netflixdatalakehouse.dfs.core.windows.net/checkpoint"

# COMMAND ----------

# Stream only run when action is perform like display, collect , show and write.
df=spark.readStream\
    .format('cloudFiles')\
    .option('cloudFiles.format','csv')\
    .option('cloudFiles.schemaLocation',checkpoint_location)\
    .load('abfss://raw@netflixdatalakehouse.dfs.core.windows.net')

# COMMAND ----------

display(df)

# COMMAND ----------

# availableNow for bulk load the data in trigger

df.writeStream\
    .option('checkpointLocation', checkpoint_location)\
    .trigger(processingTime='10 seconds')\
    .start('abfss://bronze@netflixdatalakehouse.dfs.core.windows.net/netflix_titles')
    

# COMMAND ----------

