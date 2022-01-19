#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 17:39:28 2022

@author: nahuel
"""
import numpy as np
import mne
from libb import *

print("hola mundo!")
#event = mne.make_fixed_length_events()
path_raiz = 'DATA/'
name = 'T21'
path = path_raiz + name

data = np.load(path + '/data.npy')
raw = loadDatos(data, 'ch_names.txt')

#event = mne.make_fixed_length_events(raw, id=1, start=0, stop=None, duration=1.0, first_samp=True, overlap=0.0)
#events = np.load(path +'/events.npy')
labels = np.load(path + '/labels.npy')
#print(labels[:, 0])
print(raw.times)
print(raw.ch_names)
print(raw.n_times)
print(len(raw.times))
print(raw.times[2])