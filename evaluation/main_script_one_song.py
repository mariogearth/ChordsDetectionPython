import essentia
import matplotlib.pyplot as plt
from matplotlib import *
import essentia.standard as estd	
from pylab import *
from essentia.standard import *
import os
sys.path.append('/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/mir_eval-master/')
import mir_eval



if __name__ == '__main__':

    songname = '01_Please_Please_Me__08_Love_Me_Do'

    chordpath = "/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/"

    weighttype = "cosine"
    bandpreset = False
    minfrequency = 40
    maxfrequency = 5000

    loader = estd.MonoLoader(filename = chordpath + 'beatles/audio/' + songname + '.flac')
    audio = loader()

    w = Windowing(type = 'hann')
    spectrum = Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum
    spectralpeaks = SpectralPeaks()
    hpcp = estd.HPCP(weightType = weighttype, bandPreset = bandpreset, minFrequency = minfrequency, maxFrequency = maxfrequency)

    specpeaks = []
    hpcps = []
    framesize = 2048
    hopsize = 512

    for frame in FrameGenerator(audio, frameSize = framesize, hopSize = hopsize):
        specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

        hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
        hpcps.append(hpcp_output)

    mintempo = 30
    maxtempo = 220
    degaraBTalgo = estd.BeatTrackerDegara()
    ticks = degaraBTalgo(audio)

    chordsdetection = estd.ChordsDetection(windowSize = 1.0, hopSize = hopsize)
    chords, strength = chordsdetection(essentia.array(hpcps),ticks)

    _ticks = list(ticks)
    _chords = list(chords)
    _strength = list(strength)

    # Until last line what it have been done is Essentia estimation of chords
    # Next Step: saving chords and time in text files

    # REFERENCE ANNOTATIONS
    ###
    words = []
    with open(chordpath + 'beatles/chords/' + songname + '.chords' , 'r') as f:
        for line in f:
            for word in line.split():
               words.append(word)

    time_index  = range(0,len(words),2)
    chords_index = range(1,len(words)+1,2)

    chords = []
    time = []
    pre_chord = []

    for i in range(0,len(time_index)):
        time.append(words[time_index[i]]) 
        chords.append(words[chords_index[i]])
    del chords[-1:]

    generalfolder = chordpath + 'beatles/1tests/chords'
    fileID = '001'
    ext = '.lab'
    typefolder = '/ref/'
    textfile = 'ref'
    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")
    
    for i in range(0,len(chords)):
        f.write(str(time[i]) + " " + str(time[i+1]) + " " + str(chords[i]) + '\n' )
        #print 'writing ' + str(time[i]) + ' ' + str(time[i+1]) + ' ' + str(chords[i]) + ' with i = ' + str(i) 
    f.close()

    ###

    # ESSENTIA ESTIMATION
    ###
    assert(len(_ticks)>len(_chords))

    while(len(_chords)+1<len(_ticks)):
        del _ticks[-1:]

    typefolder = '/est/'
    textfile = 'est'
    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")
    
    for i in range(0,len(_chords)):
        if(_chords[i].find("m")>0):
            _chords[i] = _chords[i][0] + ":min"
        else:
            pass
        f.write(str(float(_ticks[i])) + " " + str(float(_ticks[i+1])) + " " + str(_chords[i]) + '\n' )
    f.close()


    ###

    #  TEST ACCURACY
    ###

    path = generalfolder

    ref_intervals, ref_labels = mir_eval.io.load_intervals(path + "/ref/ref_intervals001.lab")
    est_intervals, est_labels = mir_eval.io.load_intervals(path + "/est/est_intervals001.lab")
    est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
    intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)  
    score = mir_eval.chord.majmin(ref_labels, est_labels, intervals)
    total.append(score)












    





