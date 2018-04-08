import numpy as np
import math
import time
import sounddevice as sd
from bigsample import BigSample
from classes.note import Note
from classes.measure import Measure


"""
global sampling rate
I'm using 20k because it sounds alright and is faster
to create arrays than like 44100 or something
"""
rate = 20000

"""
===================================================
					METHODS
===================================================
"""

def createSample(frequency, length, articulation='regular', rate=rate) :
	"""
	Create an array of a musical note from a given
	note, octave, and length.
	Articulation is used to specify staccato, legato, etc.

	TODO: add a length field like 
		quarter note, eighth note, sixteenth, etc 

	"""
	samples = (np.sin(2*np.pi*np.arange(rate*length)*frequency/rate)).astype(np.float32)
	#samples = np.multiply(samples, ampl_arr)

	return samples


#timing. using this to evaluate performance
timer = time.time()

"""
Temporary articulations dict for eight notes
Will have to rework this part
"""

G = Note(tone="g", octave=2, notelength="quarter")
A = Note(tone="a", octave=2, notelength="eighth")
m = Measure()
m.add(G, 0)
m.add(A, 8)
print(m.note_dict)

samples = []
for key in m.note_dict :
	freq = m.note_dict[key][0]
	length = m.note_dict[key][1]
	tup = (createSample(freq, length), key)
	samples.append(tup)

#master sequence that I add samples to. silent
beats = 4
positions = m.MAX_POSITION + 1
big = BigSample(beats, rate)

#add samples to the master sample
for samp, pos in samples :
	big.add_inplace(samp, pos, positions)

#second timer to calculate elapsed time
t2 = time.time() - timer
print("runtime: {0}s".format(t2))

time.sleep(1)
#actually play our sample
bytes1 = big.get_bytes()
sd.play(bytes1, rate, blocking=True)