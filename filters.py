# -*- coding: utf-8 -*-

from music import Music

import wave
import sys
import getopt
import numpy as np
from math import cos, pi
from collections import deque, namedtuple

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
    base_level given in the unit interval (preferably in [0.9, 1[ ), represents
    the minimum value the sound will oscilate to. Frequency given in Hertz
    '''
    if base_level > 1:
        print('base_level must be a float between 0 and 1')
    
    def based_cos(x): return (1-base_level)*cos(x) + base_level
    
    tremolo_frames = _modulate(music, based_cos, frequency)
    music.frames = tremolo_frames
    return music


def chopper(music, frequency=1):
    '''Makes the music object sound as if it had been "chopped" '''
    def square_wave(x): return x//pi % 2 # with period 2 pi
    
    chopped_frames = _modulate(music, square_wave, frequency)
    music.frames = chopped_frames
    return music


def chorus(music, amplitude=1, frequency=4, voices=2):
    '''Adds a chorus-like effect to the music object'''
    pass

def delay(music, time_delay, voices):
    '''Adds a delay effect to the music object'''
    pass

def echo(music, time_delay, decay):
    '''Adds echo to the music object'''
    pass


def senoide(music, windowSize=1000):
    '''isolates the leading harmonic at each time window'''
    
    '''Notas:
    Para uma windowSize de tamanho n, conseguimos medir harmônicos de freq.
    frame_rate/n. Para frame_rate=44100, n=1000, temos freq.=44.1 hz (o limite 
    humano é 5hz). Nossa janela n=1000 dura 1/freq ~= 0.022 s
    
    Essa implementação está péssima, bem lenta e usa muita memória.
    Para nosso arquivo-padrão, no meu pc leva ~1 min.
    
    Por enquanto incrementamos a janela frame a frame; futuramente seria melhor
    incrementar de windowSize/2, algo assim (e abandonar o uso de stacks).
    
    Recomendo testar windowSizes menores, 100, 25 e 3 <-- bem esquisito
    
    Não sei bem por que os valores de output não estão oscilando até o zero
    '''

    frames = music.frames #[:1000] # descomente pra deixar bem mais rápido
    
    # margens refletidas para minimizar efeitos de borda
    margemEsquerda = frames[windowSize//2 - 1 : 0 : -1]
    margemDireita = frames[-2 : -windowSize//2 - 1 : -1]
    
    # concatenemos as três
    soundwave = np.r_[margemEsquerda, frames, margemDireita]
   
    # FIFO stack guardando os pontos da janela
    stack = deque([0] + soundwave[:windowSize-1])
    
    # lista onde guardarei cada nota que isolar
    notas = []
    # estrutura para representar as notas: frequência (em unidades windowSize)
    # do maior harmônico e valor (intensidade) total do sinal
    harmonic = namedtuple('haupt_harmonic', ('freq', 'valor'))
    
    # Vamos passar pelo sinal, isolando o harmônico de cada janela.
    # A cada iteração, removemos o primeiro elemento da janela e adicionamos
    # outro na esquerda (FIFO stack, como havia dito)
    for i, val in zip(range(len(frames)), soundwave[windowSize-2:]):
        stack.popleft()
        stack.append(val)
        fourier = np.fft.rfft(stack)
        max_harm = np.argmax(abs(fourier[1:])) + 1
        nota = harmonic(max_harm, fourier[0].real)
        notas.append(nota)
    
    # vamos dar uma olhada nos harmônicos que isolamos
    from matplotlib import pyplot as plt
    # frequências = [i.freq for i in notas]
    # intensidades = [i.valor for i in notas]
    # plt.plot(frequências, intensidades, 'ro')
    # plt.show()
    
    print('vamos ver os primeiros harmônicos que detectamos:')
    for n in notas[:50]:
        print(n)
    
    # faz a inverse fft do harmônico isolado; talvez devesse usar o np mesmo...
    def coseno(frame): # frame é o indice do frame central da janela em questão
        n = notas[frame]
        return n.valor * (cos(2*pi * n.freq/windowSize * frame) + 1)
    
    output = []
    print(f'{len(notas)=}')
    print(f'{len(frames)=}')
    print(f'{len(soundwave[windowSize:])=}')
    print(f'{len(margemDireita)=}')
    
    # escreve a melodia que isolamos, em output
    for f in range(len(frames)):
        output.append(coseno(f))
    
    unit = max(output)
    print(f'antigo max output: {unit}')
    output = [255 * i/unit for i in output]
    print(f'novo max output: {max(output)}')
    print(f'na posição {output.index(max(output))}')
    
    plt.plot(output[:1000])
    plt.plot(frames[:1000])
    plt.legend(('output', 'frames'))
    plt.show()
    music.frames = output
    
        
        
if __name__=='__main__':        
    path = r'C:/users/Gabriel/Music/sim_sala_bim_vocal.wav'
    def path_out(n, path=path): 
        return path[:-4] + f'_novo_{n}.wav'
    
    size = 100
    som = Music(path)
    senoide(som, windowSize=size)
    som.output(path_out(size))
    
