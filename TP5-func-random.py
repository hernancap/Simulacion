import random
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import chi2

k = 30
array = []
cont = 0
n = 10000
nivelConf = 0.95

subinterv = 1/k
for z in range(k):
	array.append(0)
for x in range(n):
	r = random.random()
	for y in range(k):
		cont = cont + subinterv
		if(r<=cont):
			array[y] = array[y] + 1
			break
	cont = 0
print(array, sep=", ")

varChi2 = 0
valEsp = n/k
for z in range(k):
	varChi2 = varChi2 + (((array[z] - valEsp)**2) / valEsp)

print(varChi2)

chi2Tabla = chi2.isf(1 - nivelConf, k - 1)
print(chi2Tabla)

if(varChi2 > chi2Tabla):
	print("Se rechaza la hipótesis nula (H0)")
else: print("No se rechaza la hipótesis nula (H0)")


x = np.arange(k)

plt.title('Histograma')
plt.bar(x, array)
plt.xlim(-1, k)


plt.tight_layout()
plt.show()