import chords_textfiles as TF
import os
import numpy as np
import sys
sys.path.append('/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/mir_eval-master/')
import mir_eval





# #~~~~~~~~~~~~~ Save text files with predictions from Essentia
# folder_audio = '/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/beatles/audio'
# AU = os.listdir(folder_audio)
# if '.DS_Store' in AU:
#     AU.remove('.DS_Store')

# for i in range(len(AU)):
	
# 	fileID = '{0:03d}'.format(i)
# 	chords_P, ticks_P = TF.doPrediction(AU[i])

# 	TF.savePredictedFile(chords_P,ticks_P,fileID)

# #~~~~~~~~~~~~~ Save SINGLE text file with predictions
# i = 1
# fileID = '{0:03d}'.format(i)
# chords_P, ticks_P = TF.doPrediction(AU[i])
# TF.savePredictedFile(chords_P,ticks_P,fileID)


# #~~~~~~~~~~~~~ Save text files with Ground Truth Annotations
# folder_chords = '/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/beatles/chords'
# CH = os.listdir(folder_chords)
# if '.DS_Store' in CH:
# 	CH.remove('.DS_Store')

# for i in range(len(CH)):
# 	fileID = '{0:03d}'.format(i)
# 	TF.saveGroundTruthTextFile(CH[i],fileID)

# #~~~~~~~~~~~~~ Save SINGLE text file with GTA
# i = 1
# fileID = '{0:03d}'.format(i)
# TF.saveGroundTruthTextFile(CH[i],fileID)

# #~~~~~~~~~~~~~ Copying evaluationChords.py (angelfaraldo) I do the evaluation between 2 folders

folder_GT = '/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/beatles/1tests/chords/ref/'
folder_P = '/Users/Mario/Dropbox/MTG/essentia-master/src/python/chords_detector/beatles/1tests/chords/est/'

GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')
P = os.listdir(folder_P)
if '.DS_Store' in P:
    P.remove('.DS_Store')


total = []
totalMU = []
totalSTD = []
for i in range(len(GT)):
    ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(folder_GT + 'ref' + '{0:03d}'.format(i) + '.lab')
    est_intervals, est_labels = mir_eval.io.load_labeled_intervals(folder_P  + 'est' + '{0:03d}'.format(i) + '.lab')
    est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
    intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)
    score = mir_eval.chord.majmin(ref_labels, est_labels)
    
    totalMU.append(np.mean(score))
    totalSTD.append(np.std(score))
    
#print np.mean(total)
#print np.std(total)  