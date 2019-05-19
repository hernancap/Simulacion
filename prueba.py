import random
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import chi2

k = 12
array = [29, 24, 22, 19, 21, 18, 19, 20, 23, 18, 20, 23]
cont = 0
n = 256
nivelConf = 0.95


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