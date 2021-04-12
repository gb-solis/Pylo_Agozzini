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
            nframes = self.params.nframes
            self.frames = inputfile.readframes(nframes)

    """ TODO: convolutes the music with a filter function. Need to learn about
    audio processing techniques, such as windowing.
    """
    def convolve(self, f, windowSize):
        pass

      
    # adapted from https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
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
        
        # margens refletidas para minimizar efeitos de borda
        margemEsquerda = soundwave[windowSize-1 : 0 : -1]
        margemDireita = soundwave[-2 : -windowSize-1 : -1]
        
        s = np.r_[margemEsquerda, soundwave, margemDireita] # concatenemos as três
        
        if window == 'flat': # moving-average
            w = np.ones(windowSize,'d')
        else:
            w = eval('np.' + window + '(windowSize)')
    
        outputRaw = np.convolve(w/w.sum(), s, mode='valid') 
        # removemos as margens e transformamos elems. em inteiros
        output = [int(frame) for frame in 
                  outputRaw[windowSize//2 - 1 : -windowSize//2]]
        # transformamos lista em bytes. TEM de ser aplicado à lista toda,
        # por algum motivo.
        self.frames = bytes(output)
      
      
    """ Saves another .wav. file at filepath with the parameters and frames of
    the object.
    """
    def output(self, filepath):
        with wave.open(filepath, 'w') as outputfile:
            outputfile.setparams(self.params)
            outputfile.writeframes(self.frames)
    
    def __repr__(self):
        return str(self.params)

    def __len__(self):
        return self.params.nframes
    
    def __getitem__(self, index):
        return self.frames[index]

    
""" Helper function for debugging. """
def debug(inputpath, outputpath):
    music = Music(inputpath)
    print(music)
    music.output(outputpath)
    
def smoothtest(path_in, path_out, windowSize, windowType='hanning', points=100, 
               plot=True, save=True):
    ''' gets file from "path_in" and applies smooth(windowSize, windowType)
    If "save" is set to True, a .wav file is saved in "path_out", but under a new name.
    If "plot" is set to True, the first "points" points are plotted.
    '''
    som = Music(path_in)
    som.smooth(windowSize, windowType)
    frames = [int(i) for i in som.frames]
    if plot:
        from matplotlib import pyplot as plt
        plt.plot(frames[:points])
    if save:
        som.output(path_out[:-4] + f'_smooth_{windowType}_{windowSize}.wav')    
  
  
""" Code below adapted from 
https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""
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
