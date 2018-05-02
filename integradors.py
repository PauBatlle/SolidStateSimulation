import numpy as np
from acc import acceleracions
import logging

"""
Fitxer d'integradors: Un integrador ha d'agafar
--> Posicions(t): Np array de (npart,3)
--> Velocitats(t): Np array de (npart,3)
--> Acceleracions(t): Np array de (npart,3) (Que prové de crida la funcio de forces)
--> Timestep

I ha de retornar, AMB AQUEST ORDRE:
--> Posicions(t+1): Una nova np array de (npart, 3)
--> Velocitats(t+1): Una nova np array de (npart, 3)
És a dir, únicament ha de fer UN step (el for es fa des del codi principal)

En els mètodes més elaborats s'ha de cridar a la funció acceleracions de acc.py
"""

#Mètode d'Euler: y' = f(y) --> y(t+1) = y(t) + h*f(y(t))

def Euler(x_t, x_t_1, vel_t, acc_t, timestep, limits, step):

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
	new_x = vel_t*timestep + x_t
	new_v = acc_t*timestep + vel_t
	
	# I ara condicions de contorn
	new_v = new_v*np.sign(new_x)*np.sign(limits-new_x)
	new_x = np.absolute(new_x)
	new_x = np.minimum(2*limits-new_x, new_x)
	return new_x, new_v

"""
def Runge_Kutta(x_t, x_t_1,vel_t, acc_t, timestep):
	
	raise Exception("Mètode no implementat encara")
	new_v = np.zeros((npart, 3))
	new_x = np.zeros((npart, 3))
	#[...]
	return new_x, new_v
"""

def Verlet(x_t, x_t_1, vel_t, acc_t, timestep, limits, step):

	if step == 0:
		new_x = x_t + vel_t*timestep+0.5*acc_t*timestep*timestep

	if step != 0:
		new_x = 2*x_t-x_t_1+acc_t*np.power(timestep,2)
		
	""" I ara condicions de contorn"""
	new_xp = 2*x_t-new_x
	new_x = np.maximum(new_x, -new_xp*np.sign(x_t))
	#faig una reflexio per fer-ho mes facil d'entendre
	x_tr = limits-x_t
	new_xr = limits-new_x
	new_xpr = limits-new_xp
	#i repeteixo
	new_xr = np.maximum(new_xr, -new_xpr*np.sign(x_tr))
	new_x = limits-new_xr
	
	if step == 0:
		new_v = vel_t
	if step == 1:
		new_v = (x_t-x_t_1)/timestep
	return new_x, new_v


#Auxiliar: no tocar
def string2func(s):
	if (s == "Euler"):
		return Euler
	if (s == "Verlet"):
		return Verlet