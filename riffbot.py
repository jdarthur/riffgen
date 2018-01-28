import pyaudio
import wave
import sys
import numpy as np
import math
import time
import sounddevice as sd
import math
import random

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
def create_attackdecay(start_decibels, end_decibels, length):
	"""
	create a smaller array to control attack/decay in
	the complete amplitude array. 

	It will smoothly ramp decibels which correlated to a 
	logarithmic increase/decrease in amplitude I believe.
	"""

	inc = (start_decibels - end_decibels) * (1 / length)
	decibels = start_decibels
	ar = []
	for i in range(0, length) :
		decibels = decibels - inc
		vol = math.pow(10, decibels/20)
		ar.append(vol)
	return ar

def create_ampl_array(leng, rate, decayfactor) :
	"""
	Create an array to control amplitude in the sample

	This will use a fixed attack length (1/64 of leng * rate). 
		Might rework this part if it matters
	Decay is variable based on decayfactor [0.0 : 1.0)
	I'm using this decay to do different articulations
		i.e. staccato has a decay factor of about .8
	"""
	amplitude_array = []
	high_db= 0
	inaudible_db = -200

	#attack phase
	attack_length = int(leng * rate / 64)
	att = create_attackdecay(inaudible_db, high_db, attack_length)

	#decay phase
	decay_length = int(leng * rate * decayfactor)
	dec = create_attackdecay(high_db, inaudible_db, decay_length)

	for i in range(0, leng * rate) :
		if(i < attack_length) :
			amplitude_array.append(att[i])
		elif(leng * rate - i < decay_length) :
			amplitude_array.append(dec[decay_length - (leng * rate) + i])
		else :
			amplitude_array.append(math.pow(10, high_db))
	return amplitude_array

"""
i = 0
small = []
for a in ar :
	if( i % 100 == 0) : 
		small.append(a)
		#pass
	i += 1
#print(small)

import matplotlib.pyplot as plt

plt.plot(small)

plt.xlabel('time (s)')
plt.ylabel('AMPLITUDE')
plt.grid(True)
plt.show()

"""


def createSample(leng, rate, ampl_array, f = 440) :
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
	samples = np.multiply(samples, ampl_array)

	return samples

def createNote(note, octave, leng=1, articulation='regular', rate=rate) :
	"""
	Create an array of a musical note from a given
	note, octave, and length.
	Articulation is used to specify staccato, legato, etc.

	TODO: add a length field like 
		quarter note, eighth note, sixteenth, etc 

	"""
	f = frequencies[note.upper()]
	adjustfactor = math.pow(2, octave - 4)
	f = f * adjustfactor
	ampl_arr = articulations[articulation]
	note = createSample(leng, int(rate), ampl_arr, f)
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

"""
Temporary articulations dict for eight notes
Will have to rework this part
"""
articulations = {
	'regular' : create_ampl_array(1, 10000, .7),
	'staccato' : create_ampl_array(1, 10000, .80),
	'legato' :	create_ampl_array(1, 10000, .625),
	'staccatissimo' : create_ampl_array(1, 10000, .90),
}



#master sequence that I add samples to. silent
beats = 4
positions = beats * 8
big = create_empty_sample(beats, rate)

#create random sequence of (note, octave, position) tuples
randseq = rand_sequence(12, 16)

"""
#Play a scale (for testing)
sequence = [("c", 4), ('d', 4), ("e", 4), ('f', 4),
			("g", 4), ('a', 4), ("b", 4), ('c', 5),
]
i = 0
seq2 = []
for note, octave in sequence :
	seq2.append((note, octave, i))
	i += 2
"""


#create samples based on our random sequence
#store in list
samples = []
#for note, octave, pos in randseq:
for note, octave, pos in randseq:
	n = createNote(note, octave, leng=.5, 
		articulation='staccato'), pos
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
