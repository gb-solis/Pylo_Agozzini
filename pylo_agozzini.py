# -*- coding: utf-8 -*-

from music import Music
from filters import smooth

import wave
import sys
import getopt
import numpy as np

def copyCommand(inputpath, outputpath):
    """ Copies music from inputpath to outputpath. """
    music = Music(inputpath)
    music.output(outputpath)
    
def smoothCommand(path_in, path_out, windowSize, windowType='hanning', points=100, 
               plot=True, save=True):
    ''' Helper function to speed up the workflow with the smooth filter.
    Gets file from "path_in" and applies smooth(windowSize, windowType)
    May save it in 'path_out', under a new name, or plot the first "points" 
    points.
    '''
    music = Music(path_in)
    music.frames = smooth(music, int(windowSize), windowType) # Need to change this!
    frames = [int(i) for i in music.frames]
    if plot:
        from matplotlib import pyplot as plt
        plt.plot(frames[:points])
    if save:
        music.output(path_out[:-4] + f'_smooth_{windowType}_{windowSize}.wav')    
    
# Code below adapted from 
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    inputfile = ''
    outputfile = ''
    helpMessage = 'test.py -i <inputfile> -o <outputfile> <command> [<args>]'
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=','ofile='])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpMessage)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
    
    if not args:
        print('Pass some command')
        print(helpMessage)
        sys.exit(2)
    
    try:
        if args[0] == 'copy':
            copyCommand(inputfile, outputfile)
        elif args[0] == 'smooth':
            windowSize = int(args[1])
            smoothCommand(inputfile, outputfile, windowSize)
        else:
            print(f'I do not recognize the command {args[0]}')
            print(helpMessage)
    except FileNotFoundError:
        print(f"Input file '{inputfile}' was not found")
        print(helpMessage)

if __name__ == "__main__":
   main(sys.argv[1:])