#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 21:37:02 2021

@author: nahuel
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 20:39:10 2021

@author: nahuel
"""
import os
from os import listdir
from os.path import isfile, isdir

#mne
import mne
from mne.decoding import CSP
from mne.channels import read_layout
from mne.channels import make_standard_montage
from mne.preprocessing import (create_eog_epochs, create_ecg_epochs,
                               compute_proj_ecg, compute_proj_eog)


def ls1(path):
    lista = []
    if os.path.exists(path) and os.path.isdir(path):
        lista = [obj for obj in listdir(path) if isdir(path + obj)]
    return lista

def filtro(lista, inicial):
    result=[]
    for a in lista:
        if a[:len(inicial)]==inicial:
            result.append( int(a[1:]) )
    return result

def new_name(path, inicial):
    #Calculamos directorio enumerado    
    directorios = ls1(path)
    #filtramos los directorios que empiezan con T
    lista = filtro(directorios, inicial)
    num=1
    if lista:
        num = max(lista) + 1
    name = inicial + str(num)
    return name

def loadDatos(data_cnt, ch_name_file):
    #Seteamos frecuencia de muestreo Cyton
    freq=250
    #Se carga la matriz de datos
    #data_cnt=data_cnt.transpose()
    print("data_cnt: ", data_cnt.shape)
    
    #Se carga los nombre de los caneles
    ch_names_txt = open(ch_name_file, "r")
    ch_names = ch_names_txt.read().split(',')
    for i in range(len(ch_names)):
        ch_names[i]=ch_names[i].strip()
    info = mne.create_info(ch_names, freq, 'eeg')
    raw = mne.io.RawArray(data_cnt, info, first_samp=0, copy='auto', verbose=None)
    
    return raw