# -*- coding: utf-8 -*-

from music import Music

import wave
import sys
import getopt
import numpy as np

def convolve(music, f, windowSize):
    """ TODO: convolutes the music with a filter function. Need to learn 
    about audio processing techniques, such as windowing.
    """
    pass

  
# adapted from https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
def smooth(music, windowSize, windowType='hanning'):
    ''' Smoothens the input signal via convolution, using a window of size
    windowSize, and of tipe windowType'''
    windowType = windowType.lower()
    soundwave = np.array([int(frame) for frame in music.frames])
    
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
    return bytes(output)
    