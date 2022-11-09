# Tanque de agua inteligente - IOT
-------------------------------------------------------------------
### Objetivo:
Implementar rutinas de automatización usando computadores de placa reducida y bases de datos no relacionales.
 
### Problema:
Se requiere que usted implemente un programa en un computador de placa reducida para controlar el vaciado y llenado de un tanque de agua en una reconocida industria de la región. Considere las siguientes entradas y salidas:

<p align="center">
  <img src="resources\1.png" width="600" title="hover text">
</p>


### Descripción funcional
Considere el siguiente diagrama:

<p align="center">
  <img src="resources\2.png" width="600" title="hover text">
</p>

El tanque tendrá dos modos de llenado: Automático y Manual. En el caso del llenado automático, la válvula de llenado se activará de acuerdo con valor reportado por el sensor de nivel ultrasónico, de tal manera que si el nivel es inferior al nivel mínimo (en la base de datos) la válvula se activará, y cuando el nivel sea mayor al nivel máximo (en la base de datos), la válvula se cerrará. En el caso del llenado manual, el operador accionará el interruptor de llenado manual (nivel lógico 1), y la válvula de llenado se activará siempre y cuando el nivel sea inferior al nivel mínimo. Para parar el llenado manual, el operador llevará el interruptor de llenado manual a cero lógico. 

Por otro lado, en el caso del vaciado del tanque, el operador podrá activar la válvula de vaciado de dos formas: i) accionando el pulsador de vaciado (nivel lógico 1) y ii) cambiando de cero a uno lógico el campo inicio vaciado en la base de datos. Para cualquiera de los dos mecanismos de vaciado, la válvula únicamente se accionará siempre y cuando el nivel del tanque sea mayor al nivel mínimo.

Notas:
1)	Los interruptores de entrada deberán ser simulados por medio de switches montados en un protoboard
2)	Las válvulas serán simuladas por medio de leds. Recuerde que debe usar una resistencia limitadora para no averiar las salidas de la Raspberry.
3)	El valor reportado por el sensor de nivel deberá ser enviado a la base de datos para que el usuario pueda observarlo en línea.
4)	Se dispondrá de un campo adicional en la base de datos el cual mostrará si el proceso se encuentra en REPOSO, LLENANDO o VACIANDO.

