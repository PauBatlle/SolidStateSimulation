import argparse
import logging
import numpy as np
import random
from random import uniform as rnd
## Codi per generar inputs llegibles, a partir d'uns certs paràmetres d'entrada

## Per reproducibilitat
random.seed(23)

## Part per modificar

npart = 10 #Nombre de partícules
xmax = 3 #Les x inicials estaran uniformes entre [xmin, xmax]
xmin = -xmax
ymax = 3 #Les y inicials estaran uniformes entre [ymin, ymax]
ymin = -ymax
zmax = 3 #Les z inicials estaran uniformes entre [zmin, zmax]
zmin = -zmax
vxmax = 3 #Les vx inicials estaran uniformes entre [vxmin, vxmax]
vxmin = -vxmax
vymax = 3 #Les vy inicials estaran uniformes entre [vymin, vtmax]
vymin = -vymax
vzmax = 3 #Les vz inicials estaran uniformes entre [vzmin, vzmax]
vzmin = -vzmax
massmax = 1 #Les masses estaran uniformes entre [massmin, massmax]
massmin = 0

nom_model = "Exemple2"
output = "../InputsGenerats/"+nom_model

## No tocar a partir d'aquí

aux_vec = [xmax, ymax, zmax]
aux_vec_m = [xmin, ymin, zmin]

aux_vec_v = [vxmax, vymax, vzmax]
aux_vec_vm = [vxmin, vymin, vzmin]

posicions = np.zeros((npart, 3))
velocitats = np.zeros((npart, 3))

for i in range(3):
	posicions[:,i] = np.array([rnd(aux_vec_m[i], aux_vec[i]) for j in range(npart)])
	velocitats[:,i] = np.array([rnd(aux_vec_vm[i], aux_vec_v[i]) for j in range(npart)])

masses = [rnd(massmin, massmax) for i in range(npart)]

#Llegeix en un fitxer
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
