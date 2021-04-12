# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 20:09:43 2021

@author: Leonardo A. Lessa & Gabriel Solis
"""
import wave
import sys
import getopt

class Music:
    
    """ Opens .wav file at filepath and saves its parameters and frames. """
    def __init__(self, filepath):
        with wave.open(filepath,mode='rb') as inputfile:
            self.params = inputfile.getparams()
            nframes = self.params[3]
            self.frames = inputfile.readframes(nframes)

    """ TODO: convolutes the music with a filter function. Need to learn about
    audio processing techniques, such as windowing.
    """
    def convolve(self, f, windowSize):
        pass

    """ Saves another .wav. file at filepath with the parameters and frames of
    the object.
    """
    def output(self, filepath):
        with wave.open(filepath, 'w') as outputfile:
            outputfile.setparams(self.params)
            outputfile.writeframes(self.frames)

""" Helper function for debugging. """
def debug(inputpath, outputpath):
    music = Music(inputpath)
    print(music.params)
    print(music.frames[:10])
    music.output(outputpath)
    
""" Code below adapted from 
https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""
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
    try:
        debug(inputfile, outputfile)
    except FileNotFoundError:
        print(f"Input file '{inputfile}' was not found. I am going to pass")

if __name__ == "__main__":
   main(sys.argv[1:])
