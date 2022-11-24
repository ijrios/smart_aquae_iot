# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 23:28:27 2022

@author: JOSERIOS3PALACIOS

"""
#Modules importari
import RPi.GPIO as GPIO
import time,os
from firebase import firebase
import threading
from eje3_ultrasonic import ultrasonic_sensor
from led_time import led_
import datetime
import pymysql as MySQLdb
global db


#Satus GPIO
TRIG = 3
ECHO = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
GPIO.setup(2, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvae manualis
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvae automatica
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvae inanis
GPIO.setup(11, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvae pluvia
GPIO.setup (25, GPIO.OUT) #Valvae imple
GPIO.setup (26, GPIO.OUT) #Valvae exinanita

#MYSQL DATABASE - General Occasus
#Optiones ad database nexu
hostname = '127.0.0.1'
username = 'pi'
password = 'raspberry'
database = 'pidata'


print("Expectans sensorem ad habitandum")
time.sleep(1) #Sedatis tempore

def adepto_distantia(sensorem):
    dist_addere = 0
    k = 0
    for x in range(20):
        numerare = 0
        try:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulsus_satus = time.time()

            while GPIO.input(ECHO)==1:
                pulsus_finis = time.time()

            pulsus_diuturnitas = pulsus_finis - pulsus_satus

            distantia = (pulsus_diuturnitas *  34300)/2

            distance = round(distance, 3)
            print(x, "distantia: ", distantia)

            dist_addere = dist_addere + distantia
            #print("dist_addere: ", dist_addere)
             
            if(sensorem == 1):
                numerare = numerare+0.1
                #print("[INFO] Rain:{}".format(pluvia))
            elif(sensorem == 0):
                numerare = numerare
            
            print(x, "Pluvia: ", numerare)
            time.sleep(.1) #100ms intervallum inter lectiones
         

        except Exception as e:
       
            pass
       
    return distantia,numerare
       
       
def legere_firebase():

    global db

    while True:
       
        altitudo_tank = db.get("/Occasum/","Altitudo_Cisternin")
        print("[INFO] Altitudo tank: {}".format(altitudotank))
       
        level_minimum = db.get("/Occasum/","levelminimum")
        print("[INFO] Minimum planum: {}".format(level_minimum))
       
        level_maximum = db.get("/Occasum/","Maximum")
        
        tempus = db.get("/Occasum/","Tempus")
       
        print("[INFO] Level maximum: {}".format(tempus))
        time.sleep(1)


def scribe_MYSQL(identification,timestamp,level,rain):
    print("Scribere database")
    query = "INSERT INTO electronica (identification,timestamp,level,rain) " \
                "VALUES (%s,%s,%s,%s)"
    args = (identification,timestamp,level,rain)

    try:
        conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    
def legere_MYSQL():

    try:
        
        conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        query = ("SELECT * FROM electronica ")
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print('Total Row(s):', cursor.rowcount)
        numerare = []
        for row in rows:
           numerare.append(row[0])

    except ValueError as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return numerare


def level_minimum(dist):
   
    altitudo_tank = 120
    level = altitudo_tank-dist
    if(level<10):
        time.sleep(2)
        print("-------------------- ")
        print("Inanis tank: ", level)
        print("-------------------- ")
        return False  
    else:
        print("Non est inanis")
    return True

def level_maximum(dist):
   
    altitudo_tank = 120
    level = altitudo_tank-dist
    if(level>115):
        time.sleep(2)
        print("-------------------- ")
        print("Plenus tank: ", level)
        print("-------------------- ")
        return False  
    else:
        print("Non plena")
    return True



def main():
   
    global db
    #db = firebase.FirebaseApplication("https://digital-7a2c5-default-rtdb.firebaseio.com/")
    cont = 0
    #Print welcome
    print('[{0:s}] starting on {1:s}...'.format("GPIO_Final", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
    
        
    while True:

        print("Legere database indices")
        ultima = legere_MYSQL()
        print(ultima)
    
        if(len(ultima) != 0):
            tardus = ultima[-1]
        else:
            tardus = 0

        input_pluvia = GPIO.input(11) #Sequitur inanis
        a, b = adepto_distantia(input_pluvia)
        print ("distantia: ", a)
        
        #Database firebase
        #t_rad = threading.Thread(target = read_firebase)
        #t_sensor = threading.Thread(target = ultrasonic_sensor())
        #t_sensor.start()
        #t_read.start()
        pretium = "De custodia"
        #print("[INFO] Conditio: {}".format(pretium))
        db.put("/Occasum/",Conditio", pretium)
       
        #---- Inputs et Outputs incipere
        input_manualis = GPIO.input(2) #Manualis
        input_auto = GPIO.input(22) #Automatic
        input_inanis = GPIO.input(23) #Sequi inanis
        
        output_imple = GPIO.input(25) #Imple
        output_exinanita = GPIO.input(26) #Exinanita
        
        #distantia = ultrasonic_sensor().adepto_distantia(distantia)
        minimun = level_minimum(a)
        maximun = level_maximum(a)
        print("---------------------------")

        #---------------------------Automatic modus---------------------------
        if (input_auto == False and input_manualis == True):

            print("------------Automatic modus----------------- ")
        
            if(minimun == False and maximun == True):
                #Inanis est
                pretium = "Impletio"
                GPIO.output (25, GPIO.LOW) #Aperit - Repletus - DUXERIT volvitur in
                GPIO.output (26, GPIO.HIGH) #Claudit - Inanis - DUXERIT non lucet
                print("Reple valvae opens")
                print("Impletio")
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= tardus+1
                #print("[INFO] Conditio: {}".format(pretium))
                #db.put("/Occasum/",Conditio", pretium)
                print("Database")
                write_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                print("Scriptum in database")
               
       
            elif(maximun == False and minimun == True ):
                #Plenum est
                print("Database")
                pretium = "Exinanitio"
                GPIO.output (25, GPIO.HIGH) #Claudit - Inanis - DUXERIT non lucet
                GPIO.output (26, GPIO.LOW) #Aperit - Repletus - DUXERIT volvitur in
                print("Exhaurire valvae opens")
                print("Exinanitio")
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= tardus+1
                #print("[INFO] Conditio: {}".format(pretium))
                #db.put("/Occasum/",Conditio", pretium)
                print("Database")
                scribe_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                print("Scriptum in database")
               
        #---------------------------Modus manualis---------------------------

        elif (input_auto == True and input_manualis == False):
         
            print("Modus manualis")
               
            if(minimun == False and maximun == True ):
                print("Tank inanis, vis imple")
                if(input_inanis == False):
                    #Inanis est
                    pretium = "Impletio"
                    GPIO.output (25, GPIO.LOW) #Aperit - Repletus - DUXERIT volvitur in
                    GPIO.output (26, GPIO.HIGH) #Claudit - Inanis - DUXERIT non lucet
                    print("Imple valvae opens")
                    time.sleep(5)
                    print("-------------------------------")
                    print("--------- Impletio ------------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= tardus+1
                    print("Database")
                    scribe_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                    print("Scriptum in database")
                else:
                    print("-------------------------------")
                    print("----- Expectans user ----------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= tardus+1
                    print("Database")
                    scribe_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                    print("Scriptum in database")
                    #print("[INFO] Conditio: {}".format(pretium))
                    #db.put("/Occasum/",Conditio", pretium)
               
            elif(maximun == False and minimun == True):
                print("Plena tank, vis evacuare")
                if(input_inanis == True):
                    #Plenum est
                    pretium = "Exinanitio"
                    GPIO.output (25, GPIO.HIGH) #Claudit - Inanis - DUXERIT non lucet
                    GPIO.output (26, GPIO.LOW) #Aperit - Repletus - DUXERIT volvitur in
                    print("Exhaurire valvae opens")
                    time.sleep(5)
                    print("-------------------------------")
                    print("--------- Exinanitio ----------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= tardus+1
                    print("Database")
                    scribe_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                    print("Scriptum in database")
                else:
                    print("-------------------------------")
                    print("------ Expectans user ---------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= tardus+1
                    print("Database")
                    scribe_MYSQL(str(cont),str(date),format(a,'.2f'),str(b))
                    print("Scriptum in database")
                    #print("[INFO] Conditio: {}".format(pretium))
                    #db.put("/Occasum/",Conditio", pretium)

        time.sleep(1)
        
 
if __name__ == '__main__':
    main()