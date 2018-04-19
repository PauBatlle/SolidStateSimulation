import argparse
import logging
import numpy as np
import random
from random import uniform as rnd
## Codi per generar inputs llegibles, a partir d'uns certs paràmetres d'entrada

## Per reproducibilitat
random.seed(23)

## Part per modificar

npart = 2 #Nombre de partícules
xini = 4 #Distància inicial entre partícules en l'eix x
bmax = 3 #Patàmetre d'impacte màxim
bnum = 16 #Mida de la partició uniforme dels valors del 
			#paràmetre d'impacte que provem
vmod = 1 #Mòdul de la velocitat a l'inici


b = np.linspace(0,bmax, bnum)

for k in range(bnum):
	nom_model = "XocSimetric"+str(k)
	output = "../InputsExpAdam/"+nom_model


	## No tocar a partir d'aquí

	posA = np.array([-xini/2, b[k]/2, 0.0], dtype = float)
	posB = -posA

	velA = vmod*np.array([1.0, 0.0, 0.0])
	velB = -velA

	posicions = np.array([posA,posB])
	velocitats = np.array([velA,velB])

	masses = [1 for i in range(npart)]

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
