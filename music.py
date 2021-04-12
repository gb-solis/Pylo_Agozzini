# -*- coding: utf-8 -*-

import wave
import sys
import getopt
import numpy as np


class Music:
    
    def __init__(self, filepath):
        """ Opens .wav file at filepath and saves its parameters and frames."""
        with wave.open(filepath, mode='rb') as inputfile:
            self.params = inputfile.getparams()
            nframes = self.params.nframes
            self.frames = inputfile.readframes(nframes)

    def convolve(self, f, windowSize):
        """ TODO: convolutes the music with a filter function. Need to learn 
        about audio processing techniques, such as windowing.
        """
        pass

      
    # adapted from https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
    def smooth(self, windowSize, windowType='hanning'):
        ''' Smoothens the input signal via convolution, using a window of size
        windowSize, and of tipe windowType'''
        windowType = windowType.lower()
        soundwave = np.array([int(frame) for frame in self.frames])
        
        if soundwave.size < windowSize:
            raise ValueError("Input vector needs to be bigger than window "
                             "size.")
        if windowSize < 3:
            return soundwave
    
        if windowType not in ['flat', 'hanning', 'hamming', 'bartlett', 
                          'blackman']:
            raise ValueError("Window is one of 'flat', 'hanning', 'hamming',"
                " 'bartlett', 'blackman'")
        
        # margens refletidas para minimizar efeitos de borda
        margemEsquerda = soundwave[windowSize-1 : 0 : -1]
        margemDireita = soundwave[-2 : -windowSize-1 : -1]
        
        # concatenemos as três
        s = np.r_[margemEsquerda, soundwave, margemDireita]
        
        if windowType == 'flat': # moving-average
            w = np.ones(windowSize,'d')
        else:
            w = eval('np.' + windowType + '(windowSize)')
    
        outputRaw = np.convolve(w/w.sum(), s, mode='valid') 
        
        # removemos as margens, transformamos elems. em inteiros
        output = [int(frame) for frame in 
                  outputRaw[windowSize//2 - 1 : -windowSize//2]]
        
        # transformamos lista em bytes. TEM de ser aplicado à lista toda,
        # por algum motivo.
        self.frames = bytes(output)
      
      
    def output(self, filepath):
        """ Saves another .wav. file at filepath with the parameters and frames
        of the object.
        """
        with wave.open(filepath, 'w') as outputfile:
            outputfile.setparams(self.params)
            outputfile.writeframes(self.frames)
    
    def __repr__(self):
        return str(self.params)

    def __len__(self):
        return self.params.nframes
    
    def __getitem__(self, index):
        return self.frames[index]

