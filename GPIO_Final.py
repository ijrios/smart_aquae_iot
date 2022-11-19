# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 23:28:27 2022

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


#GPIO portubus
TRIG = 3
ECHO = 4
GPIO.setwarnings(False) #Satus terrores
GPIO.setmode(GPIO.BCM) #GPIOs sunt initialized
GPIO.setup(TRIG,GPIO.OUT) #Ultrasound sensorem
GPIO.setup(ECHO,GPIO.IN) #Ultrasound sensorem
GPIO.output(TRIG, False) #Ultrasound sensorem
GPIO.setup(2, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Manualis valvae 
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Automatic valvae 
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP) #Exinanitio
GPIO.setup (25, GPIO.OUT) #Implens valvae
GPIO.setup (26, GPIO.OUT) #Exinanitio valvae

# MYSQL DATABASE - General Occasus
# Optiones ad database nexu
hostname = '172.20.34.21'
username = 'ijrios'
password = 'verbum_logos'
database = 'pidata'

class pluviometer:
    def __init__(self, rain_pin = 2, sample_time = 10):
        self.rain_pin = rain_pin
        self.sample_time = sample_time
        self.counter = 0
        self.rain = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rain_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.rain_pin, GPIO.FALLING, callback = self.count_pulses, bouncetime = 300)
        t_rain = threading.Thread(target = self.get_rain)
        t_rain.start()
    
    def count_pulses(self, rain_pin):
        if GPIO.input(self.rain_pin) == False:
            self.counter = self.counter + 1
            print("[INFO] counter:{}".format(self.counter))
            
            
    def obtinere_pluvia(self):
        while True:
            time.sleep(self.sample_time)
            self.rain = self.counter *0.2
            
            print("[INFO] Rain:{}".format(self.rain))
            
def obtinere_distantia():
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

            pulsus_duratione = pulsus_finis - pulsus_satus
            #conversus distantia
            distantia = (pulsus_duratione *  34300)/2
            #nos organize distantia
            distantia = round(distantia, 3)
            #nos imprimere distantia
            print (x, "distantia: ", distantia)
            dist_add = dist_add + distantia
            #print "dist_add: ", dist_add
            time.sleep(.1) # 100ms inter lectiones

        except Exception as e: 
 
            pass
        
    return distantia
        
def scribere_firebase():
    global db
    while True:
        
        altura_tanque = db.get("/Configuracion/","Altura_Tanque")
        print("[INFO] Altura del tanque: {}".format(altura_tanque))
        
        nivel_minimo = db.get("/Configuracion/","nivelminimo")
        print("[INFO] nivel minimo: {}".format(nivel_minimo))
        
        nivel_maximo = db.get("/Configuracion/","Maximo")
        
        print("[INFO] max level: {}".format(nivel_maximo))
        time.sleep(1)


def scribere_MYSQL(identification,timestamp,level,rain):
    
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
    
    tank_altitudo=120
    level=tank_altitudo-dist
    if(level<10):
        time.sleep(2)
        print("-------------------- ")
        print("Inanis tank: ", level )
        print("-------------------- ")
        return False  
    else:
        print("Non est inanis") 
    return True

def nivel_maximum(dist):
    
    tank_altitudo=120
    level=tank_altitudo-dist
    if(level>115):
        time.sleep(2)
        print("-------------------- ")
        print("Plena tank: ",   level)
        print("-------------------- ")
        return False  
    else:
        print("Non plena") 
    return True
       
print("Expectans sensorem ad habitandum")
time.sleep(1) #Sedatis tempore

