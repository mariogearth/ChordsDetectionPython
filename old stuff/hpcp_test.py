import essentia

import essentia.standard as estd
#import essentia.streaming

loader = essentia.standard.MonoLoader(filename = '../test/audio/dmajor.mp3')

audio = loader()

from pylab import *

plot(audio[1*44100:2*44100])
show()

from essentia.standard import *
w = Windowing(type = 'hann')
spectrum = Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum
spectralpeaks = SpectralPeaks()
hpcp = HPCP()

frame = audio[2*44100 : 2*44100 + 1024]
spec = spectrum(w(frame))

plot(spec)
show()

specpeaks = []
framesize = 2048
hopSize = 1024

hpcps = []

# Matlab-like
#for fstart in range(0, len(audio)-frameSize, hopSize):
#    frame = audio[fstart:fstart+framesize]
#    specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))

# Essentia-like
for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    specpeaks_mX, specpeaks_f = spectralpeaks(spectrum(w(frame)))
    hpcp_output = hpcp(specpeaks_mX, specpeaks_f)
    hpcps.append(hpcp_output)
    
imshow(essentia.array(hpcps).T, origin='lower', aspect = 'auto')
show()

# specpeaks = essentia.array(specpeaks).T
# imshow(specpeaks[1:,:], aspect = 'auto')
# show()
# print specpeaks


