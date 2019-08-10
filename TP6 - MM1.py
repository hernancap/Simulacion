import numpy as np
import random
import matplotlib.pyplot as plt
import math

def exponencial(mean):
    u = random.random()
    return ((-1/mean) * math.log(u))


Busy = 1
Idle = 0

TimeArrival = []
TimeNextEvent = []
tiempoPromEnCola = []
numeroPromEnCola = []
utilizacionServ = []

tiempoPromEnColaC = []
numeroPromEnColaC = []
utilizacionServC = []

sumAvgDelayInQ = 0
sumAvgNumInQ = 0
sumUtilizacionServ = 0

while True:

    MeanInterarrival = int(input("Ingrese la tasa entre arribos (Clientes/minutos): "))
    MeanService = int(input("Ingrese la tasa de servicio (Clientes/minutos): "))

    if MeanInterarrival >= MeanService:
        print("La cola tiende a infinito si la tasa entre arribos es igual o mayor que la tasa de servicio")
    else:
        break



NumEvents = 2
NumDelaysRequired = 25000
numSimul = 500

#Valores teóricos
Util = MeanInterarrival/MeanService
numeroPromEnColaT = (Util**2)/(1 - Util)
tiempoPromEnColaT = Util/(MeanService*(1-Util))

for c in range(numSimul):

    TimeArrival.clear()
    TimeNextEvent.clear()
    tiempoPromEnCola.clear()
    numeroPromEnCola.clear()
    utilizacionServ.clear()

    Time = 0
    ServerStatus = Idle
    NuminQ = 0
    TimeLastEvent = 0
    NumCustDelayed = 0
    TotalOfDelays = 0
    AreaNuminQ = 0
    AreaServerStatus = 0

    TimeNextEvent.append(Time + exponencial(MeanInterarrival))
    TimeNextEvent.append(10**30)

    #print("Tiempo prox 0: ", TimeNextEvent[0])
    #print("Tiempo prox 1: ", TimeNextEvent[1])
    #print("-------------------------------")



    for j in range(NumDelaysRequired):

        #Timing

        if TimeNextEvent[0] < TimeNextEvent[1]:
            Time = TimeNextEvent[0]
            NextEventType = 0
        else:
            Time = TimeNextEvent[1]
            NextEventType = 1

        #print("Tiempo prox 0: ", TimeNextEvent[0])
        #print("Tiempo prox 1: ", TimeNextEvent[1])
        #print("Tiempo: ", Time)
        #print("-------------------------------")

        #Timing ended

        #UpdateTimeAvgStats

        TimeSinceLastEvent = Time - TimeLastEvent
        TimeLastEvent = Time
        AreaNuminQ = AreaNuminQ + NuminQ * TimeSinceLastEvent
        AreaServerStatus = AreaServerStatus + ServerStatus * TimeSinceLastEvent

        #UpdateTimeAvgStats ended

        if NextEventType == 0:
            #Arrive

            TimeNextEvent[0] = Time + exponencial(MeanInterarrival)

            if ServerStatus == Busy:

                NuminQ = NuminQ + 1
                TimeArrival.append(Time)

            else: 
                Delay = 0
                TotalOfDelays = TotalOfDelays + Delay
                NumCustDelayed = NumCustDelayed + 1
                ServerStatus = Busy
                TimeNextEvent[1] = Time + exponencial(MeanService)

            #Arrive ended
        else:
            #Depart

            if NuminQ == 0:

                ServerStatus = Idle
                TimeNextEvent[1] = 10**30

            else:
                NuminQ = NuminQ - 1
                Delay = Time - TimeArrival[0]
                TotalOfDelays = TotalOfDelays + Delay
                NumCustDelayed = NumCustDelayed + 1
                TimeNextEvent[1] = Time + exponencial(MeanService)
                for k in range(NuminQ):
                    TimeArrival[k] = TimeArrival[k + 1]
                TimeArrival.pop(len(TimeArrival) - 1)

            #Depart ended
        
        AvgDelayInQ = TotalOfDelays / NumCustDelayed
        AvgNumInQ = AreaNuminQ / Time
        ServerUtilization = AreaServerStatus / Time

        tiempoPromEnCola.append(AvgDelayInQ)
        numeroPromEnCola.append(AvgNumInQ)
        utilizacionServ.append(ServerUtilization)

    #Arrays de corridas
    sumAvgDelayInQ = sumAvgDelayInQ + AvgDelayInQ
    sumAvgNumInQ = sumAvgNumInQ + AvgNumInQ
    sumUtilizacionServ = sumUtilizacionServ + ServerUtilization

    tiempoPromEnColaC.append(sumAvgDelayInQ/(c+1))
    numeroPromEnColaC.append(sumAvgNumInQ/(c+1))
    utilizacionServC.append(sumUtilizacionServ/(c+1))


