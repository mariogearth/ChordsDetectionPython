import essentia

import essentia.standard as estd	
#import essentia.streaming

weighttype = "gaussian"
bandpreset = False
minfrequency = 220
maxfrequency = 500

loader = estd.MonoLoader(filename = 'audio/Norwegian Wood split.mp3')

audio = loader()
from pylab import *
from essentia.standard import *
w = Windowing(type = 'hann')
spectrum = Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum
spectralpeaks = SpectralPeaks()
hpcp = estd.HPCP(weightType = weighttype, bandPreset = bandpreset, minFrequency = minfrequency, maxFrequency = maxfrequency)

t_ind = 13.9
frame = audio[t_ind*44100 : t_ind*44100 + 1024]
spec = spectrum(w(frame))

#plot(spec)
#show()

#hpcp.configure(weightType = "gaussian")
#hpcp.configure(bandPreset = False)
#hpcp.configure(minFrequency = 20)
#hpcp.configure(maxFrequency = 1000)

specpeaks = []
framesize = 1024
hopsize = 512

hpcps = []

K = 4
std = 15/((K+1)/2)


#for i in range(1,K)
	
for frame in FrameGenerator(audio, frameSize = framesize, hopSize = hopsize):
    specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

	# should I re-configure HPCP here to perform in the new gaussian interval?

    hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
    hpcps.append(hpcp_output)


imshow(essentia.array(hpcps).T, origin='lower', aspect = 'auto')
show()

