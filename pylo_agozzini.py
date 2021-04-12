# -*- coding: utf-8 -*-

from music import Music

import wave
import sys
import getopt
import numpy as np

def debug(inputpath, outputpath):
    """ Helper function for debugging. """
    music = Music(inputpath)
    print(music)
    music.output(outputpath)
    
def smoothtest(path_in, path_out, windowSize, windowType='hanning', points=100, 
               plot=True, save=True):
    ''' Helper function to speed up the workflow with the smooth filter.
    Gets file from "path_in" and applies smooth(windowSize, windowType)
    May save it in 'path_out', under a new name, or plot the first "points" 
    points.
    '''
    som = Music(path_in)
    som.smooth(windowSize, windowType)
    frames = [int(i) for i in som.frames]
    if plot:
        from matplotlib import pyplot as plt
        plt.plot(frames[:points])
    if save:
        som.output(path_out[:-4] + f'_smooth_{windowType}_{windowSize}.wav')    
  
  
# Code below adapted from 
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=','ofile='])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
            
    # Do something with inputfile and outputfile
    try:
        debug(inputfile, outputfile)
        smoothtest(inputfile, outputfile, windowSize=3)
        
    except FileNotFoundError:
        print(f"Input file '{inputfile}' was not found. I am going to pass")

if __name__ == "__main__":
   main(sys.argv[1:])