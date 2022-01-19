#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 00:30:40 2021

@author: nahuel
"""
import signal
import sys
import time
import StreamData

import numpy as np
import os
from datetime import datetime
from os import listdir
from os.path import isfile, isdir
from libb import *
import joblib

#mne
import mne
from mne.decoding import CSP
from mne.channels import read_layout
from mne.channels import make_standard_montage
from mne.preprocessing import (create_eog_epochs, create_ecg_epochs,
                               compute_proj_ecg, compute_proj_eog)

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    # print("[EXCEPTION] exception raised", e)
    pass

## Keyboard Interrupt handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")
    raise ServiceExit

def main():
    
    low_freq, high_freq = 7., 30.
    path_raiz = 'DATA/'
    name_model = 'T20'
    #path modelo
    path_model = path_raiz + name_model
    #Cargamos modelo
    model = joblib.load(path_model + '/model.pkl')
    
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print("Inicio...")
        cyton = StreamData.CytonBoard("/dev/ttyUSB0")
        cyton.start_stream()
        resta = 0
        data2 = None
        time.sleep(1)  ## Updating the window in every one second
        samples= 501
        while True:
            data = cyton.poll(samples - resta)  ## Polling for samples

            #Seleccionamos los canales egg
            #data = data[1:9, :]
            data1= data[:,: (samples - resta) ]
            
            if data2 is None:
                data_new = data1                
            else:
                data_new = np.append(data2, data1, axis=1)
            
            #data_new = data1                
            data2 = data[:, (samples - resta):]
            
            resta = data2.shape[1]
            
            #timestamp
            ts=data_new[22][0]
            #Seleccionamos los canales egg
            data_new = data_new[1:9, :]
            
            raw=loadDatos(data_new, 'ch_names.txt')
            #Seleccionamos los canales a utilizar
            raw.pick_channels(['P3', 'P4', 'C3', 'C4','P7', 'P8', 'O1', 'O2'])
            
            #Seteamos la ubicacion de los canales segun el 
            montage = make_standard_montage('standard_1020')
            raw.set_montage(montage)
            
            # Se aplica filtros band-pass
            raw.filter(low_freq, high_freq, fir_design='firwin', skip_by_annotation='edge', verbose='critical')
            
            
            data_raw = raw.get_data(verbose='critical') #array de 2 dimensiones
            data_raw = np.array([data_raw])  #array de 3 dimensiones
            
            #data = np.array([data_out])
            result=model.predict(data_raw)
            #print("data_cnt: ", data_cnt.shape)
            print(result, " - ", data_raw.shape, " - ", data.shape, " - ", data1.shape, " - ", data2.shape, " - ", data2.shape[1], ' - ', resta , '-', datetime.fromtimestamp(ts) )
            
            #time.sleep(1)  ## Updating the window in every one second
            
        cyton.stop_stream()
    except ServiceExit:
        cyton.stop_stream()
        print("Fin...")
        sys.exit()

if __name__ == "__main__":
    main()