#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 19:12:06 2021

@author: nahuel
"""
import signal
import sys
import time
import StreamDataPlayback as StreamData
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

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


def set_plot(ax, p, fontsize=12):
    n = len(p)
    left= 0 if n < 750 else  n - 750
    right = n
    ax.plot(p, color='blue')    
    ax.set_xlim(left= left, right=right)
"""
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)
"""

def main():
    data=None
    #Inicializamos variables
    p1 = [] 
    p2 = []
    p3 = []
    p4 = []
    #plt.close('all')
    plt.ion()
    fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(nrows=4)
    fig.set_size_inches(10, 10)
    
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print("Inicio...")
        cyton = StreamData.CytonBoard("foo3.csv")
        cyton.start_stream()
        while True:
            ## Devuelve como minimo 250 samples
            data_stream = cyton.poll(250)  
            ## Append (columna) stream a data 
            ## ch x sample (23 x N)
            data = data_stream if data is None else np.append(data, data_stream, axis=1)
            while len(data[0]) > 250:
                #Nos quedamos con 250 samples en Y
                y = data[:, :250]
                
                #Seleccionamos solo el channel 1 para graficar
                p1.extend(y[1,:])
                p2.extend(y[2,:])
                p3.extend(y[3,:])
                p4.extend(y[4,:])
                
                set_plot(ax1, p1)
                set_plot(ax2, p2)
                set_plot(ax3, p3)
                set_plot(ax4, p4)
                plt.tight_layout()
                plt.pause(0.1)
                
                #Dejamos el resto de samples para la proxima iteracion
                data=data[:, 250:]
                #pausa de 1 seg.
                time.sleep(1)
        cyton.stop_stream()
    except ServiceExit:
        cyton.stop_stream()
        print("Fin...")
        sys.exit()

if __name__ == "__main__":
    main()