import essentia
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import *
import essentia.standard as estd	
from pylab import *
from essentia.standard import *

weighttype = "cosine"
bandpreset = False
minfrequency = 40
maxfrequency = 5000

loader = estd.MonoLoader(filename = 'beatles/audio/01_Please_Please_Me__08_Love_Me_Do.flac')

audio = loader()

w = Windowing(type = 'hann')
spectrum = Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum
spectralpeaks = SpectralPeaks()
hpcp = estd.HPCP(weightType = weighttype, bandPreset = bandpreset, minFrequency = minfrequency, maxFrequency = maxfrequency)


specpeaks = []
hpcps = []
framesize = 2048
hopsize = 512

# t_ind = 10
# frame = audio[t_ind*44100 : t_ind*44100 + framesize]
# spec = spectrum(w(frame))

mintempo = 30
maxtempo = 220
degaraBTalgo = estd.BeatTrackerDegara()
ticks = degaraBTalgo(audio)
	
for frame in FrameGenerator(audio, frameSize = framesize, hopSize = hopsize):
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

figure
plt.imshow(essentia.array(hpcps).T, origin='lower', aspect = 'auto')
plt.show()
plt.close()

size(hpcps)

chordsdetection = estd.ChordsDetection(windowSize = 1.0, hopSize = hopsize)
chords, strength = chordsdetection(essentia.array(hpcps),ticks)



