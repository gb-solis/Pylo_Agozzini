# -*- coding: utf-8 -*-

from music import Music

import wave
import sys
import getopt
import numpy as np
from math import cos, pi

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
    soundwave = np.array([round(frame) for frame in music.frames])
    
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
    output = outputRaw[windowSize//2 - 1 : -windowSize//2]
    
    music.frames = output
    return music


def _modulate(music, envelope, frequency):
    '''Helper-function which modulates the input signal according to the 
    given envelope function, up to changes in amplitude and frequency.
    envelope is assumed to be periodic of period 2pi
    frequency given in Hertz.
    '''
    framerate = music.params.framerate
    w = frequency * 2*pi / framerate # conversion factor
    
    frames = music.frames
    mod_frames = [envelope(w*n) * frame for n, frame in enumerate(frames)]
    return mod_frames
    


def tremolo(music, frequency=1, base_level=0.95):
    '''Simple tremolo-effect', modulating the input signal's amplitude.
    base_level given in unit interval (preferably [0.9, 1[), represents
    the minimum value the sound will oscilate to. Frequency given in Hertz
    '''
    if base_level > 1:
        print('base_level must be a float between 0 and 1')
    
    def based_cos(x): return (1-base_level)*cos(x) + base_level
    
    tremolo_frames = _modulate(music, based_cos, frequency)
    music.frames = tremolo_frames
    return music


def chopper(music, frequency=1):
    def square_wave(x): return x//pi % 2 # with period 2 pi
    
    chopped_frames = _modulate(music, square_wave, frequency)
    music.frames = chopped_frames
    return music


def chorus(music, amplitude=1, frequency=60, voices=2):
    '''Adds a chorus-like effect to the music object'''
    pass