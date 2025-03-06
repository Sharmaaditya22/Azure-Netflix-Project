# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Notebook Lookup Tables

# COMMAND ----------

# MAGIC %md
# MAGIC ### Parameters

# COMMAND ----------

dbutils.widgets.text('sourcefolder','netflix_cast')
dbutils.widgets.text('targetfolder','netflix_cast')

# COMMAND ----------

# MAGIC %md
# MAGIC ### variables

# COMMAND ----------

var_src_folder=dbutils.widgets.get('sourcefolder')
var_tgt_folder=dbutils.widgets.get('targetfolder')

# COMMAND ----------

df=spark.read.format('csv')\
    .option('header',True)\
    .option('inferSchema',True)\
    .load(f'abfss://bronze@netflixdatalakehouse.dfs.core.windows.net/{var_src_folder}')

# COMMAND ----------

display(df)

# COMMAND ----------

df.write.format('delta')\
    .mode('append')\
    .option('path',f'abfss://silver@netflixdatalakehouse.dfs.core.windows.net/{var_tgt_folder}')\
    .save()

# COMMAND ----------

