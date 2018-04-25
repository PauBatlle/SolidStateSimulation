import argparse
import logging
import numpy as np
import random
from random import uniform as rnd
## Codi per generar inputs amb distribucio amb equilaters

## Per reproducibilitat
random.seed(23)

## Part per modificar
temperatura = 8 #idea de l'energia inicial que tindra, anar cambiant
m = 7 #masses
x_1 = 5 #Origen cordenada x
y_1 = 5 #Origen cordenada y
altura = 10 #quantes files/2
llargada = 8 #quantes columnes
dist = 1 #distància de separacio



npart = altura*llargada*2

#mal escrit pero diu on han d'estar les coses
for alt = 1:altura
    for llar = 1:llargda
        x_1+llar*a, y_1+alt*sqrt(3), 0

for alt = 1:altura
    for llar = 1:llargda
        x_1+llar*a+a/2, y_1+a*alt*sqrt(3)+a*sqrt(3)/2, 0

#Usar per la distribucio de velocitats en els eixos x i y
np.random.normal(0, sqrt(temperatura/m))

