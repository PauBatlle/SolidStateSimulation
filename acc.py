import numpy as np 
from np.linalg import norm

def acceleracions(x, masses, A = 1, B = 1):
	""" Funció d'acceleracions 
	Agafa les posicions de totes les partículesm en t (npart, 3)
	Retorna l'acceleracio de cada particula en t, usant Newton (npart, 3)
	"""
	npart = x.shape[0]
	"""S'ha de fer una versió més xetada usant 3a llei de Newton, no cal fer tants calculs """
	forces = np.zeros((npart, 3))
	for part_rep in range(npart):
		x_rep = x[part_rep]
		força_part_rep = np.zeros(3)
		for part_actua in range(npart):
			x_actua = x[part_actua]
			vec = x_rep-x_actua
			força = (A/np.pow(norm(vec), 13) + B/np.pow(norm(vec), 7))*vec
			força_part_rep += força

		forces[part_rep] = força_part_rep
	return np.multiply(1/masses, forces)



