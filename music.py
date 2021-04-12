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
            self._frames = inputfile.readframes(nframes) # hidden property
            self.duration = self.params.nframes/self.params.framerate # seconds
      
    def output(self, filepath):
        """ Saves another .wav. file at filepath with the parameters and frames
        of the object.
        """
        with wave.open(filepath, 'w') as outputfile:
            outputfile.setparams(self.params)
            outputfile.writeframes(self._frames)
    
    def __repr__(self):
        return str(self.params)

    def __len__(self):
        return self.params.nframes
    
    def __getitem__(self, index):
        return self.frames[index]
    
    @property
    def frames(self):
        # takes byte-like frames and presents them as integers between 0, 255
        byte_frames = self._frames
        return [round(f) for f in byte_frames]
    
    @frames.setter 
    def frames(self, int_frames):
        # takes a list of integer frames and stores them as byte-like frames
        if any(not isinstance(f, int) for f in int_frames):
            raise ValueError('The frames must be represented by integers')
        if max(int_frames) > 255:
            raise ValueError('The frames must be between 0 and 255')
        
        self._frames = bytes(int_frames)
        self.params.nframes = len(self._frames)
