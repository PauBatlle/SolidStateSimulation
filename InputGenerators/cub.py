import numpy as np
import random
from math import sqrt
from IPython import embed
## Codi per generar inputs amb distribucio en quadricula

## Per reproducibilitat
random.seed(23)

## Part per modificar
temperatures = [0.11, 0.22,0.33, 0.44]#idea de l'energia inicial que tindra, anar cambiant

for temperatura in temperatures:
	nom_model = "cub3_T="+str(temperatura)
	output = "../InputsGenerats/"+nom_model

	m = 1 #masses
	x_1 = 3 #Origen cordenada x
	y_1 = 3 #Origen cordenada y
	z_1 = 3
	altura = 3 #
	a = dist = np.power(2,1/6) #distància de separacio
	npart = altura**3
	posicions = np.zeros((npart, 3))
	comptador = 0
	#mal escrit pero diu on han d'estar les coses
	for alt in range(altura):
		for llar in range(altura):
			for prof in range(altura):
				posicions[comptador] = np.array([x_1+a*alt,y_1+a*llar, z_1+a*prof])
				comptador+=1

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
		velocitats[i,2] = np.random.normal(0, sqrt(temperatura/m))

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

#WIP