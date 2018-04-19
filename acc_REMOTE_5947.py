import numpy as np 
from numpy.linalg import norm

def acceleracions(x, masses, A = 1, B = 1):#sugerencia: masses = columna de 1ns o similar, ¿1 sol parametre?
	""" 
	Funció d'acceleracions 
	X: les posicions de totes les partícules  en t (npart, 3)
	Retorna l'acceleracio de cada particula en t, usant Newton (npart, 3)
	"""
	eps = 1e-10
	npart = x.shape[0]
	forces = np.zeros((npart, npart, 3)) #Creo una matriu on M(i,j) = Força i --> j
	for i in range(npart):
		x_actua = x[i]
		for j in range(i):
			x_rep = x[j]
			vec = x_rep-x_actua
			força = (A/(np.power(norm(vec), 13)+eps) + B/(np.power(norm(vec), 7)+eps))*vec
			forces[i][j] = força

	for j in range(npart):  #3a llei de newton
		for i in range(j):
			forces[i][j] = -forces[j][i]

	forces = np.sum(forces, axis=0) #Sumem per columnes
	return np.multiply(1/(masses.reshape(npart, 1)), forces)

