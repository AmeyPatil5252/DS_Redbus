import mysql.connector
con = mysql.connector.connect(                   #connection
    host="localhost",
    user="root",
    password="Qazplm@1",
)
cursor = con.cursor()
cursor

query = "create database if not exists Redbus" #create Database
cursor.execute(query)

query = "use Redbus"
cursor.execute(query)

import pandas as pd #Cleaning and preparing database to be imported to SQL
import numpy as np
df = pd.read_excel(r"C:\Users\AMEY\Desktop\Dekstop\Guvi\Project\Redbus_data.xlsx")
df = df.replace({np.nan: None})
df['seats_available'] = df['seats_available'].str.split(' ', expand=True)[0]
df['bustype'] = df['bustype'].apply(lambda x: 'Non A/C' if 'Non' in x else 'A/C')
df

cursor.execute("DROP TABLE IF EXISTS RB_rawdata") #Fail safe method to avoide overlaaping of data

query = """create table if not exists RB_rawdata (
                                              route_name varchar(200),
                                              route_link varchar(500),
                                              route_start varchar(200), 
                                              route_end	 varchar(200),
                                              bus_name varchar(200),
                                              bustype varchar(200),
                                              departing_time time(0),
                                              duration varchar(200),
                                              reaching_time	 time(0),
                                              star_rating decimal(20.1),
                                              price decimal(20.1),
                                              seats_available int
                                              )
                                              """
cursor.execute(query)

query = "insert into RB_rawdata values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for index in df.index:
    row =list(df.loc[index].values)
    cursor.execute(query,row)
    con.commit()

query = "select * from RB_rawdata"
cursor.execute(query)
for info in cursor:
    print(info)