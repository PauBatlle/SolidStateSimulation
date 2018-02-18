import logging
import argparse
from tqdm import tqdm as t 
import numpy as np
from input_reader import llegeix
import integradors
from acc import acceleracions
from IPython import embed

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

class Experiment():
	def __init__(self, fitxer_entrada, params):
		self.initial = llegeix(fitxer_entrada)
		self.params = params
		self.itera()
		self.postprocessa()

	def itera(self):
		npart = self.initial["npart"]
		masses = self.initial["masses"]
		#Creo una matriu per guardar totes les dades
		self.positions = np.zeros((npart, 3, self.params.niter))
		self.velocities = np.zeros((npart, 3, self.params.niter))
		self.accelerations = np.zeros((npart, 3, self.params.niter))
		pos_act = self.initial["posicions_inicials"]
		vel_act = self.initial["velocitats_inicials"]
		integrador = integradors.string2func(self.params.integrador) #De moment!
		logging.info("Començant simulació, " + str(self.params.niter) + " iteracions, timestep = " + str(self.params.timestep))
		for step in t(range(self.params.niter)):
			pos_ant = self.positions[:,:,step-1]
			self.positions[:,:,step] = pos_act
			self.velocities[:,:,step] = vel_act
			acc_act = acceleracions(pos_act, masses, self.params.A, self.params.B)
			self.accelerations[:,:,step] = acc_act
			pos_act, vel_act = integrador(pos_act, pos_ant, vel_act, acc_act, timestep)
	
	def postprocessa(self):
		logging.info("Simulació acabada correctament, processant resultats")		
		#Energies potencial i cinètica
		#Trajectòries
		#
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
Experiment(args_parsed.input, parameters(niter = niter, timestep = timestep, sigma = sigma, eps = eps, integrador = integrador))