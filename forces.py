import numpy as np 
from numpy.linalg import norm
from time import time
import numpy.random as rnd
import multiprocessing as mp 
from itertools import repeat

def forces1(x):
	"""
	Funció de forces naïve 
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	"""
	eps = 1e-13
	npart = x.shape[0]
	forces = np.zeros((npart, npart, 3))
	for i in range(npart):
		x_act = x[i]
		for j in range(i):
			x_rep = x[j]
			v = x_rep-x_act
			r = norm(v)
			forces[i][j] = 24*(2*np.power(r, -13)-np.power(r, -7))*v/r
	for j in range(npart):
		for i in range(j):
			forces[i][j] = -forces[j][i]
	return np.sum(forces, axis = 0)



def una_fila(inpu):
	i, npart, x = inpu
	resu = np.zeros((npart, 3))
	x_act = x[i]
	for j in range(i):
		x_rep = x[j]
		v = x_rep-x_act
		r = norm(v)
		if r < 2.5:
			resu[j] = 24*(2*np.power(r, -14)-np.power(r, -8))*v
	return resu

def forces2(x):
	"""
	Funció de forces naïve paralelitzada 
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	"""
	npart = x.shape[0]
	res = np.zeros((npart, npart, 3))
	pool = mp.Pool(processes=mp.cpu_count())
	res = pool.map(forssa, [[i,npart,x] for i in range(npart)])
	for j in range(npart):
		for i in range(j):
			res[i][j] = -res[j][i]

	return np.sum(res, axis = 0)

def forces3(x):
	"""
	Funció de forces paralelitzada 
	X: les posicions de totes les particules en t (npart, 3)
	Retorna les acceleracions de cada particula en t (npart, 3)
	"""
	npart = x.shape[0]
	res = np.zeros((npart, npart, 3))
	pool = mp.Pool(processes=mp.cpu_count())
	tempsinicial = time()
	res = np.array(pool.map(una_fila, [[i,npart,x] for i in range(npart)]))
	t2 = time()
	print(t2-tempsinicial)
	res =  np.sum(res - np.transpose(res, (1,0,2)), axis = 0)
	print(time()-t2)
	return res


sample = np.array([[1,0,0],[0,1,0], [0,0,1]])
def fes_testos(funcio):
	print(funcio)
	print("Test Cases")
	assert(funcio(np.array([[0,0,0],[1,0,0]])).shape == (2,3))
	assert(funcio(np.array([[0,0,1],[1,1,1],[0,0,0],[1,0,0]])).shape == (4,3))
	assert(np.all(np.isclose(funcio(np.array([[0,0,0],[1,0,0]])), np.array([[-24,0,0],[24,0,0]]))))
	modulus = 24*(np.power(2, -11/2)-np.power(2, -7/2))
	x1 = modulus*1/np.sqrt(2)*np.array([2,-1,-1])
	x2 = modulus*1/np.sqrt(2)*np.array([-1,2,-1])
	x3 = modulus*1/np.sqrt(2)*np.array([-1,-1,2])
	resultat = np.array([x1,x2,x3])
	assert(np.all(np.isclose(funcio(np.array([[1,0,0],[0,1,0], [0,0,1]])), resultat)))
	print("Temps")
	t0 = time()
	funcio(entrada)
	tf = time()-t0
	print(tf)

rnd.seed(23)
funcions = [forces3]
for i in funcions:
	entrada = 20*rnd.random((10000,3))
	i(entrada)
	#fes_testos(i)

