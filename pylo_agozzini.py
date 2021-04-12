# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 20:09:43 2021

@author: Leonardo A. Lessa & Gabriel Solis
"""
import wave
import sys, getopt
import numpy as np

class Music:
    
    # Opens .wav file at filepath and saves its parameters and frames
    def __init__(self, filepath):
        inputfile = wave.open(filepath,mode='rb')
        self.params = inputfile.getparams()
        nframes = self.params[3]
        self.frames = inputfile.readframes(nframes)
        inputfile.close()

    # TODO: convolutes the music with a filter function. Need to learn about
    # audio processing techniques, such as windowing
    def convolve(self, f, windowSize):
        pass
    
    def smooth(self, windowSize, window='hanning'):
        window = window.lower()
        
        soundwave = np.array([int(frame) for frame in self.frames])
        
        if soundwave.size < windowSize:
            raise ValueError("Input vector needs to be bigger than window "
                             "size.")
    
        if windowSize < 3:
            return soundwave
    
        if window not in ['flat', 'hanning', 'hamming', 'bartlett', 
                          'blackman']:
            raise ValueError("Window is one of 'flat', 'hanning', 'hamming',"
                " 'bartlett', 'blackman'")
    
        soundwaveA = soundwave[windowSize-1 : 0 : -1]
        soundwaveB = soundwave[-2 : -windowSize-1 : -1]
        s = np.r_[soundwaveA, soundwave, soundwaveB]
        #print(len(s))
        
        if window == 'flat': #moving average
            w = np.ones(windowSize,'d')
        else:
            w = eval('np.' + window + '(windowSize)')
    
        output = np.convolve(w/w.sum(), s, mode='valid')
        
        self.frames = bytes(output)
        
        # if bits:
        #     return np.array([bytes(frame) for frame in output])
        # else:
        #     return output

    # Saves another .wav. file at filepath with the parameters and frames of
    # the object
    def output(self, filepath):
        outputfile = wave.open(filepath, 'w')
        outputfile.setparams(self.params)
        outputfile.writeframes(self.frames)
        outputfile.close()

# Helper function for debugging
def debug(inputpath, outputpath):
    music = Music(inputpath)
    print(music.params)
    print(music.frames[:10])
    music.output(outputpath)
    
def smoothtest(path_in, path_out, windowSize, windowType='hanning', points=100, 
               plot=True, save=True):
    ''' gets file from path and applies smooth(windowSize, windowType)
    If "save_n" is given, .wav file is saved as path +'_smooth_<save_n>.wav'
    Plots the first "points" points, if "plot" is set to True
    '''
    som = Music(path_in)
    som.smooth(windowSize, windowType)
    frames = [int(i) for i in som.frames]
    if plot:
        from matplotlib import pyplot as plt
        plt.plot(frames[:points])
    if save:
        som.output(path_out[:-4] + f'_smooth_{windowType}_{windowSize}.wav')
    
# Code below adapted from https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    # Do something with inputfile and outputfile
    debug(inputfile, outputfile)
    
    smoothtest(inputfile, outputfile, windowSize=3)

if __name__ == "__main__":
   main(sys.argv[1:])