import essentia
import matplotlib.pyplot as plt
from matplotlib import *
import essentia.standard as estd	
from pylab import *
from essentia.standard import *

def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

if __name__ == '__main__':

    chordpath = "/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/"

    weighttype = "cosine"
    bandpreset = False
    minfrequency = 40
    maxfrequency = 5000

    loader = estd.MonoLoader(filename = chordpath + 'beatles/audio/01_Please_Please_Me__08_Love_Me_Do.flac')

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
    with open(chordpath + 'beatles/chords/01_Please_Please_Me__08_Love_Me_Do.chords' , 'r') as f:
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
    typefolder = '/ref/'
    textfile = 'ref'
    fileID = '001'
    ext = '.lab'

    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")

    for i in range(0,len(chords)):
        f.write(str(time[i]) + " " + str(time[i+1]) + " " + chords[i] + '\n' )
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

    for i in range(0,len(chords)):
        if(_chords[i].find("m")>0):
            _chords[i] = _chords[i][0] + ":min"
            f.write(str(_ticks[i]) + " " + str(_ticks[i+1]) + " " + _chords[i] + '\n' )
        else:
            f.write(str(_ticks[i]) + " " + str(_ticks[i+1]) + " " + _chords[i] + '\n' )
    f.close()


    ###

    #  TEST ACCURACY
    ###
    import os
    import mir_eval

    path = generalfolder

    ref_intervals, ref_labels = mir_eval.io.load_intervals(path + "/ref/ref001.lab")
    est_intervals, est_labels = mir_eval.io.load_intervals(path + "/est/est001.lab")
    est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
    intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)  
    score = mir_eval.chord.sevenths_inv(ref_labels, est_labels, intervals)
    total.append(score)












    





