import essentia

import essentia.standard as estd	
#import essentia.streaming

weighttype = "cosine"
bandpreset = False
minfrequency = 40
maxfrequency = 5000

loader = estd.MonoLoader(filename = 'audio/ukelele cfcg.wav')

audio = loader()
from pylab import *
from essentia.standard import *
w = Windowing(type = 'hann')
spectrum = Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum
spectralpeaks = SpectralPeaks()
hpcp = estd.HPCP(weightType = weighttype, bandPreset = bandpreset, minFrequency = minfrequency, maxFrequency = maxfrequency)


specpeaks = []
hpcps = []
framesize = 2048
hopsize = 1024

# t_ind = 10
# frame = audio[t_ind*44100 : t_ind*44100 + framesize]
# spec = spectrum(w(frame))

mintempo = 30
maxtempo = 220
degaraBTalgo = estd.BeatTrackerDegara()
ticks = degaraBTalgo(audio)
	
#for i in range(0,len(ticks))
i = 0
frame = audio[ticks[i]*44100:ticks[i+4]*44100]
specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))
hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
hpcps.append(hpcp_output)


# frame = audio[t_ind*44100 + 0*framesize : t_ind*44100 + 1*framesize]
# spec = spectrum(w(frame))
	
# specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

# hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
# hpcps.append(hpcp_output)

# frame = audio[t_ind*44100 + framesize : t_ind*44100 + 2*framesize]

# specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

# hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
# hpcps.append(hpcp_output)

#imshow(essentia.array(hpcps).T, origin='lower', aspect = 'auto')
#show()

print(size(hpcps))

chordsdetection = estd.ChordsDetection()
chords, strength = chordsdetection((essentia.array(hpcps)))

print(chords)



