import chords_textfiles as TF
import os
import numpy as np
import sys
sys.path.append('/Users/Mario/Dropbox/MTG/ChordsDetectionPython/mir_eval-master/')
import mir_eval
import csv
import timeit
import pdb

# #~~~~~~~~~~~~~ Save text files with predictions from Essentia
start = timeit.default_timer()

folder_audio = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/beatles/audio'
AU = os.listdir(folder_audio)
if '.DS_Store' in AU:
    AU.remove('.DS_Store')

print 'Saving the predicted files...'

typefolder = 'P_master_JR/'
joinrepeated = True
algo = 'ChordsDetection'
framesWindow = 84
framesize=512
fs=44100.0
j = 0    
for i in range(len(AU)):
    
    j = j + 1
    print '%d/180' % j
    fileID = '{0:03d}'.format(i)
    chords_P = TF.doPrediction(AU[i],algo)
    chords2 = []; time2 = [] 
        
    for i in range(framesWindow,len(chords_P),framesWindow):        
        if(i >= len(chords_P)):
            break
        chords2.append(chords_P[i])
        time2.append(float("{0:.4f}".format(i*framesize/fs)))
        
    time2.insert(0,0.0)
        
    TF.savePredictedFile(chords2,time2,fileID,typefolder,joinrepeated)

stop = timeit.default_timer()
timePrediction = stop - start
print 'timePrediction = ' + repr(timePrediction)

# # #~~~~~~~~~~~~~ Save SINGLE text file with predictions
# # i = 1
# # fileID = '{0:03d}'.format(i)
# # chords_P, ticks_P = TF.doPrediction(AU[i])
# # TF.savePredictedFile(chords_P,ticks_P,fileID)


# # #~~~~~~~~~~~~~ Save text files with Ground Truth Annotations
# folder_chords = '/Users/Mario/Dropbox/MTG/essentia-master/src/python/ChordsDetectionPython/beatles/chords'
# CH = os.listdir(folder_chords)
# if '.DS_Store' in CH:
# 	CH.remove('.DS_Store')

# print 'Saving the annotations files...'
# for i in range(len(CH)):
# 	fileID = '{0:03d}'.format(i)
# 	TF.saveGroundTruthTextFile(CH[i],fileID)

# # #~~~~~~~~~~~~~ Save SINGLE text file with GTA
# # i = 1
# # fileID = '{0:03d}'.format(i)
# # TF.saveGroundTruthTextFile(CH[i],fileID)

#~~~~~~~~~~~~~ Copying evaluationChords.py (angelfaraldo) I do the evaluation between 2 folders

folder_GT = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/beatles/1tests/chords/GT/'
folder_P = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/beatles/1tests/chords/' + typefolder


GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
	GT.remove('.DS_Store')
P = os.listdir(folder_P)
if '.DS_Store' in P:
	P.remove('.DS_Store')

print 'Doing the mir_eval.chord.majmin evaluation...'

totalMU = []; totalSTD = []; wrongChords = []

for i in range(len(GT)):
	ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(folder_GT + 'GT-' + '{0:03d}'.format(i) + '.lab')
	est_intervals, est_labels = mir_eval.io.load_labeled_intervals(folder_P  + 'P-' + '{0:03d}'.format(i) + '.lab')
	est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
	intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)

	score = mir_eval.chord.majmin(ref_labels, est_labels)
	wrong = []
	for j, value in enumerate(score):
		if value == -1:
			wrongChords.append([ref_labels[j],est_labels[j]])

	totalMU.append(np.mean(score))
	totalSTD.append(np.std(score))

print ' MU = ' + str(np.mean(totalMU))
print 'STD = ' + str(np.std(totalSTD)) 
print 'number of wrongChords = ' + str(len(wrongChords))

csvname = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/beatles/1tests/chords/' + typefolder + 'outWrong-' + typefolder[:-1] + '.csv'
writer = csv.writer(open(csvname, 'wb'), dialect='excel')
for item in wrongChords:
     writer.writerows([item,])



