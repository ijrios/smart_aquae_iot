# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:26:48 2022

@author: JOSERIOS3PALACIOS
"""

import datetime
import pymysql as MySQLdb

# MYSQL DATABASE - General settings
# Settings for database connection
hostname = '127.0.0.1'
username = 'pi'
password = 'raspberry'
database = 'pidata'

hire_start = datetime.datetime(2022, 11, 19, 3, 50, 00)
hire_end = datetime.datetime(2022, 11, 19, 4, 5, 30)

def query_with_fetchall():
    try:
        
        conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        query = ("SELECT * FROM electronica "
                 "WHERE timestamp BETWEEN %s AND %s")
        cursor.execute(query,(hire_start, hire_end))
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    query_with_fetchall()

