import logging
import numpy as np
from input_reader import llegeix
from integradors import *

class Experiment():
	def __init__(self, fitxer_entrada):
		self.info = llegeix(fitxer_entrada)

Expeiment(fitxer_entrada)