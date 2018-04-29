#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('db.sqlite3')

conn.execute('''CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);''')
conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

cursor = conn.execute("SELECT * from COMPANY")
for row in cursor:
   print("ID = ", row[0])
   
conn.close()