def main():
    
    global db
    cont = 0
    #Print welcome 
    print('[{0:s}] starting on {1:s}...'.format("GPIO_Final", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
    #db = firebase.FirebaseApplication("https://digital-7a2c5-default-rtdb.firebaseio.com/")

    while True:
        distantia = obtinere_distantia()
        print ("distantia: ", distantia)
        #t_read = threading.Thread(target = read_firebase)
        #t_sensor = threading.Thread(target = ultrasonic_sensor())
        #t_sensor.start()
        #t_read.start()

        pretium = "De custodia"
        #print("[INFO] Conditio: {}".format(valor))
        #db.put("/Configuracion/","Estado", valor)
        
        #---- Inputs et Outputs incipere
        input_manual = GPIO.input(2) #Manual
        input_auto = GPIO.input(22) #Automatic
        input_vacio = GPIO.input(23) #Sequitur inanis
        output_llenado = GPIO.input(25) #Imple
        output_vaciado = GPIO.input(26) #Exinanitio
 
        #distancia = ultrasonic_sensor().obtinere_distantia(distantia)
        minimum = nivel_minimum(distantia)
        maximun = nivel_maximum(distantia)
        print("---------------------------")

        #---------------------------Automatic modus---------------------------
        if (input_auto == False and input_manual == True):

            print("Automatic modus ")
            
            if(minimun == False and maximun == True ):
                #Inanis est
                pretium = "Impletio"
                GPIO.output (25, GPIO.LOW) #Aperit - Repletus - Duxerit volvitur in
                GPIO.output (26, GPIO.HIGH) #Claudit - Inanis - Duxerit non lucet
                print("Se abre valvula llenado")
                print("Llenando")
                #--------------scribe database----------
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= cont+1
                #print("[INFO] Estado: {}".format(valor))
                #db.put("/Configuracion/","Estado", valor)
                scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                
        
            elif(maximun == False and minimun == True ):
                #Plenum est
                pretium = "Exinanitio"
                GPIO.output (25, GPIO.HIGH) #Claudit - Inanis - Duxerit non lucet
                GPIO.output (26, GPIO.LOW) #Aperit - Repletus - Duxerit volvitur in
                print("Exhaurire valvae opens")
                print("Exinanitio")
                #--------------scribe database----------
                now = datetime.datetime.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                cont= cont+1
                #print("[INFO] Conditio: {}".format(pretium))
                #db.put("/Configuracion/","Conditio", pretium)
                scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                
                
        #--------------------------Modus manualis---------------------------
        elif (input_auto == True and input_manual == False):
          
            print("Modus manualis ")
               
            if(minimun == False and maximun == True ):
                print("Lacus inanis, vis imple")
                if(input_vacio == False):
                    #Inanis est
                    pretium = "Impletio"
                    GPIO.output (25, GPIO.LOW) #Aperit - Repletus - Duxerit volvitur in
                    GPIO.output (26, GPIO.HIGH) #Claudit - Inanis - Duxerit non lucet
                    print("Imple valvae opens")
                    time.sleep(5)
                    print("-------------------------------")
                    print("------------Impletio-----------")
                    print(".------------------------------")
                    #--------------scribe database----------
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                else:
                    print("-------------------------------")
                    print("----- Expectans user ----------")
                    print(".------------------------------")
                    #--------------scribe database----------
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                    #print("[INFO] Conditio: {}".format(pretium))
               	    #db.put("/Configuracion/","Conditio", pretium)
                
            elif(maximun == False and minimun == True):
                print("Plena cisternina, vis evacuare")
                if(input_vacio == True):
                    #Plenum est
                    pretium = "Exinanitio"
                    GPIO.output (25, GPIO.HIGH) #Claudit - Inanis - Duxerit non lucet
                    GPIO.output (26, GPIO.LOW) #Aperit - Repletus - Duxerit volvitur in
                    print("Exhaurire valvae opens")
                    time.sleep(5)
                    print("-------------------------------")
                    print("------------Exinanitio-----------")
                    print(".------------------------------")
                    #--------------scribe database----------
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                else:
                    print("-------------------------------")
                    print("------ Expectans user ---------")
                    print(".------------------------------")
                    #--------------scribe database----------
                    now = datetime.datetime.now()
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    cont= cont+1
                    scribere_MYSQL(str(cont),str(date),format(distance,'.2f'),format(distance,'.2f'))
                    #print("[INFO] Conditio: {}".format(valor))
                    #db.put("/Configuracion/","Conditio", valor)

        time.sleep(1)
 
 
    
if __name__ == '__main__':
    main()
