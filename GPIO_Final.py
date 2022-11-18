# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 23:28:27 2022

@author: JOSERIOS3PALACIOS
"""
import RPi.GPIO as GPIO
import time,os
from firebase import firebase
import threading
from eje3_ultrasonic import ultrasonic_sensor
from led_time import led_
import datetime
import MySQLdb
global db


#GPIO 
TRIG = 3
ECHO = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
GPIO.setup(2, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvula manual 
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Valvula automatica
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Vaciar
GPIO.setup (25, GPIO.OUT) #Valvula Llenado
GPIO.setup (26, GPIO.OUT) #Valvula Vaciado

# MYSQL DATABASE - General settings
# Settings for database connection
hostname = '172.20.34.21'
username = 'ijrios'
password = 'verbum_logos'
database = 'pidata'


print ("Waiting For Sensor To Settle")
time.sleep(1) #settling time 
def get_distance():
    dist_add = 0
    k = 0
    for x in range(20):
        try:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = (pulse_duration *  34300)/2

            distance = round(distance, 3)
            print (x, "distance: ", distance)

            dist_add = dist_add + distance
            #print "dist_add: ", dist_add
            time.sleep(.1) # 100ms interval between readings

        except Exception as e: 
        
            pass
        
    return distance
        
def read_firebase():
    global db
    while True:
        
        altura_tanque = db.get("/Configuracion/","Altura_Tanque")
        print("[INFO] Altura del tanque: {}".format(altura_tanque))
        
        nivel_minimo = db.get("/Configuracion/","nivelminimo")
        print("[INFO] nivel minimo: {}".format(nivel_minimo))
        
        nivel_maximo = db.get("/Configuracion/","Maximo")
        
        print("[INFO] nivel maximo: {}".format(nivel_maximo))
        time.sleep(1)


def read_MYSQL(identification,timestamp,level,rain):
    
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



def nivel_minimum(dist):
    
    altura_tanque=120
    nivel=altura_tanque-dist
    if(nivel<10):
        time.sleep(2)
        print("-------------------- ")
        print("Tanque vació: ", nivel)
        print("-------------------- ")
        return False  
    else:
        print("No está vacío") 
    return True

def nivel_maximum(dist):
    
    altura_tanque=120
    nivel=altura_tanque-dist
    if(nivel>115):
        time.sleep(2)
        print("-------------------- ")
        print("Tanque Lleno: ", nivel)
        print("-------------------- ")
        return False  
    else:
        print("No está LLeno") 
    return True
       

def main():
    
    global db
    #db = firebase.FirebaseApplication("https://digital-7a2c5-default-rtdb.firebaseio.com/")
    cont = 0
    # Print welcome 
    print('[{0:s}] starting on {1:s}...'.format("GPIO_Final", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

    while True:
        #db = firebase.FirebaseApplication("https://digital-7a2c5-default-rtdb.firebaseio.com/")
        distance=get_distance()
        print ("distance: ", distance)
        #t_read = threading.Thread(target = read_firebase)
        #t_sensor = threading.Thread(target = ultrasonic_sensor())
        #t_sensor.start()
        #t_read.start()

        valor = "En espera"
        #print("[INFO] Estado: {}".format(valor))
        #db.put("/Configuracion/","Estado", valor)
        
        #---- Se inician Entradas y Salidas
        input_manual = GPIO.input(2) #Manual
        input_auto = GPIO.input(22) #Automatica
        input_vacio = GPIO.input(23) #Seguir vacio
        output_llenado = GPIO.input(25) #Llenado
        output_vaciado = GPIO.input(26) #Vaciado
 
        #distancia = ultrasonic_sensor().get_distance(distance)
        minimun = nivel_minimum(distance)
        maximun = nivel_maximum(distance)
        print("---------------------------")

        #---------------------------Modo automatico---------------------------
        if (input_auto == False and input_manual == True):

            print("Modo Automatico ")
            
            if(minimun == False and maximun == True ):
                #Está vacío 
                valor = "Llenando"
                GPIO.output (25, GPIO.LOW) #Se abre - Llenado - prende led
                GPIO.output (26, GPIO.HIGH) #Se cierra - Vaciado - no prende led
                print("Se abre valvula llenado")
                print("Llenando")
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= cont+1
                #print("[INFO] Estado: {}".format(valor))
               #db.put("/Configuracion/","Estado", valor)
                read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                
        
            elif(maximun == False and minimun == True ):
                #Está lleno
                valor = "Vaciando"
                GPIO.output (25, GPIO.HIGH) #Se cierra - Llenado - apaga led
                GPIO.output (26, GPIO.LOW) #Se abre - Vaciado - prende led
                print("Se abre valvula Vaciado")
                print("Vaciando")
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= cont+1
                #print("[INFO] Estado: {}".format(valor))
               # db.put("/Configuracion/","Estado", valor)
                read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                
                
        #---------------------------Modo manual---------------------------
        elif (input_auto == True and input_manual == False):
          
            print("Modo Manual ")
               
            if(minimun == False and maximun == True ):
                print("Tanque vacío, desea llenar")
                if(input_vacio == False):
                    #Está vacío 
                    valor = "Llenando"
                    GPIO.output (25, GPIO.LOW) #Se abre - Llenado - prende led
                    GPIO.output (26, GPIO.HIGH) #Se cierra - Vaciado - apaga led
                    print("Se abre valvula llenado")
                    time.sleep(5)
                    print("-------------------------------")
                    print("------------Llenando-----------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                else:
                    print("-------------------------------")
                    print("----Esperando usuario----------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                #print("[INFO] Estado: {}".format(valor))
                #db.put("/Configuracion/","Estado", valor)
                
            elif(maximun == False and minimun == True):
                print("Tanque lleno, desea vaciar")
                if(input_vacio == True):
                    #Está lleno
                    valor = "Vaciando"
                    GPIO.output (25, GPIO.HIGH) #Se cierra - Llenado - prende led
                    GPIO.output (26, GPIO.LOW) #Se abre - Vaciado - apaga led
                    print("Se abre valvula Vaciado")
                    time.sleep(5)
                    print("-------------------------------")
                    print("------------Vaciando-----------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                else:
                    print("-------------------------------")
                    print("-----Esperando usuario---------")
                    print(".------------------------------")
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    read_MYSQL(cont,date,format(distance,'.2f'),format(distance,'.2f'))
                #rint("[INFO] Estado: {}".format(valor))
                #db.put("/Configuracion/","Estado", valor)

        time.sleep(1)
 
 
    
if __name__ == '__main__':
    main()

