# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *

# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Data Transformation

# COMMAND ----------

df=spark.read.format('delta')\
    .option('header',True)\
    .option('inferschema',True)\
    .load('abfss://bronze@netflixdatalakehouse.dfs.core.windows.net/netflix_titles')

# COMMAND ----------

#Autoloader create resure column in file.
df.display()

# COMMAND ----------

df=df.fillna({'duration_minutes':'0', 'duration_seasons':'1'})

# COMMAND ----------

df.display()

# COMMAND ----------

df=df.withColumn('duration_minutes',col('duration_minutes').cast(IntegerType()))\
    .withColumn('duration_seasons',col('duration_seasons').cast(IntegerType()))\
    .withColumn('date_added',to_date(col('date_added')))

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df=df.withColumn('shorttitle',split(col('title'),':')[0])
df.display()

# COMMAND ----------

df=df.withColumn('rating',split(col('rating'),'-')[0])
df.display()

# COMMAND ----------

df=df.withColumn('typeflag',when(col('type')=='Movie',lit(1))
                 .when(col('type')=='TV Show',lit(2)).otherwise(lit(0)))

# COMMAND ----------

df.display()

# COMMAND ----------

window=Window.orderBy(col('duration_minutes').desc())
df=df.withColumn('duration_rank',dense_rank().over(window))

# COMMAND ----------

df.display()

# COMMAND ----------

df_visualization=df.groupBy(col('type')).agg(count('*').alias('total_count'))
df_visualization.display()

# COMMAND ----------

df.write.format('delta')\
    .mode('overwrite')\
    .option('path','abfss://silver@netflixdatalakehouse.dfs.core.windows.net/netflix_titles')\
    .save()

# COMMAND ----------

