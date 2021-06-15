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
    
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print("Inicio...")
        cyton = StreamData.CytonBoard("/dev/ttyUSB0")
        cyton.start_stream()
        while True:
            data = cyton.poll(250)  ## Polling for 250 samples
            print(data.shape)
            time.sleep(1)  ## Updating the window in every one second
        cyton.stop_stream()
    except ServiceExit:
        cyton.stop_stream()
        print("Fin...")
        sys.exit()

if __name__ == "__main__":
    main()