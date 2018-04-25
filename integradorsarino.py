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

def Euler(x_t, x_t_1, vel_t, masses, timestep):

    acc_t = acceleracions(x_t, masses)
	return vel_t*timestep + x_t, acc_t*timestep + vel_t

def Runge_Kutta(x_t, x_t_1, vel_t, acc_t, timestep):
	
    raise Exception("Mètode no implementat encara")
    #crida a Runge Kutta, RK4 necessita calcular acceleracions, ¿problema amb masses?, totes iguals per defecte 
	return 2*x_t-x_t_1+acc_t*np.power(timestep,2), acc_t*timestep + vel_t
	

def Verlet(x_t, x_t_1, vel_t, masses, timestep):
	acc_t = acceleracions(x_t, masses)
	return 2*x_t-x_t_1+acc_t*np.power(timestep,2), acc_t*timestep + vel_t


#Auxiliar: no tocar
def string2func(s):
	if (s == "Euler"):
		return Euler
	if (s == "Runge_Kutta"):
		return Runge_Kutta
	if (s == "Verlet"):
		return Verlet