# Databricks notebook source
# MAGIC %md
# MAGIC ### Array Parameter

# COMMAND ----------

files=[
    {
        'sourcefolder':'netflix_directors',
        'targetfolder':'netflix_directors'
   },
    {
        'sourcefolder':'netflix_cast',
        'targetfolder':'netflix_cast'
   },
    {
        'sourcefolder':'netflix_category',
        'targetfolder':'netflix_category'
   },
    {
        'sourcefolder':'netflix_countries',
        'targetfolder':'netflix_countries'
   }
    
]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Job utility to reture the Array

# COMMAND ----------

dbutils.jobs.taskValues.set(key='myarr',value=files)