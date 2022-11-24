# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:26:48 2022

@author: JOSERIOS3PALACIOS

"""

import datetime
import pymysql as MySQLdb

#MYSQL DATABASE - General Occasus
#Optiones ad database nexu
hostname = '127.0.0.1'
username = 'pi'
password = 'raspberry'
database = 'pidata'


def query_cum_fetchall(pretium_satus,pretium_finis):

    try:
        
        conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        query = ("SELECT * FROM electronica "
                 "WHERE timestamp BETWEEN %s AND %s")
        cursor.execute(query,(pretium_satus,pretium_finis))
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
    
    except ValueError as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return rows


if __name__ == '__main__':

    print("Intra latitudinem temporum vis consulere")
    print("Intra initium date")
    annus_1 = int(input("Intra annum initium date: "))
    mensis_1 = int(input("Intra mense initium date: ")) 
    diem_1 = int(input("Intra diem initium date: "))
    print("Intra initium temporis")
    hora_1 = int(input("Intra hora initium date: "))
    minuta_1 = int(input("Intra minuta initium date: "))
    seconds_1 = int(input("Intrant ducens seconds: "))

    print("Intra finem date")
    annus_2 = int(input("Intra annum finalis date: "))
    mensis_2 = int(input("Intra mense finalis date: ")) 
    diem_2 = int(input("Intra diem finalis date: "))
    print("Intra finem temporis")
    hora_2 = int(input("Intra hora finis date: "))
    minuta_2 = int(input("Intra minuta finalis date: "))
    seconds_2 = int(input("Intra seconds finalis date: "))
    
    pretium_satus = datetime.datetime(annus_1, mensis_1, diem_1, hora_1, minuta_1, seconds_1)
    pretium_finis = datetime.datetime(annus_2, mensis_2, diem_2, hora_2, minuta_2, seconds_2)
    archive = query_cum_fetchall(pretium_satus,pretium_finis)
    
    #Scribe archive
    file = open("test.txt","w")
    file.writelines("identification,timestamp,level,rain")

    for row in archive:
        dato = str(row)
        string = dato.replace("(","").replace(")","")
        print(string)
        file.writelines("\n")
        file.writelines(str(string))
    print("Generatae file")
    file.close()
