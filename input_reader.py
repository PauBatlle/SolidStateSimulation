import numpy as np
import logging 

def llegeix(fitxer): 

	""" Llegeix un fitxer d'entrada i 
	retorna un diccionari amb les dades del model

	Elements del diccionari:

	Model: Nom del model
	Npart: Nombre de particules
	Masses: Numpy array de (Npart, 1) amb les masses de les partícules
	posicions_inicials: Numpy array de (Npart,3) amb les posicions inicials
	velocitats_inicials: Numpy array de (Npart,3) amb les velocitats inicials


	"""
	logging.info("Llegint dades d'entrada")
	output = {}
	with open(fitxer) as file:
		text_complert = file.read()
	linies = text_complert.split('\n')[:-1]	
	output["model"] = linies[0]
	output["npart"] = int(linies[1])
	output["masses"] = np.array([float(i) for i in linies[2].split(" ")])
	assert(np.size(output["masses"]) == output["npart"])
	posicions = np.zeros((output["npart"], 3))
	velocitats = np.zeros((output["npart"], 3))

	for n in range(3, 3+output["npart"]):
		posicions[n-3] = np.array([float(i) for i in linies[n].split(" ")])
	
	for n in range(3+output["npart"], 3+2*output["npart"]):
		velocitats[n-3-output["npart"]] =  np.array([float(i) for i in linies[n].split(" ")])

	output["posicions_inicials"] = posicions
	output["velocitats_inicials"] = velocitats

	logging.info("El model " + output["model"] + " s'ha llegit correctament")
	return output

