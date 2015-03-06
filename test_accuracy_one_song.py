import essentia
import matplotlib.pyplot as plt
from matplotlib import *
import essentia.standard as estd	
from pylab import *
from essentia.standard import *
import os
sys.path.append('/Users/Mario/Dropbox/MTG/ChordsDetectionPython/mir_eval-master/')
import mir_eval
import ipdb
import numpy as np



if __name__ == '__main__':
    
    ## FILL WITH THE SONG NAME
    songname = '10_CD2_The_Beatles__05_Sexy_Sadie'

    chordpath = "/Users/Mario/Dropbox/MTG/ChordsDetectionPython/"

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

    #ipdb.set_trace()
    #ticks = np.insert(ticks,0,0)
    _ticks = list(ticks)
    #_ticks.insert(0,0.0)

    chordsdetectionbeats = estd.ChordsDetectionBeats(windowSize = 1.0, hopSize = hopsize)
    
    chords, strength = chordsdetectionbeats(essentia.array(hpcps),essentia.array(_ticks))

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

    GT_list = []

    for i in range(0,len(time_index)):
        time.append(words[time_index[i]]) 
        chords.append(words[chords_index[i]])
    del chords[-1:]

    for i in range(0, len(chords)):
        GT_list.append([time[i],time[i+1],chords[i]])

    generalfolder = chordpath + 'beatles/1tests/chords'
    fileID = '000'
    ext = '.lab'
    typefolder = '/testGT/'
    textfile = 'GT'
    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")
    
    for i in range(0,len(GT_list)):
        f.write(str(GT_list[i][0]) + " " + str(GT_list[i][1]) + " " + str(GT_list[i][2]) + '\n' )
        #print 'writing ' + str(time[i]) + ' ' + str(time[i+1]) + ' ' + str(chords[i]) + ' with i = ' + str(i) 
    f.close()

    ###

    # ESSENTIA ESTIMATION
    ###
    assert(len(_ticks)>len(_chords))

    while(len(_chords)+1<len(_ticks)):
        del _ticks[-1:]

    P_list = []
    for i in range(0, len(_chords)):
        P_list.append([_ticks[i],_ticks[i+1],_chords[i]])

    # Deleting repetitions in the estimation
    P_list2 = []

    P_list2.append([P_list[0][0],P_list[0][1],P_list[0][2]])
    lastChord = P_list[0][2]
    timesRepeated = 0

    for i in range(1,len(P_list)):
        sameChord = lastChord == P_list[i][2]
        if(sameChord == True):
            timesRepeated += 1
            P_list2[i-timesRepeated][1] = P_list[i][1]
        else:
            P_list2.append([P_list[i][0],P_list[i][1],P_list[i][2]])
        lastChord = P_list[i][2]
    
    #P_list = P_list2
    


    typefolder = '/testP/'
    textfile = 'P'
    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")
    
    for i in range(0,len(P_list)):
        if(P_list[i][2].find("m")>0):
            P_list[i][2] = (P_list[i][2])[0] + ":min"
        elif(P_list[i][2].find("aug")>0):
            P_list[i][2] = (P_list[i][2])[0] + ":aug"
        elif(P_list[i][2].find("dim")>0):
            P_list[i][2] = (P_list[i][2])[0] + ":dim"
        else:
            pass
        f.write(str(float(P_list[i][0])) + " " + str(float(P_list[i][1])) + " " + str(P_list[i][2]) + '\n' )
    f.close()


    ###

    #  TEST ACCURACY
    ###
    total = []
    path = generalfolder

    ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(path + "/testGT/GT000.lab")
    est_intervals, est_labels = mir_eval.io.load_labeled_intervals(path + "/testP/P000.lab")
    est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
    
    intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)  
    score = mir_eval.chord.triads(ref_labels, est_labels)
    total.append(score)
    print np.mean(total)












    





