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

for temperatura in np.linspace(0,200,2):
	nom_model = "equilater50_T="+str(temperatura)
	output = "../InputsExpArino/"+nom_model

	m = 1 #masses
	x_1 = 11.4 #Origen cordenada x
	y_1 = 9 #Origen cordenada y
	z_1 = 9 #Origen coordenada z
	altura = 2 #quantes files/2
	llargada = 5 #quantes columnes
	amplada = 2 #quantes capes/2
	a = dist = np.power(2,1/6) #distància de separacio
	npart = altura*llargada*amplada*4
	posicions = np.zeros((npart, 3))
	comptador = 0
	#Capes A
	for amp in range(0,amplada):
		for alt in range(0,altura):
			for llar in range(0,llargada):
				posicions[comptador] = np.array([x_1+llar*a, y_1+alt*a*sqrt(3), z_1+amp*a*2*sqrt(6)/3])
				comptador += 1

		for alt in range(0,altura):
			for llar in range(0,llargada): 
				posicions[comptador] = np.array([x_1+llar*a+a/2, y_1+a*alt*sqrt(3)+a*sqrt(3)/2, z_1+amp*a*2*sqrt(6)/3])
				comptador += 1

	#Capes B
	for amp in range(0,amplada):
		for alt in range(0,altura):
			for llar in range(0,llargada):
				posicions[comptador] = np.array([x_1+llar*a+a/2, y_1+alt*a*sqrt(3)+a*sqrt(3)/6, z_1+amp*a*2*sqrt(6)/3+a*sqrt(6)/3])
				comptador += 1

		for alt in range(0,altura):
			for llar in range(0,llargada): 
				posicions[comptador] = np.array([x_1+llar*a+a, y_1+a*alt*sqrt(3)+a*sqrt(3)/6+a*sqrt(3)/2, z_1+amp*a*2*sqrt(6)/3+a*sqrt(6)/3])
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
