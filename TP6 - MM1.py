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


Time = 0
ServerStatus = Idle
NuminQ = 0
TimeLastEvent = 0
NumCustDelayed = 0
TotalOfDelays = 0
AreaNuminQ = 0
AreaServerStatus = 0

MeanInterarrival = int(input("Ingrese la tasa entre arribos (Clientes/minutos): "))
MeanService = int(input("Ingrese la tasa de servicio (Clientes/minutos): "))

#    temp = np.random.exponential(1/IAT_rate)*60*60

NumEvents = 2
NumDelaysRequired = 40000


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



#Report
AvgDelayInQ = TotalOfDelays / NumCustDelayed
AvgNumInQ = AreaNuminQ / Time
ServerUtilization = AreaServerStatus / Time

Util = MeanInterarrival/MeanService
numeroPromEnColaT = (Util**2)/(1 - Util)
tiempoPromEnColaT = Util/(MeanService*(1-Util))

print("-------------------------------------")
print("Resultados de la simulación:")
print("Tiempo promedio en cola:", round(AvgDelayInQ, 4), " minutos")
print("Número promedio en cola:", round(AvgNumInQ, 4))
print("Utilización del servidor:", round(ServerUtilization, 4))
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
plt.plot(tiempoPromEnCola)

plt.subplot(1, 3, 2)
plt.title('Nº prom. en cola')
plt.ylabel('Clientes')
plt.xlabel('Eventos')
plt.axhline(y=numeroPromEnColaT, color='g', linestyle='--')
plt.plot(numeroPromEnCola)

plt.subplot(1, 3, 3)
plt.title('Utilizacion del SV')
plt.ylabel('Utilización del SV')
plt.xlabel('Eventos')
plt.axhline(y=Util, color='g', linestyle='--')
plt.plot(utilizacionServ)

plt.tight_layout()
plt.show()