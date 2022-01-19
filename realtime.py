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
        data_aux = None
        time.sleep(1)  ## Updating the window in every one second
        samples= 501
        while True:
            
            poll_sample = (samples * 2) - resta
            data = cyton.poll(poll_sample)  ## Polling for samples

            #Seleccionamos los canales egg
            #data = data[1:9, :]
            data_new = data[:,: poll_sample ]
            
            if data_aux is None:
                data_new = data_new                
            else:
                data_new = np.append(data_aux, data_new, axis=1)
                        
            data_aux = data[:, poll_sample :]
            
            resta = data_aux.shape[1]
            
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
            
            data_raw1 = np.array( [ data_raw[:,:samples] ] )
            data_raw2 = np.array( [ data_raw[:, samples//2 : samples + samples//2 ] ] )
            data_raw3 = np.array( [ data_raw[:,samples:] ])
            #data_raw = np.array([data_raw])  #array de 3 dimensiones
            
            #data = np.array([data_out])
            result1=model.predict(data_raw1)
            result2=model.predict(data_raw2)
            result3=model.predict(data_raw3)
            #print("data_cnt: ", data_cnt.shape)
            #print(result, " - ", data_raw.shape, " - ", data.shape, "-", data_new.shape," - ", data_aux.shape, " - ", data_aux.shape[1], ' - ', resta , '-', datetime.fromtimestamp(ts) )
            print( data_raw.shape, " - ", result1, " - ", data_raw1.shape, '-', result2, " - ", data_raw2.shape, '-', result3, " - ", data_raw3.shape,' - ', resta , '-', datetime.fromtimestamp(ts) )
            #print( data_raw.shape, " - ",  data_raw1.shape, '-', data_raw3.shape,' - ', resta , '-', datetime.fromtimestamp(ts) )
            
            #time.sleep(1)  ## Updating the window in every one second
            
        cyton.stop_stream()
    except ServiceExit:
        cyton.stop_stream()
        print("Fin...")
        sys.exit()

if __name__ == "__main__":
    main()