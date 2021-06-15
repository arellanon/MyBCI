#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 00:58:00 2021

@author: nahuel
"""
import argparse
import time
import numpy as np
import pandas as pd
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
def main():
    BoardShim.enable_dev_board_logger()
    # use my board for demo
    params = BrainFlowInputParams()
    params.serial_port = '/dev/ttyUSB0'
    board = BoardShim(BoardIds.CYTON_BOARD.value, params)
    board.prepare_session()     # some question
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    #data = board.get_current_board_data(20)  # get 20 latest data points dont remove them from internal buffer
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()
    # demo how to convert it to pandas DF and plot data
    #eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_DAISY_BOARD.value)
    print(data.shape)
    print(data[0])
    print(data[1])
    print(type(data[1,0]))
    #df = pd.DataFrame(np.transpose(data))
    #df = pd.DataFrame(data)
    #print('Data From the Board')
    #print(df.head(10))
    # demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
    np.savetxt("foo3.csv", np.transpose(data), fmt='%10.7f', delimiter=",")
    #DataFilter.write_file( data, 'test.csv', 'w')  # use 'a' for append mode
    
    #restored_data = DataFilter.read_file('test.csv')
    #restored_df = pd.DataFrame(np.transpose(restored_data))
    #print('Data From the File')
    #print(restored_df.head(10))
if __name__ == "__main__":
    main()