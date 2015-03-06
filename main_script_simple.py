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


folder = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/simple-test/'
print 'folder = ' + repr(folder)
folder_audio = folder + 'audio/'
AU = os.listdir(folder_audio)
if '.DS_Store' in AU:
    AU.remove('.DS_Store')

print 'Saving the predicted files...'

predictPath = folder + 'P/'
joinrepeated = False
algo = 'ChordsDetectionBeats'
    
for i in range(len(AU)):

    fileID = '{0:03d}'.format(i)
    chords_P, ticks_P = TF.doPrediction(AU[i],folder_audio,algo)

    TF.savePredictedFile(chords_P,ticks_P,fileID,predictPath,joinrepeated)

stop = timeit.default_timer()
timePrediction = stop - start
print 'timePrediction = ' + repr(timePrediction)

folder_GT = folder + 'GT/'
folder_P = predictPath


GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
	GT.remove('.DS_Store')
P = os.listdir(folder_P)
if '.DS_Store' in P:
	P.remove('.DS_Store')

print 'Doing the mir_eval.chord evaluation...'

totalMU = []; totalSTD = []; mismatched = []

for i in range(len(GT)):
	ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(folder_GT + AU[i][:-4] + '.txt')
	est_intervals, est_labels = mir_eval.io.load_labeled_intervals(folder_P  + 'P-' + '{0:03d}'.format(i) + '.txt')
	est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
	intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)

	score = mir_eval.chord.triads(ref_labels, est_labels)
	wrong = []
	for j, value in enumerate(score):
		if value == -1:
			mismatched.append([ref_labels[j],est_labels[j]])

	totalMU.append(np.mean(score))
	totalSTD.append(np.std(score))

print ' MU = ' + str(np.mean(totalMU))
print 'STD = ' + str(np.std(totalSTD)) 
print 'number of mismatched chords = ' + str(len(mismatched))

# csvname = '/Users/Mario/Dropbox/MTG/ChordsDetectionPython/simple-test/outMismatched.csv'
# writer = csv.writer(open(csvname, 'wb'), dialect='excel')
# for item in mismatched:
#      writer.writerows([item,])



