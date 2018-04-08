import numpy as np
import math
import time
import sounddevice as sd
from bigsample import BigSample
from classes.note import Note
from classes.measure import Measure
from utils import choose_weighted
import random


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

def random_measure(notecount) :
	measure = Measure()
	tonechoices = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
	toneweights = [ 30,  10,  30,  10,  30,  10,  10]

	lenchoices = ['quarter', 'eighth', 'sixteenth']
	lenweights = [ 30,  50,  10]
	seq = []

	for i in range(0, notecount) :
		tone = choose_weighted(tonechoices, toneweights)
		notelength = choose_weighted(lenchoices, lenweights)
		note = Note(tone=tone, octave=2, notelength=notelength)
		position = random.randint(0, int(measure.MAX_POSITION/2)) * 2
		measure.add(note, position)
	return measure

def add_to_bigsample(measure, bigsample) :
	samples = []
	for key in m.note_dict :
		freq = m.note_dict[key][0]
		length = m.note_dict[key][1]
		tup = (createSample(freq, length), key)
		samples.append(tup)

	#add samples to the master sample
	for samp, pos in samples :
		big.add_inplace(samp, pos, m.MAX_POSITION + 1)

#timing. using this to evaluate performance
timer = time.time()

m = random_measure(12)

big = BigSample(m.beats, rate)
add_to_bigsample(m, big)

#second timer to calculate elapsed time
t2 = time.time() - timer
print("runtime: {0}s".format(t2))

#actually play our sample
bytes1 = big.get_bytes()
sd.play(bytes1, rate, blocking=True)