#Report
print("-------------------------------------")
print("Resultados de la última simulación:")
print("Tiempo promedio en cola:", round(AvgDelayInQ, 4), " minutos")
print("Número promedio en cola:", round(AvgNumInQ, 4))
print("Utilización del servidor:", round(ServerUtilization, 4))
print("-------------------------------------")
print("Resultados del total de simulaciones:")
print("Tiempo promedio en cola:", round(tiempoPromEnColaC[numSimul-1], 4), " minutos")
print("Número promedio en cola:", round(numeroPromEnColaC[numSimul-1], 4))
print("Utilización del servidor:", round(utilizacionServC[numSimul-1], 4))
print("-------------------------------------")
print("Resultados teóricos:")
print("Tiempo promedio en cola: (Teórico)", round(tiempoPromEnColaT, 4), " minutos")
print("Número promedio en cola: (Teórico)", round(numeroPromEnColaT, 4))
print("Utilización del servidor: (Teórico)", round(Util, 4))

#Report ended

plt.subplot(1, 3, 1)
plt.title('Tiempo prom. en cola')
plt.ylabel('Minutos')
plt.xlabel('Eventos')
plt.axhline(y=tiempoPromEnColaT, color='g', linestyle='--')
plt.ylim(tiempoPromEnColaT*0.001, tiempoPromEnColaT*2)
plt.plot(tiempoPromEnCola)

plt.subplot(1, 3, 2)
plt.title('Nº prom. en cola')
plt.ylabel('Clientes')
plt.xlabel('Eventos')
plt.axhline(y=numeroPromEnColaT, color='g', linestyle='--')
plt.ylim(numeroPromEnColaT*0.001, numeroPromEnColaT*2)
plt.plot(numeroPromEnCola)

plt.subplot(1, 3, 3)
plt.title('Utilizacion del SV')
plt.ylabel('Utilización del SV')
plt.xlabel('Eventos')
plt.axhline(y=Util, color='g', linestyle='--')
plt.plot(utilizacionServ)

plt.suptitle('Última simulación') 
plt.tight_layout()
plt.show()

plt.subplot(1, 3, 1)
plt.title('Tiempo prom. en cola')
plt.ylabel('Minutos')
plt.xlabel('Eventos')
plt.axhline(y=tiempoPromEnColaT, color='g', linestyle='--')
plt.plot(tiempoPromEnColaC)

plt.subplot(1, 3, 2)
plt.title('Nº prom. en cola')
plt.ylabel('Clientes')
plt.xlabel('Eventos')
plt.axhline(y=numeroPromEnColaT, color='g', linestyle='--')
plt.plot(numeroPromEnColaC)

plt.subplot(1, 3, 3)
plt.title('Utilizacion del SV')
plt.ylabel('Utilización del SV')
plt.xlabel('Eventos')
plt.axhline(y=Util, color='g', linestyle='--')
plt.plot(utilizacionServC)

plt.suptitle('Promedio del total de simulaciones') 
plt.tight_layout()
plt.show()
