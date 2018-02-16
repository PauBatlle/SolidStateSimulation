import logging
from tqdm import tqdm as t 
import numpy as np
from input_reader import llegeix
from integradors import *
from acc import acceleracions

class parameters():
	def __init__(self, niter = 5000, timestep = 1e-8, sigma = 1, eps = 1):
		self.niter = niter #Nombre d'iteracions
		self.timestep = timestep #Timestep de l'integrador
		self.sigma = sigma #Finite distance in which interpotential = 0
		self.eps = eps #Eps = Depth of the potential well
		self.calcula_altres()

	def calcula_altres(self):
		""" Calcula A, B, r_m """ 
		self.A = 4*self.eps*np.power(self.sigma, 12)
		self.B = 4*self.eps*np.power(self.sigma, 12)
		self.r_m = self.sigma*np.power(2, 1/6) #Distància amb el mínim de potencial

class Experiment():
	def __init__(self, fitxer_entrada, params):
		self.initial = llegeix(fitxer_entrada)
		self.params = params
		itera()

	def itera(self):
		npart = self.initial["npart"]
		masses = self.initial["masses"]
		#Creo una matriu per guardar totes les dades
		All_positions = np.zeros((npart, 3, self.params.niter))
		All_velocities = np.zeros((npart, 3, self.params.niter))
		posicions = self.initial["posicions_inicials"]
		vels = self.initial["velocitats_inicials"]
		logging.info("Starting simulation")
		for step in t(range(self.params.niter)):
			accs = acceleracions(posicions, masses, self.params.A, self.params.B)

Experiment(fitxer_entrada, parameters())