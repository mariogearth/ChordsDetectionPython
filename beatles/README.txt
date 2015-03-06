name: The Beatles dataset

contact: Sebastian Böck 

description: all songs of The Beatles dicography with annotations

creator: Chris Harte

reference: http://isophonics.net/content/reference-annotations-beatles
           chris_harte_phd_thesis.pdf

annotations: structural segmentation, keys, harmony, beats, tempo

content:
audio/                    original audio files in .flac format
annotations/beats/        beat annotations
annotations/chords/       chord annotations
annotations/keys/         key annotations
annotations/segmentation/ structural segmentation annotations
annotations/tempo/        tempo annotations (median of inter beat interval)
annotations/original/     the original annotations
annotations/giantsteps/   annotations in the GiantSteps project format
annotations/.git/          git repo with annotations

NOTE: this set is not checked manually and thus should be used with caution!
      The tempo annotations have been generated automatically. If a song has
	  multiple tempi, only the strongest is considered.

The audio files are the original Queen Mary University ones, the annotations
have been downloaded from from the site mentioned in the reference section.

The annotations should be aligned to the audio, if not there's a tool which
should be able to align them (however, I had very mixed results with the beat
annotations on audio from another source).
http://www.ee.columbia.edu/ln/rosa/matlab/beatles_fprint/

To convert the audio files to .wav use 'flac -d *.flac'

If you find this dataset useful, think about donating beer to the contact
person :)