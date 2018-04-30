import numpy as np 
from numpy.linalg import norm
import multiprocessing as mp

def una_fila(entrada):
	"""
	Calcula una de les files de la matriu F[i][j]
	entrada: Llista que conté:
	i --> Numero de fila de la matriu
	npart --> Nombre de partícules
	x --> Posicions
	Funció auxiliar per ajudar a la paralelització
	"""
	i, npart, x = entrada
	resu = np.zeros((npart, 3))
	x_act = x[i]
	for j in range(i):
		x_rep = x[j]
		v = x_rep-x_act
		r = norm(v)
		#Versió amb clipping
		#if r < 2.5:
		#resu[j] = 24*(2*np.power(r, -14)-np.power(r, -8))*v
		resu[j] = 24*(2*np.power(r, -14)-np.power(r, -8))*v
	return resu


def pot(i, x, forces):
	resu = 0
	for j in range(x.shape[0]):
		if j != i:
			r = norm(x[i]-x[j])
			resu += norm(forces[i][j])*r/6 - 4*np.power(r,-12)
	return resu

def acceleracions2(x, masses):
	"""
	Funció de forces i acceleracions paralelitzada
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	També retorna l'energia potencial per a comprovacions posteriors
	"""
	npart = x.shape[0]
	res = np.zeros((npart, npart, 3))
	
	with mp.Pool(processes=mp.cpu_count()) as pool:
		(pool.map(una_fila, [[i,npart,x] for i in range(npart)]))
	forces = np.sum(res - np.transpose(res, (1,0,2)), axis = 0)
	potencial = None
	potencial = np.sum([pot(i, x, res) for i in range(npart)])
	return np.multiply(1/(masses.reshape(npart, 1)), forces), potencial

def acceleracions(x, masses):
	"""
	Funció de forces naïve 
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	"""
	npart = x.shape[0]
	forces = np.zeros((npart, npart, 3))
	for i in range(npart):
		x_act = x[i]
		for j in range(i):
			x_rep = x[j]
			v = x_rep-x_act
			r = norm(v)
			forces[i][j] = 24*(2*np.power(r, -13)-np.power(r, -7))*v/r
	forces = np.sum(forces - np.transpose(forces, (1,0,2)), axis = 0)
	return np.multiply(1/(masses.reshape(npart, 1)), forces)

def cinetica(vel, masses):
	"""
	Entrada: 
	vel (velocitat actual): ((npart, 3))
	masses: npart
	"""
	moduls = np.linalg.norm(vel, axis = 1)
	return np.sum(np.multiply(masses,np.power(moduls,2)))