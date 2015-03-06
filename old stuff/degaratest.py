

# Test on Degara's Beat Tracker Essentia Algorithm

import essentia
import essentia.standard as estd

mintempo = 30
maxtempo = 220

loader = estd.MonoLoader(filename = 'audio/Yesterday.mp3')

audio = loader()

degaraBTalgo = estd.BeatTrackerDegara()

ticks = degaraBTalgo(audio)
