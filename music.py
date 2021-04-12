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

