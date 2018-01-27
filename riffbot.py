import pyaudio
import wave
import sys
import numpy as np
import math
import time
import sounddevice as sd
import math
import random
import matplotlib

"""
DONE: 
	bing
	variable length
	multibing
	tones
	random sequence
TODO:
	different length for notes
		quarter, eighth, whole, whatever
	better volume dropoff
		more legato
	note weighting
		-might base it on last note played
	random seeds to recreate a riff
	improve note addition for performance
		- numpy probably has a method like this already
"""



"""
===================================================
					CONSTANTS
===================================================
"""

"""
Frequencies of musical notes. 
This is octave 4 i.e. middle C I believe

C5 is created by doubling the frequency
	-> 523.252 Mhz

Might need longer floats here to be accurate at lower
octaves. We'll see. 

"""
frequencies = { 
'C'   :	261.626,
'C#'  : 277.183,
'D'   :	293.665,
'D#'  : 311.127,
'E'   :	329.628,
'F'   :	349.228,
'F#'  :	369.994,
'G'   :	391.995,
'G#'  : 415.305,
'A'   :	440,
'A#'  :	466.164,
'B'   :	493.883,
'rest' : 0,  
}
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


def createSample(leng, rate, f = 440) :
	"""
	create an array representing a sample

	a playable sound essentially. 
	args:
		leng: number of frames
		rate: sampleing rate
		f: frequency in MHz
	
	This gives you a sine wave array that sounds nice enough
	Maybe I need more waveforms

	it's kind of a 'boop' sound at the moment due to how I am 
	calculating the amplitude.

	Got to figure out a way to make this configurable
		i.e. longer notes

	"""

	samples = (np.sin(2*np.pi*np.arange(rate*leng)*f/rate)).astype(np.float32)
	decibels = 0
	negdec = 200
	for i in range(0, len(samples)) :
		inc =  negdec * (1 / (leng * rate))
		decibels = decibels - inc
		vol = math.pow(10, decibels/20)
		samples[i] = samples[i] * vol
		if( i % 200 == 0) : 
			pass
	return samples

def createNote(note, octave, leng=1, rate=rate) :
	"""
	Create an array of a musical note from a given
	note, octave, and length

	TODO: add a length field like 
		quarter note, eighth note, sixteenth, etc 

	"""
	f = frequencies[note.upper()]
	adjustfactor = math.pow(2, octave - 4)
	f = f * adjustfactor
	note = createSample(leng, int(rate), f)
	return note


def create_empty_sample(leng, rate) :
	"""	
	Create an empty sample of 'leng' seconds at sampling rate 'rate'
	"""
	samples = (np.empty(rate*leng)).astype(np.float32)
	return samples

def add_sample(sample1, sample2, position, num_pos, rate=rate) :
	"""
	Add a sample to a bigger sample.
	will check for overrun (and skip if encountered). 
	
	Just adding amplitude values together in a loop here.
	The if-else is to avoid clipping on polyphony
		if there is already nonzero data here, average the 2 amplitudes
		maybe theres a better solution

	"""
	rets = sample1
	startpoint = int(len(sample1) / num_pos) * position
	if(startpoint + len(sample2)) > len(sample1) :
		print("overrun. not adding")
		return rets
	for i in range (0, len(sample2)) :
		if rets[startpoint + i] == 0 :
			rets[startpoint + i] += sample2[i]
		else :
			rets[startpoint + i] = (rets[startpoint + i] + sample2[i]) / 2

	return rets


def rand_sequence(items, num_positions) :
	"""
	Create a random sequence of (note, octave, postion) tuples
		
	args:
		items: number of items in the sequence
		num_positions: number of quantized postions to put a note at
			i.e. 4 beats using 16th notes will give 16 positions
	
	Currently using a Major C scale
	TODO:
		Different base scales
			- pass in optional arg note_pool or something
		note weighting
			- e.g. prefer C > E-G > D-F > A > B based on percentages
			- not currently implemented because random.choice doesn't
			have the weighting method in python 3.4 (it's in 3.6)
			- might just right my own method to do it
		Might restructure the position part
			- thinking about looping through the positions
			sequentially and adding a note/rest
			- weight the next note off of what we just played

	"""


	choices = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
	weights = [ 10,  10,  10,  10,  10,  10,  10]
	seq = []
	for i in range(0, items) :
		note = random.choice(choices)
		pos = random.randint(0, num_positions)
		seq.append((note, 4, pos))
	return seq


"""
===================================================
				  SCRIPT PART
===================================================
"""



#timing. using this to evaluate performance
timer = time.time()


#master sequence that I add samples to. silent
beats = 4
positions = beats * 8
big = create_empty_sample(beats, rate)

#create random sequence of (note, octave, position) tuples
randseq = rand_sequence(12, 16)

#create samples based on our random sequence
#store in list
samples = []
for note, octave, pos in randseq :
	n = createNote(note, octave, leng=.5), pos
	samples.append(n)

#add samples to the master sample
for samp, pos in samples :
	big = add_sample(big, samp, pos, positions)

#second timer to calculate elapsed time
t2 = time.time() - timer
print("runtime: {0}s".format(t2))


#actually play our sample
sd.play(big, rate)

time.sleep(beats)
