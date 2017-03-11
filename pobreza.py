#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 08:40:24 2017

@author: gonesbuyo
"""

import pandas as pd
# import numpy as np
# import csv as csv

filename1 = "C:\\Users\\b o r j a\\Desktop\\Hack4good\\9bf31c7ff062936a96d3c8bd1f8f2ff3\\hack4good_dwells.csv"
filename2 = "C:\\Users\\b o r j a\\Desktop\\Hack4good\\9bf31c7ff062936a96d3c8bd1f8f2ff3\\hack4good_antenas.csv"

output = "C:\\Users\\b o r j a\\Desktop\\Hack4good\\9bf31c7ff062936a96d3c8bd1f8f2ff3\\pobreza.csv"

# n = 1122 #numero de municipios

diccionario = {}

w2g = 0.256/1.656
w3g = 1.4/1.656

estancias = []
personas = []

names1 = ['dwells','people']
names2 = ['3g_traf_dl', '3g_traf_ul', '3g_completadas', '3g_no_completadas', '2g_traf_dl', '3g_traf_ul', '2g_completadas', '2g_no_completadas']

data1 = pd.read_csv(filename1, header=0)
data2 = pd.read_csv(filename2, header=0)

# print data1
# print data2
    
def media(data, columns):
    for column in columns:
        medias = data.groupby('cod_mpio').agg("mean")
        munList = list(medias.index)
        
        for mun in munList:
            mun2 = str(mun)
            try:
                diccionario[mun2][column] = medias.loc[mun,column]
            except:
                diccionario[mun2] = {}
                diccionario[mun2][column] = medias.loc[mun,column]
    return munList

def returnValFloat(i, j):
    try:
        return float(diccionario[i][j])
    except:
        return 0.
    
def returnValInt(i, j):
    try:
        return round(float(diccionario[i][j]),0)
    except:
        return 0
                
media(data1, names1)
munList = media(data2, names2)

for i in range(len(munList)):
    munList[i] = str(munList[i])

for mun in munList:
    diccionario[mun]['consumo3g'] = returnValFloat(mun,'3g_traf_dl') + returnValFloat(mun,'3g_traf_ul')
    diccionario[mun]['consumo2g'] = returnValFloat(mun,'2g_traf_dl') + returnValFloat(mun,'2g_traf_ul')
 
    if (returnValInt(mun,'3g_completadas') + returnValInt(mun,'3g_no_completadas')) > 0:
        diccionario[mun]['c3g'] = returnValInt(mun,'3g_completadas') / (returnValInt(mun,'3g_completadas') + returnValInt(mun,'3g_no_completadas'))
    else:
        diccionario[mun]['c3g'] = 0
    
    if (returnValInt(mun,'2g_completadas') + returnValInt(mun,'2g_no_completadas')) > 0:
        diccionario[mun]['c2g'] = returnValInt(mun,'2g_completadas') / (returnValInt(mun,'2g_completadas') + returnValInt(mun,'2g_no_completadas'))
    else:
        diccionario[mun]['c2g'] = 0
        
    try:
        diccionario[mun]['indiceRiqueza'] = (((diccionario[mun]['consumo3g']*(1-diccionario[mun]['c3g'])*w3g) + (diccionario[mun]['consumo2g']*(1-diccionario[mun]['c2g'])*w2g))*diccionario[mun]['dwells'])/diccionario[mun]['people']
    except:
        diccionario[mun]['indiceRiqueza'] = 0.

results = open(output,"w")
results.write("cod_mpio,pobreza")

for i in sorted(diccionario.keys()):
    if 'indiceRiqueza' in diccionario[i].keys():
        if diccionario[i]['indiceRiqueza'] > 0:
            text = "\n" + i + "," + str(diccionario[i]['indiceRiqueza'])
        else:
            text = "\n" + i + "," + str(0.0)
    else:
        text = "\n" + i + "," + str(0.0)
        
    results.write(text)

results.close()


