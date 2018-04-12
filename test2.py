import numpy as np
import math
import time
import sounddevice as sd
from classes.note import Note
from classes.measure import Measure
from classes.riff import Riff
from lib.utils import choose_weighted
import random


"""
===================================================
					METHODS
===================================================
"""

def random_measure(notecount) :
	"""
	create a bunch of random notes in random locations
	"""
	measure = Measure()
	tonechoices = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
	toneweights = [ 50,  10,  10,  10,  10,  10,  10]

	lenchoices = ['quarter', 'eighth', 'sixteenth']
	lenweights = [ 30,  100,  30]
	seq = []

	pos = 0
	for i in range(0, notecount) :
		tone = choose_weighted(tonechoices, toneweights)
		notelength = choose_weighted(lenchoices, lenweights)
		note = Note(tone=tone, octave=2, notelength=notelength)
		pos += note.len
		if(pos + note.len <= measure.MAX_POSITION) :
			measure.add(note, pos)
	return measure


#timing. using this to evaluate performance
timer = time.time()

m = random_measure(12)
m2 = random_measure(12)

r = Riff(Measures=[m, m2])
big = r.create_sample()
bytes1 = big.get_bytes()

#second timer to calculate elapsed time
t2 = time.time() - timer
print("runtime: {0}s".format(t2))

#actually play our sample
sd.play(bytes1, big.rate, blocking=True)