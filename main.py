import logging
import argparse
import os
from tqdm import tqdm as t 
import numpy as np
from input_reader import llegeix
import integradors
from acc import acceleracions2
from IPython import embed
import matplotlib.animation as animation
import matplotlib.pyplot as plt

class parameters():
	def __init__(self, niter, timestep, sigma, eps, integrador, save):
		self.niter = niter #Nombre d'iteracions
		self.timestep = timestep #Timestep de l'integrador
		self.sigma = sigma #Finite distance in which interpotential = 0
		self.eps = eps #Eps = Depth of the potential well
		self.integrador = integrador
		self.save = save #Si guardem tots els valors o no. NO recomanable si npart >> 100 i/o timestep >> 1000

	def __str__(self):
		s = ""
		s = s + "_Sig_" + str(round(self.sigma, 4))
		s = s + "_Eps_" + str(round(self.eps, 4))
		s = s + "_Niter_" + str(self.niter)
		s = s + "_tstep_" + str(self.timestep)
		s = s + "_Integr_" + self.integrador
		return s

class Experiment():
	def __init__(self, fitxer_entrada, params):
		self.initial = llegeix(fitxer_entrada)
		self.params = params
		self.unique_str = self.initial["model"]+str(self.params)
		if not self.done_before():
			self.itera()
			if self.params.save:
				self.save()
				self.postprocessa()


		#os.system("rm "+"-r "+self.directory) #S'ha de borrar això després, és temporal!!
	
	def done_before(self):
		"""
		Miro si ja he fet abans aquest experiment.
		"""
		logging.info("Comprovant si ja s'ha calculat la simulació")
		self.directory = "Resultats/"+self.unique_str
		if not os.path.exists(self.directory):
			if self.params.save:
				os.makedirs(self.directory)
				logging.info("No s'ha calculat, creant directori per guardar els resultats")
				return False
			else:
				logging.info("No s'ha calculat, però no es guardaran els resultats")
				return False
		logging.info("Simulació ja calculada, acabant execució" + self.directory)
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
			acc_act = acceleracions2(pos_act, masses)
			self.accelerations[:,:,step] = acc_act
			pos_act, vel_act = integrador(pos_act, pos_ant, vel_act, acc_act, timestep, limit_contorn) 
		logging.info("")
	
	def postprocessa(self):
		logging.info("Simulació acabada correctament, processant resultats")		
		#Energies potencial i cinètica
		
		#Trajectòries
		
		#Video
		if self.params.save:
			logging.info("Preparant el video")
			pos = self.positions
			skip = 10
			stop = self.params.niter
			npart = self.initial["npart"]
			colors = np.linspace(0, 1, npart)
			def _update_plot(i, fig, scat):
	   			scat.set_offsets(tuple([[pos[j,0,skip*i], pos[j,1,skip*i]] for j in range(npart)]))
	   			return scat

			fig = plt.figure()
			x = pos[:,0,0]
			y = pos[:,1,0]
			ax = fig.add_subplot(111)
			#ax.set_xlim([np.min(pos[:,0,:]),np.max(pos[:,0,:])])
			#ax.set_ylim([np.min(pos[:,1,:]),np.max(pos[:,1,:])])
			ax.set_xlim([max(-25, np.min(pos[:,0,:])), min(25, np.max(pos[:,0,:]))])
			ax.set_ylim([max(-25, np.min(pos[:,1,:])), min(25, np.max(pos[:,1,:]))])

			scat = plt.scatter(x, y, s = 5, c = colors, cmap = "gist_rainbow")
			anim = animation.FuncAnimation(fig, _update_plot, fargs = (fig, scat), frames = int(stop/skip)-1, interval = 10)
			anim.save(self.directory+"/"+'video.mp4', writer="ffmpeg")
			#WIP

	def save(self):
		logging.info("Guardant els resultats")
		np.save(self.directory+"/positions", self.positions)
		np.save(self.directory+"/velocities", self.velocities)
		np.save(self.directory+"/accelerations", self.accelerations)

### Paràmetres Default
niter = 5000
timestep = 1e-7
sigma = 1
eps = 1
integrador = "Euler"
limit_contorn = 100
save = False

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
parser.add_argument("--save")
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
if args_parsed.save is not None:
	save = bool(args_parsed.save)

if args_parsed.integrador is not None:
	if args_parsed.integrador in integradors_suportats:
		integrador = args_parsed.integrador
	else:
		raise Exception("Integrador desconegut")



logging.basicConfig(format='%(asctime)s %(module)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Començant Experiment")
exp = Experiment(args_parsed.input, parameters(niter = niter, timestep = timestep, sigma = sigma, eps = eps, integrador = integrador, save = save))
