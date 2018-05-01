import numpy as np 
from numpy.linalg import norm
import multiprocessing as mp

def pot(i, x, forces):
	resu = 0
	for j in range(x.shape[0]):
		if j != i:
			r = norm(x[i]-x[j])
			resu += norm(forces[i,j])*r/6 - 4*np.power(r,-12)
	return resu

def acceleracions(x, masses):
	"""
	Funció de forces naïve 
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	"""
	npart = x.shape[0]
	forces = np.zeros((npart, npart, 3))
	potencials = np.zeros((npart, npart))
	for i in range(npart):
		x_act = x[i]
		for j in range(i):
			x_rep = x[j]
			v = x_rep-x_act
			r = norm(v)
			forces[i,j] = 24*(2*np.power(r, -14)-np.power(r, -8))*v
			potencials[i,j] = 4*(np.power(r,-12)-np.power(r,-6))
	forces = forces - np.transpose(forces, (1,0,2))
	#potencial = np.sum([pot(i, x, forces) for i in range(npart)])
	potencial = np.sum(potencials)
	forces = np.sum(forces, axis = 0)
	return np.multiply(1/(masses.reshape(npart, 1)), forces), potencial

def cinetica(vel, masses):
	"""
	Entrada: 
	vel (velocitat actual): ((npart, 3))
	masses: npart
	"""
	moduls = np.linalg.norm(vel, axis = 1)
	return np.sum(np.multiply(masses*0.5,np.power(moduls,2)))