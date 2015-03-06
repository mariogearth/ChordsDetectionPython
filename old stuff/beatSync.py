import essentia as e
import essentia.standard as estd
import scipy.io as io
from scipy.io import wavfile

name = 'ukelele cfcg'
audiofile = 'audio/' + name + '.wav'
silencefile = 'audio/3minutesilence.wav'

sound = estd.MonoLoader(filename=audiofile)
silence = estd.MonoLoader(filename=silencefile)
beat = estd.BeatTrackerDegara()

# RUN ANALYSIS
#=============
audio = sound()
ticks = beat(audio)
calcOnsets = estd.AudioOnsetsMarker(onsets=ticks)
audio2 = silence() 
ticksToFile = calcOnsets(audio2)
#final = ticksToFile[0:len(audio)] + audio
#wavfile.write('audio/withTick_' + name + '.wav', 44100, ticksToFile)
wavfile.write('audio/ticksFor_' + name + '.wav', 44100, ticksToFile)