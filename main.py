import logging
import argparse
import os
from tqdm import tqdm as t 
import numpy as np
from input_reader import llegeix
import integradors
from acc import acceleracions
from IPython import embed

from sys import exit as rop

class parameters():
	def __init__(self, niter, timestep, sigma, eps, integrador):
		self.niter = niter #Nombre d'iteracions
		self.timestep = timestep #Timestep de l'integrador
		self.sigma = sigma #Finite distance in which interpotential = 0
		self.eps = eps #Eps = Depth of the potential well
		self.integrador = integrador
		self.calcula_altres()

	def calcula_altres(self):
		""" Calcula A, B, r_m """ 
		self.A = 4*self.eps*np.power(self.sigma, 12)
		self.B = 4*self.eps*np.power(self.sigma, 12)
		self.r_m = self.sigma*np.power(2, 1/6) #Distància amb el mínim de potencial

	def __str__(self):
		s = ""
		s = s + "-Sig:" + str(round(self.sigma, 4))
		s = s + "-Eps:" + str(round(self.eps, 4))
		s = s + "-Niter:" + str(self.niter)
		s = s + "-logtstep:" + str(round(np.log10(self.timestep), 4))
		s = s + "-Integr:" + self.integrador
		return s

class Experiment():
	def __init__(self, fitxer_entrada, params):
		self.initial = llegeix(fitxer_entrada)
		self.params = params
		self.unique_str = self.initial["model"]+str(self.params)
		if not self.done_before():
			self.itera()
			self.postprocessa()
			self.save()
		#os.system("rm "+"-r "+self.directory) #S'ha de borrar això després, és temporal!!
	def done_before(self):
		"""
		Miro si ja he fet abans aquest experiment.
		"""
		logging.info("Comprovant si ja s'ha calculat la simulació")
		self.directory = "Resultats/"+self.unique_str
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
			logging.info("No s'ha calculat, creant directori per guardar els resultats")
			return False
		logging.info("Simulació ja calculada, " + self.directory)
		return True
		


	def itera(self):
		npart = self.initial["npart"]
		masses = self.initial["masses"]
		#Creo una matriu per guardar totes les dades
		self.positions = np.zeros((npart, 3, self.params.niter))
		self.velocities = np.zeros((npart, 3, self.params.niter))
		self.accelerations = np.zeros((npart, 3, self.params.niter))
		pos_act = self.initial["posicions_inicials"]
		vel_act = self.initial["velocitats_inicials"]
		integrador = integradors.string2func(self.params.integrador)
		logging.info("Començant simulació, " + str(self.params.niter) + " iteracions, timestep = " + str(self.params.timestep))
		for step in t(range(self.params.niter)):
			pos_ant = self.positions[:,:,step-1]
			self.positions[:,:,step] = pos_act
			self.velocities[:,:,step] = vel_act
			acc_act = acceleracions(pos_act, masses, self.params.A, self.params.B)
			self.accelerations[:,:,step] = acc_act
			pos_act, vel_act = integrador(pos_act, vel_act, acc_act, timestep)
		logging.info("")
	def postprocessa(self):
		logging.info("Simulació acabada correctament, processant resultats")		
		#Energies potencial i cinètica
		
		#Trajectòries
		
		#Video
		#WIP
		pass

	def save(self):
		logging.info("Guardant els resultats")
		np.save(self.directory+"/positions", self.positions)
		np.save(self.directory+"/velocities", self.velocities)
		np.save(self.directory+"/accelerations", self.accelerations)
		pass

### Paràmetres Default
niter = 5000
timestep = 1e-7
sigma = 1
eps = 1
integrador = "Euler"

### Integradors suportats
integradors_suportats = ["Euler", "Runge_Kutta", "Verlet"]
##Llegeix parametres d'entrada
parser = argparse.ArgumentParser()
parser.add_argument("--input", required = True)
parser.add_argument("--niter")
parser.add_argument("--timestep")
parser.add_argument("--sigma")
parser.add_argument("--eps")
parser.add_argument("--integrador")
	#Si he entrat algun valor, sobreescriure
args_parsed = parser.parse_args()
if args_parsed.niter is not None:
	niter = int(args_parsed.niter)
if args_parsed.timestep is not None:
	timestep = float(args_parsed.timestep)
if args_parsed.sigma is not None:
	sigma = float(args_parsed.sigma)
if args_parsed.eps is not None:
	eps = float(args_parsed.eps)

if args_parsed.integrador is not None:
	if args_parsed.integrador in integradors_suportats:
		integrador = args_parsed.integrador
	else:
		raise Exception("Integrador desconegut")



logging.basicConfig(format='%(asctime)s %(module)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Començant Experiment")
exp = Experiment(args_parsed.input, parameters(niter = niter, timestep = timestep, sigma = sigma, eps = eps, integrador = integrador))
