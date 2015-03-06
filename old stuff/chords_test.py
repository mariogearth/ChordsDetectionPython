import essentia

from pylab import *
import essentia.standard as estd	
#import essentia.streaming

Chords = ['C','F','G','C','C','Am','Dm','G','C','G','Am','F','C','F','G','C']
Key = 'C'
Scale = 'major'

cdescriptor = estd.ChordsDescriptors()

#descriptor.configure(chords = Chords, key = Key, scale = Scale)

#descriptor.input("chords").set

histogram, cnr, ccr, ckey, cscale = cdescriptor(Chords,Key,Scale)

