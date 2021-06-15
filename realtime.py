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
    name_model = 'T10'
    #path modelo
    path_model = path_raiz + name_model
    #Cargamos modelo
    model = joblib.load(path_model + '/model.pkl')
    
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print("Inicio...")
        cyton = StreamData.CytonBoard("/dev/ttyUSB0")
        cyton.start_stream()
        while True:
            data = cyton.poll(250)  ## Polling for 250 samples
            #timestamp
            ts=data[22][0]
            #Seleccionamos los canales egg
            data = data[1:9, :]
            
            raw=loadDatos(data, 'ch_names.txt')
            #Seleccionamos los canales a utilizar
            raw.pick_channels(['P3', 'P4', 'C3', 'C4','P7', 'P8', 'O1', 'O2'])
            
            #Seteamos la ubicacion de los canales segun el 
            montage = make_standard_montage('standard_1020')
            raw.set_montage(montage)
            
            # Se aplica filtros band-pass
            raw.filter(low_freq, high_freq, fir_design='firwin', skip_by_annotation='edge')
            data = raw.get_data()
            
            data1= data[:,:251]
            
            data = np.array([data1])
            #data = np.array([data_out])
            result=model.predict(data)
            
            print(result)
            
            time.sleep(1)  ## Updating the window in every one second
            
        cyton.stop_stream()
    except ServiceExit:
        cyton.stop_stream()
        print("Fin...")
        sys.exit()

if __name__ == "__main__":
    main()