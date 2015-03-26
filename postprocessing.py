from essentia.standard import *
import essentia.standard as estd    
from pylab import *
import numpy as np
import pdb

def sliding_window(chords, ticks):
    
    unique = ['A'    , 'A#'    , 'B'    , 'C'    , 'C#'    , 'D'    , 'D#'    , 'E'    , 'F'    , 'F#'    , 'G'    , 'G#'    ,
              'A:min', 'A#:min', 'B:min', 'C:min', 'C#:min', 'D:min', 'D#:min', 'E:min', 'F:min', 'F#:min', 'G:min', 'G#:min',
              'A:dim', 'A#:dim', 'B:dim', 'C:dim', 'C#:dim', 'D:dim', 'D#:dim', 'E:dim', 'F:dim', 'F#:dim', 'G:dim', 'G#:dim',
              'A:aug', 'A#:aug', 'B:aug', 'C:aug', 'C#:aug', 'D:aug', 'D#:aug', 'E:aug', 'F:aug', 'F#:aug', 'G:aug', 'G#:aug']
    print len(ticks), len(chords)
    #pdb.set_trace()
    P_list = []; P_list2 = []; _chords = []; _ticks = []
    for k in range(len(chords)):
        P_list.append([ticks[k],ticks[k+1],chords[k]])
    
    i = 0
    while(i<len(P_list)-5):
        w = np.zeros(48)
        w[unique.index(chords[i  ])] += 1
        w[unique.index(chords[i+1])] += 1
        w[unique.index(chords[i+2])] += 1
        w[unique.index(chords[i+3])] += 1
        w[unique.index(chords[i+4])] += 1
        
        ind = np.argmax(w)
        P_list2.append([ticks[i],ticks[i+1],unique[ind]])
        i += 1
    
    for j in range(len(P_list2)):
        _chords.append(P_list2[j][2])
        _ticks.append(P_list2[j][0])
    
    _ticks.append(P_list2[len(P_list2)-1][1])
    
    return _chords, _ticks

def remove_redundancy(chords, ticks)
    
        
        
    
    
    
    
        
    
        
    