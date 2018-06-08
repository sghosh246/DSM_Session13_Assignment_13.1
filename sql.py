# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:29:42 2018

@author: souravg

"""

"""
Read the following data set:
https://archive.ics.uci.edu/ml/machine-learning-databases/adult/
Rename the columns as per the description from this file:
https://archive.ics.uci.edu/ml/machine-learn
ing-databases/adult/adult.names
Task:
Create a sql db from adult dataset and name it sqladb
1. Select 10 records from the adult sqladb
2. Show me the average hours per week of all men who are working in private sector
3. Show me the frequency table for education, occupation and relationship, separately
4. Are there any people who are married, working in private sector and having a masters
degree
5. What is the average, minimum and maximum age group for people working in
different sectors
6. Calculate age distribution by country
7. Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss
"""
import pandas as pd
import sqlite3
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
adultdata = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", sep=' *, *', header=None, engine="python")
adultdata.columns = ('age','workclass','fnlwgt','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country','salary')
adultdata.head(10)
# Create a sql db from adult dataset and name it sqladb
print("Create a sql db from adult dataset and name it sqladb\n",'-'*50, sep='')
conn=sqlite3.connect('sqladb.db')
adultdata.to_sql('atable', conn)
# 1.Select 10 records from the adult sqladb
print("Select 10 records from the adult sqladb\n",'-'*50, sep='')
cur = conn.cursor()
cur.execute("SELECT * FROM atable limit 10;")
rows = cur.fetchall()
for row in rows:
    print(row)
print('-'*50, sep='')
# 2.Show me the average hours per week of all men who are working in private sector
print("Show the average hours per week of all men who are working in private sector\n",'-'*70, sep='')
pysqldf("SELECT workclass, sex, avg(`hours-per-week`) as AVG_HRS_PER_WEEK FROM adultdata where sex= 'Male' and workclass = 'Private' group by workclass,sex;")
print('-'*70, sep='')
# 3.Show me the frequency table for education, occupation and relationship, separately
print("Show the frequency table for education, occupation and relationship, separately\n",'-'*65, sep='')
pysqldf("SELECT education,count(education) as Frequency FROM adultdata group by education;")
print('-'*65, sep='')
pysqldf("SELECT occupation,count(occupation) as Frequency FROM adultdata group by occupation;")
print('-'*65, sep='')
pysqldf("SELECT relationship,count(relationship) as Frequency FROM adultdata group by relationship;")
print('-'*65, sep='')
# 4. Are there any people who are married, working in private sector and having a masters degree
print("Are there any people who are married, working in private sector and having a masters degree\n",'-'*70, sep='')
pysqldf("SELECT EXISTS(SELECT * FROM adultdata where `marital-status` in ('Married-civ-spouse','Married-spouse-absent','Married-AF-spouse') and `workclass` = 'Private' and education = 'Masters') as Status;")
print("The Status 1 reveals - Yes, there are people who are married, working in private sector and having a masters degree\n",'-'*70, sep='')
print('-'*70, sep='')
# 5 What is the average, minimum and maximum age group for people working in different sectors
print("What is the average, minimum and maximum age group for people working in different sectors\n",'-'*70, sep='')
pysqldf("SELECT workclass, avg(age), min(age), max(age) from adultdata group by workclass;")
print('-'*70, sep='')
# 6.Calculate age distribution by country
print("Calculate age distribution by country\n",'-'*70, sep='')
pysqldf("SELECT `native-country`, avg(age), min(age), max(age) from adultdata group by `native-country`;")
print('-'*70, sep='')
# 7.Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss'
print("Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss'\n",'-'*70, sep='')
pysqldf("SELECT (`capital-gain` - `capital-loss`) as `Net-Capital-Gain` from adultdata;")
print('-'*70, sep='')