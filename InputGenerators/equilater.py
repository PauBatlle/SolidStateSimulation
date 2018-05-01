import argparse
import logging
import numpy as np
import random
from math import sqrt
from IPython import embed
## Codi per generar inputs amb distribucio amb equilaters

## Per reproducibilitat
random.seed(23)

## Part per modificar
temperatura = 0 #idea de l'energia inicial que tindra, anar cambiant

for temperatura in np.linspace(0,0,1):
	nom_model = "equilater2_T="+str(temperatura)
	nom_model = "TRIANGULET"
	output = "../InputsExpArino/"+nom_model

	m = 1 #masses
	x_1 = 2 #Origen cordenada x
	y_1 = 2 #Origen cordenada y
	altura = 1 #quantes files/2
	llargada = 2 #quantes columnes
	a = dist = np.power(2,1/6) #distància de separacio
	npart = altura*llargada*2
	posicions = np.zeros((npart, 3))
	comptador = 0
	#mal escrit pero diu on han d'estar les coses
	for alt in range(1,altura+1):
		for llar in range(1,llargada+1):
			posicions[comptador] = np.array([x_1+llar*a, y_1+alt*sqrt(3), 0.0])
			comptador += 1

	for alt in range(1,altura+1):
		for llar in range(1,llargada+1): 
			posicions[comptador] = np.array([x_1+llar*a+a/2, y_1+a*alt*sqrt(3)+a*sqrt(3)/2, 0.0])
			comptador += 1

	#Descomentar si vull que la partícula de més abaix a l'esq estigui al 0,0
	"""
	posicions[:,0] -= min(posicions[:,0])
	posicions[:,1] -= min(posicions[:,1])
	#Un apaño per centar-les una mica
	posicions[:,0] += 0.25
	posicions[:,1] += 0.25
	"""
	#Usar per la distribucio de velocitats en els eixos x i y
	velocitats = np.zeros((npart,3))
	for i in range(npart):
		velocitats[i,0] = np.random.normal(0, sqrt(temperatura/m))
		velocitats[i,1] = np.random.normal(0, sqrt(temperatura/m))

	masses = [m for i in range(npart)]

	#Escriu en un fitxer
	with open(output, "w") as fitxer:
		fitxer.write(nom_model + '\n')
		fitxer.write(str(npart) + '\n')
		for i in range(npart):
			if (i):
				fitxer.write(" ")
			fitxer.write(str(masses[i])) 
		fitxer.write('\n')

		for i in range(npart):
			for j in range(3):
				if (j):
					fitxer.write(" ")
				fitxer.write(str(posicions[i, j]))
			fitxer.write('\n')

		for i in range(npart):
			for j in range(3):
				if (j):
					fitxer.write(" ")
				fitxer.write(str(velocitats[i, j]))
			fitxer.write('\n')
