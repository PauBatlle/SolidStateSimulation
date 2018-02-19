import numpy as np
from acc import acceleracions
import logging

"""
joan midif
Fitxer d'integradors: Un integrador ha d'agafar
--> Posicions(t): Np array de (npart,3)
--> Velocitats(t): Np array de (npart,3)
--> Acceleracions(t): Np array de (npart,3) (Que prové de crida la funcio de forces)
(En alguns casos, també posicions de t-1)
I ha de retornar, AMB AQUEST ORDRE: gnornfope
--> Posicions(t+1): Una nova np array de (npart, 3)
--> Velocitats(t+1): Una nova np array de (npart, 3)
És a dir, únicament ha de fer UN step (el for es fa des del codi principal)
"""

#Mètode d'Euler: y' = f(y) --> y(t+1) = y(t) + h*f(y(t))

def Euler(x_t, x_t_menys_h, vel_t, acc_t, timestep):
	""" Versió ineficient, però llegible """
	"""
	npart = x_t.shape[0]
	new_v = np.zeros((npart, 3))
	new_x = np.zeros((npart, 3))
	for part in range(npart):
		new_v[part, :] = acc_t[part, :]*timestep + vel_t[part, :]
		new_x[part, :] = vel_t[part, :]*timestep + x_t[part, :]
	"""

	""" Versió vectoritzada """
	return vel_t*timestep + x_t, acc_t*timestep + vel_t

def Runge_Kutta(x_t, x_t_menys_h, vel_t, acc_t, timestep):
	
	raise Exception("Mètode no implementat encara")
	new_v = np.zeros((npart, 3))
	new_x = np.zeros((npart, 3))
	#[...]
	return new_x, new_v
	

def Verlet(x_t, x_t_menys_h, vel_t, acc_t, timestep):
	
	raise Exception("Mètode no implementat encara")
	new_v = np.zeros((npart, 3))
	new_x = np.zeros((npart, 3))
	#[...]
	return new_x, new_v


#Auxiliar: no tocar
def string2func(s):
	if (s == "Euler"):
		return Euler
	if (s == "Runge_Kutta"):
		return Runge_Kutta
	if (s == "Verlet"):
		return Verlet