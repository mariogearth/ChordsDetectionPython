
from essentia.standard import *
import essentia.standard as estd    
from pylab import *
import numpy

def doPrediction(name,audiopath,algo,zeroFirstTick=False):

    loader = estd.MonoLoader(filename = audiopath + name)
    audio = loader()
    
    weighttype = "cosine"
    bandpreset = False
    minfrequency = 40
    maxfrequency = 5000
    harmonix = 10

    w = Windowing(type = 'hann'); spectrum = Spectrum(); spectralpeaks = SpectralPeaks()
    
    hpcp = estd.HPCP(harmonics = harmonix, weightType = weighttype, bandPreset = bandpreset, minFrequency = minfrequency, maxFrequency = maxfrequency)

    specpeaks = []; hpcps = []
    framesize = 8192
    hopsize = 1024

    for frame in FrameGenerator(audio, frameSize = framesize, hopSize = hopsize):
        specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

        hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
        hpcps.append(hpcp_output)

    if(algo=='ChordsDetection'):
        chordsdetection = estd.ChordsDetection(windowSize = 1.0, hopSize = hopsize)
        chords, strength = chordsdetection(essentia.array(hpcps))
        ticks = numpy.array(range(len(hpcps)))*hopsize/44100.0
        return list(chords), list(ticks)
        
    elif(algo=='ChordsDetectionBeats'):
        mintempo = 30; maxtempo = 220
        degaraBTalgo = estd.BeatTrackerDegara()
        ticks = degaraBTalgo(audio)
        #ticks = numpy.array(range(len(hpcps)))*hopsize/44100.0
        
        if(zeroFirstTick==True):
            _ticks.insert(0,0.0)
        else:
            pass
        chordsdetection = estd.ChordsDetectionBeats(hopSize = hopsize, numHarmonics = harmonix+1)
        chords, strength = chordsdetection(essentia.array(hpcps),essentia.array(ticks))
        return list(chords), list(ticks)
    else:
        return 'Error: incorrect algorithm name'

def savePredictedFile(_chords,_ticks,fileID,predictPath,joinRepeated=True):
    
    #assert(len(_ticks)>len(_chords))
    if(len(_ticks)==len(_chords)):
        del _chords[-1]
        
    while(len(_chords)+1<len(_ticks)):
        del _ticks[-1:]

    P_list = []
    for i in range(0, len(_chords)):
        P_list.append([_ticks[i],_ticks[i+1],_chords[i]])

    # Deleting repetitions in the estimation
    if(joinRepeated==True):
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
        
        P_list = P_list2
    else:
        pass
    
    textfile = 'P-'
    path = predictPath + textfile + fileID + '.txt'
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
    
def saveGroundTruthTextFile(name,fileID):

    chordpath = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/'
    words = []
    with open(chordpath + 'beatles/chords/' + name , 'r') as f:
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
    ext = '.lab'
    typefolder = '/GT/'
    textfile = 'GT-'
    path = generalfolder + typefolder + textfile + fileID + ext
    f = open(path, "w")
    
    for i in range(0,len(chords)):
        f.write(str(time[i]) + " " + str(time[i+1]) + " " + str(chords[i]) + '\n' )
    f.close()











    





